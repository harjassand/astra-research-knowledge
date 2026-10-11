"""Finite independent checks for the arbitrary-support semigroup derivation.

Stdlib only. The proof in ARBITRARY_SUPPORT_SEMIGROUP.md is primary;
these checks can detect bookkeeping errors but cannot certify the theorem.
"""
from collections import deque
from fractions import Fraction as F
from itertools import combinations, product
from math import ceil, lcm
from pathlib import Path
import json


def multiply(table, x, y):
    identity = len(table)
    if x == identity:
        return y
    if y == identity:
        return x
    return table[x][y]


def power(table, a, exponent):
    out = len(table)
    while exponent:
        if exponent & 1:
            out = multiply(table, out, a)
        a = multiply(table, a, a)
        exponent >>= 1
    return out


def index_period(table, a):
    seen, k, x = {}, 1, a
    while x not in seen:
        seen[x] = k
        k += 1
        x = table[x][a]
    return seen[x], k - seen[x]


def defect_words(table, support, a, p):
    initial = (len(table), 0)
    words = {initial: ()}
    todo = deque([initial])
    while todo:
        y, residue = todo.popleft()
        for b in support:
            if b == a:
                continue
            next_state = (multiply(table, y, b), (residue + 1) % p)
            if next_state not in words:
                words[next_state] = words[(y, residue)] + (b,)
                todo.append(next_state)
    return words


def metadata_residue_graph(table, support):
    periods = {a: index_period(table, a) for a in support}
    words = {a: defect_words(table, support, a, periods[a][1]) for a in support}
    C = max(len(w) for mapping in words.values() for w in mapping.values())
    tau = max(t for t, p in periods.values())
    B = sum(t - 1 for t, p in periods.values())
    L = lcm(*(p for t, p in periods.values()))
    assert C <= (len(table) + 1) * max(p for t, p in periods.values()) - 1
    return periods, words, C, tau, B, L


def metadata(table, support):
    """Sharper local-unit construction, independently compared with old graph."""
    periods = {a: index_period(table, a) for a in support}
    words = {}
    for a in support:
        tau_a, p_a = periods[a]
        e = power(table, a, p_a * ceil(F(tau_a, p_a)))
        u = table[e][a]
        inverse_u = e if p_a == 1 else power(table, u, p_a - 1)
        assert table[u][inverse_u] == e
        generators = {b: table[inverse_u][table[e][b]] for b in support if b != a}
        local_words = {e: ()}
        todo = deque([e])
        while todo:
            h = todo.popleft()
            for b, generator in generators.items():
                next_h = table[h][generator]
                if next_h not in local_words:
                    local_words[next_h] = local_words[h] + (b,)
                    todo.append(next_h)
        encoded = {}
        for h, word in local_words.items():
            y = len(table)
            for b in word:
                y = multiply(table, y, b)
            key = (y, len(word) % p_a)
            assert key not in encoded
            encoded[key] = word
        words[a] = encoded
    C = max(len(w) for mapping in words.values() for w in mapping.values())
    tau = max(t for t, p in periods.values())
    B = min(len(table) - 1, sum(t - 1 for t, p in periods.values()))
    L = lcm(*(p for t, p in periods.values()))
    assert C <= len(table) - 1
    return periods, words, C, tau, B, L


def relation_and_witnesses(table, support, n, meta):
    periods, words, C, tau, B, L = meta
    assert n >= tau + C
    witnesses = {}
    for a in support:
        for (y, residue), word in words[a].items():
            z = multiply(table, power(table, a, n - len(word)), y)
            witnesses.setdefault((a, z), word)
    return set(witnesses), witnesses


def direct_abundant_relation(table, support, n, a, threshold):
    states = {(len(table), 0)}
    for step in range(n):
        states = {
            (multiply(table, y, b), min(threshold, count + (a == b)))
            for y, count in states for b in support
        }
    return {y for y, count in states if count == threshold}


def solve(matrix, vector):
    n = len(vector)
    augmented = [list(map(F, row)) + [F(rhs)] for row, rhs in zip(matrix, vector)]
    for col in range(n):
        pivot = next(row for row in range(col, n) if augmented[row][col])
        augmented[col], augmented[pivot] = augmented[pivot], augmented[col]
        p = augmented[col][col]
        augmented[col] = [x / p for x in augmented[col]]
        for row in range(n):
            if row != col:
                p = augmented[row][col]
                augmented[row] = [x - p * y for x, y in zip(augmented[row], augmented[col])]
    return [row[-1] for row in augmented]


