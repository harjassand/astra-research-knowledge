#!/usr/bin/env python3
"""Exact Fraction checker for the two-type tangent-resummed sampler certificate.

This checks a finite-state resolvent example. It is not a PDE discretization,
Monte Carlo accuracy check, or floating-point diffusion implementation.
"""
from fractions import Fraction as F
import json
from pathlib import Path


def mmul(a, b):
    return [[sum((a[i][k] * b[k][j] for k in range(len(b))), F(0))
             for j in range(len(b[0]))] for i in range(len(a))]


def mv(a, x):
    return [sum((a[i][j] * x[j] for j in range(len(x))), F(0))
            for i in range(len(a))]


def qstr(x):
    return f"{x.numerator}/{x.denominator}"


def main():
    # L is the generator of a symmetric two-state CTMC with jump rate 3.
    lam = F(2)
    L = [[F(-3), F(3)], [F(3), F(-3)]]
    resolvent_matrix = [[lam - L[i][j] if i == j else -L[i][j]
                         for j in range(2)] for i in range(2)]
    # K = lam * (lam I - L)^(-1), verified by the exact matrix identity below.
    K = [[F(5, 8), F(3, 8)], [F(3, 8), F(5, 8)]]
    assert mmul(resolvent_matrix, K) == [[lam, F(0)], [F(0), lam]]
    assert all(sum(row, F(0)) == 1 and min(row) >= 0 for row in K)

    # Equation: -L u + F_i(u_i) = r_i, with v=0 and spatial envelope h=(2,1).
    V = [F(1), F(2)]
    c2 = [F(1, 2), F(0)]
    B2 = [F(1, 2), F(0)]
    r = [F(1), F(0)]
    h = [F(2), F(1)]
    assert all(h_i > 0 for h_i in h)
    assert all(abs(c2[i]) <= B2[i] for i in range(2))
    a1 = [1 - v / lam for v in V]
    g0 = [abs(x) / lam for x in r]
    g1 = [a1[i] * h[i] for i in range(2)]
    g2 = [B2[i] * h[i] ** 2 / lam for i in range(2)]
    A0, A1, A2 = (mv(K, g) for g in (g0, g1, g2))
    totals = [A0[i] + A1[i] + A2[i] for i in range(2)]
    assert all(totals[i] <= h[i] for i in range(2))
    event_probabilities = {
        "source": [A0[i] / h[i] for i in range(2)],
        "one_child": [A1[i] / h[i] for i in range(2)],
        "two_children": [A2[i] / h[i] for i in range(2)],
        "zero_leaf": [1 - totals[i] / h[i] for i in range(2)],
    }
    assert event_probabilities["source"] == [F(5, 32), F(3, 16)]
    assert event_probabilities["one_child"] == [F(5, 16), F(3, 8)]
    assert event_probabilities["two_children"] == [F(5, 16), F(3, 8)]
    assert event_probabilities["zero_leaf"] == [F(7, 32), F(1, 16)]
    assert totals == [F(25, 16), F(15, 16)]
    assert all(sum(event_probabilities[k][i] for k in event_probabilities) == 1
               for i in range(2))

    # Every nonzero event samples endpoint A: the tilted measures have support {A}.
    for g in (g0, g1, g2):
        assert g[1] == 0 and g[0] > 0

    # M f = h^-1 K[(a1*h + 2*B2*h^2/lam) f].
    offspring_weight = [a1[i] * h[i] + 2 * B2[i] * h[i] ** 2 / lam
                        for i in range(2)]
    M = [[K[i][j] * offspring_weight[j] / h[i] for j in range(2)]
         for i in range(2)]
    assert M == [[F(15, 16), F(0)], [F(9, 8), F(0)]]
    w = [F(1), F(6, 5)]
    alpha = F(15, 16)
    assert all(Mw <= alpha * wi for Mw, wi in zip(mv(M, w), w))
    # This rank-one triangular matrix has eigenvalues 15/16 and 0.
    assert M[0][0] == alpha and M[1][1] == 0 and M[0][1] == 0

    # Exact total progeny: generations n>=1 are alpha^n from A;
    # from B they are (9/16)*alpha^(n-1).
    expected_nodes_A = 1 + alpha / (1 - alpha)
    expected_nodes_B = 1 + F(9, 8) / (1 - alpha)
    assert expected_nodes_A == 16
    assert expected_nodes_B == 19

    # The old scalar certificate has R=1 and B2=1/2. Its enclosure is
    # impossible for every radius because max_h(lambda*h-B2*h^2)=1/2<R.
    # At h=max(h)=2, both displayed scalar inequalities fail.
    old_lambda = min(V)
    old_h = max(h)
    old_gamma = 2 * max(B2) * old_h
    old_enclosure_lhs = max(abs(x) for x in r) + max(B2) * old_h ** 2
    old_enclosure_rhs = old_lambda * old_h
    old_best_enclosure_rhs = old_lambda ** 2 / (4 * max(B2))
    assert old_gamma == 2 and old_gamma >= old_lambda
    assert old_enclosure_lhs == 3 and old_enclosure_lhs > old_enclosure_rhs
    assert old_best_enclosure_rhs == F(1, 2) < max(abs(x) for x in r)

    # Verify the algebraic fixed point in Q(sqrt(19)) by reducing its defining
    # quadratic: u_A^2 + (22/5)u_A - 2 = 0; u_B=3u_A/5.
    ua_const, ua_sqrt = F(-11, 5), F(3, 5)
    poly_const = ua_const**2 + 19 * ua_sqrt**2 + F(22, 5) * ua_const - 2
    poly_sqrt = 2 * ua_const * ua_sqrt + F(22, 5) * ua_sqrt
    assert poly_const == 0 and poly_sqrt == 0
    # 4 < sqrt(19) < 5 gives 1/5 < u_A < 4/5 and 3/25 < u_B < 12/25.
    solution = "u_A=(-22+6*sqrt(19))/10; u_B=3*(-22+6*sqrt(19))/50"
    checks = {
        "status": "PASS",
        "scope": "Exact rational certificate for a two-state continuous-time Markov resolvent sampler.",
        "parameters": {
            "Lambda": qstr(lam),
            "L": [[qstr(x) for x in row] for row in L],
            "K": [[qstr(x) for x in row] for row in K],
            "V": [qstr(x) for x in V],
            "r": [qstr(x) for x in r],
            "c2": [qstr(x) for x in c2],
            "B2": [qstr(x) for x in B2],
            "h": [qstr(x) for x in h],
        },
        "event_probabilities_by_root_A_B": {
            key: [qstr(x) for x in value]
            for key, value in event_probabilities.items()
        },
        "envelope_total_by_root_A_B": [qstr(x) for x in totals],
        "offspring_operator": [[qstr(x) for x in row] for row in M],
        "positive_vector": [qstr(x) for x in w],
        "contraction_and_spectral_radius_upper": qstr(alpha),
        "expected_total_nodes_A_B": [qstr(expected_nodes_A), qstr(expected_nodes_B)],
        "ordinary_sup_norm_of_M": qstr(max(sum(row, F(0)) for row in M)),
        "old_global_criterion": {
            "lambda": qstr(old_lambda),
            "Gamma": qstr(old_gamma),
            "Gamma_lt_lambda": False,
            "enclosure_lhs": qstr(old_enclosure_lhs),
            "enclosure_rhs": qstr(old_enclosure_rhs),
            "best_possible_lambda_h_minus_B_h2": qstr(old_best_enclosure_rhs),
            "enclosure_passes": False,
        },
        "fixed_point_in_tube": solution,
        "fixed_point_algebraic_identity": "u_A^2 + (22/5)*u_A - 2 = 0; verified coefficientwise in Q(sqrt(19))",
        "exact_diffusion_cost_scope": (
            "The endpoint operation is a two-state CTMC resolvent draw. The check does not price a continuous Brownian endpoint or any physical acquisition."
        ),
    }
    target = Path(__file__).with_name("certificate.json")
    target.write_text(json.dumps(checks, indent=2) + "\n")
    print(json.dumps({"status": checks["status"], "certificate": str(target),
                      "rho_upper": qstr(alpha),
                      "expected_nodes_A_B": [qstr(expected_nodes_A), qstr(expected_nodes_B)]},
                     indent=2))


if __name__ == "__main__":
    main()
