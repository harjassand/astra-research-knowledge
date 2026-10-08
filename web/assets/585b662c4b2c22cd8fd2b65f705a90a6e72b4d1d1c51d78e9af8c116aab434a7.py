"""Finite check of the exact SVD-modulus reduction for SU(3) wall L_w.

This script is diagnostic only.  The identity in the accompanying memo is
proved algebraically and applies in every finite dimension.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[5]
CHECKER = ROOT / "outputs/research/sol_semiclassical_memory/regular_su3/verify_regular_su3.py"
spec = importlib.util.spec_from_file_location("regular_su3", CHECKER)
su3 = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(su3)


def frame(a: int, b: int):
    ts, _ = su3.harmonic_carrier(a, b)
    n = a + b
    c2 = (a*a + a*b + b*b + 3*a + 3*b) / 3
    c3 = (a-b) * (2*a+b+3) * (a+2*b+3) / 18
    alpha = c3/c2
    delta = c2*(c2/3 + .25) - c3*c3/c2
    ds = [sum(su3.d_symbol[k, i, j] * ts[i] @ ts[j]
              for i in range(8) for j in range(8)) for k in range(8)]
    ss = [(ds[k] - alpha*ts[k])/n for k in range(8)]
    return ts, ss, n, delta/n**2


def energy(a, generators):
    return sum(float(np.linalg.norm(g @ a - a @ g, "fro")**2)
               for g in generators)


def trial(a, b, seed):
    ts, ss, n, cs = frame(a, b)
    d = ts[0].shape[0]
    rng = np.random.default_rng(seed)
    # Coefficients of the two positive pieces in L_w.
    families = [(ts, 1/n**2), (ss, 1/(n*np.sqrt(cs)))]
    worst_identity_residual = 0.0
    min_weighted_gap = float("inf")
    min_psd_ratio = float("inf")
    samples = []
    ranks = sorted(set(q for q in (1, 2, max(2, d//3), d//2) if q <= d))
    for q in ranks:
        for _ in range(4):
            u0 = rng.normal(size=(d, d)) + 1j*rng.normal(size=(d, d))
            v0 = rng.normal(size=(d, d)) + 1j*rng.normal(size=(d, d))
            u, _ = np.linalg.qr(u0)
            v, _ = np.linalg.qr(v0)
            s = np.zeros(d)
            s[:q] = np.exp(rng.uniform(-1.0, 1.0, size=q))
            x = (u*s) @ v.conj().T
            left = (u*s) @ u.conj().T
            right = (v*s) @ v.conj().T
            ew_x = sum(weight*energy(x, gs) for gs, weight in families)
            ew_l = sum(weight*energy(left, gs) for gs, weight in families)
            ew_r = sum(weight*energy(right, gs) for gs, weight in families)
            gap = ew_x - (ew_l+ew_r)/2
            exact = 0.0
            for gs, weight in families:
                for g in gs:
                    h = u.conj().T @ g @ u
                    k = v.conj().T @ g @ v
                    # Sum_{i,j} s_i s_j |h_ij-k_ij|^2 is the
                    # difference e_G(X)-(e_G(|X|)+e_G(|X*|))/2.
                    exact += weight*float(np.sum(
                        (s[:, None]*s[None, :])*np.abs(h-k)**2))
            residual = abs(gap-exact)
            worst_identity_residual = max(worst_identity_residual, residual)
            min_weighted_gap = min(min_weighted_gap, gap)
            min_psd_ratio = min(min_psd_ratio, min(ew_l, ew_r)/ew_x)
            assert gap >= -2e-8, (a, b, q, gap)
            assert residual <= 2e-7*max(1.0, abs(ew_x)), residual
            samples.append({"rank": q, "gap": gap, "chosen_modulus_ratio":
                            min(ew_l, ew_r)/ew_x})
    return {"a": a, "b": b, "N": n, "d": d, "C_S": cs,
            "samples": len(samples),
            "worst_identity_residual": worst_identity_residual,
            "minimum_gap": min_weighted_gap,
            "minimum_best_modulus_ratio": min_psd_ratio}


if __name__ == "__main__":
    cases = [(3, 1), (4, 1), (4, 2), (5, 2)]
    print(json.dumps({"status": "finite-diagnostic-only",
                      "cases": [trial(a, b, 20261008 + 17*a + b)
                                for a, b in cases]}, indent=2))
