#!/usr/bin/env python3
"""Exact finite checks for the pendant-pair Gaussian/matching reduction.

Standard library only. This is an exponential small-instance verifier, NOT an
efficient Gaussian sampler or a newly implemented perfect-matching FPRAS.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations
from math import factorial
from pathlib import Path
import json
import random
import time


def pm_count(A):
    n = len(A)
    @lru_cache(None)
    def rec(mask):
        if not mask:
            return 1
        first = (mask & -mask).bit_length() - 1
        rest = mask ^ (1 << first)
        return sum(A[first][j] * rec(rest ^ (1 << j))
                   for j in range(first + 1, n) if rest >> j & 1)
    return rec((1 << n) - 1)


def remove_pair(A, u, v):
    keep = [i for i in range(len(A)) if i not in (u, v)]
    return tuple(tuple(A[i][j] for j in keep) for i in keep)


def kernel(A, u, v, shift=0):
    n = len(A)
    t, lam = F(1, 4*n), F(1, 4*2**shift)
    B = [[F(0) for _ in range(n+2)] for _ in range(n+2)]
    for i in range(n):
        for j in range(n):
            B[i][j] = t*A[i][j]
    B[u][n] = B[n][u] = lam
    B[v][n+1] = B[n+1][v] = lam
    return tuple(tuple(row) for row in B), t, lam


def hafnian_repeated(B, counts):
    """Direct labelled-token Wick recursion, including repeated leaf tokens."""
    tokens = tuple(i for i, c in enumerate(counts) for _ in range(c))
    @lru_cache(None)
    def rec(xs):
        if not xs:
            return F(1)
        if len(xs) % 2:
            return F(0)
        a = xs[0]
        return sum((B[a][xs[j]] * rec(xs[1:j] + xs[j+1:])
                    for j in range(1, len(xs))), F(0))
    return rec(tokens)


def exact_q(A, u, v, shift=0):
    n = len(A)
    z = pm_count(A)
    zminor = pm_count(remove_pair(A, u, v))
    p = F(zminor, z)
    R = F(n, 4*4**shift)
    odds = R*R*p*p
    return odds/(1+odds), p


def graph_from_mask(n, mask):
    A = [[0]*n for _ in range(n)]
    for k, (i, j) in enumerate(combinations(range(n), 2)):
        if mask >> k & 1:
            A[i][j] = A[j][i] = 1
    return tuple(tuple(row) for row in A)


def run():
    started = time.perf_counter()
    rng = random.Random(20261010)
    graphs = [graph_from_mask(n, mask)
              for n in (2, 4)
              for mask in range(1 << (n*(n-1)//2))]
    for n in (6, 8, 10, 12):
        graphs += [graph_from_mask(n, rng.getrandbits(n*(n-1)//2))
                   for _ in range(30)]
        graphs.append(graph_from_mask(n, (1 << (n*(n-1)//2))-1))
        A = [[0]*n for _ in range(n)]
        for i in range(0, n, 2):
            A[i][i+1] = A[i+1][i] = 1
        graphs.append(tuple(tuple(row) for row in A))

    positive = pairs = fock_patterns = calibration_steps = 0
    examples = []
    for A in graphs:
        n, z = len(A), pm_count(A)
        if not z:
            continue
        positive += 1
        for v in range(1, n):
            if not A[0][v]:
                continue
            pairs += 1
            B, t, lam = kernel(A, 0, v)
            assert max(map(sum, B)) < F(1, 2)
            frob = sum((x*x for row in B for x in row), F(0))
            assert frob < F(5, 16)
            assert F(4, 3)*frob < F(5, 12)
            masses = {}
            for a in range(3):
                for b in range(3):
                    h = hafnian_repeated(B, (1,)*n+(a,b))
                    masses[a,b] = h*h/F(factorial(a)*factorial(b))
                    fock_patterns += 1
                    if (a,b) not in ((0,0),(1,1)):
                        assert masses[a,b] == 0
            assert masses[0,0] == t**n*z*z
            zm = pm_count(remove_pair(A, 0, v))
            assert masses[1,1] == lam**4*t**(n-2)*zm*zm
            q, p = exact_q(A, 0, v)
            assert q == masses[1,1]/sum(masses.values())
            assert (1+F(n*n,16))*F(1,4)**n >= sum(masses.values())

        # Exact-frequency calibration and telescoping; no stochastic calls.
        current = A
        squared_count = F(1)
        trace = []
        while current:
            N = len(current)
            candidates = [(exact_q(current, 0, v)[0], v)
                          for v in range(1,N) if current[0][v]]
            q, v = max(candidates)
            assert q >= F(1,17)
            shift = 0
            while q > F(1,2):
                shift += 1
                q, p = exact_q(current, 0, v, shift)
                calibration_steps += 1
            assert F(1,32) < q <= F(65,128)
            R = F(N,4*4**shift)
            squared_count *= R*R*(1-q)/q
            trace.append({'N':N,'v':v,'shift':shift,'q':str(q)})
            current = remove_pair(current, 0, v)
        assert squared_count == z*z
        if n in (2,4,8,12) and len(examples) < 8:
            examples.append({'n':n,'matching_count':z,'trace':trace})
    result = {
        'status':'PASS', 'seed':20261010, 'graphs':len(graphs),
        'positive_graphs':positive, 'edge_pairs':pairs,
        'direct_fock_patterns':fock_patterns,
        'calibration_halvings':calibration_steps,
        'exact_telescoping_cases':positive,
        'elapsed_seconds':time.perf_counter()-started,
        'scope':'Exact small rational identities, energy upper bounds, support, '
                'calibration and telescoping. No physical experiment, independent '
                'proof certification, or efficient conditional sampler.',
        'examples':examples,
    }
    path = Path(__file__).with_name('REDUCTION_CHECKS.json')
    path.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='examples'},indent=2))


if __name__ == '__main__':
    run()
