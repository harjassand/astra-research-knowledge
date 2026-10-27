"""Exact rational Hermite certificate for the frozen cosine-fixture sampler.

All polynomial arithmetic, squared norms, elementary-constant enclosures and
tail bounds are rational. Floats are used only when printing final numbers.
This is a fixture certificate, not a certificate for an arbitrary black box.
"""

from __future__ import annotations

import csv
import math
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path


ROOT = Path(__file__).resolve().parent
N = 64  # first omitted even Hermite degree of h
ELL = F(7, 20)


def add(*polys):
    out = {}
    for p in polys:
        for key, value in p.items():
            out[key] = out.get(key, F(0)) + value
    return {key: value for key, value in out.items() if value}


def scale(p, factor):
    return {key: value * factor for key, value in p.items() if value * factor}


@lru_cache(None)
def factors(i, j):
    return tuple((i + j - 2 * k, math.factorial(k) * math.comb(i, k) * math.comb(j, k)) for k in range(min(i, j) + 1))


def mul(a, b):
    out = {}
    for (i, j), av in a.items():
        for (k, l), bv in b.items():
            value = av * bv
            for p, gp in factors(i, k):
                for q, gq in factors(j, l):
                    key = (p, q)
                    out[key] = out.get(key, F(0)) + value * gp * gq
    return {key: value for key, value in out.items() if value}


def derivative(p, coordinate):
    out = {}
    for (i, j), value in p.items():
        degree = (i, j)[coordinate]
        if degree:
            key = (i - 1, j) if coordinate == 0 else (i, j - 1)
            out[key] = value * degree
    return out


def norm2_squared(p, hyper_weight=1):
    return sum((value * value * math.factorial(i) * math.factorial(j) * hyper_weight ** (i + j) for (i, j), value in p.items()), F(0))


