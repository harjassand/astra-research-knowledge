#!/usr/bin/env python3
"""Run the exact scientific checks sequentially; no external dependencies."""
from pathlib import Path
import json
import platform
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
STAGES = [
    ("parity_acquisition.py", "acquisition.json", False),
    ("parity_inference.py", "conditional_inference.json", False),
    ("graphic_acquisition.py", "graphic.json", False),
    ("discover_chain.py", "discovered_chain.json", True),
    ("learn_planar.py", "learned_planar.json", True),
    ("physical_queries.py", "physical_queries.json", True),
    ("audit_discover_chain.py", "chain_audit.json", True),
    ("signed_parity_audit.py", "signed_parity_audit.json", False),
    ("lpn_interface_check.py", "lpn_interface.json", False),
]


def main():
    start = time.perf_counter()
    reports = []
    (ROOT / "results").mkdir(exist_ok=True)
    for script, receipt, owns_receipt in STAGES:
        t0 = time.perf_counter()
        result = subprocess.run([sys.executable, str(ROOT / "experiments" / script)],
                                cwd=ROOT, text=True, capture_output=True)
        if result.returncode:
            print(result.stdout)
            print(result.stderr, file=sys.stderr)
            raise SystemExit(result.returncode)
        parsed = json.loads(result.stdout)
        path = ROOT / "results" / receipt
        if not owns_receipt:
            path.write_text(json.dumps(parsed, indent=2) + "\n")
        json.loads(path.read_text())
        reports.append({"script": script, "receipt": receipt,
                        "seconds": time.perf_counter() - t0, "passed": True})
        print(json.dumps(reports[-1]), flush=True)
    report = {"python": platform.python_version(), "stages": reports,
              "all_passed": True, "total_seconds": time.perf_counter() - start,
              "dependencies": "Python standard library only",
              "scope": "Exact finite checks supplement the written proofs; timings are single-run local measurements."}
    (ROOT / "results" / "reproduction.json").write_text(json.dumps(report, indent=2) + "\n")


if __name__ == "__main__":
    main()
