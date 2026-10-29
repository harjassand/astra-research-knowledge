#!/usr/bin/env python3
"""Finite population diagnostics for the independently kicked transport model.

No Monte Carlo, acquired confidence, apparatus, or asymptotic theorem is
certified here. Sparse matrix exponentials compute finite-time current MGFs.
The original escape diagonal is retained in the tilted generator.
"""
from __future__ import annotations

import argparse
import itertools
import json
import math
from pathlib import Path

import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import expm_multiply


def configurations(n: int, particles: int) -> list[int]:
    return [sum(1 << i for i in c)
            for c in itertools.combinations(range(n), particles)]


def amplitude(mask: int, i: int, n: int, context: int, cap: float) -> float:
    """A frozen nonlocal amplitude, invariant under its own exchange."""
    j = (i + 1) % n
    field = 0.27 * math.cos((context + 1) * (i + 0.5))
    for k in range(n):
        if k not in (i, j):
            weight = math.sin((i + 1) * (k + 2) * math.sqrt(2)
                              + 0.7 * context)
            field += 0.65 * weight * (2 * ((mask >> k) & 1) - 1)
    return cap * math.tanh(field)


def build(n: int, particles: int, gamma: float, lam: float,
          context: int, cap: float = 0.85, s: float = 1.0,
          with_signs: bool = True) -> tuple[csr_matrix, list[int]]:
    configs = configurations(n, particles)
    indices = {m: i for i, m in enumerate(configs)}
    signs = 1 << n if with_signs else 1
    size = len(configs) * signs
    rows, cols, vals = [], [], []
    for ei, mask in enumerate(configs):
        for sm in range(signs):
            row = ei * signs + sm
            escape = 0.0
            for i in range(n):
                j = (i + 1) % n
                delta = ((mask >> i) & 1) - ((mask >> j) & 1)
                if not delta:
                    continue
                swapped = mask ^ (1 << i) ^ (1 << j)
                alpha = amplitude(mask, i, n, context, cap) if with_signs else 0.
                if with_signs:
                    assert abs(alpha - amplitude(swapped, i, n, context, cap)) < 1e-14
                sigma = 1 - 2 * ((sm >> i) & 1)
                rate = n * n * s * (1 + alpha * sigma) / 2
                assert rate > 0
                rows.append(row)
                cols.append(indices[swapped] * signs + sm)
                vals.append(rate * math.exp(lam * delta / n))
                escape += rate
            if with_signs and gamma:
                for i in range(n):
                    rows.append(row)
                    cols.append(ei * signs + (sm ^ (1 << i)))
                    vals.append(n * n * gamma)
                    escape += n * n * gamma
            rows.append(row)
            cols.append(row)
            vals.append(-escape)
    return csr_matrix((vals, (rows, cols)), shape=(size, size)), configs


def log_mgf(n: int, particles: int, gamma: float, lam: float,
            context: int, horizon: float, cap: float = .85,
            with_signs: bool = True) -> tuple[float, int]:
    matrix, configs = build(n, particles, gamma, lam, context, cap,
                            with_signs=with_signs)
    initial_mask = sum(1 << i for i in range(0, n, 2))
    if initial_mask.bit_count() != particles:
        initial_mask = configs[0]
    signs = 1 << n if with_signs else 1
    initial = configs.index(initial_mask) * signs  # All signs recorded +1.
    values = expm_multiply(horizon * matrix, np.ones(matrix.shape[0]),
                           traceA=horizon * matrix.diagonal().sum())
    assert np.isfinite(values[initial]) and values[initial] > 0
    return math.log(float(values[initial])) / n, matrix.shape[0]


def run(horizon: float) -> dict:
    structural = []
    for n in (4, 6):
        q, _ = build(n, n // 2, 1.3, 0., 1)
        row_error = float(np.max(np.abs(q @ np.ones(q.shape[0]))))
        symmetry_error = float(np.max(np.abs((q - q.T).data))) if (q - q.T).nnz else 0.
        assert row_error < 1e-10 and symmetry_error < 1e-10
        a, _ = log_mgf(n, n // 2, 1.3, 1.7, 1, horizon, cap=0.)
        b, _ = log_mgf(n, n // 2, 0., 1.7, 1, horizon, with_signs=False)
        assert abs(a - b) < 2e-10
        structural.append(dict(n=n, zero_tilt_row_error=row_error,
                               detailed_balance_error=symmetry_error,
                               zero_modulation_reduction_error=abs(a-b)))
    rows = []
    for n in (4, 6):
        for lam in (-3., 3.):
            baseline, _ = log_mgf(n, n // 2, 0., lam, 0, horizon,
                                  with_signs=False)
            asymptotic = .5 * .25 * horizon * lam * lam
            for context in (0, 1):
                for gamma in (0., .5, 2., 8., 32.):
                    value, states = log_mgf(n, n // 2, gamma, lam,
                                            context, horizon)
                    rows.append(dict(n=n, states=states, context=context,
                                     gamma=gamma, lambda_=lam,
                                     log_mgf_per_site=value,
                                     exact_finite_n_ssep=baseline,
                                     limiting_flat_formula=asymptotic,
                                     error_to_finite_n_ssep=value-baseline))
    return dict(scope="Deterministic floating-point finite population matrix checks; not data acquisition or an LDP proof.",
                horizon_macro=horizon, physical_horizon="n^2 * horizon_macro",
                s=1., amplitude_cap=.85, initial_signs="all +1, retained",
                initial_visible="alternating half-filled ring",
                normalization="N^-1 log E exp(lambda * sum signed jumps / N)",
                structural_checks=structural, results=rows)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--horizon", type=float, default=.3)
    parser.add_argument("--output", type=Path,
                        default=Path(__file__).with_name("RARE_TRANSPORT_CHECK.json"))
    args = parser.parse_args()
    result = run(args.horizon)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    for n in (4, 6):
        rr = [r for r in result["results"] if r["n"] == n]
        print(json.dumps(dict(n=n, states=rr[0]["states"],
                              max_error_frozen=max(abs(r["error_to_finite_n_ssep"]) for r in rr if r["gamma"] == 0),
                              max_error_gamma32=max(abs(r["error_to_finite_n_ssep"]) for r in rr if r["gamma"] == 32))))
    print(str(args.output))
