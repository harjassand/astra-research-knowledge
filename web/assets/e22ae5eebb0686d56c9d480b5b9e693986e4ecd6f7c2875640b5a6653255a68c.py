"""Finite three-angle fast-flavor first-pulse diagnostic.

This is an internal mean-field computation, not an astrophysical simulation.
It checks whether a single unstable mode produces a seed-independent first
nonlinear conversion pulse after removing its logarithmic onset delay.
"""

import numpy as np


V = np.array([-1.0, 1.0 / 3.0, 1.0])
G = np.array([-4.0, -4.0, 1.0])


def rhs(_t, flat):
    p = flat.reshape(3, 3)
    d0 = p.sum(axis=0)
    d1 = (V[:, None] * p).sum(axis=0)
    return np.cross(d0[None, :] - V[:, None] * d1[None, :], p).ravel()


def conversion(p):
    # Charge-balanced flip amount, zero initially; the total z lepton charge
    # makes the positive- and negative-G sector conversions equal.
    return 0.5 * np.sum(np.abs(G) - np.sign(G) * p[:, 2])


def rk4_step(t, y, h):
    k1 = rhs(t, y)
    k2 = rhs(t + h / 2.0, y + h * k1 / 2.0)
    k3 = rhs(t + h / 2.0, y + h * k2 / 2.0)
    k4 = rhs(t + h, y + h * k3)
    return y + h * (k1 + 2 * k2 + 2 * k3 + k4) / 6.0


def main():
    d1z = float(V @ G)
    # q_i = P_i^x+iP_i^y.  In the frame corotating with D_0^z,
    # qdot_i = -i v_i D_1^z q_i - i G_i sum_j q_j
    #          + i v_i G_i sum_j v_j q_j.
    a = (
        -1j * np.diag(V * d1z)
        - 1j * np.diag(G) @ np.ones((len(G), len(G)))
        + 1j * np.outer(V * G, V)
    )
    eigvals, eigvecs = np.linalg.eig(a)
    j = int(np.argmax(eigvals.real))
    lam = eigvals[j]
    q = eigvecs[:, j]
    q /= np.max(np.abs(q))
    gamma = float(lam.real)
    if gamma <= 0:
        raise RuntimeError(f"No unstable mode found: {eigvals}")

    # Include a global-rotation neutral vector and the stable eigenvector as
    # seed contamination.  They are O(epsilon) at t=0 and disappear from the
    # first-pulse limit after the logarithmic shift.
    neutral = G.astype(complex) / np.max(np.abs(G))
    neutral_index = int(np.argmin(np.abs(eigvals.real)))
    stable_index = int(np.argmin(eigvals.real))
    stable = eigvecs[:, stable_index]
    stable /= np.max(np.abs(stable))
    seeds = (
        ("pure", 1.0 + 0.0j, 0.0j, 0.0j),
        ("phase_and_neutral", 0.3 * np.exp(0.7j), 0.7 + 0.2j, 0.0j),
        ("phase_and_stable", 0.6 * np.exp(-1.1j), 0.0j, 0.8 - 0.1j),
    )
    taus = np.linspace(-2.0, 8.0, 2001)
    peak_offset = np.log(4.0 * np.sqrt(2.0)) / gamma
    predicted_pulse = 2.0 / np.cosh(gamma * (taus - peak_offset)) ** 2
    report = []
    curves = {}
    for seed_name, alpha, beta, delta in seeds:
      for eps in (1e-3, 1e-4, 1e-5):
        unstable_amplitude = eps * abs(alpha)
        onset = np.log(1.0 / unstable_amplitude) / gamma
        initial_transverse = eps * (alpha * q + beta * neutral + delta * stable)
        if np.max(np.abs(initial_transverse)) >= np.min(np.abs(G)):
            raise RuntimeError("Seed is too large to preserve the beam lengths")
        z0 = np.sign(G) * np.sqrt(G**2 - np.abs(initial_transverse) ** 2)
        p0 = np.column_stack(
            (initial_transverse.real, initial_transverse.imag, z0)
        )
        # Starting exactly at tau=-2 means t=onset-2; integrate through the
        # nonlinear pulse in onset-shifted time.
        t0 = onset + taus[0]
        if t0 <= 0:
            raise RuntimeError("Chosen tau window starts before physical t=0")
        final_time = onset + taus[-1]
        nsteps = int(np.ceil(final_time / 0.001))
        h = final_time / nsteps
        times = np.linspace(0.0, final_time, nsteps + 1)
        history = np.empty((nsteps + 1, 9))
        history[0] = p0.ravel()
        state = p0.ravel()
        for n in range(nsteps):
            state = rk4_step(times[n], state, h)
            history[n + 1] = state
        targets = onset + taus
        p = np.column_stack(
            [np.interp(targets, times, history[:, k]) for k in range(9)]
        ).reshape(len(taus), 3, 3)
        c = np.array([conversion(frame) for frame in p])
        curves[(seed_name, eps)] = c
        imax = int(np.argmax(c))
        report.append(
            {
                "seed": seed_name,
                "epsilon": eps,
                "onset_time": onset,
                "peak_tau": float(taus[imax]),
                "peak_conversion": float(c[imax]),
                "z_at_peak": p[imax, :, 2].tolist(),
                "d0_error": float(np.max(np.abs(p.sum(axis=1) - p[0].sum(axis=0)))),
                "length_error": float(
                    np.max(np.abs(np.linalg.norm(p, axis=2) - np.linalg.norm(p[0], axis=1)))
                ),
            }
        )

    reference = curves[("pure", 1e-5)]
    pairwise = {
        key: float(np.max(np.abs(curve - reference)))
        for key, curve in curves.items()
        if key != ("pure", 1e-5)
    }
    print(f"D1z={d1z:.12g}; unstable eigenvalue={lam}; gamma={gamma:.12g}")
    print(f"unstable eigenvector={q}; sum={sum(q)}")
    print(f"neutral eigenvalue={eigvals[neutral_index]}; stable eigenvalue={eigvals[stable_index]}")
    print(f"predicted logarithmic-shift peak offset={peak_offset:.12g}")
    for row in report:
        print(row)
    print(f"max shifted-conversion differences vs pure eps=1e-5: {pairwise}")
    print(
        "max absolute error versus first-pulse law for pure eps=1e-5: "
        f"{np.max(np.abs(reference - predicted_pulse)):.12g}"
    )


if __name__ == "__main__":
    main()
