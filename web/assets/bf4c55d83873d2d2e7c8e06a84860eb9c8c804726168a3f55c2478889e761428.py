#!/usr/bin/env python3
"""Exact finite checks for the dyadic regularization/AP reduction.

Uses only the Python standard library and Fraction arithmetic. These tests
check small instances and the stated identities/bounds; the proof is in
RESULT.txt and is not replaced by finite testing.
"""
from fractions import Fraction as F
from itertools import combinations, product
from math import comb
import json
from pathlib import Path


def eye(n):
    return [[F(i == j) for j in range(n)] for i in range(n)]


def det(a):
    a = [[F(x) for x in row] for row in a]
    n = len(a)
    if n == 0:
        return F(1)
    out = F(1)
    for j in range(n):
        pivot_row = next((i for i in range(j, n) if a[i][j]), None)
        if pivot_row is None:
            return F(0)
        if pivot_row != j:
            a[j], a[pivot_row] = a[pivot_row], a[j]
            out = -out
        pivot = a[j][j]
        out *= pivot
        for i in range(j + 1, n):
            if a[i][j]:
                ratio = a[i][j] / pivot
                for s in range(j + 1, n):
                    a[i][s] -= ratio * a[j][s]
                a[i][j] = F(0)
    return out


def inverse(a):
    n = len(a)
    aug = [[F(x) for x in row] + eye(n)[i] for i, row in enumerate(a)]
    for j in range(n):
        p = next((i for i in range(j, n) if aug[i][j]), None)
        if p is None:
            raise ValueError("singular matrix")
        aug[j], aug[p] = aug[p], aug[j]
        pivot = aug[j][j]
        aug[j] = [x / pivot for x in aug[j]]
        for i in range(n):
            if i != j and aug[i][j]:
                ratio = aug[i][j]
                aug[i] = [x - ratio * y for x, y in zip(aug[i], aug[j])]
    return [row[n:] for row in aug]


def matmul(a, b):
    return [[sum((a[i][s] * b[s][j] for s in range(len(b))), F(0))
             for j in range(len(b[0]))] for i in range(len(a))]


def transpose(a):
    return [list(row) for row in zip(*a)]


def pm_count(m, edges):
    adj = [set() for _ in range(m)]
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)

    def rec(vertices):
        if not vertices:
            return 1
        u = min(vertices)
        return sum(rec(vertices - {u, v}) for v in adj[u] & vertices)

    return rec(set(range(m)))


def ceil_log2_integer(x):
    assert x >= 1
    return (x - 1).bit_length()


def ceil_log2_fraction(x):
    x = F(x)
    assert x >= 1
    q = 0
    while (1 << q) < x:
        q += 1
    return q


def pad_graph(m, edges):
    """Return (m',edges'); handle no-edge source instances separately."""
    edges = list(edges)
    if m == 0:
        return 0, edges, "empty-source-instance"
    if not edges:
        return m, edges, "zero-count-no-edges"
    if len(edges) >= m:
        return m, edges, "unpad"
    u, v = m, m + 1
    return m + 2, edges + [(u, v)] + [(u, w) for w in range(m)], "forced-leaf-padding"


def gadget(m, edges):
    m2, edges2, padding = pad_graph(m, edges)
    if padding in ("empty-source-instance", "zero-count-no-edges"):
        return None, dict(padding=padding, source_vertices=m,
                          source_edges=len(edges), source_pm=pm_count(m, edges))
    e = len(edges2)
    d = e - m2
    assert d >= 0
    n = e + d
    assert n == m2 + 2 * d and n >= 2 and n % 2 == 0
    b = [[F(0) for _ in range(n)] for _ in range(n)]
    c = [[F(0) for _ in range(n)] for _ in range(n)]
    for j, (u, v) in enumerate(edges2):
        b[u][j] = 1
        c[v][j] = 1
    for j in range(d):
        b[m2 + 2 * j][e + j] = 1
        c[m2 + 2 * j + 1][e + j] = 1
    # Every column of B is exactly one coordinate vector.
    f = [next(i for i in range(n) if b[i][j]) for j in range(n)]
    assert all(sum(b[i][j] for i in range(n)) == 1 for j in range(n))
    return (b, c), dict(padding=padding, source_vertices=m,
                        source_edges=len(edges), vertices=m2, edges=e,
                        dummies=d, n=n, k=n // 2,
                        functional_map=f, source_pm=pm_count(m, edges))