def construction_check(table, support, n, meta, target_kernel):
    _, witnesses = relation_and_witnesses(table, support, n, meta)
    C = meta[2]
    qsize, m = len(support), len(table)
    weights = list(range(1, qsize + 1))
    mu = [F(w, sum(weights)) for w in weights]
    assert n > 2 * C and min(mu) >= F(C, n)
    M = [[F(0) for b in support] for a in support]
    for i, a in enumerate(support):
        for z, prob in target_kernel[a].items():
            word = witnesses[(a, z)]
            counts = [word.count(b) + ((n - len(word)) if b == a else 0) for b in support]
            assert sum(counts) == n
            actual_product = len(table)
            for b, count in zip(support, counts):
                actual_product = multiply(table, actual_product, power(table, b, count))
            assert actual_product == z
            for j, count in enumerate(counts):
                M[i][j] += prob * F(count, n)
        assert sum(M[i]) == 1 and M[i][i] >= 1 - F(C, n)
    adjusted = solve([[M[i][j] for i in range(qsize)] for j in range(qsize)], mu)
    assert sum(adjusted) == 1 and min(adjusted) >= 0
    assert [sum(adjusted[i] * M[i][j] for i in range(qsize)) for j in range(qsize)] == mu
    target = [sum(mu[i] * target_kernel[a].get(z, F(0)) for i, a in enumerate(support)) for z in range(m)]
    actual = [sum(adjusted[i] * target_kernel[a].get(z, F(0)) for i, a in enumerate(support)) for z in range(m)]
    tv = sum(abs(x - y) for x, y in zip(actual, target)) / 2
    assert tv <= F(C, n)
    return tv


def commutative_semigroups(m):
    coords = [(i, j) for i in range(m) for j in range(i, m)]
    for values in product(range(m), repeat=len(coords)):
        table = [[None] * m for _ in range(m)]
        for (i, j), value in zip(coords, values):
            table[i][j] = table[j][i] = value
        if all(table[table[i][j]][k] == table[i][table[j][k]] for i, j, k in product(range(m), repeat=3)):
            yield table


def nonempty_supports(m):
    for q in range(1, m + 1):
        yield from combinations(range(m), q)


def weak_compositions(total, q):
    if q == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for rest in weak_compositions(total - first, q - 1):
            yield (first,) + rest


def projected_hull(points):
    q = len(points[0])
    if q == 1:
        return (points[0][0],)
    if q == 2:
        return (min(p[0] for p in points), max(p[0] for p in points))
    assert q == 3
    points = sorted(set((p[0], p[1]) for p in points))
    if len(points) <= 1:
        return tuple(points)
    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lower = []
    for p in points:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    upper = []
    for p in reversed(points):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return tuple(lower[:-1] + upper[:-1])


def count_fiber_vertex_check(table, support, n, D):
    powers = {}
    for a in support:
        powers[a] = [len(table)]
        for exponent in range(1, n + 1):
            powers[a].append(multiply(table, powers[a][-1], a))
    fibers = {}
    bounded_fibers = {}
    for counts in weak_compositions(n, len(support)):
        z = len(table)
        for a, count in zip(support, counts):
            z = multiply(table, z, powers[a][count])
        fibers.setdefault(z, []).append(counts)
        if sum(count >= D for count in counts) <= 1:
            bounded_fibers.setdefault(z, []).append(counts)
    for z, points in fibers.items():
        assert z in bounded_fibers
        assert projected_hull(points) == projected_hull(bounded_fibers[z])
    return len(fibers)


counts = dict(semigroups=0, supports=0, relation_checks=0, periodicity_checks=0,
              local_unit_comparisons=0, idempotent_support_checks=0,
              exact_count_fiber_hull_checks=0,
              marginal_balancing_checks=0, sharpness_checks=0, group_coset_checks=0)
