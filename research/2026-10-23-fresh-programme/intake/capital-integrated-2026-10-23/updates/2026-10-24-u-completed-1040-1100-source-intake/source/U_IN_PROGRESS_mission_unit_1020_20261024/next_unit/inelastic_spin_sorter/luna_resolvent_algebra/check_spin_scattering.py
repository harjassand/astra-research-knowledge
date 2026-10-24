#!/usr/bin/env python3
"""Exact SymPy replay for the declared spin-conserving 3-site/TLS fixture."""

import sympy as sp


I = sp.I
E = sp.Rational(1, 2)
Delta = sp.Integer(1)
eta = sp.Rational(2, 5)
phi = sp.pi / 2
P3 = sp.diag(0, 0, 1)
I3 = sp.eye(3)


def abs2(z):
    return sp.simplify(sp.expand_complex(z * sp.conjugate(z)))


def molecule(spin):
    """Hopping convention: H31=exp(i spin phi), H13=conjugate."""
    return sp.Matrix(
        [
            [0, 1, sp.exp(-I * spin * phi)],
            [1, sp.Rational(3, 10), 1],
            [sp.exp(I * spin * phi), 1, -sp.Rational(1, 5)],
        ]
    )


def channel_data(spin):
    H = molecule(spin)
    sigmas, gammas, greens = [], [], []
    for n in (0, 1):
        En = E - n * Delta
        sigma = sp.simplify((En - I * sp.sqrt(4 - En**2)) / 2)
        gamma = sp.simplify(-2 * sp.im(sigma))
        G = sp.simplify((En * I3 - H - sp.diag(sigma, sigma, 0)).inv())
        sigmas.append(sigma)
        gammas.append(gamma)
        greens.append(G)
    return H, sigmas, gammas, greens


def full_scattering(spin):
    H, sigmas, gammas, _ = channel_data(spin)
    H6 = sp.BlockMatrix(
        [[H, eta * P3], [eta * P3, H + Delta * I3]]
    ).as_explicit()
    Sigma6 = sp.diag(sigmas[0], sigmas[0], 0, sigmas[1], sigmas[1], 0)
    G6 = sp.simplify((E * sp.eye(6) - H6 - Sigma6).inv())
    contact_idx = [0, 1, 3, 4]  # [L0,R0,L1,R1]
    Gcontacts = G6.extract(contact_idx, contact_idx)
    roots = [sp.sqrt(gammas[0]), sp.sqrt(gammas[0]), sp.sqrt(gammas[1]), sp.sqrt(gammas[1])]
    GammaHalf = sp.diag(*roots)
    S = sp.simplify(sp.eye(4) - I * GammaHalf * Gcontacts * GammaHalf)
    return G6, S


def main():
    Hp = molecule(+1)
    Hm = molecule(-1)
    assert Hm == Hp.T

    G6p, Sp = full_scattering(+1)
    G6m, Sm = full_scattering(-1)
    assert sp.simplify(Sm - Sp.T) == sp.zeros(4)
    assert sp.simplify(Sp * Sp.conjugate().T - sp.eye(4)) == sp.zeros(4)
    assert sp.simplify(Sm * Sm.conjugate().T - sp.eye(4)) == sp.zeros(4)

    _, _, gammas, (G0, G1) = channel_data(+1)
    D = sp.simplify(1 - eta**2 * G0[2, 2] * G1[2, 2])
    G10_formula = sp.simplify(eta * G1 * P3 * G0 / D)
    G10_full = G6p.extract([3, 4, 5], [0, 1, 2])
    assert sp.simplify(G10_full - G10_formula) == sp.zeros(3)

    # Contact-order amplitudes: r10 is reflected 0->1; r01 is 1->0.
    r10_rankone = sp.simplify(
        -I * sp.sqrt(gammas[0] * gammas[1]) * eta * G1[0, 2] * G0[2, 0] / D
    )
    r01_rankone = sp.simplify(
        -I * sp.sqrt(gammas[0] * gammas[1]) * eta * G0[0, 2] * G1[2, 0] / D
    )
    assert sp.simplify(Sp[2, 0] - r10_rankone) == 0
    assert sp.simplify(Sp[0, 2] - r01_rankone) == 0

    # Ground TLS input from the left. Spin minus is the transpose sector.
    Tplus = sp.simplify(abs2(Sp[1, 0]) + abs2(Sp[3, 0]))
    Tminus = sp.simplify(abs2(Sm[1, 0]) + abs2(Sm[3, 0]))
    Rexc_plus = abs2(Sp[2, 0])
    Rexc_minus = abs2(Sm[2, 0])
    P_ref_exc = sp.simplify((Rexc_plus + Rexc_minus) / 2)
    P_exc_total = sp.simplify(
        (
            Rexc_plus
            + abs2(Sp[3, 0])
            + Rexc_minus
            + abs2(Sm[3, 0])
        )
        / 2
    )
    Tavg = sp.simplify((Tplus + Tminus) / 2)
    PT = sp.simplify((Tplus - Tminus) / (Tplus + Tminus))
    lhs = sp.simplify(Tavg * abs(PT))

    r10, r01 = Sp[2, 0], Sp[0, 2]
    deltaT_from_reflection = sp.simplify(abs2(r01) - abs2(r10))
    assert sp.simplify(Tplus - Tminus - deltaT_from_reflection) == 0
    assert (P_ref_exc - lhs).is_positive
    assert (P_exc_total - P_ref_exc).is_positive

    print("Sminus equals Splus transpose; both are exactly unitary.")
    print("G10 rank-one formula and both inelastic reflection amplitudes pass.")
    for name, value in [
        ("Tplus", Tplus),
        ("Tminus", Tminus),
        ("PT", PT),
        ("Tavg*abs(PT)", lhs),
        ("P_ref_exc", P_ref_exc),
        ("P_exc_total", P_exc_total),
        ("Tplus-Tminus", sp.simplify(Tplus - Tminus)),
    ]:
        print(f"{name} = {sp.factor(value)} ~= {sp.N(value, 14)}")


if __name__ == "__main__":
    main()
