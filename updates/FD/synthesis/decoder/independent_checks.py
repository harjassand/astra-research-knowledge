"""Independent bounded exact checks; no source implementation is imported.

Tests support implementations and narrow finite lemmas, not universal proof,
novelty, entropy, or a physical service. All writes stay in this audit folder.
"""
from __future__ import annotations

import itertools
import json
import math
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent


def parity(x):
    return x.bit_count() & 1


def xor_sum(basis, mask):
    out = 0
    for i, v in enumerate(basis):
        if mask >> i & 1:
            out ^= v
    return out


def masks(k, d):
    return [sum(1 << i for i in s)
            for j in range(min(k, d) + 1)
            for s in itertools.combinations(range(k), j)]


def poly(terms, point):
    return sum((point & term) == term for term in terms) & 1


def interpolation(values):
    terms = []
    for s in sorted(values, key=lambda v: (v.bit_count(), v)):
        if values[s] ^ poly(terms, s):
            terms.append(s)
    return terms


def coordinates(basis, x):
    pivots = {}
    for i, v in enumerate(basis):
        c = 1 << i
        while v:
            j = v.bit_length() - 1
            if j in pivots:
                old, oldc = pivots[j]
                v ^= old
                c ^= oldc
            else:
                pivots[j] = v, c
                break
        assert v
    out = 0
    while x:
        j = x.bit_length() - 1
        v, c = pivots[j]
        x ^= v
        out ^= c
    return out


class Teacher:
    def __init__(self, n, d, seed):
        rng = random.Random(seed)
        self.n, self.calls = n, 0
        self.rows = [1 << i for i in range(n)]
        for _ in range(10 * n):
            i, j = rng.sample(range(n), 2)
            self.rows[i] ^= self.rows[j]
        rng.shuffle(self.rows)
        self.offset = rng.getrandbits(n)
        self.functions = [[s for s in masks(i, d) if rng.getrandbits(1)]
                          for i in range(n)]

    def rank(self, x):
        u = sum(parity(row & x) << i for i, row in enumerate(self.rows)) ^ self.offset
        out = 0
        for i, terms in enumerate(self.functions):
            out = 2 * out + ((u >> i & 1) ^ poly(terms, u))
        return out

    def query(self, x, y):
        assert x != y
        self.calls += 1
        return int(self.rank(x) < self.rank(y))


def learn(n, d, query, seed, beta=.01):
    rng = random.Random(seed)
    P = n * (n - 1) // 2
    T = math.ceil(math.log2(P / beta))
    basis, functions = [], []
    S = [1 << i for i in range(n)]
    contests = interpolation_calls = response_calls = matching_attempts = 0
    for k in range(n):
        w = S[0]
        for v in S[1:]:
            for _ in range(T):
                x = rng.getrandbits(n)
                a, b = 1 ^ query(x, x ^ v), 1 ^ query(x, x ^ w)
                matching_attempts += 1
                if a == b:
                    if query(x ^ v, x ^ w) == a:
                        w = v
                    contests += 1
                    break
            else:
                return None
        values = {a: 1 ^ query(xor_sum(basis, a), xor_sum(basis, a) ^ w)
                  for a in masks(k, d)}
        interpolation_calls += len(values)
        functions.append(interpolation(values))
        w_index = S.index(w)
        responses = [1 if i == w_index else values[0] ^ (1 ^ query(v, v ^ w))
                     for i, v in enumerate(S)]
        response_calls += len(S) - 1
        S = [v ^ (w if responses[i] else 0)
             for i, v in enumerate(S) if i != w_index]
        basis.append(w)
    D = sum(math.comb(n, j + 1) for j in range(min(d, n - 1) + 1))
    assert interpolation_calls == D and response_calls == contests == P
    return basis, functions, dict(D=D, P=P, T=T,
                                 interpolation_calls=interpolation_calls,
                                 response_calls=response_calls,
                                 priority_calls=contests,
                                 matching_attempts=matching_attempts,
                                 maximum_comparisons=D + (2 * T + 2) * P)


def evaluate(model, x):
    basis, functions, _ = model
    t = coordinates(basis, x)
    y = 0
    for i, terms in enumerate(functions):
        y = 2 * y + ((t >> i & 1) ^ poly(terms, t & ((1 << i) - 1)))
    return y


