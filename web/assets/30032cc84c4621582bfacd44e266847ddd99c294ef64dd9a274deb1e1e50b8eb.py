#!/usr/bin/env python3
"""Independent exact audit: integer-scaled DP versus all binary strings.

No root checker is imported. Brute force occurs only in this finite diagnostic;
the implemented marginal DP itself has polynomial state count.
"""
from collections import Counter, defaultdict
from fractions import Fraction as Q
from itertools import product
from math import factorial
from pathlib import Path
import json


def signature(x):
    positions = [i + 1 for i, bit in enumerate(x) if bit]
    if not positions:
        return None
    return tuple(sorted(Counter(v - u for u, v in zip(positions, positions[1:])).items()))


def partitions(cap):
    p = [1] + [0] * cap
    for j in range(1, cap + 1):
        for s in range(j, cap + 1):
            p[s] += p[s - j]
    return p


def integer_marginal(n, prefix, p, facts):
    """Returns H(prefix)=K_n*n!*Q_n(prefix), not a floating probability."""
    t = len(prefix)
    assert 0 <= t <= n
    positions = [i + 1 for i, bit in enumerate(prefix) if bit]
    if not positions:
        total = facts[n]  # Separate allzero type.
        for s, count in enumerate(p):
            available = max(n - s - t, 0)
            assert facts[n] % (n - s) == 0
            total += count * available * (facts[n] // (n - s))
        return total
    a, last = positions[0], positions[-1]
    c = Counter(v - u for u, v in zip(positions, positions[1:]))
    r, b, cap = len(positions) - 1, t - last, n - a
    table = {(0, 0): (1, 0)}
    for j in range(1, cap + 1):
        next_table = defaultdict(lambda: [0, 0])
        minimum = c[j]
        for (s, R), (base, marked) in table.items():
            for count in range(minimum, (cap - s) // j + 1):
                w = facts[count] // facts[count - minimum]
                mark = count - minimum if j > b else 0
                item = next_table[s + j * count, R + count]
                item[0] += w * base
                item[1] += w * (marked + mark * base)
        table = next_table
    total = 0
    for (s, R), (base, marked) in table.items():
        assert R >= r and s >= R
        if R == r:
            denom = (n - s) * facts[R]
            numerator = base
        else:
            denom = (n - s) * facts[R] // facts[R - r - 1]
            numerator = marked
        assert denom > 0 and facts[n] % denom == 0
        total += numerator * (facts[n] // denom)
    return total


def renewal_mass(x, law):
    n = len(x)
    mean = sum((j * mass for j, mass in law.items()), Q(0))
    ones = [i + 1 for i, bit in enumerate(x) if bit]
    if not ones:
        return sum((max(j - n, 0) * mass for j, mass in law.items()), Q(0)) / mean
    a = ones[0]
    result = sum((mass for j, mass in law.items() if j >= a), Q(0)) / mean
    for u, v in zip(ones, ones[1:]):
        result *= law.get(v - u, Q(0))
    age = n - ones[-1]
    result *= sum((mass for j, mass in law.items() if j > age), Q(0))
    return result


def audit(n):
    facts = [factorial(j) for j in range(n + 1)]
    p = partitions(n - 1)
    K = 1 + sum(p)
    strings = list(product((0, 1), repeat=n))
    groups = Counter(signature(x) for x in strings)
    assert len(groups) == K
    for key, count in groups.items():
        if key is None:
            assert count == 1
            continue
        span = sum(j * c for j, c in key)
        R = sum(c for _, c in key)
        expected = (n - span) * facts[R]
        for _, c in key:
            expected //= facts[c]
        assert count == expected and facts[n] % count == 0
    brute = defaultdict(int)
    for x in strings:
        weight = facts[n] // groups[signature(x)]
        for t in range(n + 1):
            brute[x[:t]] += weight
    comparisons = 0
    normalizations = 0
    for prefix, expected in brute.items():
        actual = integer_marginal(n, prefix, p, facts)
        assert actual == expected, (n, prefix, actual, expected)
        comparisons += 1
        if len(prefix) < n:
            children = (integer_marginal(n, prefix + (0,), p, facts)
                        + integer_marginal(n, prefix + (1,), p, facts))
            assert children == actual
            normalizations += 1
    assert brute[()] == K * facts[n]
    laws = [
        {1: Q(1)},
        {2: Q(1)},
        {1: Q(1, 3), 2: Q(1, 3), 5: Q(1, 3)},
        {1: Q(1, 1000), 200: Q(999, 1000)},
        {200: Q(1)},
        {1: Q(1, 2), 4: Q(1, 2)},
    ]
    regret_checks = 0
    for law in laws:
        masses = {x: renewal_mass(x, law) for x in strings}
        assert sum(masses.values()) == 1
        for x, mass in masses.items():
            code = Q(brute[x], K * facts[n])
            assert mass <= K * n * code
            regret_checks += 1
    return dict(N=n, types=K, prefix_equalities=comparisons,
                normalization_equalities=normalizations,
                exact_regret_checks=regret_checks,
                marginal_scale_bits=(K * facts[n]).bit_length())


def main():
    checks = [audit(n) for n in range(1, 11)]
    # The horizon family is deliberately not projective.
    q2 = Q(integer_marginal(2, (0,), partitions(1), [factorial(i) for i in range(3)]),
           (1 + sum(partitions(1))) * factorial(2))
    q3 = Q(integer_marginal(3, (0,), partitions(2), [factorial(i) for i in range(4)]),
           (1 + sum(partitions(2))) * factorial(3))
    assert q2 == Q(1, 2) and q3 == Q(13, 30) and q2 != q3
    result = dict(status='PASS', arithmetic='exact integers and Fraction', cases=checks,
                  total_prefix_equalities=sum(x['prefix_equalities'] for x in checks),
                  total_normalizations=sum(x['normalization_equalities'] for x in checks),
                  total_exact_regret_checks=sum(x['exact_regret_checks'] for x in checks),
                  nonprojectivity_example={'Q2_first0':str(q2),'Q3_first0':str(q3)},
                  scope='Finite independent diagnostic, not all-N proof or external validation.')
    out = Path(__file__).with_name('CHECKS.json')
    out.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: result[k] for k in ('status','total_prefix_equalities','total_normalizations','total_exact_regret_checks')}))


if __name__ == '__main__':
    main()
