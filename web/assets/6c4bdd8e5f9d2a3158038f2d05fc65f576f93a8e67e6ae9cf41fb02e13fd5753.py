#!/usr/bin/env python3
"""Small exact checks for the finite-ring SSEP formulas in CYCLE2_REPORT.md.

This enumerates canonical occupancy states using only the Python standard
library. It checks the active-bond mean, the telescoping drift identity, and
the finite-size conductivity/NE algebra. It is a finite diagnostic, not a
proof of the general statements and not a trajectory simulation.
"""

from fractions import Fraction
from itertools import combinations


def active_bonds(L: int, occupied: tuple[int, ...]) -> int:
    occ = set(occupied)
    return sum(((x in occ) != ((x + 1) % L in occ)) for x in range(L))


def check_ring(L: int, N: int) -> int:
    states = list(combinations(range(L), N))
    assert states
    total_b = 0
    for state in states:
        occ = set(state)
        eta = [int(x in occ) for x in range(L)]
        B = active_bonds(L, state)
        total_b += B

        # Conditional drift of the unwrapped total particle displacement,
        # in units of gamma*a, is sum_x (eta_x - eta_{x+1}).
        drift = sum(eta[x] - eta[(x + 1) % L] for x in range(L))
        assert drift == 0

        # The number of enabled hops is exactly the unlike-bond count.
        assert 0 <= B <= L

    mean_b = Fraction(total_b, len(states))
    exact_mean_b = Fraction(2 * N * (L - N), L - 1)
    assert mean_b == exact_mean_b, (L, N, mean_b, exact_mean_b)

    # With two identical independent lanes, F has twice this mean. From
    # D_tag = gamma*a^2*(L-N)/(N*(L-1)), normalize both conductivities by
    # beta*q^2*gamma*a/(A*L); their remaining factors are as below.
    mu_F = 2 * mean_b
    d_tag_without_gamma_a2 = Fraction(L - N, N * (L - 1))
    sigma_EH_over_common = Fraction(N * (L - N), L - 1)
    sigma_NE_over_common = Fraction(L - N, L - 1)
    assert sigma_EH_over_common / sigma_NE_over_common == N
    assert mu_F / 4 == sigma_EH_over_common
    assert N * d_tag_without_gamma_a2 == sigma_NE_over_common
    return len(states)


def main() -> None:
    checked = 0
    cases = 0
    for L in range(3, 11):
        for N in range(1, L):
            checked += check_ring(L, N)
            cases += 1
    print(f"PASS: {cases} (L,N) cases; {checked} canonical states checked")


if __name__ == "__main__":
    main()
