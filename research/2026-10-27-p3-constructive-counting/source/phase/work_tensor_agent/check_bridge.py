"""Exact small obstructions to applying N1077 to arbitrary circuit tensors.

Run: python work_tensor_agent/check_bridge.py
Standard library only. All arithmetic is integral or rational.
"""
from fractions import Fraction as Q
from itertools import product
import json


def transpose(a):
    return [list(row) for row in zip(*a)]


def mul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(2))
             for j in range(2)] for i in range(2)]


def inverse(a):
    det = a[0][0] * a[1][1] - a[0][1] * a[1][0]
    assert det
    return [[Q(a[1][1], det), Q(-a[0][1], det)],
            [Q(-a[1][0], det), Q(a[0][0], det)]]


def cp_tensor(factors):
    return {bits: sum(factors[0][bits[0]][s] *
                      factors[1][bits[1]][s] *
                      factors[2][bits[2]][s] for s in range(2))
            for bits in product(range(2), repeat=3)}


def hyperdet(t):
    a, b, c, d, e, f, g, h = (t[x] for x in product(range(2), repeat=3))
    return (a*a*h*h + b*b*g*g + c*c*f*f + d*d*e*e
            - 2*(a*b*g*h + a*c*f*h + a*d*e*h + b*c*f*g
                 + b*d*e*g + c*d*e*f) + 4*(a*d*f*g + b*c*e*h))


def main():
    eye = [[1, 0], [0, 1]]
    a = [[1, 0], [1, 1]]
    c = [[1, -1], [0, 1]]
    t = cp_tensor([a, a, c])
    assert all(t[x] == int(x[2] == (x[0] & x[1])) for x in t)
    assert hyperdet(t) == 1
    assert mul(transpose(c), a) == eye

    # Opposite edge basis changes preserve the CP pairing exactly.
    changes = [[[2, 1], [3, 2]], [[1, -3], [2, 1]], [[-2, 5], [1, 4]]]
    for g in changes:
        new_c = mul(g, c)
        new_a = mul(transpose(inverse(g)), a)
        assert mul(transpose(new_c), new_a) == eye

    # Two vertices joined by three parallel edges, a planar trivalent graph.
    w = [[1, 2], [3, 5]]
    left = cp_tensor([eye, eye, eye])
    right = cp_tensor([w, w, w])
    assert hyperdet(left) == 1 and hyperdet(right) == 1
    beta_left = Q(w[1][0]*w[1][1], w[0][0]*w[0][1])**3
    beta_right = Q(w[0][1]*w[1][1], w[0][0]*w[1][0])**3
    assert beta_left == Q(3375, 8)
    assert beta_right == Q(1000, 27)
    z = sum(left[x] * right[x] for x in left)
    assert z == sum(y**3 for row in w for y in row) == 161

    results = {
        "and_tensor_entries": [t[x] for x in product(range(2), repeat=3)],
        "and_hyperdeterminant": hyperdet(t),
        "and_chain_cp_pairing": eye,
        "exact_gauge_checks": len(changes),
        "theta_hyperdeterminants": [hyperdet(left), hyperdet(right)],
        "theta_beta": [str(beta_left), str(beta_right)],
        "theta_exact_contraction": z,
        "all_assertions_passed": True,
    }
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
