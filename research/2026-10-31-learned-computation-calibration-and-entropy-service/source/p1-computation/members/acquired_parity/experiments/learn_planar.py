#!/usr/bin/env python3
"""End-to-end scalar acquisition, graph discovery, and retained exact inference.

The two execution methods are conventional: a cached min-fill variable
elimination schedule and a cached Fisher/Kasteleyn Pfaffian.  Both receive the
same acquired edge-labelled graph.  No extra Astra execution layer is used.
"""
from __future__ import annotations

from fractions import Fraction as Q
from itertools import combinations
from math import prod, comb
from pathlib import Path
import json
import random
import sys
import time

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[1]))
try:
    import graphic_acquisition as ga
    from parity_acquisition import ScalarOracle, acquire_certified, basis, parity, linear_combination
    from parity_inference import GF2System, BitSource, lincomb
except ImportError:
    from next_tractability import graphic_acquisition as ga
    from next_independent.parity_acquisition import ScalarOracle, acquire_certified, basis, parity, linear_combination
    from next_causal.parity_inference import GF2System, BitSource, lincomb


class RetainedPfaffian:
    def __init__(self, graph, embedding):
        self.graph, self.embedding = graph, embedding
        self.nv, self.edges = graph["vertices"], graph["edges"]
        self.size, self.internal, faces, _, matching = ga.fisher_cubic(
            graph, embedding, [(1, 1)] * len(self.edges))
        _, self.orientation = ga.kasteleyn_matrix(self.size, self.internal, faces)
        self.sign = ga.matching_orientation_sign(matching, self.orientation)
        self.external = []
        for u, v in self.edges:
            a = 4 * u + embedding["rotation"][u].index(v) + 1
            b = 4 * v + embedding["rotation"][v].index(u) + 1
            self.external.append(tuple(sorted((a, b))))
        self.calls = 0
        self.signed_requests = 0
        self.interpolation_evaluations = 0

    def partition(self, weights):
        if len(weights) != len(self.edges):
            raise ValueError("Wrong number of edge factors")
        if any(min(w) < 0 for w in weights):
            raise ValueError("Nonnegative factors required")
        return self._nonsingular_partition(weights)

    def signed_partition(self, weights):
        """Exact signed extension; interpolate only zero-sum nonzero pairs."""
        if len(weights) != len(self.edges):
            raise ValueError("Wrong number of edge factors")
        self.signed_requests += 1
        if any(w[0] == 0 and w[1] == 0 for w in weights):
            return Q(0)
        zeros = {e for e, w in enumerate(weights) if w[0] + w[1] == 0}
        if not zeros:
            return self._nonsingular_partition(weights)
        q, answer = len(zeros), Q(0)
        for j in range(1, q + 2):
            perturbed = [(w[0] + j, w[1] + j) if e in zeros else w
                         for e, w in enumerate(weights)]
            answer += (-1 if j % 2 == 0 else 1) * comb(q + 1, j) * self._nonsingular_partition(perturbed)
            self.interpolation_evaluations += 1
        return answer

    def _nonsingular_partition(self, weights):
        ew, prefactor = dict(self.internal), Q(1 << (self.nv - 1))
        for e, pair in zip(self.external, weights):
            w0, w1 = map(Q, pair)
            if w0 + w1 == 0:
                if w0 == 0:
                    return Q(0)
                raise ValueError("Use signed interpolation for a zero-sum pair")
            a, b = (w0 + w1) / 2, (w0 - w1) / 2
            prefactor *= a
            ew[e] = b / a
        mat = [[Q(0)] * self.size for _ in range(self.size)]
        for (u, v), value in ew.items():
            mat[u][v] = self.orientation[u, v] * value
            mat[v][u] = -mat[u][v]
        self.calls += 1
        return prefactor * self.sign * ga.pfaffian(mat)


