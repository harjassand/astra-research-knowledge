"""Exact hard determinant-parity counting with t nonsingleton rows.

Regular rows may collide on columns. Their directed incidence graph is a
pseudoforest, handled by leaf messages and cycle traces in a commuting
double-exterior algebra. Tiny checks use exact Gaussian integers.
"""
from collections import deque
from random import Random
from time import perf_counter
from pathlib import Path
import json
from near_monomial_dp import G, determinant, brute_counts, add


def wedge_sign(P, R):
    return -1 if sum((R & ((1 << a) - 1)).bit_count()
                    for a in range(P.bit_length()) if P >> a & 1) % 2 else 1


def mul(x, y, maxk):
    out = {}
    for (P, Q, k), u in x.items():
        for (R, S, l), v in y.items():
            if P & R or Q & S or k + l > maxk: continue
            add(out, (P | R, Q | S, k + l),
                u * v * (wedge_sign(P, R) * wedge_sign(Q, S)))
    return out


def plus(*polys):
    out = {}
    for p in polys:
        for key, v in p.items(): add(out, key, v)
    return out


def shift(p, row, factor, maxk):
    return {(P, Q, k + row): v * factor for (P, Q, k), v in p.items()
            if k + row <= maxk and v * factor}


ONE = {(0, 0, 0): G(1)}


def inspect(F):
    n = len(F)
    H, to = [], [None] * n
    for i, row in enumerate(F):
        nz = [j for j, x in enumerate(row) if x]
        if len(nz) > 1: H.append(i)
        elif len(nz) == 1: to[i] = nz[0]
    children = [[] for _ in range(n)]
    for i, j in enumerate(to):
        if j is not None: children[j].append(i)
    indeg = list(map(len, children))
    queue = deque(i for i in range(n) if not indeg[i])
    peeled = []
    while queue:
        i = queue.popleft(); peeled.append(i)
        j = to[i]
        if j is not None:
            indeg[j] -= 1
            if indeg[j] == 0: queue.append(j)
    core = set(range(n)) - set(peeled)
    cycles, seen = [], set()
    for i in sorted(core):
        if i in seen: continue
        cycle, j = [], i
        while j not in seen:
            seen.add(j); cycle.append(j); j = to[j]
        cycles.append(cycle)
    return H, to, children, peeled, core, cycles


