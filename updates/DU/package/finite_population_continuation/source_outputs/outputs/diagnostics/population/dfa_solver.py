#!/usr/bin/env python3
"""Exact rational finite-population DFA solver and succinct coupling compiler.

The graph approximates arbitrary correlated inputs with identical supplied
one-coordinate marginals. No independence or stationary-process constraint is
imposed. All arithmetic affecting certificates uses integers or Fraction.
"""
from __future__ import annotations

import argparse
from collections import deque
from fractions import Fraction
from hashlib import sha256
from math import comb, lcm
from pathlib import Path
import random
import sys


def frac(value):
    if isinstance(value, float):
        raise ValueError("Use integer or rational strings, never JSON floats")
    return Fraction(value)


def fs(value):
    return str(Fraction(value))


def compositions(total, cells):
    """Every weak composition once; only cells*log(total+1) iterator storage."""
    if total < 0 or cells < 1:
        raise ValueError("Nonnegative total and positive cell count required")
    values = [0]*cells
    values[-1] = total
    while True:
        yield tuple(values)
        remaining, position = values[-1], cells-2
        while position >= 0 and remaining == 0:
            remaining += values[position]
            position -= 1
        if position < 0:
            return
        values[position] += 1
        for j in range(position+1, cells-1):
            values[j] = 0
        values[-1] = remaining-1


def bits(mask):
    while mask:
        bit = mask & -mask
        yield bit.bit_length() - 1
        mask ^= bit


class Model:
    def __init__(self, spec):
        self.spec = spec
        self.states = tuple(spec["states"])
        self.alphabet = tuple(spec["alphabet"])
        if not self.states or not self.alphabet:
            raise ValueError("Nonempty explicitly listed states and alphabet required")
        if len(set(self.states)) != len(self.states) or len(set(self.alphabet)) != len(self.alphabet):
            raise ValueError("State and letter names must be distinct")
        self.d = len(self.states)
        self.start = self.states.index(spec["start"])
        mu_all = tuple(frac(spec["marginal"][a]) for a in self.alphabet)
        if min(mu_all) < 0 or sum(mu_all) != 1:
            raise ValueError("Marginals must be a rational probability law")
        self.support = tuple(a for a, p in zip(self.alphabet, mu_all) if p)
        self.mu = tuple(p for p in mu_all if p)
        self.m = len(self.mu)
        self.alpha = min(self.mu)
        # Validate the whole supplied table, including letters of zero mass.
        for s in self.states:
            for a in self.alphabet:
                if spec["transition"][s][a] not in self.states:
                    raise ValueError("Unknown transition destination")
        self.delta = tuple(tuple(self.states.index(spec["transition"][s][a])
                                 for a in self.support) for s in self.states)
        self.target = tuple(frac(spec["target"][s]) for s in self.states)
        if min(self.target) < 0 or sum(self.target) != 1:
            raise ValueError("Target must be a rational probability law")
        self.Q = spec["population"]
        if not isinstance(self.Q, int) or isinstance(self.Q, bool) or self.Q < 1:
            raise ValueError("Population must be a positive integer")
        self.M = lcm(*(p.denominator for p in self.mu))
        self.u = tuple(int(p * self.M) for p in self.mu)
        self.umin = min(self.u)
        self.F = self.d * self.M * self.M
        self.branch_den = self.Q * self.umin + self.d * self.M
        self.uniform_seed_den = self.M * self.branch_den
        self.beta = Fraction(self.d * self.M, self.branch_den)
        self.r = Fraction(self.d, 2 * self.Q)
        self.initial = tuple(self.Q if s == self.start else 0 for s in range(self.d))

    def tv(self, histogram):
        return sum(abs(Fraction(x, self.Q) - p)
                   for x, p in zip(histogram, self.target)) / 2

    def allocation(self, flat):
        if len(flat) != self.d * self.m or min(flat) < 0 or sum(flat) != self.Q:
            raise ValueError("Invalid nonnegative integer allocation")
        rows = tuple(sum(flat[s*self.m:(s+1)*self.m]) for s in range(self.d))
        counts = tuple(sum(flat[s*self.m+a] for s in range(self.d)) for a in range(self.m))
        if any(abs(Fraction(c) - self.Q*p) > self.d for c, p in zip(counts, self.mu)):
            raise ValueError("Allocation violates letter discrepancy budget")
        dest = [0] * self.d
        for s in range(self.d):
            for a in range(self.m):
                dest[self.delta[s][a]] += flat[s*self.m+a]
        qnum = tuple(self.Q*self.umin*u + self.d*self.M*u - self.M*self.umin*c
                     for u, c in zip(self.u, counts))
        if min(qnum) < 0 or sum(qnum) != self.F:
            raise AssertionError("Filler is not a probability law")
        for a in range(self.m):
            assert ((1-self.beta)*Fraction(counts[a], self.Q)
                    + self.beta*Fraction(qnum[a], self.F)) == self.mu[a]
        return rows, tuple(dest), counts, qnum

    def letter(self, qnum, seed):
        if not 0 <= seed < self.F:
            raise ValueError("Quantile seed outside its finite range")
        end = 0
        for a, mass in enumerate(qnum):
            end += mass
            if seed < end:
                return a
        raise AssertionError("Missing quantile interval")

    def slot_data(self, flat):
        source, dest, _, _ = self.allocation(flat)
        offsets = [sum(source[:s]) for s in range(self.d)]
        dest_next = [sum(dest[:s]) for s in range(self.d)]
        permutation = [-1] * self.Q
        letters = [-1] * self.Q
        for s in range(self.d):
            cursor = offsets[s]
            for a in range(self.m):
                t = self.delta[s][a]
                for _ in range(flat[s*self.m+a]):
                    permutation[cursor] = dest_next[t]
                    letters[cursor] = a
                    cursor += 1
                    dest_next[t] += 1
        assert sorted(permutation) == list(range(self.Q))
        return permutation, letters