class RetainedElimination:
    """Cache a classical min-fill elimination order and all index maps."""
    def __init__(self, graph, cell_budget=2_000_000):
        self.graph, self.edges = graph, graph["edges"]
        nv = graph["vertices"]
        scopes = {e: tuple(ends) for e, ends in enumerate(self.edges)}
        adjacency = [set() for _ in range(nv)]
        for u, v in self.edges:
            adjacency[u].add(v)
            adjacency[v].add(u)
        active, self.width, self.cells, self.steps = set(range(nv)), 0, 0, []
        next_id = len(scopes)
        self.scalar_multiplications = 0
        while active:
            def score(v):
                ns = list(adjacency[v])
                fill = sum(b not in adjacency[a] for a, b in combinations(ns, 2))
                return fill, len(ns), v
            v = min(active, key=score)
            ns = adjacency[v]
            self.width = max(self.width, len(ns))
            for a, b in combinations(ns, 2):
                adjacency[a].add(b)
                adjacency[b].add(a)
            for a in ns:
                adjacency[a].remove(v)
            active.remove(v)
            bucket = [i for i, scope in scopes.items() if v in scope]
            output = tuple(sorted({x for i in bucket for x in scopes[i]} - {v}))
            self.cells += 1 << len(output)
            if self.cells > cell_budget:
                raise ValueError("Variable elimination compilation budget exceeded")
            positions = {x: j for j, x in enumerate(output)}
            maps = [tuple(-1 if x == v else positions[x] for x in scopes[i]) for i in bucket]
            lookups = []
            for assignment in range(1 << len(output)):
                lookups.append(tuple(tuple(sum((value if p == -1 else (assignment >> p) & 1) << j
                                                 for j, p in enumerate(mapping))
                                             for mapping in maps)
                                     for value in (0, 1)))
            self.scalar_multiplications += 2 * len(bucket) * len(lookups)
            self.steps.append((next_id, bucket, lookups))
            for i in bucket:
                del scopes[i]
            scopes[next_id] = output
            next_id += 1
        self.final_ids = list(scopes)
        assert all(scope == () for scope in scopes.values())
        self.calls = 0

    def partition(self, weights):
        if len(weights) != len(self.edges) or any(min(w) < 0 for w in weights):
            raise ValueError("Nonnegative pair for each edge required")
        return self.signed_partition(weights)

    def signed_partition(self, weights):
        if len(weights) != len(self.edges):
            raise ValueError("One pair per edge required")
        # Fractions are used only when supplied. Integer inputs retain the much
        # cheaper exact integer semiring until the final division by two.
        tables = {e: (w[0], w[1], w[1], w[0]) for e, w in enumerate(weights)}
        for out_id, bucket, lookups in self.steps:
            inputs = [tables[i] for i in bucket]
            result = [sum(prod(table[key] for table, key in zip(inputs, keys))
                          for keys in both) for both in lookups]
            for i in bucket:
                del tables[i]
            tables[out_id] = result
        self.calls += 1
        return Q(prod(tables[i][0] for i in self.final_ids), 2)


def clamp(weights, evidence):
    return [((w[0], 0) if evidence[e] == 0 else (0, w[1])) if e in evidence else w
            for e, w in enumerate(weights)]


class LearnedDistribution:
    def __init__(self, n, support, engine, weights):
        self.n, self.support, self.engine = n, tuple(support), engine
        self.weights = tuple(tuple(pair) for pair in weights)
        self.lift = GF2System(support, n)
        self.fiber_size = 1 << len(self.lift.kernel)

    def partition(self, evidence=None):
        return self.fiber_size * self.engine.partition(clamp(self.weights, evidence or {}))

    def sample(self, bits, evidence=None):
        """Exact self-reduction using <=s new partition calls and a uniform lift."""
        evidence = dict(evidence or {})
        current = self.engine.partition(clamp(self.weights, evidence))
        if current <= 0:
            raise ValueError("Inconsistent evidence")
        y = sum(b << e for e, b in evidence.items())
        for e in range(len(self.support)):
            if e in evidence:
                continue
            evidence[e] = 0
            z0 = self.engine.partition(clamp(self.weights, evidence))
            p0 = z0 / current
            choose_zero = bits.randbelow(p0.denominator) < p0.numerator
            if choose_zero:
                current = z0
            else:
                evidence[e] = 1
                current -= z0
                y |= 1 << e
        x = self.lift.particular(y)
        return x ^ lincomb(self.lift.kernel, bits.getrandbits(len(self.lift.kernel)))


