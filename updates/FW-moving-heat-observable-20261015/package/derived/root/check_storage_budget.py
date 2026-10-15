"""Exact sufficient-budget consequences; no optimization/grid enumeration."""
from fractions import Fraction as Q
from pathlib import Path
import json

M = 224
gamma = Q(3, 1250)
old = Q(1, 2500000)
N = 10**17
E = 2 * M / gamma
R4 = (2 * M + 1) / gamma
checks = {
    "constant_gain": gamma / old == 6000,
    "gradient_21": R4 < 21**4,
    "horizon_001": (6960 * E)**4 < Q(1, 1000)**4 * (N - 1)**3,
}
assert all(checks.values())
out = {
    "status": "EXACT_PASS", "gamma": str(gamma), "old_gamma": str(old),
    "gain": str(gamma / old), "R4": str(R4), "E_star": str(E), "N": N,
    "checks": checks,
    "scope": "Sufficient horizon/gradient budget only; no spatial grid or storage value computed",
}
Path(__file__).with_name("STORAGE_BUDGET_CHECK.json").write_text(json.dumps(out, indent=2) + "\n")
print(json.dumps(out))
