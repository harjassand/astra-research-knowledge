"""Independent finite exact comparators for low_sector_sampler.py.

Small Pfaffian recursion and Leibniz determinants occur ONLY in comparators.
All outputs are owned by c01_s03. Seeded draws corroborate implementation;
they do not prove the universal error or bit-complexity theorems.
"""
import itertools
import json
import math
import random
import time
from fractions import Fraction
from pathlib import Path
from low_sector_sampler import LowSector, ZERO, ONE, add, mul, scale, conj, pfaffian_norm_coefficient

assertions = 0

def check(test):
    global assertions
    assertions += 1
    assert test


def norm(z):
    return z[0]*z[0] + z[1]*z[1]


def det(a):
    value = ZERO
    for p in itertools.permutations(range(len(a))):
        term = ONE
        for i, j in enumerate(p):
            term = mul(term, a[i][j])
        negative = sum(p[i] > p[j] for i in range(len(p)) for j in range(i+1, len(p))) % 2
        value = add(value, scale(term, -1 if negative else 1))
    return value


def pf(a):
    if not a:
        return ONE
    total = ZERO
    for j in range(1, len(a)):
        others = [i for i in range(len(a)) if i != 0 and i != j]
        tail = [[a[i][h] for h in others] for i in others]
        total = add(total, scale(mul(a[0][j], pf(tail)), (-1)**(j+1)))
    return total


def direct_mass(engine, k, up=(), down=(), empty=()):
    up, down, empty = set(up), set(down), set(empty)
    total = 0
    for rows in itertools.combinations(range(engine.n), k):
        i = set(rows)
        if not up <= i or i & (down | empty):
            continue
        for cols in itertools.combinations(range(engine.n), k):
            j = set(cols)
            if i & j or not down <= j or j & (up | empty):
                continue
            total += norm(det([[engine.g[x][y] for y in cols] for x in rows]))
    return total


