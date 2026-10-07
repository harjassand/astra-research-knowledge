"""Exact finite algebra checks of the cloned chiral representation.

This is not an implementation of the imported FPRAS or quantum compiler.
"""
from itertools import combinations, product
from pathlib import Path
import json
import random
import sympy as sp


def subsets(n, k):
    return list(combinations(range(n), k))


def coeffs(F, t):
    n = F.rows
    out = []
    for k in range(n + 1):
        value = sp.S.Zero
        for I in subsets(n, k):
            for J in subsets(n, k):
                d = F.extract(I, J).det() if k else sp.S.One
                value += d * sp.conjugate(d) * sp.prod(t[i] for i in set(I) & set(J))
        out.append(sp.simplify(value))
    return out


def check(F, alpha, beta):
    # alpha=sqrt(t), beta=sqrt(1-t), chosen rational for exact fixtures.
    n = F.rows
    assert all(a*a+b*b == 1 for a, b in zip(alpha, beta))
    t = [a*a for a in alpha]
    B = (2 * F * sp.diag(*beta)).row_join(sp.sqrt(2) * F * sp.diag(*alpha))
    H = sp.zeros(3*n)
    H[:n, n:] = B
    H[n:, :n] = B.conjugate().T
    x = sp.Symbol("x", real=True)
    mean_chi = sp.S.Zero
    for bits in product((0, 1), repeat=n):
        S = [i if bits[i] else n+i for i in range(n)] + list(range(2*n, 3*n))
        chi = H.extract(S, S).charpoly()
        mean_chi += chi.as_expr().subs(chi.gen, x)
    mean_chi = sp.expand(mean_chi / 2**n)
    Z = coeffs(F, t)
    expected = sum((-1)**k * z * x**(2*n-2*k) for k, z in enumerate(Z))
    assert sp.simplify(mean_chi-expected) == 0, (F, t, mean_chi, expected)
    return {"n": n, "rank": F.rank(), "t": list(map(str, t)),
            "Z": list(map(str, Z)), "chiral_identity": True}


def main():
    rng = random.Random(910073)
    pairs = [(sp.S.Zero, sp.S.One), (sp.S.One, sp.S.Zero),
             (sp.Rational(3, 5), sp.Rational(4, 5)),
             (sp.Rational(4, 5), sp.Rational(3, 5))]
    records = []
    # Every filter endpoint and both interior Pythagorean values for n=1,2.
    for n in (1, 2):
        F = sp.Matrix(n, n, lambda i, j: sp.Rational(2*i-j+1, i+j+1)
                      + sp.I * sp.Rational(i+j-1, 2))
        for ab in product(pairs, repeat=n):
            records.append(check(F, [a for a, _ in ab], [b for _, b in ab]))
    # Complex, singular, diagonal, off-diagonal, and zero n=3 fixtures.
    matrices = [sp.Matrix(3, 3, lambda i, j: sp.Rational(rng.randint(-3, 3), rng.randint(1, 4))
                          + sp.I * sp.Rational(rng.randint(-2, 2), rng.randint(1, 3))),
                sp.Matrix([[1, 2, 3], [2, 4, 6], [1, 0, 1]]),
                sp.diag(1, sp.I, 2),
                sp.Matrix([[0, 1, 0], [0, 0, 2], [3, 0, 0]]),
                sp.zeros(3)]
    for q, F in enumerate(matrices):
        ab = [pairs[(q+i) % len(pairs)] for i in range(3)]
        records.append(check(F, [a for a, _ in ab], [b for _, b in ab]))
    # Sharp repulsive boundary: swap pairing with t1=t2=2 gives nonreal zeros.
    swap = sp.Matrix([[0, 1], [1, 0]])
    attractive = coeffs(swap, [sp.Rational(2), sp.Rational(2)])
    assert attractive == [1, 2, 4]
    discriminant = attractive[1]**2 - 4*attractive[0]*attractive[2]
    assert discriminant == -12
    output = {"status": "exact algebra checks passed", "exact_chiral_cases": len(records),
              "principal_submatrix_characteristic_polynomials": sum(2**r["n"] for r in records),
              "records": records, "t_gt_1_counterexample": {"F": "swap", "t": [2, 2],
              "Z": list(map(str, attractive)), "discriminant": str(discriminant)},
              "scope": "finite algebra diagnostics; general theorem separately proved; FPRAS/compiler unimplemented"}
    Path(__file__).with_name("canonical_bcs_check.json").write_text(json.dumps(output, indent=2)+"\n")
    print(json.dumps({k: output[k] for k in ("status", "exact_chiral_cases", "principal_submatrix_characteristic_polynomials")}))


if __name__ == "__main__":
    main()
