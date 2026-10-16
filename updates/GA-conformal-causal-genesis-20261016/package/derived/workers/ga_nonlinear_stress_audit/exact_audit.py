#!/usr/bin/env python3
"""Independent exact audit of the separated-potential stress certificate.

The polynomial and matrix checks use only Python's Fraction arithmetic, not
the constructor's verification code, optimizer files, or SymPy.  The input
Gram is untrusted certificate data. Analytic integration and Sobolev density
are justified separately in AUDIT.md; they are not machine-verified here.
"""
from __future__ import annotations

from fractions import Fraction as F
from pathlib import Path
from math import factorial
from itertools import product
import hashlib
import json
import platform

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
INPUT = ROOT / "workers/ga_sharp_invention/SEPARATED_STRESS_EXACT_CERTIFICATE.json"
SOURCE = ROOT / "originals/conformal_packet/RESEARCH_REPORT.md"
CONSTRUCTOR_REPORT = ROOT / "workers/ga_sharp_invention/REPORT.md"
ZERO = (0, 0, 0, 0, 0)
checks = []


def check(name, condition, detail=None):
    if not condition:
        raise RuntimeError("FAILED: " + name)
    checks.append({"name": name, "status": "PASS", "detail": detail})


def add(*args):
    out = {}
    for p in args:
        for k, v in p.items():
            out[k] = out.get(k, F(0)) + v
    return {k: v for k, v in out.items() if v}


def scale(p, q):
    return {k: v * F(q) for k, v in p.items() if v * F(q)}


def mul(p, q):
    out = {}
    for k, v in p.items():
        for ell, w in q.items():
            m = tuple(x + y for x, y in zip(k, ell))
            out[m] = out.get(m, F(0)) + v * w
    return {k: v for k, v in out.items() if v}


def powp(p, n):
    out = {ZERO: F(1)}
    for _ in range(n):
        out = mul(out, p)
    return out


def deriv(p, coordinate):
    out = {}
    for k, v in p.items():
        if k[coordinate]:
            ell = list(k)
            ell[coordinate] -= 1
            out[tuple(ell)] = v * k[coordinate]
    return out


def variable(i):
    k = [0] * 5
    k[i] = 1
    return {tuple(k): F(1)}


def coeff_s(p, n):
    return {k[:4] + (0,): v for k, v in p.items() if k[4] == n}


def j1(a0, b0, c0, d0):
    # Reconstruct from the original Jr formula at r=1: alpha=1/8,
    # beta=0, and r=1. No residual formula is imported.
    u = add(powp(a0, 2), powp(c0, 2))
    v = add(powp(b0, 2), powp(d0, 2))
    j = add(mul(a0, d0), scale(mul(b0, c0), -1))
    h = powp(add(u, v, scale(j, -2)), 2)
    return add(scale(h, F(1, 8)), powp(j, 2), mul(u, j))


def matmul(a0, b0):
    return [[sum((x * y for x, y in zip(row, col)), F(0))
             for col in zip(*b0)] for row in a0]


def transpose(a0):
    return [list(row) for row in zip(*a0)]


def ldl(a0):
    n = len(a0)
    low = [[F(int(i == j)) for j in range(n)] for i in range(n)]
    diag = []
    for j in range(n):
        pivot = a0[j][j] - sum((low[j][k] ** 2 * diag[k] for k in range(j)), F(0))
        if pivot <= 0:
            raise RuntimeError("Nonpositive exact LDL pivot: " + str(pivot))
        diag.append(pivot)
        for i in range(j + 1, n):
            low[i][j] = (a0[i][j] - sum((low[i][k] * low[j][k] * diag[k]
                                       for k in range(j)), F(0))) / pivot
    diagonal = [[diag[i] if i == j else F(0) for j in range(n)] for i in range(n)]
    if matmul(matmul(low, diagonal), transpose(low)) != a0:
        raise RuntimeError("LDL reconstruction failed")
    return low, diag


