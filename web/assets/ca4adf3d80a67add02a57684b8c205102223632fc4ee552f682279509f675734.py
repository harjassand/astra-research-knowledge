#!/usr/bin/env python3
"""Pure-Python Fourier check for the high-frequency shear cell equation.

No third-party packages are required.  The cell equation is

    Psi_t = alpha Psi_zz - i q sin(z) Psi,  Psi(z,0)=1,

on the 2-pi torus.  Fourier truncation plus RK4 checks the exact energy
identity and the small-alpha / large-alpha dissipation asymptotics used in
v1.txt.  This verifies the reduced linear PDE, not a turbulent-flow claim.
"""

from __future__ import annotations

import math


def rhs(c: list[complex], modes: list[int], alpha: float, q: float) -> list[complex]:
    out = [0j] * len(c)
    for j, m in enumerate(modes):
        value = -alpha * m * m * c[j]
        if j + 1 < len(c):
            value += 0.5 * q * c[j + 1]
        if j > 0:
            value -= 0.5 * q * c[j - 1]
        out[j] = value
    return out


def add_scaled(a: list[complex], b: list[complex], scale: float) -> list[complex]:
    return [x + scale * y for x, y in zip(a, b)]


def norm2(c: list[complex]) -> float:
    return sum(z.real * z.real + z.imag * z.imag for z in c)


def gradient_norm2(c: list[complex], modes: list[int]) -> float:
    return sum(m * m * (z.real * z.real + z.imag * z.imag)
               for m, z in zip(modes, c))


def solve(alpha: float, q: float, time: float, cutoff: int = 20) -> tuple[float, float, float]:
    modes = list(range(-cutoff, cutoff + 1))
    c = [0j] * len(modes)
    c[cutoff] = 1.0 + 0j
    if time == 0.0:
        return 1.0, 0.0, 0.0

    # The diffusion operator has largest retained rate alpha*cutoff^2.
    # The extra q bound controls the skew multiplication term.
    dt_limit = min(0.002, 0.18 / max(alpha * cutoff * cutoff, 1.0),
                   0.08 / max(abs(q), 1.0))
    steps = max(1, math.ceil(time / dt_limit))
    dt = time / steps
    diss_integral = 0.0
    g_old = gradient_norm2(c, modes)

    for _ in range(steps):
        k1 = rhs(c, modes, alpha, q)
        k2 = rhs(add_scaled(c, k1, dt / 2), modes, alpha, q)
        k3 = rhs(add_scaled(c, k2, dt / 2), modes, alpha, q)
        k4 = rhs(add_scaled(c, k3, dt), modes, alpha, q)
        c = [z + (dt / 6) * (a + 2 * b + 2 * d + e)
             for z, a, b, d, e in zip(c, k1, k2, k3, k4)]
        g_new = gradient_norm2(c, modes)
        diss_integral += 0.5 * dt * (g_old + g_new)
        g_old = g_new

    energy = norm2(c)
    # PDE identity: 1 - ||Psi(t)||_2^2 = 2 alpha int_0^t ||Psi_z||_2^2 ds.
    identity_rhs = 2 * alpha * diss_integral
    return energy, identity_rhs, abs((1.0 - energy) - identity_rhs)


def main() -> None:
    q = 2.0
    time = 0.5
    alphas = [0.0, 0.02, 0.1, 0.5, 1.0, 5.0, 100.0]
    print("alpha, scalar_dissipation, identity_residual, asymptotic_reference")
    for alpha in alphas:
        energy, diss, residual = solve(alpha, q, time, cutoff=20)
        chi = (1.0 - energy) / 4.0
        if 0.0 < alpha <= 0.1:
            reference = alpha * q * q * time**3 / 12.0
        elif alpha >= 100.0:
            reference = q * q * time / (4.0 * alpha)
        else:
            reference = float("nan")
        print(f"{alpha:.6g}, {chi:.12g}, {residual:.3e}, {reference:.12g}")

    # A truncation check at the matched finite-dissipation point.
    alpha = 0.5
    coarse = solve(alpha, q, time, cutoff=16)[0]
    fine = solve(alpha, q, time, cutoff=24)[0]
    print(f"cutoff_check_abs_energy_difference={abs(coarse - fine):.3e}")

    no_shear_energy = solve(0.5, 0.0, time, cutoff=12)[0]
    print(f"zero_shear_cell_energy={no_shear_energy:.12g}")

    # The first nonzero term is chi = alpha*q^2*t^3/12 + O(t^4).
    alpha = 0.7
    q_small = 1.3
    t_small = 0.004
    energy, _, residual = solve(alpha, q_small, t_small, cutoff=12)
    measured = (1.0 - energy) / 4.0
    predicted = alpha * q_small * q_small * t_small**3 / 12.0
    print(f"small_time_measured={measured:.12g}")
    print(f"small_time_leading_term={predicted:.12g}")
    print(f"small_time_relative_error={abs(measured-predicted)/predicted:.3e}")
    print(f"small_time_identity_residual={residual:.3e}")


if __name__ == "__main__":
    main()
