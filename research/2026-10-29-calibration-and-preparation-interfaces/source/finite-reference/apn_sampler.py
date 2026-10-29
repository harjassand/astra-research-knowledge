#!/usr/bin/env python3
"""Exact finite-field diagnostics and differential pair sampler; stdlib only.

The prefix evaluator is supplied, not learned by this file. APN and quadratic
permutation promises are mathematical preconditions of the generic sampler.
The concrete Gold examples justify those promises directly.
"""
from __future__ import annotations
import json
import math
import random
import time
from pathlib import Path


def pmod(a, b):
    while a and a.bit_length() >= b.bit_length():
        a ^= b << (a.bit_length()-b.bit_length())
    return a


def pgcd(a, b):
    while b:
        a, b = b, pmod(a, b)
    return a


def mul(a, b, modulus):
    n = modulus.bit_length()-1
    c = 0
    while b:
        if b & 1:
            c ^= a
        b >>= 1
        a <<= 1
        if a >> n:
            a ^= modulus
    return c


def irreducible(modulus):
    n = modulus.bit_length()-1
    if n < 1 or not modulus & 1:
        return False
    x, power = 2, 2
    for k in range(1, n+1):
        power = mul(power, power, modulus)
        if k <= n//2 and pgcd(power ^ x, modulus) != 1:
            return False
    return power == x


def acquire_modulus(n):
    attempts = 0
    for low in range(1, 1 << n, 2):
        attempts += 1
        p = (1 << n) | low
        if irreducible(p):
            return p, attempts
    raise RuntimeError('No irreducible polynomial found')


def affine_solution(columns, constant, n, t):
    """Return a particular solution and independent kernel basis, or None."""
    rows = []
    for b in range(t):
        mask = sum(((col >> b) & 1) << j for j, col in enumerate(columns))
        rows.append(mask | (((constant >> b) & 1) << n))
    pivots = []
    rank = 0
    for j in range(n):
        at = next((i for i in range(rank, t) if (rows[i] >> j) & 1), None)
        if at is None:
            continue
        rows[rank], rows[at] = rows[at], rows[rank]
        for i in range(t):
            if i != rank and (rows[i] >> j) & 1:
                rows[i] ^= rows[rank]
        pivots.append(j)
        rank += 1
    maskn = (1 << n)-1
    if any((row & maskn) == 0 and (row >> n) & 1 for row in rows):
        return None
    particular = sum(((rows[i] >> n) & 1) << j for i, j in enumerate(pivots))
    free = [j for j in range(n) if j not in pivots]
    basis = []
    for f in free:
        v = 1 << f
        for i, j in enumerate(pivots):
            if (rows[i] >> f) & 1:
                v ^= 1 << j
        basis.append(v)
    return particular, basis, rank


def slice_for_displacement(prefix, n, t, u):
    zero, at_u = prefix(0), prefix(u)
    constant = zero ^ at_u
    columns = [prefix(u ^ (1 << j)) ^ prefix(1 << j) ^ constant for j in range(n)]
    return affine_solution(columns, constant, n, t)


def sample_pair(prefix, n, t, rng):
    trials = 0
    while True:
        trials += 1
        u = rng.randrange(1, 1 << n)
        solution = slice_for_displacement(prefix, n, t, u)
        if solution is None:
            continue
        x, basis, _ = solution
        coins = rng.getrandbits(len(basis))
        for i, v in enumerate(basis):
            if (coins >> i) & 1:
                x ^= v
        return x, x ^ u, trials


def verify_candidate(candidate, comparator, n, delta, rng):
    """One-sided test. Does not acquire or verify the candidate's APN promise."""
    per_prefix = math.ceil(32*math.log(1/delta))
    comparisons = trials = 0
    for t in range(n):
        prefix = lambda x, t=t: candidate(x) >> (n-t)
        for _ in range(per_prefix):
            x, y, count = sample_pair(prefix, n, t, rng)
            trials += count
            comparisons += 1
            if bool(comparator(x, y)) != (candidate(x) < candidate(y)):
                return dict(accepted=False, comparisons=comparisons, trials=trials, rejection_prefix=t)
    return dict(accepted=True, comparisons=comparisons, trials=trials)


def run():
    start = time.perf_counter()
    rng = random.Random(2026102902)
    small = []
    checked_displacements = checked_pairs = 0
    for n in (3, 5, 7):
        mod, attempts = acquire_modulus(n)
        cube = lambda x, mod=mod: mul(mul(x, x, mod), x, mod)
        values = [cube(x) for x in range(1 << n)]
        assert len(set(values)) == 1 << n
        counts = []
        for t in range(n):
            prefix = lambda x, t=t, n=n: values[x] >> (n-t)
            valid = 0
            for u in range(1, 1 << n):
                checked_displacements += 1
                sol = slice_for_displacement(prefix, n, t, u)
                if sol is None:
                    assert all(prefix(x) != prefix(x ^ u) for x in range(1 << n))
                    continue
                valid += 1
                x0, basis, rank = sol
                assert rank == t and len(basis) == n-t
                xs = set()
                for b in range(1 << len(basis)):
                    x = x0
                    for j, v in enumerate(basis):
                        if (b >> j) & 1:
                            x ^= v
                    assert x not in xs and prefix(x) == prefix(x ^ u)
                    xs.add(x)
                    checked_pairs += 1
                assert len(xs) == 1 << (n-t)
            assert valid == (1 << n)-(1 << t)
            counts.append(valid)
        # A different explicit quadratic permutation: x^5 over odd degree.
        fifth = lambda x, mod=mod: mul(mul(mul(x,x,mod),mul(x,x,mod),mod),x,mod)
        exact_accept = verify_candidate(cube, lambda x,y: cube(x)<cube(y), n, 0.1, rng)
        false_reject = verify_candidate(cube, lambda x,y: fifth(x)<fifth(y), n, 0.1, rng)
        assert exact_accept['accepted'] and not false_reject['accepted']
        small.append(dict(n=n, modulus=mod, acquisition_candidates=attempts,
                          valid_displacements_by_prefix=counts,
                          true_candidate=exact_accept, false_candidate=false_reject))
    n = 31
    mod, attempts = acquire_modulus(n)
    cube = lambda x: mul(mul(x,x,mod),x,mod)
    samples = trials = 0
    for t in (0, 1, 15, 29, 30):
        prefix = lambda x, t=t: cube(x) >> (n-t)
        for _ in range(64):
            x, y, count = sample_pair(prefix,n,t,rng)
            assert x != y and prefix(x) == prefix(y)
            samples += 1
            trials += count
    return dict(status='all exact finite diagnostics passed; no general learner implemented',
                seed=2026102902, checked_displacements=checked_displacements,
                enumerated_same_prefix_pairs=checked_pairs, small_cases=small,
                large_case=dict(n=n, population=1<<n, modulus=mod,
                                acquisition_candidates=attempts, sampled_pairs=samples,
                                displacement_trials=trials, enumerated_population=False),
                elapsed_seconds=time.perf_counter()-start)


if __name__ == '__main__':
    data = run()
    Path(__file__).with_name('apn_sampler_results.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps(data,indent=2))
