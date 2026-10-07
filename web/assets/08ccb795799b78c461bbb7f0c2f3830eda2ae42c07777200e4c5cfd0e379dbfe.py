"""Finite exact fixtures for repulsive_filter_audit; no FPRAS implementation."""
from __future__ import annotations

import itertools
import json
import math
from fractions import Fraction
from pathlib import Path

import numpy as np
import sympy as sp


def subsets(n, k=None):
    if k is None:
        return [tuple(i for i in range(n) if mask >> i & 1) for mask in range(1 << n)]
    return list(itertools.combinations(range(n), k))


def residual_hessian(q, tables, t):
    """Normalized Hessian of a quadratic derivative of complementary g."""
    site = [j for j, size in enumerate(q) for _ in range(size - t[j])]
    rho = {}
    for j, size in enumerate(q):
        remaining = size - t[j]
        if remaining >= 2:
            b = tables[j]
            rho[j] = sp.Rational(b[remaining] * b[remaining - 2], b[remaining - 1] ** 2)
    return sp.Matrix(len(site), len(site), lambda i, k:
                     0 if i == k else (rho[site[i]] if site[i] == site[k] else 1))


def check_all_residuals(q, tables):
    checked = 0
    max_second = -float("inf")
    for t in itertools.product(*(range(size + 1) for size in q)):
        remaining = sum(q) - sum(t)
        if remaining < 2:
            continue
        H = residual_hessian(q, tables, t)
        eig = np.linalg.eigvalsh(np.array(H, dtype=float))
        max_second = max(max_second, float(eig[-2]))
        assert np.count_nonzero(eig > 1e-8) <= 1, (q, t, eig)
        checked += 1
    return {"patterns_checked": checked, "largest_second_eigenvalue": max_second}


def physical_weight(S, blocks, tables):
    return sp.prod(tables[j][len(set(S) & set(block))] for j, block in enumerate(blocks))


def determinant_count_fixture():
    A = sp.Matrix([
        [1, 0, 1], [0, 1, sp.I], [1, 1, 0],
        [1, 2, 1], [sp.I, 1, 2], [2, 0, 1-sp.I],
    ])
    n, r = A.shape
    blocks = [(0, 1), (2, 3), (4, 5)]
    tables = [[1, 1, 2], [1, 1, sp.Rational(7, 4)], [1, 1, sp.Rational(1, 3)]]
    coeff = {}
    for S in subsets(n, r):
        determinant = A.extract(S, range(r)).det()
        coeff[S] = sp.expand(determinant * sp.conjugate(determinant))
    direct = sum(coeff[S] * physical_weight(S, blocks, tables) for S in coeff)
    # [x_all] f_A g is precisely this complement sum.
    convolution = 0
    for T in subsets(n, n-r):
        S = tuple(i for i in range(n) if i not in T)
        g_coefficient = sp.prod(tables[j][len(block) - len(set(T) & set(block))]
                               for j, block in enumerate(blocks))
        convolution += coeff[S] * g_coefficient
    assert sp.simplify(direct - convolution) == 0
    prefix_checks = 0
    for depth in range(n + 1):
        for bits in itertools.product((0, 1), repeat=depth):
            included = {i for i, bit in enumerate(bits) if bit}
            excluded = set(range(depth)) - included
            expected = sum(v * physical_weight(S, blocks, tables)
                           for S, v in coeff.items()
                           if included <= set(S) and not (excluded & set(S)))
            remaining = list(range(depth, n))
            rebuilt = 0
            for W in subsets(len(remaining), r-len(included)) if 0 <= r-len(included) <= len(remaining) else []:
                S = tuple(sorted(included | {remaining[i] for i in W}))
                shifted = sp.prod(tables[j][len(included & set(block)) +
                                           len((set(S)-included) & set(block))]
                                  for j, block in enumerate(blocks))
                rebuilt += coeff[S] * shifted
            assert sp.simplify(expected - rebuilt) == 0
            prefix_checks += 1
    return {"A_rank": A.rank(), "normalizer": str(direct), "prefixes_checked": prefix_checks}


