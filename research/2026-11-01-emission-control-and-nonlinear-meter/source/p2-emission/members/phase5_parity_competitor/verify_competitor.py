#!/usr/bin/env python3
"""Reproducible algebra and resource checks for an established parity-meter route.

This is a model certificate, not a microscopic superconducting-circuit simulation.
It uses only NumPy and SciPy, and writes its own results beside this script.
Run: python phase5_parity_competitor/verify_competitor.py
"""

from __future__ import annotations

import itertools
import json
from pathlib import Path

import numpy as np
from scipy.linalg import expm
from scipy.optimize import brentq
from scipy.special import erfc, erfcinv, i0e, j0


HERE = Path(__file__).resolve().parent
I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Z = np.diag([1, -1]).astype(complex)


def kron_all(xs):
    out = np.array([[1.0]], dtype=complex)
    for x in xs:
        out = np.kron(out, x)
    return out


def pauli(n, x_sites=(), z_sites=()):
    return kron_all([
        (X if k in x_sites else I2) @ (Z if k in z_sites else I2)
        for k in range(n)
    ])


def parity_meter_case(name, delta_e=None, delta_f=None, gamma_e=0.0,
                      rate_spread=0.0):
    """Exact 3x3 cross-block Lindblad evolution for all four-data-qubit coherences.

    H_s = diag(0, h_e(s), h_f(s)); g,e,f are ancilla levels.
    All bath records are traced over, not replaced by a coarse parity outcome.
    Delta arrays are fractional errors relative to pi radians per unit dwell.
    """
    w, T = 4, 1.0
    de = np.zeros(w) if delta_e is None else np.array(delta_e)
    df = np.zeros(w) if delta_f is None else np.array(delta_f)
    occupations = np.array(list(itertools.product([0, 1], repeat=w)))
    parities = (-1) ** occupations.sum(axis=1)
    gamma_f, gamma_phi = 0.23, 0.17
    Q = np.diag([0.0, 1.0, 1.0])
    # Ramsey preparation and final Ramsey analysis on the g-f subspace.
    R = np.array([[1/np.sqrt(2), 0, 1/np.sqrt(2)],
                  [0, 1, 0],
                  [1/np.sqrt(2), 0, -1/np.sqrt(2)]], dtype=complex)
    initial = np.outer(R[:, 0], R[:, 0].conj())
    amps, hs, jumps = [], [], []
    for occ in occupations:
        he, hf = np.pi * ((1 + de) @ occ), np.pi * ((1 + df) @ occ)
        h = np.diag([0.0, he, hf]).astype(complex)
        gf = gamma_f * (1 + rate_spread * (2 * occ[0] - 1))
        jf = np.zeros((3, 3), dtype=complex)
        jf[1, 2] = np.sqrt(gf)
        je = np.zeros((3, 3), dtype=complex)
        je[0, 1] = np.sqrt(gamma_e)
        js = [jf, je, np.sqrt(gamma_phi) * Q]
        heff = h - 0.5j * sum((j.conj().T @ j for j in js), np.zeros((3, 3)))
        amps.append(R @ expm(-1j * heff * T) @ R[:, 0])
        hs.append(h)
        jumps.append(js)
    # Each outcome is a Schur multiplier on the data density matrix.
    G = np.zeros((3, 2**w, 2**w), dtype=complex)
    for s in range(2**w):
        for sp in range(2**w):
            L = -1j * (np.kron(np.eye(3), hs[s]) - np.kron(hs[sp].T, np.eye(3)))
            for js, jsp in zip(jumps[s], jumps[sp]):
                L += np.kron(jsp.conj(), js)
                L -= 0.5 * np.kron(np.eye(3), js.conj().T @ js)
                L -= 0.5 * np.kron((jsp.conj().T @ jsp).T, np.eye(3))
            r = (expm(T * L) @ initial.reshape(-1, order="F")).reshape((3, 3), order="F")
            G[:, s, sp] = np.diag(R @ r @ R.conj().T)
    Gsum = G.sum(axis=0)
    sector_errors, prob_spreads, coherence_losses, no_click_errors = [], [], [], []
    for p in [1, -1]:
        ids = np.flatnonzero(parities == p)
        for m in range(3):
            block = G[m][np.ix_(ids, ids)]
            sector_errors.append(np.max(np.abs(block - block[0, 0])))
            prob_spreads.append(np.ptp(np.real(np.diag(block))))
            no_click_errors.append(np.max(np.abs(np.array(amps)[ids, m] - np.array(amps)[ids[0], m])))
        coherence_losses.append(np.max(1 - np.abs(Gsum[np.ix_(ids, ids)])))
    return {
        "name": name,
        "max_intrasector_instrument_scalar_defect": float(max(sector_errors)),
        "max_intrasector_outcome_probability_spread": float(max(prob_spreads)),
        "max_intrasector_unconditional_coherence_loss": float(max(coherence_losses)),
        "max_no_click_kraus_scalar_defect": float(max(no_click_errors)),
        "trace_preservation_error": float(np.max(np.abs(np.diag(Gsum) - 1))),
    }


