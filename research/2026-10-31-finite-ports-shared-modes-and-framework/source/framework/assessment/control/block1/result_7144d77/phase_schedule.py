#!/usr/bin/env python3
"""A finite legal uniform coarse-accuracy construction.

For any excess eta>0, approximate the desired gate to full diamond error
at most sqrt(5554/7969)+eta, uniformly in the question's gain/bath class.
This is NOT an arbitrary-accuracy solution. PROOF.md proves a constant
lower bound for the entire phase-only comparison interface used here.

The schedule is lazy: huge physical words are never materialized.
"""
from dataclasses import dataclass
from fractions import Fraction as F
from math import sqrt
import sys


BASE_ERROR_SQUARED = F(5554, 7969)
MEAN = F(11, 30)
WORD = (('B', -1), ('C', -1), ('B', 1), ('C', 1),
        ('A', -1), ('C', -1), ('B', -1), ('C', 1),
        ('B', 1), ('A', 1))


def nearest(x):
    return (2*x.numerator+x.denominator)//(2*x.denominator)


@dataclass(frozen=True)
class Plan:
    eta: F
    outer_block_bits: int
    outer_cap: int
    phase_mesh: F
    q: int
    max_cycles: int
    ideal_compilation_error: F

    @property
    def max_segments(self):
        return 10*self.max_cycles

    @property
    def max_duration(self):
        return F(self.max_segments, self.q)

    @property
    def duration_tolerance(self):
        return self.eta/(32*self.max_segments**2)

    @property
    def maximum_phase(self):
        return self.outer_cap*self.phase_mesh


def make_plan(eta):
    eta = F(eta)
    if eta <= 0:
        raise ValueError('eta must be positive')
    eta = min(eta, F(1))
    d = 1
    while F(128)*MEAN*MEAN/F((1 << d)-1) > eta/4:
        d += 1
    b = 0
    while F(1, 1 << b) > eta/8:
        b += 1
    cap = (1 << d)*b
    mesh = MEAN/F((1 << d)-1)
    phase_max = cap*mesh
    q = 128
    while True:
        n = nearest(phase_max*q**3/4)
        error = F(50000*n, q**4)+F(32, q**3)
        if error <= eta/8:
            break
        q *= 2
    return Plan(eta, d, cap, mesh, q, n, error)


def _bit(source):
    value = next(source)
    if value not in (0, 1):
        raise ValueError('private fair source must yield zeros or ones')
    return value


def native_segments(plan, fair_bits):
    """Yield (handle, signed strength, duration).

    All bits must be fresh independent private fair bits. A capped geometric
    law is sampled before the inner-cycle coins, so no inner signs are
    reused for later policy decisions.
    """
    bits = iter(fair_bits)
    failures = plan.outer_cap
    for j in range(plan.outer_cap):
        block = [_bit(bits) for _ in range(plan.outer_block_bits)]
        if all(value == 0 for value in block):
            failures = j
            break
    alpha = failures*plan.phase_mesh
    cycles = nearest(alpha*plan.q**3/4)
    duration = F(1, plan.q)
    for _ in range(cycles):
        sa, sb = 2*_bit(bits)-1, 2*_bit(bits)-1
        signs = {'A': sa, 'B': sb, 'C': sa*sb}
        for handle, orientation in WORD:
            yield handle, orientation*signs[handle], duration


def display(plan):
    p = F(1, 1 << plan.outer_block_bits)
    geometric_error = 128*MEAN*plan.phase_mesh
    # (1-p)^(1/p)<=exp(-1)<=1/2 gives the rational tail certificate.
    tail_blocks = plan.outer_cap >> plan.outer_block_bits
    tail_error = F(2, 1 << tail_blocks)
    timing_error = 4*plan.max_segments**2*plan.duration_tolerance
    total_excess = geometric_error+tail_error+plan.ideal_compilation_error+timing_error
    assert total_excess <= plan.eta
    print('uniform base full-diamond error:', sqrt(float(BASE_ERROR_SQUARED)))
    print('requested excess eta:', plan.eta)
    print('certified excess bound:', float(total_excess))
    print('outer geometric success probability:', p)
    print('outer blocks cap:', plan.outer_cap)
    print('maximum outer fair bits:', plan.outer_block_bits*plan.outer_cap)
    print('phase mesh:', plan.phase_mesh)
    print('maximum phase:', plan.maximum_phase)
    print('native duration delta:', F(1, plan.q))
    print('maximum cycles:', plan.max_cycles)
    print('maximum native segments:', plan.max_segments)
    print('maximum switches:', max(0, plan.max_segments-1))
    print('maximum inner private bits:', 2*plan.max_cycles)
    print('maximum duration:', plan.max_duration)
    print('maximum duration decimal:', float(plan.max_duration))
    print('independent segment-duration tolerance:', plan.duration_tolerance)
    bits = 0
    while F(1, 1 << bits) > plan.duration_tolerance:
        bits += 1
    print('sufficient absolute timing binary places:', bits)


if __name__ == '__main__':
    display(make_plan(sys.argv[1] if len(sys.argv) > 1 else '0.01'))
