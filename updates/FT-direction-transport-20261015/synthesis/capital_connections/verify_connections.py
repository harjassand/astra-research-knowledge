#!/usr/bin/env python3
"""Exact finite checks for PROOFS.md; no source imports or physical simulation.

Standard-library JSON and SymPy only. Analytic, acquisition and priority limits
are stated in PROOFS.md. This checker does not certify those limits away.
"""
from pathlib import Path
import json
import sympy as S

Q = S.Rational


def main():
    A = S.Matrix([[2, 1, -1], [-1, 2, -1], [-1, -1, 3]])
    symmetric = (A + A.T) / 2
    assert all(symmetric[:i, :i].det() > 0 for i in range(1, 4))
    P = S.eye(3)[:, :2]
    b = S.Matrix([1, 0, 0])
    c = S.Matrix([0, 0, 1])
    L = S.Matrix([1, -1])
    v = P * L
    x, Y, z = A.inv() * b, A.inv() * P, A.inv() * c
    H = P.T * Y
    beta = H.inv() * (H.T - H) * H.inv() * P.T * z
    lam = z + Y * beta
    assert lam == A.T.inv() * c
    W = Y * L
    C = (v.T * W)[0]
    t = (v.T * x)[0]
    p = S.symbols('p', nonnegative=True)
    predicted = x - W * (p * t / (1 + p * C))
    actual = (A + p * v * v.T).inv() * b
    assert all(S.cancel(a - d) == 0 for a, d in zip(predicted, actual))

    # Current correction to an old abandoned illustration: nonreciprocal
    # inverse changes have distinct left and right factors.
    LL = S.Matrix([[1, 1], [0, 1]])
    eb = S.Matrix([1, 0])
    true_update = (LL + eb * eb.T).inv() - LL.inv()
    left, right = LL.inv() * eb, eb.T * LL.inv()
    two_sided = -left * right / (1 + (eb.T * LL.inv() * eb)[0])
    symmetric_claim = -left * left.T / (1 + (eb.T * LL.inv() * eb)[0])
    assert true_update == two_sided == S.Matrix([[-Q(1, 2), Q(1, 2)], [0, 0]])
    assert true_update != symmetric_claim
    assert (1 + p).subs(p, 0) == (1 + p - Q(3, 2) * p**2).subs(p, 0)
    assert S.diff(1 + p, p).subs(p, 0) == S.diff(1 + p - Q(3, 2) * p**2, p).subs(p, 0)
    assert 1 / (1 + Q(1)) == Q(1, 2)
    assert 1 / (1 + Q(1) - Q(3, 2)) == 2

    # The source's indistinguishable baseline pair separates only after a
    # newly granted v-source. A sensor alone does not grant this source.
    e = S.eye(5)
    v5 = e[:, 0] - e[:, 3]
    hidden = []
    for sign in [-1, 1]:
        aa = S.eye(5) + sign * e[:, 1] * e[:, 3].T
        xx = aa.inv() * e[:, 0]
        ww = aa.inv() * v5
        assert ww == v5 + sign * e[:, 1]
        assert (v5.T * ww)[0] == 2
        q = xx - ww * p / (1 + 2 * p)
        score = S.cancel((e[:, 1].T * q)[0])
        assert score == -sign * p / (1 + 2 * p)
        hidden.append(str(score))

    # One-dimensional rational data attain the proposed joint-error bound.
    x0 = U = C0 = t0 = Q(1, 2)
    xhat, Uhat, Chat, that = Q(51, 100), Q(49, 100), Q(51, 100), Q(49, 100)
    eps = Q(1, 100)
    invhat = 1 / (1 + Chat)
    gamma = invhat * eps
    Kbound = invhat / (1 - gamma)
    dhat = invhat * that
    dtrue = t0 / (1 + C0)
    epsd = Kbound * (eps + eps * abs(dhat))
    output_bound = eps + eps * abs(dhat) + (abs(Uhat) + eps) * epsd
    output_actual_error = abs((x0 - U * dtrue) - (xhat - Uhat * dhat))
    assert gamma < 1
    assert abs(dtrue - dhat) == epsd == Q(4, 453)
    assert output_actual_error == output_bound == Q(8, 453)

    # Common harmonic host: full well data and baseline barrier agree, while
    # the unacquired transition-state projection gives opposite clamp effects.
    KK = S.Matrix([[2, -1], [-1, 2]])
    port = S.Matrix([1, 0])
    compliance = (port.T * KK.inv() * port)[0]
    fA = S.Matrix([1, 0])
    FA = -(fA.T * KK.inv() * fA)[0] / 2
    RA = (port.T * KK.inv() * fA)[0] ** 2 / (2 * compliance)
    kappa = Q(3, 2)
    chi = kappa * compliance / (1 + kappa * compliance)
    worlds = []
    for fU, EU in [(S.Matrix([0, 1]), Q(1)), (S.Matrix([2, 0]), Q(2))]:
        FU = EU - (fU.T * KK.inv() * fU)[0] / 2
        RU = (port.T * KK.inv() * fU)[0] ** 2 / (2 * compliance)
        shift = chi * (RU - RA)
        assert FU - FA == 1
        worlds.append({'baseline_barrier': '1', 'R_U': str(RU), 'barrier_shift': str(shift)})
    assert [w['barrier_shift'] for w in worlds] == ['-1/8', '1/2']
    # Singular multiport support uses a formula without S^{-1}.
    K3 = S.Matrix([[3, -1, 0], [-1, 3, -1], [0, -1, 2]])
    P3 = S.eye(3)[:, :2]
    S3 = S.diag(2, 0)
    H3 = P3.T * K3.inv() * P3
    M3 = (S.eye(2) + S3 * H3).inv() * S3
    assert M3 == M3.T
    for f in [S.Matrix([1, 2, 0]), S.Matrix([0, 1, 3])]:
        mean = P3.T * K3.inv() * f
        direct = (f.T * (K3.inv() - (K3 + P3 * S3 * P3.T).inv()) * f)[0] / 2
        assert direct == (mean.T * M3 * mean)[0] / 2

    # Exact finite candidate set; PROOFS.md proves the bound outside it.
    negatives, zeros, positives = [], [], []
    for a in range(-2, 3):
        for q in range(-2, 3):
            norm2 = a * a + q * q
            if not 0 < norm2 <= 5:
                continue
            value = 4 * norm2 + 8 * q * q - Q(64 * q * q, norm2)
            determinant_sign = (a * a + q * q) * (a * a + 3 * q * q) - 16 * q * q
            assert value * norm2 / 4 == determinant_sign
            if value < 0:
                negatives.append([a, q])
            elif value == 0:
                zeros.append([a, q])
            else:
                positives.append((value, value / norm2, [a, q]))
    assert len(negatives) == 8 and not zeros
    assert min(x[0] for x in positives) == Q(4, 5)
    assert min(x[1] for x in positives) == Q(4, 25)
    sharp = [x[2] for x in positives if x[0] == Q(4, 5)]

    result = {
        'status': 'PASS',
        'scope': 'Exact finite identities and witnesses; analytic and physical claims remain separately scoped.',
        'port_span_finite_response': {'base_det': str(A.det()), 'exact_all_p_identity': True,
                                      'port_adjoint_identity': True, 'control_response_C': str(C)},
        'PR90_abandoned_illustration_correction': {'true_update': str(true_update),
                                                  'symmetric_factor_formula_fails': True},
        'local_derivative_does_not_supply_finite_law': {'same_baseline_and_derivative': True,
                                                       'scores_at_one': ['1/2', '2']},
        'extra_probe_hidden_support_pair': hidden,
        'joint_error_bound_sharp_scalar_witness': {'denominator_gamma': str(gamma),
                                                   'response_error': str(epsd), 'output_error': str(output_bound)},
        'same_well_same_barrier_worlds': worlds,
        'singular_multiport_support_identity': True,
        'phase_local_spectrum': {'real_negative_index': 8, 'negative_integer_frequencies': negatives,
                                 'no_nongauge_zero_integer_frequencies': True,
                                 'positive_L2_gap': '4/5', 'positive_H1_seminorm_gap': '4/25',
                                 'sharp_positive_frequencies': sharp,
                                 'outside_finite_enumeration': 'Analytic t>=6 estimate in PROOFS.md, not numerical sampling.'},
        'historical_priority': 'UNKNOWN', 'independent_correctness': 'UNKNOWN',
        'physical_acquisition': 'NOT_ESTABLISHED',
    }
    Path(__file__).with_name('CONNECTION_VERIFICATION.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
