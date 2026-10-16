#!/usr/bin/env python3
"""Exact finite checks and a constructive signed-witness compiler.

This verifies finite algebra, not the analytic interpolation theorem, the
all-degree null-polynomial proof, historical priority, or sharp quasiconvexity.
Inputs in this replay use rational sigma and rational polynomial coefficients.
"""
from collections import defaultdict
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
import math
import sympy as S

OUT = Path(__file__).resolve().parent
a, b, c, q, eps = S.symbols("a b c q eps")
X, Y, Z, K = S.symbols("X Y Z K")
VARS = (a, b, c, q)


def require(test, message):
    if not test:
        raise RuntimeError(message)


def fstr(x):
    return str(F(x))


def terms(expr):
    return [(mon, F(coef)) for mon, coef in S.Poly(expr, *VARS).terms()]


def weight(mon):
    return mon[0] + 2 * (mon[2] + mon[3])


def weighted_parts(expr):
    result = defaultdict(lambda: S.Integer(0))
    for mon, coef in terms(expr):
        result[weight(mon)] += S.Rational(coef.numerator, coef.denominator) * math.prod(
            var ** n for var, n in zip(VARS, mon)
        )
    return dict(sorted(result.items()))


def evaluate(ts, values):
    return sum(coef * math.prod(v ** n for v, n in zip(values, mon)) for mon, coef in ts)


def mixed_coefficient(ts, vectors):
    """Coefficient t1...tm in R(sum t_i v_i), via finite differences."""
    m = len(vectors)
    answer = F(0)
    for mask in range(1 << m):
        value = [F(0)] * 4
        for i, vector in enumerate(vectors):
            if mask & (1 << i):
                value = [x + y for x, y in zip(value, vector)]
        answer += (-1) ** (m - mask.bit_count()) * evaluate(ts, value)
    return answer


def clean(poly):
    return {key: val for key, val in poly.items() if val}


def add(*polys):
    result = defaultdict(F)
    for poly in polys:
        for key, value in poly.items():
            result[key] += value
    return clean(result)


def scale(poly, scalar):
    return clean({key: value * scalar for key, value in poly.items()})


def times(left, right):
    result = defaultdict(F)
    for (el, xl, yl), cl in left.items():
        for (er, xr, yr), cr in right.items():
            result[(el + er, xl + xr, yl + yr)] += cl * cr
    return clean(result)


def power(poly, n):
    answer = {(0, 0, 0): F(1)}
    for _ in range(n):
        answer = times(answer, poly)
    return answer


def cosine_bank(frequencies, amplitudes, assignment):
    """assignment False: psi cosine; True: independent k cosine."""
    psi = defaultdict(F)
    scalar = defaultdict(F)
    for freq, amp, is_scalar in zip(frequencies, amplitudes, assignment):
        dest = scalar if is_scalar else psi
        for sign in (-1, 1):
            dest[(sign * freq[0], sign * freq[1])] += F(amp, 2)
    return clean(psi), clean(scalar)


def hessian_component(poly, i, j):
    return {freq: -freq[i] * freq[j] * coef for freq, coef in poly.items()}


def correction_component(poly, i, j, factor=F(1)):
    return {
        freq: factor * F(freq[i] * freq[j], freq[0] ** 2 + freq[1] ** 2) * coef
        for freq, coef in poly.items()
    }


def graded(poly, exponent):
    return {(exponent, *freq): coef for freq, coef in poly.items() if coef}


def gradient_family(psi, scalar, sigma):
    aa = add(graded(hessian_component(psi, 0, 1), 1),
             graded(correction_component(scalar, 0, 0, 1 / sigma), 2))
    bb = add(graded(hessian_component(psi, 1, 1), 0),
             graded(correction_component(scalar, 0, 1, 1 / sigma), 1))
    cc = add(scale(graded(hessian_component(psi, 0, 0), 2), -sigma),
             graded(correction_component(scalar, 0, 1), 3))
    qq = graded(scalar, 2)
    dd = add(qq, scale(aa, -sigma))
    return aa, bb, cc, qq, dd


def polynomial_average(expr, fields):
    result = defaultdict(F)
    for mon, coef in terms(expr):
        term = {(0, 0, 0): coef}
        for field, n in zip(fields, mon):
            term = times(term, power(field, n))
        for (ee, xx, yy), value in term.items():
            if xx == yy == 0:
                result[ee] += value
    return dict(sorted(clean(result).items()))


def value_at_eps(avg, e):
    return sum(coef * e ** n for n, coef in avg.items())


def norm_sup_bound(poly):
    return sum(abs(coef) for coef in poly.values())


