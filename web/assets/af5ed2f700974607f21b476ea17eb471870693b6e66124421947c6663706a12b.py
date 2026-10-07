"""Bounded, independent exact comparators for the low-k implementation."""
from lowk_bcs import *
from pathlib import Path
import json
import time


def leibniz(a):
    value = ZERO
    for p in itertools.permutations(range(len(a))):
        term = ONE
        for i, j in enumerate(p):
            term = term*a[i][j]
        sg = (-1)**sum(p[i] > p[j] for i in range(len(p)) for j in range(i+1, len(p)))
        value = value+sg*term
    return value


def law(f, k):
    n = len(f)
    out = {}
    for rows in itertools.combinations(range(n), k):
        for cols in itertools.combinations([j for j in range(n) if j not in rows], k):
            w = leibniz([[f[i][j] for j in cols] for i in rows]).abs2()
            if w:
                out[rows, cols] = w
    return out


def pf(a):
    if not a:
        return ONE
    z = ZERO
    for j in range(1, len(a)):
        inds = [i for i in range(len(a)) if i not in (0, j)]
        z = z+(-1)**(j+1)*a[0][j]*pf([[a[i][h] for h in inds] for i in inds])
    return z


def direct_skew_norm(v, signs, r):
    n = len(v)
    a = [[sum((s*(v[i][2*h]*v[j][2*h+1]-v[i][2*h+1]*v[j][2*h])
                    for h, s in enumerate(signs)), ZERO) for j in range(n)] for i in range(n)]
    return sum(pf([[a[i][j] for j in inds] for i in inds]).abs2()
               for inds in itertools.combinations(range(n), 2*r))


