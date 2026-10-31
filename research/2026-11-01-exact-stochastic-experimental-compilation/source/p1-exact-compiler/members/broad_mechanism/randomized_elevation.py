"""Exact rational randomized elevation for multivariate Bernoulli factories.

The caller supplies certified coefficient functions, derivative bounds and
mass bounds. This module executes the exact finite operation; it does not
infer or numerically certify those analytic bounds.

The getrandbits interface is ideal fair randomness in the mathematical
contract. random.Random is used only by the reproducible validation program.
"""
from dataclasses import dataclass
from fractions import Fraction
from math import comb, factorial, lcm

F = Fraction


def product(values):
    ans = F(1)
    for value in values:
        ans *= value
    return ans


def falling(n, k):
    ans = 1
    for j in range(k):
        ans *= n - j
    return ans


def multiindices(dimension, total):
    """Enumerate fixed total degree, never a (degree+1)^dimension cube."""
    if dimension == 0:
        if total == 0:
            yield ()
        return
    if dimension == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for rest in multiindices(dimension - 1, total - first):
            yield (first,) + rest


def centered_moments(n, s, order):
    """Hypergeom(2n,s,n)/n-s/(2n), via exact factorial moments."""
    x = F(s, 2 * n)
    stirling = [[1]]
    for k in range(1, order + 1):
        prev = stirling[-1]
        row = [0] * (k + 1)
        for j in range(1, k + 1):
            row[j] = prev[j - 1] + (j * prev[j] if j < len(prev) else 0)
        stirling.append(row)
    raw = []
    for k in range(order + 1):
        val = F(0)
        for j in range(k + 1):
            if j > n or j > s:
                continue
            val += F(stirling[k][j] * falling(n, j) * falling(s, j), falling(2 * n, j))
        raw.append(val)
    return tuple(
        sum(F(comb(k, j)) * (-x) ** (k - j) * raw[j] / n ** j
            for j in range(k + 1))
        for k in range(order + 1)
    )


class FairBits:
    def __init__(self, getrandbits):
        self.getrandbits = getrandbits
        self.bits = 0

    def randbelow(self, upper):
        if upper < 1:
            raise ValueError("positive integer upper bound required")
        if upper == 1:
            return 0
        width = (upper - 1).bit_length()
        while True:
            self.bits += width
            z = self.getrandbits(width)
            if z < upper:
                return z

    def bernoulli(self, p):
        p = F(p)
        if not 0 <= p <= 1:
            raise ValueError("probability is outside [0,1]")
        return self.randbelow(p.denominator) < p.numerator

    def integer_weighted(self, weights):
        total = sum(weights)
        if total <= 0 or any(w < 0 for w in weights):
            raise ValueError("nonnegative weights with positive total required")
        u = self.randbelow(total)
        for i, w in enumerate(weights):
            if u < w:
                return i
            u -= w
        raise AssertionError("unreachable")