def det(a0):
    b0 = [row[:] for row in a0]
    answer = F(1)
    for j in range(len(b0)):
        if not b0[j][j]:
            candidates = [i for i in range(j + 1, len(b0)) if b0[i][j]]
            if not candidates:
                return F(0)
            i = candidates[0]
            b0[i], b0[j] = b0[j], b0[i]
            answer = -answer
        pivot = b0[j][j]
        answer *= pivot
        for i in range(j + 1, len(b0)):
            q = b0[i][j] / pivot
            for k in range(j + 1, len(b0)):
                b0[i][k] -= q * b0[j][k]
            b0[i][j] = F(0)
    return answer


def moment(cos_degree, sin_degree):
    # Normalized integral of cos(x)^m sin(x)^n over a circle.
    if cos_degree % 2 or sin_degree % 2:
        return F(0)
    p, q = cos_degree // 2, sin_degree // 2
    return F(factorial(2 * p) * factorial(2 * q),
             4 ** (p + q) * factorial(p) * factorial(q) * factorial(p + q))


def mixed_average(p):
    # f=sin x sin y, g=lambda cos x cos y. Then
    # a=cos x sin y, b=sin x cos y, c=-lambda b, d=-lambda a.
    # Return polynomial in (lambda, s), integrated exactly.
    out = {}
    for (ka, kb, kc, kd, ks), val in p.items():
        v = val * (-1) ** (kc + kd) * moment(ka + kd, kb + kc) ** 2
        k = (kc + kd, ks)
        out[k] = out.get(k, F(0)) + v
    return {k: v for k, v in out.items() if v}


def at_lambda_one(p):
    out = {}
    for (_, ks), val in p.items():
        out[ks] = out.get(ks, F(0)) + val
    return {k: v for k, v in out.items() if v}


def serial_poly(p):
    return [{"exponent": list(k) if isinstance(k, tuple) else k,
             "coefficient": str(v)} for k, v in sorted(p.items())]


