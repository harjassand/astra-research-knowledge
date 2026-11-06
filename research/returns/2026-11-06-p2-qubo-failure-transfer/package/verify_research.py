#!/usr/bin/env python3
"""Exact, single-process checks for scoped QUBO research results.

This is NOT a polynomial-time unrestricted QUBO algorithm.  The reference
solver enumerates all assignments.  Finite checks below supplement, and do
not replace, the quantified proofs in RESEARCH_REPORT.txt.

Run: python3 verify_research.py
Only the Python standard library is used.  No network, worker, or device.
"""

from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations, permutations
from math import comb
from pathlib import Path
import hashlib
import json
import platform
import time


@dataclass
class QUBO:
    c: int
    a: list[int]
    b: dict[tuple[int, int], int]

    def __post_init__(self):
        assert isinstance(self.c, int)
        assert all(isinstance(v, int) for v in self.a)
        assert all(0 <= i < j < len(self.a) and isinstance(v, int)
                   for (i, j), v in self.b.items())

    @property
    def n(self):
        return len(self.a)

    def energy(self, mask):
        assert 0 <= mask < (1 << self.n)
        return (self.c
                + sum(v for i, v in enumerate(self.a) if (mask >> i) & 1)
                + sum(v for (i, j), v in self.b.items()
                      if (mask >> i) & 1 and (mask >> j) & 1))

    def exhaustive_minimum(self):
        # Exponential reference, with deterministic tie-breaking by mask.
        value, mask = min((self.energy(x), x) for x in range(1 << self.n))
        return value, [(mask >> i) & 1 for i in range(self.n)]

    def fixture(self):
        # Exact signed binary strings; every variable is explicitly listed.
        return {
            "variables": [f"x{i + 1}" for i in range(self.n)],
            "coefficient_encoding": "signed base-2 strings without prefix",
            "constant": format(self.c, "b"),
            "linear": [format(v, "b") for v in self.a],
            "quadratic": [[i + 1, j + 1, format(v, "b")]
                          for (i, j), v in sorted(self.b.items()) if v],
        }


def star(k):
    return QUBO(0, [0] * k + [1], {(i, k): -1 for i in range(k)})


def weighted_square(weights, target):
    n = len(weights)
    return QUBO(target * target,
                [w * w - 2 * target * w for w in weights],
                {(i, j): 2 * weights[i] * weights[j]
                 for i, j in combinations(range(n), 2)})


def grid(k):
    edges = []
    for r in range(k):
        for c in range(k):
            u = r * k + c
            if c + 1 < k:
                edges.append((u, u + 1))
            if r + 1 < k:
                edges.append((u, u + k))
    a = [0] * (k * k)
    a[0] = 1
    for u, v in edges:
        a[u] += 1
        a[v] += 1
    return QUBO(0, a, {(u, v): -2 for u, v in edges}), edges


def subset_sums(weights):
    sums = [0]
    for w in weights:
        sums += [s + w for s in sums]
    return sorted(sums)


def determinant(matrix):
    a = [[Fraction(x) for x in row] for row in matrix]
    n = len(a)
    result = Fraction(1)
    for i in range(n):
        pivot = next((r for r in range(i, n) if a[r][i]), None)
        if pivot is None:
            return Fraction(0)
        if pivot != i:
            a[pivot], a[i] = a[i], a[pivot]
            result = -result
        p = a[i][i]
        result *= p
        for r in range(i + 1, n):
            q = a[r][i] / p
            for c in range(i + 1, n):
                a[r][c] -= q * a[i][c]
            a[r][i] = 0
    return result


def audit_star():
    rows = []
    for k in range(2, 13):
        values = [min(0, 1 - x.bit_count()) for x in range(1 << k)]
        coefficients = values[:]
        for i in range(k):
            for mask in range(1 << k):
                if mask & (1 << i):
                    coefficients[mask] -= coefficients[mask ^ (1 << i)]
        for mask, value in enumerate(coefficients):
            degree = mask.bit_count()
            expected = (-1) ** (degree + 1) if degree >= 2 else 0
            assert value == expected
        for mask, value in enumerate(values):
            factored = 1 - mask.bit_count() - (1 if mask == 0 else 0)
            assert value == factored
        q = star(k)
        actual_min, assignment = q.exhaustive_minimum()
        assert actual_min == 1 - k
        rows.append({"k": k, "nonzero_monomials": sum(v != 0 for v in coefficients),
                     "expected": (1 << k) - k - 1,
                     "minimum": actual_min, "minimizer": assignment})
    return rows


