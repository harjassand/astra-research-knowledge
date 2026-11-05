#!/usr/bin/env python3
"""Regenerate the finite checks shipped with the noisy-interface construction.

No external papers, network, device or accepted predecessor re-audit is needed.
The checks support the algebra; the proof notes establish the asymptotic results.
"""
from pathlib import Path
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
SCRIPTS = [
    ("verify_precompensation.py", None),
    ("classical_tree_regenerator.py", None),
    ("passive_route/check_static_tree.py", "passive_route/static_tree_checks.json"),
    ("endpoint_route/check_interface_identities.py", "endpoint_route/interface_identity_checks.json"),
    ("verify_blackout_boundary.py", None),
]


def main():
    receipt = []
    for filename, captured_result in SCRIPTS:
        result = subprocess.run(
            [sys.executable, str(ROOT / filename)],
            cwd=ROOT, text=True, capture_output=True, check=False,
        )
        item = {"script": filename, "returncode": result.returncode}
        if result.returncode:
            sys.stderr.write(result.stdout + result.stderr)
            raise SystemExit(result.returncode)
        if captured_result is not None:
            parsed = json.loads(result.stdout)
            (ROOT / captured_result).write_text(json.dumps(parsed, indent=2) + "\n")
        receipt.append(item)
        print(filename + ": passed", flush=True)
    (ROOT / "finite_check_receipt.json").write_text(json.dumps({
        "scope": "Finite algebra, coupling and sampler checks; not a device simulation, family lifetime measurement or numerical hardware threshold.",
        "checks": receipt,
    }, indent=2) + "\n")


if __name__ == "__main__":
    main()
