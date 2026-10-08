#!/usr/bin/env python3
"""Exact Floquet first-event yield for a driven two-electron radical pair.

The source-adjacent model is the two-electron, static-Gaussian-hyperfine-field
ensemble in Xiang et al. (JACS 2025) `SCRP_spin_and_chem_sim.m`, extended by a
transverse monochromatic RF field. Recombination is a singlet-selective sink
and separation is spin-independent. The drive-phase-averaged yield is computed
from a truncated Floquet-Liouville linear system, not trajectory propagation.

This is a conditional model calculation: the Gaussian field width and rates
are inherited from the source model, not measured for the 2026 mScarlet-I/FMN
system. Results must not be read as quantitative predictions for that sample.
"""
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from typing import Iterable

import numpy as np


def paulis() -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    sx = np.array([[0, 1], [1, 0]], dtype=complex)
    sy = np.array([[0, -1j], [1j, 0]], dtype=complex)
    sz = np.array([[1, 0], [0, -1]], dtype=complex)
    eye = np.eye(2, dtype=complex)
    return sx, sy, sz, eye


SX, SY, SZ, I2 = paulis()
I4 = np.eye(4, dtype=complex)
S1 = (np.kron(SX, I2), np.kron(SY, I2), np.kron(SZ, I2))
S2 = (np.kron(I2, SX), np.kron(I2, SY), np.kron(I2, SZ))
SINGLET = np.array([0, 1, -1, 0], dtype=complex) / np.sqrt(2)
P_S = np.outer(SINGLET, SINGLET.conj())
P_T = I4 - P_S
RHO_T = P_T / 3.0
X_RF_PER_T = -0.5 * (S1[0] + S2[0])  # H/hbar per (rad/ns/T) coefficient.


def commutator_superop(H: np.ndarray) -> np.ndarray:
    # Column-major vectorization: vec(H rho - rho H)=(I⊗H-H^T⊗I)vec(rho).
    return -1j * (np.kron(I4, H) - np.kron(H.T, I4))


@dataclass(frozen=True)
class SpinModel:
    sigma_T: float = 0.002
    gamma_rad_ns_T: float = 2 * np.pi * 28.0  # 28 GHz/T = 28/ns/T in cycles.
    k_recomb_ns: float = 0.1
    eta_recomb_over_sep: float = 1.0

    @property
    def k_sep_ns(self) -> float:
        return self.k_recomb_ns / self.eta_recomb_over_sep


def static_generator(h1_T: np.ndarray, h2_T: np.ndarray,
                     model: SpinModel) -> tuple[np.ndarray, np.ndarray]:
    """Return L0 and L_RF, with L(B_RF cos wt)=L0+B_RF cos(wt)L_RF."""
    H = np.zeros((4, 4), dtype=complex)
    for a, S in zip(h1_T, S1):
        H -= model.gamma_rad_ns_T * a * S / 2
    for a, S in zip(h2_T, S2):
        H -= model.gamma_rad_ns_T * a * S / 2
    K = model.k_sep_ns * I4 + model.k_recomb_ns * P_S
    L0 = commutator_superop(H) - 0.5 * (np.kron(I4, K) + np.kron(K.T, I4))
    Hrf_per_T = model.gamma_rad_ns_T * X_RF_PER_T
    Lrf = commutator_superop(Hrf_per_T)
    return L0, Lrf