def audit_minplus_square():
    splits = 0
    strict_pairs = 0
    for n in range(2, 11):
        all_bits = (1 << n) - 1
        for mask in range(1, all_bits):
            if n > 8 and mask.bit_count() != n // 2:
                continue
            u = subset_sums([1 << i for i in range(n) if (mask >> i) & 1])
            v = subset_sums([1 << i for i in range(n) if not ((mask >> i) & 1)])
            m = min(len(u), len(v))
            u, v = u[:m], list(reversed(v[:m]))
            target = ((1 << n) - 1) // 3
            for i, j in combinations(range(m), 2):
                diagonal = (u[i] + v[i] - target) ** 2 + (u[j] + v[j] - target) ** 2
                cross = (u[i] + v[j] - target) ** 2 + (u[j] + v[i] - target) ** 2
                gap = cross - diagonal
                assert gap == 2 * (u[j] - u[i]) * (v[i] - v[j]) >= 2
                strict_pairs += 1
            splits += 1
    u, v, target = [0, 1, 4, 5], [0, 2, 8, 10], 5
    matrix = [[(a + b - target) ** 2 for b in v] for a in u]
    costs = [(sum(matrix[i][p[i]] for i in range(4)), p)
             for p in permutations(range(4))]
    best = min(c for c, _ in costs)
    minimizers = [list(p) for c, p in costs if c == best]
    assert minimizers == [[3, 2, 1, 0]]
    return {"checked_variable_splits": splits, "checked_strict_pairs": strict_pairs,
            "four_by_four_matrix": matrix, "assignment_minimum": best,
            "unique_assignment_permutation": minimizers[0]}


def induced_cross_matching(edges, left_mask):
    cross = []
    for u, v in edges:
        if ((left_mask >> u) ^ (left_mask >> v)) & 1:
            cross.append((u, v) if (left_mask >> u) & 1 else (v, u))
    neighbors = {}
    for u, v in cross:
        neighbors.setdefault(u, set()).add(v)
        neighbors.setdefault(v, set()).add(u)
    remaining = cross[:]
    selected = []
    while remaining:
        u, v = remaining[0]
        selected.append((u, v))
        banned = neighbors[u] | neighbors[v]
        remaining = [(a, b) for a, b in remaining if a not in banned and b not in banned]
    for i, (u, v) in enumerate(selected):
        for a, b in selected[i + 1:]:
            assert a != u and b != v
            assert b not in neighbors[u] and v not in neighbors[a]
    assert 32 * len(selected) >= len(cross)
    return cross, selected


