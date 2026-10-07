"""Exact checks of all-spin bipartite PH transfer and hard parity barriers.

No FPRAS or quantum circuit execution is implemented here.
"""
from itertools import combinations, product
from math import factorial
from pathlib import Path
import json
import random
import sympy as sp


def create(state, mode):
    out = {}
    for mask, a in state.items():
        if mask & (1 << mode):
            continue
        sign = (-1)**(mask & ((1 << mode)-1)).bit_count()
        new = mask | (1 << mode)
        out[new] = out.get(new, 0) + sign*a
    return out


def pair(state, F):
    n = F.rows
    out = {}
    for i in range(n):
        for j in range(n):
            if F[i, j] == 0:
                continue
            for mask, a in create(create(state, n+j), i).items():
                out[mask] = out.get(mask, 0) + F[i, j]*a
    return {mask: sp.simplify(a) for mask, a in out.items() if a != 0}


def bcs(F):
    term = {0: sp.S.One}
    out = dict(term)
    for k in range(1, F.rows+1):
        term = pair(term, F)
        for mask, a in term.items():
            out[mask] = out.get(mask, 0) + a/factorial(k)
    return {mask: sp.simplify(a) for mask, a in out.items() if a != 0}


def majorana_y(state, mode):
    # i(c^dagger-c) = Z_<mode Y_mode in Jordan-Wigner coordinates.
    out = {}
    for mask, a in state.items():
        sign = (-1)**(mask & ((1 << mode)-1)).bit_count()
        occupied = bool(mask & (1 << mode))
        out[mask ^ (1 << mode)] = sp.I * (-1 if occupied else 1) * sign * a
    return out


def fermionic_permute(state, order):
    out = {}
    dest = {old: new for new, old in enumerate(order)}
    for mask, a in state.items():
        old_occ = [i for i in range(len(order)) if mask & (1 << i)]
        new_occ = [dest[i] for i in old_occ]
        inv = sum(new_occ[i] > new_occ[j] for i in range(len(new_occ)) for j in range(i+1, len(new_occ)))
        new = sum(1 << j for j in new_occ)
        out[new] = (-1)**inv*a
    return out


def coeff(F, t, k):
    total = sp.S.Zero
    for I in combinations(range(F.rows), k):
        for J in combinations(range(F.rows), k):
            d = F.extract(I, J).det() if k else sp.S.One
            total += d*sp.conjugate(d)*sp.prod(t[i] for i in set(I)&set(J))
    return sp.simplify(total)


def check_case(F, A, B, t):
    n, a, b = F.rows, len(A), len(B)
    assert sorted(A+B) == list(range(n))
    assert F.extract(A, A).is_zero_matrix and F.extract(B, B).is_zero_matrix
    M = sp.zeros(2*a, 2*b)
    M[:a, b:] = F.extract(A, B)
    M[a:, :b] = -F.extract(B, A).T
    G = M.col_join(sp.eye(2*b))
    order = A+[n+i for i in A]+B+[n+i for i in B]
    C = B+[n+i for i in B]
    original = bcs(F)
    transformed = original
    for mode in reversed(C):
        transformed = majorana_y(transformed, mode)
    transformed = fermionic_permute(transformed, order)
    norm_by_sector = [sp.S.Zero]*(n+1)
    checked = 0
    for S in combinations(range(2*n), 2*b):
        d = G.extract(S, range(2*b)).det() if b else sp.S.One
        mask = sum(1 << j for j in S)
        assert sp.simplify(transformed.get(mask, 0)-(-1)**b*d) == 0
        weight = d*sp.conjugate(d)
        for i, site in enumerate(A):
            load = int(i in S)+int(a+i in S)
            if load == 2:
                weight *= t[site]
        for i, site in enumerate(B):
            load = int(2*a+i in S)+int(2*a+b+i in S)
            if load == 0:
                weight *= t[site]
        k = sum(j < 2*a for j in S)
        if k <= n:
            norm_by_sector[k] += weight
        else:
            assert weight == 0
        checked += 1
    for k in range(n+1):
        assert sp.simplify(norm_by_sector[k]-coeff(F, t, k)) == 0
    return {"n": n, "A": A, "B": B, "t": list(map(str, t)),
            "Slater_basis_checks": checked, "norm_coefficients": list(map(str, norm_by_sector))}


