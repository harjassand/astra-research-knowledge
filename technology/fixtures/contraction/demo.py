#!/usr/bin/env python3
"""Exposed synthetic bookkeeping example. No novel algorithm or hardware result."""
import argparse
from fractions import Fraction
import json
from pathlib import Path


def run():
    target = Fraction(1, 16)
    x = Fraction(1)
    steps = 0
    while x > target:
        x /= 2
        steps += 1
    return {"fixture": True, "kind": "exact_finite_software_diagnostic",
            "supplied_q": "1/2", "supplied_x0": "1", "target_error": str(target),
            "candidate": {"updates": steps, "error": str(x)},
            "equally_informed_stopping_control": {"updates": steps, "error": str(x)},
            "fixed_ten_step_reference": {"updates": 10, "error": str(Fraction(1, 1024))},
            "advantage_over_competent_control": False,
            "wall_time_energy_and_acquisition_cost": None,
            "physical_measurements": 0, "independent_reproduction": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = run()
    if args.check:
        expected = json.loads(Path(__file__).with_name("results.json").read_text())
        if expected != result:
            raise SystemExit("fixture output differs from recorded exact results")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