def audit_grid():
    k = 4
    q, edges = grid(k)
    cut_count = 0
    smallest_cut = len(edges)
    for chosen in combinations(range(k * k), k * k // 2):
        mask = sum(1 << i for i in chosen)
        cross, matching = induced_cross_matching(edges, mask)
        assert len(cross) >= k
        smallest_cut = min(smallest_cut, len(cross))
        assert 32 * len(matching) >= k
        cut_count += 1
    structured = []
    masks = [sum(1 << (r * k + c) for r in range(k) for c in range(k)
                 if rule(r, c))
             for rule in (lambda r, c: r < k // 2,
                          lambda r, c: c < k // 2,
                          lambda r, c: (r + c) % 2 == 0)]
    for left_mask in masks:
        _, matching = induced_cross_matching(edges, left_mask)
        chosen = matching[:3]
        m = len(chosen)
        energies = {}
        for a in range(1 << m):
            for b in range(1 << m):
                assignment = sum(((a >> i) & 1) << u | ((b >> i) & 1) << v
                                 for i, (u, v) in enumerate(chosen))
                energies[a, b] = q.energy(assignment)
        for a in range(1 << m):
            for b in range(1 << m):
                row = energies[a, 0] - a.bit_count()
                column = energies[0, b] - b.bit_count()
                assert energies[a, b] == (a ^ b).bit_count() + row + column
        structured.append({"left_mask": left_mask, "matching_size": len(matching),
                           "restricted_checked_matching_size": m})
    optimum, assignment = q.exhaustive_minimum()
    zero_count = sum(q.energy(x) == 0 for x in range(1 << q.n))
    assert optimum == 0 and assignment == [0] * q.n and zero_count == 1
    return {"grid_side": k, "balanced_cuts_checked": cut_count,
            "minimum_crossing_edges": smallest_cut,
            "restricted_kernel_checks": structured,
            "unique_global_minimum": 0}


def audit_submodular_contacts():
    checked = 0
    rows = []
    for n in range(2, 9):
        k = n // 2
        full = (1 << n) - 1
        layer = [x for x in range(1 << n) if x.bit_count() == k]
        for flip in range(1 << n):
            unflipped = full ^ flip
            for x, y in combinations(layer, 2):
                if (x & flip) != (y & flip) and (x & unflipped) != (y & unflipped):
                    continue
                meet = ((x ^ flip) & (y ^ flip)) ^ flip
                join = ((x ^ flip) | (y ^ flip)) ^ flip
                gap = (meet.bit_count() - k) ** 2 + (join.bit_count() - k) ** 2
                assert gap >= 2
                checked += 1
        numerator, denominator = comb(n, k), 1 << (n // 2)
        rows.append({"n": n, "middle_layer": numerator,
                     "unflipped_component_lower_bound": numerator,
                     "arbitrary_flip_component_lower_bound":
                     (numerator + denominator - 1) // denominator})
    return {"exact_oriented_contact_inequalities_checked": checked, "bounds": rows}


def audit_sdp():
    q = QUBO(0, [-31, -30, -28], {(0, 1): 32, (0, 2): 32, (1, 2): 32})
    f = Fraction
    moment = [[f(1), f(1, 2), f(1, 2), f(1, 2)],
              [f(1, 2), f(1, 2), f(1, 8), f(1, 8)],
              [f(1, 2), f(1, 8), f(1, 2), f(1, 8)],
              [f(1, 2), f(1, 8), f(1, 8), f(1, 2)]]
    principal_minors = []
    for size in range(1, 5):
        for subset in combinations(range(4), size):
            d = determinant([[moment[i][j] for j in subset] for i in subset])
            assert d >= 0
            principal_minors.append({"indices": list(subset), "determinant": str(d)})
    expectation = sum(f(a, 2) for a in q.a) + sum(f(b, 8) for b in q.b.values())
    assert expectation == -f(65, 2)
    value, assignment = q.exhaustive_minimum()
    assert (value, assignment) == (-31, [1, 0, 0])
    assert sum(q.energy(x) == value for x in range(8)) == 1
    return {"all_energies_by_mask": [q.energy(x) for x in range(8)],
            "minimum": value, "unique_minimizer": assignment,
            "feasible_pseudomoment_objective": str(expectation),
            "gap_to_true_minimum": str(value - expectation),
            "moment_matrix": [[str(v) for v in row] for row in moment],
            "principal_minors": principal_minors,
            "pair_marginals_00_01_10_11": ["1/8", "3/8", "3/8", "1/8"]}


def transfer_objects():
    # Deliberately contains objects, failed claims, scope and numerical witnesses,
    # not proof narratives or preferred repairs.
    qgrid, _ = grid(4)
    return {
        "status": "UNRESTRICTED_QUBO_UNRESOLVED",
        "transfer_rule": "Objects and exact failed-claim scopes only; no preferred repairs or proof narratives.",
        "objects": [
            {"id": "F1_STAR_ELIMINATION", "family": "E_k(x,y)=y*(1-sum_i x_i), k>=2",
             "failed_claim": "One-variable exact elimination keeps the explicit multilinear monomial list polynomial in the QUBO input length.",
             "scope": "Explicit monomial representation after eliminating y; not factored circuits or all algorithms.",
             "witness": {"eliminated_function": "min(0,1-sum_i x_i)",
                         "nonzero_monomials": "2^k-k-1", "maximum_degree": "k"},
             "fixture": star(5).fixture()},
            {"id": "F2_WEIGHTED_SQUARE_MINPLUS", "family": "E_n(x)=(sum_i 2^(i-1)*x_i-T)^2, 0<=T<2^n",
             "failed_claim": "Every quadratic energy admits a polynomial-state exact, or uniformly <1/2-error, min-plus representation across at least one balanced bipartition of its variables.",
             "scope": "Representations H(x_A,x_B)=min_{s<=r}(f_s(x_A)+g_s(x_B)); whole-function uniform error, arbitrary real factors. Not arbitrary symbolic arithmetic or minimum-only computation.",
             "witness": {"state_lower_bound": "2^min(|A|,|B|) for every split A|B",
                         "easy_optimum": "0 at the ordinary binary expansion of T"},
             "fixture": weighted_square([1, 2, 4, 8], 5).fixture()},
            {"id": "F3_BOUNDED_COEFFICIENT_GRID_MINPLUS", "family": "E_G(x)=x_(0,0)+sum_grid_edges (x_u-x_v)^2 on an even k by k grid",
             "failed_claim": "Bounded integer coefficients guarantee polynomial exact or uniformly <1/2-error min-plus separation width after choosing a variable ordering.",
             "scope": "Same separated-state representation as F2, at every balanced split; not general algorithms, including min-cut.",
             "witness": {"state_lower_bound": "2^ceil(k/32)",
                         "coefficient_bound": "|a_i|<=5, |b_ij|<=2",
                         "easy_unique_optimum": "0 at all-zero assignment"},
             "fixture": qgrid.fixture()},
            {"id": "F4_SUBMODULAR_ENVELOPE", "family": "E_n(x)=(sum_i x_i-floor(n/2))^2",
             "failed_claim": "Every QUBO admits a polynomial-size pointwise minimum of submodular components, each allowed its own fixed coordinate complements, with uniform additive error <1/2.",
             "scope": "Finite pointwise minimum; each component submodular after a fixed coordinate-complement map. Includes partial minimization of jointly submodular auxiliary models. Not arbitrary optimization-preserving reductions or other tractable families.",
             "witness": {"component_lower_bound_with_complements": "ceil(binomial(n,floor(n/2))/2^floor(n/2))",
                         "component_lower_bound_without_complements": "binomial(n,floor(n/2))",
                         "easy_optimum": "0 at any assignment of Hamming weight floor(n/2)"},
             "fixture": weighted_square([1] * 6, 3).fixture()},
            {"id": "F5_THREE_BIT_PSD_GAP", "family": "E(x)=-31*x1-30*x2-28*x3+32*(x1*x2+x1*x3+x2*x3)",
             "failed_claim": "The first Boolean moment SDP, even with all valid pairwise marginal inequalities, always has a lower bound sufficient to recover an integer optimum by ceiling.",
             "scope": "This relaxation and its degree-two affine-SOS/Boolean dual certificates; not higher-order certificates or all algorithms.",
             "witness": {"minimum": -31, "unique_minimizer": [1, 0, 0],
                         "feasible_relaxation_value": "-65/2",
                         "first_moments": ["1/2"] * 3,
                         "distinct_pair_moments": ["1/8"] * 3},
             "fixture": QUBO(0, [-31, -30, -28], {(0, 1): 32, (0, 2): 32, (1, 2): 32}).fixture()},
        ],
    }


def main():
    root = Path(__file__).resolve().parent
    wall_start, cpu_start = time.perf_counter(), time.process_time()
    results = {
        "status": "ALL_LISTED_FINITE_CHECKS_PASSED",
        "scope": "Exact finite diagnostics, not a proof of unrestricted polynomial solvability or a general lower bound.",
        "python_version": platform.python_version(),
        "integer_arithmetic": "Python arbitrary precision; Fraction for rational matrices",
        "star": audit_star(),
        "minplus_square": audit_minplus_square(),
        "grid": audit_grid(),
        "submodular_contacts": audit_submodular_contacts(),
        "sdp": audit_sdp(),
    }
    results["process_cpu_seconds"] = time.process_time() - cpu_start
    results["wall_seconds"] = time.perf_counter() - wall_start
    results["code_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    results["resource_scope"] = "This one audit process only; model inference and source retrieval costs not measured."
    (root / "audit_results.json").write_text(json.dumps(results, indent=2) + "\n")
    (root / "FAILURE_OBJECTS_ONLY.json").write_text(json.dumps(transfer_objects(), indent=2) + "\n")
    print(json.dumps({"status": results["status"],
                      "cpu_seconds": results["process_cpu_seconds"],
                      "wall_seconds": results["wall_seconds"],
                      "minplus_splits": results["minplus_square"]["checked_variable_splits"],
                      "grid_bisections": results["grid"]["balanced_cuts_checked"],
                      "oriented_contacts": results["submodular_contacts"]["exact_oriented_contact_inequalities_checked"]}, indent=2))


if __name__ == "__main__":
    main()
