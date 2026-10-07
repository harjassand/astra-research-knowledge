"""Finite diagnostics only; analytical claims are in random_matrices.md."""
import json
from pathlib import Path
import numpy as np

rng = np.random.default_rng(741026)

def tsvd(a, k):
    u, s, vh = np.linalg.svd(a, full_matrices=False)
    return (u[:, :k] * s[:k]) @ vh[:k]

def op(a):
    return np.linalg.norm(a, 2)

checks = []
for m, n in [(2, 2), (4, 7), (7, 4), (8, 8), (16, 10)]:
    p = min(m, n)
    for k in [1, p // 2, p - 1]:
        for trial in range(100):
            # Include a wide retained spectrum and a narrow boundary gap.
            s = np.sort(np.exp(rng.uniform(-3, 5, size=p)))[::-1]
            if trial % 3 == 0:
                s[k-1] = max(s[k], 1.0) * (1 + 10**rng.uniform(-6, -1))
                s[:k-1] = np.maximum(s[:k-1], s[k-1] * 2)
                s[k:] = np.minimum(s[k:], s[k-1] * 0.9999999)
            s = np.sort(s)[::-1]
            u, _ = np.linalg.qr(rng.normal(size=(m, p)) + 1j*rng.normal(size=(m, p)))
            v, _ = np.linalg.qr(rng.normal(size=(n, p)) + 1j*rng.normal(size=(n, p)))
            a = (u*s) @ v.conj().T
            e = rng.normal(size=(m, n)) + 1j*rng.normal(size=(m, n))
            gap = s[k-1] - s[k]
            eta = gap * 10**rng.uniform(-4, 3)
            e *= eta/op(e)
            lhs = op(tsvd(a+e, k)-tsvd(a, k))
            scale = s[k-1]/gap * eta
            checks.append({"m":m,"n":n,"k":k,"ratio_to_unit_scale":float(lhs/scale)})

# Necessity of the boundary factor: a 2x2 off-diagonal perturbation.
necessity = []
for gap in [1e-1, 1e-2, 1e-3, 1e-4]:
    a = np.diag([1+gap, 1.0])
    eta = gap * 1e-3
    e = np.array([[0.0, eta], [eta, 0.0]])
    ratio = op(tsvd(a+e,1)-tsvd(a,1)) / ((1+gap)/gap*eta)
    necessity.append({"gap":gap,"ratio_to_unit_scale":float(ratio)})

result = {"scope":"finite diagnostics, not proof or priority evidence",
          "cases":len(checks),
          "max_ratio_to_unit_scale":max(x["ratio_to_unit_scale"] for x in checks),
          "candidate_constant":8,
          "all_cases_below_candidate_constant":all(x["ratio_to_unit_scale"] <= 8*(1+1e-7) for x in checks),
          "boundary_factor_necessity":necessity}
Path(__file__).with_suffix(".json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps(result,indent=2))