def floquet_first_event_yield(h1_T: np.ndarray, h2_T: np.ndarray, *,
                              model: SpinModel, B0_T: float, B1_T: float,
                              f_GHz: float, sidebands: int = 1) -> dict[str, float]:
    """Exact phase-averaged yields at a finite Floquet cutoff.

    B0 is along z and B1 is the peak RF amplitude along x. f_GHz is cycles/ns.
    Integrating the driven unnormalized density over time gives the Floquet
    resolvent system A X = -rho(0) at harmonic zero. `sidebands=1` is exact to
    second order in B1; higher sidebands capture higher drive orders.
    """
    b0 = np.array([0.0, 0.0, B0_T])
    L0, Lrf = static_generator(h1_T + b0, h2_T + b0, model)
    w = 2 * np.pi * f_GHz  # rad/ns
    harmonics = np.arange(-sidebands, sidebands + 1)
    d = 16
    A = np.zeros((d * len(harmonics), d * len(harmonics)), dtype=complex)
    for i, m in enumerate(harmonics):
        sl = slice(i * d, (i + 1) * d)
        A[sl, sl] = L0 - 1j * m * w * np.eye(d)
        if i > 0:
            A[sl, slice((i - 1) * d, i * d)] = (B1_T / 2) * Lrf
        if i + 1 < len(harmonics):
            A[sl, slice((i + 1) * d, (i + 2) * d)] = (B1_T / 2) * Lrf
    rho_vec = RHO_T.reshape(-1, order="F")
    rhs = np.zeros(d * len(harmonics), dtype=complex)
    center = sidebands * d
    rhs[center:center + d] = -rho_vec
    x = np.linalg.solve(A, rhs)
    x0 = x[center:center + d].reshape((4, 4), order="F")
    y_sep = model.k_sep_ns * np.trace(x0)
    y_singlet_recomb = model.k_recomb_ns * np.trace(P_S @ x0)
    residual = abs((y_sep + y_singlet_recomb) - 1.0)
    return {
        "beta_sep": float(np.real(y_sep)),
        "y_recomb": float(np.real(y_singlet_recomb)),
        "max_imaginary_residual": float(max(abs(np.imag(y_sep)), abs(np.imag(y_singlet_recomb)))),
        "normalization_residual": float(residual),
    }


def ensemble_yield(*, n: int = 512, seed: int = 20261008,
                   model: SpinModel | None = None, B0_T: float = 0.0159,
                   B1_T: float = 0.0, f_GHz: float = 0.447,
                   sidebands: int = 1) -> dict[str, float]:
    """Monte Carlo over source-model independent Gaussian static fields."""
    if model is None:
        model = SpinModel()
    rng = np.random.default_rng(seed)
    fields = rng.normal(0.0, model.sigma_T, size=(n, 2, 3))
    vals = np.empty((n, 3), dtype=float)
    for j in range(n):
        z = floquet_first_event_yield(fields[j, 0], fields[j, 1], model=model,
                                      B0_T=B0_T, B1_T=B1_T, f_GHz=f_GHz,
                                      sidebands=sidebands)
        vals[j] = (z["beta_sep"], z["y_recomb"], z["normalization_residual"])
    out = {
        "n": n,
        "seed": seed,
        "sigma_T": model.sigma_T,
        "k_recomb_ns": model.k_recomb_ns,
        "eta": model.eta_recomb_over_sep,
        "k_sep_ns": model.k_sep_ns,
        "B0_T": B0_T,
        "B1_T_peak": B1_T,
        "f_GHz": f_GHz,
        "sidebands": sidebands,
        "beta_sep_mean": float(vals[:, 0].mean()),
        "beta_sep_sem": float(vals[:, 0].std(ddof=1) / np.sqrt(n)),
        "y_recomb_mean": float(vals[:, 1].mean()),
        "y_recomb_sem": float(vals[:, 1].std(ddof=1) / np.sqrt(n)),
        "max_per_sample_normalization_residual": float(vals[:, 2].max()),
    }
    return out


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--n", type=int, default=512)
    p.add_argument("--seed", type=int, default=20261008)
    p.add_argument("--sigma-mT", type=float, default=2.0)
    p.add_argument("--eta", type=float, default=1.0)
    p.add_argument("--krec-per-ns", type=float, default=0.1)
    p.add_argument("--B0-mT", type=float, default=15.9)
    p.add_argument("--B1-mT", type=float, default=0.0)
    p.add_argument("--f-MHz", type=float, default=447.0)
    p.add_argument("--sidebands", type=int, default=1)
    args = p.parse_args()
    model = SpinModel(sigma_T=args.sigma_mT * 1e-3,
                      k_recomb_ns=args.krec_per_ns,
                      eta_recomb_over_sep=args.eta)
    result = ensemble_yield(n=args.n, seed=args.seed, model=model,
                            B0_T=args.B0_mT * 1e-3,
                            B1_T=args.B1_mT * 1e-3,
                            f_GHz=args.f_MHz * 1e-3,
                            sidebands=args.sidebands)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
