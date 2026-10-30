#!/usr/bin/env python3
"""Exact finite-word checks and analytic phase/noise certificates.

Standard library only. These checks support PROOF.md; they are not a
numerical substitute for its uniform statements.
"""
from fractions import Fraction as F
from math import factorial, pi, tan, sqrt
import cmath


# Exact Gaussian rationals.
ZERO, ONE, IM = (F(0), F(0)), (F(1), F(0)), (F(0), F(1))


def add(a, b):
    return a[0] + b[0], a[1] + b[1]


def mul(a, b):
    return a[0]*b[0]-a[1]*b[1], a[0]*b[1]+a[1]*b[0]


def scale(a, c):
    return a[0]*c, a[1]*c


TABLE = {
    ('X', 'Y'): (IM, 'Z'), ('Y', 'Z'): (IM, 'X'),
    ('Z', 'X'): (IM, 'Y'),
    ('Y', 'X'): (scale(IM, -1), 'Z'),
    ('Z', 'Y'): (scale(IM, -1), 'X'),
    ('X', 'Z'): (scale(IM, -1), 'Y'),
}


def pauli(a, b):
    phase, result = ONE, ''
    for x, y in zip(a, b):
        if x == 'I':
            result += y
        elif y == 'I':
            result += x
        elif x == y:
            result += 'I'
        else:
            factor, z = TABLE[x, y]
            phase, result = mul(phase, factor), result + z
    return phase, result


WORDS = {'A': 'XIX', 'B': 'IXY', 'C': 'YIZ'}
GAIN = {'A': (1, 0, 0), 'B': (0, 1, 0), 'C': (0, 0, 1)}


def product(a, b, order):
    result = [dict() for _ in range(order+1)]
    for n in range(order+1):
        for m in range(order+1-n):
            for (x, gx), cx in a[n].items():
                for (y, gy), cy in b[m].items():
                    phase, word = pauli(x, y)
                    key = word, tuple(u+v for u, v in zip(gx, gy))
                    result[n+m][key] = add(result[n+m].get(key, ZERO),
                                           mul(mul(cx, cy), phase))
    return [{k: v for k, v in p.items() if v != ZERO} for p in result]


def pulse(handle, sign, order):
    result, power = [], ONE
    for n in range(order+1):
        key = (WORDS[handle] if n % 2 else 'III',
               tuple(n*x for x in GAIN[handle]))
        result.append({key: scale(power, F(1, factorial(n)))})
        power = mul(power, (F(0), F(-sign)))
    return result


def series(word, signs, order):
    result = [{('III', (0, 0, 0)): ONE}] + [dict() for _ in range(order)]
    for handle, orientation in word:
        result = product(pulse(handle, orientation*signs[handle], order),
                         result, order)
    return result


def inverse(word):
    return [(j, -s) for j, s in reversed(word)]


def comm(u, v):
    # Chronological list, with the final entry acting last.
    return inverse(v) + inverse(u) + v + u


def primitive_area(word, handle):
    """Integral |integral_0^t f_handle| dt in normalized time.

    Each native segment has normalized duration one. Values are exact.
    """
    current, area = F(0), F(0)
    for j, s in word:
        slope = F(s if j == handle else 0)
        end = current + slope
        if current*end < 0:
            # General crossing formula; unit-sign words cannot cross in
            # an open unit interval, but retaining it makes this reusable.
            area += (current*current + end*end)/(2*abs(slope))
        else:
            area += (abs(current) + abs(end))/2
        current = end
    assert current == 0
    return area


def exact_word_checks():
    a, b, c = [('A', 1)], [('B', 1)], [('C', 1)]
    cubic = comm(a, comm(b, c))
    fifth = comm(a, comm(a, cubic))
    assert len(cubic) == 10 and len(fifth) == 46
    for word, degree, gain, coefficient in [
        (cubic, 3, (1, 1, 1), -4),
        (fifth, 5, (3, 1, 1), 16),
    ]:
        for sa in (-1, 1):
            for sb in (-1, 1):
                signs = {'A': sa, 'B': sb, 'C': sa*sb}
                actual = series(word, signs, degree)
                expected = [{('III', (0, 0, 0)): ONE}]
                expected += [dict() for _ in range(degree-1)]
                expected += [{('ZXI', gain): (F(0), F(coefficient))}]
                assert actual == expected, (degree, signs, actual)
        area = primitive_area(word, 'A')
        print(f'EXACT degree {degree}: {len(word)} segments; '
              f'leading {coefficient} i g^{gain} ZXI; A-area={area}')
    return cubic, fifth


def moment_certificate():
    n = 9
    v = [cmath.exp(1j*pi*j/n)/sqrt(n) for j in range(n)]
    target = [[1 if j == k else (1j if j < k else -1j)
               for k in range(n)] for j in range(n)]
    eigenvalue = 1-1/tan(pi/(2*n))
    residual = max(abs(sum(target[j][k]*v[k] for k in range(n))
                       - eigenvalue*v[j]) for j in range(n))
    assert residual < 1e-13
    bound = -eigenvalue/(n-1)
    print('ANALYTIC phase-only full-diamond lower bound:', f'{bound:.12f}')
    print('9x9 witness eigen-equation floating residual:', f'{residual:.3g}')
    # Independent finite distributions: their moment Toeplitz quadratic
    # forms must be nonnegative. No optimizer or bath samples are involved.
    distributions = [
        [(1., 0.)],
        [(.2, -3.), (.5, .3), (.3, 11.)],
        [(1/101, (j-50)/7) for j in range(101)],
    ]
    for distribution in distributions:
        moments = {k: sum(p*cmath.exp(-2j*a*k) for p, a in distribution)
                   for k in range(-8, 9)}
        q = sum(v[j].conjugate()*moments[j-k]*v[k]
                for j in range(n) for k in range(n))
        error = max(abs(moments[k]+1j) for k in range(1, 9))
        assert q.real >= -1e-12 and abs(q.imag) < 1e-12
        assert error >= bound-1e-12
        print('MOMENTS: witness positivity', f'{q.real:.8g}',
              'sampled worst error', f'{error:.8g}')
    return bound


def constructive_upper_bound():
    # alpha ~ exponential of mean a; phi(h)=1/(1+2 i a h).
    # Balance endpoints of h in [1,8]. The interior is better.
    x = (63+sqrt(10241))/224
    a = x/2
    improvement = (2*x-1)/(1+x*x)
    bound = sqrt(1-improvement)
    worst_grid = max(abs(1/(1+2j*a*(1+7*j/10000))+1j)
                     for j in range(10001))
    assert abs(worst_grid-bound) < 1e-12
    print('ANALYTIC exponential-phase uniform upper bound:', f'{bound:.12f}')
    print('exponential phase mean a:', f'{a:.12f}')
    # An explicit finite rational histogram approximates the law. The
    # probability calculations here are diagnostics; PROOF gives the bound.
    return a, bound


if __name__ == '__main__':
    exact_word_checks()
    moment_certificate()
    constructive_upper_bound()