def verify_cnot_teleportation():
    """Verify all 256 branches, not selected successful measurement outcomes.

    Mode order: input u, input v, resource a,b, output c,d.
    Resource preparation: |0000>, measure X_a X_c X_d and X_b X_d.
    Bell measurements: XX, then individual Z measurements of consumed modes.
    """
    n, dim = 6, 64
    identity = np.eye(dim, dtype=complex)
    S1, S2 = pauli(n, (2, 4, 5)), pauli(n, (3, 5))
    B1, B2 = pauli(n, (0, 2)), pauli(n, (1, 3))
    initial = np.zeros((dim, 4), dtype=complex)
    for inp in range(4):
        initial[inp * 16, inp] = 1
    target = np.zeros((4, 4), dtype=complex)
    for u, v in itertools.product([0, 1], repeat=2):
        target[2*u + (v ^ u), 2*u + v] = 1
    max_error, probabilities, total = 0.0, [], np.zeros((4, 4), dtype=complex)
    phase_fault_errors, readout_fault_errors = [], []
    for r1, r2 in itertools.product([0, 1], repeat=2):
        resource = ((identity + (-1)**r2*S2)/2) @ ((identity + (-1)**r1*S1)/2) @ initial
        resource = pauli(n, z_sites=tuple(k for k, b in [(2, r1), (3, r2)] if b)) @ resource
        for x1, x2 in itertools.product([0, 1], repeat=2):
            bell = ((identity + (-1)**x2*B2)/2) @ ((identity + (-1)**x1*B1)/2)
            state = bell @ resource
            for zu, zv, za, zb in itertools.product([0, 1], repeat=4):
                offset = (8*zu + 4*zv + 2*za + zb) * 4
                K = state[offset:offset+4]
                z1, z2 = zu ^ za, zv ^ zb
                correction = pauli(2,
                    x_sites=tuple(k for k, b in [(0, z1), (1, z1 ^ z2)] if b),
                    z_sites=tuple(k for k, b in [(0, x1 ^ x2), (1, x2)] if b))
                corrected = correction.conj().T @ K
                amplitude = np.trace(target.conj().T @ corrected) / 4
                max_error = max(max_error, np.linalg.norm(corrected - amplitude*target))
                probabilities.append(float(abs(amplitude)**2))
                total += K.conj().T @ K
                # A false XX outcome induces only a Z correction error.
                for flip in [0, 1]:
                    xx1, xx2 = x1 ^ (flip == 0), x2 ^ (flip == 1)
                    wrong = pauli(2,
                        x_sites=tuple(k for k, b in [(0, z1), (1, z1 ^ z2)] if b),
                        z_sites=tuple(k for k, b in [(0, xx1 ^ xx2), (1, xx2)] if b))
                    diff = wrong.conj().T @ correction
                    phase_fault_errors.append(np.max(np.abs(diff - np.diag(np.diag(diff)))))
                # By contrast, one false Z readout causes an X-type frame error.
                wrong_z1 = z1 ^ 1
                wrong = pauli(2,
                    x_sites=tuple(k for k, b in [(0, wrong_z1), (1, wrong_z1 ^ z2)] if b),
                    z_sites=tuple(k for k, b in [(0, x1 ^ x2), (1, x2)] if b))
                readout_fault_errors.append(float(np.max(np.abs(np.diag(wrong.conj().T @ correction)))))
    # Z faults on any physical mode immediately before Bell projection remain Z-type on outputs.
    physical_phase_fault_defect = 0.0
    resource = ((identity + S2)/2) @ ((identity + S1)/2) @ initial
    for site in range(6):
        faulty_resource = pauli(n, z_sites=(site,)) @ resource
        for x1, x2 in itertools.product([0, 1], repeat=2):
            state = ((identity + (-1)**x2*B2)/2) @ ((identity + (-1)**x1*B1)/2) @ faulty_resource
            for zu, zv, za, zb in itertools.product([0, 1], repeat=4):
                offset = (8*zu + 4*zv + 2*za + zb) * 4
                z1, z2 = zu ^ za, zv ^ zb
                correction = pauli(2,
                    x_sites=tuple(k for k, b in [(0, z1), (1, z1 ^ z2)] if b),
                    z_sites=tuple(k for k, b in [(0, x1 ^ x2), (1, x2)] if b))
                E = correction.conj().T @ state[offset:offset+4] @ target.conj().T
                physical_phase_fault_defect = max(physical_phase_fault_defect,
                    float(np.linalg.norm(E - np.diag(np.diag(E)))))
    return {
        "branches_checked": len(probabilities),
        "max_corrected_branch_operator_error": float(max_error),
        "min_branch_probability": min(probabilities),
        "max_branch_probability": max(probabilities),
        "completeness_error": float(np.linalg.norm(total - np.eye(4))),
        "xx_record_flip_non_Z_defect": float(max(phase_fault_errors)),
        "physical_Z_fault_non_Z_defect": physical_phase_fault_defect,
        "wrong_Z_readout_frame_has_zero_diagonal": max(readout_fault_errors) == 0.0,
    }


