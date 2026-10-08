"""Exact pair-spectrum and explicit-seed replay for Spin(13), d=64.

This avoids the triple-spinor finitecompiler. It computes pair eigenvalues by
Clifford conjugation and moments for five explicit computational-basis seeds.
It does not certify the full mixed-grade star inequality.
"""
from itertools import combinations
from math import comb
from pathlib import Path
import json
import sympy as sp

N = 6
M = 2 * N + 1
D = 1 << N


def pair_eigen(k, ell):
    """Eigenvalue of C_k on Clifford grade ell in S* tensor S.

    With column vectorization, C_k=sum_{|A|=k} T_A^T tensor T_A acts as
    X -> sum_A T_A X T_A. For a k-blade A and ell-blade B, conjugation has
    sign (-1)^(k*ell-|A intersect B|).
    """
    return sum(((-1) ** (k * ell - r)) * comb(ell, r) * comb(M - ell, k - r)
               for r in range(max(0, k + ell - M), min(k, ell) + 1))


def pmul(a, b):
    tab = {('I','I'):(0,'I'),('I','X'):(0,'X'),('I','Y'):(0,'Y'),('I','Z'):(0,'Z'),
           ('X','I'):(0,'X'),('Y','I'):(0,'Y'),('Z','I'):(0,'Z'),('X','X'):(0,'I'),
           ('Y','Y'):(0,'I'),('Z','Z'):(0,'I'),('X','Y'):(1,'Z'),('Y','X'):(3,'Z'),
           ('Y','Z'):(1,'X'),('Z','Y'):(3,'X'),('Z','X'):(1,'Y'),('X','Z'):(3,'Y')}
    phase = 0
    out = []
    for x, y in zip(a, b):
        q, z = tab[x, y]
        phase = (phase + q) % 4
        out.append(z)
    return phase, tuple(out)


def gamma_words():
    out = []
    for q in range(N):
        pre, suf = ('Z',) * q, ('I',) * (N - q - 1)
        out.extend((pre + ('X',) + suf, pre + ('Y',) + suf))
    out.append(('Z',) * N)
    return out


GAM = gamma_words()


def clifford_words(k):
    for A in combinations(range(M), k):
        phase = 0
        word = ('I',) * N
        for a in A:
            q, word = pmul(word, GAM[a])
            phase = (phase + q) % 4
        phase = (phase + k * (k - 1) // 2) % 4
        yield A, phase, word


def apply_word(word, bits):
    out, phase = bits, 0
    for q, p in enumerate(word):
        bit = (bits >> q) & 1
        if p == 'X':
            out ^= 1 << q
        elif p == 'Y':
            out ^= 1 << q
            phase += 1 if bit == 0 else 3
        elif p == 'Z' and bit:
            phase += 2
    return out, phase % 4


def seed_moments(a, b=None):
    """Moments sum_{|A|=k}|<psi,T_A psi>|^2 for |a> or (|a>+|b>)/sqrt(2)."""
    amplitudes = {a: 1} if b is None else {a: 1, b: 1}
    denominator = len(amplitudes)
    result = []
    for k in range(1, N + 1):
        score = sp.Integer(0)
        for _A, phase, word in clifford_words(k):
            expectation = sp.Integer(0)
            for source, amplitude in amplitudes.items():
                target, q = apply_word(word, source)
                if target in amplitudes:
                    expectation += sp.I ** (phase + q) * amplitudes[target] * amplitude / denominator
            expectation = sp.simplify(expectation)
            if expectation.is_real is not True:
                raise AssertionError(('nonreal expectation', k, _A, expectation))
            score += expectation ** 2
        result.append(int(sp.factor(score)))
    if sum(result) != D - 1:
        raise AssertionError(('Parseval', result, sum(result)))
    return tuple(result)


def main():
    seeds = {'basis_0': seed_moments(0)}
    for h in range(3, N + 1):
        seeds[f'two_weight_{h}'] = seed_moments(0, (1 << h) - 1)

    pair = [[pair_eigen(k, ell) for ell in range(N + 1)] for k in range(1, N + 1)]
    trace_coefficients = [comb(M, k) for k in range(1, N + 1)]
    if [row[0] for row in pair] != trace_coefficients:
        raise AssertionError(('singlet eigenvalues', pair))
    if [sum(pair[k - 1][ell] for k in range(1, N + 1)) for ell in range(1, N + 1)] != [-1] * N:
        raise AssertionError(('full traceless basis normalization', pair))

    c0 = trace_coefficients[0]
    b = max(pair[0][1:])
    coarse_star_bound = sp.Rational(c0 + b) + sp.Rational(c0 - b, D)
    e1_trace_plus_exact_support = sp.Integer(c0 + 1)
    result = {
        'status': 'COARSE_BOUND_INSUFFICIENT',
        'scope': 'Spin(13), d=64. Exact pair spectrum and five attained seed moment vectors; no exact triple-star or all-seed support calculation.',
        'pair_eigenvalues_rows_k_columns_ell0_to_6': pair,
        'trace_coefficients': trace_coefficients,
        'attained_seed_moments_grades1_to6': {name: list(v) for name, v in seeds.items()},
        'e1_control': {
            'c0': c0,
            'nontrivial_pair_eigenvalues': pair[0][1:],
            'b_max_nontrivial_eigenvalue': b,
            'coarse_star_upper_bound': str(coarse_star_bound),
            'trace_plus_exact_canonical_support': str(e1_trace_plus_exact_support),
            'coarse_bound_gap': str(sp.factor(coarse_star_bound - e1_trace_plus_exact_support)),
            'interpretation': 'The pair-singlet compression is too weak already for the vector-grade equality control; this is a failed sufficient bound, not a star violation.'
        },
        'pair_formula': 'c_{k,ell}=sum_{r=max(0,k+ell-13)}^{min(k,ell)} (-1)^(k*ell-r) binom(ell,r) binom(13-ell,k-r)',
        'coarse_bound_formula': 'If c0>=b=max_{ell>=1} c_ell(alpha), then lambda_max(H_alpha)<=c0+b+(c0-b)/64, by C_alpha<=b I+(c0-b)P0 and lambda_max(P0_RB+P0_RC)=1+1/64.',
        'seed_cost': 'Five seeds; 4095 nonidentity Clifford words replayed per seed using exact integer/rational arithmetic.'
    }
    Path(__file__).with_name('spin13_pair_support_certificate.json').write_text(json.dumps(result, indent=2) + '\n')
    print('pair eigenvalue table:', pair)
    print('seed moments:', seeds)
    print('e1 control:', result['e1_control'])
    print('CERTIFICATE WRITTEN: exact pair spectrum and seed replay; star bound remains insufficient')


if __name__ == '__main__':
    main()
