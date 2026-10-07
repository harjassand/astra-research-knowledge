"""Bounded exact transcription checks; not a proof or a physical sampler."""
from collections import defaultdict
from fractions import Fraction as F
from itertools import permutations, product
from math import factorial
from pathlib import Path
from time import perf_counter
import json


def partitions(n, cap=None):
    if n == 0:
        yield ()
        return
    for a in range(min(n, n if cap is None else cap), 0, -1):
        for tail in partitions(n-a, a):
            yield (a,) + tail


def parity(p):
    return (-1)**sum(p[i] > p[j] for i in range(len(p)) for j in range(i+1, len(p)))


def clean(v):
    return {k: x for k, x in v.items() if x}


def column_vector(lam):
    hs = [sum(x > c for x in lam) for c in range(lam[0])]
    v = {(): 1}
    for h in hs:
        out = {}
        for old, coef in v.items():
            for p in permutations(range(h)):
                out[old+p] = coef*parity(p)
        v = out
    return hs, v


def raising(v, a):
    out = defaultdict(int)
    for word, coef in v.items():
        for i, letter in enumerate(word):
            if letter == a+1:
                out[word[:i]+(a,)+word[i+1:]] += coef
    return clean(out)


def swaps_sum(v):
    out = defaultdict(int)
    n = len(next(iter(v)))
    for word, coef in v.items():
        for i in range(n):
            for j in range(i+1, n):
                w = list(word)
                w[i], w[j] = w[j], w[i]
                out[tuple(w)] += coef
    return clean(out)


def dimensions(lam, d):
    padded = lam+(0,)*(d-len(lam))
    weyl = F(1)
    for i in range(d):
        for j in range(i+1, d):
            weyl *= F(padded[i]-padded[j]+j-i, j-i)
    hooks = 1
    for i, row in enumerate(lam):
        for j in range(row):
            below = sum(x > j for x in lam[i+1:])
            hooks *= row-j+below
    specht = F(factorial(sum(lam)), hooks)
    assert weyl.denominator == specht.denominator == 1
    return int(weyl), int(specht)


def matrix_rank(rows):
    a = [[F(x) for x in row] for row in rows]
    r = 0
    for c in range(len(a[0])):
        piv = next((i for i in range(r, len(a)) if a[i][c]), None)
        if piv is None:
            continue
        a[r], a[piv] = a[piv], a[r]
        scale = a[r][c]
        a[r] = [x/scale for x in a[r]]
        for i in range(r+1, len(a)):
            scale = a[i][c]
            if scale:
                a[i] = [x-scale*y for x, y in zip(a[i], a[r])]
        r += 1
        if r == len(a):
            break
    return r


def infinitesimal_rotation(v, a, b):
    out = defaultdict(int)
    for word, coef in v.items():
        for i, letter in enumerate(word):
            if letter == b:
                out[word[:i]+(a,)+word[i+1:]] += coef
            if letter == a:
                out[word[:i]+(b,)+word[i+1:]] -= coef
    return clean(out)


def main():
    start = perf_counter()
    fixtures = []
    for d in range(1, 5):
        for n in range(1, 7):
            dim_sum = 0
            for lam in partitions(n):
                if len(lam) > d:
                    continue
                hs, v = column_vector(lam)
                assert max(hs) == len(lam)
                assert sum(c*c for c in v.values()) == factorial(1)*prod_factorials(hs)
                for word in v:
                    assert tuple(word.count(i) for i in range(d)) == lam+(0,)*(d-len(lam))
                for i in range(d-1):
                    assert not raising(v, i)
                casimir_scalar = sum(x*(x-2*i-1)//2 for i, x in enumerate(lam))
                assert swaps_sum(v) == clean({w: casimir_scalar*c for w, c in v.items()})
                weyl, specht = dimensions(lam, d)
                dim_sum += weyl*specht
                fixtures.append({"d": d, "N": n, "lambda": lam, "columns": hs,
                                 "sparse_terms": len(v), "D": weyl, "f": specht})
            assert dim_sum == d**n

    # SU(2) filtered Haar mean: p=|<0|u>|^2 is uniform on [0,1].
    acceptance_checks = 0
    min_ratio = F(1)
    for n in range(1, 9):
        for b in range(n//2+1):
            k = n-2*b
            for a1, a2 in [(F(4), F(1)), (F(3), F(2)), (F(5,4), F(1,4)), (F(1), F(1))]:
                integral = sum(F(factorial(k), factorial(j)*factorial(k-j))*
                               a2**(k-j)*(a1-a2)**j/F(j+1) for j in range(k+1))
                character = (a1*a2)**b * sum(a1**j*a2**(k-j) for j in range(k+1))
                mean = (a1*a2)**b*integral
                assert mean == character/(k+1)
                envelope = a1**(n-b)*a2**b
                assert envelope <= character <= (k+1)*envelope
                ratio = mean/envelope
                assert F(1, k+1) <= ratio <= 1
                min_ratio = min(min_ratio, ratio)
                acceptance_checks += 1

    # Proper-group counterexample: symmetric Cartesian spin-one four-body singlet.
    basis = list(product(range(3), repeat=4))
    t = {w: int(w[0] == w[1] and w[2] == w[3]) +
              int(w[0] == w[2] and w[1] == w[3]) +
              int(w[0] == w[3] and w[1] == w[2]) for w in basis}
    t = clean(t)
    assert sum(x*x for x in t.values()) == 45
    for p in permutations(range(4)):
        assert {tuple(w[i] for i in p): c for w, c in t.items()} == t
    for a, b in [(0,1), (0,2), (1,2)]:
        assert not infinitesimal_rotation(t, a, b)
    flat13 = [[t.get((a,)+rest, 0) for rest in product(range(3), repeat=3)] for a in range(3)]
    flat22 = [[t.get(left+right, 0) for right in product(range(3), repeat=2)]
              for left in product(range(3), repeat=2)]
    assert matrix_rank(flat13) == 3
    assert matrix_rank(flat22) == 6

    result = {"status": "PASS_EXACT_TRANSCRIPTION_CHECKS_ONLY",
              "column_fixtures": len(fixtures), "max_N": 6, "max_d": 4,
              "max_sparse_terms": max(f["sparse_terms"] for f in fixtures),
              "normalizer_dimension_sums": 24,
              "qubit_rejection_moment_fixtures": acceptance_checks,
              "minimum_checked_rejection_ratio": str(min_ratio),
              "spin1_counterexample": {"norm_squared": 45, "rank_1_3": 3,
                                       "rank_2_2": 6, "permutations_checked": 24,
                                       "rotation_generators_checked": 3},
              "runtime_seconds": perf_counter()-start,
              "fixtures": fixtures,
              "limits": "No Haar sampler, finite-bit compiler, physical preparation, lower-bound search or theorem certification executed."}
    path = Path(__file__).with_suffix('.json')
    path.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k != 'fixtures'}, indent=2))


def prod_factorials(hs):
    x = 1
    for h in hs:
        x *= factorial(h)
    return x


if __name__ == '__main__':
    main()