def inverse_prefix(model, k, target, free):
    basis, functions, _ = model
    t = free << k
    for i in range(k):
        t |= ((target >> (k - i - 1) & 1)
              ^ poly(functions[i], t & ((1 << i) - 1))) << i
    return xor_sum(basis, t)


def compact_cases():
    cases = []
    for n in range(2, 9):
        for d in range(1, min(4, n) + 1):
            seed = 1026014 + 101 * n + 7 * d
            teacher = Teacher(n, d, seed)
            model = learn(n, d, teacher.query, seed + 10000)
            assert model is not None
            receipt = model[2]
            assert teacher.calls <= receipt['maximum_comparisons']
            for x in range(1 << n):
                rank = teacher.rank(x)
                assert evaluate(model, x) == rank
                assert inverse_prefix(model, n, rank, 0) == x
            fiber_points = 0
            for k in range(n + 1):
                for target in range(1 << k):
                    points = [inverse_prefix(model, k, target, free)
                              for free in range(1 << (n - k))]
                    assert len(set(points)) == len(points)
                    assert all(teacher.rank(x) >> (n - k) == target for x in points)
                    fiber_points += len(points)
            cases.append(dict(n=n, d=d, seed=seed, comparisons=teacher.calls,
                              rank_and_inverse_points=1 << n,
                              exhaustive_prefix_seed_points=fiber_points,
                              exact=True, **receipt))
    return cases


def coefficient_majority_all_centers(n, d, truth, bad):
    """Separate implementation of exact-population coefficient votes."""
    recovered = []
    for S in sorted(masks(n, d), key=lambda s: -s.bit_count()):
        votes = 0
        for x in range(1 << n):
            vote = 0
            a = S
            while True:
                z = x ^ a
                vote ^= poly(truth, z) ^ int(z in bad)
                if a == 0:
                    break
                a = (a - 1) & S
            for U in recovered:
                if U != S and U & S == S:
                    vote ^= int(x & (U ^ S) == U ^ S)
            votes += vote
        assert votes != 1 << (n - 1)
        if votes > 1 << (n - 1):
            recovered.append(S)
    return set(recovered)


def shifted_ball_population_audit():
    n, d = 4, 2
    mon = masks(n, d)
    count = 0
    for coeff in range(1 << len(mon)):
        truth = [term for j, term in enumerate(mon) if coeff >> j & 1]
        for b in range(1 << n):
            assert coefficient_majority_all_centers(n, d, truth, {b}) == set(truth)
            count += 1
    return dict(n=n, d=d, cases=count, error_density='1/16',
                all_quadratic_coefficients=True, all_single_bad_positions=True,
                exact_population_majorities=True,
                scope='All uniform centers, not a finite-sample confidence test')


def directed_rank_threshold_audit():
    # All arbitrary directed incident answers for one bad item among N=8.
    # Each x gets its own independently selected incident answer; reversal
    # consistency is deliberately absent. The lemma does not assume epsilon<1/16.
    N = 8
    count = max_errors = 0
    for bad in range(N):
        others = [i for i in range(N) if i != bad]
        for answers in range(1 << (2 * (N - 1))):
            incoming = {y: answers >> j & 1 for j, y in enumerate(others)}
            outgoing = {x: answers >> (N - 1 + j) & 1 for j, x in enumerate(others)}
            errors = 0
            for x in range(N):
                pred = 0
                for y in range(N):
                    if x == y:
                        continue
                    if x == bad:
                        pred += incoming[y]
                    elif y == bad:
                        pred += outgoing[x]
                    else:
                        pred += int(y < x)
                errors += int(pred >= N // 2) != int(x >= N // 2)
            assert errors <= 2
            max_errors = max(max_errors, errors)
            count += 1
    return dict(fiber_size=N, bad_count=1, cases=count,
                arbitrary_directed_incident_answers=True,
                maximum_mislabels=max_errors, proved_bound_fixture=2)


def main():
    result = dict(scope='Internal independent finite audit only',
                  compact_cases=compact_cases(),
                  shifted_ball_population=shifted_ball_population_audit(),
                  directed_rank_threshold=directed_rank_threshold_audit())
    (HERE / 'independent_results.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(dict(compact_cases=len(result['compact_cases']),
                          shifted_ball_population=result['shifted_ball_population'],
                          directed_rank_threshold=result['directed_rank_threshold']), indent=2))


if __name__ == '__main__':
    main()
