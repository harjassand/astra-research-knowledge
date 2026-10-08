#!/usr/bin/env python3
"""Exact finite check for the d=3 positive stochastic embedding in CYCLE2.md."""

from fractions import Fraction as Q
from itertools import permutations
import json


def eye(n):
    return [[Q(int(i == j)) for j in range(n)] for i in range(n)]


def mm(a, b):
    return [
        [sum((a[i][k] * b[k][j] for k in range(len(b))), Q(0))
         for j in range(len(b[0]))]
        for i in range(len(a))
    ]


def madd(a, b):
    return [[a[i][j] + b[i][j] for j in range(len(a[0]))]
            for i in range(len(a))]


def mscale(s, a):
    return [[s * x for x in row] for row in a]


def inv(a):
    n = len(a)
    work = [row[:] + eye(n)[i] for i, row in enumerate(a)]
    for j in range(n):
        pivot = next(i for i in range(j, n) if work[i][j])
        work[j], work[pivot] = work[pivot], work[j]
        z = work[j][j]
        work[j] = [x / z for x in work[j]]
        for i in range(n):
            if i != j:
                z = work[i][j]
                work[i] = [x - z * y for x, y in zip(work[i], work[j])]
    return [row[n:] for row in work]


def det(a):
    n = len(a)
    w = [row[:] for row in a]
    out = Q(1)
    for j in range(n):
        pivot = next((i for i in range(j, n) if w[i][j]), None)
        if pivot is None:
            return Q(0)
        if pivot != j:
            w[j], w[pivot] = w[pivot], w[j]
            out = -out
        z = w[j][j]
        out *= z
        for i in range(j + 1, n):
            q = w[i][j] / z
            for k in range(j + 1, n):
                w[i][k] -= q * w[j][k]
    return out


def s4(xs):
    d = len(xs[0])
    out = [[Q(0) for _ in range(d)] for _ in range(d)]
    for p in permutations(range(4)):
        inversions = sum(p[i] > p[j]
                         for i in range(4) for j in range(i + 1, 4))
        word = eye(d)
        for k in p:
            word = mm(word, xs[k])
        out = madd(out, mscale(Q(-1 if inversions % 2 else 1), word))
    return out


def rat_matrix(xs):
    return [[Q(x) for x in row] for row in xs]


def main():
    a = [
        rat_matrix([[0, -1, 0], [-1, -1, 0], [-1, 1, -1]]),
        rat_matrix([[0, 1, 1], [-1, 0, -1], [1, 1, 0]]),
        rat_matrix([[-1, 0, 0], [-1, -1, 0], [0, -1, -1]]),
        rat_matrix([[-1, 1, 0], [1, 0, 0], [0, 0, -1]]),
        [[Q(0) for _ in range(3)] for _ in range(3)],
    ]
    d, m = 3, 4
    e = [[Q(int(i == j) - int(i == d)) for j in range(d)]
         for i in range(m)]
    f = [[Q(int(j == i) if j < d else 0) - Q(1, m)
          for j in range(m)] for i in range(d)]
    one = [[Q(1)] for _ in range(m)]
    top = [[Q(1, m) for _ in range(m)]]
    sinv = top + f
    s = [[one[i][0]] + [e[i][j] for j in range(d)] for i in range(m)]

    assert mm(f, e) == eye(d)
    assert mm(e, f) == [[Q(int(i == j)) - Q(1, m)
                         for j in range(m)] for i in range(m)]
    assert mm(sinv, s) == eye(m)

    def entry_l1(x):
        return sum((abs(v) for row in x for v in row), Q(0))

    ea = [mm(mm(e, x), f) for x in a]
    k = 1 + max(max(entry_l1(x), entry_l1(y)) for x, y in zip(a, ea))
    t, c = Q(1, 64 * m * k), Q(1, 2)
    jmat = [[Q(1, m) for _ in range(m)] for _ in range(m)]
    p = []
    for delta in ea:
        baseline = [[(1 - c) * jmat[r][q] + (c if r == q else 0)
                     for q in range(m)] for r in range(m)]
        p.append(madd(baseline, mscale(t, delta)))

    # Exact Markov and similarity/decode checks.
    for i, pi in enumerate(p):
        assert all(x > 0 for row in pi for x in row)
        assert all(sum(row, Q(0)) == 1 for row in pi)
        assert all(sum((pi[r][q] for r in range(m)), Q(0)) == 1
                   for q in range(m))
        expected_block = madd(mscale(c, eye(d)), mscale(t, a[i]))
        expected_similarity = [[Q(1)] + [Q(0) for _ in range(d)]]
        expected_similarity += [[Q(0)] + row for row in expected_block]
        assert mm(mm(sinv, pi), s) == expected_similarity

    # Decode explicitly and verify the noncommutative output block.
    decoded = [mscale(1 / t, madd(mm(mm(f, pi), e), mscale(-c, eye(d))))
               for pi in p]
    assert decoded == a
    sa = s4(a[:4])
    assert sa == rat_matrix([[1, -2, 1], [4, -2, 2], [-3, 6, 1]])
    assert det(sa) == 24
    sp = s4(p[:4])
    expected_lower = mscale(t ** 4, sa)
    expected_s4_block = [[Q(0) for _ in range(m)] for _ in range(m)]
    expected_s4_block[0][0] = Q(0)
    for r in range(d):
        for q in range(d):
            expected_s4_block[r + 1][q + 1] = expected_lower[r][q]
    assert mm(mm(sinv, sp), s) == expected_s4_block

    ip5 = madd(eye(m), p[4])
    phi_p = mm(sp, inv(ip5))
    y = mm(mm(f, phi_p), e)
    expected_y = mscale(Q(2, 3) * t ** 4, sa)
    assert y == expected_y
    assert phi_p[0][0] == Q(1, 64424509440000)

    summary = {
        "dimension_d": d,
        "states_m": m,
        "K": str(k),
        "t": str(t),
        "minimum_transition_entry": str(min(x for mat in p for row in mat for x in row)),
        "s4_determinant": str(det(sa)),
        "max_abs_raw_output_entry": str(max(abs(x) for row in phi_p for x in row)),
        "phi_p_1_1": str(phi_p[0][0]),
        "all_exact_checks_passed": True,
        "n51_list_member": False,
    }
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
