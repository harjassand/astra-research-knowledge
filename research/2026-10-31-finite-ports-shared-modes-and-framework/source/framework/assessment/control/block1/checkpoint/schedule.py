#!/usr/bin/env python3
"""Finite parameter construction and lazy native schedule.

The fair_bits argument must supply independent private uniform bits.
This file constructs a mathematical control family, not hardware access.
"""
from dataclasses import dataclass
from fractions import Fraction
import sys


def nearest_positive(x):
    return (2*x.numerator+x.denominator)//(2*x.denominator)


def atan_inverse(n, tolerance):
    total = Fraction(0)
    k = 0
    while True:
        total += Fraction((-1)**k, (2*k+1)*n**(2*k+1))
        next_term = Fraction(1, (2*k+3)*n**(2*k+3))
        if next_term <= tolerance:
            return total
        k += 1


def certified_pi(bits):
    """Return a dyadic pi estimate with absolute error <= 2**(-bits).

    Machin identity, alternating-series bounds, and exact rational rounding.
    Each arctangent remainder is <= ulp/64; the weighted error is <=
    20*ulp/64, and rounding adds <= ulp/2.
    """
    scale = 1 << bits
    tolerance = Fraction(1, 64*scale)
    estimate = 16*atan_inverse(5, tolerance)-4*atan_inverse(239, tolerance)
    return Fraction(nearest_positive(estimate*scale), scale)


@dataclass(frozen=True)
class Plan:
    requested_error: Fraction
    b: int
    q: int
    cycles: int
    ideal_error_bound: Fraction

    @property
    def segments(self):
        return 10*self.cycles

    @property
    def duration(self):
        return Fraction(self.segments, self.q)

    @property
    def independent_duration_tolerance(self):
        e = min(self.requested_error, Fraction(1))
        return e/(4*self.segments**2)


def make_plan(epsilon):
    epsilon = Fraction(epsilon)
    if epsilon <= 0:
        raise ValueError('epsilon must be positive')
    e = min(epsilon, Fraction(1))
    b, q = 0, 1
    while q*e < 4000:
        b, q = b+1, 2*q
    pi_hat = certified_pi(3*b)
    cycles = nearest_positive(pi_hat*q**3/16)
    error = Fraction(10000*cycles, q**4)+Fraction(9, 2*q**3)
    assert error <= e/2
    return Plan(epsilon, b, q, cycles, error)


ORIENTED_CYCLE = (('B', -1), ('C', -1), ('B', 1), ('C', 1),
                  ('A', -1), ('C', -1), ('B', -1), ('C', 1),
                  ('B', 1), ('A', 1))


def native_segments(plan, fair_bits):
    """Yield (handle, signed strength, exact duration), chronologically.

    No materialization of the enormous complete word is necessary. Each
    cycle consumes exactly two bits from the supplied private fair source.
    """
    duration = Fraction(1, plan.q)
    fair_bits = iter(fair_bits)
    for _ in range(plan.cycles):
        sa, sb = 2*next(fair_bits)-1, 2*next(fair_bits)-1
        if sa not in (-1, 1) or sb not in (-1, 1):
            raise ValueError('fair_bits must yield zeros or ones')
        signs = dict(A=sa, B=sb, C=sa*sb)
        for handle, orientation in ORIENTED_CYCLE:
            yield handle, orientation*signs[handle], duration


def display(plan):
    tolerance = plan.independent_duration_tolerance
    timing_bits = 0
    while Fraction(1, 1 << timing_bits) > tolerance:
        timing_bits += 1
    print('requested full trace/diamond error:', plan.requested_error)
    print('b:', plan.b)
    print('q:', plan.q)
    print('each specified native duration:', Fraction(1, plan.q))
    print('cycles N:', plan.cycles)
    print('native segments m:', plan.segments)
    print('switches at most:', plan.segments-1)
    print('private fair bits:', 2*plan.cycles)
    print('total specified duration:', plan.duration)
    print('total specified duration, decimal:', float(plan.duration))
    print('ideal-schedule error bound:', float(plan.ideal_error_bound))
    print('independent duration tolerance:', tolerance)
    print('sufficient absolute binary timing places:', timing_bits)
    print('total error including duration tolerance <=', min(plan.requested_error, Fraction(1)))


if __name__ == '__main__':
    display(make_plan(sys.argv[1] if len(sys.argv) > 1 else '0.1'))
