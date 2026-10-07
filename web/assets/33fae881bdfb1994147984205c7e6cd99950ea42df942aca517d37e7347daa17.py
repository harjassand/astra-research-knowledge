"""Independent exact audit of the low-sector physical-prefix identity.

This checker is intentionally small and exponential: it directly expands
Pfaffians and disjoint minors on n=4 rational-complex fixtures. It does not
import or execute any peer implementation.
"""
from fractions import Fraction as Fr
from itertools import combinations, product
from math import comb, factorial
import json
from pathlib import Path


def z(a=0, b=0, den=1):
    return (Fr(a, den), Fr(b, den))


ZERO, ONE = z(), z(1)


def add(x, y):
    return x[0] + y[0], x[1] + y[1]


def neg(x):
    return -x[0], -x[1]


def sub(x, y):
    return add(x, neg(y))


def mul(x, y):
    return x[0] * y[0] - x[1] * y[1], x[0] * y[1] + x[1] * y[0]


def div(x, y):
    den = y[0] * y[0] + y[1] * y[1]
    if den == 0:
        raise ZeroDivisionError
    return ((x[0] * y[0] + x[1] * y[1]) / den,
            (x[1] * y[0] - x[0] * y[1]) / den)


def abs2(x):
    return x[0] * x[0] + x[1] * x[1]


def det(a):
    """Exact Gaussian-rational determinant by pivoted elimination."""
    n = len(a)
    if n == 0:
        return ONE
    m = [list(row) for row in a]
    value, sign = ONE, 1
    for j in range(n):
        pivot = next((i for i in range(j, n) if m[i][j] != ZERO), None)
        if pivot is None:
            return ZERO
        if pivot != j:
            m[j], m[pivot] = m[pivot], m[j]
            sign = -sign
        p = m[j][j]
        value = mul(value, p)
        for i in range(j + 1, n):
            if m[i][j] == ZERO:
                continue
            factor = div(m[i][j], p)
            for h in range(j + 1, n):
                m[i][h] = sub(m[i][h], mul(factor, m[j][h]))
    return value if sign == 1 else neg(value)


def pfaffian(a):
    """Exact recursive Pfaffian; used only on these tiny audit fixtures."""
    n = len(a)
    if n == 0:
        return ONE
    if n % 2:
        return ZERO
    total = ZERO
    for j in range(1, n):
        rest = [h for h in range(1, n) if h != j]
        minor = [[a[r][c] for c in rest] for r in rest]
        term = mul(a[0][j], pfaffian(minor))
        total = add(total, term if j % 2 else neg(term))
    return total


def xk(a, k):
    n = len(a)
    if k == 0:
        return Fr(1)
    if 2 * k > n:
        return Fr(0)
    total = Fr(0)
    for rows in combinations(range(n), 2 * k):
        minor = [[a[i][j] for j in rows] for i in rows]
        total += abs2(pfaffian(minor))
    return total


def skew_restriction(f, labels, signs, up_value, retained):
    """A_ij=tau_i F_ij - tau_j F_ji for a real integer z=up_value."""
    tau = []
    for i, lab in enumerate(labels):
        if lab == 0:       # forced up
            tau.append(Fr(up_value))
        elif lab in (1, 2):  # forced down or empty
            tau.append(Fr(0))
        else:              # undecided physical site, with a sign
            tau.append(Fr(signs[i]))
    return [[sub(tuple(tau[i] * v for v in f[i][j]),
                 tuple(tau[j] * v for v in f[j][i]))
             for j in retained] for i in retained]


def prefix_draw(f, k, labels, signs):
    """Finite-difference / deletion formula, evaluated independently."""
    n = len(f)
    up = {i for i, x in enumerate(labels) if x == 0}
    down = {i for i, x in enumerate(labels) if x == 1}
    empty = {i for i, x in enumerate(labels) if x == 2}
    a, b = len(up), len(down)
    if a > k or b > k or 2 * k > n - len(empty):
        return Fr(0)
    degree = 2 * a
    answer = Fr(0)
    for tsize in range(b + 1):
        for t in combinations(sorted(down), tsize):
            removed = set(t)
            retained = [i for i in range(n) if i not in empty and i not in removed]
            if len(retained) < 2 * k:
                continue
            difference = Fr(0)
            for j in range(degree + 1):
                val = xk(skew_restriction(f, labels, signs, j, retained), k)
                difference += (-1) ** (degree - j) * comb(degree, j) * val
            top = difference / factorial(degree)
            answer += (-1) ** tsize * top
    return answer


