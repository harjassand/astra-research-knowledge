#!/usr/bin/env python3
"""Finite diagnostics for the CRAY bounded-field envelope compiler.

This is NOT the general polynomial-time implementation.  The rank-one
prototype enumerates its small base spin system.  Gaussian interval masses
are evaluated with mpmath; these are high-precision, not interval-certified.
The general-rank pointwise tests enumerate small spin systems as well.

Run: python verify_compiler.py --output results.json
Dependencies: numpy, scipy, mpmath (no network access).
"""
from __future__ import annotations
import argparse
import itertools
import json
import math
import time
from dataclasses import dataclass
from fractions import Fraction as F
from pathlib import Path

import mpmath as mp
import numpy as np
from scipy.special import logsumexp


def states(n: int) -> np.ndarray:
    return np.asarray(list(itertools.product((-1, 1), repeat=n)), dtype=float)


def to_mp(x: F | int | float) -> mp.mpf:
    if isinstance(x, F):
        return mp.mpf(x.numerator) / x.denominator
    return mp.mpf(x)


def mp_logsum(values: list[mp.mpf]) -> mp.mpf:
    top = max(values)
    return top + mp.log(mp.fsum(mp.exp(v - top) for v in values))


def log_normal_interval(a: mp.mpf, b: mp.mpf) -> mp.mpf:
    """High-precision log P(a < N(0,1) < b); avoid 1-CDF subtraction."""
    if not a < b:
        raise ValueError("Empty normal interval")
    root2 = mp.sqrt(2)
    if a >= 0:
        value = (mp.erfc(a / root2) - mp.erfc(b / root2)) / 2
    elif b <= 0:
        value = (mp.erfc(-b / root2) - mp.erfc(-a / root2)) / 2
    else:
        value = (mp.erf(b / root2) - mp.erf(a / root2)) / 2
    if value <= 0:
        raise ArithmeticError("Insufficient precision for normal interval")
    return mp.log(value)


@dataclass
class Cell:
    left: F | None
    right: F | None
    c: list[F]
    d: F
    e: F
    log_z_base: mp.mpf


def construct_rank_one(a: list[F], h: list[F], j0: list[list[F]]) -> tuple[list[Cell], int]:
    n = len(a)
    if n == 0 or len(h) != n or len(j0) != n:
        raise ValueError("Inconsistent input sizes")
    r_bound = max(sum(abs(j0[i][j]) for j in range(n) if j != i) for i in range(n))
    L = math.ceil(r_bound) + math.ceil(math.log2(4 * n))
    step = F(1, 4 * n)
    knots = [F(-L) + k * step for k in range(8 * n * L + 1)]
    endpoints = sorted({(t - h[i]) / a[i] for i in range(n) if a[i] != 0 for t in knots})
    bounds = [None, *endpoints, None]
    ss = list(itertools.product((-1, 1), repeat=n))
    base_energies = [sum(j0[i][j] * x[i] * x[j] for i in range(n) for j in range(n)) / 2 for x in ss]
    cells = []
    for left, right in zip(bounds[:-1], bounds[1:]):
        y = (right - 1) if left is None and right is not None else ((left + 1) if right is None and left is not None else (F(0) if left is None else (left + right) / 2))
        c: list[F] = []
        d = F(0)
        e = F(0)
        for ai, hi in zip(a, h):
            ell = hi + ai * y
            if ell >= L:
                c.append(F(L)); d += ai; e += hi - L
            elif ell <= -L:
                c.append(F(-L)); d -= ai; e += -hi - L
            else:
                k = (ell + L) // step
                c.append(F(-L) + (F(k) + F(1, 2)) * step)
        log_z = mp_logsum([to_mp(energy + sum(ci * xi for ci, xi in zip(c, x))) for energy, x in zip(base_energies, ss)])
        cells.append(Cell(left, right, c, d, e, log_z))
    return cells, L


def rank_one_mass_check(a: list[F], h: list[F], j0: list[list[F]], cells: list[Cell], variance: F) -> dict:
    n = len(a)
    k = to_mp(variance)
    rootk = mp.sqrt(k)
    log_weights = []
    for cell in cells:
        d, e = to_mp(cell.d), to_mp(cell.e)
        mean = k * d
        lower = -mp.inf if cell.left is None else (to_mp(cell.left) - mean) / rootk
        upper = mp.inf if cell.right is None else (to_mp(cell.right) - mean) / rootk
        log_g = e + k * d * d / 2 + mp.log(2 * mp.pi * k) / 2 + log_normal_interval(lower, upper)
        log_weights.append(cell.log_z_base + log_g)
    log_q = mp_logsum(log_weights)
    target_logs = []
    for x in itertools.product((-1, 1), repeat=n):
        base = sum(j0[i][j] * x[i] * x[j] for i in range(n) for j in range(n)) / 2
        projection = sum(ai * xi for ai, xi in zip(a, x))
        energy = base + variance * projection * projection / 2 + sum(hi * xi for hi, xi in zip(h, x))
        target_logs.append(to_mp(energy))
    log_z = mp_logsum(target_logs)
    alpha = mp.exp(log_z + mp.log(2 * mp.pi * k) / 2 - log_q - mp.mpf(1) / 8)
    lower_bound = mp.mpf(3) / 4 * mp.exp(-mp.mpf(1) / 4)
    assert lower_bound - mp.mpf('1e-30') <= alpha <= 1 + mp.mpf('1e-30')
    return {"variance_rational": str(variance), "cells": len(cells), "log_Z": mp.nstr(log_z, 32), "ideal_acceptance": mp.nstr(alpha, 28), "universal_acceptance_lower_bound": mp.nstr(lower_bound, 28)}


