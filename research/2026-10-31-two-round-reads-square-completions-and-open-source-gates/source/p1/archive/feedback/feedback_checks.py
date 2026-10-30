"""Exact finite diagnostics for two-round coordinate acquisition.

Uses only the standard library. Known pairwise factors/prior tables are input;
ordinary optimal adaptive Bellman recursion is the equally-informed baseline.
Every call in the separate unknown-quadratic reconstruction test is counted.
"""

from functools import lru_cache
from fractions import Fraction as Q
from itertools import product
from math import comb, ceil, log
from random import Random
import json
import time


def matching_cover(n, edges):
    used = set()
    matching = []
    for i, j in sorted(edges):
        if i not in used and j not in used:
            used.update((i, j))
            matching.append((i, j))
    assert all(i in used or j in used for i, j in edges)
    return sorted(used), matching


class FinitePairwise:
    def __init__(self, priors, unary, pairwise):
        self.priors = priors
        self.unary = unary
        self.pairwise = pairwise
        self.n = len(priors)

    def value(self, x):
        return sum(self.unary[i][x[i]] for i in range(self.n)) + sum(
            table[x[i], x[j]] for (i, j), table in self.pairwise.items()
        )

    @lru_cache(None)
    def risk(self, state):
        missing = [i for i, x in enumerate(state) if x is None]
        mean = Q(0)
        square = Q(0)
        for choices in product(*(self.priors[i] for i in missing)):
            x = list(state)
            prob = Q(1)
            for i, a in zip(missing, choices):
                x[i] = a
                prob *= self.priors[i][a]
            val = self.value(x)
            mean += prob * val
            square += prob * val * val
        return square - mean * mean

    @lru_cache(None)
    def optimal(self, state, budget):
        best = self.risk(state)
        if budget == 0:
            return best
        for i, x in enumerate(state):
            if x is not None:
                continue
            expected = Q(0)
            for a, prob in self.priors[i].items():
                child = list(state)
                child[i] = a
                expected += prob * self.optimal(tuple(child), budget - 1)
            best = min(best, expected)
        return best

    def conditional_additive_variances(self, cover, values):
        observed = dict(zip(cover, values))
        result = {}
        for i in range(self.n):
            if i in observed:
                continue
            vals = {}
            for a in self.priors[i]:
                val = self.unary[i][a]
                for (j, ell), table in self.pairwise.items():
                    if i == j:
                        assert ell in observed
                        val += table[a, observed[ell]]
                    if i == ell:
                        assert j in observed
                        val += table[observed[j], a]
                vals[a] = val
            mean = sum(self.priors[i][a] * vals[a] for a in vals)
            second = sum(self.priors[i][a] * vals[a] ** 2 for a in vals)
            result[i] = second - mean ** 2
        return result

    def hybrid(self, cover, budget):
        total = Q(0)
        for values in product(*(self.priors[i] for i in cover)):
            prob = Q(1)
            state = [None] * self.n
            for i, a in zip(cover, values):
                state[i] = a
                prob *= self.priors[i][a]
            variances = self.conditional_additive_variances(cover, values)
            residual = sum(sorted(variances.values(), reverse=True)[budget:])
            # Check conditional additivity against independently enumerated risk.
            assert sum(variances.values()) == self.risk(tuple(state))
            assert residual == self.optimal(tuple(state), budget)
            total += prob * residual
        return total


