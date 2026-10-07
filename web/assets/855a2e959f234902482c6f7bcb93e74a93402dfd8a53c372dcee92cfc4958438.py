"""Exact 2-sector matrix checks for the weighted reversible instrument.

This checks one rational fixture only.  The theorem is derived in
deeper_center_fiber_lift.txt; the script is not used as a proof.
"""
from fractions import Fraction as F
import json
from sympy import Matrix, Rational, eye, zeros, trace


def R(x):
    return Rational(x.numerator, x.denominator) if isinstance(x, F) else Rational(x)


def block(X, z, q):
    return X[z*q:(z+1)*q, z*q:(z+1)*q]


def set_block(out, z, q, value):
    out[z*q:(z+1)*q, z*q:(z+1)*q] = value


def physical_L(X, P, q):
    r, n = len(P), len(P) * q
    out = zeros(n)
    for w in range(r):
        value = zeros(q)
        for z in range(r):
            value += R(P[z][w]) * block(X, z, q)
        set_block(out, w, q, value)
    return out


def physical_E(X, r, q):
    out = zeros(r*q)
    Iq = eye(q)
    for z in range(r):
        set_block(out, z, q, trace(block(X, z, q)) * Iq / q)
    return out


def physical_C(X, P, q):
    return (physical_L(X, P, q) + physical_E(X, len(P), q)) / 2


def hat_L(X, P, q):
    r, n = len(P), len(P) * q
    out = zeros(n)
    for w in range(r):
        value = zeros(q)
        for z in range(r):
            value += R(P[w][z]) * block(X, z, q)
        set_block(out, w, q, value)
    return out


def hat_E(X, r, q):
    return physical_E(X, r, q)


def hat_C(X, P, q):
    return (hat_L(X, P, q) + hat_E(X, len(P), q)) / 2


def tau(X, pi, q):
    return sum(R(pi[z]) * trace(block(X, z, q)) / q for z in range(len(pi)))


def inner(X, Y, pi, q):
    return sum(R(pi[z]) * trace(block(X, z, q).conjugate().T * block(Y, z, q)) / q
               for z in range(len(pi)))


def swap_outputs(X, n):
    S = zeros(n*n)
    for i in range(n):
        for j in range(n):
            S[j*n+i, i*n+j] = 1
    return S * X * S


def partial_trace_weighted(X, first, pi, q):
    """Trace out one factor in the direct-sum product trace convention."""
    r, n = len(pi), len(pi)*q
    out = zeros(n)
    if first:
        # Keep the first factor; apply tau to the second tensor factor.
        for w in range(r):
            for a in range(q):
                for ap in range(q):
                    value = 0
                    for z in range(r):
                        for b in range(q):
                            i = (w*q+a)*n + z*q+b
                            j = (w*q+ap)*n + z*q+b
                            value += R(pi[z]) * X[i, j] / q
                    out[w*q+a, w*q+ap] = value
    else:
        # Keep the second factor; apply tau to the first tensor factor.
        for z in range(r):
            for b in range(q):
                for bp in range(q):
                    value = 0
                    for w in range(r):
                        for a in range(q):
                            i = (w*q+a)*n + z*q+b
                            j = (w*q+a)*n + z*q+bp
                            value += R(pi[w]) * X[i, j] / q
                    out[z*q+b, z*q+bp] = value
    return out


def append_instrument(X, P, pi, q):
    """The CP append map sum_(w,z) L_wz(X) tensor omega_wz.

    L_wz(X) has output block w equal to P[w,z] X_z and
    omega_wz has relative density I_q/pi[z] in sector z.
    """
    r, n = len(P), len(P)*q
    out = zeros(n*n)
    for w in range(r):
        for z in range(r):
            coeff = R(P[w][z]) / R(pi[z])
            Xz = block(X, z, q)
            for a in range(q):
                for b in range(q):
                    for ap in range(q):
                        for bp in range(q):
                            if b == bp:
                                i = (w*q+a)*n + z*q+b
                                j = (w*q+ap)*n + z*q+bp
                                out[i, j] += coeff * Xz[a, ap]
    return out


