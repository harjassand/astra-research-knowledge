"""Exact checks for reciprocal dephasing-block acquisition and cost claims.

This is a small independent source-geometry checker, not a reduced compiler.
The only approximate values in its JSON output are human-readable diagnostics.
Every asserted equality/inequality uses Fraction or integer arithmetic.
"""
from __future__ import annotations

from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path


def eye(d=3):
    return tuple(tuple(F(i == j) for j in range(d)) for i in range(d))


def outer(x, y):
    return tuple(tuple(a * b for b in y) for a in x)


def transpose(a):
    return tuple(zip(*a))


def mul(a, b):
    bt = transpose(b)
    return tuple(tuple(sum((x * y for x, y in zip(row, col)), F(0))
                       for col in bt) for row in a)


def scale(c, a):
    return tuple(tuple(c * x for x in row) for row in a)


def power(a, k):
    result = eye(len(a))
    while k:
        if k & 1:
            result = mul(a, result)
        a = mul(a, a)
        k >>= 1
    return result


def trace(a):
    return sum((a[i][i] for i in range(len(a))), F(0))


def apply_word(ops, word):
    result = eye()
    for index in word:
        result = mul(ops[index], result)
    return result


def axes(q):
    # q is a power of four, so its integer square root is exact.
    root = 1 << ((q.bit_length() - 1) // 2)
    assert root * root == q
    return ((F(1), F(0), F(0)),
            (F(q - 1, q + 1), F(2 * root, q + 1), F(0)))


def minimum_half_norm_length(c):
    # A length-L alternating word has norm c**(L-1).
    lo, hi = 1, 2
    while c ** (2 * (hi - 1)) > F(1, 4):
        hi *= 2
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        if c ** (2 * (mid - 1)) <= F(1, 4):
            hi = mid
        else:
            lo = mid
    assert c ** (2 * (hi - 1)) <= F(1, 4)
    assert c ** (2 * (hi - 2)) > F(1, 4)
    return hi


def check_family(n):
    q = 4 ** n
    n0, n1 = axes(q)
    c = n1[0]
    assert sum(x * x for x in n1) == 1
    p0, p1 = (outer(axis, axis) for axis in (n0, n1))
    for p in (p0, p1):
        assert transpose(p) == p
        assert mul(p, p) == p
    b = mul(p1, p0)
    bd = mul(p0, p1)
    assert b == scale(c, outer(n1, n0))
    assert bd == transpose(b)
    assert mul(bd, b) == scale(c * c, p0)
    # Squared one-step distance from span{n0}.
    h = p1[0][0]
    z = mul(p1, p1)[0][0]
    assert h == z == c * c
    assert z - h * h == c * c * (1 - c * c)

    primitive_word_count = 0
    for length in range(1, 7):
        for word in product(range(2), repeat=length):
            w = apply_word((p0, p1), word)
            switches = sum(a != b for a, b in zip(word, word[1:]))
            boundary = int(word[0] == 1) + int(word[-1] == 1)
            assert w == scale(c ** switches,
                              outer((n0, n1)[word[-1]],
                                    (n0, n1)[word[0]]))
            assert mul(transpose(w), w) == scale(
                c ** (2 * switches), (p0, p1)[word[0]])
            assert w[0][0] == c ** (switches + boundary)
            primitive_word_count += 1

    macro_word_count = 0
    for length in range(1, 5):
        for word in product(range(2), repeat=length):
            w = apply_word((b, bd), word)
            # Every nonempty product has rank one. Its Frobenius norm is
            # therefore exactly its operator norm.
            norm_squared = trace(mul(transpose(w), w))
            assert norm_squared <= c ** (2 * length)
            macro_word_count += 1

    eta = F(1, 1000)
    k = 1
    reads = 0
    actuator_applications = 0
    while True:
        d = power(b, k)
        scalar = d[0][0]
        assert scalar == c ** (2 * k)
        assert mul(transpose(d), d) == scale(c ** (4 * k - 2), p0)
        # Worst upward reading error eta, followed by its valid upper
        # endpoint. Any other allowed read has an endpoint no larger.
        upper = scalar + 2 * eta
        reads += 1
        actuator_applications += 2 * k
        if upper <= F(1, 4):
            assert c ** (4 * k - 2) <= upper <= F(1, 4)
            break
        assert scalar > F(1, 4)  # No allowed noise could stop earlier.
        k *= 2
    assert k == q // 2
    assert reads == 2 * n
    assert actuator_applications == 2 * q - 2
    minimum_length = minimum_half_norm_length(c)
    assert minimum_length <= 2 * k

    c_pair = F(4 * q - 1, 4 * q + 1)
    difference = c_pair - c
    assert difference == F(6 * q, (q + 1) * (4 * q + 1))
    assert difference < F(3, 2 * q)
    for exponent in range(1, 9):
        assert 0 < c_pair ** exponent - c ** exponent <= exponent * difference
    future_first = c ** q
    future_second = c_pair ** q
    assert future_first < F(1, 7)
    assert future_second > F(1, 2)
    assert future_second - future_first > F(5, 14)
    return {
        "n": n,
        "Q": q,
        "axis_cosine": str(c),
        "primitive_words_checked": primitive_word_count,
        "macro_words_checked": macro_word_count,
        "exact_dictionary_novelty": str(c * c * (1 - c * c)),
        "centered_error_contract": str(eta),
        "doubling_reads": reads,
        "doubling_primitive_applications": actuator_applications,
        "selected_macro_primitive_length": 2 * k,
        "minimum_half_norm_primitive_length": minimum_length,
        "selected_macro_norm_diagnostic": float(c ** (2 * k - 1)),
        "paired_future_centered_gap_diagnostic": float(
            future_second - future_first),
        "all_assertions_exact": True,
    }


def main():
    cases = [check_family(n) for n in range(1, 6)]
    result = {
        "purpose": "Independent exact block geometry, acquisition, and physical-cost checks",
        "no_compiler_claim": True,
        "cases": cases,
        "total_primitive_words_checked": sum(x["primitive_words_checked"] for x in cases),
        "total_macro_words_checked": sum(x["macro_words_checked"] for x in cases),
        "all_checks_passed": True,
    }
    destination = Path(__file__).with_name("BLOCK_GEOMETRY_RESULTS.json")
    destination.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({
        "all_checks_passed": True,
        "primitive_words": result["total_primitive_words_checked"],
        "macro_words": result["total_macro_words_checked"],
        "costs": [[x["Q"], x["doubling_reads"],
                   x["doubling_primitive_applications"],
                   x["minimum_half_norm_primitive_length"]] for x in cases],
        "output": str(destination),
    }, indent=2))


if __name__ == "__main__":
    main()
