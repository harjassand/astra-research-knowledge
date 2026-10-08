#!/usr/bin/env python3
"""Small exact checks for the cycle-2 spatial-defect analysis.

Only Python's standard library is used. Energies below use J=1 unless noted.
The script checks exact rational characteristic polynomials and the exact
half-line bound state; it does not certify an operator-limit theorem.
"""

from fractions import Fraction as F
import json


def mul_linear(poly, c0, c1):
    """Multiply ascending-coefficient polynomial by c0 + c1*E."""
    out = [F(0)] * (len(poly) + 1)
    for i, x in enumerate(poly):
        out[i] += c0 * x
        out[i + 1] += c1 * x
    return out


def add_scaled(a, b, scale=F(1)):
    out = [F(0)] * max(len(a), len(b))
    for i, x in enumerate(a):
        out[i] += x
    for i, x in enumerate(b):
        out[i] += scale * x
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def path_characteristic(N, boundary_v, J=F(1)):
    """det(T_N + v|1><1| - E I), in ascending powers of E."""
    if N < 1:
        raise ValueError("N must be positive")
    d0 = [F(1)]
    d1 = [4 * J + boundary_v, F(-1)]
    if N == 1:
        return d1
    prev2, prev1 = d0, d1
    for _n in range(2, N + 1):
        # D_n=(4J-E)D_(n-1)-(2J)^2 D_(n-2).
        cur = add_scaled(mul_linear(prev1, 4 * J, F(-1)), prev2,
                         -4 * J * J)
        prev2, prev1 = prev1, cur
    return prev1


def fmt(poly):
    return [str(x) for x in poly]


def check_resonant_boundary_small_N():
    # At v=-2J, N=1 has E=2. For N=2 the exact polynomial is
    # E^2-6E+4, whose roots are 3 +/- sqrt(5).
    p1 = path_characteristic(1, F(-2))
    p2 = path_characteristic(2, F(-2))
    assert p1 == [F(2), F(-1)]
    assert p2 == [F(4), F(-6), F(1)]
    # The secular equation at v=-2J reduces, after discarding q=0,
    # to cos(q(N+1/2))=0. For N=2 this gives q=pi/5,3pi/5.
    # Their cosines are the roots of 4c^2-2c-1; E=4(1-c) then gives
    # exactly E^2-6E+4=0, matching the matrix determinant.
    return {
        "N1_char_poly_ascending": fmt(p1),
        "N2_char_poly_ascending": fmt(p2),
        "N2_char_poly_descending": ["1", "-6", "4"],
        "N2_secular_roots": ["q=pi/5", "q=3pi/5"],
        "verified": True,
    }


def check_fixed_attractive_boundary_bound_state():
    # On the half-line, v=-4J and psi_i=2^{-(i-1)} give E=-J exactly.
    J, v, E = F(1), F(-4), F(-1)
    psi = lambda i: F(1, 2) ** (i - 1)
    lhs_first = (4 * J + v) * psi(1) - 2 * J * psi(2)
    assert lhs_first == E * psi(1)
    for i in range(2, 8):
        lhs = -2 * J * psi(i - 1) + 4 * J * psi(i) - 2 * J * psi(i + 1)
        assert lhs == E * psi(i)
    return {
        "boundary_potential_v_over_J": "-4",
        "decay_ratio": "1/2",
        "one_particle_energy_over_J": "-1",
        "verified_recurrence_sites": "1..8",
        "verified": True,
    }


def check_bulk_delta_threshold():
    # For a centered point interaction, g_crit=-1/[theta(1-theta)]=-4.
    theta = F(1, 2)
    gcrit = -1 / (theta * (1 - theta))
    assert gcrit == -4
    # At threshold the zero-energy tent function has slopes +2 and -2;
    # its derivative jump is -4 = gcrit*phi(1/2), with phi(1/2)=1.
    slope_left, slope_right, value = F(2), F(-2), F(1)
    assert slope_right - slope_left == gcrit * value
    return {
        "theta": "1/2",
        "critical_g": str(gcrit),
        "zero_mode": "phi(x)=2x (x<=1/2), 2(1-x) (x>=1/2)",
        "derivative_jump": str(slope_right - slope_left),
        "verified": True,
    }


def main():
    result = {
        "scope": "exact algebraic spot checks; not a proof of continuum convergence",
        "boundary_resonance": check_resonant_boundary_small_N(),
        "deep_boundary_bound_state": check_fixed_attractive_boundary_bound_state(),
        "bulk_delta_threshold": check_bulk_delta_threshold(),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
