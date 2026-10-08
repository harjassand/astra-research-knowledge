"""New rank-deficit conventions only; not a uniform or external proof.

Exact CP2 radial Berezin Gram energies are evaluated independently of the
Casimir comparison. Small nonnormal matrices check the right-kernel Green
normalization. Importing earlier helper definitions does not rerun old tests.
"""
import importlib.util
import json
import math
from fractions import Fraction
from pathlib import Path

import numpy as np


def dimension(m):
    return (m + 1) * (m + 2) // 2


def radial_gram(m):
    d = dimension(m)
    return [[Fraction(2 * d * math.comb(m, n) * math.comb(m, t)
                      * math.factorial(n + t + 1)
                      * math.factorial(2 * m - n - t),
                      math.factorial(2 * m + 2))
             for t in range(m + 1)] for n in range(m + 1)]


def cap(m, q):
    k = 0
    while (k + 2) * (k + 3) // 2 <= q:
        k += 1
    return [Fraction(max(k + 1 - n, 0), k + 1)
            for n in range(m + 1)], 'cap'


def filter_for(m, q):
    d = dimension(m)
    h = d - q
    if q * 2 <= d or m < 8 or 128 * h > m * m:
        return cap(m, q)
    r = math.isqrt(2 * h)
    if r * r < 2 * h:
        r += 1
    b = 2 * r
    assert b * 2 <= m
    terms = [Fraction(1, (m - n) * (n + 1) * (n + 2))
             for n in range(r - 1, b)]
    resistance = sum(terms, Fraction(0))
    f = [Fraction(0) for n in range(m + 1)]
    for n in range(r, b):
        f[n] = sum(terms[:n - r + 1], Fraction(0)) / resistance
    for n in range(b, m + 1):
        f[n] = Fraction(1)
    return f, 'resistance'


def radial_cases():
    cases = []
    for m in (1, 2, 4, 8, 16, 32):
        d = dimension(m)
        gram = radial_gram(m)
        # Complete for the smallest two carriers, selected disparate ranks
        # otherwise. The near-full fixtures are new to this evidence file.
        budgets = (set(range(1, d)) if m <= 2 else
                   {1, 2, d // 4, d // 2, d // 2 + 1,
                    d - 1, d - 2, d - 3, d - 8})
        for q in sorted(x for x in budgets if 1 <= x < d):
            f, mode = filter_for(m, q)
            rank = sum(x != 0 for x in f)
            assert rank <= q
            norm = sum(Fraction(n + 1) * f[n] ** 2
                       for n in range(m + 1))
            symbol_energy = sum(gram[n][t] * f[n] * f[t]
                                for n in range(m + 1)
                                for t in range(m + 1))
            energy = norm - symbol_energy
            cas = sum(Fraction((m - n) * (n + 1) * (n + 2))
                      * (f[n + 1] - f[n]) ** 2 for n in range(m))
            assert 0 <= energy <= cas / m
            error = float(energy / norm)
            profile = math.sqrt(1 / q - 1 / d)
            assert error <= 64 * profile
            cases.append({'m': m, 'd': d, 'Q': q, 'actual_rank': rank,
                          'mode': mode, 'exact_energy': str(energy),
                          'exact_norm': str(norm), 'pure_error': error,
                          'error_over_profile': error / profile})
    return cases


def kernel_cases():
    helper = Path(__file__).with_name('check_cold_carrier.py')
    spec = importlib.util.spec_from_file_location('cold_helpers', helper)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rng = np.random.default_rng(81179)
    cases = []
    c0 = 1 - math.exp(-1)
    g0 = 4 / c0 * (1 + 11 * math.sqrt(2) / 3)
    for m in (1, 2, 3, 4):
        _, _, shells = module.representation(m)
        d = dimension(m)
        a = [1 - math.factorial(m) * math.factorial(m + 2) /
             (math.factorial(m - ell) * math.factorial(m + ell + 2))
             for ell in range(m + 1)]
        for h in sorted({1, 2, max(1, d // 4), (d - 1) // 2}):
            if h * 2 >= d:
                continue
            z = rng.normal(size=(d, h)) + 1j * rng.normal(size=(d, h))
            v, _ = np.linalg.qr(z)
            p = v @ v.conj().T
            aa = ((rng.normal(size=(d, d)) +
                   1j * rng.normal(size=(d, d))) @ (np.eye(d) - p))
            aa /= np.linalg.norm(aa, 'fro')
            assert np.linalg.norm(aa @ p, 'fro') < 1e-12
            flatp, flata = p.ravel(order='F'), aa.ravel(order='F')
            mass = [float(np.vdot(flatp, pi @ flatp).real) for pi in shells]
            amass = [float(np.vdot(flata, pi @ flata).real) for pi in shells]
            for ell in range(m + 1):
                assert mass[ell] <= h * h * (ell + 1) ** 3 / d + 1e-11
            green = sum(mass[ell] / a[ell] for ell in range(1, m + 1))
            energy = sum(amass[ell] * a[ell] for ell in range(1, m + 1))
            master = 1 / (d * green / (h * h) + (m + 3) / 3)
            assert energy >= master - 1e-11
            assert green <= g0 * h ** 1.5 + 1e-11
            cases.append({'m': m, 'd': d, 'h': h,
                          'green': green, 'Berezin_energy': energy,
                          'master_lower': master,
                          'kernel_residual': float(np.linalg.norm(aa @ p))})
    return cases


def main():
    radial = radial_cases()
    kernel = kernel_cases()
    result = {'status': 'FINITE-EVIDENCE',
              'scope': 'New exact radial Berezin rank-deficit energies and '
                       'small nonnormal right-kernel Green conventions only',
              'radial_fixture_count': len(radial),
              'right_kernel_fixture_count': len(kernel),
              'maximum_filter_error_over_profile':
                  max(x['error_over_profile'] for x in radial),
              'radial_fixtures': radial, 'right_kernel_fixtures': kernel,
              'old_tests_rerun': False,
              'uniform_or_external_validation': False}
    Path(__file__).with_suffix('.json').write_text(
        json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items()
                      if k not in ('radial_fixtures', 'right_kernel_fixtures')},
                     indent=2))


if __name__ == '__main__':
    main()