def serialized_fourier(poly):
    return [{"frequency": list(freq), "complex_exponential_coefficient": fstr(coef)}
            for freq, coef in sorted(poly.items())]


def compile_witness(expr, sigma, alpha):
    """Find the bounded-frequency leading signed witness, then exact epsilon data.

    No assertion of non-nullness is hidden: an exhausted bank raises an error.
    The theorem proves exhaustion cannot occur for a non-null leading part.
    """
    ts = terms(expr)
    degrees = {sum(mon) for mon, _ in ts}
    require(len(degrees) == 1, "homogeneous input required")
    m = degrees.pop()
    require(m >= 2, "degree must be at least two")
    parts = weighted_parts(expr)
    j, leading = next(iter(parts.items()))
    require(j < 2 * alpha, "input is not excluded at requested defect power")
    leading_terms = terms(leading)
    tested = 0
    found = None
    # Five positive values suffice because the resonance polynomial has degree
    # at most four in each coordinate, with the final frequency minus the sum.
    for assignment in product((False, True), repeat=m):
        for entries in product(range(1, 6), repeat=2 * (m - 1)):
            freqs = [tuple(entries[2 * i:2 * i + 2]) for i in range(m - 1)]
            freqs.append(tuple(-sum(freq[d] for freq in freqs) for d in (0, 1)))
            vectors = [
                (F(0), F(0), F(0), F(1)) if is_scalar
                else (-F(x * y), -F(y * y), sigma * x * x, F(0))
                for (x, y), is_scalar in zip(freqs, assignment)
            ]
            tested += 1
            coefficient = mixed_coefficient(leading_terms, vectors)
            if coefficient:
                found = (assignment, freqs, coefficient)
                break
        if found:
            break
    require(found is not None, "bounded frequency bank exhausted")
    assignment, freqs, coefficient = found
    # Merge equal cosine frequencies within the same source BEFORE choosing
    # amplitudes. Original labelled-slot amplitudes could add up beyond m+1.
    # The labelled integral is the grouped polynomial evaluated on sums, so a
    # nonzero labelled polynomial implies a nonzero grouped polynomial.
    groups = []
    for typ, freq in zip(assignment, freqs):
        canonical = freq if freq[0] > 0 or (freq[0] == 0 and freq[1] > 0) else tuple(-v for v in freq)
        group = (typ, canonical)
        if group not in groups:
            groups.append(group)
    grouped_assignment = tuple(typ for typ, _ in groups)
    grouped_freqs = tuple(freq for _, freq in groups)
    amplitude_tests = 0
    selected = None
    for amplitudes in product(range(1, m + 2), repeat=len(groups)):
        amplitude_tests += 1
        psi, scalar = cosine_bank(grouped_freqs, amplitudes, grouped_assignment)
        fields = gradient_family(psi, scalar, sigma)
        leading_avg = polynomial_average(leading, fields[:4])
        if leading_avg.get(j, F(0)):
            selected = (amplitudes, psi, scalar, fields)
            break
    require(selected is not None, "amplitude interpolation grid exhausted")
    amplitudes, psi, scalar, fields = selected
    require(len(groups) <= m and len(groups) == len(set(groups)), "grouped mode count failed")
    require(all(1 <= amp <= m + 1 for amp in amplitudes), "merged cosine amplitude bound failed")
    aa, bb, cc, qq, dd = fields
    avg = polynomial_average(expr, fields[:4])
    require(min(avg) == j, "wrong leading power")
    determinant_avg = polynomial_average(a * q - sigma * a * a - b * c, fields[:4])
    require(not determinant_avg, "family is not determinant-null")
    # Fourier compatibility: a_y=b_x, c_y=d_x in the base coordinates with
    # physical y derivative N*partial_y, i.e. epsilon exponent minus one.
    def derivative(poly, direction):
        return clean({(ee - (direction == 1), xx, yy): coef * (xx, yy)[direction]
                      for (ee, xx, yy), coef in poly.items()})
    require(derivative(aa, 1) == derivative(bb, 0), "first row curl failed")
    require(derivative(cc, 1) == derivative(dd, 0), "second row curl failed")
    rest = sum(abs(coef) for ee, coef in avg.items() if ee > j)
    threshold = max(1, math.ceil(2 * rest / abs(avg[j])))
    M0 = sum(norm_sup_bound(field) for field in (aa, bb, cc, dd))
    E0 = norm_sup_bound(qq) + norm_sup_bound(cc)
    # Each defect field has epsilon order >=2, so E<=E0*N^-2 for N>=1;
    # M<=M0. Therefore ratio>=abs(I_j)/(2 E0^alpha M0^(m-alpha))*N^(2alpha-j).
    require(E0 > 0 and M0 > 0, "zero norm budget in witness")
    return {
        "degree": m,
        "polynomial_in_a_b_c_q": str(S.expand(expr)),
        "sigma": fstr(sigma),
        "excluded_defect_power": fstr(alpha),
        "leading_weight": j,
        "leading_signed_average": fstr(avg[j]),
        "resonance_mixed_coefficient": fstr(coefficient),
        "cosine_product_average": fstr(F(1, 2 ** (m - 1))),
        "resonance_slots": [{"source": "k" if typ else "psi", "frequency": list(freq)}
                            for typ, freq in zip(assignment, freqs)],
        "slots": [{"source": "k" if typ else "psi", "frequency": list(freq), "amplitude": amp}
                  for typ, freq, amp in zip(grouped_assignment, grouped_freqs, amplitudes)],
        "distinct_source_cosine_mode_count": len(groups),
        "maximum_merged_mode_cosine_amplitude": max(amplitudes),
        "universal_merged_mode_cosine_amplitude_bound": m + 1,
        "psi_fourier": serialized_fourier(psi),
        "k_fourier": serialized_fourier(scalar),
        "exact_signed_epsilon_polynomial": {str(ee): fstr(coef) for ee, coef in avg.items()},
        "all_N_at_least": threshold,
        "gradient_norm_upper_bound_M0": fstr(M0),
        "defect_norm_upper_bound_E0_times_N_minus_2": fstr(E0),
        "ratio_lower_growth_power": fstr(2 * alpha - j),
        "ratio_lower_prefactor": f"{fstr(abs(avg[j]))}/(2*({fstr(E0)})^({fstr(alpha)})*({fstr(M0)})^({fstr(m-alpha)}))",
        "tested_resonances": tested,
        "tested_amplitudes": amplitude_tests,
        "worst_case_resonance_test_count": 2 ** m * 5 ** (2 * (m - 1)),
        "worst_case_amplitude_test_count": (m + 1) ** len(groups),
        "universal_worst_case_amplitude_test_count": (m + 1) ** m,
        "max_frequency_coordinate": max(abs(x) for freq in freqs for x in freq),
        "universal_max_frequency_coordinate": 5 * (m - 1),
        "row_curl_exact": True,
        "determinant_average_exact_zero": True,
    }