def independence_fixture():
    blocks = [{0, 1, 2}, {3, 4}, {5}]
    lower, upper, rank = [1, 0, 0], [2, 1, 1], 3
    bases = [set(S) for S in subsets(6, rank)
             if all(lower[j] <= len(set(S) & block) <= upper[j]
                    for j, block in enumerate(blocks))]
    for I in map(set, subsets(6)):
        oracle = all(len(I & block) <= upper[j] for j, block in enumerate(blocks)) and \
                 sum(max(lower[j], len(I & block)) for j, block in enumerate(blocks)) <= rank
        extension = any(I <= B for B in bases)
        assert oracle == extension, I
    for X, Y in itertools.product(bases, repeat=2):
        for a in X-Y:
            assert any((X-{a}) | {b} in bases for b in Y-X)
    return {"subsets_checked": 64, "bases": len(bases)}


def hard_gutzwiller_fixture():
    A = sp.Matrix([
        [1, 0, 1], [0, 1, sp.I], [1, 1, 0],
        [1, 2, 1], [sp.I, 1, 2], [2, 0, 1-sp.I],
    ])
    blocks = [(0, 1), (2, 3), (4, 5)]
    tables = [[1, 1, 0]] * 3
    totals = {}
    for r in (2, 3):
        Ar = A[:, :r]
        value = 0
        allowed = 0
        for S in subsets(6, r):
            weight = physical_weight(S, blocks, tables)
            if weight:
                allowed += 1
                det = Ar.extract(S, range(r)).det()
                value += sp.expand(det * sp.conjugate(det))
        totals[str(r)] = {"allowed_support_sets": allowed, "normalizer": str(value)}
        assert value > 0
    impossible = sp.zeros(6, 3)
    for j in range(3):
        impossible[j, j] = 1
    assert impossible.rank() == 3
    zero = sum(abs(impossible.extract(S, range(3)).det())**2 *
               physical_weight(S, blocks, tables) for S in subsets(6, 3))
    assert zero == 0
    return {"doped_and_half_filled": totals, "full_rank_zero_filtered_norm": str(zero)}


def purification_fixture():
    n = 3
    B = sp.Matrix([[1, sp.I/2, 0], [sp.Rational(1, 3), 1, 1], [1, 0, 2-sp.I]])
    A = B.col_join(sp.eye(n))
    blocks = [(0, 1), (2,)]
    tables = [[1, 1, sp.Rational(1, 2)], [1, 2]]
    physical_sets = subsets(n)
    amplitude = {}
    for S in physical_sets:
        for T in subsets(n, n-len(S)):
            rows = list(S) + [n+i for i in T]
            amplitude[S, T] = sp.simplify(A.extract(rows, range(n)).det() *
                                           sp.sqrt(physical_weight(S, blocks, tables)))
    reduced = sp.zeros(1 << n)
    expected = sp.zeros(1 << n)
    L = B * sp.conjugate(B.T)
    checked = 0
    for i, S in enumerate(physical_sets):
        for j, U in enumerate(physical_sets):
            if len(S) != len(U):
                continue
            reduced[i, j] = sp.simplify(sum(amplitude[S, T] * sp.conjugate(amplitude[U, T])
                                             for T in subsets(n, n-len(S))))
            expected[i, j] = sp.simplify(L.extract(S, U).det() *
                                         sp.sqrt(physical_weight(S, blocks, tables) *
                                                 physical_weight(U, blocks, tables)))
            assert sp.simplify(reduced[i, j] - expected[i, j]) == 0, (S, U)
            checked += 1
    assert reduced == expected
    return {"matrix_entries_checked": checked, "trace": str(sp.trace(reduced)),
            "identity": "Tr_anc |Slater([B;I]) filtered><...| = D Gamma(B B*) D"}