def selected_matrix(b, c, sites, eps=F(0)):
    n = len(b)
    cols = []
    for j in sites:
        cols.append([b[i][j] + (eps if i == j else 0) for i in range(n)])
        cols.append([c[i][j] for i in range(n)])
    return transpose(cols)


def paired_weights(b, c, eps):
    n = len(b)
    k = n // 2
    weights = {}
    for sites in combinations(range(n), k):
        weights[sites] = det(selected_matrix(b, c, sites, eps)) ** 2
    return weights


def target_z(a, k):
    n = len(a)
    value = F(0)
    indices = range(n)
    for rows in combinations(indices, k):
        row_set = set(rows)
        for cols in combinations(indices, k):
            if row_set.isdisjoint(cols):
                minor = [[a[i][j] for j in cols] for i in rows]
                value += det(minor) ** 2
    return value


def determinant_polynomial(b, c, sites):
    """Coefficients of det([B+eps I,C]) selected at the given sites."""
    n = len(b)
    k = len(sites)
    coeffs = [0] * (k + 1)
    for mask in range(1 << k):
        cols = []
        for r, j in enumerate(sites):
            if (mask >> r) & 1:
                cols.append([F(i == j) for i in range(n)])
            else:
                cols.append([b[i][j] for i in range(n)])
            cols.append([c[i][j] for i in range(n)])
        coeffs[mask.bit_count()] += int(det(transpose(cols)))
    return coeffs


def poly_square_sum(b, c):
    n = len(b)
    k = n // 2
    total = [0] * (n + 1)
    for sites in combinations(range(n), k):
        p = determinant_polynomial(b, c, sites)
        for i, x in enumerate(p):
            for j, y in enumerate(p):
                total[i + j] += x * y
    return total


def eval_poly(p, x):
    return sum((F(a) * x ** j for j, a in enumerate(p)), F(0))


