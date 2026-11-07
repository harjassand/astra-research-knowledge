"""Exact rational implementation of Huber arXiv:1308.1562, Algorithm 1.

Known coins use rejection on fair bits. The unknown coin is a callable and no
population value is passed to this algorithm. The exact version terminates a.s.
and has the cited expected source-query bound. No hard time limit or expected
bit-work bound is asserted here. Use sampling_control.py for a full hard budget.
Python's seeded RNG is used only by audits, not supplied as physical randomness.
"""
from fractions import Fraction as F


class Counts:
    def __init__(self, getbits):
        self.getbits = getbits
        self.fair_bits = 0
        self.unknown_coins = 0
        self.rational_coins = 0
        self.maximum_integer_bits = 0
        self.rescalings = 0

    def known(self, p):
        p = F(p)
        if not 0 <= p <= 1:
            raise ValueError("Invalid probability")
        self.rational_coins += 1
        self.maximum_integer_bits = max(self.maximum_integer_bits,
                                        p.numerator.bit_length(), p.denominator.bit_length())
        if p == 0 or p == 1:
            return int(p)
        bits = p.denominator.bit_length()
        while True:
            u = self.getbits(bits)
            self.fair_bits += bits
            if u < p.denominator:
                return int(u < p.numerator)

    def unknown(self, coin):
        value = coin()
        if value not in (0, 1):
            raise ValueError("Source did not return a bit")
        self.unknown_coins += 1
        return value


def linear_factory(coin, multiplier, slack, counts):
    c, eps = F(multiplier), min(F(slack), F(1, 2))
    if c <= 1 or not 0 < eps < 1:
        raise ValueError("Requires c>1 and a supplied positive slack")
    # The promise c*p <= 1-eps must come from the interface, not empirical data.
    k = F(23, 5)/eps
    i = 1
    while True:
        while True:
            b = counts.unknown(coin)
            if b:
                i -= 1
            else:
                # Geometric((c-1)/c), support 1,2,... .
                g = 1
                while not counts.known((c-1)/c):
                    g += 1
                i += g-1
            if i == 0 or i >= k:
                break
        if i == 0:
            return 1
        scale = 1+eps/2
        if not counts.known((1/scale)**i):
            return 0
        c *= scale
        eps /= 2
        k *= 2
        counts.rescalings += 1


def exact_command(cold_coin, hot_coin, target, cold_upper, hot_lower, counts):
    q = F(target)
    if not 0 <= cold_upper < q < hot_lower <= 1:
        raise ValueError("Missing strict bracket")
    while True:
        hot = counts.known(q)
        if hot:
            reject = linear_factory(cold_coin, 1/q, (q-cold_upper)/q, counts)
        else:
            reject = linear_factory(lambda: 1-hot_coin(), 1/(1-q),
                                    (hot_lower-q)/(1-q), counts)
        if not reject:
            return hot

