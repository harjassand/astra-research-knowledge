#!/usr/bin/env python3
"""Exact Clifford-moment replay for a rational Spin(15) pure-spinor seed."""
from __future__ import annotations

from itertools import combinations
from fractions import Fraction
from math import comb
from pathlib import Path
import hashlib
import json


NQ = 7
DIM = 1 << NQ
REAL = [-1,-6,2,-3,0,-2,10,-11,14,8,-7,0,1,-3,-3,-6,-2,-7,9,4,-4,-3,12,4,8,0,-1,2,-3,6,8,2,-4,8,0,9,7,6,16,1,-13,-6,-6,5,6,-5,1,-5,8,-2,-5,-13,-3,8,-7,-3,-6,-2,1,-4,0,1,-3,3,2,6,0,-6,-12,4,6,-4,12,-10,-5,4,3,-3,-7,2,-2,6,5,0,-1,-8,2,0,-2,0,-15,-5,7,-4,4,5,2,-7,-2,-5,-3,0,9,12,9,0,3,-1,1,-5,8,-6,9,-7,5,9,1,1,2,3,-1,6,-4,-3,11,5,2,4]
IMAG = [6,-4,-10,-12,11,-3,-6,-4,7,-1,-3,1,8,-7,-9,8,9,0,-4,11,3,1,-4,-7,-2,-9,3,6,8,4,10,3,3,-6,4,10,0,-6,-1,2,13,1,-9,-5,-5,11,-4,-9,8,-4,0,-7,5,-7,-3,4,-10,-4,-11,1,-5,2,-10,7,4,1,1,-4,8,-3,-2,1,-2,12,-3,-15,13,0,1,6,7,-1,-2,-7,-8,5,1,3,-4,-7,-3,1,-9,5,1,-3,-13,-3,-5,-9,1,5,8,6,0,9,5,-2,0,9,-1,-6,-8,-3,1,-8,5,-5,7,0,3,-4,-6,2,8,-6,-6,20]

PAULI_PRODUCT = {
    ('I','I'):(0,'I'),('I','X'):(0,'X'),('I','Y'):(0,'Y'),('I','Z'):(0,'Z'),
    ('X','I'):(0,'X'),('Y','I'):(0,'Y'),('Z','I'):(0,'Z'),
    ('X','X'):(0,'I'),('Y','Y'):(0,'I'),('Z','Z'):(0,'I'),
    ('X','Y'):(1,'Z'),('Y','X'):(3,'Z'),('Y','Z'):(1,'X'),
    ('Z','Y'):(3,'X'),('Z','X'):(1,'Y'),('X','Z'):(3,'Y'),
}


def gamma_words():
    out = []
    for q in range(NQ):
        out.extend((('Z',)*q + ('X',) + ('I',)*(NQ-q-1),
                    ('Z',)*q + ('Y',) + ('I',)*(NQ-q-1)))
    out.append(('Z',)*NQ)
    return out


def apply(word, basis):
    target = basis
    phase = 0
    for q, p in enumerate(word):
        bit = (basis >> q) & 1
        if p in ('X','Y'):
            target ^= 1 << q
        if p == 'Y':
            phase += 1 if bit == 0 else 3
        elif p == 'Z' and bit:
            phase += 2
    return target, phase % 4


def real_expectation_numerator(word, phase, norm_sq):
    total = 0
    for basis in range(DIM):
        target, local_phase = apply(word, basis)
        p = (phase + local_phase) % 4
        xr, yi = REAL[target], IMAG[target]
        xb, yb = REAL[basis], IMAG[basis]
        product_re = xr*xb + yi*yb
        product_im = xr*yb - yi*xb
        if p == 0:
            total += product_re
        elif p == 1:
            total -= product_im
        elif p == 2:
            total -= product_re
        else:
            total += product_im
    return total


def moment_numerators():
    gam = gamma_words()
    moments = []
    for k in range(1, NQ+1):
        score_num = 0
        for A in combinations(range(2*NQ+1), k):
            phase = 0
            word = ('I',)*NQ
            for a in A:
                p = 0
                out = []
                for x, y in zip(word, gam[a]):
                    q, z = PAULI_PRODUCT[x, y]
                    p = (p + q) % 4
                    out.append(z)
                phase = (phase + p) % 4
                word = tuple(out)
            phase = (phase + k*(k-1)//2) % 4
            num = real_expectation_numerator(word, phase, 1)
            score_num += num*num
        moments.append(Fraction(score_num, 1))
    return moments


def main():
    if len(REAL) != DIM or len(IMAG) != DIM:
        raise AssertionError('state coordinate count')
    norm_sq = sum(x*x+y*y for x,y in zip(REAL, IMAG))
    score_nums = []
    gam = gamma_words()
    for k in range(1, NQ+1):
        score_num = 0
        for A in combinations(range(2*NQ+1), k):
            phase = 0
            word = ('I',)*NQ
            for a in A:
                p = 0
                out = []
                for x, y in zip(word, gam[a]):
                    q, z = PAULI_PRODUCT[x, y]
                    p = (p + q) % 4
                    out.append(z)
                phase = (phase + p) % 4
                word = tuple(out)
            phase = (phase + k*(k-1)//2) % 4
            num = real_expectation_numerator(word, phase, norm_sq)
            score_num += num*num
        score_nums.append(score_num)
    moments = [Fraction(v, norm_sq*norm_sq) for v in score_nums]
    if sum(moments) != DIM - 1:
        raise AssertionError(('Parseval failed', sum(moments), DIM-1))
    support_56 = moments[4] + moments[5]
    result = {
        'status': 'EXACT_ATTAINED_PURE_SEED',
        'group': 'Spin(15)',
        'spinor_dimension': DIM,
        'state': {'real_numerators': REAL, 'imag_numerators': IMAG,
                  'common_amplitude_denominator': norm_sq},
        'grade_moments': [str(x) for x in moments],
        'parseval_sum': str(sum(moments)),
        'support_grade5_plus_grade6': str(support_56),
        'support_grade5_plus_grade6_decimal': float(support_56),
        'seed_family_support_grade5_plus_grade6': 62,
        'r0_star_required_support_for_alpha_e5_plus_e6': 63.0768180146715,
        'sha256_state_coordinates': hashlib.sha256((str(REAL)+str(IMAG)+str(norm_sq)).encode()).hexdigest(),
        'scope': 'One attained pure-spinor support value; not a support maximum or a full factor-two proof.',
    }
    out = Path(__file__).with_name('spin15_rational_seed_certificate.json')
    out.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
