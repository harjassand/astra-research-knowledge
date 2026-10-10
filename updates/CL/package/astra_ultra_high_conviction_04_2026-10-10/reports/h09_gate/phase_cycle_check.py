"""Port-only three-tone finite-amplitude extraction of one H3 value.

This is a numerical interface check, not a physical experiment or noise study.
It integrates a small damped cubic oscillator from rest, uses eight sign-cycle
runs to take the mixed amplitude derivative, and compares with the analytic
third-order Volterra coefficient.
"""
import json
from pathlib import Path

import numpy as np


OUT = Path(__file__).resolve().parent
n = 3
e1 = np.eye(n)[:, 0]
rng = np.random.default_rng(915)
U, _ = np.linalg.qr(rng.normal(size=(n, n)))
# Fix mode signs only; this does not affect K.
U *= np.sign(U[0, :])[None, :]
lam = np.array([1.0, 2.25, 4.0])
K = (U * lam) @ U.T
alpha = np.array([0.20, 0.25, 0.30])
gamma = 0.50

# All tones are on the 0.1 rad/s grid. The target combination is
# 2.5 - 2.3 + 0.6 = 0.8 rad/s; the eight signed triplets have no other
# third-order collision at the target.
w1, w2, w3, ws = 2.5, 2.3, 0.6, 0.8
phase = np.array([0.31, -0.27, 0.52])
period = 2 * np.pi / 0.1
steps_per_period = 8192
dt = period / steps_per_period
total_periods = 3
collect_start = 2 * steps_per_period


def q(s):
    return np.linalg.solve((s * s + gamma * s) * np.eye(n) + K, e1)


s1, s2, s3 = 1j * w1, -1j * w2, 1j * w3
analytic_h3 = -np.sum(alpha * q(1j * ws) * q(s1) * q(s2) * q(s3))
expected = (3 / 4) * analytic_h3 * np.exp(1j * (phase[0] - phase[1] + phase[2]))


def rhs(state, time, amps):
    x, v = state[:n], state[n:]
    u = sum(amps[j] * np.cos(freq * time + phase[j])
            for j, freq in enumerate((w1, w2, w3)))
    return np.r_[v, -gamma * v - K @ x - alpha * x**3 + e1 * u]


def one_run(amps):
    state = np.zeros(2 * n)
    y = np.empty(steps_per_period)
    for k in range(total_periods * steps_per_period):
        t = k * dt
        a = rhs(state, t, amps)
        b = rhs(state + 0.5 * dt * a, t + 0.5 * dt, amps)
        c = rhs(state + 0.5 * dt * b, t + 0.5 * dt, amps)
        d = rhs(state + dt * c, t + dt, amps)
        state += (dt / 6) * (a + 2 * b + 2 * c + d)
        if k >= collect_start:
            y[k - collect_start] = state[0]
    # The state stored at loop index k is the post-step value at (k+1)*dt.
    t = (collect_start + 1 + np.arange(steps_per_period)) * dt
    return np.mean(y * np.exp(-1j * ws * t))


def mixed_cubic(amplitude):
    total = 0j
    for mask in range(8):
        signs = np.array([1 if (mask >> j) & 1 else -1 for j in range(3)])
        total += np.prod(signs) * one_run(signs * amplitude)
    return total / (8 * amplitude**3)


rows = []
measured_by_rho = {}
for rho in (0.10, 0.05, 0.025):
    measured = mixed_cubic(rho)
    measured_by_rho[rho] = measured
    # The mixed derivative is (3/4) H3 times the phase signature for cosine
    # input components. The ratio should approach 1 as rho tends to zero.
    rows.append({
        "rho": rho,
        "measured_mixed_coefficient": [measured.real, measured.imag],
        "expected_cubic_coefficient": [expected.real, expected.imag],
        "relative_error": float(abs(measured - expected) / abs(expected)),
    })

# Two-scale Richardson extrapolation cancels the leading fifth-order response:
# M(rho)=C3+C5*rho^2+O(rho^4).
richardson = (4 * measured_by_rho[0.05] - measured_by_rho[0.10]) / 3

result = {
    "disclosure": __doc__.strip(),
    "n": n,
    "gamma": gamma,
    "frequencies_rad_s": [w1, w2, w3, ws],
    "phase_signature": [1, -1, 1],
    "eight_run_sign_cycle_per_amplitude": True,
    "settling_periods": 2,
    "collected_periods": 1,
    "analytic_H3": [analytic_h3.real, analytic_h3.imag],
    "expected_cosine_input_coefficient": [expected.real, expected.imag],
    "results": rows,
    "richardson_rho_0.05_0.10": {
        "coefficient": [richardson.real, richardson.imag],
        "relative_error": float(abs(richardson - expected) / abs(expected)),
    },
}
(OUT / "phase_cycle_results.json").write_text(json.dumps(result, indent=2))
print(json.dumps(result, indent=2))
