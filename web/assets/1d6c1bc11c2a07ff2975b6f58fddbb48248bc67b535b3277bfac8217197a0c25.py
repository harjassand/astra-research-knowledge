#!/usr/bin/env python3
"""Exact rational-square-variant tests for weighted PM -> fixed Z.

Standard library only. The proof and finite-bit analysis are in RESULT.txt;
these small fixtures are exact corroboration, not a substitute for the proof.
"""
from fractions import Fraction as F
from itertools import combinations
from math import comb
import json
from pathlib import Path

from check_exact import (ceil_log2_fraction, ceil_log2_integer, det, eye,
                         fmt, inverse, matmul, target_z, transpose,
                         paired_weights)


def square_atoms(w):
    """Return nonnegative rationals a_i with sum a_i^2 = w, in poly time."""
    w = F(w)
    if w <= 0:
        if w == 0:
            return []
        raise ValueError("weight must be nonnegative")
    p, q = w.numerator, w.denominator
    integer = p * q
    atoms = []
    for j in range(integer.bit_length()):
        if (integer >> j) & 1:
            root = 1 << (j // 2)
            if j % 2:
                atoms.extend((F(root, q), F(root, q)))
            else:
                atoms.append(F(root, q))
    assert sum((a * a for a in atoms), F(0)) == w
    assert len(atoms) <= 2 * integer.bit_length()
    return atoms


def weighted_pm_count(m, edges):
    adj = [[] for _ in range(m)]
    for u, v, w in edges:
        w = F(w)
        if w > 0:
            adj[u].append((v, w))
            adj[v].append((u, w))

    def rec(mask):
        if mask == 0:
            return F(1)
        u = (mask & -mask).bit_length() - 1
        rest = mask ^ (1 << u)
        return sum((w * rec(rest ^ (1 << v)) for v, w in adj[u]
                    if (rest >> v) & 1), F(0))

    return rec((1 << m) - 1)


def find_positive_pm(m, edges):
    adj = [[] for _ in range(m)]
    for u, v, w in edges:
        w = F(w)
        if w > 0:
            adj[u].append((v, w))
            adj[v].append((u, w))

    def rec(mask):
        if mask == 0:
            return F(1)
        u = (mask & -mask).bit_length() - 1
        rest = mask ^ (1 << u)
        for v, w in adj[u]:
            if (rest >> v) & 1:
                tail = rec(rest ^ (1 << v))
                if tail:
                    return w * tail
        return F(0)

    return rec((1 << m) - 1)


def weighted_gadget(m, edges):
    """Build coordinate-pair gadget, exactly encoding rational edge weights."""
    original_value = weighted_pm_count(m, edges)
    if m == 0:
        assert original_value == 1
        return None, dict(branch="empty", source_value=original_value)
    positive = [(u, v, F(w)) for u, v, w in edges if F(w) > 0]
    if not positive:
        assert original_value == 0
        return None, dict(branch="zero-support", source_value=original_value)
    if find_positive_pm(m, positive) == 0:
        assert original_value == 0
        return None, dict(branch="infeasible-support", source_value=original_value)

    m2 = m
    padded = False
    if len(positive) < m:
        u, v = m, m + 1
        positive = positive + [(u, v, F(1))] + [(u, w, F(1)) for w in range(m)]
        m2 = m + 2
        padded = True

    edge_variants = []
    for u, v, w in positive:
        if u > v:
            u, v = v, u
        edge_variants.extend((u, v, a) for a in square_atoms(w))
    edge_variant_count = len(edge_variants)
    dummies = edge_variant_count - m2
    assert dummies >= 0
    n = edge_variant_count + dummies
    k = n // 2
    assert n == m2 + 2 * dummies and n % 2 == 0

    b = [[F(0) for _ in range(n)] for _ in range(n)]
    c = [[F(0) for _ in range(n)] for _ in range(n)]
    for j, (u, v, amplitude) in enumerate(edge_variants):
        b[u][j] = 1
        c[v][j] = amplitude
    for j in range(dummies):
        b[m2 + 2 * j][edge_variant_count + j] = 1
        c[m2 + 2 * j + 1][edge_variant_count + j] = 1

    amplitudes = [a for _, _, a in edge_variants] + [F(1)] * dummies
    # W = e_k(a_1^2,...,a_N^2), computed by a polynomial-time exact DP.
    dp = [F(0)] * (k + 1)
    dp[0] = F(1)
    seen = 0
    for a in amplitudes:
        seen += 1
        for j in range(min(k, seen), 0, -1):
            dp[j] += dp[j - 1] * a * a
    W = dp[k]
    assert W > 0
    f = [next(i for i in range(n) if b[i][j]) for j in range(n)]
    assert all(sum(b[i][j] for i in range(n)) == 1 for j in range(n))

    # The source denominator grid only needs the original r=m/2 edge weights.
    Delta = 1
    for _, _, w in positive:
        Delta *= F(w).denominator
    return (b, c), dict(branch="constructed", source_value=original_value,
                        m=m, padded_m=m2, original_edges=len(edges),
                        positive_or_padded_edges=len(positive), padded=padded,
                        variants=edge_variant_count, dummies=dummies,
                        n=n, k=k, source_r=m // 2, W=W, Delta=Delta,
                        amplitudes=amplitudes, functional_map=f)


def rational_det_poly(b, c, sites):
    n = len(b)
    k = len(sites)
    coeffs = [F(0)] * (k + 1)
    for mask in range(1 << k):
        cols = []
        for r, j in enumerate(sites):
            if (mask >> r) & 1:
                cols.append([F(i == j) for i in range(n)])
            else:
                cols.append([b[i][j] for i in range(n)])
            cols.append([c[i][j] for i in range(n)])
        coeffs[mask.bit_count()] += det(transpose(cols))
    return coeffs


def weighted_R_poly(b, c):
    n = len(b)
    k = n // 2
    total = [F(0)] * (n + 1)
    for sites in combinations(range(n), k):
        p = rational_det_poly(b, c, sites)
        for i, x in enumerate(p):
            for j, y in enumerate(p):
                total[i + j] += x * y
    return total


def eval_poly(p, x):
    return sum((a * x ** j for j, a in enumerate(p)), F(0))


def nearest_integer(x):
    y = F(x) + F(1, 2)
    return y.numerator // y.denominator


def check_weighted(name, m, edges):
    gadget, meta = weighted_gadget(m, edges)
    if meta["branch"] != "constructed":
        return dict(name=name, branch=meta["branch"],
                    source_value=fmt(meta["source_value"]))
    b, c = gadget
    n, k = meta["n"], meta["k"]
    P = meta["source_value"]
    coeffs = weighted_R_poly(b, c)
    assert coeffs[0] == P, (name, coeffs[0], P)
    W = meta["W"]
    coeff_bounds = [W * comb(n, ell) for ell in range(n + 1)]
    assert all(abs(x) <= bound for x, bound in zip(coeffs, coeff_bounds))
    assert meta["Delta"] ** meta["source_r"] * P == int(
        meta["Delta"] ** meta["source_r"] * P)

    L = find_positive_pm(m, edges)
    assert L > 0 and W >= L
    h = ceil_log2_integer(n)
    grid = meta["Delta"] ** meta["source_r"]
    assert W * grid >= 1
    q_exact = n + h + 4 + ceil_log2_fraction(W * grid)
    eps_exact = F(1, 1 << q_exact)
    R_exact = eval_poly(coeffs, eps_exact)
    direct = sum(paired_weights(b, c, eps_exact).values(), F(0))
    assert R_exact == direct
    coefficient_tail = W * sum((F(comb(n, ell)) * eps_exact ** ell
                                for ell in range(1, n + 1)), F(0))
    analytic_tail = 2 * n * W * eps_exact
    actual_error = abs(R_exact - P)
    grid_error = F(1, 8 * grid)
    assert n * eps_exact <= F(1, 2)
    assert actual_error <= coefficient_tail <= analytic_tail <= grid_error
    assert nearest_integer(grid * R_exact) == int(grid * P)

    beta = F(1, 3)
    q_rel = n + h + 4 + ceil_log2_fraction(W / (beta * L))
    eps_rel = F(1, 1 << q_rel)
    R_rel = eval_poly(coeffs, eps_rel)
    rel_additive = abs(R_rel - P)
    assert rel_additive <= beta * L / 8
    assert rel_additive / P <= beta / 8

    # Check exact chart identity and rational input bit bounds.
    chart = []
    max_amp_num = max(abs(a.numerator).bit_length() for a in meta["amplitudes"])
    max_amp_den = max(a.denominator.bit_length() for a in meta["amplitudes"])
    for q, eps in ((q_exact, eps_exact), (q_rel, eps_rel)):
        M = [[b[i][j] + (eps if i == j else 0) for j in range(n)]
             for i in range(n)]
        dM = det(M)
        assert dM and abs(dM) >= eps ** n
        A_t = matmul(inverse(M), c)
        A = transpose(A_t)
        Z = target_z(A, k)
        R = sum(paired_weights(b, c, eps).values(), F(0))
        assert dM ** 2 * Z == R == eval_poly(coeffs, eps)
        Qeps = 1 << q
        T = [[Qeps * b[i][j] + F(i == j) for j in range(n)]
             for i in range(n)]
        dT = det(T)
        assert dT
        A_t_from_adj = matmul([[Qeps * x for x in row] for row in inverse(T)], c)
        assert A_t == A_t_from_adj
        hbits = ceil_log2_integer(n)
        det_bound = n * (q + 1 + hbits) + 2
        cof_bound = (n - 1) * (q + 1 + hbits) + 2
        num_bound = q + cof_bound + max_amp_num
        den_bound = det_bound + max_amp_den
        max_num = max(abs(x.numerator).bit_length() for row in A for x in row)
        max_den = max(x.denominator.bit_length() for row in A for x in row)
        assert max_num <= num_bound and max_den <= den_bound
        chart.append(dict(q=q, epsilon=fmt(eps), R=fmt(R), Z=fmt(Z),
                          det_M=fmt(dM), det_T=fmt(dT),
                          max_numerator_bits=max_num,
                          max_denominator_bits=max_den,
                          numerator_bound=num_bound,
                          denominator_bound=den_bound,
                          dense_entry_bits_bound=n * n * (num_bound + den_bound + 2)))

    # FPRAS composition as in the unweighted case.
    Mrel = [[b[i][j] + (eps_rel if i == j else 0) for j in range(n)]
            for i in range(n)]
    zrel = target_z(transpose(matmul(inverse(Mrel), c)), k)
    scale = det(Mrel) ** 2
    gamma = beta / 4
    worst = max(abs(scale * zrel * (1 + gamma) - P),
                abs(scale * zrel * (1 - gamma) - P)) / P
    assert worst <= F(13, 32) * beta < beta

    return dict(name=name, source_weighted_PM=fmt(P), found_matching_weight=fmt(L),
                vertices=m, padded_vertices=meta["padded_m"],
                variants=meta["variants"], dummies=meta["dummies"],
                N=n, target_k=k, source_r=meta["source_r"],
                delta_denominator_product=meta["Delta"],
                W=fmt(W), polynomial_coefficients=[fmt(x) for x in coeffs],
                coefficient_bounds=[fmt(x) for x in coeff_bounds],
                exact_q=q_exact, exact_epsilon=fmt(eps_exact),
                exact_scaled_error=fmt(grid * actual_error),
                exact_grid_tolerance=fmt(grid_error),
                relative_beta=fmt(beta), relative_q=q_rel,
                relative_epsilon=fmt(eps_rel),
                relative_additive_error=fmt(rel_additive),
                relative_error=fmt(rel_additive / P), chart_checks=chart)


def main():
    weighted_cases = [
        ("C4_one_half_weight", 4,
         [(0, 1, F(1, 2)), (1, 2, F(1)), (2, 3, F(1)), (3, 0, F(1))]),
        ("K2_half_weight_with_forced_padding", 2, [(0, 1, F(1, 2))]),
        ("zero_source", 4,
         [(0, 1, F(1)), (0, 2, F(1, 2)), (0, 3, F(1, 3))]),
    ]
    results = [check_weighted(*case) for case in weighted_cases]
    receipt = dict(status="PASS",
                   arithmetic="exact Python Fraction; no floating point or external packages",
                   assertions=[
                       "binary square atoms sum exactly to each rational edge weight",
                       "R(0) equals the rational weighted perfect-matching partition function",
                       "weighted coefficient bounds and exact denominator-grid extraction hold",
                       "relative dyadic perturbation plus one FPRAS call gives <=13 beta/32",
                       "determinant/target chart identity and rational bit bounds hold",
                       "zero and forced-padding branches are checked",
                   ],
                   cases=results,
                   scope="Finite diagnostics only; the general weighted extension is proved in RESULT.txt.")
    out = Path(__file__).with_name("check_weighted.json")
    out.write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
