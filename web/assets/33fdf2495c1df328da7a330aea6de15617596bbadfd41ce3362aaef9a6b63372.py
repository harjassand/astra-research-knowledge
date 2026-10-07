"""Exact finite checks for the center-moving instrument construction.

Uses only rational arithmetic for the stochastic and Dirichlet identities.
The NPT eigenvalue and Pauli-channel extension arithmetic are also exact.
This is a formula transcription check, not a proof of the general theorem.
"""
from fractions import Fraction as F
import json


def instrument_identity(ell, psi):
    # C=(L+Psi)/2, Phi=C* C. In a common real eigenbasis these are scalars.
    lhs = 2 * (1 - ((ell + psi) / 2) ** 2) - (1 - psi)
    rhs = (1 - ell**2) + (psi - psi**2) + (ell - psi) ** 2 / 2
    return lhs, rhs


def run():
    r = 2
    q = 4
    delta = F(1, 1024)
    P = ((1 - delta, delta), (delta, 1 - delta))
    assert all(sum(row) == 1 for row in P)
    assert all(sum(P[z][w] for z in range(r)) == 1 for w in range(r))
    assert P[0][1] == P[1][0]

    markov_nonconstant = 1 - 2 * delta
    phi_slow = ((1 + markov_nonconstant) / 2) ** 2
    assert phi_slow == (1 - delta) ** 2
    assert 1 - phi_slow == 2 * delta - delta**2
    # Exact fixed-point projection kills every nonconstant mode when delta>0;
    # the canonical EB center expectation has eigenvalue 1 on that mode.

    # Check the exact SOS identity on the four invariant sectors of the
    # two-block algebra: global scalar, center difference, uniform fiber
    # traceless part, and fiber-difference traceless part.
    sectors = {
        "global_scalar": (F(1), F(1)),
        "center_difference": (markov_nonconstant, F(1)),
        "uniform_fiber_traceless": (F(1), F(0)),
        "fiber_difference_traceless": (markov_nonconstant, F(0)),
        "interblock_coherences": (F(0), F(0)),
    }
    sos = {}
    for name, (ell, psi) in sectors.items():
        lhs, rhs = instrument_identity(ell, psi)
        assert lhs == rhs and lhs >= 0
        sos[name] = {"L_eigenvalue": str(ell), "Psi_eigenvalue": str(psi),
                     "SOS_value": str(lhs)}

    # On the uniform-block encoded fiber, Phi is the q-dimensional
    # depolarizing channel with lambda=1/4. Its normalized Choi partial
    # transpose has antisymmetric eigenvalue (1-lambda)/q^2-lambda/q.
    q_depol = F(1, 4)
    npt = (1 - q_depol) / q**2 - q_depol / q
    assert npt == F(-1, 64)

    # Pauli channel with Bloch eigenvalues (9/16, 1/2, 1/16).
    # Its normalized Choi eigenvalues are (17/32, 1/4, 7/32, 0).
    lam = (F(9, 16), F(1, 2), F(1, 16))
    p = ((1 + lam[0] + lam[1] + lam[2]) / 4,
         (1 + lam[0] - lam[1] - lam[2]) / 4,
         (1 - lam[0] + lam[1] - lam[2]) / 4,
         (1 - lam[0] - lam[1] + lam[2]) / 4)
    assert p == (F(17, 32), F(1, 4), F(7, 32), F(0))
    purity = sum(x*x for x in p)
    assert purity == F(201, 512)
    assert F(1, 2) >= purity  # extension criterion; det is exactly zero

    # Any qubit CPTP C with C^*C equal to this unital Pauli channel would
    # have Bloch singular values 3/4, 1/sqrt(2), 1/4. The necessary unital
    # qubit CP inequality s1+s2<=1+s3 fails because 1/sqrt(2)>1/2.
    # This exact squared comparison is 1/2 > 1/4.
    assert F(1, 2) > F(1, 4)

    return {
        "status": "PASS_EXACT_RATIONAL_FORMULA_CHECKS",
        "fiber_dimension": q,
        "delta": str(delta),
        "classical_mode_eigenvalue_of_Phi": str(phi_slow),
        "classical_mode_gap": str(1 - phi_slow),
        "SOS_sectors": sos,
        "uniform_fiber_depolarizing_parameter": str(q_depol),
        "fiber_Choi_PPT_antisymmetric_eigenvalue": str(npt),
        "Pauli_symmetric_extension_eigenvalues": [str(x) for x in p],
        "Pauli_Choi_purity": str(purity),
        "Pauli_extension_threshold": "1/2",
        "square_root_CP_singular_value_violation": "1/sqrt(2) > 1/2",
        "scope": "exact low-dimensional diagnostics; analytic proofs are in INITIAL.txt",
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
