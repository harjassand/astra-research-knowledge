"""Exact-bit, nonnegative physical-prefix estimator and low-sector sampler.

Phase-two attributed origin: c03_l10's random-sign Pfaffian norm estimator;
c03_l06's self-reduction; c03_s02's physical-prefix projection and Cauchy bound.
This implementation is written independently. Production coefficient work uses
matrix powers and a logarithmic-derivative recurrence, not minor enumeration.
Default randomness is SystemRandom. A supplied seeded RNG is diagnostic only.
"""
from fractions import Fraction
from itertools import combinations, product
from math import comb, factorial, lcm
from random import SystemRandom

ZERO = (0, 0)
ONE = (1, 0)


def add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def mul(a, b):
    return (a[0]*b[0] - a[1]*b[1], a[0]*b[1] + a[1]*b[0])


def conj(a):
    return (a[0], -a[1])


def scale(a, z):
    return (a[0]*z, a[1]*z)


def matmul(a, b):
    n = len(a)
    out = [[ZERO for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for h in range(n):
            if a[i][h] == ZERO:
                continue
            for j in range(n):
                if b[h][j] != ZERO:
                    out[i][j] = add(out[i][j], mul(a[i][h], b[h][j]))
    return out


def pfaffian_norm_coefficient(a, k, stats=None):
    """[t^k] sqrt(det(I+t A* A)) using q'/q = tr(B(I+tB)^-1)/2."""
    n = len(a)
    if k == 0:
        return 1
    if 2*k > n:
        return 0
    b = matmul([[conj(a[j][i]) for j in range(n)] for i in range(n)], a)
    power = b
    tr = [0]
    for j in range(1, k+1):
        real = sum(power[i][i][0] for i in range(n))
        imaginary = sum(power[i][i][1] for i in range(n))
        assert imaginary == 0
        tr.append(real)
        if j != k:
            power = matmul(power, b)
    q = [1]
    for degree in range(1, k+1):
        numerator = sum((-1)**(j-1) * tr[j] * q[degree-j]
                        for j in range(1, degree+1))
        assert numerator % (2*degree) == 0
        q.append(numerator // (2*degree))
        assert q[-1] >= 0
    if stats is not None:
        stats['coefficient_calls'] = stats.get('coefficient_calls', 0) + 1
        stats['largest_trace_bits'] = max(stats.get('largest_trace_bits', 0),
                                          max(abs(x).bit_length() for x in tr))
    return q[k]


def ceiling(x):
    return -((-x.numerator)//x.denominator)


def ceil_log2(x):
    x = Fraction(x)
    b = 0
    while (1 << b)*x.denominator < x.numerator:
        b += 1
    return b


class LowSector:
    """F over Q(i), encoded as numbers or (real, imaginary) rational tuples."""
    def __init__(self, f):
        self.n = len(f)
        if any(len(row) != self.n for row in f):
            raise ValueError('square matrix required')
        raw = [[(Fraction(v[0]), Fraction(v[1])) if isinstance(v, tuple)
                else (Fraction(v), Fraction(0)) for v in row] for row in f]
        den = 1
        for row in raw:
            for a, b in row:
                den = lcm(den, a.denominator, b.denominator)
        self.denominator = den
        self.g = [[(int(a*den), int(b*den)) for a, b in row] for row in raw]
        self.stats = {}

    def _restrictions(self, k, up, down, empty):
        if not isinstance(k, int) or not 0 <= k <= self.n//2:
            raise ValueError('legal integer sector required')
        up, down, empty = frozenset(up), frozenset(down), frozenset(empty)
        if up & down or up & empty or down & empty:
            raise ValueError('site restrictions must be disjoint')
        if not (up | down | empty) <= set(range(self.n)):
            raise ValueError('invalid site index')
        return up, down, empty

    def prefix_draw_integer(self, k, signs, up=(), down=(), empty=()):
        up, down, empty = self._restrictions(k, up, down, empty)
        a, b = len(up), len(down)
        if a > k or b > k or 2*k > self.n-len(empty):
            return 0
        if len(signs) != self.n:
            raise ValueError('one sign coordinate per site required')
        free = set(range(self.n)) - up - down - empty
        if any(signs[i] not in (-1, 1) for i in free):
            raise ValueError('free coordinates require Rademacher signs')
        degree = 2*a
        answer = 0
        for removed_size in range(b+1):
            for removed in combinations(sorted(down), removed_size):
                retained = [i for i in range(self.n) if i not in empty and i not in removed]
                if len(retained) < 2*k:
                    continue
                finite_difference = 0
                for z in range(degree+1):
                    activities = [z if i in up else 0 if i in down or i in empty
                                  else signs[i] for i in range(self.n)]
                    skew = [[add(scale(self.g[i][j], activities[i]),
                                 scale(self.g[j][i], -activities[j]))
                             for j in retained] for i in retained]
                    value = pfaffian_norm_coefficient(skew, k, self.stats)
                    finite_difference += (-1)**(degree-z)*comb(degree, z)*value
                assert finite_difference % factorial(degree) == 0
                top = finite_difference // factorial(degree)
                assert top >= 0
                answer += (-1)**removed_size * top
        assert answer >= 0
        return answer

    def range_multiplier(self, k, a, b):
        c = comb(2*k-a-b, k-a)
        assert (1 << b)*c <= comb(2*k, k)
        return c

    def estimate(self, k, eta, delta, up=(), down=(), empty=(), rng=None,
                 enumerate_if_cheaper=True, memoize=True):
        """Relative estimate, confidence 1-delta, deterministic runtime cap.

        True zero always outputs zero; positive mass can output zero with
        probability at most delta. Zero output is not an exact-zero certificate.
        Small sign spaces are enumerated only if cheaper than the stated cap.
        """
        eta, delta = Fraction(eta), Fraction(delta)
        if not 0 < eta <= Fraction(1, 2) or not 0 < delta < 1:
            raise ValueError('require 0<eta<=1/2 and 0<delta<1')
        up, down, empty = self._restrictions(k, up, down, empty)
        a, b = len(up), len(down)
        if a > k or b > k or 2*k > self.n-len(empty):
            return Fraction(0)
        c = self.range_multiplier(k, a, b)
        free = sorted(set(range(self.n)) - up - down - empty)
        sign_template = [1]*self.n
        self.stats['count_calls'] = self.stats.get('count_calls', 0) + 1
        if c == 1:
            self.stats['constant_draw_calls'] = self.stats.get('constant_draw_calls', 0) + 1
            return Fraction(self.prefix_draw_integer(k, sign_template, up, down, empty),
                            self.denominator**(2*k))
        # The range bound X <= c*mu gives multiplicative Chernoff:
        # P(|mean-mu|>eta*mu) <= 2 exp(-m eta^2/(3c)).
        sample_cap = ceiling(3*c*ceil_log2(2/delta)/(eta*eta))
        enumeration_size = 1 << len(free)
        if enumerate_if_cheaper and enumeration_size <= sample_cap:
            total = 0
            for word in product((-1, 1), repeat=len(free)):
                signs = sign_template.copy()
                for i, s in zip(free, word):
                    signs[i] = s
                total += self.prefix_draw_integer(k, signs, up, down, empty)
            self.stats['enumerated_words'] = self.stats.get('enumerated_words', 0) + enumeration_size
            return Fraction(total, enumeration_size*self.denominator**(2*k))
        rng = SystemRandom() if rng is None else rng
        total, cache = 0, {}
        for _ in range(sample_cap):
            word = rng.getrandbits(len(free))
            if not memoize or word not in cache:
                signs = sign_template.copy()
                for j, i in enumerate(free):
                    signs[i] = 1 if (word >> j)&1 else -1
                value = self.prefix_draw_integer(k, signs, up, down, empty)
                if memoize:
                    cache[word] = value
            else:
                value = cache[word]
            total += value
        self.stats['random_draws'] = self.stats.get('random_draws', 0) + sample_cap
        self.stats['random_bits'] = self.stats.get('random_bits', 0) + sample_cap*len(free)
        self.stats['maximum_cache_entries'] = max(self.stats.get('maximum_cache_entries', 0), len(cache))
        return Fraction(total, sample_cap*self.denominator**(2*k))

    def born_sample(self, k, epsilon, rng=None, enumerate_if_cheaper=True, memoize=True):
        """TV-epsilon sampler on {supported configurations} union {FAIL}.

        Promise: c_k(F)>0. FAIL is charged to estimation confidence. Every
        successful return has positive target weight, including on bad events.
        Finite dyadic categorical sampling never introduces a zero-weight child.
        """
        epsilon = Fraction(epsilon)
        if not 0 < epsilon < 1:
            raise ValueError('require 0<epsilon<1')
        self._restrictions(k, (), (), ())
        rng = SystemRandom() if rng is None else rng
        if k == 0:
            return {'status': 'OK', 'I': [], 'J': []}
        eta, delta = epsilon/(8*self.n), epsilon/(12*self.n)
        bits = ceil_log2(8*self.n/epsilon)
        q = 1 << bits
        up, down, empty = set(), set(), set()
        for site in range(self.n):
            kwargs = {'rng': rng, 'enumerate_if_cheaper': enumerate_if_cheaper,
                      'memoize': memoize}
            weights = [self.estimate(k, eta, delta, up | {site}, down, empty, **kwargs),
                       self.estimate(k, eta, delta, up, down | {site}, empty, **kwargs),
                       self.estimate(k, eta, delta, up, down, empty | {site}, **kwargs)]
            total = sum(weights)
            if total == 0:
                self.stats['failures'] = self.stats.get('failures', 0) + 1
                return {'status': 'FAIL', 'site': site}
            boundaries = [ceiling(Fraction(0))]
            # Floors of exact cumulative probabilities. A zero child's two
            # endpoints agree exactly, so rounding preserves zero support.
            for w in (weights[0], weights[0]+weights[1]):
                x = q*w/total
                boundaries.append(x.numerator//x.denominator)
            word = rng.getrandbits(bits)
            if word < boundaries[1]:
                up.add(site)
            elif word < boundaries[2]:
                down.add(site)
            else:
                empty.add(site)
            self.stats['categorical_bits'] = self.stats.get('categorical_bits', 0) + bits
        assert len(up) == len(down) == k
        return {'status': 'OK', 'I': sorted(up), 'J': sorted(down)}
