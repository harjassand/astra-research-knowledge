"""Independent finite-configuration checks and a deliberately invalid witness.

Run with ordinary Python (not python -O). Uses only the standard library.
The brute-force checks use the original trial-functional definition, rather
than the verifier's centered-monomial contraction.
"""
from __future__ import annotations
from copy import deepcopy
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
from verify import verify_lower, verify_upper, verify_file


def brute_upper(p: F) -> F:
    sites = tuple(range(-3, 5))
    t = 1 / ((p - 3) * (p + 1))
    answer = F(0)
    def f(eta: dict[int, int], shift: int) -> F:
        h = {i: F(eta[shift+i]) - p for i in range(4)}
        return t * (h[0]*h[1]*h[3] - h[0]*h[2]*h[3])
    for bits in product((0, 1), repeat=len(sites)):
        eta = dict(zip(sites, bits))
        c = 1 - eta[-1]*eta[2]
        if not c:
            continue
        swapped = eta.copy()
        swapped[0], swapped[1] = eta[1], eta[0]
        gf = sum((f(swapped, shift)-f(eta, shift) for shift in range(-3, 2)), F(0))
        weight = p**sum(bits) * (1-p)**(len(bits)-sum(bits))
        answer += weight * (eta[0]-eta[1]+gf)**2
    return answer/(2*p*(1-p))


def run() -> None:
    root = Path(__file__).parent
    for p in (F(1, 2), F(4, 5), F(19, 20), F(1, 3)):
        q = 1-p
        k = 1/(1+q)
        witness = {'density': str(p), 'scale': k.denominator,
                   'dual': {'outer': [-1, 2], 'terms': [
                       {'shape': [], 'numerator': 2*k.numerator},
                       {'shape': [-1], 'numerator': -k.numerator},
                       {'shape': [2], 'numerator': -k.numerator}]}}
        assert verify_lower(witness) == 2*q/(1+q)
        t = 1/((p-3)*(p+1))
        upper = {'density': str(p), 'scale': t.denominator,
                 'primal': {'terms': [
                     {'shape': [0, 1, 3], 'numerator': t.numerator},
                     {'shape': [0, 2, 3], 'numerator': -t.numerator}]}}
        expected = (1-p)*(p**3-p**2+5*p+3)/((3-p)*(p+1))
        assert verify_upper(upper) == expected == brute_upper(p)
    sample = json.loads((root/'certificate_1_2.json').read_text())
    broken = deepcopy(sample)
    broken['dual']['terms'].append({'shape': [], 'numerator': 1})
    try:
        verify_lower(broken)
    except AssertionError:
        pass
    else:
        raise AssertionError('The deliberately nonconservative current was accepted.')
    for path in sorted(root.glob('certificate_*.json')):
        verify_file(path)
    print('PASS: exact baseline lower bounds, direct 256-state upper checks at four densities,')
    print('      rejection of a one-unit current perturbation, and all three certificates.')


if __name__ == '__main__':
    run()
