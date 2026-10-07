"""Exact finite-table compiler for the phase-two covariance-channel theorem.

Only the sufficient conditional-entropy criterion is optimized. Gaussian
output sampling is idealized and deliberately not implemented as floats.
Run in this owned directory; writes only the explicitly selected own output.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
import json
import math
import time


def fs(x: F) -> str:
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


@lru_cache(maxsize=None)
def atanh_interval(t: F, terms: int) -> tuple[F, F]:
    assert 0 <= t <= F(1, 3)
    total, power = F(0), t
    for i in range(terms):
        total += 2 * power / (2 * i + 1)
        power *= t * t
    tail = 2 * power / ((2 * terms + 1) * (1 - t * t))
    return total, total + tail


@lru_cache(maxsize=None)
def log_interval(x: F, bits: int) -> tuple[F, F]:
    assert x > 0 and bits >= 8
    if x == 1:
        return F(0), F(0)
    exponent = x.numerator.bit_length() - x.denominator.bit_length()
    z = x / (1 << exponent) if exponent >= 0 else x * (1 << -exponent)
    while z < 1:
        z *= 2
        exponent -= 1
    while z >= 2:
        z /= 2
        exponent += 1
    terms = bits + abs(exponent).bit_length() + 4
    lo, hi = atanh_interval((z - 1) / (z + 1), terms)
    l2, u2 = atanh_interval(F(1, 3), terms)
    if exponent >= 0:
        lo, hi = lo + exponent * l2, hi + exponent * u2
    else:
        lo, hi = lo + exponent * u2, hi + exponent * l2
    assert 0 <= hi - lo <= F(1, 1 << bits)
    return lo, hi


@lru_cache(maxsize=None)
def phi_interval(a: F, bits: int) -> tuple[F, F]:
    assert a >= 0
    if a == 0:
        return F(0), F(0)
    lo, hi = log_interval(a, bits)
    return a * lo, a * hi


def cell_cost(rows: list[dict], indices: tuple[int, ...], bits: int) -> tuple[F, F, F, F]:
    mass = sum((rows[i]["p"] for i in indices), F(0))
    mean = sum((rows[i]["p"] * rows[i]["a"] for i in indices), F(0)) / mass
    if all(rows[i]["a"] == mean for i in indices):
        return F(0), F(0), mass, mean
    low, high = F(0), F(0)
    for i in indices:
        l, u = phi_interval(rows[i]["a"], bits)
        low += rows[i]["p"] * l
        high += rows[i]["p"] * u
    l, u = phi_interval(mean, bits)
    low, high = max(F(0), low - mass * u), high - mass * l
    assert high >= low
    return low, high, mass, mean


def compile_table(raw: dict, bits: int = 48) -> dict:
    rows = [{"id": x["id"], "p": F(x["p"]), "a": F(x["a"])} for x in raw["rows"]]
    assert rows and all(r["p"] > 0 and r["a"] >= 0 for r in rows)
    assert sum((r["p"] for r in rows), F(0)) == 1
    assert len({r["id"] for r in rows}) == len(rows)
    rows.sort(key=lambda r: (r["a"], r["id"]))
    C, eps, L = F(raw["domination_C"]), F(raw["epsilon"]), F(raw["cap_L"])
    t0, t1, k = F(raw["T0"]), F(raw["T1"]), int(raw["outputs_k"])
    assert C >= 1 and 0 < eps <= 1 and L > 0 and 0 < t0 < t1 and k >= 1
    W = 1 / t0 - 1 / t1
    threshold = 4 * W * eps * eps / (k * C)
    n = len(rows)
    cells = {(l, r): cell_cost(rows, tuple(range(l, r)), bits)
             for l in range(n) for r in range(l + 1, n + 1)}
    low, up = [[None] * (n + 1) for _ in range(n + 1)], [[None] * (n + 1) for _ in range(n + 1)]
    parents = [[None] * (n + 1) for _ in range(n + 1)]
    low[0][0] = up[0][0] = F(0)
    for d in range(1, n + 1):
        for r in range(d, n + 1):
            for l in range(d - 1, r):
                if low[d - 1][l] is None:
                    continue
                lower = low[d - 1][l] + cells[l, r][0]
                upper = up[d - 1][l] + cells[l, r][1]
                if low[d][r] is None or lower < low[d][r]:
                    low[d][r] = lower
                if up[d][r] is None or upper < up[d][r]:
                    up[d][r], parents[d][r] = upper, l
    chosen = next(d for d in range(1, n + 1) if up[d][n] <= threshold)
    partition, end = [], n
    for d in range(chosen, 0, -1):
        start = parents[d][end]
        partition.append((start, end))
        end = start
    partition.reverse()
    codebook, encoder_map = [], {}
    actual_low, actual_high = F(0), F(0)
    for j, (l, r) in enumerate(partition):
        lower, upper, mass, mean = cells[l, r]
        actual_low += lower
        actual_high += upper
        ids = [rows[i]["id"] for i in range(l, r)]
        encoder_map.update({x: j for x in ids})
        codebook.append({"label": j, "input_ids": ids, "reference_mass": fs(mass),
                         "reference_covariance_mean": fs(mean),
                         "entropy_cost": {"lower": fs(lower), "upper": fs(upper)}})
    tv_squared = k * C * actual_high / (4 * W)
    assert tv_squared <= eps * eps
    minimal = all(low[d][n] > threshold for d in range(1, chosen))
    return {
        "status": "CERTIFIED_FOR_SUPPLIED_FINITE_TABLE_AND_DOMINATION",
        "retained_dimension": chosen,
        "fixed_binary_bits": (chosen - 1).bit_length(),
        "minimum_D_for_sufficient_entropy_criterion": chosen if minimal else "UNKNOWN",
        "precision_bits": bits,
        "input_rows": n,
        "C": fs(C), "k": k, "L": fs(L), "T0": fs(t0), "T1": fs(t1), "W": fs(W),
        "epsilon": fs(eps), "entropy_threshold": fs(threshold),
        "entropy_selected_interval": {"lower": fs(actual_low), "upper": fs(actual_high)},
        "TV_squared_upper": fs(tv_squared),
        "encoder_map": encoder_map, "codebook": codebook,
        "all_D_criterion_optimum_intervals": [
            {"D": d, "lower": fs(low[d][n]), "upper": fs(up[d][n])} for d in range(1, n + 1)
        ],
        "sampler_status": "IDEAL_GAUSSIAN_DECODER_SPECIFIED; FINITE_BIT_OUTPUT_NOT_IMPLEMENTED",
        "global_optimal_archive_dimension": "UNKNOWN",
    }


def decoder_variance(code: dict, label: int, T: F) -> F:
    assert T > 0 and 0 <= label < code["retained_dimension"]
    mean, L = F(code["codebook"][label]["reference_covariance_mean"]), F(code["L"])
    s = T * mean
    return 1 + s / (1 + s / L)


def partitions(n: int):
    """All unlabeled set partitions for a tiny independent finite optimum audit."""
    blocks: list[list[int]] = []
    def rec(i: int):
        if i == n:
            yield tuple(tuple(b) for b in blocks)
            return
        for b in blocks:
            b.append(i)
            yield from rec(i + 1)
            b.pop()
        blocks.append([i])
        yield from rec(i + 1)
        blocks.pop()
    yield from rec(0)


def audit_finite_optima(raw: dict, code: dict, bits: int) -> dict:
    rows = [{"id": x["id"], "p": F(x["p"]), "a": F(x["a"])} for x in raw["rows"]]
    rows.sort(key=lambda r: (r["a"], r["id"]))
    n = len(rows)
    assert n <= 8
    best_low, best_high, count = {}, {}, 0
    for part in partitions(n):
        count += 1
        values = [cell_cost(rows, b, bits) for b in part]
        low = sum((c[0] for c in values), F(0))
        high = sum((c[1] for c in values), F(0))
        d = len(part)
        best_low[d] = min(best_low.get(d, low), low)
        best_high[d] = min(best_high.get(d, high), high)
    tolerance = F(1, 1 << (bits - 8))
    for item in code["all_D_criterion_optimum_intervals"]:
        d = item["D"]
        assert F(item["lower"]) <= best_high[d] and best_low[d] <= F(item["upper"])
        assert F(item["upper"]) - best_low[d] <= tolerance
    return {"all_set_partitions_checked": count, "scope": "FINITE_ALGEBRA_OPTIMUM_AUDIT",
            "consecutive_DP_matches_global_interval_optima": True}


def gaussian_kl_envelope_diagnostic(raw: dict, code: dict) -> dict:
    """Floating check of the analytic KL integral, not a theorem or MI estimate."""
    rows = {r["id"]: (float(F(r["p"])), float(F(r["a"]))) for r in raw["rows"]}
    L = float(F(raw["cap_L"]))
    def c(a, t):
        s = t * a
        return 1 + s / (1 + s / L)
    def f(u):
        T = math.exp(u)
        kl = 0.0
        for item in code["codebook"]:
            cm = c(float(F(item["reference_covariance_mean"])), T)
            for name in item["input_ids"]:
                p, a = rows[name]
                ratio = c(a, T) / cm
                kl += p * 0.5 * (ratio - 1 - math.log(ratio))
        return kl * math.exp(-u)
    steps, left, right = 4000, -20.0, 20.0
    h = (right - left) / steps
    integral = h / 3 * (f(left) + f(right) + sum((4 if i % 2 else 2) * f(left + i * h) for i in range(1, steps)))
    upper = float(F(code["entropy_selected_interval"]["upper"])) / 2
    assert integral >= -1e-9 and integral <= upper + 1e-7
    return {"status": "DIAGNOSTIC_ONLY", "quadrature_log_T": [left, right], "steps": steps,
            "conditional_KL_integral_approx": integral, "analytic_H_J_over_2": upper,
            "actual_mutual_information_evaluated": False}


def fixture() -> dict:
    return {"rows": [
        {"id": "zero", "p": "2/5", "a": "0"},
        {"id": "tiny", "p": "1/5", "a": "1/64"},
        {"id": "small", "p": "1/10", "a": "1/16"},
        {"id": "quarter", "p": "1/10", "a": "1/4"},
        {"id": "one", "p": "1/10", "a": "1"},
        {"id": "four", "p": "1/20", "a": "4"},
        {"id": "sixteen", "p": "1/20", "a": "16"}],
        "domination_C": "2", "epsilon": "1/4", "cap_L": "8", "T0": "1", "T1": "2", "outputs_k": 1}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path)
    parser.add_argument("--output", type=Path, default=Path(__file__).with_name("covariance_codec_certificate.json"))
    parser.add_argument("--bits", type=int, default=48)
    args = parser.parse_args()
    own_root = Path(__file__).resolve().parent
    target = args.output.resolve()
    assert target.is_relative_to(own_root), "Output must stay in this owned revisions directory"
    assert not target.exists(), "Preserve existing certificates; choose a new output path"
    raw = json.loads(args.input.read_text()) if args.input else fixture()
    started = time.perf_counter()
    code = compile_table(raw, args.bits)
    checks = {"exact_finite_optimum": audit_finite_optima(raw, code, args.bits) if len(raw["rows"]) <= 8 else "NOT_RUN",
              "KL_integral_diagnostic": gaussian_kl_envelope_diagnostic(raw, code)}
    variance_samples = [{"label": j, "T": "3/2", "variance_exact": fs(decoder_variance(code, j, F(3, 2)))}
                        for j in range(code["retained_dimension"])]
    record = {"input": raw, "certificate": code, "checks": checks, "decoder_covariance_samples": variance_samples,
              "local_seconds": time.perf_counter() - started, "backend_energy_tokens": "UNKNOWN"}
    target.write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps({"output": str(target), "D": code["retained_dimension"], "binary_bits": code["fixed_binary_bits"],
                      "minimum_D_criterion": code["minimum_D_for_sufficient_entropy_criterion"],
                      "epsilon": code["epsilon"], "TV_upper_approx": math.sqrt(float(F(code["TV_squared_upper"]))),
                      "entropy_upper_approx": float(F(code["entropy_selected_interval"]["upper"])),
                      "checks": checks, "local_seconds": record["local_seconds"]}, indent=2))


if __name__ == "__main__":
    main()
