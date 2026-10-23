#!/usr/bin/env python3
"""Exact integer-interval audit for the companion support formulas."""


def audit(radius: int) -> None:
    assert radius >= 0
    r = radius + 1
    core = range(-r, 5 * r)  # inclusive T=[-r, 5r-1]

    a_supports = [
        set(range(i - max(radius, 1), i + radius + 1)) for i in core
    ]
    b_supports = [set(range(i - radius, i + radius + 1)) for i in core]

    m_a = radius + max(radius, 1) + 1
    m_b = 2 * radius + 1
    assert all(len(set(range(i - max(radius, 1), i + radius + 1))) == m_a
               for i in core)
    assert all(len(set(range(i - radius, i + radius + 1))) == m_b
               for i in core)

    actual_union = set().union(*a_supports, *b_supports)
    expected_lo = -r - max(radius, 1)
    expected_hi = 5 * r - 1 + radius
    expected_union = set(range(expected_lo, expected_hi + 1))
    assert actual_union == expected_union
    assert len(expected_union) == 6 * r + radius + max(radius, 1)

    if radius == 0:
        assert m_a == 2 and m_b == 1
        assert (expected_lo, expected_hi, len(expected_union)) == (-2, 4, 7)
    if radius == 2:
        assert m_a == 5 and m_b == 5
        assert (expected_lo, expected_hi, len(expected_union)) == (-5, 16, 22)


if __name__ == "__main__":
    # One edge case and one nonzero-radius case; this is arithmetic validation,
    # not a sweep over model or physical parameters.
    audit(0)
    audit(2)
    print("support counts and preparation windows pass for R=0 and R=2")
