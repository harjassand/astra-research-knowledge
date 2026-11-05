"""Run the bundled mathematical implementation checks from any working directory."""
from pathlib import Path
import hashlib
import importlib.metadata
import json
import platform
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
SCRIPTS = [
    "sampler_route/verify_two_square_fano.py",
    "sampler_route/verify_lawrence_minor.py",
    "decoding_route/audit_matroid_subdivision.py",
    "sampler_route/verify_cover_and_adaptive_clock.py",
    "decoding_route/verify_central_quotient.py",
    "verify_register.py",
    "intervention_route/finite_reset.py",
]
receipt = {
    "interpretation": "Exact algebraic and finite numerical implementation checks; not experimental validation or substitutes for the symbolic proofs.",
    "python": platform.python_version(),
    "packages": {name: importlib.metadata.version(name)
                 for name in ["numpy", "scipy", "mpmath"]},
    "checks": [],
}
for relative in SCRIPTS:
    p = ROOT / relative
    start = time.perf_counter()
    result = subprocess.run([sys.executable, str(p)], cwd=ROOT,
                            capture_output=True, text=True, timeout=240)
    check = {
        "script": relative,
        "sha256": hashlib.sha256(p.read_bytes()).hexdigest(),
        "exit_code": result.returncode,
        "elapsed_seconds": time.perf_counter() - start,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }
    receipt["checks"].append(check)
    print(("PASS " if result.returncode == 0 else "FAIL ") + relative, flush=True)
    if result.returncode:
        receipt["all_checks_passed"] = False
        (ROOT / "verification_receipt.json").write_text(json.dumps(receipt, indent=2)+"\n")
        sys.exit(result.returncode)

reset = json.loads((ROOT / "intervention_route/finite_reset_results.json").read_text())
residual = max(max(case["verification"].values()) for case in reset["cases"])
assert len(reset["cases"]) == 4
assert residual < 2e-54
assert all(0 < case["corrected_sine_amplitude"] <= 1
           and case["fresh_actuator_variance"] > 0
           and case["observable_momentum_arm_contrast"] > 0
           for case in reset["cases"])
receipt["finite_reset_maximum_residual"] = residual
receipt["all_checks_passed"] = True
(ROOT / "verification_receipt.json").write_text(json.dumps(receipt, indent=2)+"\n")
print("All seven bundled checks passed; reset residual %.4g." % residual, flush=True)