def main():
    rng = random.Random(170117)
    nv, edges = ga.truncated_octahedron_fixture()
    hidden_rows = ga.hidden_matrix(nv, edges, 718)
    abstract_support = ga.columns(hidden_rows, len(edges))
    n, embedding_vectors = 32, []
    while len(embedding_vectors) < len(hidden_rows):
        v = rng.getrandbits(n)
        if len(basis(embedding_vectors + [v])) > len(embedding_vectors):
            embedding_vectors.append(v)
    support = [linear_combination(embedding_vectors, a) for a in abstract_support]
    coefficients = [rng.choice([-3, -2, -1, 1, 2, 3]) for _ in support]
    oracle = ScalarOracle(n, support, coefficients, 1)
    learned = acquire_certified(n, len(support) + 1, .01, oracle, random.Random(1203))
    assert learned["success"]
    assert learned["all_coefficients"] == {0: Q(1), **dict(zip(support, map(Q, coefficients)))}
    A = learned["support"]
    # This is the only model sent to the structural acquisition routine.
    K = [sum(((a >> i) & 1) << e for e, a in enumerate(A)) for i in range(n)]
    start = time.perf_counter()
    G = ga.acquire_graph(K, len(A), 3)
    primal_seconds = time.perf_counter() - start
    assert G is not None
    start = time.perf_counter()
    dual = ga.acquire_graph(ga.nullspace(K, len(A)), len(A), 6)
    assert dual is not None
    rotation = ga.acquire_sphere_embedding(G, dual)
    embedding_seconds = time.perf_counter() - start
    assert rotation is not None
    start = time.perf_counter()
    pf = RetainedPfaffian(G, rotation)
    pf_compile_seconds = time.perf_counter() - start
    start = time.perf_counter()
    ve = RetainedElimination(G)
    ve_compile_seconds = time.perf_counter() - start
    weights = []
    for a in A:
        c = int(learned["coefficients"][a])
        weights.append((1 << (abs(c) - c), 1 << (abs(c) + c)))
    tasks = []
    for q in range(12):
        w = weights if q == 0 else [(rng.randrange(1, 9), rng.randrange(1, 9)) for _ in A]
        witness = rng.getrandbits(n)
        evidence = {} if q == 0 else {e: parity(a & witness) for e, a in enumerate(A) if rng.randrange(5) == 0}
        restricted = clamp(w, evidence)
        start = time.perf_counter()
        zpf = pf.partition(restricted)
        pf_seconds = time.perf_counter() - start
        start = time.perf_counter()
        zve = ve.partition(restricted)
        ve_seconds = time.perf_counter() - start
        assert zpf == zve
        tasks.append({"clamped_edges": len(evidence), "pfaffian_seconds": pf_seconds,
                      "variable_elimination_seconds": ve_seconds,
                      "exact_equal": True, "numerator_bits": zpf.numerator.bit_length(),
                      "denominator_bits": zpf.denominator.bit_length()})
    # A cycle with odd parity is inconsistent. Recover a cycle directly from
    # the acquired annihilator, so no fixture is consulted.
    relation = ga.nullspace(K, len(A))[0]
    cyclic = {e: 0 for e in ga.bit_members(relation)}
    cyclic[next(iter(cyclic))] = 1
    assert pf.partition(clamp(weights, cyclic)) == ve.partition(clamp(weights, cyclic)) == 0
    distribution = LearnedDistribution(n, A, ve, weights)
    unconditional = distribution.partition()
    physical_scale = int(learned["constant"]) + sum(abs(int(learned["coefficients"][a])) for a in A)
    physical_partition = unconditional / (1 << physical_scale)
    rare_evidence = {e: 0 for e in range(len(A))}
    rare = distribution.partition(rare_evidence) / unconditional
    source = BitSource(8303)
    sample_calls_before = ve.calls
    start = time.perf_counter()
    partial = {e: 0 for e in range(0, len(A), 5)}
    samples = [distribution.sample(source, partial) for _ in range(8)]
    sample_seconds = time.perf_counter() - start
    assert all(all(parity(A[e] & x) == b for e, b in partial.items()) for x in samples)
    acq_log = {k: v for k, v in learned.items()
               if k not in {"support", "coefficients", "constant", "all_coefficients"}}
    result = {"n": n, "features": len(A), "rank": len(ga.basis(K)),
              "dependency": len(A) - len(ga.basis(K)), "raw_domain_size": 1 << n,
              "acquisition": acq_log, "energy_calls_after_acquisition": 0,
              "graph_acquisition": {"vertices": G["vertices"],
                  "primal_seconds": primal_seconds, "embedding_seconds": embedding_seconds,
                  "primal_cost": {k:v for k,v in G.items() if k not in {"edges","stars","rowspace_certificate"}},
                  "dual_cost": {k:v for k,v in dual.items() if k not in {"edges","stars","rowspace_certificate"}},
                  "euler_certificate": rotation["euler_characteristic"]},
              "retained_pfaffian": {"dimension": pf.size, "compile_seconds": pf_compile_seconds},
              "retained_variable_elimination": {"width": ve.width, "compiled_table_cells": ve.cells,
                  "scalar_multiplication_bound_per_query": ve.scalar_multiplications,
                  "compile_seconds": ve_compile_seconds},
              "actual_task_comparisons": tasks,
              "ordinary_conventional_winner": "retained min-fill variable elimination",
              "physical_partition_at_beta_ln2": {"numerator": physical_partition.numerator,
                  "denominator": physical_partition.denominator, "integerization_scale_power": physical_scale},
              "rare_all_zero_feature_probability": {"numerator": rare.numerator,
                  "denominator": rare.denominator, "decimal": float(rare)},
              "conditional_samples": len(samples), "sample_conditioned_features": len(partial),
              "sample_partition_calls": ve.calls - sample_calls_before,
              "sample_seconds": sample_seconds, "sample_random_bits": source.bits_used,
              "inconsistent_cycle_evidence_returned_zero": True,
              "retained_support": A, "retained_coefficients": [str(learned["coefficients"][a]) for a in A],
              "limitations": ["This exact scalar simulator grants arbitrary configuration preparation; all such calls are charged.",
                  "Graph recognizer is self-contained and complete for its stated bounded-degree, 3-connected promise.",
                  "Exact Pfaffian is the polynomial fallback, not the measured compact-instance winner.",
                  "Feature evidence is closed under this kernel; arbitrary input-coordinate evidence is not included.",
                  "Sampler law follows exact self-reduction; finite sampled feasibility checks are not a statistical proof."]}
    out = HERE.parent / "results" / "learned_planar.json"
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: result[k] for k in ["n","features","rank","dependency","acquisition","graph_acquisition","retained_pfaffian","retained_variable_elimination","ordinary_conventional_winner","rare_all_zero_feature_probability","sample_partition_calls"]}, indent=2))


if __name__ == "__main__":
    main()
