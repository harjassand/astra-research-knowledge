"""Finite diagnostic for the unicycle rate-sum current bound.

This does not prove the theorem or establish novelty. It samples positive rates
with a prescribed cycle affinity, normalizes their bare sum K to one, solves
the stationary distribution, and compares the exact finite-chain current with
the analytic candidate envelope. Python standard library only.
"""
from math import tanh
import random


def solve(A, b):
    """Small dense linear solve by pivoted Gaussian elimination."""
    n = len(b)
    M = [list(A[i]) + [b[i]] for i in range(n)]
    for j in range(n):
        pivot = max(range(j, n), key=lambda i: abs(M[i][j]))
        if abs(M[pivot][j]) < 1e-14:
            raise ArithmeticError("singular stationary system")
        M[j], M[pivot] = M[pivot], M[j]
        scale = M[j][j]
        M[j] = [x / scale for x in M[j]]
        for i in range(n):
            if i == j:
                continue
            scale = M[i][j]
            M[i] = [x - scale * y for x, y in zip(M[i], M[j])]
    return [M[i][-1] for i in range(n)]


def stationary(forward, backward):
    n = len(forward)
    Q = [[0.0] * n for _ in range(n)]  # row generator
    for i, (u, w) in enumerate(zip(forward, backward)):
        j = (i + 1) % n
        Q[i][j] += u
        Q[j][i] += w
        Q[i][i] -= u
        Q[j][j] -= w
    # Solve Q^T p=0, replacing the final equation by sum(p)=1.
    M = [[Q[j][i] for j in range(n)] for i in range(n)]
    M[-1] = [1.0] * n
    rhs = [0.0] * (n - 1) + [1.0]
    return solve(M, rhs)


def cycle_current(p, forward, backward):
    n = len(forward)
    return sum(p[i] * forward[i] - p[(i + 1) % n] * backward[i]
               for i in range(n)) / n


def sample_rates(n, affinity, rng):
    # Arbitrary positive edge scale factors and edge affinity allocation.
    local = [rng.gauss(0.0, 1.0) for _ in range(n)]
    mean = sum(local) / n
    local = [x - mean + affinity / n for x in local]
    scale = [rng.uniform(-2.0, 2.0) for _ in range(n)]
    forward = [__import__("math").exp(s + a / 2.0)
               for s, a in zip(scale, local)]
    backward = [__import__("math").exp(s - a / 2.0)
                for s, a in zip(scale, local)]
    K = sum(forward) + sum(backward)
    return ([x / K for x in forward], [x / K for x in backward])


def uniform_rates(n, affinity, K=1.0):
    z = tanh(affinity / (2.0 * n))
    pair_sum = K / n
    return ([pair_sum * (1 + z) / 2] * n,
            [pair_sum * (1 - z) / 2] * n)


def main():
    rng = random.Random(20261008)
    samples = 1000
    print("finite diagnostic only; seed=20261008; K normalized to 1")
    print("N,A,samples,max sampled J/J_bound,uniform equality error")
    for n in (2, 3, 4, 5, 7):
        for affinity in (0.2, 1.0, 4.0):
            bound = tanh(affinity / (2.0 * n)) / (n * n)
            max_ratio = 0.0
            for _ in range(samples):
                f, b = sample_rates(n, affinity, rng)
                p = stationary(f, b)
                J = cycle_current(p, f, b)
                max_ratio = max(max_ratio, abs(J) / bound)
            f, b = uniform_rates(n, affinity)
            p = stationary(f, b)
            J = cycle_current(p, f, b)
            eq_error = abs(J - bound) / bound
            print(f"{n},{affinity},{samples},{max_ratio:.12g},{eq_error:.3g}")


if __name__ == "__main__":
    main()
