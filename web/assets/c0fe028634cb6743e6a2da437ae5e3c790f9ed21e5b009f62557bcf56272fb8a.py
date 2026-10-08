#!/usr/bin/env python3
"""Finite-step bisection for two resident-cycle invasion sign changes.

This is a numerical diagnostic, not interval validation. It inherits the
fixed-step RK4 implementation and resident-orbit convergence criterion from
reproduce_chemostat.py.
"""
import json
from pathlib import Path
from reproduce_chemostat import face_orbit

NSTEP = 960
MAX_ITER = 28
TARGETS = [
    {"name": "lambda3_on_12", "residents": (0, 1), "missing": 2,
     "lo": 0.300, "hi": 0.325},
    {"name": "lambda2_on_13", "residents": (0, 2), "missing": 1,
     "lo": 0.275, "hi": 0.300},
]

def rate(amp, residents, missing):
    row = face_orbit(amp, residents, nstep=NSTEP)
    return row["lambda"][missing], row

results = []
for target in TARGETS:
    lo, hi = target["lo"], target["hi"]
    flo, left = rate(lo, target["residents"], target["missing"])
    fhi, right = rate(hi, target["residents"], target["missing"])
    if flo * fhi >= 0:
        raise ValueError(f"Root not bracketed: {target['name']} {flo} {fhi}")
    history = []
    for _ in range(MAX_ITER):
        mid = (lo + hi) / 2
        fm, row = rate(mid, target["residents"], target["missing"])
        history.append({"amp": mid, "rate": fm, "cycles": row["cycles"],
                        "periodic_residual": row["periodic_residual"]})
        if flo * fm <= 0:
            hi, fhi, right = mid, fm, row
        else:
            lo, flo, left = mid, fm, row
    results.append({
        "name": target["name"],
        "nstep_per_period": NSTEP,
        "iterations": MAX_ITER,
        "bracket": [lo, hi],
        "endpoint_rates": [flo, fhi],
        "estimate": (lo + hi) / 2,
        "history": history,
    })
    print(target["name"], "bracket", lo, hi, "rates", flo, fhi,
          "estimate", (lo + hi) / 2, flush=True)

out = Path(__file__).with_name("threshold_bisection.json")
out.write_text(json.dumps(results, indent=2) + "\n")
print("wrote", out)
