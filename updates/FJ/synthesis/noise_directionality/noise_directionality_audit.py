#!/usr/bin/env python3
"""Reproducible algebraic/numerical audit for FJ hydraulic noise directionality.

Units are normalized.  The script checks the hidden-port elimination identity,
the classical equilibrium FDT, and a frequency-dependent chiral example.
No source repository or FJ sibling artifact is imported.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parent


def effective_response(K: np.ndarray, C: np.ndarray, G: np.ndarray,
                       Y: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return H, the internal voltage response A^-1, and Y's Hermitian part."""
    A = G + Y
    Ainv = np.linalg.inv(A)
    H = K - C @ Ainv @ C
    Yh = (Y + Y.conj().T) / 2
    return H, Ainv, Yh


def effective_noise(K: np.ndarray, C: np.ndarray, G: np.ndarray,
                    Ainv: np.ndarray, Yh: np.ndarray) -> np.ndarray:
    """Reduced noise covariance divided by 2 k_B T.

    Primitive wet noise is ordered (eta_Q, eta_I), with covariance
    [[K,C],[C,G]].  Dry-network noise eta_Y has covariance Yh and is
    independent.  KCL gives eta_eff=eta_Q-C A^-1(eta_I+eta_Y).
    """
    z = np.zeros_like(K, dtype=complex)
    primitive = np.block([
        [K.astype(complex), C.astype(complex), z],
        [C.astype(complex), G.astype(complex), z],
        [z, z, Yh],
    ])
    transfer = np.hstack([
        np.eye(K.shape[0], dtype=complex),
        -C @ Ainv,
        -C @ Ainv,
    ])
    return transfer @ primitive @ transfer.conj().T


def close(a: np.ndarray, b: np.ndarray, tol: float = 2e-11) -> bool:
    return bool(np.max(np.abs(a - b)) <= tol)


