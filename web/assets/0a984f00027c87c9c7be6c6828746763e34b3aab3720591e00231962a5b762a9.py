"""Exact rational witnesses for the XXZ local-gate LC boundary.

Standard-library only. This is a local-interface diagnostic, not an FPRAS
implementation or a proof of hardness for the physical Hamiltonian problem.
"""
from fractions import Fraction as F
import json


def add(*xs):
    return sum(xs, F(0))


def vec_dot(x, y):
    return add(*(a * b for a, b in zip(x, y)))


def q_hessian_at_point(terms, x):
    """Return q, grad q, Hess q for terms (coefficient, variable-index tuple)."""
    n = len(x)
    q = F(0)
    grad = [F(0) for _ in range(n)]
    hess = [[F(0) for _ in range(n)] for _ in range(n)]
    for coeff, inds in terms:
        val = coeff
        for i in inds:
            val *= x[i]
        q += val
        for i in inds:
            grad[i] += val / x[i]
            for j in inds:
                if i != j:
                    hess[i][j] += val / (x[i] * x[j])
    return q, grad, hess


def log_hessian_direction(terms, x, v):
    q, grad, hess = q_hessian_at_point(terms, x)
    hv = [add(*(hess[i][j] * v[j] for j in range(len(v)))) for i in range(len(v))]
    return vec_dot(v, hv) / q - (vec_dot(v, grad) ** 2) / (q ** 2)


def six_vertex_terms(a, b, c):
    return [
        (a, (0, 1)), (a, (2, 3)),
        (b, (0, 3)), (b, (1, 2)),
        (c, (0, 2)), (c, (1, 3)),
    ]


def fmt(x):
    return f"{x.numerator}/{x.denominator}"


def main():
    alpha, s = F(1), F(1, 10)
    witnesses = []
    for gamma, direction, label in [
        (F(11, 10), (1, 1, -1, -1), "gamma>alpha"),
        (F(-11, 10), (1, -1, -1, 1), "gamma<-alpha"),
    ]:
        a = 1 + s * (3 * alpha + gamma)
        b = 1 + s * (3 * alpha - gamma)
        c = 2 * s * alpha
        eig_of_gate_hessian = (
            a - b - c if gamma > alpha else -a + b - c
        )
        directional = log_hessian_direction(
            six_vertex_terms(a, b, c),
            (F(1),) * 4,
            tuple(F(z) for z in direction),
        )
        rayleigh = directional / 4
        witnesses.append({
            "side": label,
            "alpha": fmt(alpha), "gamma": fmt(gamma), "s": fmt(s),
            "a": fmt(a), "b": fmt(b), "c": fmt(c),
            "second_positive_eigenvalue_of_hessian_q": fmt(eig_of_gate_hessian),
            "log_hessian_directional_second_derivative": fmt(directional),
            "log_hessian_rayleigh_quotient": fmt(rayleigh),
        })

    # Rotate axes so the large gamma coupling becomes X, with alpha on Y and Z.
    # The standard 3*alpha identity shift keeps all diagonal entries positive.
    gamma = F(2)
    A = 1 + s * (4 * alpha)
    B = 1 + s * (2 * alpha)
    C = s * (gamma + alpha)
    D = s * (gamma - alpha)
    rotated_terms = [
        (A, (0, 1)), (A, (2, 3)),
        (B, (0, 3)), (B, (1, 2)),
        (C, (0, 2)), (C, (1, 3)),
        (D, ()), (D, (0, 1, 2, 3)),
    ]
    t = F(1, 100)
    rotated_directional = log_hessian_direction(
        rotated_terms, (t,) * 4, (F(1),) * 4
    )
    rotated = {
        "alpha": fmt(alpha), "gamma": fmt(gamma), "s": fmt(s),
        "A": fmt(A), "B": fmt(B), "C": fmt(C), "D_pairflip": fmt(D),
        "test_point_each_coordinate": fmt(t),
        "ones_direction_log_hessian_second_derivative": fmt(rotated_directional),
        "positive": rotated_directional > 0,
        "origin_limit_directional_value": fmt(4 * (A + B + C) / D),
    }

    print(json.dumps({
        "scope": "exact local tensor diagnostics only",
        "standard_orientation_witnesses": witnesses,
        "axis_permutation_witness": rotated,
        "ancilla_no_go": (
            "A nonnegative log-concave lift cannot return a non-log-concave "
            "gate by fixing auxiliary variables to positive values. For a "
            "multiaffine lift, any fixed auxiliary coefficient is obtained "
            "by repeated partial-derivative limits and zero specializations, "
            "which also preserve log-concavity. A global variable-degree "
            "encoding is not covered by this local no-go."
        ),
    }, indent=2))


if __name__ == "__main__":
    main()