def double_decay_probability(T, gamma_f, gamma_e):
    # Includes the initial probability 1/2 to be in f.
    if abs(gamma_f - gamma_e) < 1e-12:
        return 0.5 * (1 - np.exp(-gamma_f*T) * (1 + gamma_f*T))
    survival = (gamma_f*np.exp(-gamma_e*T) - gamma_e*np.exp(-gamma_f*T)) / (gamma_f-gamma_e)
    return 0.5 * (1 - survival)


def cat_projection(nbar, phi):
    alpha, s = np.sqrt(nbar), np.exp(-2*nbar)
    diagonal = np.exp(-phi*phi/2) * j0(2*alpha*phi)
    offdiagonal = np.exp(-(phi-2*alpha)**2/2) * i0e(2*alpha*phi)
    even = (diagonal + offdiagonal) / (1+s)
    odd = (diagonal - offdiagonal) / (1-s)
    return (even+odd)/2, (even-odd)/2


def resource_frontier():
    # Arithmetic example, NOT a measured decomposition of the 2025 experiment.
    clocks = {"prep_us": 0.2, "mapping_window_per_link_us": 0.35,
              "switches_outside_mapping_us": 0.2, "readout_us": 0.8,
              "reset_us": 0.7, "restabilization_us": 0.9, "controller_us": 0.2}
    overhead = clocks["prep_us"] + clocks["switches_outside_mapping_us"] + clocks["controller_us"]
    overhead += max(clocks["readout_us"] + clocks["reset_us"], clocks["restabilization_us"])
    rows = []
    for w in [2, 3, 4]:
        for schedule in ["sequential", "simultaneous"]:
            dwell = clocks["mapping_window_per_link_us"] * (w if schedule == "sequential" else 1)
            cycle = overhead + dwell
            rows.append({"weight": w, "schedule": schedule, "mapping_us": dwell,
                "full_cycle_us": cycle,
                "per_cat_odd_loss_probability_n2_T1_63us": float((1-np.exp(-2*2*cycle/63))/2),
                "double_decay_probability_T1f25us_T1e50us": float(double_decay_probability(dwell, 1/25, 1/50)),
                "f_decay_probability_initial_half": float((1-np.exp(-dwell/25))/2)})
    zeno = []
    eta, qm, pd, epsilon, q = 0.5, 0.01, 0.05, 0.1, 0.1
    A = erfcinv(2*qm)**2
    B = -np.log(1-2*pd)/2
    for nbar in [2.0, 4.0]:
        alpha = np.sqrt(nbar)
        c, d = cat_projection(nbar, 2*alpha)
        grid = np.linspace(0.5*alpha, 2*alpha, 501)
        roots = []
        for lo, hi in zip(grid[:-1], grid[1:]):
            if cat_projection(nbar, lo)[0] * cat_projection(nbar, hi)[0] < 0:
                roots.append(brentq(lambda phi: cat_projection(nbar, phi)[0], lo, hi))
        root = max(roots, key=lambda phi: abs(cat_projection(nbar, phi)[1])) if roots else None
        for w in [2, 4]:
            # Optimistic phi_readout -> 0 factor set to one; neglects transient penalty.
            gamma_over_k2 = 2*epsilon*q*abs(d)**w
            zeno.append({"nbar": nbar, "weight": w,
                "identity_coefficient_at_phi_2alpha": float(c),
                "parity_coefficient_at_phi_2alpha": float(d),
                "fractional_identity_contamination": float(abs(c/d)),
                "nearest_high_signal_zero_identity_phi": root,
                "optimistic_Gamma_m_over_kappa2": float(gamma_over_k2),
                "required_kappa2_over_kappa1": float(A*nbar/(eta*B*gamma_over_k2))})
    zread = [{"nbar": n, "eta": 0.5,
              "single_release_homodyne_error": float(0.5*erfc(np.sqrt(2*0.5*n))),
              "four_readout_union_bound": float(2*erfc(np.sqrt(2*0.5*n)))} for n in [2, 4, 8]]
    return {"arithmetic_example_only": True, "clock_assumptions": clocks, "cycle_rows": rows,
            "zeno_frontier_assumptions": {"eta": eta, "readout_error": qm, "allowed_per_cat_phase_flip": pd,
                "EJ_over_hbar_kappa2": epsilon, "readout_nbar_times_phi_squared": q,
                "homodyne_erfc_constant": float(A), "loss_exposure_constant": float(B)},
            "zeno_frontier": zeno, "destructive_Z_readout_examples": zread}


