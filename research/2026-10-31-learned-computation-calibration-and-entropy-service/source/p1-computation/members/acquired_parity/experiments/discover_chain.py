#!/usr/bin/env python3
"""Discover a certified low-width order from acquired parity masks.

All inference kernels are classical minimal-trellis / transfer-matrix kernels.
The non-supplied object in this experiment is the relation graph and its order.
Only this module's fixture builder reads a hidden chain.  The acquisition and
recognizer receive scalar oracle access and learned masks, respectively.
"""
from __future__ import annotations

from fractions import Fraction
from pathlib import Path
import json
import random
import sys
import time

# Both layouts are supported: development tree and self-contained bundle.
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[1]))
try:
    from parity_acquisition import (ScalarOracle, acquire_certified, basis,
        basis_and_relations, CompiledTrellis, parity, solve_rows)
except ImportError:
    from next_independent.parity_acquisition import (ScalarOracle,
        acquire_certified, basis, basis_and_relations, CompiledTrellis,
        parity, solve_rows)
try:
    from parity_inference import GF2System, BitSource, lincomb
except ImportError:
    from next_causal.parity_inference import GF2System, BitSource, lincomb


def relation_width(support: list[int], order: list[int] | None = None):
    """Compute all cut ranks before allocating an exponential state table."""
    if order is None:
        order = list(range(len(support)))
    if sorted(order) != list(range(len(support))):
        raise ValueError("Order must permute all acquired features")
    ordered = [support[i] for i in order]
    _, checks = basis_and_relations(ordered)
    columns = [sum(((row >> j) & 1) << i for i, row in enumerate(checks))
               for j in range(len(ordered))]
    d = len(checks)
    cuts = [len(basis(columns[:j])) + len(basis(columns[j:])) - d
            for j in range(len(ordered) + 1)]
    return {"dependency": d, "cut_dimensions": cuts, "width": max(cuts),
            "state_cells": sum(1 << q for q in cuts),
            "max_states": 1 << max(cuts)}


def discover_triangle_path(support: list[int]):
    """Polynomial recognizer with an exact relation-span certificate.

It accepts a connected path of 3-term XOR relations that spans *all*
dependencies. Non-path inputs return UNKNOWN; they are not called hard.
The output's cut dimensions are separately computed, never assumed.
"""
    start = time.perf_counter()
    s = len(support)
    if len(set(support)) != s or 0 in support:
        return {"status": "UNKNOWN", "reason": "requires distinct nonzero masks"}
    index = {a: j for j, a in enumerate(support)}
    triangles = set()
    pair_tests = 0
    for i in range(s):
        for j in range(i + 1, s):
            pair_tests += 1
            k = index.get(support[i] ^ support[j])
            if k is not None:
                triangles.add(tuple(sorted((i, j, k))))
    triangles = sorted(triangles)
    relation_masks = [sum(1 << j for j in t) for t in triangles]
    rank_A = len(basis(support))
    d = s - rank_A
    if not triangles or len(basis(relation_masks)) != d:
        return {"status": "UNKNOWN", "reason": "triangles do not span all relations",
                "pair_tests": pair_tests, "triangles": len(triangles)}
    neighbors = [set() for _ in triangles]
    for i in range(len(triangles)):
        for j in range(i + 1, len(triangles)):
            overlap = set(triangles[i]) & set(triangles[j])
            if len(overlap) > 1:
                return {"status": "UNKNOWN", "reason": "overlap exceeds one feature"}
            if overlap:
                neighbors[i].add(j)
                neighbors[j].add(i)
    if len(triangles) == 1:
        path = [0]
    else:
        ends = [i for i, adjacent in enumerate(neighbors) if len(adjacent) == 1]
        if len(ends) != 2 or any(len(adjacent) not in (1, 2) for adjacent in neighbors):
            return {"status": "UNKNOWN", "reason": "overlap graph is not a path"}
        path, previous, current = [], None, min(ends)
        while current is not None:
            path.append(current)
            onward = neighbors[current] - ({previous} if previous is not None else set())
            previous, current = current, (next(iter(onward)) if onward else None)
        if len(path) != len(triangles):
            return {"status": "UNKNOWN", "reason": "overlap graph is disconnected"}
    ordered = []
    seen = set()
    for p, ti in enumerate(path):
        future = set(triangles[path[p + 1]]) if p + 1 < len(path) else set()
        # The previous shared feature was deferred at the preceding bag.
        emit = set(triangles[ti]) - seen - future
        previous_shared = (set(triangles[path[p - 1]]) & set(triangles[ti])) if p else set()
        # Complete the preceding relation before opening the next one.
        for j in sorted(emit & previous_shared):
            ordered.append(j)
            seen.add(j)
        emit -= previous_shared
        ordered.extend(sorted(emit))
        seen.update(emit)
    # Features in no relation are independent and may be appended anywhere.
    ordered.extend(j for j in range(s) if j not in seen)
    width = relation_width(support, ordered)
    return {"status": "CERTIFIED", "order": ordered, "triangles": triangles,
            "relation_rank": len(basis(relation_masks)), "rank_A": rank_A,
            "pair_tests": pair_tests, "overlap_pair_tests": len(triangles) * (len(triangles) - 1) // 2,
            "seconds": time.perf_counter() - start, **width}