def finite_bellman_checks():
    rng = Random(271828)
    cases = []
    for case in range(10):
        n = 5 + case % 2
        priors = []
        unary = []
        for i in range(n):
            support = [0, 1, 2] if (i + case) % 4 == 0 else [0, 1]
            weights = [rng.randrange(1, 8) for _ in support]
            z = sum(weights)
            priors.append({a: Q(w, z) for a, w in zip(support, weights)})
            unary.append({a: Q(rng.randrange(-4, 5), 3) for a in support})
        pairwise = {}
        for i in range(n):
            for j in range(i + 1, n):
                include = (i == 0 and rng.random() < 0.7) if case < 5 else (rng.random() < 0.25)
                if include:
                    pairwise[i, j] = {
                        (a, b): Q(rng.randrange(-5, 6), 4)
                        for a in priors[i] for b in priors[j]
                    }
        model = FinitePairwise(priors, unary, pairwise)
        cover, matching = matching_cover(n, pairwise)
        row = {"n": n, "edges": len(pairwise), "cover": cover, "budgets": []}
        for k in range(4):
            opt = model.optimal((None,) * n, k)
            hybrid = model.hybrid(cover, k)
            assert hybrid <= opt
            row["budgets"].append({"k": k, "adaptive_risk": str(opt),
                                   "hybrid_risk": str(hybrid),
                                   "hard_hybrid_reads_at_most": min(n, len(cover) + k)})
        cases.append(row)
    return {"cases": cases, "all_comparisons_exact_and_valid": True}


def best_fixed_rare(m, reads):
    p = Q(1, m)
    leaves = 2 * m - 1
    dp = {0: Q(0)}
    for _ in range(m):
        nxt = {}
        for cost, value in dp.items():
            for gate in (0, 1):
                for ell in range(leaves + 1):
                    newcost = cost + gate + ell
                    if newcost > reads:
                        break
                    gain = Q(ell, leaves) * (p if gate else p * p)
                    nxt[newcost] = max(nxt.get(newcost, Q(-1)), value + gain)
        dp = nxt
    return max(dp.values())


def rare_checks():
    results = []
    for m in (2, 3, 4, 5, 8, 13, 20):
        p, leaves, k = Q(1, m), 2 * m - 1, 2 * m
        exact_risk = sum(
            Q(comb(m, a)) * p ** a * (1 - p) ** (m - a)
            * Q(max(0, a * leaves - k), leaves) for a in range(m + 1)
        )
        p2 = 1 - (1 - p) ** m - m * p * (1 - p) ** (m - 1)
        formula = (1 - p) ** m - p2 / leaves
        assert exact_risk == formula
        fixed_gain = best_fixed_rare(m, 3 * m)
        assert fixed_gain <= Q(3 * m, m * leaves)
        assert exact_risk <= Q(m - 1, 2 * m - 1)
        results.append({"m": m, "n": 2 * m * m,
                        "hard_comparator_reads": k,
                        "hard_two_round_reads_at_most": 3 * m,
                        "two_round_risk": str(exact_risk),
                        "two_round_risk_float": float(exact_risk),
                        "best_fixed_risk_at_same_3m_budget": str(1 - fixed_gain),
                        "best_fixed_risk_float": float(1 - fixed_gain)})
    return results


class QuadraticOracle:
    def __init__(self, n, constant, linear, edges):
        self.n, self.constant, self.linear, self.edges = n, constant, linear, edges
        self.calls = 0

    def __call__(self, selected):
        self.calls += 1
        selected = set(selected)
        return self.constant + sum(self.linear[i] for i in selected) + sum(
            a for (i, j), a in self.edges.items() if i in selected and j in selected)


