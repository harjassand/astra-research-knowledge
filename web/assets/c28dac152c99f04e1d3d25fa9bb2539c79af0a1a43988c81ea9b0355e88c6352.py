#!/usr/bin/env python3
"""Exact finite regressions for the shared-denominator report.

All exponents, jumps, and directions are Fractions. Coefficients are omitted:
the support-order criterion depends only on supports when coefficients are
strictly positive.
"""

from fractions import Fraction as F
from itertools import product


def dot(a, b):
    return sum((x * y for x, y in zip(a, b)), F(0))


def rate_test(channels, denominator_supports, direction):
    """Apply the exact active-minimum rule to sparse positive supports.

    Each channel is (jump, numerator_support), and denominator_supports has
    one support per channel. An empty active set is vacuously accepted.
    """
    active = [i for i, (jump, _) in enumerate(channels)
              if dot(jump, direction) != 0]
    if not active:
        return True
    orders = {
        i: min(dot(alpha, direction) for alpha in channels[i][1])
           - min(dot(beta, direction) for beta in denominator_supports[i])
        for i in active
    }
    minimum = min(orders.values())
    return all(dot(channels[i][0], direction) > 0
               for i in active if orders[i] == minimum)


def monomial_source_test(channels, direction):
    """Ordinary source test for channels with singleton numerators."""
    active = [i for i, (jump, _) in enumerate(channels)
              if dot(jump, direction) != 0]
    if not active:
        return True
    orders = {i: dot(channels[i][1][0], direction) for i in active}
    minimum = min(orders.values())
    return all(dot(channels[i][0], direction) > 0
               for i in active if orders[i] == minimum)


def main():
    zero = F(0)
    one = F(1)

    # A lower source is neutral and must not affect the active minimum.
    neutral_fixture = [
        ((zero, one), ((zero, zero),)),
        ((one, zero), ((one, zero),)),
    ]
    r = (one, zero)
    assert rate_test(neutral_fixture, [((zero, zero),)] * 2, r)
    assert monomial_source_test(neutral_fixture, r)

    # Different source vectors tie in direction r; one outward tie refutes.
    tie_fixture = [
        ((-one, zero), ((zero, zero),)),
        ((one, zero), ((zero, one),)),
    ]
    assert not rate_test(tie_fixture, [((zero, zero),)] * 2, r)
    assert not monomial_source_test(tie_fixture, r)

    # A nonconstant common denominator cancels on an exact finite direction
    # grid, including directions with neutral channels and support ties.
    grid_fixture = [
        ((one, zero), ((zero, zero),)),
        ((-one, one), ((one, zero),)),
        ((zero, -one), ((zero, one),)),
    ]
    common_q = ((zero, zero), (F(2), zero), (zero, F(3)))
    checked = 0
    for rx, ry in product(range(-4, 5), repeat=2):
        direction = (F(rx), F(ry))
        assert rate_test(grid_fixture, [common_q] * 3, direction) == \
            monomial_source_test(grid_fixture, direction)
        checked += 1

    # The graph 0->1, 2->1 passes with a shared Q=1+x^10. Making the second
    # denominator reaction-specific reverses the negative-direction minimum.
    one_d_channels = [
        ((one,), ((zero,),)),
        ((-one,), ((F(2),),)),
    ]
    shared_q = ((zero,), (F(10),))
    separate_q = [((zero,),), ((zero,), (F(10),))]
    rneg = (-one,)
    assert monomial_source_test(one_d_channels, rneg)
    assert rate_test(one_d_channels, [shared_q] * 2, rneg)
    assert not rate_test(one_d_channels, separate_q, rneg)

    print("PASS: a lower neutral source is excluded before minimization")
    print("PASS: an outward channel tied at the active minimum refutes")
    print(f"PASS: common-denominator/source equivalence on {checked} exact directions")
    print("PASS: channel-specific Hill denominator changes the outcome")


if __name__ == "__main__":
    main()
