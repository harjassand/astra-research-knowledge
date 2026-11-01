"""Preserve the independent matrix-exponential audit method and its provenance.

IMPORTANT: This is a reconstruction of the independent calculation, NOT the
original executed script. The historical audit was executed inline and only
ROOT_CONSTRUCTION_AUDIT.json was retained. That record reports 300 cases and a
maximum absolute error of 9.575673587391975e-15. It does not retain the random
seed, parameter sampler, or individual cases. These cannot be honestly recovered
from the aggregate result. This file was saved without executing further tests.

The independently constructed four-state continuous-time generator is preserved
below. Its state order is B (bound, unhydrolyzed), H (hydrolyzed, still bound),
V (valid escape), I (bypass escape): B--h-->H--e-->V; B--b-->I.

No new random sampler or seed is substituted for the missing historical one.
If the original cases are recovered, pass a JSON list of {t,h,e,bypass} records:

    python3 stage2_existing/audit_completion_math.py --cases ORIGINAL_CASES.json

With no arguments, only the provenance record is printed; no tests are run.
All parameter cases are dimensionless algebra checks, not physical predictions.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
from typing import Iterable, Mapping


HERE = Path(__file__).resolve().parent
ORIGINAL_RANDOM_SEED = None  # Not retained; do not infer or replace.
ORIGINAL_CASE_GENERATOR = None  # Not retained.
ORIGINAL_CASE_COUNT = 300
HISTORICAL_MAXIMUM_ABSOLUTE_ERROR = 9.575673587391975e-15


def four_state_generator(h: float, e: float, bypass: float):
    """Return row-convention CTMC generator, independently of the closed form."""
    import numpy as np

    if min(h, e, bypass) < 0:
        raise ValueError("Rates must be nonnegative")
    return np.array(
        [
            [-(h + bypass), h, 0.0, bypass],
            [0.0, -e, e, 0.0],
            [0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0],
        ],
        dtype=float,
    )


def matrix_exponential_probabilities(t: float, h: float, e: float, bypass: float):
    """Initial state is B; first row of exp(Q*t) gives the four probabilities."""
    from scipy.linalg import expm

    if t < 0:
        raise ValueError("Time must be nonnegative")
    return expm(four_state_generator(h, e, bypass) * t)[0]


def load_closed_form():
    source = HERE.parent / "stage2_root" / "completion_exit.py"
    spec = importlib.util.spec_from_file_location("completion_exit_under_audit", source)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load {source}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.competed_exit


def audit_explicit_cases(cases: Iterable[Mapping[str, float]]) -> dict:
    """Equivalent independent method; does not recreate missing historical cases.

    This function has not been executed as part of preserving this file. It is
    provided for the original case list, if that list is later recovered.
    """
    import numpy as np

    closed_form = load_closed_form()
    keys = ("bound", "hydrolyzed_bound", "valid", "invalid")
    errors = []
    for case in cases:
        t, h, e, bypass = (float(case[k]) for k in ("t", "h", "e", "bypass"))
        independent = matrix_exponential_probabilities(t, h, e, bypass)
        calculated = closed_form(t, h, e, bypass)
        errors.append(float(np.max(np.abs(independent - [calculated[k] for k in keys]))))
    if not errors:
        raise ValueError("Supply an explicit nonempty case list")
    return {
        "status": "new execution on supplied explicit cases, not historical replay",
        "case_count": len(errors),
        "maximum_absolute_error": max(errors),
        "parameter_status": "dimensionless algebra cases, not measured kinetics",
    }


def provenance() -> dict:
    return {
        "status": "historical result retained; exact sampler and seed not retained",
        "historical_result_file": str(HERE / "ROOT_CONSTRUCTION_AUDIT.json"),
        "historical_case_count": ORIGINAL_CASE_COUNT,
        "historical_maximum_absolute_error": HISTORICAL_MAXIMUM_ABSOLUTE_ERROR,
        "original_random_seed": ORIGINAL_RANDOM_SEED,
        "original_case_generator": ORIGINAL_CASE_GENERATOR,
        "script_status": "reconstructed independent method; not executed for this preservation",
        "reproducibility_limit": "Cannot exactly reproduce the historical 300-case draw without original cases or sampler and seed",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cases", type=Path, help="Explicit original case-list JSON, if recovered")
    args = parser.parse_args()
    result = provenance()
    if args.cases is not None:
        result["explicit_case_execution"] = audit_explicit_cases(
            json.loads(args.cases.read_text())
        )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
