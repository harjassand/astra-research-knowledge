"""Exact finite paired-hole diagnostics; no FPRAS or Markov chain implemented."""
from itertools import combinations
from functools import lru_cache
import json
import math
import random
import time
from fractions import Fraction


def det_int(matrix):
    if not matrix:
        return 1
    a = [list(row) for row in matrix]
    sign = previous = 1
    n = len(a)
    for k in range(n - 1):
        pivot_row = next((i for i in range(k, n) if a[i][k]), None)
        if pivot_row is None:
            return 0
        if pivot_row != k:
            a[k], a[pivot_row] = a[pivot_row], a[k]
            sign *= -1
        pivot = a[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                num = a[i][j] * pivot - a[i][k] * a[k][j]
                assert num % previous == 0
                a[i][j] = num // previous
            a[i][k] = 0
        previous = pivot
    return sign * a[-1][-1]


def partitions(F):
    n = len(F)
    f = [0] * (1 << n)
    for u in range(1 << n):
        R = [i for i in range(n) if not u >> i & 1]
        if len(R) % 2:
            continue
        for I in combinations(R, len(R) // 2):
            Iset = set(I)
            J = [j for j in R if j not in Iset]
            f[u] += det_int([[F[i][j] for j in J] for i in I]) ** 2
    return f


def paired_basis_partition(pairs, dimension):
    total = Fraction(0)
    for selected in combinations(pairs, dimension // 2):
        columns = [v for first, second, activity in selected
                   for v in (first, second)]
        matrix = [[column[i] for column in columns] for i in range(dimension)]
        weight = math.prod(activity for _, _, activity in selected)
        total += weight * det_int(matrix) ** 2
    return total


def fixed_k_checks(rng, repetitions=12):
    tests = 0
    for n, k in ((3, 1), (4, 1), (4, 2), (5, 2)):
        for _ in range(repetitions):
            F = [[rng.randrange(-2, 3) for _ in range(n)] for _ in range(n)]
            gram_sum = 0
            minor_sum = 0
            for I in combinations(range(n), k):
                cols = []
                for i in I:
                    cols.extend([[int(j == i) for j in range(n)], F[i]])
                gram_sum += det_int([[sum(a * b for a, b in zip(v, w))
                                      for w in cols] for v in cols])
                available = [j for j in range(n) if j not in I]
                for J in combinations(available, k):
                    minor_sum += det_int([[F[i][j] for j in J] for i in I]) ** 2
            assert gram_sum == minor_sum
            dummy = n - 2 * k
            dimension = n + dummy
            e = [[int(i == j) for i in range(dimension)]
                 for j in range(dimension)]
            pairs = [(e[i], F[i] + [0] * dummy, 1) for i in range(n)]
            pairs.extend((e[i], e[j], 1) for i in range(n)
                         for j in range(n, dimension))
            augmented = paired_basis_partition(pairs, dimension)
            assert augmented == math.factorial(dummy) * gram_sum
            tests += 1
    return tests


def subdivision_checks(rng, repetitions=24):
    tests = 0
    dimension = 4
    for _ in range(repetitions):
        original = []
        subdivided = []
        count = 3
        new_dimension = dimension + 2 * count
        e = [[int(i == j) for i in range(new_dimension)]
             for j in range(new_dimension)]
        middle_product = 1
        for line in range(count):
            first = [rng.randrange(-2, 3) for _ in range(dimension)]
            second = [rng.randrange(-2, 3) for _ in range(dimension)]
            left, middle, right = [rng.randrange(1, 4) for _ in range(3)]
            original.append((first, second, Fraction(left * right, middle)))
            first = first + [0] * (2 * count)
            second = second + [0] * (2 * count)
            s, t = dimension + 2 * line, dimension + 2 * line + 1
            subdivided.extend([(first, e[s], left), (e[s], e[t], middle),
                               (e[t], second, right)])
            middle_product *= middle
        old = paired_basis_partition(original, dimension)
        new = paired_basis_partition(subdivided, new_dimension)
        assert new == middle_product * old
        tests += 1
    return tests


def root_bounds(x, digits=24):
    scale = 10 ** digits
    lower = math.isqrt(x * scale * scale)
    return lower, lower + int(lower * lower != x * scale * scale)


@lru_cache(None)
def roots_leq(lhs, rhs):
    """Certify sqrt(lhs)<=sum(sqrt(rhs)) with integer arithmetic."""
    if not lhs or lhs <= sum(rhs):
        return True
    _, left_hi = root_bounds(lhs)
    right_lo = sum(root_bounds(v)[0] for v in rhs)
    if left_hi <= right_lo:
        return True
    left_lo, _ = root_bounds(lhs)
    right_hi = sum(root_bounds(v)[1] for v in rhs)
    if left_lo > right_hi:
        return False
    # Equality of a positive sum to one radical requires one square class.
    total = Fraction(0)
    rational = True
    for v in rhs:
        if not v:
            continue
        g = math.gcd(v, lhs)
        num, den = v // g, lhs // g
        p, q = math.isqrt(num), math.isqrt(den)
        if p * p != num or q * q != den:
            rational = False
            break
        total += Fraction(p, q)
    if rational:
        return total >= 1
    for digits in (48, 96, 192):
        _, left_hi = root_bounds(lhs, digits)
        right_lo = sum(root_bounds(v, digits)[0] for v in rhs)
        if left_hi <= right_lo:
            return True
        left_lo, _ = root_bounds(lhs, digits)
        right_hi = sum(root_bounds(v, digits)[1] for v in rhs)
        if left_lo > right_hi:
            return False
    raise ArithmeticError('Radical comparison remains undecided')


def sqrt_exchange(F, f):
    n = len(F)
    tested = 0
    worst = (0.0, None)
    certified_failure = None
    for S in range(1 << n):
        if S.bit_count() not in (2, 4) or not f[S]:
            continue
        for T in range(1 << n):
            if T.bit_count() != 2 or not f[T]:
                continue
            diff = S ^ T
            for a in range(n):
                if not diff >> a & 1:
                    continue
                lhs = f[S] * f[T]
                rhs = [f[S ^ (1 << a) ^ (1 << j)] *
                       f[T ^ (1 << a) ^ (1 << j)]
                       for j in range(n) if j != a and diff >> j & 1]
                val = math.sqrt(lhs) / sum(map(math.sqrt, rhs))
                tested += 1
                if val > worst[0]:
                    worst = (val, (S, T, a, lhs, rhs))
                if not roots_leq(lhs, tuple(sorted(rhs))):
                    lo, _ = root_bounds(lhs)
                    hi = sum(root_bounds(v)[1] for v in rhs)
                    if lo > hi:
                        certified_failure = {
                            'F': F, 'S': S, 'T': T, 'a': a,
                            'left_product': lhs, 'right_products': rhs,
                            'certified_left_sqrt_lower_scaled': lo,
                            'certified_right_sqrt_sum_upper_scaled': hi,
                            'scale': 10 ** 24,
                            'ratio_float_diagnostic': val,
                        }
                        return tested, worst, certified_failure
    return tested, worst, certified_failure


def four_holes(f, n):
    tested = 0
    worst_ratio = (0.0, None)
    for U in combinations(range(n), 4):
        a, b, c, d = U
        mask = sum(1 << i for i in U)
        lhs = f[0] * f[mask]
        rhs = [f[(1 << a) | (1 << b)] * f[(1 << c) | (1 << d)],
               f[(1 << a) | (1 << c)] * f[(1 << b) | (1 << d)],
               f[(1 << a) | (1 << d)] * f[(1 << b) | (1 << c)]]
        assert lhs <= 3 * sum(rhs), (lhs, rhs)
        assert roots_leq(lhs, tuple(sorted(rhs))), (lhs, rhs)
        if sum(rhs):
            if lhs / sum(rhs) > worst_ratio[0]:
                worst_ratio = (lhs / sum(rhs), (U, lhs, rhs))
        tested += 1
    return tested, worst_ratio


def signed_coeff(f, n):
    return {u: ((-1) ** ((n - u.bit_count()) // 2)) * v
            for u, v in enumerate(f) if v}


def auxiliary(f, i, j, w):
    bits = (1 << i) | (1 << j)
    return [v + (w * f[u | bits] if not u & bits else 0)
            for u, v in enumerate(f)]


def signed_eval(q, x, deleted=0):
    out = 0
    for u, c in q.items():
        if u & deleted != deleted:
            continue
        v = c
        for j, z in enumerate(x):
            if u >> j & 1 and not deleted >> j & 1:
                v *= z
        out += v
    return out


def rayleigh_checks(f, n, rng, reps=3):
    q = signed_coeff(f, n)
    tested = 0
    for _ in range(reps):
        x = [rng.randrange(-3, 4) for _ in range(n)]
        value = signed_eval(q, x)
        for a, b in combinations(range(n), 2):
            A, B = 1 << a, 1 << b
            delta = (signed_eval(q, x, A) * signed_eval(q, x, B) -
                     value * signed_eval(q, x, A | B))
            assert delta >= 0, (n, a, b, x, f, delta)
            tested += 1
    return tested


def run():
    rng = random.Random(291173)
    t0 = time.time()
    named = [[0, 0, 1, 1], [0, 0, 1, -1], [0, 0, 0, 0], [0, 0, 0, 0]]
    fn = partitions(named)
    assert fn[0] == 4 and fn[-1] == 1
    assert sum(fn[u] * fn[15 ^ u] for u in (3, 5, 9)) == 2
    factor_two = [[0, 1, -1, -2, 0, 0], [0, 0, 0, 0, 0, 0],
                  [0, -1, 0, 2, 0, 0], [-1, 2, 0, 0, 2, 0],
                  [0, 0, 0, -1, 0, 0], [0, 2, 1, 0, -2, 0]]
    ff = partitions(factor_two)
    a, b, c, d = 1, 2, 4, 5
    U = (1 << a) | (1 << b) | (1 << c) | (1 << d)
    products = [ff[(1 << a) | (1 << b)] * ff[(1 << c) | (1 << d)],
                ff[(1 << a) | (1 << c)] * ff[(1 << b) | (1 << d)],
                ff[(1 << a) | (1 << d)] * ff[(1 << b) | (1 << c)]]
    assert ff[0] * ff[U] == 565 and products == [100, 25, 100]
    scaled = [[0, 1, 16, 0], [1, 0, 0, 16],
              [16, 0, 0, 16], [0, 16, 16, 0]]
    cut = lambda I: det_int([[scaled[i][j] for j in range(4) if j not in I]
                            for i in I])
    before = cut((0, 1)) ** 2 * cut((2, 3)) ** 2
    after = cut((0, 2)) ** 2 * cut((1, 3)) ** 2
    assert Fraction(after, before) == Fraction(1, 16 ** 4)
    stats = {'exact_factor_one_counterexample': {'F': named, 'f': fn},
             'exact_factor_two_counterexample': {
                 'F': factor_two, 'holes': [1, 2, 4, 5],
                 'left_product': 565, 'pairing_products': products},
             'exact_microscopic_union_ratio': {
                 'scaled_F': scaled, 'delta': '1/16',
                 'before_weight_product': before, 'after_weight_product': after,
                 'ratio': '1/65536'}}
    cases = four = exchange = rayleigh = aug_rayleigh = 0
    worst_four = (0.0, None)
    worst_exchange = (0.0, None)
    failed = None
    for n, count in ((4, 128), (6, 768), (8, 64)):
        for trial in range(count):
            F = [[rng.randrange(-2, 3) if rng.random() < (0.3 if trial % 2 else 0.8)
                  else 0 for _ in range(n)] for _ in range(n)]
            for i in range(n):
                F[i][i] = 0
            f = partitions(F)
            cases += 1
            c, w = four_holes(f, n)
            four += c
            if w[0] > worst_four[0]:
                worst_four = (w[0], {'n': n, 'F': F, 'details': w[1]})
            rayleigh += rayleigh_checks(f, n, rng)
            fa = f
            for _ in range(3):
                i, j = rng.sample(range(n), 2)
                fa = auxiliary(fa, i, j, rng.randrange(1, 4))
            aug_rayleigh += rayleigh_checks(fa, n, rng)
            c, w, failure = sqrt_exchange(F, f)
            exchange += c
            if w[0] > worst_exchange[0]:
                worst_exchange = (w[0], {'n': n, 'F': F, 'details': w[1]})
            if failure:
                failed = failure
                break
        if failed:
            break
    stats.update({'matrix_cases': cases,
                  'four_hole_exact_tests': four,
                  'maximum_four_hole_ratio': worst_four,
                  'bounded_hole_sqrt_exchange_tests': exchange,
                  'maximum_sqrt_exchange_ratio': worst_exchange,
                  'sqrt_exchange_certified_failure': failed,
                  'integer_Rayleigh_tests': rayleigh,
                  'auxiliary_integer_Rayleigh_tests': aug_rayleigh,
                  'seconds': round(time.time() - t0, 3),
                  'scope': 'Exact finite partition enumeration and integer Rayleigh checks; radical comparisons certified by integer-sqrt intervals. No counting or chain algorithm.'})
    # Independent seeds keep the original signed-hole diagnostic corpus fixed.
    identity_rng = random.Random(987311)
    stats['fixed_k_Gram_minor_dummy_identity_tests'] = fixed_k_checks(identity_rng)
    stats['arbitrary_vector_pair_subdivision_identity_tests'] = subdivision_checks(identity_rng)
    stats['seconds'] = round(time.time() - t0, 3)
    return stats


if __name__ == '__main__':
    result = run()
    print(json.dumps(result, indent=2))
    with open('work/cycle4/parity_hole_checks.json', 'w') as out:
        json.dump(result, out, indent=2)
        out.write('\n')
