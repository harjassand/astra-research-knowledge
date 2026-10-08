#!/usr/bin/env python3
"""Small synthetic checks for the JUN conditional-count likelihood."""

from __future__ import annotations

import importlib.util
import math
from pathlib import Path


HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("jun_count_model", HERE / "jun_count_model.py")
JUN = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(JUN)


def pair_row(input_count, output_count):
    row = {}
    for r in range(1, 7):
        row[f"count_e{r}_s0"] = str(input_count)
        row[f"count_e{r}_s1"] = str(output_count)
    return row


def wt_row(input_count, output_count):
    return pair_row(input_count, output_count)


def main():
    # Equal matched input counts and 2:1 outputs give the exact conditional
    # binomial MLE log(2), which the two-sided profile interval must contain.
    variant = pair_row(1000, 2000)
    wildtype = wt_row(1000, 1000)
    fit = JUN.fit_profile(variant, wildtype)
    assert fit is not None and fit["n_reps"] == 6
    assert abs(fit["estimate"] - math.log(2.0)) < 1e-9, fit
    assert fit["lower95"] < math.log(2.0) < fit["upper95"], fit

    # Zero mutant outputs are retained as data: they produce a one-sided
    # likelihood bound instead of a pseudocount estimate or an empty result.
    zero_variant = pair_row(1000, 0)
    zero_fit = JUN.fit_profile(zero_variant, wildtype)
    assert zero_fit is not None and zero_fit["n_reps"] == 6
    assert zero_fit["estimate"] == -math.inf
    assert zero_fit["lower95"] == -math.inf
    assert math.isfinite(zero_fit["upper95"]) and zero_fit["upper95"] < 0.0

    # An input-zero replicate has no defined offset and is excluded only for
    # that replicate; the remaining five observations still estimate delta.
    missing = pair_row(0, 2000)
    for r in range(2, 7):
        missing[f"count_e{r}_s0"] = "1000"
        missing[f"count_e{r}_s1"] = "2000"
    missing_wt = wt_row(1000, 1000)
    omitted = JUN.fit_profile(missing, missing_wt)
    assert omitted is not None and omitted["n_reps"] == 5
    assert abs(omitted["estimate"] - math.log(2.0)) < 1e-9, omitted
    print("PASS: exact log-odds MLE, zero-output one-sided bound, input-zero omission")


if __name__ == "__main__":
    main()
