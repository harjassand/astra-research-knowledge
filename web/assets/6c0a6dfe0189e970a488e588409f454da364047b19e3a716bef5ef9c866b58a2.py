#!/usr/bin/env python3
"""Finite-particle checks for the nonreciprocal COM-force identity.

This is an algebra/numerics check for a specified short-range pair kernel,
not a simulation of phase separation and not empirical evidence.
"""

from cmath import exp as cexp
from math import exp, pi, sqrt
import json


def grad_ua(r, epsilon=1.0, ell=1.0):
    """Derivative of U_a(r) = epsilon exp(-r^2/(2 ell^2))."""
    return -epsilon * r / (ell * ell) * exp(-0.5 * (r / ell) ** 2)


def nonreciprocal_com_force(xa, xb, epsilon=1.0, ell=1.0):
    """Sum pair forces for U_AB=U_s+U_a, U_BA=U_s-U_a.

    Reciprocal U_s cancels pairwise.  The remaining force on A and B
    together is -2 U_a'(x_A-x_B).
    """
    return sum(-2.0 * grad_ua(x - y, epsilon, ell) for x in xa for y in xb)


def direct_pair_force_sum(xa, xb, epsilon=1.0, ell=1.0):
    """Compute both members' forces explicitly, with reciprocal part zero."""
    force = 0.0
    for x in xa:
        for y in xb:
            r = x - y
            # Force on A from B: -U_AB'(r) = -U_a'(r).
            force += -grad_ua(r, epsilon, ell)
            # Force on B from A: +U_BA'(r) = -U_a'(r).
            force += -grad_ua(r, epsilon, ell)
    return force


def periodized_grad_ua(r, L, epsilon=1.0, ell=1.0):
    """Derivative of the periodized Gaussian on a ring of length L."""
    return sum(grad_ua(r + n * L, epsilon, ell) for n in range(-3, 4))


def periodic_direct_force(xa, xb, L, epsilon=1.0, ell=1.0):
    return sum(-2.0 * periodized_grad_ua(x - y, L, epsilon, ell)
               for x in xa for y in xb)


def periodic_spectral_force(xa, xb, L, epsilon=1.0, ell=1.0, nmax=80):
    """Fourier form of -2 sum_AB U_a'(x_A-x_B), with periodized U_a."""
    total = 0.0
    for n in range(1, nmax + 1):
        k = 2.0 * pi * n / L
        uhat = epsilon * sqrt(2.0 * pi) * ell * exp(-0.5 * ell * ell * k * k)
        ahat = sum(cexp(-1j * k * x) for x in xa)
        bhat = sum(cexp(-1j * k * x) for x in xb)
        total += k * uhat * (ahat * bhat.conjugate()).imag
    return -4.0 * total / L


def interface_positions(R, spacing=0.2, gap=0.0):
    """Two flat 1D slabs meeting at one unlike-species interface."""
    n = round(R / spacing)
    xa = [-spacing / 2.0 - i * spacing for i in range(n)]
    xb = [gap + spacing / 2.0 + i * spacing for i in range(n)]
    return xa, xb, n * spacing


def main():
    # Identity check on a deliberately irregular configuration.
    xa = [-1.3, -0.2, 0.8]
    xb = [-0.7, 0.4, 1.9, 2.3]
    identity_error = abs(
        nonreciprocal_com_force(xa, xb) - direct_pair_force_sum(xa, xb)
    )

    # Check the continuum Fourier identity against the exact periodic pair sum.
    L = 12.0
    ring_a = [i * L / 12.0 for i in range(12)]
    phase = 0.23
    ring_b = [(x + phase) % L for x in ring_a]
    periodic_force = periodic_direct_force(ring_a, ring_b, L)
    spectral_force = periodic_spectral_force(ring_a, ring_b, L)
    reversed_b = [(x - phase) % L for x in ring_a]
    reversed_force = periodic_direct_force(ring_a, reversed_b, L)

    rows = []
    for requested_R in (2, 4, 8, 16, 32):
        xa, xb, R = interface_positions(requested_R)
        force = nonreciprocal_com_force(xa, xb)
        N = len(xa) + len(xb)
        speed = force / N  # unit drag coefficient
        rows.append({
            "R": R,
            "N": N,
            "nonreciprocal_force": force,
            "rigid_COM_speed": speed,
            "R_times_speed": R * speed,
        })

    # Mirror the interface.  Since U_a' is odd, the force must reverse.
    xa, xb, _ = interface_positions(16)
    force = nonreciprocal_com_force(xa, xb)
    mirror_force = nonreciprocal_com_force([-x for x in xa], [-x for x in xb])

    print(json.dumps({
        "identity_error": identity_error,
        "mirror_force_sum": force + mirror_force,
        "periodic_spectral_error": abs(periodic_force - spectral_force),
        "phase_lag_force": periodic_force,
        "reversed_phase_lag_force": reversed_force,
        "phase_reversal_sum": periodic_force + reversed_force,
        "interface_scaling": rows,
        "status": "finite algebraic check; no phase-separation dynamics or empirical confirmation",
    }, indent=2))


if __name__ == "__main__":
    main()