def fmt(x):
    x = F(x)
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def test_source_branch(m, edges):
    gadget_data, info = gadget(m, edges)
    if info["padding"] == "empty-source-instance":
        assert info["source_pm"] == 1
        return info
    if info["padding"] == "zero-count-no-edges":
        assert info["source_pm"] == 0
        return info

    b, c = gadget_data
    n, k, p = info["n"], info["k"], info["source_pm"]
    coeffs = poly_square_sum(b, c)
    assert coeffs[0] == p, (info, coeffs[0], p)
    coefficient_bounds = [comb(n, k) * comb(n, ell) for ell in range(n + 1)]
    assert all(abs(x) <= bound for x, bound in zip(coeffs, coefficient_bounds))

    # q= n+ceil(log2 n)+4 yields an absolute error < 1/8 for every instance.
    h = ceil_log2_integer(n)
    q_exact = n + h + 4
    eps_exact = F(1, 1 << q_exact)
    n_eps = n * eps_exact
    exact_R = eval_poly(coeffs, eps_exact)
    direct_R = sum(paired_weights(b, c, eps_exact).values(), F(0))
    assert exact_R == direct_R
    actual_error = abs(exact_R - p)
    coefficient_tail = comb(n, k) * sum(
        (F(comb(n, ell)) * eps_exact ** ell for ell in range(1, n + 1)), F(0))
    analytic_tail = F(2 ** (n + 1) * n) * eps_exact
    assert n_eps <= F(1, 2)
    assert actual_error <= coefficient_tail <= analytic_tail <= F(1, 8)
    rounded = (exact_R + F(1, 2)).numerator // (exact_R + F(1, 2)).denominator
    assert rounded == p

    # For a nonzero source count, instantiate the FPRAS-transfer precision.
    beta = F(1, 3)
    q_rel = n + h + ceil_log2_fraction(F(16, 1) / beta)
    eps_rel = F(1, 1 << q_rel)
    R_rel = eval_poly(coeffs, eps_rel)
    delta = abs(R_rel - p)
    assert delta <= beta / 8

    # Verify the matrix identity and exact chart bit bounds for both choices.
    chart_records = []
    for q, eps in ((q_exact, eps_exact), (q_rel, eps_rel)):
        M = [[b[i][j] + (eps if i == j else 0) for j in range(n)]
             for i in range(n)]
        det_M = det(M)
        assert det_M
        assert abs(det_M) >= eps ** n  # functional-map spectral-factor bound
        inv_M = inverse(M)
        A_t = matmul(inv_M, c)
        A = transpose(A_t)
        z = target_z(A, k)
        R = sum(paired_weights(b, c, eps).values(), F(0))
        assert det_M ** 2 * z == R
        assert R == eval_poly(coeffs, eps)

        # T=2^q B+I; A^T=2^q T^{-1}C.
        Q = 1 << q
        T = [[Q * b[i][j] + F(i == j) for j in range(n)] for i in range(n)]
        det_T = det(T)
        assert det_T
        assert A_t == matmul([[Q * x for x in row] for row in inverse(T)], c)
        hbits = ceil_log2_integer(n)
        det_bit_bound = n * (q + 1 + hbits) + 2
        cofactor_bit_bound = (n - 1) * (q + 1 + hbits) + 2
        num_bit_bound = q + cofactor_bit_bound
        max_num_bits = max(abs(x.numerator).bit_length() for row in A for x in row)
        max_den_bits = max(x.denominator.bit_length() for row in A for x in row)
        assert max_num_bits <= num_bit_bound
        assert max_den_bits <= det_bit_bound
        chart_records.append(dict(q=q, epsilon=fmt(eps), R=fmt(R), Z=fmt(z),
                                  det_M=fmt(det_M), det_T=fmt(det_T),
                                  max_numerator_bits=max_num_bits,
                                  max_denominator_bits=max_den_bits,
                                  numerator_bit_bound=num_bit_bound,
                                  denominator_bit_bound=det_bit_bound,
                                  full_matrix_entry_bit_bound=n * n *
                                      (num_bit_bound + det_bit_bound + 2)))

    # One-call relative-error composition: beta/4 oracle accuracy plus beta/8
    # perturbation produces at most 13 beta/32 relative error.
    if p > 0:
        eps = eps_rel
        M = [[b[i][j] + (eps if i == j else 0) for j in range(n)]
             for i in range(n)]
        inv_M = inverse(M)
        z = target_z(transpose(matmul(inv_M, c)), k)
        scale = det(M) ** 2
        R = scale * z
        gamma = beta / 4
        worst = max(abs(R * (1 + gamma) - p), abs(R * (1 - gamma) - p)) / p
        assert worst <= F(13, 32) * beta < beta

    return dict(name=info["padding"] + f"_m{m}_e{len(edges)}",
                source_vertices=m, source_edges=len(edges),
                padded_vertices=info.get("vertices"),
                padded_edges=info.get("edges"), dummies=info.get("dummies"),
                n=n, k=k, perfect_matchings=p,
                selected_subsets=comb(n, k),
                polynomial_coefficients=coeffs,
                coefficient_bounds=coefficient_bounds,
                exact_q=q_exact, exact_epsilon=fmt(eps_exact),
                exact_R=fmt(exact_R), exact_absolute_error=fmt(actual_error),
                coefficient_tail=fmt(coefficient_tail),
                analytic_tail=fmt(analytic_tail),
                relative_beta=fmt(beta), relative_q=q_rel,
                relative_epsilon=fmt(eps_rel),
                relative_perturbation_error=fmt(delta),
                chart_checks=chart_records)


def main():
    cases = [
        ("cycle4", 4, [(0, 1), (1, 2), (2, 3), (3, 0)]),
        ("K4", 4, list(combinations(range(4), 2))),
        ("P4-padding", 4, [(0, 1), (1, 2), (2, 3)]),
        ("two-triangles-zero", 6, [(0, 1), (1, 2), (2, 0),
                                  (3, 4), (4, 5), (5, 3)]),
        ("C6", 6, [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0)]),
        ("zero-edge-branch", 4, []),
        ("empty-graph-branch", 0, []),
    ]
    results = [dict(label=name, **test_source_branch(m, edges))
               for name, m, edges in cases]
    receipt = {
        "status": "PASS",
        "arithmetic": "exact Python fractions; no floating point or external packages",
        "assertions": [
            "R(0)=#PM on every constructed gadget",
            "all coefficients satisfy |c_l| <= binom(N,N/2) binom(N,l)",
            "dyadic exact and relative perturbation bounds hold exactly",
            "nearest-integer recovery holds including a zero-count constructed case",
            "det(B+epsilon I)^2 Z_(N/2)(A) = R(epsilon)",
            "adjugate-based rational chart agrees with exact inversion",
            "observed rational entries obey explicit Hadamard bit bounds",
            "one-call relative-error composition is at most 13 beta/32",
            "empty/no-edge source branches are handled without an oracle call",
        ],
        "cases": results,
        "scope": "Finite arithmetic checks only; the general claims are proved in RESULT.txt.",
    }
    out = Path(__file__).with_name("check_exact.json")
    out.write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
