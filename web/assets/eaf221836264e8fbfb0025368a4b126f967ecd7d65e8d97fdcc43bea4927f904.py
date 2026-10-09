#!/usr/bin/env python3
"""Finite diagnostics for EIT evanescence versus wave travel-time echoes.

This is an equation check and scale illustration, not a proof or a simulated
instrument. EIT numbers use the exact 2-D radial transfer recursion; wave
numbers use the exact single-interface reflection response.
"""

from __future__ import annotations

import math


def radial_admittance(n: int, sigmas: list[float], widths: list[float]) -> float:
    """Return y_n=lambda_n/n for concentric 2-D constant-conductivity shells.

    sigmas has one more entry than widths; the final entry is the conductivity
    of the core. Widths are shell thicknesses in x=-log(r), from outside in.
    """
    if n < 1 or len(sigmas) != len(widths) + 1:
        raise ValueError("need n>=1 and len(sigmas)=len(widths)+1")
    y = sigmas[-1]
    for j in range(len(widths) - 1, -1, -1):
        s = sigmas[j]
        t = math.tanh(n * widths[j])
        y = s * (y + s * t) / (s + y * t)
    return y


def radial_reflection(n: int, sigmas: list[float], widths: list[float]) -> float:
    y = radial_admittance(n, sigmas, widths)
    s0 = sigmas[0]
    return (y - s0) / (y + s0)


def annulus_reflection(n: int, depth: float, width: float, contrast: float) -> float:
    """Exact reflection for sigma0 / sigma1 annulus / sigma0 core.

    ``contrast`` is rho=(sigma1-sigma0)/(sigma1+sigma0). The model has an
    outer sigma0 region of log-thickness ``depth``, then a sigma1 shell of
    log-thickness ``width``, then sigma0 to the center.
    """
    q = math.exp(-2 * n * width)
    return math.exp(-2 * n * depth) * contrast * (1 - q) / (1 - contrast**2 * q)


def annulus_reflection_by_transfer(
    n: int, depth: float, width: float, contrast: float
) -> float:
    """Evaluate the same annulus by the full admittance recurrence."""
    sigma0 = 1.0
    sigma1 = (1 + contrast) / (1 - contrast)
    y = radial_admittance(n, [sigma0, sigma1, sigma0], [depth, width])
    return (y - sigma0) / (y + sigma0)


def radial_peel_identity_error(n: int) -> float:
    """Check R_outer=e^(-2nd) R_inner for a three-region example."""
    s0, s1, s2 = 1.0, 2.2, 0.7
    d0, d1 = 0.38, 0.21
    y_inner = radial_admittance(n, [s1, s2], [d1])
    r_inner = (y_inner - s0) / (y_inner + s0)
    r_outer = radial_reflection(n, [s0, s1, s2], [d0, d1])
    return abs(r_outer - math.exp(-2 * n * d0) * r_inner)


def wave_difference_norm(bandwidth: float, shift: float, contrast: float) -> float:
    """Compute ||r(exp(2 i omega h)-1)||_{L2[-B,B]} by midpoint quadrature."""
    count = 200_000
    step = 2 * bandwidth / count
    total = 0.0
    for j in range(count):
        omega = -bandwidth + (j + 0.5) * step
        value = 2 * contrast * math.sin(omega * shift)
        total += value * value
    return math.sqrt(total * step)


def wave_difference_norm_asymptotic(bandwidth: float, shift: float, contrast: float) -> float:
    return math.sqrt(8.0 / 3.0) * abs(contrast) * bandwidth ** 1.5 * abs(shift)


if __name__ == "__main__":
    print("exact radial reflection identity residuals")
    for n in (1, 2, 5, 10, 20):
        print(f"n={n:2d} residual={radial_peel_identity_error(n):.3e}")

    print("\nclosed-form versus transfer for an annular perturbation")
    for n in (1, 2, 5, 10, 20):
        closed = annulus_reflection(n, 0.8, 0.06, 0.2)
        transfer = annulus_reflection_by_transfer(n, 0.8, 0.06, 0.2)
        print(f"n={n:2d} residual={abs(closed-transfer):.3e}")

    print("\nrelative EIT reflection for a single interface at log-depth d=0.8")
    contrast, depth = 0.2, 0.8
    for n in (1, 2, 5, 10, 20, 40):
        print(f"n={n:2d} |R_n|={abs(contrast) * math.exp(-2*n*depth):.6e}")

    print("\nwave phase-difference norm for B=20, |r|=0.2, h=1e-4")
    b, h, r = 20.0, 1e-4, 0.2
    exact = wave_difference_norm(b, h, r)
    approx = wave_difference_norm_asymptotic(b, h, r)
    print(f"quadrature={exact:.6e} small-shift={approx:.6e} ratio={exact/approx:.8f}")
