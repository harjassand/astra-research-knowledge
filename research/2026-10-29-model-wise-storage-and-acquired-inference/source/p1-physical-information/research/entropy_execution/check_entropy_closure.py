#!/usr/bin/env python3
"""Exact rational controls for the native excursion entropy-closure example.

No sampling, floating-point certification, external packages, or dense matrices.
All logarithms and large Laplace transforms use outward rational intervals.
The source record K12=exp(-t), K21=t*exp(-t) is supplied analytically.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction as F
from functools import lru_cache
from hashlib import sha256
import json
from pathlib import Path
import sys


# All integers are generated from the bounded lambda list below. The optional
# lambda=128 preparation certificate exceeds Python's default decimal limit.
if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(100000)


WORK_BITS = 160
CERT_BITS = 128
LOG_TERMS = 64
SCALE = 1 << WORK_BITS
LAPLACE_POINTS = (F(1, 16), F(1, 4), F(1, 2), F(1), F(2), F(4), F(16))


def ceil_div(a: int, b: int) -> int:
    return -((-a) // b)


def floor_fixed(x: F) -> int:
    return (x.numerator * SCALE) // x.denominator


def ceil_fixed(x: F) -> int:
    return ceil_div(x.numerator * SCALE, x.denominator)


@dataclass(frozen=True)
class Interval:
    lo: F
    hi: F

    def __post_init__(self) -> None:
        assert self.lo <= self.hi

    def add(self, other: "Interval") -> "Interval":
        return Interval(self.lo + other.lo, self.hi + other.hi)

    def scale(self, c: F) -> "Interval":
        if c >= 0:
            return Interval(c * self.lo, c * self.hi)
        return Interval(c * self.hi, c * self.lo)

    def minus(self, c: F) -> "Interval":
        return Interval(self.lo - c, self.hi - c)

    def contains(self, x: F) -> bool:
        return self.lo <= x <= self.hi


ZERO = Interval(F(0), F(0))


def log_unit_interval(x: F) -> Interval:
    """Enclose log(x), 1 <= x <= 2, using the positive atanh series.

    Every retained term is rounded outward to a 160-bit dyadic. For
    z=(x-1)/(x+1), the omitted tail is at most
        2*z**(2*N+1)/((2*N+1)*(1-z*z)).
    All divisions here are exact integer divisions with stated directions.
    """
    assert F(1) <= x <= F(2)
    z = (x - 1) / (x + 1)
    if not z:
        return ZERO
    a, b = z.numerator, z.denominator
    aa, bb = a * a, b * b
    ap, bp = a, b
    lo = hi = 0
    for k in range(LOG_TERMS):
        numer = 2 * ap * SCALE
        denom = (2 * k + 1) * bp
        lo += numer // denom
        hi += ceil_div(numer, denom)
        ap *= aa
        bp *= bb
    tail_num = 2 * ap * bb * SCALE
    tail_den = (2 * LOG_TERMS + 1) * bp * (bb - aa)
    hi += ceil_div(tail_num, tail_den)
    return Interval(F(lo, SCALE), F(hi, SCALE))


LOG_TWO = log_unit_interval(F(2))


@lru_cache(maxsize=None)
def log_interval(x: F) -> Interval:
    assert x > 0
    y = x
    k = 0
    while y >= 2:
        y /= 2
        k += 1
    while y < 1:
        y *= 2
        k -= 1
    result = log_unit_interval(y).add(LOG_TWO.scale(F(k)))
    assert result.hi - result.lo < F(1, 1 << CERT_BITS)
    return result


def exact_json(x: F) -> dict[str, str]:
    return {"numerator": str(x.numerator), "denominator": str(x.denominator)}


def directed_decimal(x: F, places: int, upward: bool) -> str:
    unit = 10 ** places
    numer = x.numerator * unit
    scaled = ceil_div(numer, x.denominator) if upward else numer // x.denominator
    sign = "-" if scaled < 0 else ""
    scaled = abs(scaled)
    return f"{sign}{scaled // unit}.{scaled % unit:0{places}d}"


def interval_json(x: Interval, exact: bool = True) -> dict:
    result = {
        "lower_decimal": directed_decimal(x.lo, 18, False),
        "upper_decimal": directed_decimal(x.hi, 18, True),
        "width_lt_2_to_minus_120": x.hi - x.lo < F(1, 1 << 120),
    }
    if exact:
        result["lower_exact"] = exact_json(x.lo)
        result["upper_exact"] = exact_json(x.hi)
    return result


def rational_json(x: F) -> dict:
    return {
        **exact_json(x),
        "lower_decimal": directed_decimal(x, 18, False),
        "upper_decimal": directed_decimal(x, 18, True),
        "numerator_bits": abs(x.numerator).bit_length(),
        "denominator_bits": x.denominator.bit_length(),
    }


def bit_stats(values: list[F]) -> dict[str, int]:
    return {
        "count": len(values),
        "max_numerator_bits": max(abs(x.numerator).bit_length() for x in values),
        "max_denominator_bits": max(x.denominator.bit_length() for x in values),
    }


def polynomial_laplace_interval(coefficients: list[F], q: F) -> Interval:
    """Enclose sum_{n=1}^N coefficients[n-1]*q**n by outward Horner.

    Exact q and coefficients are first rounded outward; positivity makes
    interval multiplication monotone. Fixed-point arithmetic prevents the
    giant rational denominators of a literal high-degree exact transform.
    """
    assert 0 < q <= 1
    qlo, qhi = floor_fixed(q), ceil_fixed(q)
    lo = hi = 0
    for a in reversed(coefficients):
        lo = (qlo * (lo + floor_fixed(a))) // SCALE
        hi = ceil_div(qhi * (hi + ceil_fixed(a)), SCALE)
    result = Interval(F(lo, SCALE), F(hi, SCALE))
    assert result.hi - result.lo < F(1, 1 << CERT_BITS)
    return result


def polynomial_laplace_exact(coefficients: list[F], q: F) -> F:
    result = F(0)
    for a in reversed(coefficients):
        result = q * (a + result)
    return result


def geometric_transform_exact(A: list[F], B: list[F], p: F, r: F,
                              M: int, q: F) -> tuple[F, F]:
    """Independent closed finite geometric-sum formulas, small cases only."""
    z = r * q
    a = p * q * (1 - z ** M) / (1 - z) + r ** M * q ** (M + 1)
    b = (p * p * q * (1 - (M + 1) * z ** M + M * z ** (M + 1))
         / (1 - z) ** 2
         + r ** M * (1 + M * p) * q ** (M + 1))
    assert a == polynomial_laplace_exact(A, q)
    assert b == polynomial_laplace_exact(B, q)
    return a, b


def sparse_generator_check(A: list[F], B: list[F], rate: F,
                           energy: Interval) -> dict:
    """Build only a small sparse native generator and check exact equations."""
    edges: list[dict[int, F]] = [{}, {}]
    weights = [F(1), F(1)]
    theta = [0, 1]
    channels: list[tuple[list[int], F, F]] = []
    for n, (a, b) in enumerate(zip(A, B), 1):
        forward = list(range(len(edges), len(edges) + n))
        backward = list(range(len(edges) + n, len(edges) + 2 * n))
        edges.extend({} for _ in range(2 * n))
        weights.extend([a / rate] * n + [b / rate] * n)
        theta.extend([0] * (2 * n))
        for k in range(n):
            theta[forward[k]] = backward[n - 1 - k]
            theta[backward[n - 1 - k]] = forward[k]
        for start, path, end, flux, reverse_flux in (
            (0, forward, 1, a, b), (1, backward, 0, b, a)
        ):
            edges[start][path[0]] = flux
            for k, state in enumerate(path):
                edges[state][path[k + 1] if k + 1 < n else end] = rate
            channels.append(([start, *path, end], flux, reverse_flux))

    assert sum(weights, F(0)) == 5
    assert sum(weights[2:], F(0)) == 3
    assert all(theta[theta[x]] == x for x in range(len(theta)))
    exits = [sum(row.values(), F(0)) for row in edges]
    assert exits[0] == exits[1] == 1
    assert all(x == rate for x in exits[2:])
    stationarity = [F(0)] * len(edges)
    for x, row in enumerate(edges):
        stationarity[x] -= weights[x] * exits[x]
        for y, qxy in row.items():
            stationarity[y] += weights[x] * qxy
    assert all(x == 0 for x in stationarity)

    physical_energy = ZERO
    reversed_adjoint_energy = ZERO
    support_checks = 0
    for x, row in enumerate(edges):
        assert exits[x] == exits[theta[x]]
        reverse_exit = F(0)
        for y, qxy in row.items():
            partner = edges[theta[y]].get(theta[x], F(0))
            assert partner > 0
            rxy = weights[theta[y]] * partner / weights[theta[x]]
            reverse_exit += rxy
            flux = weights[x] * qxy
            physical_energy = physical_energy.add(log_interval(qxy / partner).scale(flux))
            reversed_adjoint_energy = reversed_adjoint_energy.add(log_interval(qxy / rxy).scale(flux))
            if x >= 2:
                assert qxy == rxy
            support_checks += 1
        assert reverse_exit == exits[x]

    # Exact channel products, stronger than numerical agreement of log sums.
    for path, flux, reverse_flux in channels:
        ratio = F(1)
        for x, y in zip(path[:-1], path[1:]):
            ratio *= edges[x][y] / edges[theta[y]][theta[x]]
        assert ratio == flux / reverse_flux
    assert max(physical_energy.lo, energy.lo) <= min(physical_energy.hi, energy.hi)
    assert max(reversed_adjoint_energy.lo, energy.lo) <= min(reversed_adjoint_energy.hi, energy.hi)

    native_transform_checks = 0
    for s in (F(1, 4), F(1), F(4)):
        q = rate / (rate + s)
        for dest in (0, 1):
            absorption = [F(int(x == dest)) for x in range(len(edges))]
            for x in range(len(edges) - 1, 1, -1):
                absorption[x] = sum((qxy * absorption[y] for y, qxy in edges[x].items()), F(0)) / (s + exits[x])
            for source in (0, 1):
                native = sum((weights[source] * qxy * absorption[y]
                              for y, qxy in edges[source].items()), F(0))
                expected = (polynomial_laplace_exact(A if source == 0 else B, q)
                            if dest != source else F(0))
                assert native == expected
                native_transform_checks += 1

    return {
        "status": "PASS",
        "states": len(edges),
        "hidden_states": len(edges) - 2,
        "off_diagonal_edges": support_checks,
        "exact_stationarity_equations": len(edges),
        "exact_channel_reversal_product_checks": len(channels),
        "exact_native_laplace_checks": native_transform_checks,
        "physical_rate_interval": interval_json(physical_energy, exact=False),
        "parity_adjoint_rate_interval": interval_json(reversed_adjoint_energy, exact=False),
    }


def one_case(lam: int, build_sparse: bool) -> dict:
    assert lam >= 2 and lam & (lam - 1) == 0
    log2_lam = lam.bit_length() - 1
    M = lam * (log2_lam + 4)
    N = M + 1
    p, r = F(1, lam), F(lam - 1, lam)
    A: list[F] = []
    B: list[F] = []
    a = p
    for n in range(1, M + 1):
        A.append(a)
        B.append(n * p * a)
        assert A[-1] / B[-1] == F(lam, n)
        a *= r
    tail = r ** M
    A.append(tail)
    B.append(tail * (1 + M * p))
    assert A[-1] / B[-1] == F(lam, lam + M)
    assert sum(A, F(0)) == sum(B, F(0)) == 1

    phase_count = sum((n * (a + b) for n, (a, b) in enumerate(zip(A, B), 1)), F(0))
    m0 = phase_count / lam
    lost_first_moment = r ** (M + 1) * (M * p + 3)
    assert m0 == 3 - p - lost_first_moment
    dilation = F(3) / m0
    rate = F(lam) / dilation
    assert dilation > 1
    assert phase_count / rate == 3

    energy = ZERO
    preparation = ZERO
    for n, (a, b) in enumerate(zip(A, B), 1):
        contribution = log_interval(a / b).scale(a - b)
        assert contribution.lo >= 0
        energy = energy.add(contribution)
        preparation = preparation.add(contribution.scale(F(n, 5) / rate))
    assert energy.lo > 0
    assert energy.hi - energy.lo < F(1, 1 << 120)
    assert preparation.hi - preparation.lo < F(1, 1 << 120)

    transforms = []
    exact_formula_checks = 0
    max_grid_error_upper = F(0)
    for s in LAPLACE_POINTS:
        q = rate / (rate + s)
        ia = polynomial_laplace_interval(A, q)
        ib = polynomial_laplace_interval(B, q)
        ta, tb = F(1) / (1 + s), F(1) / (1 + s) ** 2
        ea, eb = ia.minus(ta), ib.minus(tb)
        max_grid_error_upper = max(max_grid_error_upper, abs(ea.lo), abs(ea.hi), abs(eb.lo), abs(eb.hi))
        if lam <= 4:
            xa, xb = geometric_transform_exact(A, B, p, r, M, q)
            assert ia.contains(xa) and ib.contains(xb)
            exact_formula_checks += 2
        transforms.append({
            "s": exact_json(s),
            "K12": interval_json(ia),
            "K21": interval_json(ib),
            "target_K12": exact_json(ta),
            "target_K21": exact_json(tb),
            "K12_error": interval_json(ea),
            "K21_error": interval_json(eb),
        })

    # A fully rational weighted-L1 upper bound, proved in the companion note.
    tail_mass = tail * (2 + M * p)
    collapse_bound = 2 * tail_mass * (1 + F(N, lam)) + lost_first_moment
    weighted_l1_bound = dilation * collapse_bound + (6 - 2 * p) * (dilation - 1) + 2 * p

    digest = sha256()
    for n, (a, b) in enumerate(zip(A, B), 1):
        digest.update(f"{n}:{a.numerator}/{a.denominator}:{b.numerator}/{b.denominator}\n".encode())
    phase_weights = [x / rate for x in A + B]
    native_jumps = phase_count / 2 + 1
    result = {
        "status": "PASS",
        "lambda": lam,
        "M": M,
        "maximum_channel_phases": N,
        "hidden_states": N * (N + 1),
        "total_states": N * (N + 1) + 2,
        "directed_channels": 2 * N,
        "off_diagonal_edges": N * (N + 3),
        "endpoint_flux_each_direction_unnormalized": 1,
        "port_weight_each": 1,
        "native_port_departure_rate_each": 1,
        "hidden_mass_exact": 3,
        "total_stationary_weight_exact": 5,
        "mean_native_cycle_duration_exact": exact_json(F(5, 2)),
        "kernel_at_zero_K12": rational_json(rate * A[0]),
        "kernel_at_zero_K21": rational_json(rate * B[0]),
        "ratio_of_kernels_at_zero_exact": lam,
        "pre_dilation_hidden_mass": rational_json(m0),
        "common_dilation": rational_json(dilation),
        "common_phase_rate": rational_json(rate),
        "expected_micro_jumps_per_native_departure": rational_json(native_jumps),
        "expected_micro_jump_rate_per_physical_time": rational_json(2 * native_jumps / 5),
        "entropy_E": interval_json(energy),
        "normalized_intrinsic_rate_E_over_5": interval_json(energy.scale(F(1, 5))),
        "entropy_gap_1_minus_E": interval_json(energy.scale(F(-1)).add(Interval(F(1), F(1)))),
        "stationary_parity_preparation_KL": interval_json(preparation),
        "weighted_L1_record_error_upper_bound": rational_json(weighted_l1_bound),
        "weighted_L1_tail_collapse_bound_before_dilation": rational_json(collapse_bound),
        "max_absolute_error_on_laplace_grid_upper_bound": rational_json(max_grid_error_upper),
        "coefficient_precision": {
            "entry_flux_coefficients": bit_stats(A + B),
            "hidden_stationary_weights": bit_stats(phase_weights),
            "normalized_hidden_probabilities": bit_stats([x / 5 for x in phase_weights]),
            "smallest_entry_coefficient": rational_json(min(A + B)),
            "largest_entry_coefficient": rational_json(max(A + B)),
            "coefficient_manifest_sha256": digest.hexdigest(),
            "interpretation": "Exact integer storage of this representation; not a necessary instrument-precision bound or a claim of finite-data acquisition."
        },
        "laplace_grid": transforms,
        "small_case_exact_closed_formula_checks": exact_formula_checks,
    }
    if build_sparse:
        result["sparse_native_generator"] = sparse_generator_check(A, B, rate, energy)
    else:
        result["sparse_native_generator"] = {
            "status": "NOT_BUILT",
            "reason": "Matrix-free channel identities suffice; no dense or large sparse matrix allocated."
        }
    return result


def display_mid(x: dict) -> str:
    # For compact table display only, rounded to nearest 10 decimal places.
    # The JSON retains the exact directed certificate endpoints.
    if "numerator" in x:
        value = F(int(x["numerator"]), int(x["denominator"]))
    else:
        lo, hi = x["lower_exact"], x["upper_exact"]
        value = (F(int(lo["numerator"]), int(lo["denominator"]))
                 + F(int(hi["numerator"]), int(hi["denominator"]))) / 2
    return directed_decimal(value + F(1, 2 * 10 ** 10), 10, False)


def display_upper(x: dict) -> str:
    return directed_decimal(F(int(x["numerator"]), int(x["denominator"])), 10, True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--include-128", action="store_true")
    parser.add_argument("--out", type=Path, default=Path(__file__).with_name("ENTROPY_CLOSURE_CHECKS.json"))
    args = parser.parse_args()
    lambdas = [2, 4, 8, 16, 32, 64] + ([128] if args.include_128 else [])
    cases = []
    for lam in lambdas:
        case = one_case(lam, build_sparse=lam <= 4)
        cases.append(case)
        print(f"lambda={lam}: PASS; hidden={case['hidden_states']}; "
              f"E in [{case['entropy_E']['lower_decimal']}, "
              f"{case['entropy_E']['upper_decimal']}]")
    result = {
        "status": "PASS",
        "date_utc": "2026-10-29",
        "construction_owner": "Astra root",
        "implementation_agent": "producer-workspace/controlled_realization_frontier",
        "source_record": {"K12": "exp(-t)", "K21": "t*exp(-t)", "J_exact": 1,
                          "V_exact": 3, "W_exact": 5, "normalized_closure_floor_exact": "1/5"},
        "arithmetic": {"type": "Exact rational coefficients with outward integer/dyadic transcendental bounds",
                       "working_fraction_bits": WORK_BITS, "individual_log_certificate_bits": CERT_BITS,
                       "atanh_terms": LOG_TERMS, "log_formula": "log(x)=k*log(2)+2*atanh((y-1)/(y+1)), x=2^k*y, 1<=y<2",
                       "full_energy_interval_width_lt_2_to_minus_120": True,
                       "large_laplace_method": "Outward rational Horner; no enormous literal high-degree denominator or floating-point decision"},
        "limits_proved_in_note": {"E": "1", "E_over_W": "1/5", "phase_rate_over_lambda": "1",
                                  "expected_micro_jumps_per_departure_over_lambda": "3/2",
                                  "stationary_parity_preparation_KL": "(2-EulerGamma)/5",
                                  "weighted_L1_record_error": "0"},
        "acquisition": {"source": "Analytically supplied record", "random_draws": 0,
                        "physical_observations": 0, "equipment_operations": 0,
                        "sample_advantage_claim": False},
        "script_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "cases": cases,
    }
    args.out.write_text(json.dumps(result, indent=2) + "\n")
    table = [
        "# Exact rational entropy-closure control table", "",
        "Rates, entropies and jump counts are rounded display values; the weighted-L1 bound is rounded upward. The JSON contains exact rational certificate endpoints.", "",
        "| lambda | Hidden states | Phase rate (approx.) | E (approx.) | E/5 (approx.) | Preparation KL (approx.) | Micro jumps/departure (approx.) | Weighted-L1 upper bound | Entry denominator bits |",
        "|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for c in cases:
        table.append(f"| {c['lambda']} | {c['hidden_states']:,} | "
                     f"{display_mid(c['common_phase_rate'])} | {display_mid(c['entropy_E'])} | "
                     f"{display_mid(c['normalized_intrinsic_rate_E_over_5'])} | "
                     f"{display_mid(c['stationary_parity_preparation_KL'])} | "
                     f"{display_mid(c['expected_micro_jumps_per_native_departure'])} | "
                     f"{display_upper(c['weighted_L1_record_error_upper_bound'])} | "
                     f"{c['coefficient_precision']['entry_flux_coefficients']['max_denominator_bits']} |")
    table += ["", "This supplied analytic task has direct observable entropy J=1. The family demonstrates the completion and its execution costs; it does not beat direct evaluation of J.", ""]
    args.out.with_name("ENTROPY_CLOSURE_TABLE.md").write_text("\n".join(table))
    print(f"Saved {args.out.name}; all {len(cases)} cases passed.")


if __name__ == "__main__":
    main()
