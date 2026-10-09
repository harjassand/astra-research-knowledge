#!/usr/bin/env python3
"""Synthetic checks for N21's intervention-identification calculation.

These calculations are not observations or a calibrated Earth model. Requires NumPy.
"""

from __future__ import annotations

import numpy as np


def rk4_ramp_feedback(b: float, dt: float = 0.01) -> tuple[np.ndarray, float, float]:
    """3-box energy-balanced EBM; return eigenvalues, TCR-like mean, max budget residual."""
    cs, cd, lam, kappa, tau = 8.0, 100.0, 1.3, 0.7, 300.0
    f_2x = 3.9
    t_2x = float(np.log(2.0) / np.log(1.01))
    t_end = t_2x + 10.0
    a = np.array(
        [
            [-(lam + kappa) / cs, kappa / cs, b / cs],
            [kappa / cd, -kappa / cd, 0.0],
            [1.0 / tau, 0.0, -1.0 / tau],
        ],
        dtype=float,
    )
    forcing_direction = np.array([1.0 / cs, 0.0, 0.0])
    eig = np.linalg.eigvals(a)
    x = np.zeros(3)
    mean_values: list[float] = []
    max_budget_residual = 0.0
    nsteps = round(t_end / dt)

    def derivative(t: float, state: np.ndarray) -> np.ndarray:
        forcing = f_2x * t / t_2x
        return a @ state + forcing_direction * forcing

    for i in range(nsteps):
        t = i * dt
        k1 = derivative(t, x)
        k2 = derivative(t + dt / 2, x + dt * k1 / 2)
        k3 = derivative(t + dt / 2, x + dt * k2 / 2)
        k4 = derivative(t + dt, x + dt * k3)
        x += (dt / 6) * (k1 + 2 * k2 + 2 * k3 + k4)

        # Directly check C_s*Tdot_s + C_d*Tdot_d = F-lambda*T_s+b*z.
        f_now = f_2x * (t + dt) / t_2x
        dx_now = derivative(t + dt, x)
        lhs = cs * dx_now[0] + cd * dx_now[1]
        rhs = f_now - lam * x[0] + b * x[2]
        max_budget_residual = max(max_budget_residual, abs(lhs - rhs))

        if t_2x - 10.0 < t + dt <= t_2x + 10.0:
            mean_values.append(float(x[0]))

    return eig, float(np.mean(mean_values)), max_budget_residual


def randomized_input_check(seed: int = 21, n: int = 400_000, max_lag: int = 8) -> None:
    """Recover a hidden-state impulse response by cross-covariance with white input."""
    rng = np.random.default_rng(seed)
    a = np.array([[0.94, 0.04], [0.01, 0.985]])
    b = np.array([0.10, 0.005])
    c = np.array([1.0, 0.0])
    noise_scale = np.array([0.12, 0.025])
    u = rng.choice(np.array([-1.0, 1.0]), size=n)
    w = rng.normal(size=(n, 2)) * noise_scale
    x = np.zeros((n + 1, 2))
    for t in range(n):
        x[t + 1] = a @ x[t] + b * u[t] + w[t]
    y = (x @ c)[1:]
    burn = 2_000
    u = u[burn:]
    y = y[burn:]
    u -= u.mean()
    y -= y.mean()
    var_u = float(np.mean(u * u))

    print("randomized input check (lag, exact G, cross-covariance estimate)")
    a_power = np.eye(2)
    for lag in range(1, max_lag + 1):
        if lag > 1:
            a_power = a_power @ a
        exact = float(c @ a_power @ b)
        n_pairs = len(u) - lag + 1
        estimate = float(np.mean(y[lag - 1 : lag - 1 + n_pairs] * u[:n_pairs]) / var_u)
        print(f"  {lag:2d}  {exact: .7f}  {estimate: .7f}")

    # Under no intervention, B does not enter the state law. Reuse the same A,
    # innovations, and initial condition: B and 2B have exactly the same passive y.
    x0 = np.zeros(2)
    y_passive_1 = np.empty(n)
    y_passive_2 = np.empty(n)
    for t in range(n):
        x0 = a @ x0 + w[t]
        y_passive_1[t] = c @ x0
        y_passive_2[t] = c @ x0
    y_passive_2 -= y_passive_1  # exact pathwise difference under shared innovations
    print("max passive-output difference for forcing couplings B and 2B:",
          float(np.max(np.abs(y_passive_2))))
    print("causal impulse at lag 1 for B and 2B:", float(c @ b), float(c @ (2 * b)))


def main() -> None:
    cs, cd, lam, kappa, tau = 8.0, 100.0, 1.3, 0.7, 300.0
    del cs, cd, kappa, tau
    f_2x = 3.9
    means: list[float] = []
    for b in (0.0, 0.8):
        eig, tcr20, residual = rk4_ramp_feedback(b)
        means.append(tcr20)
        ecs = f_2x / (lam - b)
        times = sorted(1.0 / abs(float(ev.real)) for ev in eig if ev.real < 0)
        print(f"b={b:.1f}: ECS={ecs:.3f} K; 20-y mean={tcr20:.6f} K")
        print(f"  low-frequency restoring feedback={lam-b:.3f} W m^-2 K^-1")
        print("  decay times (years):", ", ".join(f"{v:.2f}" for v in times))
        print(f"  maximum differential budget residual={residual:.3e} W m^-2")
    print(f"20-y mean difference (b=0.8 minus b=0): {means[1]-means[0]:.6f} K")
    randomized_input_check()


if __name__ == "__main__":
    main()
