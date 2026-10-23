#!/usr/bin/env python3
"""Known exact cases, tamper rejection, and explicitly numerical diagnostics."""
from pathlib import Path
from fractions import Fraction
from decimal import Decimal, getcontext
import copy
import json
import platform
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'src'))
from certified_jacobi import certify_jacobi, verify_certificate, cms_bounds, sturm_count_scaled


def require(ok, label):
    if not ok:
        raise RuntimeError(label)


def fraction(obj):
    return Fraction(int(obj['numerator']), int(obj['denominator']))


def contains_decimal(node, value):
    return Decimal(node['weight_lower']) <= value <= Decimal(node['weight_upper'])


def known_exact_cases():
    d = 1 << 32
    cases = [
        ('one', [7*d], [], [Fraction(7)], [Decimal(1)]),
        ('two_symmetric', [0, 0], [d], [Fraction(-1), Fraction(1)], [Decimal('0.5'), Decimal('0.5')]),
        ('two_asymmetric', [d, 4*d], [2*d], [Fraction(0), Fraction(5)], [Decimal('0.8'), Decimal('0.2')]),
        ('three_symmetric', [0, 0, 0], [d, d], None, [Decimal('0.25'), Decimal('0.5'), Decimal('0.25')]),
    ]
    results = []
    certificates = {}
    for name, a, b, values, weights in cases:
        cert = certify_jacobi(a, b, d)
        check = verify_certificate(cert, a, b, d)
        for i, node in enumerate(cert['nodes']):
            if values is not None:
                lo, hi = fraction(node['lower']), fraction(node['upper'])
                require(lo <= values[i] <= hi, f'{name}: known eigenvalue enclosure')
                require(node['exact_dyadic_root'], f'{name}: exact dyadic root was not detected')
            require(contains_decimal(node, weights[i]), f'{name}: known exact weight')
        if name == 'three_symmetric':
            neg, zero, pos = cert['nodes']
            nl, nu = fraction(neg['lower']), fraction(neg['upper'])
            pl, pu = fraction(pos['lower']), fraction(pos['upper'])
            require(nl < 0 and nu < 0 and nl*nl >= 2 and nu*nu <= 2, 'negative sqrt(2) bracket')
            require(pl > 0 and pu > 0 and pl*pl <= 2 and pu*pu >= 2, 'positive sqrt(2) bracket')
            require(fraction(zero['lower']) == fraction(zero['upper']) == 0, 'exact middle zero')
        results.append({'case': name, 'certification': cert['resource'], 'verification': check,
                        'maximum_weight_interval_width': cert['maximum_weight_interval_width']})
        certificates[name] = cert
    # Exact zero-handling: internal and terminal zeros in leading determinants.
    require(sturm_count_scaled([0, 0], [d], 0) == (1, False), 'internal Sturm zero')
    require(sturm_count_scaled([0, 0, 0], [d, d], 0) == (1, True), 'internal and terminal Sturm zeros')
    require(sturm_count_scaled([0, 0], [d], -d) == (0, True), 'strict count at first eigenvalue')
    require(sturm_count_scaled([0, 0], [d], d) == (1, True), 'strict count at second eigenvalue')
    # Exact CMS endpoint checks for the spectral measure of the 3x3 zero-diagonal
    # Jacobi matrix with unit off-diagonals, using only its leading 2x2 block.
    # Its atoms are -sqrt(2),0,sqrt(2), with weights 1/4,1/2,1/4.
    for t, true_cdf in [(Fraction(-2), Decimal(0)), (Fraction(-1), Decimal('0.25')),
                        (Fraction(-1, 2), Decimal('0.25')), (Fraction(0), Decimal('0.75')),
                        (Fraction(1, 2), Decimal('0.75')), (Fraction(1), Decimal('0.75')),
                        (Fraction(2), Decimal(1))]:
        band = cms_bounds(certificates['two_symmetric'], t)
        require(Decimal(band['lower']) <= true_cdf <= Decimal(band['upper']),
                'exact larger-measure CMS endpoint check')
    return results, certificates


def tamper_checks(cert):
    d = 1 << 32
    attempts = []
    for name, mutate in [
        ('input_binding', lambda c: c['diagonal_int'].__setitem__(0, '1')),
        ('weight_interval', lambda c: c['nodes'][0].__setitem__('weight_upper', '0.1')),
        ('ordered_index', lambda c: c['nodes'][0].__setitem__('index', 2)),
        ('sturm_count', lambda c: c['nodes'][0].__setitem__('lower_strict_sturm_count', 7)),
        ('physical_scale', lambda c: c['nodes'][0]['lower'].__setitem__('numerator', '0')),
    ]:
        bad = copy.deepcopy(cert)
        mutate(bad)
        try:
            verify_certificate(bad, [0, 0], [d], d)
        except (ValueError, ArithmeticError) as error:
            attempts.append({'case': name, 'rejected': True, 'reason': str(error)})
        else:
            raise RuntimeError('Failed to reject '+name)
    return attempts


