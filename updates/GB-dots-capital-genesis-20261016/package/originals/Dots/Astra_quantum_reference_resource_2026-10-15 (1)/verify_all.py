"""Verify package integrity and replay exact certificates from any directory."""
from pathlib import Path
import hashlib
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
for line in (ROOT / "SHA256SUMS").read_text().splitlines():
    expected, relative = line.split("  ", 1)
    path = ROOT / relative
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    if actual != expected:
        raise SystemExit("SHA-256 mismatch: " + relative)
print("SHA-256 manifest verified", flush=True)
for name in ("exact_scalar_order_certificate.py", "clean_ternary_certificate.py", "check_finite_reference.py", "check_optimized_mmse.py", "check_robust_mmse.py"):
    subprocess.run([sys.executable, str(ROOT / "checks" / name)], check=True)
print("PASS: all five exact checks and all four reconstructed result fixtures verified", flush=True)