def draw_by_pf_projection(engine, k, signs, up=(), down=(), empty=()):
    up, down, empty = set(up), set(down), set(empty)
    if len(up) > k or len(down) > k or 2*k > engine.n-len(empty):
        return 0
    total = 0
    for retained in itertools.combinations(sorted(set(range(engine.n))-empty), 2*k):
        if not up | down <= set(retained):
            continue
        projected = ZERO
        for word in itertools.product((-1, 1), repeat=len(up)):
            activity = list(signs)
            for i in down | empty:
                activity[i] = 0
            character = 1
            for i, s in zip(sorted(up), word):
                activity[i] = s
                character *= s
            skew = [[add(scale(engine.g[i][j], activity[i]),
                         scale(engine.g[j][i], -activity[j]))
                     for j in retained] for i in retained]
            projected = add(projected, scale(pf(skew), character))
        divisor = 1 << len(up)
        check(projected[0] % divisor == 0 and projected[1] % divisor == 0)
        projected = (projected[0]//divisor, projected[1]//divisor)
        total += norm(projected)
    return total


def exhaustive_case(engine, k, up=(), down=(), empty=(), name=''):
    target = direct_mass(engine, k, up, down, empty)
    a, b = len(up), len(down)
    if a > k or b > k or 2*k > engine.n-len(empty):
        bound = 0
    else:
        bound = math.comb(2*k-a-b, k-a)
    free = sorted(set(range(engine.n))-set(up)-set(down)-set(empty))
    values = []
    for word in itertools.product((-1, 1), repeat=len(free)):
        signs = [1]*engine.n
        for i, s in zip(free, word):
            signs[i] = s
        value = engine.prefix_draw_integer(k, signs, up, down, empty)
        comparator = draw_by_pf_projection(engine, k, signs, up, down, empty)
        check(value == comparator)
        check(0 <= value <= bound*target)
        values.append(value)
    mean = Fraction(sum(values), len(values))
    second = Fraction(sum(x*x for x in values), len(values))
    check(mean == target)
    check(second <= bound*target*target)
    if bound:
        check((1 << b)*bound <= math.comb(2*k, k))
    return {'name': name, 'n': engine.n, 'k': k, 'up': list(up), 'down': list(down),
            'empty': list(empty), 'sign_words': len(values), 'prefix_mass': str(Fraction(target, engine.denominator**(2*k))),
            'C': bound, 'relative_second_moment': str(second/(target*target)) if target else 'ZERO'}


def main():
    started = time.monotonic()
    rng = random.Random(770031)
    cases = []
    matrices = {}
    for n in range(2, 7):
        f = [[(rng.randrange(-3, 4), rng.randrange(-3, 4)) for _ in range(n)] for _ in range(n)]
        engine = LowSector(f)
        matrices[n] = f
        for k in range(n//2+1):
            cases.append(exhaustive_case(engine, k, name='dense_complex_root'))
        cases.append(exhaustive_case(engine, n//2, up=(0,), down=(n-1,), name='up_down_noncontiguous'))
        cases.append(exhaustive_case(engine, 1, down=(0,), empty=(1,), name='down_empty'))
        if n >= 4:
            cases.append(exhaustive_case(engine, 2, up=(1, 3), name='two_forced_up'))
    # Exhaust every physical scan prefix on one generic four-site matrix.
    engine = LowSector(matrices[4])
    for length in range(1, 5):
        for labels in itertools.product((0, 1, -1), repeat=length):
            up = [i for i, label in enumerate(labels) if label == 1]
            down = [i for i, label in enumerate(labels) if label == -1]
            empty = [i for i, label in enumerate(labels) if label == 0]
            cases.append(exhaustive_case(engine, 2, up, down, empty, name='all_four_site_prefixes'))
    # Independent block-Pfaffian verification of the square-root identity.
    for n in range(1, 6):
        raw = [[(rng.randrange(-2, 3), rng.randrange(-2, 3)) for _ in range(n)] for _ in range(n)]
        skew = [[add(raw[i][j], scale(raw[j][i], -1)) for j in range(n)] for i in range(n)]
        coefficients = [pfaffian_norm_coefficient(skew, h) for h in range(n//2+1)]
        for t in (-2, 0, 1, 3):
            block = [[ZERO for _ in range(2*n)] for _ in range(2*n)]
            for i in range(n):
                for j in range(n):
                    block[i][j] = scale(skew[i][j], t)
                    block[n+i][n+j] = scale(conj(skew[i][j]), -1)
                block[i][n+i], block[n+i][i] = ONE, (-1, 0)
            value = scale(pf(block), (-1)**(n*(n-1)//2))
            check(value == (sum(c*t**h for h, c in enumerate(coefficients)), 0))
    # Exact rational acquisition and cancellation-scale retention.
    rational = [[(Fraction(x, 6), Fraction(y, 10)) for x, y in row] for row in matrices[4]]
    engine = LowSector(rational)
    check(engine.denominator == 30)
    cases.append(exhaustive_case(engine, 2, name='rational_complex_D30'))
    cases.append(exhaustive_case(engine, 2, up=(0,), down=(2,), name='rational_prefix'))
    for bits in (8, 64, 256):
        d = Fraction(1, 1 << bits)
        f = [[0, 1+d, 1, 1], [1+d, 0, 1, 2], [1, 1, 0, 1], [1, 2, 1, 0]]
        engine = LowSector(f)
        cases.append(exhaustive_case(engine, 2, up=(0, 2), down=(1, 3), name='tiny_mass_L'+str(bits)))
        check(direct_mass(engine, 2, (0, 2), (1, 3)) == engine.denominator**2)
        # Weight of this fully forced word is delta^2, never rounded to zero.
        check(engine.estimate(2, Fraction(1, 2), Fraction(1, 4), up=(0, 2), down=(1, 3)) == d*d)
    for k in range(1, 5):
        n = 2*k
        f = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(0, n, 2):
            f[i][i+1] = f[i+1][i] = 1
        record = exhaustive_case(LowSector(f), k, name='independent_swap_blocks')
        check(record['relative_second_moment'] == str(1 << k))
        cases.append(record)
    # Universal combinatorial prefactor inequality, not merely fixed fixtures.
    for k in range(31):
        for a in range(k+1):
            for b in range(k+1):
                check((1 << b)*math.comb(2*k-a-b, k-a) <= math.comb(2*k, k))
    # Complete randomized, non-enumerating calls with the full advertised caps.
    stochastic = []
    engine = LowSector(rational)
    target = Fraction(direct_mass(engine, 2), engine.denominator**4)
    for seed in range(12):
        estimate = engine.estimate(2, Fraction(1, 3), Fraction(1, 16), rng=random.Random(seed),
                                   enumerate_if_cheaper=False)
        check(abs(estimate-target) <= target/3)
        stochastic.append({'seed': seed, 'estimate': str(estimate), 'target': str(target)})
    zero = LowSector([[0 if i == j else 1 for j in range(4)] for i in range(4)])
    check(zero.estimate(2, Fraction(1, 3), Fraction(1, 16), rng=rng, enumerate_if_cheaper=False) == 0)
    check(zero.born_sample(2, Fraction(1, 2), rng=rng, enumerate_if_cheaper=False)['status'] == 'FAIL')
    sampler_records = []
    for n, k, runs in ((3, 1, 32), (4, 2, 16), (5, 2, 4)):
        engine = LowSector(matrices[n])
        for seed in range(runs):
            sample = engine.born_sample(k, Fraction(3, 4), rng=random.Random(seed+1000),
                                        enumerate_if_cheaper=False)
            check(sample['status'] == 'OK')
            i, j = sample['I'], sample['J']
            check(len(i) == len(j) == k and not set(i) & set(j))
            check(norm(det([[engine.g[x][y] for y in j] for x in i])) > 0)
        sampler_records.append({'n': n, 'k': k, 'successful_runs': runs, 'stats': engine.stats})
    result = {'status': 'PASS', 'scope': 'Finite exact identities/moments/prefixes and full-cap seeded estimator/sampler calls; universal guarantees require the accompanying proof.',
              'assertions': assertions, 'exhaustive_cases': len(cases),
              'sign_words': sum(c['sign_words'] for c in cases), 'elapsed_seconds': time.monotonic()-started,
              'cases': cases, 'randomized_count_calls': stochastic, 'samplers': sampler_records}
    Path(__file__).with_name('low_sector_checks.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: v for k, v in result.items() if k not in ('cases', 'randomized_count_calls')}, indent=2))

if __name__ == '__main__':
    main()
