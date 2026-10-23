#!/usr/bin/env python3
"""Recompute the fixed benchmark from public code, config and random-bit tapes."""
import hashlib
import json
from pathlib import Path

from benchmark import execute

HERE = Path(__file__).resolve().parent


def main():
    files = {name: HERE / f"{name.upper()}_PUBLIC_TRANSCRIPT.json"
             for name in ("lead", "osstar", "fullgrid")}
    public = {name: json.loads(path.read_text()) for name, path in files.items()}
    tapes = {name: public[name]["bit_tape"] for name in public}
    run = execute({}, tapes)
    checks = {}
    for name, original in public.items():
        replayed = run["methods"][name]
        checks[name] = {
            "task_counts_match": replayed["task_counts"] == original["task_counts"],
            "outputs_match": replayed["outputs"] == original["outputs"],
            "events_match_exactly": replayed["events"] == original["events"],
            "bit_tape_consumed_exactly": replayed["bit_tape"] == original["bit_tape"],
        }
        if name == "fullgrid":
            checks[name]["paid_control_table_matches"] = (
                replayed["control_paid_grid_table"] == original["control_paid_grid_table"])
        if not all(checks[name].values()):
            raise AssertionError(f"public replay mismatch: {name}: {checks[name]}")
    transcript_hashes = {name: hashlib.sha256(path.read_bytes()).hexdigest()
                         for name, path in files.items()}
    out = {
        "status": "PASS",
        "scope": "deterministic recomputation from the visible benchmark code, transcript events, and consumed public bit tapes; does not certify PRNG fairness",
        "task_counts_lead_generated": run["task_counts_lead_generated"],
        "checks": checks,
        "transcript_sha256": transcript_hashes,
        "source_sha256": hashlib.sha256((HERE / "benchmark.py").read_bytes()).hexdigest(),
        "method_costs": {k: {"counters": v["counters"],
                              "rational_ledger": v["rational_ledger"],
                              "wall_seconds_including_exact_logic": v["wall_seconds_including_exact_logic"]}
                         for k, v in run["methods"].items()},
        "interpretation": [
            "Exact decisions replay conditional on the public bit tapes.",
            "Wall time is measured on this host and is not inferred from source-call counts.",
            "The task sequence is the one lead-generated adaptive stream; controls replay it and their outputs do not alter their counts.",
        ],
    }
    (HERE / "PUBLIC_REPLAY_VERIFICATION.json").write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({"status": out["status"], "checks": checks,
                      "task_counts": out["task_counts_lead_generated"]}, indent=2))


if __name__ == "__main__":
    main()
