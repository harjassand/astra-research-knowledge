"""Acquire a GF(2) matrix multiplication scheme from the schoolbook task.

No fast scheme is an input. Local moves are the known flip-graph identity.
Every attempted move, including steps in failed walks, is charged in the ledger.
Python 3, standard library only.
"""
import argparse
import hashlib
import json
import random
import time
from pathlib import Path


def schoolbook(b=2):
    return [(1 << (i*b+k), 1 << (k*b+j), 1 << (i*b+j))
            for i in range(b) for j in range(b) for k in range(b)]


def tensor(scheme, d):
    """Independent coefficient expansion; not a random input test."""
    out = [0] * (d*d*d)
    for u, v, w in scheme:
        for i in range(d):
            for j in range(d):
                for k in range(d):
                    out[(i*d+j)*d+k] ^= ((u >> i) & (v >> j) & (w >> k) & 1)
    return out


def verify(scheme, b=2):
    d = b*b
    if any(len(t) != 3 or any(not isinstance(v, int) or not 0 < v < (1 << d)
                             for v in t) for t in scheme):
        return False
    expected = [0] * (d*d*d)
    for i in range(b):
        for j in range(b):
            for k in range(b):
                expected[((i*b+k)*d+(k*b+j))*d+i*b+j] = 1
    return tensor(scheme, d) == expected


def reduce_scheme(s, ledger):
    s = [tuple(t) for t in s if all(t)]
    while True:
        changed = False
        for i in range(len(s)):
            for j in range(i):
                for free in range(3):
                    ledger['reduction_pair_axis_checks'] += 1
                    if all(s[i][a] == s[j][a] for a in range(3) if a != free):
                        t = list(s[j])
                        t[free] ^= s[i][free]
                        s = [t0 for k, t0 in enumerate(s) if k not in (i, j)]
                        if all(t):
                            s.append(tuple(t))
                        changed = True
                        ledger['rank_reductions'] += 1
                        break
                if changed:
                    break
            if changed:
                break
        if not changed:
            return s


def addition_count(scheme, d=4):
    left = sum(u.bit_count()-1 for u, _, _ in scheme)
    right = sum(v.bit_count()-1 for _, v, _ in scheme)
    out = sum(max(0, sum((w >> k) & 1 for _, _, w in scheme)-1)
              for k in range(d))
    return left+right+out


def search(seed=0, walks=50, steps=10000, b=2, target=7):
    rng = random.Random(seed)
    ledger = dict(seed=seed, walks_cap=walks, steps_per_walk_cap=steps,
                  attempted_moves=0, candidate_pair_axis_checks=0,
                  reduction_pair_axis_checks=0, rank_reductions=0,
                  failed_walks=0, initial_rank=b**3)
    start = time.perf_counter()
    best = schoolbook(b)
    for walk in range(walks):
        s = schoolbook(b)
        for step in range(steps):
            moves = []
            for i in range(len(s)):
                for j in range(i):
                    for a in range(3):
                        ledger['candidate_pair_axis_checks'] += 1
                        if s[i][a] == s[j][a]:
                            moves.append((i, j, a))
            if not moves:
                break
            i, j, a = rng.choice(moves)
            p, q = [k for k in range(3) if k != a]
            if rng.randrange(2):
                p, q = q, p
            # x*y*z + x*y'*z' = x*(y+y')*z + x*y'*(z+z').
            ti, tj = list(s[i]), list(s[j])
            ti[p] ^= tj[p]
            tj[q] ^= ti[q]
            s[i], s[j] = tuple(ti), tuple(tj)
            ledger['attempted_moves'] += 1
            s = reduce_scheme(s, ledger)
            if len(s) < len(best):
                best = list(s)
            if len(s) <= target:
                ledger['successful_walk'] = walk
                ledger['successful_step'] = step+1
                ledger['search_seconds'] = time.perf_counter()-start
                return s, ledger
        ledger['failed_walks'] += 1
    ledger['search_seconds'] = time.perf_counter()-start
    return best, ledger


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--seed', type=int, default=0)
    ap.add_argument('--walks', type=int, default=50)
    ap.add_argument('--steps', type=int, default=10000)
    ap.add_argument('--b', type=int, default=2)
    ap.add_argument('--target', type=int, default=7)
    ap.add_argument('--out', default='acquired_scheme.json')
    a = ap.parse_args()
    scheme, ledger = search(a.seed, a.walks, a.steps, a.b, a.target)
    start = time.perf_counter()
    valid = verify(scheme, a.b)
    ledger['verification_seconds'] = time.perf_counter()-start
    ledger['verification_coefficient_term_checks'] = len(scheme)*a.b**6
    ledger['final_rank'] = len(scheme)
    ledger['unshared_block_additions'] = addition_count(scheme, a.b*a.b)
    ledger['scheme_payload_bits'] = 3*len(scheme)*a.b*a.b
    ledger['verified'] = valid
    ledger['target_reached'] = len(scheme) <= a.target
    payload = dict(block_size=a.b, field='GF(2)', scheme=scheme, ledger=ledger)
    Path(a.out).write_text(json.dumps(payload, indent=2)+'\n')
    print(json.dumps(payload, indent=2))
    if not valid:
        raise SystemExit('Independent verification failed')


if __name__ == '__main__':
    main()
