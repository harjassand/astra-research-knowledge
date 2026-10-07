#!/usr/bin/env python3
"""Independent exact checks of the c03_l10 low-sector estimator identities.

Finite diagnostics only: these do not prove the all-n hypercontractive bound.
Uses SymPy exact Gaussian-rational arithmetic and exhausts every sign vector
for small matrices.
"""

from itertools import combinations, product
import json

import sympy as sp


def pfaffian(A):
    n = A.rows
    if n == 0:
        return sp.Integer(1)
    if n % 2:
        return sp.Integer(0)
    out = 0
    for j in range(1, n):
        keep = [a for a in range(n) if a not in (0, j)]
        out += (-1) ** (j + 1) * A[0, j] * pfaffian(A.extract(keep, keep))
    return sp.expand(out)


def c_direct(F, k):
    n = F.rows
    total = sp.Integer(0)
    for I in combinations(range(n), k):
        for J in combinations((j for j in range(n) if j not in I), k):
            d = F.extract(I, J).det()
            total += sp.expand_complex(d * sp.conjugate(d))
    return sp.simplify(total)


def make_A(F, signs):
    n = F.rows
    A = sp.zeros(n)
    for i, sign in enumerate(signs):
        u = sp.eye(n)[:, i]
        v = F[i, :].T
        A += sign * (u * v.T - v * u.T)
    return A


def principal_pf_sum(A, k):
    total = sp.Integer(0)
    for R in combinations(range(A.rows), 2 * k):
        p = pfaffian(A.extract(R, R))
        total += sp.expand_complex(p * sp.conjugate(p))
    return sp.simplify(total)


def formal_sqrt_coefficient(A, k, t):
    H = A.conjugate().T * A
    D = sp.Poly(sp.expand((sp.eye(A.rows) + t * H).det()), t)
    d = [D.nth(j) for j in range(k + 1)]
    q = [sp.Integer(1)]
    for m in range(1, k + 1):
        q.append(sp.simplify((d[m] - sum(q[j] * q[m - j]
                                          for j in range(1, m))) / 2))
    return sp.simplify(q[k])


