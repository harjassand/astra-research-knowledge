#!/usr/bin/env python3
"""Exact reduced r=0 seed-cone probe, without the full triple-space matrix."""
from __future__ import annotations

from itertools import combinations
from functools import reduce
from math import comb, gcd
from pathlib import Path
import json
import sys

import sympy as sp


def moment(n: int, h: int, k: int) -> int:
    if h == 0:
        return comb(n, k // 2)
    z = k % 2
    value = 0
    for q in range(h + 1):
        rem = k // 2 - q
        if q % 2 == (h * z) % 2 and 0 <= rem <= n - h:
            value += comb(h, q) * comb(n - h, rem)
    if k >= h:
        rem = (k - h) // 2
        if 0 <= rem <= n - h:
            value += 2 ** (h - 1) * comb(n - h, rem)
    return value


def primitive(q: list[sp.Rational]) -> tuple[int, ...]:
    den = sp.ilcm(*(x.q for x in q))
    vals = [int(x * den) for x in q]
    g = reduce(gcd, (abs(x) for x in vals), 0)
    return tuple(x // g for x in vals)


def extreme_rays(rows: list[sp.Matrix], n: int) -> set[tuple[int, ...]]:
    rays: set[tuple[int, ...]] = set()
    for inds in combinations(range(len(rows)), n - 1):
        M = sp.Matrix.vstack(*(rows[i] for i in inds))
        if M.rank() != n - 1:
            continue
        ker = M.nullspace()
        if len(ker) != 1:
            continue
        q = ker[0]
        for sign in (1, -1):
            v = sign * q
            if all((row * v)[0] >= 0 for row in rows):
                rays.add(primitive(list(v)))
                break
    return rays


def support_cones(vertices: list[sp.Matrix], n: int):
    out = []
    for i, v in enumerate(vertices):
        rows = [sp.eye(n).row(j) for j in range(n)]
        rows += [(v - w).T for j, w in enumerate(vertices) if j != i]
        out.append((i, extreme_rays(rows, n)))
    return out


def recoupling(n: int) -> sp.Matrix:
    N, d = 2 * n + 1, 2**n
    ds = [comb(N, j) for j in range(n + 1)]
    out = sp.zeros(n + 1)
    for j in range(n + 1):
        for k in range(n + 1):
            total = sum(
                (-1) ** (j * k - ell)
                * comb(j, ell)
                * comb(N - j, k - ell)
                for ell in range(min(j, k) + 1)
            )
            out[j, k] = (
                sp.Rational(comb(N, j) * total, d)
                * sp.sqrt(sp.Rational(1, ds[j] * ds[k]))
            )
    return out


def grade_diagonal(n: int, k: int) -> sp.Matrix:
    N = 2 * n + 1
    values = []
    for j in range(n + 1):
        values.append(
            sum(
                (-1) ** (k * j - ell)
                * comb(j, ell)
                * comb(N - j, k - ell)
                for ell in range(min(k, j) + 1)
            )
        )
    return sp.diag(*values)


def psd_principal_minors(M: sp.Matrix):
    checked = 0
    for size in range(1, M.rows + 1):
        for inds in combinations(range(M.rows), size):
            determinant = sp.factor(M.extract(inds, inds).det())
            checked += 1
            if determinant.is_negative is True:
                return False, checked, {"indices": list(inds), "determinant": str(determinant)}
            if determinant.is_nonnegative is not True:
                return False, checked, {"indices": list(inds), "undecided": str(determinant)}
    return True, checked, None


def main(n: int) -> None:
    N = 2 * n + 1
    seed_vectors = [sp.Matrix([moment(n, h, k) for k in range(1, n + 1)]) for h in range(n + 1)]
    cones = support_cones(seed_vectors, n)
    rays = sorted(set().union(*(r for _, r in cones)))
    F = recoupling(n)
    if F * F != sp.eye(n + 1) or F != F.T:
        raise AssertionError("r=0 recoupling involution check failed")
    Ds = [grade_diagonal(n, k) for k in range(1, n + 1)]
    trace = sp.Matrix([comb(N, k) for k in range(1, n + 1)])
    failures = []
    minor_checks = 0
    for ray in rays:
        alpha = sp.Matrix(ray)
        support = max((v.dot(alpha) for v in seed_vectors))
        bound = trace.dot(alpha) + support
        D = sum((alpha[k] * Ds[k] for k in range(n)), sp.zeros(n + 1))
        H = D + F * D * F
        gap = sp.simplify(bound * sp.eye(n + 1) - H)
        ok, checked, witness = psd_principal_minors(gap)
        minor_checks += checked
        if not ok:
            failures.append({"ray": list(ray), "support": str(support), "bound": str(bound), "witness": witness})
    result = {
        "n": n,
        "dimension_spinor": 2**n,
        "r0_multiplicity": n + 1,
        "seed_count": n + 1,
        "rays_by_seed": [len(r) for _, r in cones],
        "distinct_rays": len(rays),
        "principal_minor_checks": minor_checks,
        "failure_count": len(failures),
        "failures": failures,
        "status": "PASS_EXACT_R0_SEED_HULL" if not failures else "FAIL_EXACT_R0_SEED_HULL",
        "scope": "Exact r=0 block only; no claim about r>=1 or full pure-state support.",
    }
    out = Path(__file__).with_name(f"r0_seed_cone_n{n}.json")
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main(int(sys.argv[1]))