def general_rank_pointwise(seed: int = 20261012, trials: int = 240) -> dict:
    rng = np.random.default_rng(seed)
    min_acceptance = 1.0
    max_log_acceptance = -math.inf
    max_identity_log_error = 0.0
    configurations = 0
    for case in range(trials):
        n = int(rng.integers(2, 9)); r = int(rng.integers(1, 5))
        s = states(n)
        b = rng.normal(size=(n, n))
        j0 = b.T @ b
        j0 *= 0.6 / np.linalg.norm(j0, 2)
        R = float(np.max(np.sum(np.abs(j0), axis=1) - np.abs(np.diag(j0))))
        L = math.ceil(R) + math.ceil(math.log2(4 * n))
        # Includes moderate and highly saturated regimes; very large exponents
        # are tested separately with rational arithmetic and mpmath.
        A = rng.normal(size=(r, n)) * 10.0 ** rng.uniform(-2, 3)
        h = rng.normal(size=n) * 10.0 ** rng.uniform(-2, 2)
        y = rng.normal(size=r) * 10.0 ** rng.uniform(-2, 1)
        ell = h + A.T @ y
        step = 1.0 / (4 * n)
        c = np.where(ell >= L, L, np.where(ell <= -L, -L, -L + (np.floor((ell + L) / step) + 0.5) * step))
        excess = np.maximum(np.abs(ell) - L, 0.0)
        base = 0.5 * np.einsum('bi,ij,bj->b', s, j0, s)
        log_base = base + s @ c
        base_probs = np.exp(log_base - logsumexp(log_base))
        # Compute the same exponent via excess signs to reduce cancellation.
        clipped = np.clip(ell, -L, L)
        log_accept = s @ (clipped - c) - 2 * ((s * np.sign(ell) < 0) @ excess) - 0.125
        avg = float(np.dot(base_probs, np.exp(log_accept)))
        min_acceptance = min(min_acceptance, avg)
        max_log_acceptance = max(max_log_acceptance, float(log_accept.max()))
        assert log_accept.max() <= 2e-10
        assert avg >= 0.75 * math.exp(-0.25) - 2e-10
        # Unnormalised accepted joint density equals e^(-1/8) times target.
        lhs = base + s @ c + float(excess.sum()) + log_accept
        rhs = base + s @ ell - 0.125
        err = float(np.max(np.abs(lhs - rhs)))
        max_identity_log_error = max(max_identity_log_error, err)
        assert err <= 2e-8
        configurations += len(s)
    return {"trials": trials, "spin_configuration_evaluations": configurations,
            "minimum_conditional_acceptance": min_acceptance,
            "maximum_log_acceptance": max_log_acceptance,
            "maximum_accepted_density_log_identity_error": max_identity_log_error}


def clipping_failure_example() -> dict:
    # n=1, A=1, h=0, variance beta. True Z=2 exp(beta/2).
    # Discarding the excess produces 2 E cosh(clip(Y,-L,L)) <= 2 cosh L.
    beta, L = 100, 4
    return {"beta": beta, "L": L, "true_log_Z": math.log(2) + beta / 2,
            "naively_clipped_log_Z_upper_bound": math.log(2 * math.cosh(L)),
            "description": "Clipping without retaining the affine excess can lose exponential partition mass."}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=Path('results.json'))
    args = parser.parse_args()
    mp.mp.dps = 90
    start = time.perf_counter()
    a = [F(1), F(-2, 3), F(5, 7), F(1, 4)]
    h = [F(2, 5), F(-1, 3), F(3, 8), F(-2, 7)]
    v = [F(1), F(-1), F(2), F(1)]
    j0 = [[F(1, 20) * vi * vj for vj in v] for vi in v]  # PSD, norm 7/20.
    cells, L = construct_rank_one(a, h, j0)
    mass_results = [rank_one_mass_check(a, h, j0, cells, k) for k in [F(1, 2**40), F(1, 4), F(1), F(16), F(2**40)]]
    result = {"status": "finite_diagnostics_passed_not_general_validation", "mpmath_decimal_precision": mp.mp.dps,
              "rank_one_n": len(a), "rank_one_L": L, "rank_one_mass_checks": mass_results,
              "general_rank_pointwise": general_rank_pointwise(),
              "failed_naive_clipping": clipping_failure_example(),
              "elapsed_seconds": time.perf_counter() - start,
              "limitations": ["Base law is exhaustively enumerated, not the polynomial high-temperature sampler.",
                              "No general-rank Gaussian-polyhedron integration engine is implemented.",
                              "High-precision floating arithmetic is not interval-certified.",
                              "These finite checks do not establish historical novelty or the general theorem."]}
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
