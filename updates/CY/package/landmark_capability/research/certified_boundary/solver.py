#!/usr/bin/env python3
"""Finite-bit certified boundary resolvent for a product two-state CTMC.

All numerical quantities are enclosed by integer dyadic intervals.  The only
quadrature is a positive log-time trapezoid; its scalar error is bounded by
the Mellin/Poisson formula stated in RESULT.txt.  This is a small numerical
primitive, not a general high-performance linear algebra package.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import isqrt
import json
import time
from pathlib import Path


# The internal fixed-point grid.  All interval endpoints are integers divided
# by SCALE.  The proof does not assume round-to-nearest anywhere.
PRECISION_BITS = 224
SCALE = 1 << PRECISION_BITS


@dataclass(frozen=True)
class Iv:
    lo: int
    hi: int

    def __post_init__(self) -> None:
        if self.lo > self.hi:
            raise ValueError("reversed interval")


ZERO = Iv(0, 0)
ONE = Iv(SCALE, SCALE)


def ceildiv(a: int, b: int) -> int:
    if b <= 0:
        raise ValueError("nonpositive denominator")
    return -((-a) // b)


def iv_fraction(x: Fraction) -> Iv:
    n = x.numerator * SCALE
    d = x.denominator
    return Iv(n // d, ceildiv(n, d))


def iv_add(a: Iv, b: Iv) -> Iv:
    return Iv(a.lo + b.lo, a.hi + b.hi)


def iv_sub(a: Iv, b: Iv) -> Iv:
    return Iv(a.lo - b.hi, a.hi - b.lo)


def iv_mul(a: Iv, b: Iv) -> Iv:
    if min(a.lo, b.lo) < 0:
        raise ValueError("iv_mul is used only for nonnegative intervals")
    return Iv((a.lo * b.lo) // SCALE,
              ceildiv(a.hi * b.hi, SCALE))


def iv_scale(a: Iv, x: Fraction) -> Iv:
    if x < 0 or a.lo < 0:
        raise ValueError("iv_scale is used only for nonnegative intervals")
    n, d = x.numerator, x.denominator
    return Iv((a.lo * n) // d, ceildiv(a.hi * n, d))


def iv_div(a: Iv, b: Iv) -> Iv:
    if a.lo < 0 or b.lo <= 0:
        raise ValueError("iv_div requires nonnegative numerator and positive denominator")
    return Iv((a.lo * SCALE) // b.hi,
              ceildiv(a.hi * SCALE, b.lo))


def iv_sqrt_fraction(x: Fraction) -> Iv:
    if x < 0:
        raise ValueError("negative square root")
    scaled_square = (x.numerator * SCALE * SCALE) // x.denominator
    q = isqrt(scaled_square)
    exact = q * q * x.denominator == x.numerator * SCALE * SCALE
    return Iv(q, q if exact else q + 1)


def iv_complement(a: Iv) -> Iv:
    return Iv(SCALE - a.hi, SCALE - a.lo)


def exp_neg_point(x: int) -> Iv:
    """Enclose exp(-x/SCALE), for a nonnegative fixed-point x."""
    if x < 0:
        raise ValueError("negative exponential argument")
    if x == 0:
        return ONE
    # e > 2, so exp(-x) <= 2^-x.  This enclosure is useful when the
    # exponential is too small to affect the requested dyadic precision.
    if x >= PRECISION_BITS * SCALE:
        return Iv(0, 1)

    # Range reduction to z=x/2^k <= 1.  Its endpoints are rounded outwards.
    k = 0
    while x > (SCALE << k):
        k += 1
    divisor = 1 << k
    z = Iv(x // divisor, ceildiv(x, divisor))

    # Alternating Taylor series for exp(-z), z in [0,1].  Every term and
    # partial sum is outward rounded; once a term is one fixed-point unit,
    # the entire remaining alternating tail is at most one more unit.
    term = ONE
    total = ONE
    for j in range(1, 2000):
        term = iv_scale(iv_mul(term, z), Fraction(1, j))
        if j & 1:
            total = iv_sub(total, term)
        else:
            total = iv_add(total, term)
        if term.hi <= 1:
            total = Iv(max(0, total.lo - 1), min(SCALE, total.hi + 1))
            break
    else:
        raise ArithmeticError("Taylor enclosure did not converge")

    for _ in range(k):
        total = iv_mul(total, total)
    return Iv(max(0, total.lo), min(SCALE, total.hi))


def exp_neg(a: Iv) -> Iv:
    """Monotone interval extension of exp(-x) for x >= 0."""
    if a.lo < 0:
        raise ValueError("negative exponential interval")
    low = exp_neg_point(a.hi)
    high = exp_neg_point(a.lo)
    return Iv(low.lo, high.hi)


def log_ratio_interval(j: int) -> Iv:
    """Enclose log(1+1/j) by the positive atanh series."""
    z = Fraction(1, 2 * j + 1)
    z2 = z * z
    total = Fraction(0)
    power = z
    count = 0
    while True:
        total += 2 * power / (2 * count + 1)
        count += 1
        power *= z2
        remainder = 2 * power / ((2 * count + 1) * (1 - z2))
        if remainder * SCALE <= 1:
            break
    return Iv(iv_fraction(total).lo,
              iv_fraction(total + remainder).hi)


def interval_fraction(iv: Iv) -> tuple[Fraction, Fraction]:
    return Fraction(iv.lo, SCALE), Fraction(iv.hi, SCALE)


def midpoint(iv: Iv) -> Fraction:
    return Fraction(iv.lo + iv.hi, 2 * SCALE)


def radius(iv: Iv) -> Fraction:
    return Fraction(iv.hi - iv.lo, 2 * SCALE)


def dyadic_string(x: Fraction, bits: int) -> str:
    den = 1 << bits
    scaled = x * den
    if scaled.denominator != 1:
        raise ValueError("not on requested dyadic grid")
    return f"{scaled.numerator}/{den}"


def frac_json(x: Fraction) -> str:
    return f"{x.numerator}/{x.denominator}"


def grid_nodes(s: Fraction, alpha_max: Fraction, delta: Fraction,
               delta_bits: int, jstep: int) -> tuple[list[Iv], Iv]:
    """Construct a rationally enclosed geometric log grid.

    The exact ratio is (jstep+1)/jstep, with exact step
    log(1+1/jstep).  The returned q intervals enclose every exact node.
    """
    ratio = Fraction(jstep + 1, jstep)
    inv_ratio = 1 / ratio
    q0 = ONE

    q_negative = [q0]
    q = q0
    low_cut = delta / (64 * alpha_max)
    while Fraction(q.hi, SCALE) > low_cut:
        previous = q
        q = iv_scale(q, inv_ratio)
        if q == previous:
            raise ArithmeticError("fixed-point grid too coarse for lower quadrature cutoff; increase PRECISION_BITS")
        q_negative.append(q)

    q_positive = [q0]
    q = q0
    high_cut = Fraction(delta_bits + 8, 1) / s
    while Fraction(q.lo, SCALE) < high_cut:
        q = iv_scale(q, ratio)
        q_positive.append(q)

    nodes = list(reversed(q_negative)) + q_positive[1:]
    return nodes, log_ratio_interval(jstep)


def exact_inverse(matrix: list[list[Fraction]]) -> list[list[Fraction]]:
    n = len(matrix)
    aug = [list(row) + [Fraction(i == j) for j in range(n)]
           for i, row in enumerate(matrix)]
    for col in range(n):
        pivot = max(range(col, n), key=lambda row: abs(aug[row][col]))
        if aug[pivot][col] == 0:
            raise ArithmeticError("midpoint boundary matrix is singular")
        aug[col], aug[pivot] = aug[pivot], aug[col]
        d = aug[col][col]
        aug[col] = [x / d for x in aug[col]]
        for row in range(n):
            if row == col:
                continue
            d = aug[row][col]
            if d:
                aug[row] = [x - d * y for x, y in zip(aug[row], aug[col])]
    return [row[n:] for row in aug]


def certified_boundary_resolvent(
        p_input: list[Fraction],
        rates_input: list[Fraction],
        initial_input: list[Fraction],
        targets_input: list[int],
        s_input: Fraction,
        delta_bits: int = 100,
        output_bits: int = 48) -> dict:
    """Return certified enclosures for K_B(s), w_mu(s), and the hit LT.

    Inputs are exact rationals.  The product chain itself is never enumerated;
    work scales with the number of coordinates, requested targets, and
    arithmetic precision.  Keep m small: the only dense solve is m by m.
    """
    start = time.time()
    p = [Fraction(x) for x in p_input]
    rates = [Fraction(x) for x in rates_input]
    initial = [Fraction(x) for x in initial_input]
    targets = list(targets_input)
    s = Fraction(s_input)
    n = len(p)
    if n == 0 or len(rates) != n or len(initial) != n:
        raise ValueError("p, rates, and initial must have the same positive length")
    if any(not (0 < x < 1) for x in p):
        raise ValueError("stationary probabilities must lie strictly between 0 and 1")
    if any(x <= 0 for x in rates) or any(not (0 <= x <= 1) for x in initial):
        raise ValueError("rates must be positive and initial probabilities in [0,1]")
    if s <= 0 or delta_bits < 4 or output_bits < 31:
        raise ValueError("need s>0, delta_bits>=4, and output_bits>=31")
    if not targets or len(set(targets)) != len(targets):
        raise ValueError("targets must be a nonempty list of distinct states")
    if any(x < 0 or x >= (1 << n) for x in targets):
        raise ValueError("target outside the n-bit state space")
    delta = Fraction(1, 1 << delta_bits)
    jstep = delta_bits + 10
    alpha_max = s + sum(rates, Fraction(0))
    nodes, h_iv = grid_nodes(s, alpha_max, delta, delta_bits, jstep)

    p_iv = [iv_fraction(x) for x in p]
    one_minus_p = [iv_complement(x) for x in p_iv]
    r_iv = [iv_fraction(x) for x in initial]
    one_minus_r = [iv_complement(x) for x in r_iv]
    cross_const = [iv_sqrt_fraction(x * (1 - x)) for x in p]
    rates_iv = [iv_fraction(x) for x in rates]
    target_count = len(targets)
    kernel_sum = [[ZERO for _ in range(target_count)]
                  for _ in range(target_count)]
    initial_sum = [ZERO for _ in range(target_count)]

    for q in nodes:
        weight = iv_mul(iv_mul(h_iv, q), exp_neg(iv_scale(q, s)))
        exp_by_coordinate = [exp_neg(iv_scale(q, rate))
                             for rate in rates]

        for a in range(target_count):
            ta = targets[a]
            for b in range(a, target_count):
                tb = targets[b]
                product = ONE
                for i in range(n):
                    ai = (ta >> i) & 1
                    bi = (tb >> i) & 1
                    e = exp_by_coordinate[i]
                    if ai != bi:
                        factor = iv_mul(cross_const[i], iv_complement(e))
                    elif ai == 0:
                        factor = iv_add(one_minus_p[i], iv_mul(p_iv[i], e))
                    else:
                        factor = iv_add(p_iv[i], iv_mul(one_minus_p[i], e))
                    product = iv_mul(product, factor)
                contribution = iv_mul(weight, product)
                kernel_sum[a][b] = iv_add(kernel_sum[a][b], contribution)
                if a != b:
                    kernel_sum[b][a] = kernel_sum[a][b]

            # Initial-law probability at this target under P_q.  Each
            # coordinate is written as a sum of two nonnegative terms.
            product = ONE
            for i in range(n):
                bit = (ta >> i) & 1
                e = exp_by_coordinate[i]
                if bit:
                    stationary, start_mass = p_iv[i], r_iv[i]
                else:
                    stationary, start_mass = one_minus_p[i], one_minus_r[i]
                factor = iv_add(iv_mul(stationary, iv_complement(e)),
                                iv_mul(start_mass, e))
                product = iv_mul(product, factor)
            initial_sum[a] = iv_add(initial_sum[a], iv_mul(weight, product))

    # Convert the boundary free resolvent and cross row into dyadic-centered
    # intervals, then use the renewal identity f_mu(s)=c K^{-1} beta.
    stationary_target_mass = []
    beta_iv = []
    for target in targets:
        mass = Fraction(1)
        for i, pi1 in enumerate(p):
            mass *= pi1 if ((target >> i) & 1) else (1 - pi1)
        stationary_target_mass.append(mass)
        beta_iv.append(iv_sqrt_fraction(mass))
    c_iv = [iv_div(initial_sum[a], beta_iv[a]) for a in range(target_count)]

    k_center = [[midpoint(kernel_sum[a][b]) for b in range(target_count)]
                for a in range(target_count)]
    c_center = [midpoint(x) for x in c_iv]
    beta_center = [midpoint(x) for x in beta_iv]
    k_interval_radius = max(radius(x) for row in kernel_sum for x in row)
    c_interval_radius = max(radius(x) for x in c_iv)
    beta_interval_radius = max(radius(x) for x in beta_iv)

    a_norm_sq = Fraction(1)
    for pi1, r1 in zip(p, initial):
        a_norm_sq *= r1 * r1 / pi1 + (1 - r1) * (1 - r1) / (1 - pi1)
    a_norm_bound = Fraction(iv_sqrt_fraction(a_norm_sq).hi, SCALE)

    quad_matrix_error = delta / s
    entry_error_k = k_interval_radius + quad_matrix_error
    spectral_error_k = target_count * entry_error_k
    spectral_lower = 1 / alpha_max
    if spectral_error_k > spectral_lower / 2:
        raise ArithmeticError("matrix enclosure is too wide for inverse bound")

    inverse_center = exact_inverse(k_center)
    y_center = [sum(inverse_center[i][j] * beta_center[j]
                    for j in range(target_count))
                for i in range(target_count)]
    f_center = sum(c_center[i] * y_center[i]
                   for i in range(target_count))

    # Operator error of the log trapezoid is <= delta/s.  Dividing w_z by
    # sqrt(pi(z)) gives c_z=a^T(sI+A)^-1 e_z, so its added error is bounded
    # by ||a|| delta/s.  The product initial law gives ||a||^2 as the
    # coordinatewise product computed above.
    c_operator_error = a_norm_bound * delta / s
    entry_error_c = c_interval_radius + c_operator_error
    entry_error_beta = beta_interval_radius
    c0_l1 = sum(abs(x) for x in c_center)
    m = target_count
    a0 = alpha_max
    # Perturbation bound with ||K^-1|| <= a0, ||K0^-1|| <= 2 a0,
    # ||K0^-1-K^-1|| <= 4 a0^2 ||K0-K||.  L1 bounds dominate the needed
    # Euclidean norms and make this a rational, explicit error budget.
    f_error_cross = m * entry_error_c * a0
    f_error_inverse = c0_l1 * 4 * a0 * a0 * spectral_error_k
    f_error_beta = c0_l1 * 2 * a0 * m * entry_error_beta
    f_error = f_error_cross + f_error_inverse + f_error_beta

    out_bits = output_bits
    output_scale = 1 << out_bits
    lo_exact = max(Fraction(0), f_center - f_error)
    hi_exact = min(Fraction(1), f_center + f_error)
    lo_int = (lo_exact * output_scale).numerator // (lo_exact * output_scale).denominator
    hi_int = ceildiv((hi_exact * output_scale).numerator,
                     (hi_exact * output_scale).denominator)
    width = Fraction(hi_int - lo_int, output_scale)
    if width > Fraction(1, 1 << 30):
        raise ArithmeticError(f"requested 30-bit enclosure not reached: width={width}")

    k_endpoints = []
    for a in range(target_count):
        row = []
        for b in range(target_count):
            low, high = interval_fraction(kernel_sum[a][b])
            row.append((frac_json(max(Fraction(0), low - quad_matrix_error)),
                        frac_json(high + quad_matrix_error)))
        k_endpoints.append(row)
    w_endpoints = []
    for a, interval in enumerate(initial_sum):
        low, high = interval_fraction(interval)
        w_operator_error = Fraction(beta_iv[a].hi, SCALE) * a_norm_bound * delta / s
        w_endpoints.append((frac_json(max(Fraction(0), low - w_operator_error)),
                            frac_json(high + w_operator_error)))
    elapsed = time.time() - start

    return {
        "status": "interval_certified_boundary_resolvent",
        "elapsed_seconds": elapsed,
        "configuration": {
            "n": n,
            "m": target_count,
            "p": [frac_json(x) for x in p],
            "relaxation_rates": [frac_json(x) for x in rates],
            "initial_product_parameters": [frac_json(x) for x in initial],
            "targets": targets,
            "s": frac_json(s),
            "stationary_target_mass": [frac_json(x) for x in stationary_target_mass],
            "implicit_state_count": str(1 << n),
        },
        "quadrature": {
            "positive_log_nodes": len(nodes),
            "step_ratio": f"{jstep + 1}/{jstep}",
            "step_interval": [str(h_iv.lo), str(h_iv.hi), f"/2^{PRECISION_BITS}"],
            "relative_scalar_error_bound": frac_json(delta),
            "delta_bits": delta_bits,
            "trapezoid_alias_bound": frac_json(Fraction(1, 1 << jstep)),
            "negative_tail_relative_bound": frac_json(delta / 64),
            "positive_tail_relative_bound": frac_json(Fraction(1, 1 << (delta_bits + 8))),
        },
        "free_boundary_resolvent_K_enclosure": k_endpoints,
        "cross_row_w_enclosure": w_endpoints,
        "hitting_laplace_transform": {
            "definition": "E_mu[exp(-s H_B)] = c K_B(s)^(-1) beta",
            "lower": dyadic_string(Fraction(lo_int, output_scale), out_bits),
            "upper": dyadic_string(Fraction(hi_int, output_scale), out_bits),
            "width": frac_json(width),
            "midpoint_approximation": frac_json(f_center),
            "certified_absolute_error_before_output_rounding": frac_json(f_error),
        },
        "proof_error_budget": {
            "internal_fixed_point_bits": PRECISION_BITS,
            "initial_vector_norm_upper_bound": frac_json(a_norm_bound),
            "target_matrix_entry_interval_radius": frac_json(k_interval_radius),
            "quadrature_additive_matrix_entry_bound": frac_json(quad_matrix_error),
            "target_matrix_spectral_error_bound": frac_json(spectral_error_k),
            "certified_minimum_eigenvalue": frac_json(spectral_lower),
            "cross_vector_entry_error_bound": frac_json(entry_error_c),
            "cross_row_operator_error_before_beta_scaling": frac_json(c_operator_error),
            "beta_entry_error_bound": frac_json(entry_error_beta),
            "final_cross_row_contribution": frac_json(f_error_cross),
            "final_inverse_perturbation_contribution": frac_json(f_error_inverse),
            "final_beta_contribution": frac_json(f_error_beta),
        },
    }


def run() -> dict:
    n = 12
    return certified_boundary_resolvent(
        p_input=[Fraction(1, 2) for _ in range(n)],
        rates_input=[Fraction(i + 3, 4) for i in range(n)],
        initial_input=[Fraction(i + 1, i + 3) for i in range(n)],
        targets_input=[0, (1 << n) - 1],
        s_input=Fraction(1, 1 << n),
        delta_bits=100,
        output_bits=48)


def main() -> None:
    result = run()
    out_path = Path(__file__).with_name("receipt.json")
    out_path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
