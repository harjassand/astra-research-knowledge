"""Replay selected decisive public evidence in a disposable reconstructed layout.

Run with a Python providing SymPy1.14, mpmath and NumPy. This checks arithmetic
and packaging, not historical priority, external review or physical validity.
Original/frozen package bytes are never executed in place or modified.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

p = argparse.ArgumentParser()
p.add_argument("--repo", type=Path, required=True)
p.add_argument("--output", type=Path, required=True)
args = p.parse_args()
packet = args.repo.resolve() / "updates/FW-moving-heat-observable-20261015/package"
checks = [
    "workers/sharp_floor_independent/verify.py",
    "workers/sharp_boundary_qc/verify_sharp_certificate.py",
    "workers/sharp_boundary_qc/verify_universal.py",
    "workers/sharp_boundary_qc/verify_positive_obstruction.py",
    "workers/sharp_certificate_audit/independent_audit.py",
    "workers/sharp_certificate_audit/universal_audit.py",
    "workers/nonlinear_flow_audit/check_density_bridge.py",
    "workers/nonlinear_flow_audit/check_sharp_face.py",
    "workers/sharp_floor_independent/positive_branch/verify_obstruction.py",
    "workers/sharp_floor_independent/positive_branch/verify_output_skew.py",
    "workers/obstruction_escape/verify_pc_multiplier_obstruction.py",
    "workers/smooth_null_classification/pc_multiplier_audit/check_pc_multiplier.py",
    "workers/pulse_hardpair_audit/audit_hard_pair.py",
    "workers/pulse_observable_genesis/verify_hard_pair.py",
    "workers/interacting_bridge_audit/independent_checks.py",
    "root/check_sharp_consequence.py",
    "root/check_storage_budget.py",
    "root/check_output_skew_contact.py",
]
receipt = {"schema": "astra.fw-public-evidence-replay.v1", "commands": [],
           "scope": "Disposable public-layout arithmetic and packaging replay; no external scientific validation"}
with tempfile.TemporaryDirectory(prefix="astra-fw-evidence-") as temp:
    mirror = Path(temp)
    for name in ("workers", "root"):
        shutil.copytree(packet / "derived" / name, mirror / name)
    shutil.copytree(packet / "originals/sources", mirror / "sources")
    for name in checks:
        script = mirror / name
        assert script.is_file(), "Missing public proof/check: " + name
        run = subprocess.run([sys.executable, "-B", str(script)], cwd=script.parent,
                             capture_output=True, text=True)
        row = {"script": name, "script_sha256": hashlib.sha256(script.read_bytes()).hexdigest(),
               "exit_code": run.returncode, "stdout": run.stdout, "stderr": run.stderr}
        receipt["commands"].append(row)
        print(name + ": " + ("PASS" if run.returncode == 0 else "FAIL"), flush=True)
        if run.returncode:
            receipt["status"] = "FAIL"
            args.output.write_text(json.dumps(receipt, indent=2) + "\n")
            raise SystemExit(run.returncode)
receipt["status"] = "PASS"
args.output.write_text(json.dumps(receipt, indent=2) + "\n")
