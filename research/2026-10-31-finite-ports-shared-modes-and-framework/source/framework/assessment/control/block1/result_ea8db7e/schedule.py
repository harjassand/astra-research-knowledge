#!/usr/bin/env python3
"""A finite calibration-free partial controller; no physical device access.

The full diamond error is <0.84, uniformly on the specified gain/bath class.
This is not an arbitrary-accuracy solution. Supply fresh private fair bits.
The huge native schedule is represented lazily.
"""
from fractions import Fraction

M = 1 << 13
K = 16*M
Q = 1 << 30
DELTA = Fraction(1, Q)
ANGLE_STEP = Fraction(3, 65536)
SYNTHESIS_ERROR = Fraction(1, 2048)
MAX_CYCLES = 3*(1 << 89)
MAX_SEGMENTS = 10*MAX_CYCLES
MAX_DURATION = MAX_SEGMENTS*DELTA
DURATION_TOLERANCE = SYNTHESIS_ERROR/(8*MAX_SEGMENTS**2)

ORIENTED_CYCLE = (('B', -1), ('C', -1), ('B', 1), ('C', 1),
                  ('A', -1), ('C', -1), ('B', -1), ('C', 1),
                  ('B', 1), ('A', 1))


def bit(bits):
    value = next(bits)
    if value not in (0, 1):
        raise ValueError('private fair bits must be zero or one')
    return value


def sample_capped_geometric(bits):
    """At most 13*K private bits; exactly rational finite distribution."""
    for failures in range(K):
        trial = 0
        for _ in range(13):
            trial = 2*trial+bit(bits)
        if trial == 0:
            return failures
    return K


def cycle_count(k):
    if not isinstance(k, int) or not 0 <= k <= K:
        raise ValueError('angle index must lie between zero and K')
    return 3*k*(1 << 72)


def native_segments_for_index(k, fair_bits, pad_to_common_end=True):
    """Yield (handle, strength, exact duration), in chronological order.

    None is the handle for a final idle. Never materialize the full schedule.
    The angle index must itself be sampled using independent private coins.
    """
    bits = iter(fair_bits)
    cycles = cycle_count(k)
    for _ in range(cycles):
        sa, sb = 2*bit(bits)-1, 2*bit(bits)-1
        signs = {'A': sa, 'B': sb, 'C': sa*sb}
        for handle, orientation in ORIENTED_CYCLE:
            yield handle, orientation*signs[handle], DELTA
    if pad_to_common_end:
        idle = MAX_DURATION-10*cycles*DELTA
        if idle:
            yield None, 0, idle


def randomized_native_program(fair_bits):
    bits = iter(fair_bits)
    k = sample_capped_geometric(bits)
    yield from native_segments_for_index(k, bits)


def resources():
    assert 4*MAX_CYCLES*DELTA**3 == 6
    assert Fraction(100000)*MAX_CYCLES*DELTA**4 < SYNTHESIS_ERROR/2
    timing_bits = 0
    while Fraction(1, 1 << timing_bits) > DURATION_TOLERANCE:
        timing_bits += 1
    return {
        'gain_evaluations': 0,
        'angle_trials_at_most': K,
        'angle_sampling_bits_at_most': 13*K,
        'maximum_cycles': MAX_CYCLES,
        'maximum_native_segments': MAX_SEGMENTS,
        'native_switches_at_most': MAX_SEGMENTS-1,
        'maximum_specified_duration': str(MAX_DURATION),
        'maximum_specified_duration_decimal': float(MAX_DURATION),
        'private_fair_bits_at_most': 2*MAX_CYCLES+13*K,
        'specified_native_segment_duration': str(DELTA),
        'independent_segment_duration_tolerance': str(DURATION_TOLERANCE),
        'sufficient_absolute_binary_timing_places': timing_bits,
        'maximum_ideal_native_synthesis_error':
            float(Fraction(100000)*MAX_CYCLES*DELTA**4),
        'maximum_timing_error': float(SYNTHESIS_ERROR/2),
    }


if __name__ == '__main__':
    import json
    print(json.dumps(resources(), indent=2))
