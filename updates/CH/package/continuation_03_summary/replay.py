#!/usr/bin/env python3
"""Portable scoped diagnostics; not full mathematical proof validation."""
from pathlib import Path
import importlib.metadata
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
receipt = {
    "scope": "Finite diagnostics, two interval countertests, isolated conditional Lean lemma",
    "excludes": "Complete proof verification, historical priority, external validation, all searches",
    "python": sys.version,
    "dependencies": {name: importlib.metadata.version(name) for name in ("numpy", "mpmath")},
    "checks": [],
}
env = dict(os.environ, OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1", PYTHONDONTWRITEBYTECODE="1")
with tempfile.TemporaryDirectory(prefix="astra-continuation-replay-") as temp:
    root = Path(temp)
    reports = root / "work/continuation_03/reports"
    shutil.copytree(HERE / "reports", reports)
    jobs = [
        ("physical_channel_controls", [sys.executable, str(reports / "e5_realization.py"), "controls"]),
        ("conditional_amplifier_counterexample", [sys.executable, str(reports / "support/e6_conditional_amplifier_gaussian.py")]),
        ("complete_relative_entropy_counterexample", [sys.executable, str(reports / "e4_zero_support/interval_reference_certificate.py")]),
        ("dark_vector_floating_coefficient_diagnostic", [sys.executable, str(reports / "support/e3_support_dark_vector.py")]),
    ]
    lean = shutil.which("lean")
    if lean:
        jobs.append(("conditional_scalar_lean_lemma", [lean, str(reports / "e8_formal/CreationMetricTransfer.lean")]))
    else:
        receipt["checks"].append({"name": "conditional_scalar_lean_lemma", "status": "SKIPPED", "reason": "lean executable unavailable"})
    for name, cmd in jobs:
        result = subprocess.run(cmd, cwd=root, env=env, text=True, capture_output=True, timeout=300)
        entry = {"name": name, "status": "PASS" if result.returncode == 0 else "FAIL", "returncode": result.returncode, "stdout": result.stdout, "stderr": result.stderr}
        if name == "dark_vector_floating_coefficient_diagnostic":
            entry["scope_note"] = "Diagnostic executed; numerical residuals require interpretation, not a proof assertion."
        receipt["checks"].append(entry)
        print(name + ": " + entry["status"], flush=True)
(HERE / "replay_receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
if any(x["status"] == "FAIL" for x in receipt["checks"]):
    raise SystemExit(1)