def nullspace_check(m):
    mons = []
    for xx in range(m + 1):
        for yy in range(m - xx + 1):
            for zz in range(m - xx - yy + 1):
                kk = m - xx - yy - zz
                mons.append(X ** xx * Y ** yy * Z ** zz * K ** kk)
    columns = []
    coordinates = set()
    for mon in mons:
        pieces = (S.diff(mon, K), S.diff(mon, X, 2), S.diff(mon, X, Y),
                  S.diff(mon, Y, Z), S.diff(mon, Z, 2),
                  S.diff(mon, Y, 2) + 2 * S.diff(mon, X, Z))
        col = {}
        for i, piece in enumerate(pieces):
            for exponents, coef in S.Poly(piece, X, Y, Z, K).terms():
                if coef:
                    col[(i, exponents)] = coef
                    coordinates.add((i, exponents))
        columns.append(col)
    rows = sorted(coordinates)
    matrix = S.Matrix([[col.get(row, 0) for col in columns] for row in rows])
    basis = matrix.nullspace()
    expected = 1 if m == 2 else 0
    require(len(basis) == expected, f"unexpected null dimension at degree {m}")
    polynomials = [S.expand(sum(coef * mon for coef, mon in zip(v, mons))) for v in basis]
    if m == 2:
        require(S.expand(polynomials[0] / S.Poly(polynomials[0], X, Y, Z, K).coeff_monomial(X * Z)
                         - (X * Z - Y * Y)) == 0, "wrong determinant kernel")
    return {"degree": m, "polynomial_dimension": len(mons),
            "constraint_rank": matrix.rank(), "null_dimension": len(basis),
            "null_basis": [str(v) for v in polynomials]}


