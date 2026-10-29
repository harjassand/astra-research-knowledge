"""Exact general-channel witness intake from a proposed containment dual.

Complex entries are [real rational string, imaginary rational string].
No eval/sympify, optimizer, reference sampling or entropy approximation.
"""
from fractions import Fraction
from pathlib import Path
import hashlib
import json
import sys
import time
import sympy as sp


def rational(x):
    f = Fraction(x)
    return sp.Rational(f.numerator, f.denominator)


def matrix(rows):
    return sp.Matrix([[rational(x[0])+sp.I*rational(x[1]) for x in row]
                      for row in rows])


def real_scalar(x):
    x = sp.expand_complex(x)
    assert sp.im(x) == 0
    return sp.re(x)


def positive(x):
    assert x == x.conjugate().T
    minors = [real_scalar(x[:j, :j].det()) for j in range(1, x.rows+1)]
    assert all(value > 0 for value in minors)
    return minors


def encode(x):
    return [[[str(sp.re(value)), str(sp.im(value))] for value in row]
            for row in x.tolist()]


def main():
    start = time.perf_counter()
    source_path = Path(sys.argv[1]).resolve()
    data_bytes = source_path.read_bytes()
    data = json.loads(data_bytes)
    L = sp.Matrix([[rational(x) for x in row] for row in data['L']])
    K = sp.Matrix([[rational(x) for x in row] for row in data['K']])
    c = rational(data['c'])
    n, ell, m = L.cols, L.rows, K.rows
    b = m+1
    assert K.cols == n and c >= 0
    assert all(value > 0 for value in L) and all(value > 0 for value in K)
    assert all(sum(L[:, j]) == 1 and sum(K[:, j]) == 1 for j in range(n))
    y0 = matrix(data['Y0'])
    yq = [matrix(x) for x in data['Y_Q']]
    yr = [matrix(x) for x in data['Y_U_real']]
    yi = [matrix(x) for x in data['Y_U_imag']]
    assert len(yq) == len(yr) == len(yi) == n-1
    assert all(x.shape == (b, b) and x == x.conjugate().T
               for x in [y0]+yq+yr+yi)
    epsilon = rational(data['epsilon'])
    assert epsilon > 0
    G = (y0+epsilon*sp.eye(b)).T
    effects = [G/n+x.T for x in yq]
    effects.append(G/n-sum((x.T for x in yq), sp.zeros(b)))
    operators = [x.T+sp.I*y.T for x, y in zip(yr, yi)]
    operators.append(-sum(operators, sp.zeros(b)))
    positive(G)
    for effect in effects:
        positive(effect)
    assert sum(effects, sp.zeros(b)) == G
    assert sum(operators, sp.zeros(b)) == sp.zeros(b)
    forms = {}
    aggregate = {}
    for name, channel in [('L', L), ('K', K)]:
        es = [sum((channel[y, i]*effects[i] for i in range(n)), sp.zeros(b))
              for y in range(channel.rows)]
        fs = [sum((channel[y, i]*operators[i] for i in range(n)), sp.zeros(b))
              for y in range(channel.rows)]
        total = sp.zeros(b)
        for effect, operator in zip(es, fs):
            positive(effect)
            total += operator.conjugate().T*effect.inv()*operator
        total = total.applyfunc(sp.cancel)
        aggregate[name] = (es, fs, total)
        forms[name] = real_scalar(total[b-1, b-1])
    positive((G-aggregate['L'][2]).applyfunc(sp.cancel))
    assert forms['K'] > c*real_scalar(G[b-1, b-1])
    assert forms['L'] <= real_scalar(G[b-1, b-1])
    assert forms['K'] > c*forms['L']
    es, fs, _ = aggregate['K']
    score = sum(es[y][y, y] for y in range(m))
    score += sum(fs[y][y, b-1]+sp.conjugate(fs[y][y, b-1]) for y in range(m))
    score = real_scalar(score+c*G[b-1, b-1])
    assert score < 0
    result = {
        'status': 'EXACT_CENTERED_FREE_INFORMATION_VIOLATION',
        'source_path': str(source_path),
        'source_sha256': hashlib.sha256(data_bytes).hexdigest(),
        'reference_shape': [ell, n], 'release_shape': [m, n],
        'reference_dimension': b, 'tested_factor': str(c),
        'source_free_form': str(forms['L']), 'release_free_form': str(forms['K']),
        'ratio': str(forms['K']/forms['L']) if forms['L'] else 'INFINITE_KERNEL',
        'target_Omega_form': str(score), 'epsilon': str(epsilon),
        'G': encode(G), 'E': [encode(x) for x in effects],
        'h': [encode(x[:, b-1]) for x in operators],
        'matrix_square_roots_evaluated': 0,
        'solver_calls_or_reference_samples': 0,
        'finite_entropy_state_pair_acquired': False,
        'seconds_after_imports': time.perf_counter()-start,
    }
    output = source_path.with_name(source_path.stem+'_WITNESS.json')
    output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({key: value for key, value in result.items()
                      if key not in ('G', 'E', 'h')}, indent=2))


if __name__ == '__main__':
    main()