class RetainedFeatureTrellis:
    """A single classical template reused across weights and feature evidence.

Evidence keys are acquired feature indices, not arbitrary original input bits.
Hard evidence only deletes incompatible transitions; the state bound cannot
increase. Integer weights make all masses and sampling branches exact.
"""
    def __init__(self, n: int, support: list[int], order: list[int], max_cells=1000000):
        profile = relation_width(support, order)
        if profile["state_cells"] > max_cells:
            raise ValueError("Declared compilation budget exceeded")
        self.n, self.support, self.order = n, list(support), list(order)
        self.ordered = [support[j] for j in order]
        self.trellis = CompiledTrellis.compile(n, self.ordered)
        self.lift_system = GF2System(self.ordered, n)
        self.profile = profile
        self.calls = 0

    def evaluate(self, weights: list[tuple[int, int]], evidence: dict[int, int] | None = None):
        if len(weights) != len(self.support) or any(min(w) <= 0 for w in weights):
            raise ValueError("Positive integer weight pairs required")
        weights = tuple(tuple(pair) for pair in weights)
        evidence = dict(evidence or {})
        if any(j < 0 or j >= len(weights) or b not in (0, 1) for j, b in evidence.items()):
            raise ValueError("Invalid learned-feature evidence")
        tables, maxima, parents = [[1]], [1], []
        used_edges = 0
        for j, (layer, edges) in enumerate(zip(self.trellis.layers[1:], self.trellis.transitions)):
            original = self.order[j]
            weight = weights[original]
            nxt, best, parent = [0] * len(layer), [0] * len(layer), [None] * len(layer)
            for source, target, bit in edges:
                if original in evidence and evidence[original] != bit:
                    continue
                used_edges += 1
                nxt[target] += tables[-1][source] * weight[bit]
                value = maxima[source] * weight[bit]
                if value > best[target]:
                    best[target], parent[target] = value, (source, bit)
            tables.append(nxt)
            maxima = best
            parents.append(parent)
        self.calls += 1
        return TrellisEvaluation(self, weights, evidence, tables, maxima[0], parents, used_edges)


class TrellisEvaluation:
    def __init__(self, compiler, weights, evidence, tables, map_mass, parents, used_edges):
        self.compiler, self.weights, self.evidence = compiler, weights, evidence
        self.tables, self.map_mass, self.parents = tables, map_mass, parents
        self.used_edges = used_edges
        self.code_partition = tables[-1][0]
        self.partition = self.code_partition << (compiler.n - compiler.trellis.rank)

    def map_input(self):
        if self.code_partition == 0:
            raise ValueError("Inconsistent evidence")
        state, y = 0, 0
        for j in range(len(self.compiler.order) - 1, -1, -1):
            state, bit = self.parents[j][state]
            y |= bit << j
        return self.compiler.lift_system.particular(y)

    def sample(self, bits: BitSource):
        if self.code_partition == 0:
            raise ValueError("Inconsistent evidence")
        state, y = 0, 0
        for j in range(len(self.compiler.order) - 1, -1, -1):
            branches = []
            original = self.compiler.order[j]
            for source, target, bit in self.compiler.trellis.transitions[j]:
                if target != state or (original in self.evidence and self.evidence[original] != bit):
                    continue
                mass = self.tables[j][source] * self.weights[original][bit]
                if mass:
                    branches.append((source, bit, mass))
            if len(branches) == 1:
                source, bit, _ = branches[0]
            else:
                draw = bits.randbelow(sum(mass for _, _, mass in branches))
                for source, bit, mass in branches:
                    if draw < mass:
                        break
                    draw -= mass
            state = source
            y |= bit << j
        x = self.compiler.lift_system.particular(y)
        kernel = self.compiler.lift_system.kernel
        return x ^ lincomb(kernel, bits.getrandbits(len(kernel)))


