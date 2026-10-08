"""Exact finite checks for the cycle-2 omitted-phase certificate claims.

This checks the A2B arithmetic, robust panel/global LP values in the displayed
binary example, simplex-grid counts, and the stated finite-population sample
formula. It is a fixture, not a proof of the general LP or minimax theorems.
"""

from fractions import Fraction as F
from math import comb, ceil, log


def binary_lower_hull(target_x, phases):
    """Minimize mixture energy for a binary target over listed (x, lower E).

    A binary-composition hull optimum uses at most two phases. Enumerate all
    feasible pairs and exact single-phase matches using rational arithmetic.
    """
    best = None
    for x, e in phases:
        if x == target_x:
            best = e if best is None else min(best, e)
    for i, (x1, e1) in enumerate(phases):
        for x2, e2 in phases[i + 1 :]:
            if x1 == x2 or not min(x1, x2) <= target_x <= max(x1, x2):
                continue
            w1 = (x2 - target_x) / (x2 - x1)
            w2 = (target_x - x1) / (x2 - x1)
            value = w1 * e1 + w2 * e2
            best = value if best is None else min(best, value)
    return best


def main():
    # AB target at x_B=1/2, predicted energy -100 meV/atom; 5 meV residual.
    target_x, target_upper = F(1, 2), F(-95, 1000)
    endpoints = [(F(0), F(-5, 1000)), (F(1), F(-5, 1000))]
    panel_hull = binary_lower_hull(target_x, endpoints)
    assert target_upper <= panel_hull == F(-5, 1000)

    # Add the withheld A2B with E=-300 meV/atom. The optimal mixture is
    # 3/4 A2B + 1/4 B, at x_B=1/2 and E=-225 meV/atom.
    hidden = (F(1, 3), F(-300, 1000))
    global_hull = binary_lower_hull(target_x, endpoints + [hidden])
    hidden_weight = F(3, 4)
    hidden_mix_x = hidden_weight * hidden[0] + (1 - hidden_weight) * F(1)
    hidden_mix_e = hidden_weight * hidden[1] + (1 - hidden_weight) * endpoints[1][1]
    assert hidden_mix_x == target_x
    assert global_hull == hidden_mix_e == F(-905, 4000)
    assert target_upper - global_hull == F(525, 4000)
    # Exact point energies at zero-energy endpoints give the original
    # 125 meV/atom gap reported in the first-wave counterexample.
    point_hull = binary_lower_hull(target_x, [(F(0), F(0)), (F(1), F(0)), hidden])
    assert point_hull == F(-225, 1000)
    assert F(-100, 1000) - point_hull == F(125, 1000)

    # Panel supporting plane ell(x)=-5 meV/atom meets the robust endpoint
    # lower bounds and target upper bound; the hidden phase violates it.
    plane_value = F(-5, 1000)
    assert plane_value <= endpoints[0][1] and plane_value <= endpoints[1][1]
    assert plane_value >= target_upper
    assert plane_value > hidden[1]

    # Uniform composition simplex grid: q components, denominator M.
    assert comb(92 + 2 - 1, 2) == 4278
    assert comb(5 + 10 - 1, 10) == 1001

    # One bad candidate among N, uniform without-replacement audit. To bound
    # false stable at delta, the audit must inspect at least (1-delta)N IDs
    # if it certifies under the null with probability one.
    N, delta = 10_000, F(1, 20)
    required = ceil((1 - float(delta)) * N)
    assert required == 9500
    # General iid Q prevalence bound; rho=1% and delta=5% requires 299 draws.
    m_iid = ceil(log(0.05) / log(1 - 0.01))
    assert m_iid == 299

    print("panel robust lower hull: -0.005 eV/atom; target upper: -0.095 eV/atom")
    print("panel robust support-plane certificate: PASS")
    print("global lower hull with hidden A2B and endpoint interval lows: -0.22625 eV/atom")
    print("target point-energy destabilization: 0.125 eV/atom")
    print("target interval-upper excess over lower hull: 0.13125 eV/atom")
    print("same panel plane violates hidden A2B lower bound: PASS")
    print("simplex points q=92,M=2: 4278; q=5,M=10: 1001")
    print("N=10000, one hidden, delta=0.05: minimum distinct queries=9500")
    print("rho=0.01, delta=0.05 iid audit draws: 299")


if __name__ == "__main__":
    main()