def exact_grid_law(counter, grid):
    n, k = counter.n, counter.k
    out = {}

    def pickweights(w0, w1):
        assert w0+w1 > 0
        p = grid*w1/(w0+w1)
        p = Q(p.numerator//p.denominator, grid)
        return 1-p, p

    def cols(rows, s, b, i, prob):
        labels = [j for j in range(n) if j not in rows]
        if i == len(labels):
            if prob:
                out[tuple(sorted(rows)), tuple(sorted(s))] = prob
            return
        j = labels[i]
        w0 = counter.column_mass(rows, s, b | {j})
        w1 = counter.column_mass(rows, s | {j}, b)
        p0, p1 = pickweights(w0, w1)
        if p0:
            cols(rows, s, b | {j}, i+1, prob*p0)
        if p1:
            cols(rows, s | {j}, b, i+1, prob*p1)

    def rows(a, b, i, prob):
        if i == n:
            cols(a, set(), set(), 0, prob)
            return
        w0 = counter.estimate(a, b | {i}, mode='enumerate')[0]
        w1 = counter.estimate(a | {i}, b, mode='enumerate')[0]
        p0, p1 = pickweights(w0, w1)
        if p0:
            rows(a, b | {i}, i+1, prob*p0)
        if p1:
            rows(a | {i}, b, i+1, prob*p1)

    rows(set(), set(), 0, Q(1))
    return out


def main():
    start = time.monotonic()
    rng = random.Random(3030310)
    dense = [[C(rng.randrange(-2, 3), Q(rng.randrange(-2, 3), 3)) for _ in range(4)] for _ in range(4)]
    swap = [[ZERO for _ in range(6)] for _ in range(6)]
    for i in (0, 2, 4):
        swap[i][i+1] = swap[i+1][i] = ONE
    tiny = [[C(int(i != j)) for j in range(4)] for i in range(4)]
    delta = Q(1, 1 << 32)
    for j, x in enumerate((1+delta**2, 1+delta+2*delta**2, 1-delta+3*delta**2), 1):
        tiny[0][j] = tiny[j][0] = C(x)
    zero = [[C(int(i != j)) for j in range(4)] for i in range(4)]
    records, sign_words, prefix_checks, column_checks, samples = [], 0, 0, 0, 0
    for name, f, k in [('dense_complex', dense, 2), ('tiny_positive_symmetric', tiny, 2),
                       ('zero_rank_cancellation', zero, 2), ('swap_blocks', swap, 3)]:
        weights = law(f, k)
        z = sum(weights.values(), Q(0))
        counter = LowKCounter(f, k, exact_sign_cap=64)
        prefixes = [((), ()), ((0,), ()), ((0,), (1,)), ((), (1, 2))]
        if k >= 2:
            prefixes += [((0, 2), (1,))]
        for selected, excluded in prefixes:
            p = counter.prefix(selected, excluded)
            expect = sum((w for (rows, cols), w in weights.items()
                          if set(selected) <= set(rows) and not set(excluded) & set(rows)), Q(0))
            values = [p.sign_value(s) for s in itertools.product((-1, 1), repeat=len(p.free_sites))]
            sign_words += len(values)
            assert sum(values, Q(0))/len(values) == expect
            assert all(0 <= x <= p.moment_bound*expect for x in values)
            second = sum((x*x for x in values), Q(0))/len(values)
            assert second <= p.moment_bound*expect*expect
            if p.exact_mass is None:
                v = [[C(Q(a, 1), Q(b, 1)) for a, b in row] for row in p.integer_vectors]
                s = [1]*len(p.free_sites)
                assert p.sign_value(s) == p.factor*direct_skew_norm(v, s, p.remaining_pairs)
            prefix_checks += 1
        values = [counter.prefix().sign_value(s) for s in itertools.product((-1, 1), repeat=len(f))]
        rel_second = None if not z else sum((x*x for x in values), Q(0))/len(values)/z**2
        if name == 'swap_blocks':
            assert rel_second == 8
        if name == 'tiny_positive_symmetric':
            assert z == 12*delta**2*(1-delta+delta**2)
        for rows, _ in weights:
            labels = [j for j in range(len(f)) if j not in rows]
            constraints = [((), ()), ((labels[0],), ()), ((), (labels[-1],))]
            for selected, excluded in constraints:
                expect = sum((w for (i, j), w in weights.items() if i == rows and
                              set(selected) <= set(j) and not set(excluded) & set(j)), Q(0))
                assert counter.column_mass(rows, selected, excluded) == expect
                column_checks += 1
        if z:
            for _ in range(8):
                i, j, receipt = counter.sample(Q(1, 4), rng)
                assert receipt['status'] == 'OK_TV' and (i, j) in weights
                assert receipt['branch_random_bits'] <= receipt['branch_random_bits_upper_bound']
                samples += 1
        records.append({'name': name, 'n': len(f), 'k': k, 'exact_norm': str(z),
                        'relative_second_moment': str(rel_second), 'counter_stats': counter.stats})
    counter = LowKCounter(dense, 2, exact_sign_cap=32)
    gridlaw = exact_grid_law(counter, 128)
    weights = law(dense, 2)
    z = sum(weights.values(), Q(0))
    tv = sum(abs(gridlaw.get(x, 0)-weights.get(x, 0)/z) for x in set(gridlaw) | set(weights))/2
    assert sum(gridlaw.values()) == 1 and tv <= Q(2*len(dense), 128)
    randomized = []
    for seed in (3, 30, 303):
        counter = LowKCounter(dense, 2, exact_sign_cap=0)
        est, receipt = counter.estimate(eta=Q(1, 2), delta=Q(1, 4), rng=random.Random(seed), mode='random')
        randomized.append({'seed': seed, 'estimate': str(est), 'exact': str(z),
                           'observed_relative_error': str(abs(est/z-1)), 'receipt': receipt,
                           'stats': counter.stats})
    try:
        LowKCounter(dense, 2, exact_sign_cap=0, sign_budget=1).estimate(mode='random')
        raise AssertionError('budget cap failed')
    except BudgetExceeded:
        pass
    result = {'status': 'PASS', 'scope': 'finite exact identities and bounded randomized smoke evidence',
              'prefix_checks': prefix_checks, 'sign_words': sign_words, 'column_prefix_checks': column_checks,
              'end_to_end_samples': samples, 'exact_dyadic_law_TV': str(tv), 'dyadic_TV_bound': '1/16',
              'fixtures': records, 'randomized_count_smoke': randomized,
              'limits': 'No large-n full-accuracy Monte Carlo sampler benchmark or exact generic support optimizer ran',
              'elapsed_seconds': time.monotonic()-start}
    Path(__file__).with_name('checks_lowk.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: v for k, v in result.items() if k not in ('fixtures', 'randomized_count_smoke')}, indent=2))


if __name__ == '__main__':
    main()
