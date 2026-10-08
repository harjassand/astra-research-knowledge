"""Dependency-free numerical spot check for the CYCLE2 secant bias bounds.

This is a finite diagnostic of the stated linear mean-ODE model, not evidence
that biological populations follow the model or that the bounds are novel.
"""

from math import log
from random import Random


def matvec(A, x):
    return [sum(a * b for a, b in zip(row, x)) for row in A]


def expm_action(A, t, x):
    """Return exp(t A)x by a convergent Taylor series for small capped t."""
    K = len(x)
    term = x[:]
    out = x[:]
    for n in range(1, 200):
        term = [v * t / n for v in matvec(A, term)]
        out = [a + b for a, b in zip(out, term)]
        if max(abs(v) for v in term) < 1e-17:
            return out
    raise ArithmeticError("Taylor series did not converge to tolerance")


def row_generator(offdiag):
    K = len(offdiag)
    return [[offdiag[i][j] if i != j else -sum(offdiag[i])
             for j in range(K)] for i in range(K)]


def transpose(A):
    return [list(row) for row in zip(*A)]


def check_one_case(Q, r, i, tau, Lambda, R):
    K = len(r)
    QT = transpose(Q)
    A = [[QT[a][b] + (r[a] if a == b else 0.0)
          for b in range(K)] for a in range(K)]
    e_i = [1.0 if j == i else 0.0 for j in range(K)]
    x = expm_action(A, tau, e_i)
    N = sum(x)
    p = [z / N for z in x]
    qhat = [p[j] / tau for j in range(K) if j != i]
    qtrue = [Q[i][j] for j in range(K) if j != i]
    q_bias = max(abs(a - b) for a, b in zip(qhat, qtrue))
    rhat = log(N) / tau
    r_bias = abs(rhat - r[i])
    Cq = (Lambda + R) * (2 * Lambda + 3 * R) * tau
    Cr = R * (Lambda + R) * tau
    if q_bias > Cq + 5e-13 or r_bias > Cr + 5e-13:
        raise AssertionError((q_bias, Cq, r_bias, Cr))
    return q_bias, Cq, r_bias, Cr


def main():
    rng = Random(20261008)
    K = 4
    Lambda = 0.3
    R = 0.2
    max_ratio_q = 0.0
    max_ratio_r = 0.0
    cases = 0
    for _ in range(250):
        off = [[0.0] * K for _ in range(K)]
        for i in range(K):
            raw = [rng.random() for j in range(K) if j != i]
            total = sum(raw)
            scale = rng.random() * Lambda / total if total else 0.0
            k = 0
            for j in range(K):
                if j != i:
                    off[i][j] = raw[k] * scale
                    k += 1
        Q = row_generator(off)
        r = [rng.uniform(-R, R) for _ in range(K)]
        tau = rng.uniform(1e-4, 0.25)
        for i in range(K):
            qb, Cq, rb, Cr = check_one_case(Q, r, i, tau, Lambda, R)
            max_ratio_q = max(max_ratio_q, qb / Cq if Cq else 0.0)
            max_ratio_r = max(max_ratio_r, rb / Cr if Cr else 0.0)
            cases += 1
    print(f"checked {cases} pure-start/rate fixtures; caps Lambda={Lambda}, R={R}")
    print(f"max observed composition-bias / bound = {max_ratio_q:.6g}")
    print(f"max observed log-count-bias / bound = {max_ratio_r:.6g}")
    print("PASS: no sampled fixture violated the analytic bounds")


if __name__ == "__main__":
    main()
