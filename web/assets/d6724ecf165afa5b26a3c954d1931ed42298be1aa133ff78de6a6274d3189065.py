"""New thermal epsilon-lift N1 contrasts; not an iid/uniform proof."""
import importlib.util
import json
import math
from fractions import Fraction
from pathlib import Path

import numpy as np


def helpers():
    path = Path(__file__).with_name('check_iid_transfer_gate.py')
    spec = importlib.util.spec_from_file_location('epsilon_helpers', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def exact_i(m, k, q):
    total = m + k
    z = sum(Fraction(n + 1) * q ** n for n in range(total + 1))
    values = []
    d = (total + 1) * (total + 2) // 2
    for i in range(k + 1):
        f = Fraction(0)
        moment = Fraction(1)
        for ell in range(i + 1):
            if ell:
                moment *= Fraction(ell + 2, total - i + ell + 2)
            f += (-1) ** ell * math.comb(i, ell) * (1 - q) ** ell * moment
        values.append(Fraction(4 * d, 1) * q * f /
                      (z * (total - i) * (total - i + 1) * (total - i + 2)))
    r = k + 1
    plus = Fraction(m, r * r * (k + 2)) * sum(
        Fraction(i + 1) * values[i] for i in range(k + 1))
    minus = Fraction(m + k + 1, r * r * k) * sum(
        Fraction(k - i) * values[i] for i in range(k + 1))
    return plus, minus, values, z


def actual_coefficients(module, m, k, q):
    hot, cold, source = (module.occupations(k), module.occupations(m),
                         module.occupations(m + k))
    hi, ci = {n: i for i, n in enumerate(hot)}, {n: i for i, n in enumerate(cold)}
    split = np.zeros((len(cold), len(hot), len(source)), complex)
    for col, n in enumerate(source):
        for a in cold:
            b = tuple(n[i] - a[i] for i in range(3))
            if min(b) < 0 or b not in hi:
                continue
            split[ci[a], hi[b], col] = math.sqrt(
                math.factorial(m) * math.factorial(k) * module.factorial_product(n) /
                (math.factorial(m + k) * module.factorial_product(a) * module.factorial_product(b)))
    iso = np.einsum('abx,fcb->facx', split, module.epsilon_isometry(k))
    probability = np.array([float(q) ** (m + k - n[2]) for n in source])
    probability /= probability.sum()
    rho = np.einsum('facx,x,gbcx->fagb', iso, probability, iso.conj()).reshape(
        len(hot) * len(cold), len(hot) * len(cold))
    layer = [i * len(cold) + j for i, h in enumerate(hot)
             for j, c in enumerate(cold) if h[2] + m - c[2] == 1]
    rho1 = rho[np.ix_(layer, layer)]
    j2 = np.zeros_like(rho1)
    gh, gc = module.generators(k), module.generators(m)
    for a in (0, 1, 6):
        ja = np.kron(gh[a], np.eye(len(cold))) - np.kron(np.eye(len(hot)), gc[a].T)
        ja = ja[np.ix_(layer, layer)]
        j2 += ja @ ja
    eig, vec = np.linalg.eigh(j2)
    plus_j, minus_j = (k + 1) / 2, (k - 1) / 2
    plus = np.abs(eig - plus_j * (plus_j + 1)) < 1e-8
    minus = np.abs(eig - minus_j * (minus_j + 1)) < 1e-8
    assert plus.sum() == k + 2
    assert minus.sum() == 2 * k
    # The extra minus copy is outside the harmonic carrier and has zero
    # weight in this output; trace divided by k is the physical eigenvalue.
    pplus = vec[:, plus] @ vec[:, plus].conj().T
    pminus = vec[:, minus] @ vec[:, minus].conj().T
    return (float(np.trace(pplus @ rho1).real / (k + 2)),
            float(np.trace(pminus @ rho1).real / k))


def main():
    module = helpers()
    matrix = []
    for m, k in ((1, 1), (2, 1), (1, 2), (2, 2), (2, 3)):
        for q in (Fraction(1, 4), Fraction(1, 2), Fraction(3, 4)):
            plus, minus, _, _ = exact_i(m, k, q)
            actual = actual_coefficients(module, m, k, q)
            error = max(abs(actual[0] - float(plus)), abs(actual[1] - float(minus)))
            assert error < 1e-12
            matrix.append({'m': m, 'k': k, 'q': str(q),
                           'plus': float(plus), 'minus': float(minus),
                           'complete_channel_error': error})
    asymptotic = []
    for m in (16, 64, 256, 1024):
        k = math.isqrt(m)
        total = m + k
        for q in (Fraction(1, 4), Fraction(1, 2), Fraction(3, 4)):
            plus, minus, values, z = exact_i(m, k, q)
            assert minus > plus
            for i, value in enumerate(values):
                remainder = abs(value / values[0] - 1 - Fraction(3, 1) * q * i / total)
                assert remainder <= Fraction(200 * (i * i + i), total * total)
            bracket = (minus - plus) * z * total / q
            assert abs(bracket - (1 - q)) <= Fraction(602 * k, total)
            gap = k * (minus - plus)
            expected = q * (1 - q) ** 3 * Fraction(k, total)
            asymptotic.append({'m': m, 'k': k, 'q': str(q),
                               'exact_witness_gap': str(gap),
                               'gap_over_leading': float(gap / expected)})
    result = {'status': 'FINITE-EVIDENCE',
              'scope': '15 complete thermal converter N1 component coefficients '
                       'and 12 exact critical-scale beta/witness fixtures only',
              'matrix_cases': matrix, 'critical_scale_cases': asymptotic,
              'max_complete_channel_error': max(x['complete_channel_error'] for x in matrix),
              'last_scale_gap_ratios': [x['gap_over_leading'] for x in asymptotic if x['m'] == 1024],
              'old_suites_rerun': False,
              'uniform_external_or_iid_validation': False}
    Path(__file__).with_suffix('.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items()
                      if k not in ('matrix_cases', 'critical_scale_cases')}, indent=2))


if __name__ == '__main__':
    main()
