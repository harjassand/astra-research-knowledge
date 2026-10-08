#!/usr/bin/env python3
"""Exact finite-capacity frontier for a bounded-birth/linear-death chain.

All arithmetic in the worked examples and small-LP vertex audit is rational.
The candidate enumeration uses the vertex theorem recorded in CYCLE2_REPORT.md.
Run with: python3 work/agents/programmable_biology/circuit_reliability/CYCLE2_frontier.py
"""

from fractions import Fraction as F
from itertools import combinations
from math import factorial


def poisson_weights(q: F, K: int) -> list[F]:
    return [q**n / factorial(n) for n in range(K + 1)]


def normalize(weights: list[F]) -> list[F]:
    z = sum(weights, F(0))
    return [w / z for w in weights]


def mean_of(p: list[F]) -> F:
    return sum((n * p[n] for n in range(len(p))), F(0))


def frontier_vertices(q: F, M: int, mu: F, h: int) -> list[tuple[F, list[F], tuple]]:
    """Enumerate every bang-bang/one-partial vertex at the prescribed mean."""
    out: list[tuple[F, list[F], tuple]] = []

    def add(K: int, weights: list[F], label: tuple) -> None:
        p0 = normalize(weights)
        p = p0 + [F(0)] * (M + 1 - len(p0))
        if mean_of(p) == mu:
            out.append((sum(p[:h], F(0)), p, label))

    if mu == 0:
        add(0, [F(1)], (0, None, F(0)))

    for K in range(1, M + 1):
        base = poisson_weights(q, K)
        add(K, base, (K, None, F(1)))
        for j in range(K):
            A0 = sum(base[: j + 1], F(0))
            A1 = sum((n * base[n] for n in range(j + 1)), F(0))
            T0 = sum(base[j + 1 :], F(0))
            T1 = sum((n * base[n] for n in range(j + 1, K + 1)), F(0))
            numerator = mu * A0 - A1
            denominator = T1 - mu * T0
            alphas: set[F] = set()
            if denominator:
                alpha = numerator / denominator
                if 0 <= alpha <= 1:
                    alphas.add(alpha)
            elif numerator == 0:
                # The mean is independent of alpha.  The objective is linear-
                # fractional in alpha, so an endpoint is optimal.
                alphas.update((F(0), F(1)))
            for alpha in alphas:
                weights = base[: j + 1] + [alpha * x for x in base[j + 1 :]]
                add(K, weights, (K, j, alpha))
    return out


def counterexample() -> tuple[F, list[F]]:
    """The minimal-capacity exact non-threshold example from the report."""
    q, M, mu, h = F(1, 2), 2, F(1, 64), 2
    candidates = frontier_vertices(q, M, mu, h)
    objective, p, label = min(candidates, key=lambda item: item[0])
    expected_p = [F(379, 384), F(4, 384), F(1, 384)]
    assert p == expected_p, (label, p)
    assert objective == F(383, 384)
    assert mean_of(p) == mu
    assert sum(p, F(0)) == 1
    return objective, p


def solve_square(A: list[list[F]], b: list[F]) -> list[F] | None:
    """Exact Gaussian elimination; return None when the matrix is singular."""
    n = len(b)
    aug = [list(A[i]) + [b[i]] for i in range(n)]
    for col in range(n):
        pivot = next((r for r in range(col, n) if aug[r][col] != 0), None)
        if pivot is None:
            return None
        aug[col], aug[pivot] = aug[pivot], aug[col]
        scale = aug[col][col]
        aug[col] = [x / scale for x in aug[col]]
        for r in range(n):
            if r != col and aug[r][col] != 0:
                scale = aug[r][col]
                aug[r] = [x - scale * y for x, y in zip(aug[r], aug[col])]
    return [aug[i][-1] for i in range(n)]


def brute_vertices(q: F, M: int, mu: F) -> set[tuple[F, ...]]:
    """Independently enumerate all vertices by exact active-set enumeration.

    There are M+1 variables and two independent equalities, so a vertex has a
    full-rank active set containing M-1 inequalities in addition to them.
    """
    d = M + 1
    eq_rows = [[F(1) for _ in range(d)], [F(n) for n in range(d)]]
    eq_rhs = [F(1), mu]
    inequalities: list[tuple[list[F], F]] = []
    for i in range(d):
        row = [F(0)] * d
        row[i] = F(-1)
        inequalities.append((row, F(0)))
    for n in range(M):
        row = [F(0)] * d
        row[n] = -q
        row[n + 1] = F(n + 1)
        inequalities.append((row, F(0)))

    vertices: set[tuple[F, ...]] = set()
    for active in combinations(inequalities, M - 1):
        A = eq_rows + [x[0] for x in active]
        b = eq_rhs + [x[1] for x in active]
        p = solve_square(A, b)
        if p is None:
            continue
        if all(sum((a * x for a, x in zip(row, p)), F(0)) <= rhs
               for row, rhs in inequalities):
            vertices.add(tuple(p))
    return vertices


def check_m2_vertices() -> set[tuple[F, ...]]:
    """Compare structural candidates with all exact LP vertices at M=2."""
    q, M, mu = F(1, 2), 2, F(1, 64)
    structural = {tuple(p) for _, p, _ in frontier_vertices(q, M, mu, h=M + 1)}
    brute = brute_vertices(q, M, mu)
    assert structural == brute, (structural, brute)
    assert brute == {
        (F(63, 64), F(1, 64), F(0)),
        (F(379, 384), F(1, 96), F(1, 384)),
    }
    return brute


if __name__ == "__main__":
    objective, p = counterexample()
    vertices = check_m2_vertices()
    print("exact frontier example:")
    print("  q=1/2, M=2, h=2, mean=1/64")
    print("  optimal stationary law =", p)
    print("  min P(N<h) =", objective)
    print("  max P(N>=h) =", 1 - objective)
    print("single-cutoff comparator: P(N<h)=1 (the only feasible threshold has support {0,1})")
    print("all exact M=2 LP vertices =", sorted(vertices))
    print("  selected law: E[N^2]=1/48; Var(N)=253/12288")
    print("  threshold law: E[N^2]=1/64; Var(N)=63/4096")
