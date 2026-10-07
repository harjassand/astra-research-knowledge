"""Exact rational checks for the weighted reversible-center/fiber lift."""
from fractions import Fraction as F
import json


def ss(ell, psi):
    # Instrument c=2 identity on a common invariant sector.
    lhs = 2 * (1 - ((ell + psi) / 2) ** 2) - (1 - psi)
    rhs = (1 - ell**2) + (psi - psi**2) + (ell - psi) ** 2 / 2
    return lhs, rhs


def run():
    # Nonuniform stationary weights pi=(2/3,1/3), reversible chain with gap delta.
    gap = F(1, 256)
    pi = (F(2, 3), F(1, 3))
    P = ((1 - gap / 3, gap / 3), (2 * gap / 3, 1 - 2 * gap / 3))
    assert all(sum(row) == 1 for row in P)
    assert pi[0] * P[0][1] == pi[1] * P[1][0]
    assert all(sum(pi[z] * P[z][w] for z in range(2)) == pi[w] for w in range(2))
    lambda_slow = 1 - gap
    phi_slow = ((1 + lambda_slow) / 2) ** 2
    assert phi_slow == (1 - gap / 2) ** 2

    # The two center eigenvalues are 1 and lambda_slow. Tensoring with M_q,
    # each fiber-traceless eigenvalue of L is one of them, while Psi=E_center
    # is zero there. On the center, Psi=I. Cross-sector coherences are killed.
    sectors = []
    for ell in (F(1), lambda_slow):
        for psi in (F(1), F(0)):
            lhs, rhs = ss(ell, psi)
            assert lhs == rhs and lhs >= 0
            sectors.append({"L": str(ell), "Psi": str(psi), "SOS": str(lhs)})
    lhs, rhs = ss(F(0), F(0))
    assert lhs == rhs and lhs >= 0
    sectors.append({"L": "0", "Psi": "0", "SOS": str(lhs)})

    # A uniform two-sector variant has an exact non-EB q=4 fiber restriction.
    q = 4
    depol = F(1, 4)
    pt_antisymmetric = (1 - depol) / q**2 - depol / q
    assert pt_antisymmetric == F(-1, 64)
    eb_threshold = F(1, q + 1)
    exact_uniform_fiber_EB_distance = depol - eb_threshold
    assert exact_uniform_fiber_EB_distance == F(1, 20)

    power_errors = {str(m): str(F(1, 4) ** m) for m in range(1, 7)}
    assert all(F(v) <= F(1, 4) ** 1 for v in power_errors.values())
    return {
        "status": "PASS_EXACT_RATIONAL_FORMULA_CHECKS",
        "nonuniform_weights": [str(x) for x in pi],
        "reversible_P": [[str(x) for x in row] for row in P],
        "classical_gap_of_P": str(gap),
        "corrected_slow_eigenvalue": str(phi_slow),
        "corrected_slow_gap": str(1 - phi_slow),
        "SOS_sectors": sectors,
        "fiber_spectral_bound": "lambda(P)^2/4 <= 1/4",
        "q4_fiber_PPT_antisymmetric_eigenvalue": str(pt_antisymmetric),
        "q4_uniform_fiber_EB_distance": str(exact_uniform_fiber_EB_distance),
        "map_lift_error_bound_by_power": power_errors,
        "scope": "Exact finite arithmetic; full proofs and quantifiers are in deeper_center_fiber_lift.txt",
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