def sqrt_bounds(value, digits=40):
    scale_value = 10**digits
    n = math.isqrt(value.numerator * scale_value**2 // value.denominator)
    lo = F(n, scale_value)
    hi = lo if n * n * value.denominator == value.numerator * scale_value**2 else F(n + 1, scale_value)
    assert lo * lo <= value <= hi * hi
    return lo, hi


def norm_upper(p, hyper_weight=1):
    return sqrt_bounds(norm2_squared(p, hyper_weight))[1]


def exp_negative_bounds(x, terms=100):
    # Alternating-series enclosure; terms decrease throughout the retained tail.
    term, total = F(1), F(1)
    for k in range(1, terms + 1):
        term *= -x / k
        total += term
    next_total = total + term * (-x) / (terms + 1)
    return min(total, next_total), max(total, next_total)


def atan_bounds(x, terms=100):
    total = sum(((-1) ** k * x ** (2 * k + 1) / (2 * k + 1) for k in range(terms)), F(0))
    next_total = total + (-1) ** terms * x ** (2 * terms + 1) / (2 * terms + 1)
    return min(total, next_total), max(total, next_total)


def elementary_bounds():
    atan5 = atan_bounds(F(1, 5))
    atan239 = atan_bounds(F(1, 239))
    pi_lo = 16 * atan5[0] - 4 * atan239[1]
    pi_hi = 16 * atan5[1] - 4 * atan239[0]
    terms = 100
    log2_lo = 2 * sum((F(1, 3) ** (2 * k + 1) / (2 * k + 1) for k in range(terms)), F(0))
    log2_hi = log2_lo + 2 * F(1, 3) ** (2 * terms + 1) / ((2 * terms + 1) * (1 - F(1, 9)))
    sqrt2_lo, sqrt2_hi = sqrt_bounds(F(2))
    _, sqrt6_hi = sqrt_bounds(F(6))
    denominator_lo = sqrt_bounds(2 * pi_lo)[0]
    exp_half = exp_negative_bounds(F(1, 2))
    exp_three_halves = exp_negative_bounds(F(3, 2))
    phi0_hi = 1 / denominator_lo
    phi1_hi = exp_half[1] / denominator_lo
    phi3_hi = exp_three_halves[1] / denominator_lo
    return {
        "a_lower": ELL * exp_half[0],
        "a_upper": ELL * exp_half[1],
        "C2": log2_hi / sqrt2_lo,
        "C3": sqrt6_hi * (1 - pi_lo / 4),
        "C4": sqrt2_hi / 2,
        "scalar_C2": phi1_hi * log2_hi,
        "scalar_C3": (phi0_hi + 4 * phi3_hi) * (1 - pi_lo / 4),
        "scalar_C4": phi1_hi,
    }


def tail_weighted_squared(first_degree):
    # Sum_{m>=n} 7^m/m! <= first_term / (1-7/(n+1)).
    assert first_degree + 1 > 7
    return F(7**first_degree, math.factorial(first_degree)) / (1 - F(7, first_degree + 1))


def main():
    with (ROOT / "galerkin_S_rational.csv").open() as inp:
        rows = list(csv.DictReader(inp))
    s = {
        (int(r["hermite_G_degree"]), int(r["hermite_Z_degree"])):
        F(int(r["numerator"]), int(r["denominator"]))
        for r in rows if int(r["numerator"])
    }
    one, g, z = {(0, 0): F(1)}, {(1, 0): F(1)}, {(0, 1): F(1)}
    sg, sz = derivative(s, 0), derivative(s, 1)
    sgg, sgz, szz = derivative(sg, 0), derivative(sg, 1), derivative(sz, 1)
    hbase = {(m, 0): F((-1) ** (m // 2), math.factorial(m)) for m in range(0, N, 2)}
    hcenter = add(hbase, scale(one, -1))
    kbase = {(m - 1, 0): F((-1) ** (m // 2), math.factorial(m)) for m in range(2, N, 2)}
    hpbase = derivative(hbase, 0)

    constants = elementary_bounds()
    # A simple exact rational center for a=ell exp(-1/2), with proved error.
    center_scale = 10**30
    midpoint = (constants["a_lower"] + constants["a_upper"]) / 2
    a0 = F(round(midpoint * center_scale), center_scale)
    da = max(abs(a0 - constants["a_lower"]), abs(a0 - constants["a_upper"]))
    h, k, hp = scale(hcenter, a0), scale(kbase, a0), scale(hpbase, a0)

    r_poly = mul(k, hp)
    u_poly = add(mul(s, z), scale(sz, -1), mul(s, h), scale(mul(sg, k), -1))
    a1 = add(mul(z, sg), scale(sgz, -2))
    a2 = add(one, scale(s, 2))
    a3 = add(mul(g, sg), sgg)
    e_poly = add(
        scale(s, 2), mul(z, sz), scale(szz, -1),
        mul(a2, r_poly), mul(a1, k), scale(mul(mul(sg, k), h), 2),
        scale(mul(a3, mul(k, k)), -1), mul(sz, h),
    )

    # L8 truncation errors from Gaussian hypercontractivity and geometric tails.
    t_h = constants["a_upper"] * sqrt_bounds(tail_weighted_squared(N))[1] + da * norm_upper(hcenter, 7)
    t_k = constants["a_upper"] * sqrt_bounds(tail_weighted_squared(N - 1))[1] + da * norm_upper(kbase, 7)
    t_hp = constants["a_upper"] * sqrt_bounds(tail_weighted_squared(N - 1))[1] + da * norm_upper(hpbase, 7)
    # Hölder: polynomial factors in L4, tails in L4/L8, true K,h' bounded by ell.
    r_error = ELL * (t_k + t_hp) + t_k * t_hp
    u_error = norm_upper(s, 3) * t_h + norm_upper(sg, 3) * t_k
    e_error = (
        norm_upper(a1, 3) * t_k + norm_upper(sz, 3) * t_h
        + norm_upper(a2, 3) * (ELL * (t_k + t_hp) + t_k * t_hp)
        + 2 * norm_upper(sg, 3) * (2 * ELL * t_k + ELL * t_h + t_k * t_h)
        + norm_upper(a3, 3) * (2 * ELL * t_k + t_k * t_k)
    )
    r_upper = norm_upper(r_poly) + r_error
    u_upper = norm_upper(u_poly) + u_error
    e_upper = norm_upper(e_poly) + e_error
    variance_upper = ELL**2 * (norm2_squared(s) + norm2_squared(sg))
    second_moment_upper = u_upper**2 + variance_upper
    conservative = constants["C2"] * e_upper + constants["C3"] * r_upper * u_upper + constants["C4"] * second_moment_upper
    sharp = constants["scalar_C2"] * e_upper + constants["scalar_C3"] * r_upper * u_upper + constants["scalar_C4"] * second_moment_upper

    # These rounded publication ceilings are themselves checked by rational comparison.
    conservative_ceiling = F(1, 1000)
    sharp_ceiling = F(331, 1000000)
    assert conservative < conservative_ceiling
    assert sharp < sharp_ceiling
    quantities = {
        "full_equation_residual_L2_upper": e_upper,
        "initial_R_L2_upper": r_upper,
        "true_u_L2_upper": u_upper,
        "four_query_variance_upper": variance_upper,
        "four_query_second_moment_upper": second_moment_upper,
        "h_L8_tail_upper": t_h,
        "K_L8_tail_upper": t_k,
        "hprime_L8_tail_upper": t_hp,
        "full_residual_L2_tail_upper": e_error,
        "conservative_full_law_TV_upper": conservative,
        "sharp_scalar_full_law_TV_upper": sharp,
    }
    with (ROOT / "galerkin_exact_rational_bounds.csv").open("w", newline="") as out:
        writer = csv.writer(out)
        writer.writerow(["quantity", "numerator", "denominator", "decimal_display_only"])
        for name, value in quantities.items():
            writer.writerow([name, value.numerator, value.denominator, float(value)])
    lines = [
        "EXACT RATIONAL FULL-LAW CERTIFICATE: PASS",
        "Fixture h(x)=(7/20)cos(x); target N((7/20)exp(-1/2),2).",
        "Polynomial S is exactly the frozen dyadic coefficient file.",
        "All polynomial squared norms and tail/constant enclosures used rational arithmetic.",
        "Gaussian hypercontractivity controls omitted Hermite tails in L8.",
    ]
    lines += [f"{name}: {float(value):.16g}" for name, value in quantities.items()]
    lines += [
        "Rationally verified conservative bound: TV < 1/1000.",
        "Rationally verified sharper scalar bound: TV < 331/1000000.",
        "Every ideal-real runtime sample uses exactly four h-value queries plus Gaussian seeds; the uniform is Gaussian-derived.",
        "The polynomial acquisition cost is separate and already paid: 73,776 h-value queries.",
        "This certificate uses the known analytic cosine fixture only in post-fit verification.",
        "The code execution is floating point; this certificate concerns its specified exact-real mathematical sampler.",
        "No finite-bit continuous-TV claim or full rounding-error certificate is made.",
        "It is not a data-only certificate for arbitrary unknown C1,1 sources.",
        "It is not a practical or query-complexity improvement over ordinary scalar competitors.",
    ]
    report = "\n".join(lines) + "\n"
    (ROOT / "EXACT_GALERKIN_CERTIFICATE.txt").write_text(report)
    print(report, end="")


if __name__ == "__main__":
    main()
