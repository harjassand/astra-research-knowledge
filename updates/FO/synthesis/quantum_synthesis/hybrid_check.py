"""Finite N=6 AKLT check for the gap-free response bracket.

The two source files in inputs/fn-root are read-only copies from the pinned
PR84 packet.  This script uses their exact integer/rational model definition,
then computes the regularized spectral lower endpoint independently by a
floating Hermitian eigensolve.  It is a finite numerical diagnostic only.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "inputs" / "fn-root"))

import aklt_r3_obstruction as ak  # noqa: E402
from aklt_n6_interval import bond_projector  # noqa: E402


N = ak.N
Z = sum(int(v * v) for v in ak.PSI.values())
psi = np.asarray([float(ak.PSI[word]) for word in ak.ZERO])
b = np.asarray([float(v) for v in ak.B])
Hq = sum((bond_projector(j) for j in range(N)), start=__import__("sympy").zeros(len(ak.ZERO)))
H = np.asarray(Hq.tolist(), dtype=np.float64)

assert np.max(np.abs(H - H.T)) < 1e-13
assert np.max(np.abs(H @ psi)) < 1e-12
assert abs(float(psi @ psi) - Z) < 1e-10
assert abs(float(psi @ b)) < 1e-12

evals, evecs = np.linalg.eigh(H)
weights = np.abs(evecs.T @ b) ** 2 / Z
keep = evals > 1e-9
assert np.max(np.abs(evecs[:, ~keep].T @ b)) < 1e-8
chi_spectral = float(np.sum(weights[keep] / evals[keep]))

etas = [1.0, 0.5, 0.25, 0.1, 0.05]
rows = []
for eta in etas:
    chi_eta = float(np.sum(weights[keep] * evals[keep] / (evals[keep] ** 2 + eta**2)))
    rows.append({
        "eta": eta,
        "chi_eta": chi_eta,
        "chi_eta_is_lower_bound": chi_eta <= chi_spectral + 1e-12,
        "bias_to_spectral_truth": chi_spectral - chi_eta,
        "per_trial_output_bound_a1": 1.0 / (2.0 * eta),
        "hoeffding_trials_for_0.001_at_95pct": int(np.ceil(
            (1.0 / (2.0 * eta)) ** 2 * np.log(2.0 / 0.05) / (2.0 * 0.001**2)
        )),
        "spectral_gap_lower_bound_from_N816_comparator": 0.1,
    })

out = {
    "model": "periodic spin-1 AKLT N=6, source b=S_z(0)|psi>, computed in exact Sz=0 sector (dimension 141)",
    "numerical_method": "float64 Hermitian diagonalization of copied exact rational H; no stochastic trials",
    "normalizer_Z_exact_from_source_mps": str(Z),
    "source_range_kernel_orthogonality_residual": float(np.max(np.abs(evecs[:, ~keep].T @ b))),
    "spectral_chi_approx": chi_spectral,
    "N816_exact_reference_chi_approx": 1.450550837609686,
    "local_dual_upper_N816": 1.457001657709544,
    "Knabe_residual_upper_N816": 1.4537037411509957,
    "Knabe_gap_claim_scope": "N816 reports exact rational patch-to-ring derivation gamma=1/10; this check did not independently verify that derivation",
    "regularized_lower_endpoints": rows,
    "limitations": [
        "Numerical eigensolve is not an exact certificate and does not simulate the transition instrument.",
        "Hoeffding counts are a sufficient worst-case iid shot bound, not a lower bound or an implemented cost.",
        "Energy-readout, state preparation, filter, control and physical calibration costs are excluded from the shot counts.",
    ],
}
(HERE / "hybrid_check.json").write_text(json.dumps(out, indent=2) + "\n")
print(json.dumps(out, indent=2))