def physical_mass(f, k, labels):
    """Direct ordered disjoint-minor sum under the physical prefix."""
    n = len(f)
    up = {i for i, x in enumerate(labels) if x == 0}
    down = {i for i, x in enumerate(labels) if x == 1}
    empty = {i for i, x in enumerate(labels) if x == 2}
    total = Fr(0)
    for I in combinations(range(n), k):
        I = set(I)
        if not up <= I or I & (down | empty):
            continue
        for J0 in combinations(range(n), k):
            J = set(J0)
            if I & J or not down <= J or J & empty:
                continue
            d = det([[f[i][j] for j in sorted(J)] for i in sorted(I)])
            total += abs2(d)
    return total


def run_fixture(f):
    n = len(f)
    assignments = sign_cases = child_identities = positive_cases = 0
    for labels in product(range(4), repeat=n):  # up, down, empty, free
        free = [i for i, x in enumerate(labels) if x == 3]
        signs_list = product((-1, 1), repeat=len(free))
        all_signs = []
        for vals in signs_list:
            s = [1] * n
            for i, val in zip(free, vals):
                s[i] = val
            all_signs.append(s)
        for k in range(n // 2 + 1):
            mu = physical_mass(f, k, labels)
            draws = [prefix_draw(f, k, labels, s) for s in all_signs]
            assert all(y >= 0 for y in draws), (k, labels, draws)
            mean = sum(draws, Fr(0)) / len(draws)
            assert mean == mu, (k, labels, mean, mu)
            up = labels.count(0)
            down = labels.count(1)
            if up <= k and down <= k and 2 * k <= n - labels.count(2):
                c_ab = comb(2 * k - up - down, k - up)
                assert all(y <= c_ab * mu for y in draws), (k, labels, c_ab, mu, draws)
                second = sum((y * y for y in draws), Fr(0)) / len(draws)
                assert second <= c_ab * mu * mu, (k, labels, second, c_ab, mu)
                if c_ab == 1:
                    assert all(y == mu for y in draws), (k, labels, mu, draws)
                assert (mu > 0) == any(y > 0 for y in draws), (k, labels, mu, draws)
                positive_cases += int(mu > 0)
            else:
                assert mu == 0 and all(y == 0 for y in draws)
            assignments += 1
            sign_cases += len(draws)
        # Exact physical-prefix partition across every free site.
        for i in free:
            # Check each legal sector separately below; replacing site i by
            # up/down/empty partitions all configurations exactly once.
            for k in range(n // 2 + 1):
                child_sum = Fr(0)
                for child in (0, 1, 2):
                    lab = list(labels)
                    lab[i] = child
                    child_sum += physical_mass(f, k, lab)
                assert physical_mass(f, k, labels) == child_sum, (k, labels, i)
                child_identities += 1
    return {
        "n": n,
        "prefix_sector_cases": assignments,
        "exact_sign_prefix_sector_cases": sign_cases,
        "positive_prefix_cases": positive_cases,
        "exact_child_partition_checks": child_identities,
        "status": "PASS",
    }


def main():
    f = [
        [z(1), z(1, 1, 2), z(-1), z(2)],
        [z(2), z(1), z(1, -2, 3), z(-1, 1, 2)],
        [z(3, 1, 2), z(-2), z(1), z(1, 0, 2)],
        [z(1, -1), z(3), z(-1, 1, 2), z(2)],
    ]
    report = {
        "method": "independent direct Pfaffian/minor exhaustive exact check",
        "peer_code_imported_or_executed": False,
        "fixture": run_fixture(f),
        "claims_checked": [
            "E_sign Y(prefix,sign) equals exact physical prefix mass",
            "Y is pointwise nonnegative and obeys C_ab times prefix-mass bound",
            "second moment is at most C_ab times squared prefix mass",
            "C_ab=1 gives an exactly constant sample",
            "positive prefix iff at least one sign word has Y>0",
            "parent prefix mass is exactly the sum of up/down/empty child masses",
        ],
    }
    out = Path(__file__).with_suffix(".json")
    out.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