class PopulationGraph:
    def __init__(self, model, max_allocations=2_000_000):
        self.model = model
        Q, d, m = model.Q, model.d, model.m
        self.H = comb(Q+d-1, d-1)
        self.B = comb(Q+d*m-1, d*m-1)
        if max_allocations and self.B > max_allocations:
            raise RuntimeError(f"RESOURCE_LIMIT_UNKNOWN: {self.B} allocation candidates exceed {max_allocations}")
        self.histograms = tuple(compositions(Q, d))
        self.index = {x: i for i, x in enumerate(self.histograms)}
        self.start = self.index[model.initial]
        self.edges = {}
        accepted = 0
        # Each allocation determines its own source. There is no extra H factor.
        for flat in compositions(Q, d*m):
            counts = tuple(sum(flat[s*m+a] for s in range(d)) for a in range(m))
            if any(abs(c*p.denominator-Q*p.numerator) > d*p.denominator
                   for c, p in zip(counts, model.mu)):
                continue
            source, dest, _, _ = model.allocation(flat)
            accepted += 1
            key = (self.index[source], self.index[dest])
            self.edges.setdefault(key, flat)
        self.accepted_allocations = accepted
        self.rows = [0] * self.H
        for x, y in self.edges:
            self.rows[x] |= 1 << y

    def best(self, reachable):
        return min(bits(reachable), key=lambda i: (self.model.tv(self.histograms[i]), i))

    def unbounded(self):
        dummy = self.H
        predecessor = {}
        queue = deque([dummy])
        while queue:
            previous = queue.popleft()
            x = self.start if previous == dummy else previous
            for y in bits(self.rows[x]):
                if y not in predecessor:
                    predecessor[y] = (previous, (x, y))
                    queue.append(y)
        reachable = sum(1 << i for i in predecessor)
        best = self.best(reachable)
        path = []
        current = best
        while current != dummy:
            current, edge = predecessor[current]
            path.append(edge)
        path.reverse()
        assert 1 <= len(path) <= self.H
        return best, path, reachable

    def binary_horizon(self, n):
        if n < 1:
            raise ValueError("Only positive horizons are admitted")
        if n.bit_length() > 500:
            raise RuntimeError("RESOURCE_LIMIT_UNKNOWN: implementation recursion guard at 500 horizon bits")
        powers = [self.rows]
        for _ in range(1, n.bit_length()):
            old = powers[-1]
            new = []
            for row in old:
                combined = 0
                for z in bits(row):
                    combined |= old[z]
                new.append(combined)
            powers.append(new)
        reachable = 1 << self.start
        layers = []
        for level in reversed(range(n.bit_length())):
            if not ((n >> level) & 1):
                continue
            new = 0
            predecessor = {}
            for x in bits(reachable):
                row = powers[level][x]
                for y in bits(row & ~new):
                    predecessor[y] = x
                new |= row
            reachable = new
            layers.append((level, predecessor))
        best = self.best(reachable)
        chunks = []
        current = best
        for level, predecessor in reversed(layers):
            previous = predecessor[current]
            chunks.append((level, previous, current))
            current = previous
        assert current == self.start
        chunks.reverse()
        return best, chunks, powers, reachable