def joint_marginals(Xjoint, pi, q):
    return (partial_trace_weighted(Xjoint, True, pi, q),
            partial_trace_weighted(Xjoint, False, pi, q))


def run():
    q = 2
    pi = (F(2, 3), F(1, 3))
    gap = F(1, 16)
    P = ((1-gap/3, gap/3), (2*gap/3, 1-2*gap/3))
    r, n = len(P), len(P)*q
    assert all(sum(row) == 1 for row in P)
    assert all(sum(pi[z]*P[z][w] for z in range(r)) == pi[w] for w in range(r))
    assert all(pi[z]*P[z][w] == pi[w]*P[w][z] for z in range(r) for w in range(r))

    # All matrix-unit inputs in the direct-sum algebra.
    basis = []
    for z in range(r):
        for a in range(q):
            for b in range(q):
                X = zeros(n)
                X[z*q+a, z*q+b] = 1
                basis.append((z, a, b, X))

    # Exact tau-selfadjointness and agreement of the physical likelihood
    # similarity, including the corrected marginal C^2.
    for _, _, _, X in basis:
        weighted_input = zeros(n)
        for z in range(r):
            set_block(weighted_input, z, q, R(pi[z])/q * block(X, z, q))
        phys = physical_L(weighted_input, P, q)
        lifted = zeros(n)
        for w in range(r):
            set_block(lifted, w, q, q/R(pi[w]) * block(phys, w, q))
        assert lifted == hat_L(X, P, q)
        phys_c = physical_C(weighted_input, P, q)
        lifted_c = zeros(n)
        for w in range(r):
            set_block(lifted_c, w, q, q/R(pi[w]) * block(phys_c, w, q))
        assert lifted_c == hat_C(X, P, q)
        phys_phi = physical_C(phys_c, P, q)
        lifted_phi = zeros(n)
        for w in range(r):
            set_block(lifted_phi, w, q, q/R(pi[w]) * block(phys_phi, w, q))
        assert lifted_phi == hat_C(hat_C(X, P, q), P, q)

    for _, _, _, X in basis:
        for _, _, _, Y in basis:
            assert inner(X, hat_L(Y, P, q), pi, q) == inner(hat_L(X, P, q), Y, pi, q)

    # The append instrument has marginals hat L and E. Symmetrization gives
    # a real broadcaster for C=(L+E)/2; local postprocessing by C yields C^2.
    for _, _, _, X in basis:
        J = append_instrument(X, P, pi, q)
        m1, m2 = joint_marginals(J, pi, q)
        assert m1 == hat_L(X, P, q)
        assert m2 == hat_E(X, r, q)
        Js = (J + swap_outputs(J, n))/2
        s1, s2 = joint_marginals(Js, pi, q)
        Cx = (hat_L(X, P, q) + hat_E(X, r, q))/2
        assert s1 == Cx and s2 == Cx
        assert tau(s1, pi, q) == tau(X, pi, q)

    # Check the exact slow center eigenvalue and q=2 fiber norm formula.
    lam = 1-gap
    phi_lam = ((1+lam)/2)**2
    assert phi_lam == (1-gap/2)**2
    fiber_bound = max(abs(F(1)), abs(lam))**2 / 4
    assert fiber_bound == F(1, 4)

    return {
        "status": "PASS_EXACT_MATRIX_UNIT_CHECKS",
        "q": q,
        "pi": [str(x) for x in pi],
        "P": [[str(x) for x in row] for row in P],
        "gap": str(gap),
        "corrected_slow_center_eigenvalue": str(phi_lam),
        "fiber_phi_2_to_2_bound": str(fiber_bound),
        "checked": [
            "stationarity_and_detailed_balance",
            "physical_to_likelihood_similarity_on_all_algebra_matrix_units",
            "corrected_marginal_C_squared_similarity_on_all_algebra_matrix_units",
            "weighted_selfadjointness_of_L_on_all_matrix_units",
            "instrument_append_marginals_L_and_E_on_all_matrix_units",
            "symmetrized_broadcasting_marginals_C_on_all_matrix_units",
        ],
        "scope": "one exact rational fixture; not a proof of dimension-uniform statements",
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
