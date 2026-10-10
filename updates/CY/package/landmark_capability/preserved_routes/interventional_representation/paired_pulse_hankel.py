#!/usr/bin/env python3
"""Small exact-data demonstration of paired pulse/sham Hankel realization.

Requires NumPy. This is an illustrative finite fixture, not empirical evidence
about physical systems or a noisy-data guarantee.
"""

from __future__ import annotations

import numpy as np


def run_system(A: np.ndarray, B: np.ndarray, C: np.ndarray, D: float,
               x0: np.ndarray, inputs: np.ndarray) -> np.ndarray:
    """Return y[0:T] for x[t+1]=A x[t]+B u[t], y[t]=C x[t]+D u[t]."""
    x = np.array(x0, dtype=float, copy=True)
    ys = []
    for u in inputs:
        ys.append(float((C @ x).item() + D * u))
        x = A @ x + B[:, 0] * u
    return np.asarray(ys)


def paired_pulse_realization(y_pulse: np.ndarray, y_sham: np.ndarray,
                             rank: int) -> tuple[np.ndarray, np.ndarray,
                                                 np.ndarray, float, np.ndarray,
                                                 np.ndarray]:
    """Recover a rank-r minimal realization and same-start initial state."""
    r = rank
    delta = y_pulse - y_sham
    # delta[0] is D; delta[j+1] is C A^j B.
    markov = delta[1:2 * r + 1]
    H0 = np.fromfunction(lambda i, j: markov[i.astype(int) + j.astype(int)],
                         (r, r), dtype=int)
    H1 = np.fromfunction(lambda i, j: markov[i.astype(int) + j.astype(int) + 1],
                         (r, r), dtype=int)
    U, singular_values, Vt = np.linalg.svd(H0, full_matrices=False)
    U = U[:, :r]
    s = singular_values[:r]
    Vt = Vt[:r, :]
    O = U * np.sqrt(s)[None, :]
    R = np.sqrt(s)[:, None] * Vt
    Ahat = np.linalg.pinv(O) @ H1 @ np.linalg.pinv(R)
    Bhat = R[:, 0:1]
    Chat = O[0:1, :]
    Dhat = float(delta[0])
    # The sham run also identifies the initial state in the learned coordinates.
    xhat0 = np.linalg.lstsq(O[:r, :], y_sham[:r], rcond=None)[0]
    return Ahat, Bhat, Chat, Dhat, xhat0, singular_values


def main() -> None:
    # A stable, controllable, observable third-order scalar system.
    A = np.array([[0.55, 0.10, 0.00],
                  [0.00, 0.35, 0.08],
                  [0.00, 0.00, 0.20]])
    B = np.array([[1.00], [0.30], [0.20]])
    C = np.array([[0.70, -0.40, 0.90]])
    D = 0.07
    x0 = np.array([0.4, -0.2, 0.1])
    r = 3
    horizon = 2 * r + 1  # outputs t=0,...,2r include the last H1 entry.

    pulse_inputs = np.zeros(horizon)
    pulse_inputs[0] = 1.0
    sham_inputs = np.zeros(horizon)
    y_pulse = run_system(A, B, C, D, x0, pulse_inputs)
    y_sham = run_system(A, B, C, D, x0, sham_inputs)

    Ahat, Bhat, Chat, Dhat, xhat0, hankel_singular_values = \
        paired_pulse_realization(y_pulse, y_sham, r)

    rng = np.random.default_rng(20261010)
    heldout_inputs = rng.uniform(-0.8, 0.8, size=250)
    y_true = run_system(A, B, C, D, x0, heldout_inputs)
    y_learned = run_system(Ahat, Bhat, Chat, Dhat, xhat0, heldout_inputs)
    max_abs_error = float(np.max(np.abs(y_true - y_learned)))

    # Passive zero-input data cannot separate any two zero-start systems.
    zero_state = np.zeros(3)
    passive_a = run_system(A, B, C, D, zero_state, sham_inputs)
    A_alt = np.diag([0.15, 0.45, 0.70])
    B_alt = np.array([[0.2], [0.5], [0.9]])
    C_alt = np.array([[1.3, -0.1, 0.7]])
    passive_b = run_system(A_alt, B_alt, C_alt, -0.4, zero_state, sham_inputs)
    alt_pulse = run_system(A_alt, B_alt, C_alt, -0.4, zero_state, pulse_inputs)
    true_zero_start_pulse = run_system(A, B, C, D, zero_state, pulse_inputs)

    # Near-cancelling modes expose the precision limit: the two-state system is
    # minimal for delta>0, but its whole measured impulse response shrinks with
    # delta, making fixed-noise acquisition sample-hungry.
    print("paired pulse/sham Hankel realization (exact arithmetic fixture)")
    print(f"true order: {r}; recovered Hankel rank: "
          f"{int(np.sum(hankel_singular_values > 1e-10))}")
    print("Hankel singular values:", np.array2string(hankel_singular_values,
                                                     precision=6))
    print(f"held-out 250-step max absolute output error: {max_abs_error:.3e}")
    print(f"acquisition: 2 resets, 1 unit pulse, {2 * horizon} scalar readings")
    print(f"passive zero-input records distinguish alternatives: "
          f"{not np.allclose(passive_a, passive_b)}")
    print(f"pulse records distinguish alternatives: "
          f"{not np.allclose(true_zero_start_pulse, alt_pulse)}")
    for delta in (1e-1, 1e-2, 1e-3):
        A_near = np.diag([0.5, 0.5 + delta])
        B_near = np.ones((2, 1))
        C_near = np.array([[1.0, -1.0]])
        vals = np.array([float((C_near @ np.linalg.matrix_power(A_near, k)
                               @ B_near).item()) for k in range(6)])
        print(f"near-cancel delta={delta:g}: max |first 6 Markov params|="
              f"{np.max(np.abs(vals)):.3e}")
    if max_abs_error > 1e-9:
        raise SystemExit("fixture reconstruction failed its held-out simulation")


if __name__ == "__main__":
    main()
