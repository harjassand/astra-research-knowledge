"""Independent exact-rational checks for polynomial and killed-tangent samplers."""
from fractions import Fraction as Q
import json


def inv2(a):
    det = a[0][0] * a[1][1] - a[0][1] * a[1][0]
    return [[a[1][1] / det, -a[0][1] / det],
            [-a[1][0] / det, a[0][0] / det]]


def mm(a, b):
    return [[sum((a[i][k] * b[k][j] for k in range(len(b))), Q(0))
             for j in range(len(b[0]))] for i in range(len(a))]


def mv(a, v):
    return [sum((a[i][j] * v[j] for j in range(len(v))), Q(0))
            for i in range(len(a))]


def frac(x):
    return f"{x.numerator}/{x.denominator}"


def run():
    # Two-state CTMC with rational generator; the known solution e is rational.
    q = [[-Q(1, 10), Q(1, 10)], [Q(1, 5), -Q(1, 5)]]
    v = [Q(2), Q(3)]
    e = [Q(1, 20), Q(1, 25)]
    h, b2 = Q(1, 10), Q(1)
    lam, big_lam = min(v), max(v)
    gamma = 2 * b2 * h

    # PDE is -Q e + V e + e^2 = r, so F_i(t)=V_i*t+t^2.
    minus_q_plus_v = [[-q[i][j] + (v[i] if i == j else Q(0))
                       for j in range(2)] for i in range(2)]
    r = [sum((minus_q_plus_v[i][j] * e[j] for j in range(2)), Q(0)) + e[i]**2
         for i in range(2)]
    R = max(abs(x) for x in r)
    P = b2 * h**2
    assert R + P <= lam * h
    assert gamma < lam

    # Exact state-dependent-killing endpoint kernel K=(-Q+diag(V))^-1 diag(V).
    a_inv = inv2(minus_q_plus_v)
    kill_kernel = mm(a_inv, [[v[0], Q(0)], [Q(0), v[1]]])
    assert all(sum(row, Q(0)) == 1 for row in kill_kernel)
    assert all(x >= 0 for row in kill_kernel for x in row)

    # Its categorical source / 2-child probabilities are valid at every state.
    kill_p_source = [abs(r[i]) / (h * v[i]) for i in range(2)]
    kill_p_two = [b2 * h / v[i] for i in range(2)]
    assert all(kill_p_source[i] + kill_p_two[i] <= 1 for i in range(2))
    z = [x / h for x in e]
    kill_recursion = [sum((kill_kernel[i][j] *
                           (r[j] / (h * v[j]) - h * z[j]**2 / v[j])
                           for j in range(2)), Q(0)) for i in range(2)]
    assert kill_recursion == z
    kill_q_bound = gamma / lam
    kill_work_bound = 1 / (1 - kill_q_bound)

    # Exact uniformization kernel used in the supplied theorem.
    rate_matrix = [[(big_lam if i == j else Q(0)) - q[i][j]
                    for j in range(2)] for i in range(2)]
    rate_inv = inv2(rate_matrix)
    uniform_kernel = [[big_lam * rate_inv[i][j] for j in range(2)]
                      for i in range(2)]
    assert all(sum(row, Q(0)) == 1 for row in uniform_kernel)
    assert all(x >= 0 for row in uniform_kernel for x in row)
    uniform_p_source = [R / (big_lam * h)] * 2
    uniform_p_one = [1 - x / big_lam for x in v]
    uniform_p_two = [b2 * h / big_lam] * 2
    assert all(uniform_p_source[i] + uniform_p_one[i] + uniform_p_two[i] <= 1
               for i in range(2))
    uniform_recursion = [sum((uniform_kernel[i][j] *
                              (r[j] / (big_lam * h) +
                               (1 - v[j] / big_lam) * z[j] -
                               h * z[j]**2 / big_lam)
                              for j in range(2)), Q(0)) for i in range(2)]
    assert uniform_recursion == z
    uniform_q_bound = 1 - lam / big_lam + gamma / big_lam
    uniform_work_bound = 1 / (1 - uniform_q_bound)

    # Exact uncentered absolute-moment contradiction from the source note.
    # If finite uniform m existed, w=inf m would satisfy w >= 16+25w^4.
    assert Q(16) < Q(16) + 25 * Q(16)**4

    def vec(xs):
        return [frac(x) for x in xs]

    return {
        "method": "exact Fraction arithmetic; no floating-point tolerances",
        "ctmc_generator": [[frac(x) for x in row] for row in q],
        "tangent": vec(v),
        "known_error": vec(e),
        "residual": vec(r),
        "radius": frac(h),
        "global_certificate": {
            "R_plus_P": frac(R + P), "lambda_h": frac(lam * h),
            "Gamma": frac(gamma), "lambda": frac(lam),
        },
        "killed_tangent": {
            "endpoint_kernel": [[frac(x) for x in row] for row in kill_kernel],
            "source_probabilities": vec(kill_p_source),
            "two_child_probabilities": vec(kill_p_two),
            "expected_normalized_output": vec(kill_recursion),
            "offspring_bound": frac(kill_q_bound),
            "expected_nodes_bound": frac(kill_work_bound),
        },
        "constant_rate_uniformization": {
            "rate": frac(big_lam),
            "endpoint_kernel": [[frac(x) for x in row] for row in uniform_kernel],
            "source_probabilities": vec(uniform_p_source),
            "one_child_probabilities": vec(uniform_p_one),
            "two_child_probabilities": vec(uniform_p_two),
            "expected_normalized_output": vec(uniform_recursion),
            "offspring_bound": frac(uniform_q_bound),
            "expected_nodes_bound": frac(uniform_work_bound),
        },
        "concentration_scope": "Both normalized outputs are supported in [-1,1]; Hoeffding gives 2 exp(-M eps^2/(2 h^2)) in the ideal exact sampler.",
        "uncentered_scope": "The inequality w >= 16 + 25 w^4 has no nonnegative solution; this only excludes the specified uncentered independent-product expansion.",
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
