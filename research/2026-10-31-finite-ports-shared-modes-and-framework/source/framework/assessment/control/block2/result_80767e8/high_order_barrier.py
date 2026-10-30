"""Exact first-motion adversary against a degree-five native commutator.

The raw 46-segment ad_a^2[c,[a,b]] word is the predecessor's degree-five
Lie example. Its coefficient is checked independently here. All computations
use exact Gaussian integers, with rational bath amplitudes and one integer
rescaling of the series variable. No third-party packages are needed.
"""

from fractions import Fraction as Q
from math import factorial, lcm
from pauli_series import (
    HANDLES, gauss_add, polynomial_mul, series_mul, pulse_series,
)


def inverse(word):
    return [(h, -s) for h, s in reversed(word)]


def commutator(u, v):
    return inverse(v) + inverse(u) + v + u


def high_word():
    a, b, c = [('A', 1)], [('B', 1)], [('C', 1)]
    ell = commutator(c, commutator(a, b))
    return commutator(a, commutator(a, ell))


def adversary(word):
    cumulative = {h: Q(0) for h in HANDLES}
    midpoints = {h: [] for h in HANDLES}
    for active, orientation in word:
        for h in HANDLES:
            slope = Q(orientation if h == active else 0)
            midpoints[h].append(cumulative[h] + slope/2)
            cumulative[h] += slope
    assert all(value == 0 for value in cumulative.values())
    average = sum(midpoints['A'])/len(word)
    maximum = max(abs(value-average) for value in midpoints['A'])
    assert maximum > 0
    hs = [(value-average)/(2*maximum) for value in midpoints['A']]
    assert sum(hs) == 0 and max(map(abs, hs)) <= Q(1, 2)
    ja = sum(f*h for f, h in zip(midpoints['A'], hs))
    jb = sum(f*h for f, h in zip(midpoints['B'], hs))
    return hs, 2*ja, -2*jb


def exp_derivatives(generator, degree):
    result = [{'III': (1, 0)}]
    for _ in range(degree):
        result.append(polynomial_mul(generator, result[-1]))
    return result


def scaled_coefficient(term, degree, q=1, averaging=1):
    denominator = factorial(degree)*q**degree*averaging
    return {p: (Q(z[0], denominator), Q(z[1], denominator))
            for p, z in term.items() if z != (0, 0)}


def main():
    word = high_word()
    assert len(word) == 46
    hs, aa, ab = adversary(word)
    variance = aa**2 + ab**2
    scale = lcm(*(h.denominator for h in hs))
    print('Word: ad_a^2[c,[a,b]],', len(word), 'native segments.')
    print('Bath: H_M(t)=eta_k*h_j*Z_M on segment j of cycle k.')
    print('Each eta_k is a public-adversary random sign, independent of private signs.')
    print('Bath amplitudes h_j:', ','.join(map(str, hs)))
    print('sum h_j =', sum(hs), '; maximum |h_j| =', max(map(abs, hs)))
    print('Leading native/bath residual coefficients a_A,a_B:', aa, ab)
    print('Dissipator strength S=a_A^2+a_B^2:', variance)

    degree = 5
    for a in (-1, 1):
        for b in (-1, 1):
            signs = {'A': a, 'B': b, 'C': a*b}
            w = [{'III': (1, 0)}] + [{} for _ in range(degree)]
            for h, s in word:
                w = series_mul(pulse_series(HANDLES[h], s*signs[h], degree), w, degree)
            assert all(w[k] == {} for k in range(1, 5))
            assert w[5] == {'ZXI': (0, -1920)}
    print('Exact frozen certificate: U=I-16i*tau^5*Z1X2+O(tau^6), all four signs.')

    degree = 4
    sums = [{} for _ in range(degree+1)]
    for a in (-1, 1):
        for b in (-1, 1):
            signs = {'A': a, 'B': b, 'C': a*b}
            for eta in (-1, 1):
                w = [{'III': (1, 0)}] + [{} for _ in range(degree)]
                for (h, s), bath in zip(word, hs):
                    generator = {HANDLES[h]: (0, -scale*s*signs[h]),
                                 'IIZ': (0, -int(scale*bath)*eta)}
                    w = series_mul(exp_derivatives(generator, degree), w, degree)
                assert w[1] == {}
                second = scaled_coefficient(w[2], 2, scale)
                expected = {'XIY': (Q(0), -eta*a*aa)}
                if ab:
                    expected['IXX'] = (Q(0), -eta*b*ab)
                assert second == expected, (second, expected)
                for k, term in enumerate(w):
                    for p, z in term.items():
                        sums[k][p] = gauss_add(sums[k].get(p, (0, 0)), z)
    sums = [{p: z for p, z in term.items() if z != (0, 0)} for term in sums]
    assert sums[1] == sums[2] == sums[3] == {}
    fourth = scaled_coefficient(sums[4], 4, scale, averaging=8)
    assert fourth == {'III': (-variance/2, Q(0))}
    print('Exact combined-mean coefficients of tau,tau^2,tau^3: all zero.')
    print('Exact combined-mean coefficient of tau^4:', fourth)
    print('Therefore averaged channel = Id + tau^4 * [')
    print(' ', aa**2, '(Ad_XIY-Id) +', ab**2, '(Ad_IXX-Id)] + O(tau^5).')
    print('This bath reacts to the public shape/clock, never to current private signs.')


if __name__ == '__main__':
    main()
