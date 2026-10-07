#!/usr/bin/env python3
"""Independent exact Gaussian-integer audit of the Luna estimator and prefixes.

This implements polynomial-time per-sign coefficient computation by Newton
traces, not enumeration of principal minors. Direct Pfaffians/minors appear
only in separate small diagnostic comparators.
"""
import itertools
import json
import math
import random
from fractions import Fraction
from pathlib import Path

ZERO = (0, 0)
ONE = (1, 0)


def add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def sub(a, b):
    return (a[0] - b[0], a[1] - b[1])


def mul(a, b):
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def scale(a, x):
    return (a[0] * x, a[1] * x)


def conj(a):
    return (a[0], -a[1])


def norm(a):
    return a[0] ** 2 + a[1] ** 2


def matrix_mul(a, b):
    n = len(a)
    c = [[ZERO for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for r in range(n):
            if a[i][r] != ZERO:
                for j in range(n):
                    c[i][j] = add(c[i][j], mul(a[i][r], b[r][j]))
    return c


def coefficient_by_traces(a, k):
    """Coefficient of the formal square root det(I+t A* A), exactly."""
    n = len(a)
    if k == 0:
        return 1
    if 2 * k > n:
        return 0
    adjoint = [[conj(a[j][i]) for j in range(n)] for i in range(n)]
    b = matrix_mul(adjoint, a)
    power = b
    traces = [0]
    for degree in range(1, k + 1):
        trace = ZERO
        for i in range(n):
            trace = add(trace, power[i][i])
        assert trace[1] == 0
        traces.append(trace[0])
        if degree != k:
            power = matrix_mul(power, b)
    d, q = [1], [1]
    for degree in range(1, k + 1):
        numerator = sum((-1) ** (j - 1) * d[degree - j] * traces[j]
                        for j in range(1, degree + 1))
        assert numerator % degree == 0
        d.append(numerator // degree)
        numerator = d[degree] - sum(q[j] * q[degree - j]
                                   for j in range(1, degree))
        assert numerator % 2 == 0
        q.append(numerator // 2)
        assert q[-1] >= 0
    return q[k]


def skew(f, activities, retained=None):
    if retained is None:
        retained = tuple(range(len(f)))
    return [[sub(scale(f[i][j], activities[i]), scale(f[j][i], activities[j]))
             for j in retained] for i in retained]


def pfaffian(a):
    if not a:
        return ONE
    if len(a) % 2:
        return ZERO
    value = ZERO
    for j in range(1, len(a)):
        others = [i for i in range(len(a)) if i not in (0, j)]
        rest = [[a[i][l] for l in others] for i in others]
        value = add(value, scale(mul(a[0][j], pfaffian(rest)), (-1) ** (j + 1)))
    return value


def determinant(a):
    # Independent small Leibniz comparator, not the production coefficient path.
    if not a:
        return ONE
    value = ZERO
    for permutation in itertools.permutations(range(len(a))):
        term = ONE
        for i, j in enumerate(permutation):
            term = mul(term, a[i][j])
        inversions = sum(permutation[i] > permutation[j]
                         for i in range(len(a)) for j in range(i + 1, len(a)))
        value = add(value, scale(term, (-1) ** inversions))
    return value


def direct_norm(f, k, up=(), down=(), empty=()):
    value = 0
    up, down, empty = set(up), set(down), set(empty)
    for i in itertools.combinations(range(len(f)), k):
        si = set(i)
        if not up <= si or si & (down | empty):
            continue
        for j in itertools.combinations(range(len(f)), k):
            sj = set(j)
            if si & sj or not down <= sj or sj & (up | empty):
                continue
            value += norm(determinant([[f[x][y] for y in j] for x in i]))
    return value


def prefix_sample(f, k, signs, up=(), down=(), empty=()):
    """Nonnegative sample using top scalar coefficient + row inclusion-exclusion."""
    n, a, b = len(f), len(up), len(down)
    if a > k or b > k or 2 * k > n - len(empty):
        return 0
    up, down, empty = set(up), set(down), set(empty)
    assert not (up & down or up & empty or down & empty)
    degree = 2 * a
    answer = 0
    for removed_bits in itertools.product((0, 1), repeat=b):
        removed = {x for x, bit in zip(sorted(down), removed_bits) if bit}
        retained = tuple(i for i in range(n) if i not in empty | removed)
        top_difference = 0
        for z in range(degree + 1):
            activities = [z if i in up else 0 if i in down | empty else signs[i]
                          for i in range(n)]
            value = coefficient_by_traces(skew(f, activities, retained), k)
            top_difference += (-1) ** (degree - z) * math.comb(degree, z) * value
        assert top_difference % math.factorial(degree) == 0
        top = top_difference // math.factorial(degree)
        assert top >= 0
        answer += (-1) ** len(removed) * top
    assert answer >= 0
    return answer


def prefix_sample_direct(f, k, signs, up=(), down=(), empty=()):
    """Independent comparator by Fourier projection of each principal Pfaffian."""
    n, up, down, empty = len(f), set(up), set(down), set(empty)
    if len(up) > k or len(down) > k or 2 * k > n - len(empty):
        return 0
    answer = 0
    for rows in itertools.combinations([i for i in range(n) if i not in empty], 2 * k):
        if not up | down <= set(rows):
            continue
        projected = ZERO
        for forced_signs in itertools.product((-1, 1), repeat=len(up)):
            activities = [0 if i in down | empty else signs[i] for i in range(n)]
            character = 1
            for i, s in zip(sorted(up), forced_signs):
                activities[i] = s
                character *= s
            projected = add(projected, scale(pfaffian(skew(f, activities, rows)), character))
        divisor = 1 << len(up)
        assert projected[0] % divisor == projected[1] % divisor == 0
        projected = (projected[0] // divisor, projected[1] // divisor)
        answer += norm(projected)
    return answer


def audit_case(f, k, up=(), down=(), empty=(), name="", denominator=1):
    n = len(f)
    exact = direct_norm(f, k, up, down, empty)
    free = [i for i in range(n) if i not in set(up) | set(down) | set(empty)]
    values = []
    c = math.comb(2 * k - len(up) - len(down), k - len(up))
    assert (1 << len(down)) * c <= math.comb(2 * k, k)
    for word in itertools.product((-1, 1), repeat=len(free)):
        signs = [0] * n
        for i, s in zip(free, word):
            signs[i] = s
        value = prefix_sample(f, k, signs, up, down, empty)
        assert value == prefix_sample_direct(f, k, signs, up, down, empty)
        assert value <= c * exact
        values.append(value)
    mean = Fraction(sum(values), len(values))
    second = Fraction(sum(x * x for x in values), len(values))
    assert mean == exact
    assert second <= c * exact * exact
    return {"name": name, "n": n, "k": k, "forced_up": list(up),
            "forced_down": list(down), "forced_empty": list(empty),
            "sign_words": len(values), "norm_integer": exact,
            "common_denominator": denominator,
            "norm_rational": str(Fraction(exact, denominator ** (2 * k))),
            "Cauchy_relative_second_moment_bound": c,
            "relative_second_moment_exact": str(second / (exact * exact)) if exact else "ZERO",
            "all_exact_checks_passed": True}


def main():
    rng = random.Random(2032107)
    cases = []
    for n in (3, 4, 5, 6):
        f = [[(rng.randrange(-2, 3), rng.randrange(-2, 3)) for j in range(n)] for i in range(n)]
        for k in range(n // 2 + 1):
            cases.append(audit_case(f, k, name="dense_complex"))
        k = n // 2
        if k:
            cases.append(audit_case(f, k, up=(0,), down=(1,), name="complex_up_down_prefix"))
            cases.append(audit_case(f, 1, down=(0,), empty=(1,), name="complex_down_empty_prefix"))
        if k >= 2:
            cases.append(audit_case(f, k, up=(0, 1), name="two_forced_up"))
    for k in (1, 2, 3):
        n = 2 * k
        f = [[ZERO for _ in range(n)] for _ in range(n)]
        for i in range(0, n, 2):
            f[i][i + 1] = f[i + 1][i] = ONE
        record = audit_case(f, k, name="independent_swap_blocks")
        assert record["relative_second_moment_exact"] == str(1 << k)
        cases.append(record)
    f = [[ONE if i != j else ZERO for j in range(4)] for i in range(4)]
    record = audit_case(f, 2, name="positive_well_conditioned_zero_sector")
    assert record["norm_integer"] == 0
    cases.append(record)
    # Rational-complex entries with a common denominator. The integer-path
    # sample has denominator D^(2k), with no floating arithmetic.
    f = [[(rng.randrange(-5, 6), rng.randrange(-5, 6)) for j in range(4)] for i in range(4)]
    cases.append(audit_case(f, 2, name="rational_complex_denominator_6", denominator=6))
    cases.append(audit_case(f, 2, up=(0,), down=(1,),
                            name="rational_complex_denominator_6_prefix", denominator=6))
    # Very small positive sector despite bounded ambient conditioning.
    # For delta=2^-L this is the earlier independently derived symmetric
    # cancellation fixture, represented by exact numerators over D=2^(2L).
    for bits in (4, 32):
        d, h = 1 << (2 * bits), 1 << bits
        f = [[ZERO for _ in range(4)] for _ in range(4)]
        for i in range(1, 4):
            for j in range(i + 1, 4):
                f[i][j] = f[j][i] = (d, 0)
        for i, x in enumerate((d + 1, d + h + 2, d - h + 3), 1):
            f[0][i] = f[i][0] = (x, 0)
        record = audit_case(f, 2, name=f"tiny_positive_sector_L{bits}", denominator=d)
        delta = Fraction(1, h)
        assert Fraction(record["norm_integer"], d ** 4) == 12 * delta ** 2 * (1 - delta + delta ** 2)
        cases.append(record)
        cases.append(audit_case(f, 2, up=(0,), down=(1,),
                                name=f"tiny_positive_prefix_L{bits}", denominator=d))
    result = {"scope": "Exact finite identity/moment/prefix checks; no full-accuracy Born FPRAS run",
              "cases": len(cases), "sign_words": sum(x["sign_words"] for x in cases),
              "all_assertions_passed": True, "fixtures": cases}
    Path(__file__).with_name("pfaffian_prefix_checks.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({key: value for key, value in result.items() if key != "fixtures"}))


if __name__ == "__main__":
    main()
