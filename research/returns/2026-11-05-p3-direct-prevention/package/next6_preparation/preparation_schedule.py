#!/usr/bin/env python3
"""Evaluate a proved preparation schedule; this is not physical acquisition.

The sufficient implemented durations are exact rational arithmetic. The smooth
formula is reported only as an analytic comparison, never used for rounding.
"""
from fractions import Fraction
from pathlib import Path
import hashlib
import json
import math
import platform
import sys


def ceil_log2_rational(value):
    value = Fraction(value)
    if value <= 1:
        return 0
    exponent = max(0, value.numerator.bit_length() - value.denominator.bit_length())
    while Fraction(2 ** exponent) < value:
        exponent += 1
    while exponent and Fraction(2 ** (exponent - 1)) >= value:
        exponent -= 1
    return exponent


def frac_record(value):
    value = Fraction(value)
    return {
        "numerator": value.numerator,
        "denominator": value.denominator,
        "decimal": float(value),
    }


def main():
    out = Path(__file__).resolve().parent
    b = Fraction(1, 40)
    m = Fraction(1, 2)
    r_min = Fraction(1, 5)
    gamma = Fraction(7, 50)
    beta = Fraction(1, 100)
    eps = beta / 16
    clock_error = Fraction(1, 10)
    retry_failure = Fraction(1, 1000)
    c_ls = Fraction(4) / (b * m * m * r_min)
    # Conservative safe mass one half; perfect-inspection-only retry ledger.
    accept_floor = (1 - eps) / 2
    failure_one = 1 - accept_floor
    retries = 0
    while failure_one ** retries > retry_failure:
        retries += 1
    b0 = ceil_log2_rational(1 / b)
    b2 = ceil_log2_rational(8 / eps)
    rows = []
    for n in (64, 256, 1024, 4096):
        lam = n * math.log(float(1 / b))
        b1 = ceil_log2_rational(max(1, n * b0))
        t_rat = c_ls * b1 / 2 + Fraction(b2) / gamma
        actual_upper = t_rat + 2 * clock_error
        t_smooth = float(c_ls) * math.log(max(1, lam)) / 2
        t_smooth += math.log(math.e ** 2 / float(eps)) / float(gamma)
        t_gap_only = (n * math.log(float(1 / b)) + math.log(1 / float(eps))) / float(gamma)
        assert float(t_rat) >= t_smooth
        rows.append({
            "N": n,
            "Lambda_analytic": lam,
            "B0": b0,
            "B1": b1,
            "B2": b2,
            "T_mix_analytic": t_smooth,
            "T_rat_guaranteed_min_native_time": frac_record(t_rat),
            "requested_duration_with_clock_allowance": frac_record(t_rat + clock_error),
            "actual_duration_upper": frac_record(actual_upper),
            "summed_component_exposure_per_attempt_upper": frac_record(n * actual_upper),
            "perfect_inspection_retry_cap": retries,
            "perfect_inspection_total_relaxation_wall_upper": frac_record(retries * actual_upper),
            "perfect_inspection_total_summed_exposure_upper": frac_record(retries * n * actual_upper),
            "gap_only_sufficient_analytic_reference": t_gap_only,
        })
    report = {
        "kind": "analytic finite-schedule calculation, not physical or Monte Carlo execution",
        "conditions": {
            "b": frac_record(b),
            "spectral_influence_margin_m": frac_record(m),
            "r_min": frac_record(r_min),
            "physical_gap": frac_record(gamma),
            "C_LS": frac_record(c_ls),
            "target_log_density_beta": frac_record(beta),
            "raw_relative_density_error": frac_record(eps),
            "absolute_exogenous_clock_error": frac_record(clock_error),
            "perfect_inspection_acceptance_floor": frac_record(accept_floor),
            "retry_failure_budget": frac_record(retry_failure),
            "perfect_inspection_failure_at_cap": frac_record(failure_one ** retries),
        },
        "not_included": [
            "Coarse certificate acquisition is paid by the main acquired construction.",
            "Field installation, ramp and settling are separate.",
            "Finite physical inspection is separate; the retry row assumes perfect instantaneous inspection.",
            "Deployment and rejected-cell handling are separate.",
            "These schedules are sufficient, not optimal or universal lower bounds."
        ],
        "rows": rows,
    }
    result = out / "preparation_schedule.json"
    result.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    receipt = {
        "status": "completed",
        "interpreter": sys.version,
        "platform": platform.platform(),
        "script": Path(__file__).name,
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "output": result.name,
        "output_sha256": hashlib.sha256(result.read_bytes()).hexdigest(),
        "assertions": [
            "Exact rational time is at least the displayed smooth expression for each ledger row.",
            "Retry cap is the first integer meeting the exact rational perfect-inspection failure budget."
        ],
        "scope": "No physical acquisition or system trajectory was performed."
    }
    (out / "schedule_execution_receipt.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"C_LS": float(c_ls), "retry_cap": retries, "rows": [
        {"N": row["N"], "T_mix": row["T_mix_analytic"],
         "T_rat": row["T_rat_guaranteed_min_native_time"]["decimal"],
         "exposure_per_attempt": row["summed_component_exposure_per_attempt_upper"]["decimal"]}
        for row in rows]}, indent=2))


if __name__ == "__main__":
    main()