def numerical_diagnostics():
    import numpy as np
    from scipy.linalg import eigh_tridiagonal
    rng = np.random.default_rng(20261021)
    d = 1 << 32
    results = []
    for n in [3, 8, 16, 32, 64]:
        a = [int(x) for x in np.rint(rng.normal(size=n)*d)]
        b = [int(x) for x in np.rint(rng.uniform(.25, 1.5, size=n-1)*d)]
        cert = certify_jacobi(a, b, d)
        checked = verify_certificate(cert, a, b, d)
        vals, vecs = eigh_tridiagonal(np.array(a)/d, np.array(b)/d, lapack_driver='stev')
        exact_mids = np.array([float((fraction(z['lower'])+fraction(z['upper']))/2) for z in cert['nodes']])
        weight_mids = np.array([float((Fraction(Decimal(z['weight_lower']))+Fraction(Decimal(z['weight_upper'])))/2) for z in cert['nodes']])
        root_difference = float(np.max(np.abs(vals-exact_mids)))
        weight_difference = float(np.max(np.abs(vecs[0, :]**2-weight_mids)))
        require(root_difference < 5e-13, 'SciPy node diagnostic')
        require(weight_difference < 5e-12, 'SciPy weight diagnostic')
        results.append({'n': n, 'certification': cert['resource'], 'verification': checked,
                        'maximum_weight_interval_width': cert['maximum_weight_interval_width'],
                        'max_SciPy_node_difference': root_difference,
                        'max_SciPy_weight_difference': weight_difference,
                        'SciPy_role': 'diagnostic reference only; not a proof or interval oracle'})
    # A measure from a larger Jacobi matrix, with the small leading block as its
    # Gaussian quadrature rule. This checks the intended CMS interpretation.
    a = [int(x) for x in np.rint(rng.normal(size=20)*d)]
    b = [int(x) for x in np.rint(rng.uniform(.4, 1.2, size=19)*d)]
    cert = certify_jacobi(a[:6], b[:5], d)
    vals, vecs = eigh_tridiagonal(np.array(a)/d, np.array(b)/d, lapack_driver='stev')
    weights = vecs[0, :]**2
    thresholds = list(np.linspace(vals[0]-1, vals[-1]+1, 101))
    # Include certified node interval boundaries; upper envelope deliberately
    # uses <= at equality and stays conservative.
    thresholds += [fraction(z[side]) for z in cert['nodes'] for side in ['lower', 'upper']]
    worst = 0.
    for threshold in thresholds:
        cdf = float(np.sum(weights[vals <= float(threshold)]))
        band = cms_bounds(cert, threshold)
        violation = max(float(Decimal(band['lower']))-cdf, cdf-float(Decimal(band['upper'])), 0.)
        worst = max(worst, violation)
    require(worst < 5e-12, 'CMS larger-measure diagnostic')
    return {'numpy': np.__version__, 'SciPy_cases': results,
            'CMS_diagnostic': {'full_dimension': 20, 'leading_Jacobi_dimension': 6,
                               'thresholds': len(thresholds), 'maximum_numerical_violation': worst}}


def main():
    wall, cpu = time.perf_counter(), time.process_time()
    # A low ambient Decimal precision challenges hidden context-dependent ops.
    getcontext().prec = 9
    known, certificates = known_exact_cases()
    tampering = tamper_checks(certificates['two_symmetric'])
    numeric = numerical_diagnostics()
    result = {'status': 'PASS', 'known_exact_cases': known, 'tamper_checks': tampering,
              'numerical_diagnostics': numeric, 'ambient_decimal_precision': getcontext().prec,
              'runtime': {'python': sys.version, 'platform': platform.platform()},
              'wall_seconds': time.perf_counter()-wall, 'cpu_seconds': time.process_time()-cpu,
              'scope': 'No numerical eigensolver enters certification or verification. SciPy is diagnostics only.'}
    path = ROOT/'results'/'certified_jacobi_checks.json'
    path.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    for name, cert in certificates.items():
        (ROOT/'results'/f'jacobi_known_{name}.json').write_text(json.dumps(cert, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