def main() -> None:
    # Heterogeneous wet interfaces.  Each satisfies C_i^2 < K_i G_i.
    K = np.diag([1.8, 2.1])
    C = np.diag([0.55, 0.60])
    G = np.diag([0.9, 1.1])
    g_plus, g_minus = 0.8, 0.05
    Y0 = np.array([
        [g_plus + g_minus, -g_minus],
        [-g_plus, g_plus + g_minus],
    ], dtype=complex)
    shunt_capacitances = np.diag([0.4, 0.7])

    sweep = []
    max_fdt_residual = 0.0
    min_dissipative_eigenvalue = math.inf
    max_passivity_violation = 0.0
    for omega in [0.0, 0.01, 0.1, 1.0, 10.0, 100.0]:
        Y = Y0 + 1j * omega * shunt_capacitances
        H, Ainv, Yh = effective_response(K, C, G, Y)
        Neff = effective_noise(K, C, G, Ainv, Yh)
        Hh = (H + H.conj().T) / 2
        residual = float(np.max(np.abs(Neff - Hh)))
        eigs = np.linalg.eigvalsh(Hh)
        max_fdt_residual = max(max_fdt_residual, residual)
        min_dissipative_eigenvalue = min(min_dissipative_eigenvalue,
                                         float(eigs.min()))
        max_passivity_violation = max(max_passivity_violation,
                                      max(0.0, -float(eigs.min())))
        sweep.append({
            "omega_normalized": omega,
            "H11": [float(H[0, 0].real), float(H[0, 0].imag)],
            "H12": [float(H[0, 1].real), float(H[0, 1].imag)],
            "H21": [float(H[1, 0].real), float(H[1, 0].imag)],
            "H22": [float(H[1, 1].real), float(H[1, 1].imag)],
            "H21_over_H12_magnitude": float(abs(H[1, 0] / H[0, 1])),
            "min_eigenvalue_Hermitian_part": float(eigs.min()),
            "FDT_residual_after_dividing_by_2kBT": residual,
        })

    # The ideal chiral limit keeps H12=0 at all frequencies, but its useful
    # transfer decays as capacitive shunts dominate A(omega).
    Y_chiral = np.array([[g_plus, 0.0], [-g_plus, g_plus]], dtype=complex)
    chiral = []
    for omega in [0.0, 0.1, 1.0, 10.0, 100.0]:
        Y = Y_chiral + 1j * omega * shunt_capacitances
        H, Ainv, Yh = effective_response(K, C, G, Y)
        Neff = effective_noise(K, C, G, Ainv, Yh)
        Hh = (H + H.conj().T) / 2
        chiral.append({
            "omega_normalized": omega,
            "abs_H12": float(abs(H[0, 1])),
            "abs_H21": float(abs(H[1, 0])),
            "Re_H11": float(H[0, 0].real),
            "Re_H22": float(H[1, 1].real),
            "one_way_psd_slack": float((H[0, 0].real * H[1, 1].real)
                                        - abs(H[1, 0]) ** 2 / 4),
            "FDT_residual_after_dividing_by_2kBT": float(
                np.max(np.abs(Neff - Hh))),
        })

    # Exact one-way static detector and matched passive load.
    # In normalized units H=[[a,0],[b,d]], R=1/d.
    a, d, b = 1.0, 1.0, 1.8
    H_tri = np.array([[a, 0.0], [b, d]])
    Hh_tri = (H_tri + H_tri.T) / 2
    eta_max_power = b * b / (4 * a * d)
    # For p1(t)=p0 on [0,tau], W=a p0^2 tau and the loaded-flow SNR^2 is
    # eta W/(kBT).  The no-load flow readout attains the general 2W/(kBT)
    # matrix bound only in the b=2 sqrt(a d) limit.
    p0, tau = 0.3, 12.0
    W = a * p0 * p0 * tau
    SNR2_matched = eta_max_power * W  # kBT=1
    SNR2_unloaded = (b * b * p0 * p0 * tau) / (2 * d)  # kBT=1
    snr_bound_unloaded = 2 * W

    # Equality witness for the general passivity/FDT SNR bound.  It is an
    # abstract passive one-way two-port (PSD Hermitian part), not the specific
    # wet-plus-grounded-Hall topology considered in the incoming source.
    b_sharp = 2.0 * math.sqrt(a * d)
    H_sharp = np.array([[a, 0.0], [b_sharp, d]])
    Hh_sharp = (H_sharp + H_sharp.T) / 2

    # DC source-specific grounded chiral network with the heterogeneous wet
    # parameters above.  This verifies the stricter topology-specific bound.
    Y_source_chiral = np.array([[g_plus, 0.0], [-g_plus, g_plus]], dtype=complex)
    H_source, _, _ = effective_response(K, C, G, Y_source_chiral)
    a_source = float(H_source[0, 0].real)
    d_source = float(H_source[1, 1].real)
    b_source = float(abs(H_source[1, 0]))
    eta_source_actual = b_source * b_source / (4 * a_source * d_source)

    def eta_c(z: float) -> float:
        root = math.sqrt(1.0 + z)
        return (root - 1.0) / (root + 1.0)

    chi = [float(C[i, i] ** 2 / (K[i, i] * G[i, i])) for i in range(2)]
    z_values = [x / (1.0 - x) for x in chi]
    source_topology_bound = 0.25 * eta_c(z_values[0]) * eta_c(z_values[1])

    # Source-reported material figures of merit, used conditionally only.
    conditional_materials = {}
    for label, z in [("graphene_estimate", 4e-4), ("graphitic_estimate", 11.0)]:
        eta_c_one = eta_c(z)
        eta_pair = 0.25 * eta_c_one * eta_c_one
        work_kbt_for_snr5 = 25.0 / eta_pair
        kbt_300 = 1.380649e-23 * 300.0
        conditional_materials[label] = {
            "source_reported_Z_per_wet_interface": z,
            "eta_c_one_interface": eta_c_one,
            "source_topology_eta_pair_upper_bound": eta_pair,
            "input_work_kBT_for_loaded_SNR5_at_eta_bound": work_kbt_for_snr5,
            "input_work_J_for_loaded_SNR5_at_300K_if_bound_saturated":
                work_kbt_for_snr5 * kbt_300,
            "status": "conditional arithmetic on source-reported theoretical Z; not measured device performance",
        }

    # Exact OU discretization checks equilibrium pressure covariance for
    # S=I, kBT=1, dp=-H p dt + noise with D=H+H^T.
    # Use the exact stationary discrete innovation covariance I-A A^T.
    dt = 0.05
    decay = math.exp(-dt)
    Aou = decay * np.array([[1.0, 0.0], [-b * dt, 1.0]])
    Qou = np.eye(2) - Aou @ Aou.T
    eig_q = np.linalg.eigvalsh(Qou)
    rng = np.random.default_rng(20261014)
    chol_q = np.linalg.cholesky(Qou)
    state = rng.standard_normal(2)
    samples = []
    burn = 2000
    count = 100_000
    for j in range(burn + count):
        state = Aou @ state + chol_q @ rng.standard_normal(2)
        if j >= burn:
            samples.append(state.copy())
    empirical = np.cov(np.asarray(samples).T, bias=True)
    lag_cov = np.array([[1.0, 0.0], [-b * dt, 1.0]]) * decay

    assert max_fdt_residual < 1e-12
    assert min_dissipative_eigenvalue > 0.0
    assert all(abs(row["H21_over_H12_magnitude"] - 16.0) < 1e-10
               for row in sweep)
    assert all(row["abs_H12"] < 1e-12 for row in chiral)
    assert b * b <= 4 * a * d
    assert eta_source_actual <= source_topology_bound + 1e-12
    assert float(np.max(np.abs(empirical - np.eye(2)))) < 0.03

    result = {
        "scope": "dimensionless controlled linear-network example; not a device prediction",
        "conventions": {
            "temperature": "common T across wet interfaces, dry network, and any passive load",
            "PSD": "two-sided angular-frequency; S_eta=2 k_B T Hermitian(H)",
            "wet_parameters": "K=diag(1.8,2.1), C=diag(0.55,0.60), G=diag(0.9,1.1)",
            "dry_network": "three-contact chiral conductance matrix with g+=0.8, g-=0.05 plus shunt capacitances diag(0.4,0.7)",
            "no_claim": "no physical transducer, Hall element, or measurement noise was acquired",
        },
        "heterogeneous_finite_reverse_leak_sweep": sweep,
        "ideal_chiral_dynamic_sweep": chiral,
        "summary": {
            "max_FDT_residual_after_dividing_by_2kBT": max_fdt_residual,
            "min_eigenvalue_Hermitian_H_across_sweep": min_dissipative_eigenvalue,
            "max_passivity_violation": max_passivity_violation,
            "one_way_static_example": {
                "H": H_tri.tolist(),
                "Hermitian_part": Hh_tri.tolist(),
                "det_Hermitian_part": float(np.linalg.det(Hh_tri)),
                "b_squared_le_4ad_slack": float(4 * a * d - b * b),
                "max_power_load_R": 1.0 / d,
                "load_efficiency_eta": eta_max_power,
                "source_work_W_kBT_units": W,
                "matched_load_SNR_squared_kBT_units": SNR2_matched,
                "matched_load_SNR2_over_W": SNR2_matched / W,
                "unloaded_flow_SNR2_kBT_units": SNR2_unloaded,
                "unloaded_general_bound_2W_over_kBT": snr_bound_unloaded,
            },
            "general_bound_sharpness_witness": {
                "H": H_sharp.tolist(),
                "Hermitian_part": Hh_sharp.tolist(),
                "det_Hermitian_part": float(np.linalg.det(Hh_sharp)),
                "b_squared_over_4ad": float(b_sharp * b_sharp / (4 * a * d)),
                "scope": "abstract passive one-way two-port, not the incoming wet-Hall topology",
            },
            "source_specific_ideal_chiral_topology": {
                "H_DC_real": H_source.real.tolist(),
                "kappa1": a_source,
                "kappa2": d_source,
                "b_magnitude": b_source,
                "load_efficiency_eta": eta_source_actual,
                "wet_chi": chi,
                "wet_Z": z_values,
                "source_topology_eta_upper_bound_from_Z": source_topology_bound,
                "loaded_SNR2_over_input_work_kBT": eta_source_actual,
                "notes": "dimensionless toy values only; no material/device claim",
            },
            "source_reported_material_estimates_conditional": conditional_materials,
            "equilibrium_pressure_OU": {
                "dt": dt,
                "innovation_min_eigenvalue": float(eig_q.min()),
                "empirical_covariance_from_seed_20261014": empirical.tolist(),
                "target_covariance": np.eye(2).tolist(),
                "lag_1_covariance": lag_cov.tolist(),
                "lag_1_asymmetry": float(lag_cov[1, 0] - lag_cov[0, 1]),
                "sample_count_after_burn_in": count,
            },
        },
    }
    out = ROOT / "noise_directionality_results.json"
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result["summary"], indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