def main():
    sigma = F(2)
    checks = []
    for m in range(2, 9):
        checks.append(nullspace_check(m))
    dimensions = {}
    for m in range(2, 9):
        counts = defaultdict(int)
        for u in range(m + 1):
            for v in range(m - u + 1):
                for w in range(m - u - v + 1):
                    z = m - u - v - w
                    counts[weight((u, v, w, z))] += 1
        require(sum(counts.values()) == math.comb(m + 3, 3), "dimension sum failed")
        require(sum(n for wt, n in counts.items() if wt >= 2) == math.comb(m + 3, 3) - 2,
                "power-one codimension failed")
        dimensions[str(m)] = dict(sorted(counts.items()))
    r = S.symbols("r", positive=True)
    kappa = r * (r + 2) / 3
    target = S.expand(q * (2 * a * q - (r + 2) * a * a + r * c * c - 2 * b * c)
                      - kappa * a * (a * a + c * c))
    target_parts = weighted_parts(target.subs(r, 1))
    require(min(target_parts) == 3 and target_parts[3] == -a ** 3, "target weight failed")
    examples = [
        ("forbidden_first_jet_cubic", a * b ** 2, F(1)),
        ("single_wave_invisible_cubic", (sigma * a * a + b * c) * b, F(3, 2)),
        ("independent_defect_cubic", q * b ** 2, F(3, 2)),
        ("target_cubic_exponent_obstruction", target.subs(r, 1), F(2)),
        ("single_wave_invisible_quartic", (sigma * a * a + b * c) ** 2, F(5, 2)),
        ("quadratic_partial_determinant", -sigma * a * a - b * c, F(2)),
    ]
    witnesses = {}
    for name, expr, alpha in examples:
        # In the last case remove the true determinant first. The remainder -a*q
        # has the same signed integral but a detectable weight-three leading part.
        if name == "quadratic_partial_determinant":
            expr = S.expand(expr - (a * q - sigma * a * a - b * c))
            require(expr == -a * q, "quadratic subtraction failed")
        witnesses[name] = compile_witness(expr, sigma, alpha)
    # Check Jordan canonical form algebra independently for a nontrivial pencil.
    xx, yy = S.symbols("xi_x xi_y")
    A0 = S.Matrix([[2, 1], [1, 1]])
    S0 = S.Matrix([[1, 2], [3, 5]])
    J = S.Matrix([[0, 1], [0, 0]])
    B0 = A0 * S0 * J * S0.inv()
    pencil = A0 * xx + B0 * yy
    canonical = S.simplify(S0.inv() * A0.inv() * pencil * S0)
    require(canonical == S.Matrix([[xx, yy], [0, xx]]), "Jordan pencil reduction failed")
    sig = S.symbols("sigma", positive=True)
    av = -eps + eps ** 2 / (2 * sig)
    bv = av / eps
    cv = sig * eps ** 2 + eps ** 3 / 2
    dv = cv / eps
    qv = S.expand(sig * av + dv)
    require(qv == eps ** 2, "all-sigma quadratic defect failed")
    require(S.expand(av * dv - bv * cv) == 0, "all-sigma quadratic determinant failed")
    quadratic_mean = S.expand(-(sig * av ** 2 + bv * cv) / 2)
    require(S.expand(quadratic_mean - (eps ** 3 / 2 - eps ** 4 / (4 * sig))) == 0,
            "all-sigma quadratic average failed")
    tnorm = S.symbols("t", positive=True)
    sharp_rhs = S.simplify(sig ** S.Rational(-1, 2) * (sig * tnorm) ** S.Rational(3, 2)
                           * tnorm ** S.Rational(1, 2))
    require(S.simplify(sharp_rhs - sig * tnorm ** 2) == 0, "quadratic equality fixture failed")
    receipt = {
        "version": 2,
        "status": "finite exact algebra checks passed; analytic theorem and extensions remain unreviewed",
        "historical_priority": "UNKNOWN",
        "external_verification": "UNKNOWN",
        "null_polynomial_checks": checks,
        "weighted_dimensions": dimensions,
        "target_cubic_weight_parts_r1": {str(wt): str(v) for wt, v in target_parts.items()},
        "canonical_pencil_fixture": {"A": str(A0), "B": str(B0), "S": str(S0),
                                     "determinant": str(S.factor(pencil.det())),
                                     "reduced": str(canonical)},
        "sharp_quadratic_fixture": {"all_sigma_q": str(qv), "all_sigma_signed_mean": str(quadratic_mean),
                                    "equality_rhs": str(sharp_rhs),
                                    "constant": "sigma^(-1/2)", "optimal_defect_power": "3/2"},
        "witnesses": witnesses,
        "limits": ["No analytic interpolation theorem is machine verified.",
                   "No all-degree null-Lagrangian proof is machine verified.",
                   "No optimal estimate constant is computed.",
                   "No sharp conformal quasiconvexity conclusion follows.",
                   "The finite-frequency and pencil extensions need separate mathematical audit."]
    }
    (OUT / "VERIFICATION_RECEIPT.json").write_text(json.dumps(receipt, indent=2) + "\n")
    for name, witness in witnesses.items():
        print(name, "weight", witness["leading_weight"], "leading average", witness["leading_signed_average"],
              "tests", witness["tested_resonances"], witness["tested_amplitudes"])
    print("PASS: exact null constraints through degree 8, dimensions, target weights, 6 compatible witnesses, Jordan fixture")


if __name__ == "__main__":
    main()