def integerize_rationals(weights):
    denominator = 1
    for w in weights:
        denominator = lcm(denominator, w.denominator)
    return tuple(w.numerator * (denominator // w.denominator) for w in weights)


@dataclass(frozen=True)
class RationalOracle:
    # value(point) and derivative(point, multiindex) both return Fraction.
    value: object
    derivative: object


class ProductEnvelope:
    """Exactly normalized sum-of-products envelope on conditional counts."""
    def __init__(self, n, totals, r, K, scale):
        self.n = int(n)
        self.totals = tuple(int(s) for s in totals)
        self.m = len(self.totals)
        self.x = tuple(F(s, 2 * n) for s in self.totals)
        self.r, self.K, self.scale = int(r), int(K), F(scale)
        if self.scale < 0 or self.r < 1 or self.K < 0:
            raise ValueError("invalid envelope parameters")
        self.supports, self.base_weights, self.moment_weights = [], [], []
        self.Z, self.V = [], []
        self.support_terms = 0
        self.max_integer_bits = 0
        self.draws = 0
        denom = comb(2 * n, n) * (2 * n) ** K
        for s in self.totals:
            support = tuple(range(max(0, s - n), min(s, n) + 1))
            base, moment = [], []
            first = support[0]
            binomial_product = comb(s, first) * comb(2 * n - s, n - first)
            for k in support:
                d = 2 * k - s
                w = binomial_product * (2 * n + abs(d)) ** K
                base.append(w)
                moment.append(w * d ** (2 * r))
                self.max_integer_bits = max(self.max_integer_bits, w.bit_length())
                if k != support[-1]:
                    binomial_product = (binomial_product * (s - k) * (n - k)) // (
                        (k + 1) * (n - s + k + 1)
                    )
            self.supports.append(support)
            self.base_weights.append(tuple(base))
            self.moment_weights.append(tuple(moment))
            self.Z.append(F(sum(base), denom))
            self.V.append(F(sum(moment), denom * (2 * n) ** (2 * r)))
            self.support_terms += len(support)
        components = [v / z for v, z in zip(self.V, self.Z)]
        self.component_weights = integerize_rationals(components)
        self.expectation = self.scale * product(self.Z) * sum(components)

    def value(self, y):
        return self.scale * sum(v ** (2 * self.r) for v in y) * product(
            (1 + abs(v)) ** self.K for v in y
        )

    def sample(self, bits):
        if self.expectation == 0:
            raise ValueError("a zero envelope has no tilted distribution")
        self.draws += 1
        distinguished = bits.integer_weighted(self.component_weights)
        y = []
        for i, s in enumerate(self.totals):
            weights = self.moment_weights[i] if i == distinguished else self.base_weights[i]
            idx = bits.integer_weighted(weights)
            k = self.supports[i][idx]
            y.append(F(2 * k - s, 2 * self.n))
        return tuple(y)


class TaylorControl:
    def __init__(self, oracle, envelope):
        self.oracle, self.envelope = oracle, envelope
        self.order = 2 * envelope.r - 1
        self.coefficients = {}
        self.derivative_calls = 0
        self.value_calls = 0
        moments = [centered_moments(envelope.n, s, self.order) for s in envelope.totals]
        for total in range(self.order + 1):
            for beta in multiindices(envelope.m, total):
                self.derivative_calls += 1
                derivative = F(oracle.derivative(envelope.x, beta))
                if derivative:
                    self.coefficients[beta] = derivative / product(factorial(k) for k in beta)
        self.expectation = sum(
            coefficient * product(moments[i][beta[i]] for i in range(envelope.m))
            for beta, coefficient in self.coefficients.items()
        )

    def evaluate(self, y):
        return sum(coefficient * product(v ** k for v, k in zip(y, beta))
                   for beta, coefficient in self.coefficients.items())

    def remainder_estimator(self, bits):
        if self.envelope.expectation == 0:
            return F(0)
        y = self.envelope.sample(bits)
        point = tuple(x + yy for x, yy in zip(self.envelope.x, y))
        self.value_calls += 1
        remainder = F(self.oracle.value(point)) - self.evaluate(y)
        bound = self.envelope.value(y)
        if abs(remainder) > bound:
            raise ArithmeticError("the supplied Taylor remainder certificate failed")
        return self.envelope.expectation * remainder / bound


class ElevationRace:
    """Return +1, 0, or None with exact accept-one, accept-zero, continue ratios.

    lower_next/upper_next are coefficient values at the doubled counts.
    common_bound is a certified pointwise bound on each increment estimator.
    The calling proof must establish their nonnegativity and positive total.
    """
    def __init__(self, lower, upper, lower_next, upper_next, envelope, common_bound):
        self.lower = TaylorControl(lower, envelope)
        self.upper = TaylorControl(upper, envelope)
        self.lower_next, self.upper_next = F(lower_next), F(upper_next)
        self.envelope, self.bound = envelope, F(common_bound)
        self.attempts = 0
        if self.bound <= 0:
            raise ValueError("common_bound must be positive")

    def estimate_mass(self, category, bits):
        if category == 0:
            value = self.lower_next - self.lower.expectation - self.lower.remainder_estimator(bits)
        elif category == 1:
            value = self.upper.expectation + self.upper.remainder_estimator(bits) - self.upper_next
        elif category == 2:
            value = self.upper_next - self.lower_next
        else:
            raise ValueError("category must be 0, 1, or 2")
        if not 0 <= value <= self.bound:
            raise ArithmeticError("the supplied nonnegative mass/bound certificate failed")
        return value

    def sample(self, bits):
        while True:
            self.attempts += 1
            category = bits.randbelow(3)
            if bits.bernoulli(self.estimate_mass(category, bits) / self.bound):
                return (1, 0, None)[category]