def interacting_gibbs_obstruction():
    states = subsets(4, 2)
    # One down-spin hopping term between the two sites (mode indices 1 and 3).
    H = sp.zeros(len(states))
    for col, S in enumerate(states):
        for source, target in [(1, 3), (3, 1)]:
            if source in S and target not in S:
                after = list(S)
                sign = (-1) ** after.index(source)
                after.remove(source)
                sign *= (-1) ** sum(i < target for i in after)
                after.append(target)
                after.sort()
                H[states.index(tuple(after)), col] += sign
    V = sp.diag(*[int({0, 1} <= set(S)) + int({2, 3} <= set(S)) for S in states])
    split_cubic = sp.zeros(len(states))
    for i in range(4):
        for j in range(4-i):
            k = 3-i-j
            split_cubic -= V**i * H**j * V**k / (2**(i+k) * math.factorial(i) *
                                                math.factorial(j) * math.factorial(k))
    exact_cubic = -(H+V)**3 / sp.factorial(3)
    difference = sp.simplify(split_cubic-exact_cubic)
    nonzero = [(i, j, str(difference[i, j])) for i in range(len(states))
               for j in range(len(states)) if difference[i, j] != 0]
    assert nonzero
    return {"commutator_nonzero": H*V-V*H != sp.zeros(len(states)),
            "beta_cubed_difference_nonzero_entries": nonzero}


def bcs_weight_fixture():
    for n in range(1, 5):
        for t in [sp.Rational(1, 2), sp.Rational(3, 4), 1, 2]:
            g = sp.sqrt(t)
            for u in itertools.product((0, 1), repeat=n):
                for holes in itertools.product((0, 1), repeat=n):
                    original = sp.prod(g**(u[j] * (1-holes[j])) for j in range(n))
                    row_scaled = sp.prod(g**u[j] for j in range(n))
                    load_filter = sp.prod((1/g)**(u[j] * holes[j]) for j in range(n))
                    assert sp.simplify(original-row_scaled*load_filter) == 0
    return {"configurations_checked": 4 * sum(4**n for n in range(1, 5)),
            "identity": "g^(u*(1-h)) = g^u * (1/g)^(u*h)"}


def main():
    results = {}
    results["q2_all_ranks"] = check_all_residuals([2]*4,
        [[1, 1, a] for a in [2, sp.Rational(7, 4), sp.Rational(3, 2), sp.Rational(1, 2)]])
    results["factorial_q3_all_ranks"] = check_all_residuals([3, 3], [[1, 1, 2, 6]]*2)
    results["factorial_mixed_blocks_all_ranks"] = check_all_residuals([2, 3, 4],
        [[math.factorial(k) for k in range(q+1)] for q in [2, 3, 4]])
    a = sp.Rational(9, 4)
    H = residual_hessian([2, 2], [[1, 1, a]]*2, [0, 0])
    v = sp.Matrix([1, 1, -1, -1])
    curvature = (v.T*H*v)[0] / (2*a+4)
    assert curvature == sp.Rational(2, 17)
    results["sharp_q2_obstruction"] = {"a": str(a), "H_eigenvalues": [str(x) for x in H.eigenvals()],
                                       "log_Hessian_direction_at_ones": str(curvature)}
    # Direct polynomial is not the complement: b=k! has direct within=2, cross=1.
    Hd = sp.Matrix(6, 6, lambda i, j: 0 if i == j else (2 if i//3 == j//3 else 1))
    results["wrong_orientation_obstruction"] = {"direct_q3_rank2_eigenvalues":
                                                {str(e): mult for e, mult in Hd.eigenvals().items()}}
    assert sum(mult for e, mult in Hd.eigenvals().items() if e > 0) == 2
    results["determinant_counts"] = determinant_count_fixture()
    results["bounded_load_matroid"] = independence_fixture()
    results["hard_gutzwiller"] = hard_gutzwiller_fixture()
    results["finite_temperature_purification"] = purification_fixture()
    results["interacting_gibbs_obstruction"] = interacting_gibbs_obstruction()
    results["bcs_reweight"] = bcs_weight_fixture()
    target = Path(__file__).with_name("repulsive_filter_check_results.json")
    target.write_text(json.dumps(results, indent=2)+"\n")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
