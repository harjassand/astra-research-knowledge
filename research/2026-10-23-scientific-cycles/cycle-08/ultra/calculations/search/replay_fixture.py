#!/usr/bin/env python3
"""One fixed nontrivial admission and measured computation cost.

Runs the actual colored search control on commuting difference statistics of
one specified queue branch. It is not a Monte Carlo certification of epsilon.
The analytic probability theorem is in PROOF.txt; no parameter sweep occurs.
"""
from fractions import Fraction
from pathlib import Path
import argparse
import hashlib
import json
import time

from colored_search import DifferenceFixture, colored_search, parameters


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--outdir", type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    args.outdir.mkdir(parents=True, exist_ok=True)
    here = Path(__file__).resolve().parent
    fixture_input = {"L": 1048576, "K": 524288, "D": 2,
                     "epsilon": "1/64", "seed": 20261022}
    L, K, D = (fixture_input[key] for key in ("L", "K", "D"))
    epsilon = Fraction(fixture_input["epsilon"])
    T, s, Q = parameters(L, D, epsilon)
    source = DifferenceFixture(L, K, D, Q, fixture_input["seed"])
    wall_start, cpu_start = time.perf_counter(), time.process_time()
    result = colored_search(L, D, epsilon, source)
    wall, cpu = time.perf_counter() - wall_start, time.process_time() - cpu_start
    physical = [(j, color, yes) for j, color, yes in result.raw_transcript
                if 2 <= j <= L]
    nonempty_restricted_rows = sum(color + 1 <= min(j, result.cut)
                                  for j, color, _ in physical)
    allocated_bells = result.cut - nonempty_restricted_rows
    checks = {
        "nontrivial_retained_prefix": allocated_bells > 1,
        "safe_cut_on_this_fixture": result.cut <= K,
        "every_branch_cut_lower_bound": result.cut >= K - 2 * Q,
        "every_branch_allocation_lower_bound": allocated_bells >= max(1, K - 3 * Q),
        "fresh_color_budget": result.raw_calls <= Q,
        "total_support_bound": source.touched <= L - 1,
    }
    if not all(checks.values()):
        raise AssertionError(checks)
    output = {
        "status": "PASS",
        "scope": "one fixed conditional-inventory classical search-control admission; not statistical error certification or a full density-matrix replay",
        "inputs": fixture_input,
        "parameters": {"T": T, "s": s, "Q": Q},
        "observations": {
            "raw_calls_reserved": result.raw_calls,
            "physical_parity_calls": len(physical),
            "candidates": result.candidates,
            "certified_U": result.U,
            "cut_c": result.cut,
            "nonempty_disjoint_rows_after_cut": nonempty_restricted_rows,
            "allocated_Bell_pairs": allocated_bells,
            "difference_coordinates_touched": source.touched,
            "shared_random_seed_bits_in_receiver": 0,
            "auxiliary_entanglement": 0,
            "hidden_inventory_access": 0,
        },
        "checks": checks,
        "source_bindings": {name: digest(here / name)
                            for name in ("colored_search.py", "PROOF.txt", "replay_fixture.py")},
        "unavailable_totals": ["full discovery/inference computation", "physical energy", "hardware gate time"],
    }
    timing = {"wall_seconds": wall, "process_cpu_seconds": cpu,
              "measured_scope": "one colored search including used tail-difference generation and exact integer control",
              "fixture_parameter_search_runs": 0,
              "reported_replay_runs_in_this_invocation": 1}
    (args.outdir / "RESULT.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    (args.outdir / "TIMING.json").write_text(json.dumps(timing, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": "PASS", "checks": len(checks),
                      "allocated_Bell_pairs": allocated_bells,
                      "wall_seconds": wall, "process_cpu_seconds": cpu}, sort_keys=True))


if __name__ == "__main__":
    main()
