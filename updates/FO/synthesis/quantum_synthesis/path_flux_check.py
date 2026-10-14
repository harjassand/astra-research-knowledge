"""Exact rational checks of the grounded-path source-current theorem."""

from __future__ import annotations

import json
from fractions import Fraction as F
from pathlib import Path


def solve(A: list[list[F]], b: list[F]) -> list[F]:
    n = len(b)
    M = [row[:] + [rhs] for row, rhs in zip(A, b)]
    for k in range(n):
        pivot = next(i for i in range(k, n) if M[i][k])
        M[k], M[pivot] = M[pivot], M[k]
        p = M[k][k]
        M[k] = [x / p for x in M[k]]
        for i in range(n):
            if i == k:
                continue
            q = M[i][k]
            if q:
                M[i] = [x - q * y for x, y in zip(M[i], M[k])]
    return [M[i][-1] for i in range(n)]


def one_case(conductances: list[F], source: list[F]) -> dict:
    n = len(source)
    assert len(conductances) == n + 1 and all(c > 0 for c in conductances)
    A = [[F(0) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        A[i][i] = conductances[i] + conductances[i + 1]
        if i:
            A[i][i - 1] = -conductances[i]
            A[i - 1][i] = -conductances[i]
    x = solve(A, source)
    response = sum((u * v for u, v in zip(source, x)), F(0))

    prefix = [F(0)]
    for b in source:
        prefix.append(prefix[-1] + b)
    inv_c = [1 / c for c in conductances]
    C = sum((s * r for s, r in zip(prefix, inv_c)), F(0)) / sum(inv_c, F(0))
    q = [C - s for s in prefix]
    divergence = [q[i - 1] - q[i] for i in range(1, n + 1)]
    flux_energy = sum((q_i * q_i / c_i for q_i, c_i in zip(q, conductances)), F(0))
    assert divergence == source
    assert flux_energy == response

    v = [u / 2 for u in x]
    Av = [sum((A[i][j] * v[j] for j in range(n)), F(0)) for i in range(n)]
    lower = 2 * sum((b * z for b, z in zip(source, v)), F(0)) - sum(
        (z * az for z, az in zip(v, Av)), F(0)
    )
    edge_dv = [v[0]] + [v[i] - v[i - 1] for i in range(1, n)] + [-v[-1]]
    primal_dual_gap = sum(
        ((q_i - c_i * dv) ** 2 / c_i for q_i, c_i, dv in zip(q, conductances, edge_dv)),
        F(0),
    )
    assert flux_energy - lower == primal_dual_gap
    return {
        "n": n,
        "conductances": [str(c) for c in conductances],
        "source": [str(b) for b in source],
        "current_q": [str(x) for x in q],
        "response_exact": str(response),
        "flux_energy_exact": str(flux_energy),
        "primal_at_half_corrector_exact": str(lower),
        "primal_dual_gap_exact": str(primal_dual_gap),
    }


cases = []
for n in range(1, 9):
    unit = one_case([F(1)] * (n + 1), [F(1)] * n)
    expected = F(n * (n + 1) * (n + 2), 12)
    assert F(unit["response_exact"]) == expected
    cases.append(unit)

weighted = one_case(
    [F(1), F(2), F(3), F(5), F(7), F(4)],
    [F(1), F(2), F(1, 2), F(3), F(2)],
)

out = {
    "model": "finite grounded path, A=D* C D, Dirichlet endpoints",
    "theorem_checked": "b*A^-1*b = min_{D* q=b} sum_i q_i^2/c_i",
    "unit_path_exact_family": cases,
    "weighted_rational_case": weighted,
    "scope": "Exact rational identity checks for this implementation; no stochastic or physical validation.",
}
Path(__file__).with_name("path_flux_check.json").write_text(json.dumps(out, indent=2) + "\n")
print(json.dumps(out, indent=2))