def audit_matrix(F, label):
    n = F.rows
    rows = []
    for k in range(n // 2 + 1):
        target = c_direct(F, k)
        samples = []
        for signs in product((-1, 1), repeat=n):
            A = make_A(F, signs)
            x = principal_pf_sum(A, k)
            q = formal_sqrt_coefficient(A, k, sp.Symbol("t"))
            assert sp.simplify(x - q) == 0, (label, k, signs, x, q)
            assert sp.im(x) == 0 and sp.re(x) >= 0, (label, k, signs, x)
            samples.append(x)
        mean = sp.simplify(sum(samples) / len(samples))
        second = sp.simplify(sum(x * x for x in samples) / len(samples))
        assert sp.simplify(mean - target) == 0, (label, k, mean, target)
        if target:
            assert second <= 4 * 9**k * target**2, (label, k, second, target)
        else:
            assert all(x == 0 for x in samples), (label, k, samples)
        rows.append({
            "k": k,
            "c_k": str(target),
            "all_sign_mean": str(mean),
            "all_sign_second_moment": str(second),
            "zero_case_all_samples_zero": (target != 0 or all(x == 0 for x in samples)),
            "formal_sqrt_equals_principal_pf_sum": True,
            "second_moment_bound_checked": True,
        })
    return {"label": label, "n": n, "coefficients": rows}


def constrained_row_mass(F, k, forced, excluded):
    """Direct row-set mass and its forced-pair projection representation."""
    n = F.rows
    V = sp.Matrix.hstack(sp.eye(n), F.T)
    pair_cols = lambda S: [i for i in S] + [n + i for i in S]
    C = V[:, pair_cols(forced)]
    gram = C.conjugate().T * C
    det_gram = sp.simplify(gram.det())
    direct = sp.Integer(0)
    for S in combinations(range(n), k):
        if set(forced).issubset(S) and set(excluded).isdisjoint(S):
            CS = V[:, pair_cols(S)]
            direct += (CS.conjugate().T * CS).det()
    direct = sp.simplify(direct)
    if det_gram == 0:
        assert direct == 0
        return {"forced": list(forced), "excluded": list(excluded),
                "direct_mass": str(direct), "projected_mass": "0",
                "projected_sign_mean": "0", "identity_checked": True}
    remainder = [i for i in range(n) if i not in set(forced) | set(excluded)]
    r = k - len(forced)
    P = sp.eye(n) - C * gram.inv() * C.conjugate().T
    # Store each projected pair in the same site order for the skew lift.
    pair = {i: (P * V[:, i], P * V[:, n + i]) for i in remainder}
    residual_sum = sp.Integer(0)
    for T in combinations(remainder, r):
        cols = []
        for i in T:
            cols.extend([pair[i][0], pair[i][1]])
        W = sp.Matrix.hstack(*cols) if cols else sp.zeros(n, 0)
        residual_sum += sp.simplify((W.conjugate().T * W).det())
    projected_mass = sp.simplify(det_gram * residual_sum)
    assert sp.simplify(projected_mass - direct) == 0
    sample_vals = []
    for signs in product((-1, 1), repeat=len(remainder)):
        A = sp.zeros(n)
        for i, sign in zip(remainder, signs):
            u, v = pair[i]
            A += sign * (u * v.T - v * u.T)
        sample_vals.append(sp.simplify(det_gram * principal_pf_sum(A, r)))
    sign_mean = sp.simplify(sum(sample_vals) / len(sample_vals))
    second = sp.simplify(sum(x * x for x in sample_vals) / len(sample_vals))
    assert sp.simplify(sign_mean - direct) == 0
    assert second <= 4 * 9**r * direct**2
    assert all(sp.im(x) == 0 and sp.re(x) >= 0 for x in sample_vals)
    return {"forced": list(forced), "excluded": list(excluded),
            "direct_mass": str(direct), "projected_mass": str(projected_mass),
            "projected_sign_mean": str(sign_mean),
            "projected_sign_second_moment": str(second),
            "second_moment_bound_checked": True,
            "identity_checked": True}


def volume_completion_mass(M, selected, excluded):
    """Exact volume-sampling completion mass from a partial column set."""
    k, ncol = M.shape
    if len(selected) > k:
        return sp.Integer(0)
    C = M[:, selected] if selected else sp.zeros(k, 0)
    if C.rank() != len(selected):
        return sp.Integer(0)
    r = k - len(selected)
    remaining = [j for j in range(ncol)
                 if j not in set(selected) | set(excluded)]
    if len(remaining) < r:
        return sp.Integer(0)
    direct = sp.Integer(0)
    for B in combinations(remaining, r):
        cols = list(selected) + list(B)
        D = M[:, cols]
        direct += sp.simplify((D.conjugate().T * D).det())
    if selected:
        G = C.conjugate().T * C
        d = sp.simplify(G.det())
        P = sp.eye(k) - C * G.inv() * C.conjugate().T
    else:
        d = sp.Integer(1)
        P = sp.eye(k)
    Y = P * M[:, remaining]
    H = Y * Y.conjugate().T
    t = sp.Symbol("t")
    poly = sp.Poly(sp.expand((sp.eye(k) + t * H).det()), t)
    formula = sp.simplify(d * poly.nth(r))
    assert sp.simplify(formula - direct) == 0
    return formula


def audit_volume_sampling_prefixes(F, row_set):
    n = F.rows
    cols = [j for j in range(n) if j not in set(row_set)]
    M = F.extract(row_set, cols)
    k, ncol = M.shape
    checked = 0
    for state in product((0, 1, 2), repeat=ncol):
        selected = [j for j, bit in enumerate(state) if bit == 1]
        excluded = [j for j, bit in enumerate(state) if bit == 2]
        if len(selected) > k:
            continue
        volume_completion_mass(M, selected, excluded)
        checked += 1
    return {"row_set": list(row_set), "matrix_shape": list(M.shape),
            "prefix_states_checked": checked,
            "all_exact_completion_masses_match_direct_enumeration": True}


if __name__ == "__main__":
    F1 = sp.Matrix([
        [0, 1 + sp.I, 2, -1],
        [2 - sp.I, 0, 1, 3 + sp.I],
        [1, -2 + sp.I, 0, 2],
        [3, 1, -1 + 2 * sp.I, 0],
    ])
    Fzero = sp.ones(4) - sp.eye(4)
    Frational = F1.applyfunc(lambda x: sp.Rational(1, 2) * x)
    result = {
        "status": "exact finite checks only; no universal proof or external validation",
        "peer_origin": "c03_l10/low_sector_pfaffian_fpras.txt",
        "cases": [audit_matrix(F1, "dense-complex-n4"),
                  audit_matrix(Frational, "dense-complex-rational-n4-scaled-by-half"),
                  audit_matrix(Fzero, "K4-all-ones-off-diagonal-zero-c2")],
        "forced_row_prefix_checks": [
            constrained_row_mass(F1, 2, [0], []),
            constrained_row_mass(F1, 2, [0], [3]),
            constrained_row_mass(F1, 2, [], [1, 3]),
        ],
        "conditional_column_volume_prefix_check":
            audit_volume_sampling_prefixes(F1, [0, 1]),
    }
    print(json.dumps(result, indent=2, sort_keys=True))