class Witness:
    def __init__(self, graph):
        self.graph = graph
        self.model = graph.model
        self.nodes = []
        self.permutations = []
        self.letters = {}
        self.qnums = {}
        self.memo = {}
        self.root = None

    def leaf(self, x, y):
        key = ("leaf", x, y)
        if key in self.memo:
            return self.memo[key]
        flat = self.graph.edges[x, y]
        source, dest, counts, qnum = self.model.allocation(flat)
        node = {"kind": "leaf", "length": 1, "source": list(source), "target": list(dest),
                "allocation": list(flat), "label_counts": list(counts),
                "filler_marginal": [fs(Fraction(q, self.model.F)) for q in qnum]}
        permutation, letters = self.model.slot_data(flat)
        index = len(self.nodes)
        self.nodes.append(node)
        self.permutations.append(permutation)
        self.letters[index] = letters
        self.qnums[index] = qnum
        self.memo[key] = index
        return index

    def concat(self, left, right, memo_key=None):
        key = memo_key or ("concat", left, right)
        if key in self.memo:
            return self.memo[key]
        a, b = self.nodes[left], self.nodes[right]
        assert a["target"] == b["source"]
        node = {"kind": "concat", "length": a["length"]+b["length"],
                "source": a["source"], "target": b["target"], "left": left, "right": right}
        permutation = [self.permutations[right][slot] for slot in self.permutations[left]]
        index = len(self.nodes)
        self.nodes.append(node)
        self.permutations.append(permutation)
        self.memo[key] = index
        return index

    def join_balanced(self, sequence):
        if len(sequence) == 1:
            return sequence[0]
        middle = len(sequence)//2
        return self.concat(self.join_balanced(sequence[:middle]), self.join_balanced(sequence[middle:]))

    def from_path(self, path):
        self.root = self.join_balanced([self.leaf(x, y) for x, y in path])

    def from_powers(self, chunks, powers):
        def make(level, x, y):
            key = ("power", level, x, y)
            if key in self.memo:
                return self.memo[key]
            if level == 0:
                return self.leaf(x, y)
            previous = powers[level-1]
            z = next(z for z in bits(previous[x]) if (previous[z] >> y) & 1)
            return self.concat(make(level-1, x, z), make(level-1, z, y), key)
        self.root = self.join_balanced([make(*chunk) for chunk in chunks])

    def query(self, coordinate, branch, seed):
        if not 0 <= coordinate < self.nodes[self.root]["length"]:
            raise ValueError("Coordinate out of range")
        if branch == "empirical" and not 0 <= seed < self.model.Q:
            raise ValueError("Slot seed out of range")
        node_id, slot = self.root, seed
        depth = 0
        while self.nodes[node_id]["kind"] != "leaf":
            node = self.nodes[node_id]
            left, right = node["left"], node["right"]
            length = self.nodes[left]["length"]
            if coordinate < length:
                node_id = left
            else:
                coordinate -= length
                if branch == "empirical":
                    slot = self.permutations[left][slot]
                node_id = right
            depth += 1
        if branch == "empirical":
            a = self.letters[node_id][slot]
        elif branch == "filler":
            a = self.model.letter(self.qnums[node_id], seed)
        else:
            raise ValueError("Unknown branch")
        return self.model.support[a], node_id, depth

    def filler_terminal(self, seed):
        maps = []
        for i, node in enumerate(self.nodes):
            if node["kind"] == "leaf":
                a = self.model.letter(self.qnums[i], seed)
                maps.append([self.model.delta[s][a] for s in range(self.model.d)])
            else:
                left, right = maps[node["left"]], maps[node["right"]]
                maps.append([right[left[s]] for s in range(self.model.d)])
        return maps[self.root][self.model.start]

    def empirical_terminal(self, slot):
        terminal_slot = self.permutations[self.root][slot]
        end = 0
        for s, count in enumerate(self.nodes[self.root]["target"]):
            end += count
            if terminal_slot < end:
                return s
        raise AssertionError("Invalid terminal slot")

    def exact_terminal(self):
        thresholds = {0, self.model.F}
        for qnum in self.qnums.values():
            count = 0
            for mass in qnum[:-1]:
                count += mass
                thresholds.add(count)
        thresholds = sorted(thresholds)
        counts = [0] * self.model.d
        intervals = []
        for lower, upper in zip(thresholds, thresholds[1:]):
            if lower == upper:
                continue
            terminal = self.filler_terminal(lower)
            counts[terminal] += upper-lower
            intervals.append({"lower": lower, "upper": upper,
                              "terminal": self.model.states[terminal]})
        assert sum(counts) == self.model.F
        g = self.nodes[self.root]["target"]
        actual = [(1-self.model.beta)*Fraction(x, self.model.Q)
                  + self.model.beta*Fraction(c, self.model.F) for x, c in zip(g, counts)]
        assert sum(actual) == 1
        return actual, counts, intervals

    def sample_receipts(self):
        rng = random.Random(20261011)
        n = self.nodes[self.root]["length"]
        coordinates = sorted(set([0, min(1, n-1), n//2, max(0, n-2), n-1])) + [0]
        receipts = []
        # Include both branches even when one rare branch was not randomly drawn.
        seeds = [("empirical", rng.randrange(self.model.Q)), ("filler", rng.randrange(self.model.F))]
        for _ in range(4):
            branch = "empirical" if rng.randrange(self.model.branch_den) < self.model.Q*self.model.umin else "filler"
            seed = rng.randrange(self.model.Q if branch == "empirical" else self.model.F)
            seeds.append((branch, seed))
        for branch, seed in seeds:
            queries = []
            for t in coordinates:
                letter, leaf, depth = self.query(t, branch, seed)
                queries.append({"coordinate_zero_based": t, "letter": letter, "leaf": leaf, "depth": depth})
            terminal = self.empirical_terminal(seed) if branch == "empirical" else self.filler_terminal(seed)
            receipts.append({"branch": branch, "seed": seed, "terminal": self.model.states[terminal], "queries": queries})
        return receipts

    def sample(self, getrandbits=None):
        """Sample the exact coupling, assuming independent fair supplied bits.

        Default secrets.randbits is an operational source. Mathematical exactness
        is conditional on the caller's getrandbits(k) returning a fresh uniform
        k-bit integer. Rejection has finite expectation and no finite worst-case
        bound. The returned branch/seed also supplies every coordinate through
        query(t, result['branch'], result['seed']), consistently on repeats.
        """
        if getrandbits is None:
            from secrets import randbits
            getrandbits = randbits
        requested_bits = 0
        requests = 0
        rejections = 0

        def below(bound):
            nonlocal requested_bits, requests, rejections
            if bound == 1:
                return 0
            width = (bound-1).bit_length()
            while True:
                value = getrandbits(width)
                requested_bits += width
                requests += 1
                if not isinstance(value, int) or not 0 <= value < 1 << width:
                    raise ValueError("getrandbits violated its integer-range contract")
                if value < bound:
                    return value
                rejections += 1

        uniform_seed = below(self.model.uniform_seed_den)
        normal_end = self.model.Q*self.model.M*self.model.umin
        if uniform_seed < normal_end:
            branch, seed = "empirical", uniform_seed//(self.model.M*self.model.umin)
        else:
            branch, seed = "filler", uniform_seed-normal_end
        terminal = self.empirical_terminal(seed) if branch == "empirical" else self.filler_terminal(seed)
        return {"branch": branch, "seed": seed, "terminal": self.model.states[terminal],
                "uniform_seed": uniform_seed, "uniform_seed_denominator": self.model.uniform_seed_den,
                "fair_random_bits_requested": requested_bits, "random_source_requests": requests,
                "integer_rejections": rejections,
                "randomness_contract": "fresh independent uniform getrandbits(k) integers",
                "query_api": "witness.query(t, sample['branch'], sample['seed'])"}


def solve(spec, horizon=None, max_allocations=2_000_000):
    model = Model(spec)
    graph = PopulationGraph(model, max_allocations)
    witness = Witness(graph)
    if horizon is None:
        best, path, reachable = graph.unbounded()
        witness.from_path(path)
    else:
        best, chunks, powers, reachable = graph.binary_horizon(horizon)
        witness.from_powers(chunks, powers)
    vQ = model.tv(graph.histograms[best])
    actual, filler_counts, intervals = witness.exact_terminal()
    actual_tv = sum(abs(p-q) for p, q in zip(actual, model.target))/2
    lower, graph_upper = max(Fraction(0), vQ-model.r), min(Fraction(1), vQ+model.beta)
    upper = min(graph_upper, actual_tv)
    assert lower <= actual_tv <= upper
    terminal_numerators = [model.M*model.umin*x+c
                           for x, c in zip(graph.histograms[best], filler_counts)]
    assert actual == [Fraction(c, model.uniform_seed_den) for c in terminal_numerators]
    cert = {
        "schema": "rational-dfa-population-coupling-v1",
        "status": "EXACT_RATIONAL_WITNESS_AND_FINITE_GRAPH_OPTIMUM",
        "model_sha256": sha256(__import__("json").dumps(spec, sort_keys=True, separators=(",", ":")).encode()).hexdigest(),
        "mode": "unbounded_positive_horizon" if horizon is None else "binary_fixed_horizon",
        "population": model.Q,
        "positive_support": list(model.support),
        "zero_support_letters_removed": [a for a in model.alphabet if a not in model.support],
        "alpha": fs(model.alpha), "rounding_radius": fs(model.r), "repair_weight": fs(model.beta),
        "graph": {"histogram_vertices": graph.H, "allocation_candidates": graph.B,
                  "admissible_allocations": graph.accepted_allocations, "distinct_arcs": len(graph.edges),
                  "reachable_terminal_histograms": reachable.bit_count()},
        "empirical_optimum_tv": fs(vQ), "graph_only_optimum_interval": [fs(lower), fs(graph_upper)],
        "true_optimum_interval": [fs(lower), fs(upper)],
        "witness_horizon": witness.nodes[witness.root]["length"],
        "witness_root": witness.root, "witness_nodes": witness.nodes,
        "witness_node_count": len(witness.nodes), "distinct_leaf_count": len(witness.qnums),
        "empirical_terminal": [fs(Fraction(x, model.Q)) for x in graph.histograms[best]],
        "filler_quantile_denominator": model.F,
        "whole_coupling_uniform_seed_denominator": model.uniform_seed_den,
        "filler_threshold_intervals": intervals,
        "filler_terminal_numerators": filler_counts,
        "actual_repaired_terminal": [fs(p) for p in actual], "actual_repaired_tv": fs(actual_tv),
        "actual_repaired_terminal_numerators": terminal_numerators,
        "quantile_support_bound": 1+(model.m-1)*len(witness.qnums),
        "coupling_word_support_upper_bound": model.Q+len(intervals),
        "seed_receipts": witness.sample_receipts(),
        "randomness": "Exact rational branch and finite uniform seeds; seeded receipts are demonstrations, not a randomness test.",
    }
    return cert, witness


def verify(spec, certificate, recompute_optimum=True, max_allocations=2_000_000, expected_horizon=None):
    model = Model(spec)
    digest = sha256(__import__("json").dumps(spec, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    assert certificate["model_sha256"] == digest
    assert certificate["population"] == model.Q
    assert certificate["alpha"] == fs(model.alpha)
    assert certificate["rounding_radius"] == fs(model.r)
    assert certificate["repair_weight"] == fs(model.beta)
    assert certificate["positive_support"] == list(model.support)
    nodes = certificate["witness_nodes"]
    fake_graph = type("CertificateGraph", (), {"model": model})()
    witness = Witness(fake_graph)
    for i, node in enumerate(nodes):
        if node["kind"] == "leaf":
            flat = tuple(node["allocation"])
            assert all(isinstance(x, int) for x in flat)
            source, dest, counts, qnum = model.allocation(flat)
            assert node["length"] == 1
            assert tuple(node["source"]) == source and tuple(node["target"]) == dest
            assert tuple(node["label_counts"]) == counts
            assert tuple(map(frac, node["filler_marginal"])) == tuple(Fraction(q, model.F) for q in qnum)
            permutation, letters = model.slot_data(flat)
            witness.letters[i], witness.qnums[i] = letters, qnum
        else:
            assert node["kind"] == "concat"
            left, right = node["left"], node["right"]
            assert 0 <= left < i and 0 <= right < i
            a, b = nodes[left], nodes[right]
            assert a["target"] == b["source"]
            assert node["source"] == a["source"] and node["target"] == b["target"]
            assert node["length"] == a["length"]+b["length"]
            permutation = [witness.permutations[right][slot] for slot in witness.permutations[left]]
        witness.nodes.append(node)
        witness.permutations.append(permutation)
    witness.root = certificate["witness_root"]
    root = nodes[witness.root]
    assert tuple(root["source"]) == model.initial
    assert root["length"] == certificate["witness_horizon"] >= 1
    if expected_horizon is not None:
        assert certificate["mode"] == "binary_fixed_horizon"
        assert root["length"] == expected_horizon
    actual, counts, intervals = witness.exact_terminal()
    assert [fs(p) for p in actual] == certificate["actual_repaired_terminal"]
    assert certificate["empirical_terminal"] == [fs(Fraction(x, model.Q)) for x in root["target"]]
    assert certificate["empirical_optimum_tv"] == fs(model.tv(root["target"]))
    assert certificate["actual_repaired_tv"] == fs(sum(abs(p-q) for p, q in zip(actual, model.target))/2)
    assert counts == certificate["filler_terminal_numerators"]
    assert certificate["whole_coupling_uniform_seed_denominator"] == model.uniform_seed_den
    assert [Fraction(c, model.uniform_seed_den) for c in certificate["actual_repaired_terminal_numerators"]] == actual
    assert intervals == certificate["filler_threshold_intervals"]
    for receipt in certificate["seed_receipts"]:
        branch, seed = receipt["branch"], receipt["seed"]
        terminal = witness.empirical_terminal(seed) if branch == "empirical" else witness.filler_terminal(seed)
        assert model.states[terminal] == receipt["terminal"]
        for query in receipt["queries"]:
            letter, leaf, depth = witness.query(query["coordinate_zero_based"], branch, seed)
            assert (letter, leaf, depth) == (query["letter"], query["leaf"], query["depth"])
    # Independent explicit word evaluation for all empirical atoms and every
    # quantile interval when the horizon is small enough to emit those words.
    expanded_checks = 0
    if root["length"] <= 200:
        for branch, seeds in [("empirical", range(model.Q)),
                              ("filler", [i["lower"] for i in intervals])]:
            for seed in seeds:
                state = model.start
                for t in range(root["length"]):
                    a = model.support.index(witness.query(t, branch, seed)[0])
                    state = model.delta[state][a]
                expected = witness.empirical_terminal(seed) if branch == "empirical" else witness.filler_terminal(seed)
                assert state == expected
                expanded_checks += 1
    if recompute_optimum:
        horizon = root["length"] if certificate["mode"] == "binary_fixed_horizon" else None
        replay, _ = solve(spec, horizon, max_allocations)
        assert replay["empirical_optimum_tv"] == certificate["empirical_optimum_tv"]
        assert replay["true_optimum_interval"] == certificate["true_optimum_interval"]
    return {"witness_valid": True, "exact_marginal_equations_checked_on_each_leaf": True,
            "succinct_terminal_distribution_verified": True,
            "empirical_optimum_recomputed": recompute_optimum,
            "expanded_small_horizon_atom_checks": expanded_checks}


def round_layered_flow(spec, weighted_words, population):
    """Constructive whole-flow floor/ceiling rounding, for supplied finite words."""
    model = Model(dict(spec, population=population))
    words = [(tuple(word), frac(weight)) for word, weight in weighted_words]
    assert sum(weight for _, weight in words) == 1
    n = len(words[0][0])
    assert n >= 1 and all(len(word) == n for word, _ in words)
    for t in range(n):
        for a, p in zip(model.support, model.mu):
            assert sum(weight for word, weight in words if word[t] == a) == p
    raw = {}
    terminal = [Fraction(0)] * model.d
    for word, weight in words:
        state = model.start
        for t, letter in enumerate(word):
            a = model.support.index(letter)
            dest = model.delta[state][a]
            key = (t, state, a, dest)
            raw[key] = raw.get(key, Fraction(0)) + population*weight
            state = dest
        terminal[state] += weight
    edges = []
    for key, value in sorted(raw.items()):
        t, s, a, dest = key
        edges.append(((t, s), (t+1, dest), value, key))
    sink = (n+1, -1)
    for s, p in enumerate(terminal):
        if p:
            edges.append(((n, s), sink, population*p, (n, s, -1, -1)))
    values = [e[2] for e in edges]
    bounds = [(v.numerator//v.denominator, -((-v.numerator)//v.denominator)) for v in values]
    adjustments = 0
    while True:
        fractional = [i for i, value in enumerate(values) if value.denominator != 1]
        if not fractional:
            break
        parent, forest = {}, {}
        def find(x):
            parent.setdefault(x, x)
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]
        closing = None
        for i in fractional:
            u, v = edges[i][:2]
            ru, rv = find(u), find(v)
            if ru == rv:
                closing = i
                break
            parent[ru] = rv
            forest.setdefault(u, []).append((v, i))
            forest.setdefault(v, []).append((u, i))
        assert closing is not None, "Integer balances force a fractional cycle"
        u, v = edges[closing][:2]
        queue, previous = deque([u]), {u: None}
        while v not in previous:
            x = queue.popleft()
            for y, i in forest.get(x, []):
                if y not in previous:
                    previous[y] = (x, i)
                    queue.append(y)
        traversal = []
        x = v
        while x != u:
            y, i = previous[x]
            traversal.append((y, x, i))
            x = y
        traversal.reverse()
        traversal.append((v, u, closing))
        signed = [(i, 1 if edges[i][0] == x else -1) for x, _, i in traversal]
        amount = min((bounds[i][1]-values[i]) if sign == 1 else (values[i]-bounds[i][0])
                     for i, sign in signed)
        assert amount > 0
        for i, sign in signed:
            values[i] += sign*amount
        adjustments += 1
    before, after = {}, {}
    for i, (u, v, original, _) in enumerate(edges):
        for vertex, sign in [(u, 1), (v, -1)]:
            before[vertex] = before.get(vertex, Fraction(0)) + sign*original
            after[vertex] = after.get(vertex, Fraction(0)) + sign*values[i]
        assert bounds[i][0] <= values[i] <= bounds[i][1]
    assert before == after and all(x.denominator == 1 for x in after.values())
    residual = [int(v) for v in values]
    output_words, output_terminal = [], [0]*model.d
    for _ in range(population):
        state, word = model.start, []
        for t in range(n):
            i = next(i for i, e in enumerate(edges) if e[0] == (t, state) and residual[i] > 0)
            residual[i] -= 1
            a, state = edges[i][3][2:]
            word.append(model.support[a])
        i = next(i for i, e in enumerate(edges) if e[0] == (n, state) and residual[i] > 0)
        residual[i] -= 1
        output_terminal[state] += 1
        output_words.append(word)
    assert not any(residual)
    discrepancy = [[fs(abs(sum(word[t] == a for word in output_words)-population*p))
                    for a, p in zip(model.support, model.mu)] for t in range(n)]
    tv = sum(abs(Fraction(c, population)-p) for c, p in zip(output_terminal, terminal))/2
    assert tv <= model.r
    return {"status": "EXACT_RATIONAL_LAYERED_FLOW_ROUNDING_CHECKED", "horizon": n,
            "population": population, "rounded_words": output_words,
            "terminal_original": [fs(p) for p in terminal], "terminal_rounded_counts": output_terminal,
            "terminal_tv": fs(tv), "terminal_bound": fs(model.r),
            "coordinate_letter_count_discrepancies": discrepancy,
            "flow_edges": len(edges), "cycle_adjustments": adjustments,
            "all_node_balances_preserved": True, "all_edge_floor_ceiling_bounds_preserved": True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=["solve", "verify"])
    parser.add_argument("spec", type=Path)
    parser.add_argument("certificate", type=Path)
    parser.add_argument("--horizon", type=int, help="positive binary-encoded integer; omit for unbounded positive horizon")
    parser.add_argument("--max-allocations", type=int, default=2_000_000,
                        help="resource guard; 0 disables (cost remains explicit)")
    args = parser.parse_args()
    import json
    spec = json.loads(args.spec.read_text())
    if args.mode == "solve":
        certificate, _ = solve(spec, args.horizon, args.max_allocations)
        args.certificate.write_text(json.dumps(certificate, indent=2)+"\n")
        print(json.dumps({k: certificate[k] for k in ["mode", "graph", "witness_horizon", "witness_node_count",
                         "empirical_optimum_tv", "true_optimum_interval", "actual_repaired_terminal",
                         "coupling_word_support_upper_bound"]}, indent=2))
    else:
        print(json.dumps(verify(spec, json.loads(args.certificate.read_text()),
                                max_allocations=args.max_allocations, expected_horizon=args.horizon), indent=2))


if __name__ == "__main__":
    main()