def serial_matrix(a0):
    return [[str(t) for t in row] for row in a0]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    input_hash = sha(INPUT)
    data = json.loads(INPUT.read_text())
    a, b, c, d, s = [variable(i) for i in range(5)]
    j = add(mul(a, d), scale(mul(b, c), -1))
    jzero = j1(a, b, c, d)
    shifted = j1(add(a, s), b, c, add(d, s))
    constant = scale(powp(s, 4), 2)
    gap = add(shifted, scale(constant, -1))
    cubic = add(powp(a, 3), scale(mul(powp(a, 2), d), 5),
                scale(mul(mul(a, b), c), -4), mul(a, powp(c, 2)),
                scale(mul(a, powp(d, 2)), 2), scale(mul(mul(b, c), d), -2),
                mul(powp(c, 2), d))
    rawquadratic = add(powp(add(scale(a, 2), d), 2), powp(c, 2), scale(j, 3))
    linear = add(scale(a, 5), scale(d, 3))
    expected = add(constant, mul(powp(s, 3), linear),
                   mul(powp(s, 2), rawquadratic), mul(s, cubic), jzero)
    check("full Taylor reconstruction from original J1", shifted == expected)
    check("zero-background quartic retained", coeff_s(shifted, 0) == jzero)
    check("J1(sI)=2s^4", coeff_s(shifted, 4) == {ZERO: F(2)})
    sigma1 = add(scale(mul(powp(s, 2), b), -3), scale(powp(b, 3), F(1, 2)))
    sigma2 = add(scale(powp(s, 3), 3), scale(mul(powp(s, 2), a), 7),
                 scale(mul(s, powp(a, 2)), 5), scale(powp(a, 3), F(1, 2)))
    pairing = add(mul(sigma1, c), mul(sigma2, d))
    residual = add(gap, scale(mul(powp(s, 3), a), -5), scale(pairing, -1))
    check("residual is homogeneous quartic", all(sum(k) == 4 for k in residual))
    check("stress removes s^3 and s^4 residual terms", not coeff_s(residual, 3)
          and not coeff_s(residual, 4))
    check("residual s^2 coefficient", coeff_s(residual, 2) ==
          add(scale(powp(a, 2), 4), powp(c, 2), powp(d, 2)))

    exps = [tuple(k) for k in data["mons"]]
    gradient_exps = {k for k in product(range(3), repeat=5)
                     if sum(k) == 2 and k[4] == 0}
    sa_sc_sd = {(1, 0, 0, 0, 1), (0, 0, 1, 0, 1), (0, 0, 0, 1, 1)}
    check("basis exactly ten gradient quadratics plus sa sc sd",
          len(exps) == 13 and len(set(exps)) == 13
          and set(exps) == gradient_exps | sa_sc_sd,
          {"gradient_quadratics": len(gradient_exps), "total": len(exps)})
    Q = [[F(t) for t in row] for row in data["gram"]]
    check("Gram dimension", len(Q) == 13 and all(len(row) == 13 for row in Q))
    check("Gram exact symmetry", Q == transpose(Q))
    gram_poly = {}
    for i in range(13):
        for j0 in range(13):
            k = tuple(x + y for x, y in zip(exps[i], exps[j0]))
            gram_poly[k] = gram_poly.get(k, F(0)) + Q[i][j0]
    gram_poly = {k: v for k, v in gram_poly.items() if v}
    check("independent exact zTQz residual identity", gram_poly == residual,
          {"residual_nonzero_coefficients": len(residual)})
    decomposition = {}
    for name, epsilon in (("Q", F(0)), ("Q_minus_I_over_128", F(1, 128))):
        matrix = [[Q[i][j0] - (epsilon if i == j0 else F(0))
                   for j0 in range(13)] for i in range(13)]
        L, D = ldl(matrix)
        check(name + " full independent exact LDL has positive pivots", all(t > 0 for t in D))
        check(name + " exact LDL reconstructs matrix", matmul(matmul(L,
              [[D[i] if i == j0 else F(0) for j0 in range(13)] for i in range(13)]),
              transpose(L)) == matrix)
        decomposition[name] = {"lower_triangular": serial_matrix(L), "pivots": [str(t) for t in D]}
    blocks = data["blocks"]
    check("declared blocks partition basis", sorted(sum(blocks, [])) == list(range(13))
          and len(sum(blocks, [])) == 13)
    check("declared block separation", all(Q[i][j0] == 0
          for i in blocks[0] for j0 in blocks[1]))
    for name, epsilon in (("Q", F(0)), ("Q_minus_I_over_128", F(1, 128))):
        minor_record = []
        for block in blocks:
            B = [[Q[i][j0] - (epsilon if i == j0 else F(0)) for j0 in block] for i in block]
            minors = [det([row[:k] for row in B[:k]]) for k in range(1, len(block) + 1)]
            check(name + " block Sylvester minors positive " + str(block), all(t > 0 for t in minors))
            pivots = [minors[0]] + [minors[k] / minors[k - 1] for k in range(1, len(minors))]
            minor_record.append({"basis_indices": block, "leading_minors": [str(t) for t in minors],
                                 "pivots": [str(t) for t in pivots]})
        decomposition[name]["blocks"] = minor_record

    z_squared = {tuple(2 * t for t in k): F(1) for k in exps}
    all_gradient_quadratics = {tuple(2 * t for t in k): F(1) for k in gradient_exps}
    V2 = add(powp(a, 2), powp(b, 2), powp(c, 2), powp(d, 2))
    pure_fourth = add(powp(a, 4), powp(b, 4), powp(c, 4), powp(d, 4))
    check("ten monomial squares control half Frobenius fourth power exactly",
          all_gradient_quadratics == add(scale(powp(V2, 2), F(1, 2)), scale(pure_fourth, F(1, 2))))
    check("complete basis quantitative decomposition", z_squared ==
          add(all_gradient_quadratics, mul(powp(s, 2), add(powp(a, 2), powp(c, 2), powp(d, 2)))))
    divergence = add(deriv(sigma1, 1), deriv(sigma2, 0))
    expected_div = add(scale(powp(s, 2), 4), scale(mul(s, a), 10),
                       scale(add(powp(a, 2), powp(b, 2)), F(3, 2)))
    check("general-f divergence coefficient", divergence == expected_div)
    check("no other chain-rule terms in div stress", not deriv(sigma1, 0) and not deriv(sigma2, 1))
    # A conventional pointwise affine-minor support at I would have its
    # determinant slope forced to 3 by the b-c quadratic cross term.
    ordinary_support_residual = add(gap, scale(mul(powp(s, 3), linear), -1),
                                    scale(mul(powp(s, 2), j), -3))
    diagonal_curve = {}
    for (ka, kb, kc, kd, ks), val in ordinary_support_residual.items():
        if not kb and not kc:
            degree = ka + kd  # substitute a=t,d=-2t,s=1
            diagonal_curve[degree] = diagonal_curve.get(degree, F(0)) + val * (-2) ** kd
    diagonal_curve = {k: v for k, v in diagonal_curve.items() if v}
    check("forced conventional support has exact negative cubic",
          diagonal_curve == {3: F(-1), 4: F(97, 8)})
    support_value = sum((val * F(1, 100) ** k for k, val in diagonal_curve.items()), F(0))
    check("explicit conventional-support violation at t=1/100", support_value < 0,
          {"residual": str(support_value), "scope": "pointwise affine-minor support only"})
    # An entirely rational square identity suffices for the report's
    # deliberately nonsharp discriminant margin; no floating eigenvalue.
    u = add(powp(a, 2), powp(c, 2))
    v = add(powp(b, 2), powp(d, 2))
    X = add(u, scale(v, -1))
    Y = scale(j, 2)
    Z = scale(add(mul(a, b), mul(c, d)), 2)
    upper_left = add(scale(powp(V2, 2), 9), scale(jzero, -16))
    upper_right = add(powp(add(Y, scale(X, -2)), 2), scale(powp(X, 2), 3), scale(powp(Z, 2), 7))
    check("pointwise rational J1 upper bound square identity", upper_left == upper_right)
    check("optional discriminant margin arithmetic",
          F(143, 144) * F(511, 512) == F(73073, 73728))
    # An exact mixed-derivative obstruction field; a cancellation failure only.
    average_stress = mixed_average(pairing)
    average_gap = mixed_average(gap)
    check("mixed field stress pairing at lambda=1 is -s^2-9/64",
          at_lambda_one(average_stress) == {2: F(-1), 0: F(-9, 64)})
    check("mixed field Jensen gap at lambda=1 is s^2/2+17/32",
          at_lambda_one(average_gap) == {2: F(1, 2), 0: F(17, 32)})
    check("certificate input unchanged", input_hash == sha(INPUT))
    result = {
        "schema": "independent-separated-nonlinear-stress-audit/1",
        "status": "PASS",
        "scope": "Exact polynomial, rational Gram, floor, basis, and explicit mixed-field moments. Analytic proof in AUDIT.md.",
        "analytic_claim": "For periodic W1,4 phi=(F(x)+H(y),g), every real s: avg[J1(sI+Dphi)-J1(sI)] >= avg|Dphi|^4/256 + s^2 avg(a^2+c^2+d^2)/128.",
        "excluded_claims": ["universal conformal quasiconvexity", "all r", "general matrix backgrounds", "historical novelty", "external certification"],
        "checks": checks,
        "floor": "1/128",
        "basis_exponents_a_b_c_d_s": [list(k) for k in exps],
        "residual_polynomial": serial_poly(residual),
        "raw_Taylor_s2": serial_poly(rawquadratic),
        "Taylor_s1": serial_poly(cubic),
        "divergence_coefficient": serial_poly(divergence),
        "mixed_field_Jensen_gap_lambda_s": serial_poly(average_gap),
        "mixed_field_stress_pairing_lambda_s": serial_poly(average_stress),
        "conventional_support_diagonal_curve": serial_poly(diagonal_curve),
        "conventional_support_violation_at_t_1_over_100": str(support_value),
        "certificate_sha256": input_hash,
        "original_report_sha256": sha(SOURCE),
        "constructor_report_sha256": sha(CONSTRUCTOR_REPORT),
        "self_sha256": sha(Path(__file__)),
        "python": platform.python_version(),
    }
    (HERE / "INDEPENDENT_LDL_CERTIFICATE.json").write_text(json.dumps(decomposition, indent=2) + "\n")
    (HERE / "AUDIT_RECEIPT.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"status": result["status"], "checks": len(checks), "floor": result["floor"],
                      "input_sha256": input_hash,
                      "mixed_field_Jensen_gap_lambda_s": result["mixed_field_Jensen_gap_lambda_s"]}, indent=2))


if __name__ == "__main__":
    main()
