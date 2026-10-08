#!/usr/bin/env python3
"""Exact-rational CTMC and fuel-accounting check at matched total capacity.

The affinity is represented by rho=exp(A)=100, so all rates are rational while
A=log(100) is recorded exactly.  The finite-state linear systems are solved in
Q; reported means and fuel counts therefore have zero algebraic residual.
"""

from __future__ import annotations

from fractions import Fraction as F
import json
import math


def motif(state: int, i: int, n: int) -> int:
    left = (state >> ((i - 1) % n)) & 1
    center = (state >> i) & 1
    right = (state >> ((i + 1) % n)) & 1
    return 4 * left + 2 * center + right


def enzyme_set(rule: int) -> tuple[int, ...]:
    return tuple(p for p in range(8)
                 if ((rule >> p) & 1) != ((p >> 1) & 1))


def exact_solve(a: list[list[F]], b: list[F]) -> list[F]:
    n = len(b)
    m = [row[:] + [b[i]] for i, row in enumerate(a)]
    for col in range(n):
        pivot = next((r for r in range(col, n) if m[r][col] != 0), None)
        if pivot is None:
            raise ArithmeticError("singular killed generator")
        m[col], m[pivot] = m[pivot], m[col]
        scale = m[col][col]
        m[col] = [v / scale for v in m[col]]
        for row in range(n):
            if row == col or m[row][col] == 0:
                continue
            factor = m[row][col]
            m[row] = [u - factor * v for u, v in zip(m[row], m[col])]
    return [m[i][n] for i in range(n)]


def fmt(x: F) -> dict:
    return {
        "exact_rational": f"{x.numerator}/{x.denominator}",
        "decimal_12_places": f"{float(x):.12f}",
    }


def audit(rule: int, n: int = 7, total_capacity: F = F(2),
          rho: int = 100, k_spo: F = F(1, 1000)) -> dict:
    enzymes = enzyme_set(rule)
    kcat = total_capacity / len(enzymes)
    q = kcat * F(rho, rho + 1)
    r = kcat * F(1, rho + 1)
    cutoff = n // 2
    safe = [s for s in range(1 << n) if s.bit_count() <= cutoff]
    ix = {s: i for i, s in enumerate(safe)}
    size = len(safe)
    minus_q = [[F(0) for _ in range(size)] for _ in range(size)]
    gross = [F(0) for _ in range(size)]
    reverse = [F(0) for _ in range(size)]
    enzyme_set_f = set(enzymes)
    for state in safe:
        i = ix[state]
        for site in range(n):
            p = motif(state, site, n)
            qmotif = p ^ 2
            target = state ^ (1 << site)
            fwd = q if p in enzyme_set_f else F(0)
            rev = r if qmotif in enzyme_set_f else F(0)
            rate = k_spo + fwd + rev
            if not rate:
                continue
            minus_q[i][i] += rate
            if target in ix:
                minus_q[i][ix[target]] -= rate
            gross[i] += fwd
            reverse[i] += rev
    start = ix[0]
    mean_t = exact_solve(minus_q, [F(1)] * size)[start]
    mean_gross = exact_solve(minus_q, gross)[start]
    mean_reverse = exact_solve(minus_q, reverse)[start]
    mean_net = mean_gross - mean_reverse
    return {
        "rule": rule,
        "enzyme_motifs": list(enzymes),
        "enzyme_species_count": len(enzymes),
        "N": n,
        "decoder": "first passage to more than N/2 ones",
        "sum_kcat_capacity": str(total_capacity),
        "per_species_kcat": str(kcat),
        "rho_exp_affinity": rho,
        "A_beta_delta_mu": f"ln({rho})",
        "A_decimal_for_reference_only": f"{math.log(rho):.12f}",
        "spontaneous_rate_per_site": str(k_spo),
        "forward_channel_rate_q": str(q),
        "reverse_channel_rate_r": str(r),
        "mean_first_passage_time": fmt(mean_t),
        "gross_fuel_hydrolyses": fmt(mean_gross),
        "reverse_fuel_returns": fmt(mean_reverse),
        "net_fuel_consumed": fmt(mean_net),
        "chemical_work_in_kBT_units_approx": f"{float(mean_net) * math.log(rho):.12f}",
        "algebraic_residual": "exactly zero over rational generator; A is log(rho)",
    }


def main() -> None:
    print(json.dumps({
        "method": "rational finite-state generator; exact Gaussian elimination",
        "assumptions": [
            "N=7 binary ring, node energies equal as in source model",
            "each forward enzyme event consumes one fuel equivalent",
            "each reverse enzyme event returns one fuel equivalent",
            "spontaneous flips are symmetric and consume no fuel",
            "the fuel/waste reservoir is clamped; no depletion model",
        ],
        "results": [audit(166), audit(232)],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