def acquire_cover(oracle, delta, seed):
    """Exact degree-2 Boolean oracle; signed coefficients are allowed."""
    n = oracle.n
    rng = Random(seed)
    c = oracle(())
    linear = [oracle((i,)) - c for i in range(n)]
    tests = ceil(log((n // 2 + 1) / delta) / log(Q(4, 3)))

    @lru_cache(None)
    def q(vertices):
        return oracle(vertices) - c - sum(linear[i] for i in vertices)

    def cross(left, right):
        return q(tuple(sorted(left + right))) - q(tuple(left)) - q(tuple(right))

    def cross_edge(left, right):
        assert cross(left, right) != 0
        while len(left) > 1:
            middle = len(left) // 2
            first, second = left[:middle], left[middle:]
            left = first if cross(first, right) != 0 else second
        while len(right) > 1:
            middle = len(right) // 2
            first, second = right[:middle], right[middle:]
            right = first if cross(left, first) != 0 else second
        return tuple(sorted((left[0], right[0])))

    def inside_edge(vertices):
        assert q(tuple(vertices)) != 0
        assert len(vertices) >= 2
        middle = len(vertices) // 2
        left, right = vertices[:middle], vertices[middle:]
        if q(tuple(left)) != 0:
            return inside_edge(left)
        if q(tuple(right)) != 0:
            return inside_edge(right)
        return cross_edge(left, right)

    remaining = list(range(n))
    matching = []
    while len(remaining) >= 2:
        witness = None
        for _ in range(tests):
            sample = [i for i in remaining if rng.randrange(2)]
            if q(tuple(sample)) != 0:
                witness = sample
                break
        if witness is None:
            break
        edge = inside_edge(witness)
        matching.append(edge)
        remaining = [i for i in remaining if i not in edge]
    cover = sorted(i for edge in matching for i in edge)
    return cover, matching, {"tests_per_stage": tests, "scalar_calls": oracle.calls}


def oracle_checks():
    rng = Random(314159)
    cases = []
    for n, core in ((12, 1), (18, 3), (24, 5), (16, 0)):
        edges = {}
        for i in range(n):
            for j in range(i + 1, n):
                if min(i, j) < core and rng.random() < 0.7:
                    a = rng.choice((-5, -3, -1, 1, 2, 4))
                    edges[i, j] = Q(a, 7)
        oracle = QuadraticOracle(n, Q(2, 3), [Q(rng.randrange(-3, 4), 5) for _ in range(n)], edges)
        cover, matching, meta = acquire_cover(oracle, 1e-6, seed=1000 + n)
        assert all(i in cover or j in cover for i, j in edges)
        assert len(matching) <= core
        assert all(edge in edges for edge in matching)
        cover_calls = oracle.calls
        # Earn a reusable coefficient representation using the learned cover.
        # This diagnostic's calls are separate from later latent measurements.
        c = oracle(())
        singles = [oracle((i,)) for i in range(n)]
        recovered_linear = [val - c for val in singles]
        recovered_edges = {}
        for i in range(n):
            for j in range(i + 1, n):
                if i in cover or j in cover:
                    a = oracle((i, j)) - singles[i] - singles[j] + c
                    if a:
                        recovered_edges[i, j] = a
        assert c == oracle.constant
        assert recovered_linear == oracle.linear
        assert recovered_edges == oracle.edges
        cases.append({"n": n, "supplied_upper_bound_on_cover_size": core,
                      "nonzero_edges": len(edges), "learned_cover": cover,
                      "all_true_edges_covered": True, **meta,
                      "cover_scalar_calls": cover_calls,
                      "total_scalar_calls_with_full_model_recovery": oracle.calls,
                      "all_coefficients_recovered_exactly": True})
    return {"cases": cases, "scope": "Seeded finite exact diagnostics, not a deterministic certification of zero coefficients."}


def expected_budget_counterexample():
    m = 9
    p = Q(1, m)
    return {"m": m,
            "adaptive_expected_reads": str(1 + p * m),
            "adaptive_risk": "0",
            "first_gate_then_two_leaf_risk": str(p * Q(m - 2, m)),
            "explanation": "The rare branch needs m leaf reads; replacing its conditional budget by unconditional k=2 fails."}


if __name__ == "__main__":
    start = time.perf_counter()
    results = {"finite_bellman": finite_bellman_checks(),
               "rare_gate_comparison": rare_checks(),
               "unknown_graph_cover": oracle_checks(),
               "expected_budget_counterexample": expected_budget_counterexample()}
    results["wall_seconds"] = time.perf_counter() - start
    print(json.dumps(results, indent=2))
