#!/usr/bin/env python3
"""Exact/algebraic checks accompanying n09_glass_marginality/v1.txt.

This is not a glass simulation and supplies no empirical confirmation. It checks
the quartic-jet change of variables, the local barrier asymptotic, and the
conditional elastic/multipole power counts recorded in v1.txt.
Uses only the Python standard library.
"""

from itertools import permutations
from math import sqrt


def det(matrix):
    n = len(matrix)
    total = 0.0
    for perm in permutations(range(n)):
        inversions = sum(
            perm[i] > perm[j] for i in range(n) for j in range(i + 1, n)
        )
        term = (-1.0) ** inversions
        for row, col in enumerate(perm):
            term *= matrix[row][col]
        total += term
    return total


def inverse_jet(s, kappa, tau, chi):
    return (
        -kappa * s + tau * s**2 / 2.0 - chi * s**3 / 6.0,
        kappa - tau * s + chi * s**2 / 2.0,
        tau - chi * s,
        chi,
    )


def jet_jacobian(s, kappa, tau, chi):
    return [
        [-kappa + tau * s - chi * s**2 / 2.0, -s, s**2 / 2.0, -s**3 / 6.0],
        [-tau + chi * s, 1.0, -s, s**2 / 2.0],
        [-chi, 0.0, 1.0, -s],
        [0.0, 0.0, 0.0, 1.0],
    ]


def potential(y, kappa, tau, chi):
    return kappa * y**2 / 2.0 + tau * y**3 / 6.0 + chi * y**4 / 24.0


def stationary_nonzero_roots(kappa, tau, chi):
    discriminant = 9.0 * tau**2 - 24.0 * kappa * chi
    if discriminant < 0.0:
        return ()
    root = sqrt(discriminant)
    return ((-3.0 * tau + root) / (2.0 * chi),
            (-3.0 * tau - root) / (2.0 * chi))


def exponents(base_curvature_power=1.0, selection_power=0.0, tau_power=0.0):
    beta_unrestricted = 2.0 * (base_curvature_power + selection_power) + 1.0
    beta_lowest_quartic = (
        2.0 * base_curvature_power
        + 2.0 * selection_power
        + tau_power
        + 2.0
    )
    return beta_unrestricted, beta_lowest_quartic


def main():
    for s, kappa, tau, chi in ((0.3, 0.7, -0.2, 1.4),
                               (-1.1, 0.05, 0.8, 2.0),
                               (2.0, 3.0, 1.5, 0.4)):
        assert inverse_jet(s, kappa, tau, chi)[3] == chi
        assert abs(abs(det(jet_jacobian(s, kappa, tau, chi))) - kappa) < 1e-10

    print("quartic-jet Jacobian: |det| = kappa for three nonsingular checks")

    tau, chi = 1.0, 1.0
    print("fragile-well barrier check (tau=chi=1):")
    for kappa in (1e-2, 1e-3, 1e-4, 1e-5):
        saddle, lower_minimum = stationary_nonzero_roots(kappa, tau, chi)
        # The root closer to zero is the intervening saddle for positive tau.
        assert potential(saddle, kappa, tau, chi) > 0.0
        assert potential(lower_minimum, kappa, tau, chi) < 0.0
        ratio = potential(saddle, kappa, tau, chi) / kappa**3
        print(f"  kappa={kappa:.0e}: B/kappa^3={ratio:.9f}; limit=2/3")

    beta3, beta4 = exponents()
    assert beta3 == 3.0 and beta4 == 4.0
    print(f"smooth-jet predictions: unrestricted beta={beta3:.0f}; "
          f"quartic-lowest gate beta={beta4:.0f}")

    d, multipole_order = 3, 2
    phonon_power = d - 1 + 2 * multipole_order
    width_power = d - 1
    relative_width_power = d - 2
    assert phonon_power == 6 and width_power == 2 and relative_width_power == 1
    print("conditional 3D dipole-bath checks: quadrupole phonon weight ~omega^6; "
          "resonance width ~omega^2; relative width ~omega")

    print("fold basin counterexample, initial interval [-L,L], L=1:")
    for kappa in (1e-1, 1e-2, 1e-3):
        sqrt_mu = kappa / 2.0
        basin_length = 1.0 + sqrt_mu
        print(f"  kappa={kappa:.0e}: basin length={basin_length:.6f} -> 1, "
              "not proportional to kappa")

    print("all algebraic diagnostics passed; no empirical glass data were used")


if __name__ == "__main__":
    main()