def noisy_factory_frontier():
    """Exact classical final-syndrome decoding in a stated effective noise model.

    This is not a full quantum noisy-factory certificate. It models the resource
    after stabilizer projection as one of four X-syndrome sectors, with independent
    Z jumps, projective checks with classical assignment noise, and erased records.
    Crucially it decodes the LAST state and retains a finite unobserved tail.
    """
    lam, round_us, tail_us = 0.002, 2.45, 0.5  # illustrative, per cat rate in /us
    q, erasure = 0.02, 0.01
    generator = np.zeros((4, 4))
    for state in range(4):
        # Z_a and Z_c flip S1; Z_b flips S2; Z_d flips both.
        for toggle, rate in [(2, 2*lam), (1, lam), (3, lam)]:
            generator[state, state ^ toggle] += rate
            generator[state, state] -= rate
    P, Ptail = expm(generator*round_us), expm(generator*tail_us)

    def average_map_error(R, assign, erase, tail):
        emissions = []
        for o1, o2 in itertools.product([0, 1, 2], repeat=2):
            row = []
            for state in range(4):
                bits = (state//2, state % 2)
                likelihood = 1.0
                for observed, bit in zip((o1, o2), bits):
                    likelihood *= erase if observed == 2 else (1-erase)*(
                        (1-assign) if observed == bit else assign)
                row.append(likelihood)
            emissions.append(row)
        E = np.array(emissions)
        joint = np.full((1, 4), 0.25)
        for _ in range(R):
            prior = joint @ P
            joint = (prior[:, None, :] * E[None, :, :]).reshape((-1, 4))
        joint = joint @ tail
        return float(joint.sum() - joint.max(axis=1).sum())

    rows = [{"rounds": R, "factory_verification_plus_tail_us": R*round_us+tail_us,
             "mean_final_syndrome_MAP_error": average_map_error(R, q, erasure, Ptail),
             "same_checks_but_no_unobserved_tail": average_map_error(R, q, erasure, np.eye(4)),
             "perfect_records_with_same_tail": average_map_error(R, 0.0, 0.0, Ptail)}
            for R in [1, 2, 3, 4, 5]]
    tail_floor = float(1-Ptail[0].max())
    assert max(abs(row["perfect_records_with_same_tail"]-tail_floor) for row in rows) < 1e-12
    return {"effective_classical_model_only": True,
            "assumptions": {"per_cat_Z_rate_per_us": lam, "round_us": round_us,
                "unobserved_tail_us": tail_us, "assignment_error_each_check": q,
                "erasure_probability_each_check": erasure,
                "each_round_checks_both_stabilizers": True,
                "X_faults_are_invisible_to_these_checks": True},
            "exact_perfect_record_tail_floor": tail_floor, "rows": rows}


def main():
    cases = [
        parity_meter_case("matched_f_to_e_and_dephasing"),
        parity_meter_case("f_to_e_frequency_mismatch", delta_e=[.04, -.02, .03, -.01]),
        parity_meter_case("mapping_area_mismatch", delta_f=[.01, -.02, .015, -.005],
                          delta_e=[.01, -.02, .015, -.005]),
        parity_meter_case("double_decay_allowed", gamma_e=.11),
        parity_meter_case("data_dependent_decay_rate", rate_spread=.10),
    ]
    cnot = verify_cnot_teleportation()
    result = {"instrument_cases": cases, "cnot_teleportation": cnot,
              "resource_frontier": resource_frontier(),
              "noisy_factory_frontier": noisy_factory_frontier()}
    assert cases[0]["max_intrasector_instrument_scalar_defect"] < 1e-12
    assert cases[0]["max_no_click_kraus_scalar_defect"] < 1e-12
    assert cases[0]["max_intrasector_unconditional_coherence_loss"] < 1e-12
    assert all(c["trace_preservation_error"] < 1e-12 for c in cases)
    assert all(c["max_intrasector_instrument_scalar_defect"] > 1e-6 for c in cases[1:])
    assert cnot["branches_checked"] == 256
    assert cnot["max_corrected_branch_operator_error"] < 1e-12
    assert cnot["completeness_error"] < 1e-12
    assert cnot["physical_Z_fault_non_Z_defect"] < 1e-12
    (HERE / "results.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"instrument_cases": cases, "cnot_teleportation": cnot}, indent=2))
    print("Resource arithmetic written to", HERE / "results.json")


if __name__ == "__main__":
    main()