def hidden_chain(n: int, length: int, rng: random.Random):
    coordinates = []
    while len(coordinates) < length + 1:
        candidate = rng.getrandbits(n)
        if len(basis(coordinates + [candidate])) > len(coordinates):
            coordinates.append(candidate)
    nodes = coordinates
    edges = [a ^ b for a, b in zip(nodes, nodes[1:])]
    return nodes + edges, nodes, edges


def ordinary_chain_partition(nodes, edges, learned, weights, evidence=None):
    """Conventional transfer matrix given the same recovered graph.

Fixture coordinates only identify the isomorphic chain to independently
verify answers. The main comparison counts the identical acquired trellis.
"""
    evidence = evidence or {}
    index = {a: i for i, a in enumerate(learned)}
    def w(a, bit):
        j = index[a]
        return weights[j][bit] if j not in evidence or evidence[j] == bit else 0
    forward = [w(nodes[0], b) for b in (0, 1)]
    for v, edge in zip(nodes[1:], edges):
        forward = [w(v, b) * sum(forward[a] * w(edge, a ^ b) for a in (0, 1))
                   for b in (0, 1)]
    return sum(forward)


def finite_checks():
    rng = random.Random(271828)
    cases, samples = 0, 0
    for length in range(1, 5):
        n = length + 3
        support, nodes, edges = hidden_chain(n, length, rng)
        rng.shuffle(support)
        certificate = discover_triangle_path(support)
        assert certificate["status"] == "CERTIFIED"
        assert certificate["width"] == 1
        compiler = RetainedFeatureTrellis(n, support, certificate["order"])
        for trial in range(15):
            weights = [(rng.randrange(1, 8), rng.randrange(1, 8)) for _ in support]
            witness = rng.randrange(1 << n)
            evidence = {j: parity(a & witness) for j, a in enumerate(support) if rng.randrange(3) == 0}
            evaluated = compiler.evaluate(weights, evidence)
            direct, direct_max = 0, 0
            for x in range(1 << n):
                if any(parity(support[j] & x) != b for j, b in evidence.items()):
                    continue
                weight = 1
                for a, pair in zip(support, weights):
                    weight *= pair[parity(a & x)]
                direct += weight
                direct_max = max(direct_max, weight)
            assert evaluated.partition == direct
            assert evaluated.map_mass == direct_max
            assert direct == (ordinary_chain_partition(nodes, edges, support, weights, evidence)
                              << (n - len(nodes)))
            x = evaluated.map_input()
            assert all(parity(support[j] & x) == b for j, b in evidence.items())
            source = BitSource(trial + 100 * length)
            for _ in range(5):
                x = evaluated.sample(source)
                assert all(parity(support[j] & x) == b for j, b in evidence.items())
                samples += 1
            cases += 1
    return {"partition_MAP_bruteforce_cases": cases, "feasible_samples": samples}


