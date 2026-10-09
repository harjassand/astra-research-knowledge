#!/usr/bin/env python3
"""Exact-rational check of the hidden-shear Euler counterexample.

The analytic proof is in ../34_unconventional.txt.  Here the periodic box is
T^3 = [0,2pi]^3 with normalized Lebesgue measure.  We set m=4, E=1,
W=2*m^2, and use frequencies n_j=m*(j+1), j=1,...,K, all invisible on
the m-point grid in y.  Fractions verify that energy and enstrophy are
exactly E and W for every K.  The square of the vorticity-at-zero lower bound
is rational, avoiding floating-point dependence in the decisive growth test.
"""

from fractions import Fraction


def row(k: int, m: int = 4, energy: Fraction = Fraction(1)) -> tuple:
    enstrophy = 2 * m * m * energy
    excess = enstrophy - m * m * energy
    freqs = [m * (j + 1) for j in range(1, k + 1)]
    reciprocal_square_sum = sum((Fraction(1, n * n) for n in freqs), Fraction(0))
    denominator = 1 - Fraction(m * m, k) * reciprocal_square_sum
    c_sq = 2 * excess / denominator
    high_energy = c_sq * reciprocal_square_sum / (2 * k)
    base_amplitude_sq = 2 * (energy - high_energy)
    actual_energy = base_amplitude_sq / 2 + high_energy
    actual_enstrophy = m * m * base_amplitude_sq / 2 + c_sq / 2
    vorticity_lower_bound_sq = c_sq * k  # |omega(0)| >= c*sqrt(k)
    return (
        freqs,
        c_sq,
        actual_energy,
        actual_enstrophy,
        vorticity_lower_bound_sq,
        base_amplitude_sq,
    )


def main() -> None:
    m = 4
    target_energy = Fraction(1)
    target_enstrophy = Fraction(2 * m * m)
    print("K, frequencies, exact_energy, exact_enstrophy, (vorticity_lower_bound)^2")
    for k in (1, 2, 4, 8, 16, 32, 64, 128):
        freqs, c_sq, e, w, omega_lb_sq, a0_sq = row(k, m, target_energy)
        assert e == target_energy
        assert w == target_enstrophy
        assert a0_sq > 0
        assert c_sq > 0
        # All grid values vanish exactly because every frequency is a multiple
        # of m: sin(n * 2*pi*l/m) = sin(2*pi*integer) = 0.
        print(f"{k}, {freqs[0]}..{freqs[-1]}, {e}, {w}, {omega_lb_sq}")


if __name__ == "__main__":
    main()