max_C = 0
max_tv = F(0)
for m in range(1, 4):
    for table in commutative_semigroups(m):
        counts['semigroups'] += 1
        for support in nonempty_supports(m):
            counts['supports'] += 1
            meta = metadata(table, support)
            old_meta = metadata_residue_graph(table, support)
            periods, words, C, tau, B, L = meta
            max_C = max(max_C, C)
            threshold = tau + C
            for n in range(threshold, threshold + L + 2):
                relation, witnesses = relation_and_witnesses(table, support, n, meta)
                for a in support:
                    direct = direct_abundant_relation(table, support, n, a, periods[a][0])
                    assert direct == {z for base, z in relation if base == a}
                    counts['relation_checks'] += 1
                product_set = {len(table)}
                for step in range(n):
                    product_set = {multiply(table, y, b) for y in product_set for b in support}
                idempotent_relation = set()
                for a in support:
                    t, p = periods[a]
                    e = power(table, a, p * ceil(F(t, p)))
                    idempotent_relation.update((a, z) for z in product_set if table[e][z] == z)
                assert relation == idempotent_relation
                counts['idempotent_support_checks'] += 1
                assert relation == relation_and_witnesses(table, support, n + L, meta)[0]
                counts['periodicity_checks'] += 1
            compare_n = max(tau + C, old_meta[2] + old_meta[3])
            assert relation_and_witnesses(table, support, compare_n, meta)[0] == relation_and_witnesses(table, support, compare_n, old_meta)[0]
            counts['local_unit_comparisons'] += 1
            q = len(support)
            D = tau + max(p for t, p in periods.values()) ** 2
            N_v = q * (D - 1) + 1
            for vertex_n in (N_v, N_v + L):
                counts['exact_count_fiber_hull_checks'] += count_fiber_vertex_check(table, support, vertex_n, D)
            alpha = F(1, q * (q + 1) // 2)
            n = max(tau + C, 2 * C + 1, ceil(F(C, 1) / alpha))
            relation, witnesses = relation_and_witnesses(table, support, n, meta)
            allowed = {a: sorted(z for base, z in relation if base == a) for a in support}
            kernels = [
                {a: {z: F(1, len(allowed[a])) for z in allowed[a]} for a in support},
                {a: {allowed[a][0]: F(1)} for a in support},
                {a: {allowed[a][-1]: F(1)} for a in support},
            ]
            for kernel in kernels:
                max_tv = max(max_tv, construction_check(table, support, n, meta, kernel))
                counts['marginal_balancing_checks'] += 1

# Inward sharpness witness on the V-shaped join semilattice.
join_table = [[0, 2, 2], [2, 1, 2], [2, 2, 2]]
for n in range(2, 101):
    probabilities = [F(n - 1, 2 * n), F(1, 2 * n), F(1, 2)]
    words = [[0] * n, [1] * n, [0] + [1] * (n - 1)]
    marg_a = sum(p * F(word.count(0), n) for p, word in zip(probabilities, words))
    assert marg_a == F(1, 2)
    output = [F(0)] * 3
    for probability, word in zip(probabilities, words):
        value = word[0]
        for letter in word[1:]:
            value = join_table[value][letter]
        output[value] += probability
    target = [F(1, 2), F(0), F(1, 2)]
    assert sum(abs(x - y) for x, y in zip(target, output)) / 2 == F(1, 2 * n)
    assert (n - 1) * output[0] - output[1] == F(n - 2, 2)
    counts['sharpness_checks'] += 1

# Exact group corollary, including supports not equal to G and nontrivial cosets.
for m in range(2, 7):
    table = [[(i + j) % m for j in range(m)] for i in range(m)]
    for support in nonempty_supports(m):
        a0 = support[0]
        H = {0}
        todo = deque([0])
        while todo:
            h = todo.popleft()
            for b in support:
                next_h = (h + b - a0) % m
                if next_h not in H:
                    H.add(next_h)
                    todo.append(next_h)
        C = len(H) - 1
        q = len(support)
        alpha = F(1, q * (q + 1) // 2)
        n = max(2 * C + 1, ceil(F(C, 1) / alpha))
        meta = metadata(table, support)
        n = max(n, meta[2] + meta[3], 2 * meta[2] + 1, ceil(F(meta[2], 1) / alpha))
        relation, witnesses = relation_and_witnesses(table, support, n, meta)
        coset = {(n * a0 + h) % m for h in H}
        assert relation == {(a, z) for a in support for z in coset}
        kernel = {a: {z: F(1, len(coset)) for z in coset} for a in support}
        assert construction_check(table, support, n, meta, kernel) == 0
        counts['group_coset_checks'] += 1

receipt = {
    'status': 'finite diagnostics passed; not general proof certification',
    'counts': counts,
    'max_defect_bound_in_size_at_most_3_tests': max_C,
    'largest_constructor_tv_seen': str(max_tv),
    'mathematical_proof': 'ARBITRARY_SUPPORT_SEMIGROUP.md',
    'scope': 'All labelled commutative semigroups of sizes 1-3, all nonempty supports; cyclic groups 2-6; exact rational calculations.',
}
Path(__file__).with_name('verification_receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps(receipt, indent=2))