def counts(F, activities=None, row_constraints=None, col_constraints=None):
    n = len(F); maxk = n // 2
    F = [[x if isinstance(x, G) else G(x) for x in row] for row in F]
    H, to, children, peeled, core, cycles = inspect(F)
    Hset = set(H); t = len(H)
    acts = activities if activities is not None else [1] * n
    rc, cc = row_constraints or {}, col_constraints or {}
    out = [G() for _ in range(maxk + 1)]
    max_dictionary = 0
    for amask in range(1 << t):
        A = [H[j] for j in range(t) if amask >> j & 1]
        if any((i in A) != bool(v) for i, v in rc.items() if i in Hset): continue
        top = (1 << len(A)) - 1
        creators = []
        for j in range(n):
            creators.append({(1 << a, 1 << b, 0): F[ai][j] * F[bi][j].conjugate()
                             for a, ai in enumerate(A) for b, bi in enumerate(A)
                             if F[ai][j] and F[bi][j]})
        msgs, tree_inputs = {}, {}

        def children_inputs(i):
            acc = [ONE, {}]
            for child in children[i]:
                if child in core: continue
                acc = [mul(acc[0], msgs[child][0], maxk),
                       plus(mul(acc[1], msgs[child][0], maxk),
                            mul(acc[0], msgs[child][1], maxk))]
            return acc

        def row_options(i):
            if i in Hset: return (1 if i in A else 0,)
            if to[i] is None: return (0,)
            return (0, 1)

        def local(i, previous, row, inp):
            # previous is the cycle predecessor's selected row, or zero.
            if row not in row_options(i) or (i in rc and row != rc[i]): return {}
            factor = acts[i] if row else 1
            if row and i not in Hset: factor *= F[i][to[i]].abs2()
            parts = []
            for tree_count in (0, 1):
                incoming = tree_count + previous
                for extra in (0, 1):
                    col = incoming + extra
                    if row + col > 1 or col > 1: continue
                    if i in cc and col != cc[i]: continue
                    p = inp[tree_count]
                    if extra: p = mul(p, creators[i], maxk)
                    parts.append(shift(p, row, factor, maxk))
            return plus(*parts)

        components = []
        for i in peeled:
            inp = children_inputs(i)
            msgs[i] = [local(i, 0, r, inp) for r in (0, 1)]
            max_dictionary = max(max_dictionary, *(len(p) for p in msgs[i]))
            if to[i] is None: components.append(plus(*msgs[i]))
        for cyc in cycles:
            matrices = {}
            for i in cyc:
                inp = children_inputs(i)
                matrices[i] = [[local(i, previous, row, inp) for row in (0, 1)]
                               for previous in (0, 1)]
            trace = []
            for start in (0, 1):
                cur = [ONE if start == b else {} for b in (0, 1)]
                for i in cyc:
                    cur = [plus(*(mul(cur[previous], matrices[i][previous][row], maxk)
                                  for previous in (0, 1))) for row in (0, 1)]
                trace.append(cur[start])
            components.append(plus(*trace))
        total = ONE
        for component in components:
            total = mul(total, component, maxk)
            max_dictionary = max(max_dictionary, len(total))
        for (P, Q, k), value in total.items():
            if P == Q == top: out[k] += value
    assert all(z.im == 0 and z.re >= 0 for z in out), out
    return [z.re for z in out], {"exceptional_rows": t,
                                  "max_dictionary": max_dictionary,
                                  "cycles": len(cycles), "roots": sum(j is None for j in to)}


def run_checks():
    rng = Random(61302); t0 = perf_counter()
    cases = prefixes = 0; largest = 0
    for n in (4, 5, 6, 7, 8):
        for trial in range(8):
            H = set(rng.sample(range(n), 2))
            F = [[G() for _ in range(n)] for _ in range(n)]
            for i in range(n):
                if i in H:
                    F[i] = [G(rng.randint(-2, 2), rng.randint(-1, 1)) for _ in range(n)]
                elif rng.random() < .9:
                    F[i][rng.randrange(n)] = G(rng.choice((-2, -1, 1, 2)), rng.randint(-1, 1))
            acts = [rng.randint(1, 3) for _ in range(n)]
            got, stats = counts(F, acts)
            assert got == brute_counts(F, acts), (n, trial, got, brute_counts(F, acts))
            cases += 1; largest = max(largest, stats['max_dictionary'])
            for size in (1, 2, 3):
                prefix = [rng.choice(((0, 0), (1, 0), (0, 1))) for _ in range(size)]
                rc = {i: x[0] for i, x in enumerate(prefix)}
                cc = {i: x[1] for i, x in enumerate(prefix)}
                got, _ = counts(F, acts, rc, cc)
                assert got == brute_counts(F, acts, rc, cc)
                prefixes += 1
    # F has no dense rows, with arbitrary collisions and zero/self-loop rows.
    for n in range(2, 9):
        F = [[G() for _ in range(n)] for _ in range(n)]
        for i in range(n): F[i][(i * i + 1) % n] = G(i + 1, 1 - i)
        got, stats = counts(F)
        assert got == brute_counts(F)
        assert stats['exceptional_rows'] == 0
        cases += 1
    return {"status": "PASS", "seed": 61302,
            "gaussian_integer_matrices": cases, "exact_prefix_comparisons": prefixes,
            "largest_DP_dictionary": largest, "elapsed_seconds": perf_counter() - t0,
            "scope": "Finite exact bookkeeping for functional-graph/double-exterior extension, versus independent permutation-formula determinant sums."}


if __name__ == '__main__':
    result = run_checks()
    Path(__file__).with_name('functional_exterior_checks.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
