"""Exact checks for the low-output-precision obstruction to ETH Lemma D.5.

Run: python work_tensor_agent/precision_floor.py
All polynomial arithmetic is over fractions.Fraction; no numeric tolerances.
"""
from fractions import Fraction as Q
import json


def v2(x):
    x = Q(x)
    if not x:
        return None
    n, d = abs(x.numerator), x.denominator
    return (n & -n).bit_length() - (d & -d).bit_length()


def times_linear(poly, constant, slope):
    result = [Q(0)] * (len(poly) + 1)
    for j, value in enumerate(poly):
        result[j] += value * constant
        result[j + 1] += value * slope
    return result


def local_poly(a, u, m, t):
    length = 1 << a
    alpha = 2 * length
    h = m // u
    poly = [Q(1)]
    for q in range(-length, length):
        if not q or v2(q) >= u:
            continue
        multiplicity = h * (u - v2(q))
        for _ in range(multiplicity):
            poly = times_linear(poly, 1 - Q(t, q), -Q(alpha, q))
    return poly


def check(a, u, m):
    length, h = 1 << a, m // u
    degree = h * length * (2*u - 2 + Q(2, 1 << u))
    assert degree.denominator == 1
    assert degree <= m * (2*length - 1)
    zero = local_poly(a, u, m, 0)
    assert zero[0] == 1
    contents = {}
    for t in range(-length, length):
        poly = local_poly(a, u, m, t)
        content = min(v2(c) for c in poly if c)
        assert content >= 0
        if t and v2(t) < u:
            i = v2(t)
            d = length >> i
            expected = h*(u-i)*(a+1-i) + h*d*sum(
                (Q(j * min(j, u-i), 1 << j)
                 for j in range(1, a-i+1)), Q(0))
            assert content == expected
            assert content >= Q(m*d, 4*u)
            assert all(v2(c) >= content for c in poly if c)
            contents[str(t)] = content
    return {"a": a, "u": u, "M": m, "degree": int(degree),
            "F_zero": 1, "active_local_contents": contents}


def pin_example(m):
    # L=2, one real diagonal port in each packet. Each edge has two unary
    # delta_1 pins. Thus F(0)=1 and F(T)=W_00(T)^M.
    a, alpha = 1, 4
    result = {}
    for t in [-1, 1]:
        poly = [Q(1)]
        for q in [-2, -1, 1]:
            for _ in range(m):
                poly = times_linear(poly, 1-Q(t, q), -Q(alpha, q))
        content = min(v2(c) for c in poly if c)
        assert content == 2*m
        result[str(t)] = content
    return {"M": m, "root_precision": 1, "F_zero": 1,
            "canonical_tensor_entries": [0, 1],
            "active_local_contents": result}


if __name__ == "__main__":
    results = {"generic_interpolation_examples": [
        check(1, 1, 1), check(2, 1, 4), check(3, 2, 6)],
        "canonical_pin_example": pin_example(8),
        "all_assertions_passed": True}
    print(json.dumps(results, indent=2))
