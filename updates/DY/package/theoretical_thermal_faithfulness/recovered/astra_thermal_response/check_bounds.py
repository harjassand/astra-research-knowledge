#!/usr/bin/env python3
"""Finite-dimensional falsification checks for local thermal-response bounds.

These floating-point checks are not a proof or independent verification.
Run: python check_bounds.py --output checks.json
Requires Python 3.10+, NumPy and SciPy. No network access is used.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import numpy as np
from numpy.typing import NDArray
from scipy.linalg import eigh

Matrix = NDArray[np.complex128]


def random_hermitian(rng: np.random.Generator, dimension: int) -> Matrix:
    z = rng.normal(size=(dimension, dimension)) + 1j * rng.normal(size=(dimension, dimension))
    return (z + z.conj().T) / 2


def thermal_data(h: Matrix, x: Matrix, beta: float) -> tuple[float, float, NDArray, Matrix]:
    energies, vectors = eigh(h)
    probabilities = np.exp(-beta * (energies - energies.min()))
    probabilities /= probabilities.sum()
    xe = vectors.conj().T @ x @ vectors
    weights = np.sqrt(probabilities[:, None] * probabilities[None, :]) * np.abs(xe)**2
    return float(weights.sum().real), float(np.trace(xe @ np.diag(probabilities)).real), energies, weights


def dimension_counterexample(d: int, dense: bool = False) -> dict:
    """Traceless Hermitian example with bath dimension d-1 and ||V||=beta=1."""
    if d < 4 or d % 2:
        raise ValueError('d must be even and at least four')
    m = 4 * np.log(d)
    r = 2 / (np.sqrt(m*m + 4) + m)
    z = 2 + (d-2)*(np.exp(r)+np.exp(-1/r)) + (d-2)*(d-1)*np.exp(-m)
    numerator = (2 + (d-2)*(np.exp(-1/r)*(1-r*r)**2 + 2*np.exp(-m/2)*r*r)
                 + np.exp(-m)*((d-2)+(d-2)**2*r**4))
    kms = numerator/z
    hs = (2+(d-2)*r**4)/d
    result = {'d': d, 'bath_dimension': d-1, 'M': float(m), 'r': float(r),
              'kms': float(kms), 'tracial_second_moment': float(hs),
              'kms_to_tracial_ratio': float(kms/hs), 'upper_bound_3_over_d': 3/d}
    if dense:
        bdim = d-1
        k = np.diag([0.] + [m]*(bdim-1))
        h = np.kron(np.eye(d), k).astype(complex)
        local_x = np.zeros(d)
        local_x[0], local_x[1] = 1, -1
        for j in range(2, d):
            sign = 1 if j % 2 == 0 else -1
            local_x[j] = sign*r*r
            extreme = 1 if sign == 1 else 0
            low, high = j*bdim, extreme*bdim+(j-1)
            h[low, high] = h[high, low] = 1
        x = np.kron(np.diag(local_x), np.eye(bdim))
        actual, mean, _, _ = thermal_data(h, x, 1.)
        result['dense_formula_absolute_error'] = abs(actual-kms)
        result['dense_thermal_mean_absolute_value'] = abs(mean)
        assert np.isclose(actual, kms, rtol=1e-10, atol=1e-12)
        assert abs(mean) < 1e-10
    assert kms <= 3/d + 1e-12
    return result


def run_checks(seed: int = 19371) -> dict:
    rng = np.random.default_rng(seed)
    minima = {'kms_bound_ratio': float('inf'), 'finite_band_bound_ratio': float('inf'),
              'rank_profile_bound_ratio': float('inf'), 'spectral_leakage_margin': float('inf')}
    worst_compression_excess = 0.
    count = 0
    for d in (2, 3, 4):
        for bdim in (1, 2, 4, 7):
            for _ in range(25):
                k = random_hermitian(rng, bdim) * 10**rng.uniform(-1, 2)
                vmat = random_hermitian(rng, d*bdim)
                vmat *= 10**rng.uniform(-1, .3)/np.linalg.norm(vmat, 2)
                v = float(np.linalg.norm(vmat, 2))
                local_x = rng.normal(size=(d, d)) + 1j*rng.normal(size=(d, d))
                x = np.kron(local_x, np.eye(bdim))
                h0 = np.kron(np.eye(d), k)
                h = h0 + vmat
                beta = 10**rng.uniform(-2, .6)
                kms, _, energies, weights = thermal_data(h, x, beta)
                norm_x = float(np.linalg.norm(local_x, 2))
                lower = 4/(9*d)*np.exp(-4*beta*v)*norm_x**2
                band_lower = np.exp(-5*beta*v)/(72*d)*norm_x**2
                band_mass = float(weights[np.abs(energies[:, None]-energies[None, :]) <= 7*v].sum())
                singular = np.linalg.svd(local_x, compute_uv=False)
                profile_lower = np.exp(-4*beta*v)/d*np.maximum(singular-norm_x/3, 0).dot(np.maximum(singular-norm_x/3, 0))
                ratios = {'kms_bound_ratio': kms/lower,
                          'finite_band_bound_ratio': band_mass/band_lower,
                          'rank_profile_bound_ratio': kms/profile_lower}
                for name, value in ratios.items():
                    minima[name] = min(minima[name], float(value))
                    assert value >= 1-1e-8, (name, value, d, bdim, beta, v)
                e0, u0 = eigh(h0)
                e, u = eigh(h)
                cutoff = float(rng.choice(e0)) + 1e-8
                p0 = u0[:, e0 <= cutoff] @ u0[:, e0 <= cutoff].conj().T
                p = u[:, e <= cutoff+3*v] @ u[:, e <= cutoff+3*v].conj().T
                q = np.eye(d*bdim)-p
                leakage = float(np.linalg.norm(q@p0, 2))
                minima['spectral_leakage_margin'] = min(minima['spectral_leakage_margin'], 1/3-leakage)
                error = float(np.linalg.norm(p0@p@x@p@p0-p0@x@p0, 2))
                excess = error-3*leakage**2*norm_x
                worst_compression_excess = max(worst_compression_excess, excess)
                assert leakage <= 1/3+1e-8
                assert excess <= 1e-8*max(1., norm_x)
                count += 1
    counterexamples = [dimension_counterexample(d, dense=(d <= 10))
                       for d in (4, 6, 10, 100, 10_000, 1_000_000, 10**10, 10**16)]
    return {'status': 'all programmed finite checks passed within stated floating-point tolerances',
            'qualification': 'not a proof, formal verification, or independent review',
            'seed': seed, 'random_cases': count, 'minimum_ratios_and_margin': minima,
            'max_compression_inequality_excess': worst_compression_excess,
            'counterexample_family': counterexamples,
            'numpy_version': np.__version__}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=Path('checks.json'))
    args = parser.parse_args()
    result = run_checks()
    args.output.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
