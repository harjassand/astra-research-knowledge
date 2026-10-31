"""Independent exact thermal-initialization audit of root's 3-mode meter.

No coherent drives are needed: for same-parity logical branches the designed
full coherent displacement is equal, so it cancels from U_-^dagger U_+.
The remaining passive-mode overlap is computed including every emitted photon.
"""
import json
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp


def one_particle_overlap(T, g=1.0, Gamma=4.0, chi=2.0):
    matrices = []
    for z in (1, -1):
        h = np.array([[0, 0, g], [0, z * chi, g], [g, g, 0]], complex)
        matrices.append(-1j * h - np.diag([0, 0, Gamma / 2]))
    Ap, Am = matrices
    L2 = np.diag([0, 0, Gamma])

    def rhs(t, y):
        Ep, Em, W = y.reshape(3, 3, 3)
        return np.array([Ap @ Ep, Am @ Em, Em.conj().T @ L2 @ Ep]).ravel()

    initial = np.array([np.eye(3), np.eye(3), np.zeros((3, 3))], complex).ravel()
    sol = solve_ivp(rhs, [0, T], initial, method="DOP853", rtol=2e-12, atol=2e-14)
    Ep, Em, W = sol.y[:, -1].reshape(3, 3, 3)
    M = Em.conj().T @ Ep + W
    return M, np.sum(abs(Ep) ** 2, axis=0), bool(sol.success)


def thermal_visibility(M, occupations):
    # Trace[rho_thermal Gamma(M)] for a passive bosonic transformation,
    # including vacuum output continua. M is its initial-mode compression.
    return 1 / np.linalg.det(np.eye(3) + np.diag(occupations) @ (np.eye(3) - M))


def warm_bath_first_order(T, g=1.0, Gamma=4.0, chi=2.0):
    """Derivative at n_input=0 from Gamma*n_input*D[m^dagger].

    Vacuum initial modes. A heating insertion at tau contributes the
    one-photon m-state overlap at T-tau minus the vacuum overlap.
    """
    h = np.array([[0, 0, g], [0, chi, g], [g, g, 0]], complex)
    Ap = -1j * h - np.diag([0, 0, Gamma / 2])
    h[1, 1] = -chi
    Am = -1j * h - np.diag([0, 0, Gamma / 2])

    def rhs(t, y):
        p, m, overlap = y[:3], y[3:6], y[6]
        return np.concatenate([Ap @ p, Am @ m,
                               [-2j * chi * m[1].conjugate() * p[1],
                                1 - overlap]])

    y = np.array([0, 0, 1, 0, 0, 1, 1, 0], complex)
    sol = solve_ivp(rhs, [0, T], y, method="DOP853", rtol=2e-12, atol=2e-14)
    J = sol.y[7, -1]
    return {"pZ_linear_coefficient_per_input_nbar": Gamma * J.real / 2,
            "phase_linear_coefficient_per_input_nbar": -Gamma * J.imag}


def main():
    rows = []
    for T in [4., 8., 12., 16.]:
        M, survival, success = one_particle_overlap(T)
        entries = []
        for nbar in [0.0001, 0.001, 0.01, 0.1]:
            for thermal_modes, occ in [("b,c only", [nbar, nbar, 0]),
                                       ("b,c,m", [nbar] * 3),
                                       ("m only", [0, 0, nbar])]:
                overlap = thermal_visibility(M, occ)
                entries.append({"thermal_modes": thermal_modes, "nbar": nbar,
                                "visibility": abs(overlap),
                                "coherent_local_phase": float(np.angle(overlap)),
                                "dephasing_pZ_after_phase_compensation": (1 - abs(overlap)) / 2})
        rows.append({"T": T, "g": 1., "Gamma": 4., "chi": 2.,
                     "solver_success": success,
                     "one_particle_overlap_real": M.real.tolist(),
                     "one_particle_overlap_imag": M.imag.tolist(),
                     "residual_single_particle_survival_by_initial_mode": survival.tolist(),
                     "ongoing_thermal_input_first_order": warm_bath_first_order(T),
                     "thermal_cases": entries})
    # Validate the determinant formula against exact geometric thermal weights
    # for a single populated input mode. Its k-photon overlap is M[j,j]^k.
    M, _, _ = one_particle_overlap(8.)
    nbar = 0.1
    q = nbar / (1 + nbar)
    max_residual = 0
    for j in range(3):
        exact_series = sum((1-q) * q**k * M[j, j]**k for k in range(100))
        occ = [0, 0, 0]
        occ[j] = nbar
        max_residual = max(max_residual, abs(exact_series - thermal_visibility(M, occ)))
    out = {"description": "Thermal initial populations, vacuum Markov output; no ongoing heating.",
           "single_thermal_mode_geometric_series_residual": max_residual,
           "cases": rows}
    Path(__file__).with_name("thermal_mediator_results.json").write_text(json.dumps(out, indent=2) + "\n")
    for row in rows:
        print("T", row["T"], "residual survival", row["residual_single_particle_survival_by_initial_mode"])
        print("Warm bath", row["ongoing_thermal_input_first_order"])
        for case in row["thermal_cases"]:
            if case["nbar"] in [0.001, 0.01]:
                print(case)
    print("Geometric-series check", max_residual)


if __name__ == "__main__":
    main()