def cycle_barrier(q):
    n = 2*q
    F = sp.zeros(n)
    for i in range(n):
        F[i, (i+1) % n] = 1
    V = sp.eye(n).row_join(F.T)
    L = V.T*V
    supports = []
    for I in combinations(range(n), q):
        selected = list(I)+[n+i for i in I]
        w = L.extract(selected, selected).det()
        direct = sum((F.extract(I, J).det())**2
                     for J in combinations([j for j in range(n) if j not in I], q))
        assert w == direct
        if w:
            supports.append(list(I))
            assert w == 1
    assert supports == [list(range(0, n, 2)), list(range(1, n, 2))]
    alpha = sp.Symbol("alpha", positive=True)
    sign = sp.Matrix([1 if i % 2 == 0 else -1 for i in range(n)])
    H = alpha**2*sign*sign.T/4-alpha*sp.eye(n)/2
    assert H*sign == (alpha**2*q-alpha)/2*sign
    return {"q": q, "n": n, "supports": supports,
            "positive_hessian_eigenvalue_if_alpha_gt_1_over_q": "(alpha^2*q-alpha)/2",
            "maximum_sector_aperture": "pi/q", "minimum_down_up_removal_to_connect": q}


def main():
    rng = random.Random(104071)
    records = []
    specs = [(2, [0], [1]), (3, [0, 2], [1]),
             (4, [0, 1], [2, 3]), (4, [0, 2], [1, 3])]
    choices = [sp.S.Zero, sp.S.One, sp.Rational(1,16), sp.Rational(9,25),
               sp.Rational(3,2), sp.Integer(2)]
    for n, A, B in specs:
        for trial in range(6):
            F = sp.zeros(n)
            for i, j in product(A, B):
                F[i, j] = sp.Rational(rng.randint(-3, 3), rng.randint(1, 3)) + sp.I*sp.Rational(rng.randint(-2, 2), 3)
                F[j, i] = sp.Rational(rng.randint(-3, 3), rng.randint(1, 3)) + sp.I*sp.Rational(rng.randint(-2, 2), 3)
            t = [choices[(i+trial) % len(choices)] for i in range(n)]
            records.append(check_case(F, A, B, t))
            # Hard filters permit arbitrary diagonal deletion.
            t0 = [sp.S.Zero]*n
            hard = [coeff(F, t0, k) for k in range(n+1)]
            Fdiag = F+sp.diag(*[sp.Rational(i+trial+1, 2) for i in range(n)])
            assert hard == [coeff(Fdiag, t0, k) for k in range(n+1)]
    barriers = [cycle_barrier(q) for q in range(2, 7)]
    T = sp.Symbol("T", positive=True)
    source_H = sp.Matrix([[0,T,1,1], [T,0,1,1], [1,1,0,T], [1,1,T,0]])
    source_v = sp.Matrix([1,1,-1,-1])
    assert source_H*sp.ones(4,1) == (T+2)*sp.ones(4,1)
    assert source_H*source_v == (T-2)*source_v
    assert source_H*sp.Matrix([1,-1,0,0]) == -T*sp.Matrix([1,-1,0,0])
    assert source_H*sp.Matrix([0,0,1,-1]) == -T*sp.Matrix([0,0,1,-1])
    out = {"status": "exact finite checks passed", "PH_cases": len(records),
           "Slater_basis_checks": sum(r["Slater_basis_checks"] for r in records),
           "PH_records": records, "directed_cycle_parity_barriers": barriers,
           "factorial_source_range": {"two_site_Hessian_eigenvalues": ["T+2", "T-2", "-T", "-T"],
                                      "universal_admitted_range": "0<=T<=2"},
           "scope": "exact identities and structural barriers; no FPRAS/compiler run"}
    Path(__file__).with_name("hard_bcs_bipartite_check.json").write_text(json.dumps(out, indent=2)+"\n")
    print(json.dumps({k: out[k] for k in ("status", "PH_cases", "Slater_basis_checks")}))


if __name__ == "__main__":
    main()