def run():
    checks = finite_checks()
    rng = random.Random(202610312)
    n, length = 48, 30
    support, nodes, edges = hidden_chain(n, length, rng)
    coefficients = [rng.choice([-3, -2, -1, 1, 2, 3]) for _ in support]
    oracle = ScalarOracle(n, support, coefficients, 2)
    acquired = acquire_certified(n, len(support) + 1, .01, oracle, random.Random(949))
    assert acquired["success"]
    assert acquired["all_coefficients"] == {0: Fraction(2), **dict(zip(support, map(Fraction, coefficients)))}
    learned = acquired["support"]
    before = relation_width(learned)
    certificate = discover_triangle_path(learned)
    assert certificate["status"] == "CERTIFIED" and certificate["width"] == 1
    start = time.perf_counter()
    compiler = RetainedFeatureTrellis(n, learned, certificate["order"])
    compilation_seconds = time.perf_counter() - start
    # Weights derived from the acquired energy at beta=ln(2):
    # f_j=c_j chi_a. Multiply its Boltzmann pair by 2^|c_j| to
    # obtain positive integer pairs. The common factor cancels in probabilities.
    initial_weights = []
    for a in learned:
        c = int(acquired["coefficients"][a])
        initial_weights.append((1 << (abs(c) - c), 1 << (abs(c) + c)))
    initial = compiler.evaluate(initial_weights)
    initial_direct = ordinary_chain_partition(nodes, edges, learned, initial_weights) << (n - len(nodes))
    assert initial.partition == initial_direct
    physical_scale = int(acquired["constant"]) + sum(abs(int(acquired["coefficients"][a])) for a in learned)
    physical_partition = Fraction(initial.partition, 1 << physical_scale)
    energy_map_x = initial.map_input()
    energy_map = int(acquired["constant"]) + sum(
        int(acquired["coefficients"][a]) * (1 if not parity(a & energy_map_x) else -1) for a in learned)
    # A hard evidence event on every acquired parity can be extremely rare.
    # It is feasible at x=0 and retains the original width-one template.
    rare_evidence = {j: 0 for j in range(len(learned))}
    rare = compiler.evaluate(initial_weights, rare_evidence)
    rare_probability = Fraction(rare.partition, initial.partition)
    source = BitSource(111)
    for _ in range(20):
        x = rare.sample(source)
        assert all(parity(a & x) == 0 for a in learned)
    start = time.perf_counter()
    max_answer_bits, total_used_edges = 0, 0
    for task in range(250):
        weights = [(rng.randrange(1, 17), rng.randrange(1, 17)) for _ in learned]
        witness = rng.getrandbits(n)
        evidence = {j: parity(a & witness) for j, a in enumerate(learned) if rng.randrange(5) == 0}
        answer = compiler.evaluate(weights, evidence)
        ordinary = ordinary_chain_partition(nodes, edges, learned, weights, evidence) << (n - len(nodes))
        assert answer.partition == ordinary
        x = answer.map_input()
        assert all(parity(learned[j] & x) == b for j, b in evidence.items())
        max_answer_bits = max(max_answer_bits, answer.partition.bit_length())
        total_used_edges += answer.used_edges
    reuse_seconds = time.perf_counter() - start
    acq_log = {k: v for k, v in acquired.items()
               if k not in {"support", "coefficients", "constant", "all_coefficients"}}
    result = {"finite_verification": checks, "n": n, "features": len(learned),
              "rank": len(nodes), "dependency": length,
              "raw_domain_size": 1 << n, "distinct_feature_vectors": 1 << len(nodes),
              "acquisition": acq_log, "scalar_calls_after_training": 0,
              "canonical_order_profile": before, "discovered_order_certificate": certificate,
              "trellis_edges": compiler.trellis.edge_count,
              "trellis_compile_seconds": compilation_seconds,
              "all_syndromes_DP_states": 1 << length,
              "all_syndromes_DP_cells": (len(learned) + 1) * (1 << length),
              "retained_conventional_minimal_trellis": {"width": compiler.trellis.width,
                  "edges": compiler.trellis.edge_count, "same_acquisition_and_certificate": True,
                  "additional_Astra_execution_advantage": 0},
              "reuse_queries": 250, "reuse_seconds_including_independent_transfer_check": reuse_seconds,
              "reuse_total_scanned_edges": 250 * compiler.trellis.edge_count,
              "reuse_total_active_edge_evaluations": total_used_edges,
              "reuse_max_partition_bits": max_answer_bits,
              "rare_event_probability": {"numerator": rare_probability.numerator,
                  "denominator": rare_probability.denominator,
                  "decimal": float(rare_probability)},
              "rare_conditional_samples": 20,
              "rare_conditional_random_bits_used": source.bits_used,
              "physical_partition_at_beta_ln2": {"numerator": physical_partition.numerator,
                  "denominator": physical_partition.denominator, "integerization_scale_power": physical_scale},
              "acquired_energy_MAP": {"energy": energy_map, "input": energy_map_x},
              "learned_support": learned, "learned_coefficients": [str(acquired["coefficients"][a]) for a in learned],
              "limitations": ["Synthetic exact scalar energy service; configuration preparation charged in n-bit units, not a physical device.",
                  "Future evidence here clamps acquired parity features; arbitrary original-coordinate evidence is not promised tractable.",
                  "All-syndrome and raw-enumeration sizes are exact counts, not executed timing comparisons.",
                  "Classical sparse-WHT acquisition has stronger asymptotic theory than this auditable quadratic-sparsity implementation."]}
    out = HERE.parent / "results" / "discovered_chain.json"
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: result[k] for k in ["n", "features", "rank", "dependency", "acquisition", "trellis_edges", "reuse_queries", "rare_event_probability"]}, indent=2))


if __name__ == "__main__":
    run()
