"""Exact determinant-parity counts for a monomial matrix with t arbitrary rows.

No determinant-partition oracle is used. Intermediate exterior amplitudes may
have signs; returned counts are exact nonnegative Gaussian-integer sums.
The command runs only bounded tiny checks, not an asymptotic benchmark.
"""
from dataclasses import dataclass
from itertools import combinations, permutations
from math import comb
from time import perf_counter
from random import Random
import json
from pathlib import Path


@dataclass(frozen=True)
class G:
    re: int = 0
    im: int = 0

    def __add__(self, other):
        if isinstance(other, int): other = G(other)
        return G(self.re + other.re, self.im + other.im)

    __radd__ = __add__

    def __neg__(self): return G(-self.re, -self.im)

    def __sub__(self, other): return self + -other

    def __mul__(self, other):
        if isinstance(other, int): other = G(other)
        return G(self.re * other.re - self.im * other.im,
                 self.re * other.im + self.im * other.re)

    __rmul__ = __mul__

    def conjugate(self): return G(self.re, -self.im)

    def abs2(self): return self.re * self.re + self.im * self.im

    def __bool__(self): return bool(self.re or self.im)


def permutation_cycles(p):
    assert sorted(p) == list(range(len(p)))
    seen, cycles = set(), []
    for v in range(len(p)):
        if v in seen: continue
        cyc, x = [], v
        while x not in seen:
            seen.add(x); cyc.append(x); x = p[x]
        cycles.append(cyc)
    return cycles


def add(d, key, value):
    if value: d[key] = d.get(key, G()) + value


def counts(F, p, exceptional, activities=None, row_constraints=None,
           col_constraints=None):
    """Return all c_k with optional exact spin-occupation prefix constraints.

    activities are nonnegative integers in this diagnostic implementation.
    Rational activities are handled by clearing row-activity denominators.
    F entries are G or integers. p is a permutation. Only exceptional rows
    may have nonzeros off p(i). Zero monomial amplitudes are permitted.
    """
    n = len(F)
    F = [[x if isinstance(x, G) else G(x) for x in row] for row in F]
    H = sorted(exceptional); Hset = set(H)
    acts = activities if activities is not None else [1] * n
    rc, cc = row_constraints or {}, col_constraints or {}
    assert len(acts) == n and all(x >= 0 for x in acts)
    assert all(not F[i][j] for i in range(n) if i not in Hset
               for j in range(n) if j != p[i])
    cycles = permutation_cycles(p)
    answer = [G() for _ in range(n // 2 + 1)]
    max_states = 0
    for amask in range(1 << len(H)):
        A = [H[j] for j in range(len(H)) if amask >> j & 1]
        if any((i in A) != bool(v) for i, v in rc.items() if i in Hset):
            continue
        top = (1 << len(A)) - 1
        base = {(0, 0, 0): G(1)}  # ket exterior, bra exterior, row degree
        for cyc in cycles:
            result = {}
            starts = (0,) if cyc[-1] in Hset else (0, 1)
            for start in starts:
                cur = {(start, P, Q, k): v for (P, Q, k), v in base.items()}
                for i in cyc:
                    nxt = {}
                    for (incoming, P, Q, k), value in cur.items():
                        rows = ((1 if i in A else 0),) if i in Hset else (0, 1)
                        for row in rows:
                            if i in rc and row != rc[i]: continue
                            knew = k + row
                            if knew > n // 2: continue
                            outgoing = 0 if i in Hset else row
                            factor = acts[i] if row else 1
                            if row and i not in Hset: factor *= F[i][p[i]].abs2()
                            vrow = value * factor
                            for extra in (0, 1):
                                col = incoming + extra
                                if row + col > 1 or col > 1: continue
                                if i in cc and col != cc[i]: continue
                                if not extra:
                                    add(nxt, (outgoing, P, Q, knew), vrow)
                                    continue
                                for a, ai in enumerate(A):
                                    if P >> a & 1: continue
                                    h1 = F[ai][i]
                                    if not h1: continue
                                    sign1 = -1 if (P >> (a + 1)).bit_count() % 2 else 1
                                    for b, bi in enumerate(A):
                                        if Q >> b & 1: continue
                                        h2 = F[bi][i].conjugate()
                                        if not h2: continue
                                        sign2 = -1 if (Q >> (b + 1)).bit_count() % 2 else 1
                                        add(nxt, (outgoing, P | 1 << a, Q | 1 << b, knew),
                                            vrow * h1 * h2 * (sign1 * sign2))
                    cur = nxt
                    max_states = max(max_states, len(cur))
                for (outgoing, P, Q, k), value in cur.items():
                    if outgoing == start: add(result, (P, Q, k), value)
            base = result
        for (P, Q, k), value in base.items():
            if P == Q == top: answer[k] = answer[k] + value
    assert all(z.im == 0 and z.re >= 0 for z in answer), answer
    return [z.re for z in answer], max_states


def determinant(matrix):
    # Separate exact permutation formula: bounded fixtures only.
    k = len(matrix)
    if not k: return G(1)
    z = G()
    for p in permutations(range(k)):
        inv = sum(p[i] > p[j] for i in range(k) for j in range(i + 1, k))
        term = G(-1 if inv % 2 else 1)
        for i in range(k): term *= matrix[i][p[i]]
        z += term
    return z


def brute_counts(F, activities=None, row_constraints=None, col_constraints=None):
    n = len(F)
    F = [[x if isinstance(x, G) else G(x) for x in row] for row in F]
    acts = activities if activities is not None else [1] * n
    rc, cc = row_constraints or {}, col_constraints or {}
    out = [0 for _ in range(n // 2 + 1)]
    for k in range(n // 2 + 1):
        for I in combinations(range(n), k):
            Is = set(I)
            if any((i in Is) != bool(v) for i, v in rc.items()): continue
            factor = 1
            for i in I: factor *= acts[i]
            for J in combinations([j for j in range(n) if j not in Is], k):
                Js = set(J)
                if any((j in Js) != bool(v) for j, v in cc.items()): continue
                out[k] += factor * determinant([[F[i][j] for j in J] for i in I]).abs2()
    return out


def exact_sample(F, p, exceptional, k, rng, activities=None):
    """Exact expected-time fair-bit sampling via integer rejection draws.

    This is a finite diagnostic implementation, not a worst-time compiler.
    The proof specifies a dyadic approximation for worst-time TV budgets.
    """
    rows, cols = {}, {}
    for i in range(len(F)):
        branches = []
        for ri, ci in ((0, 0), (1, 0), (0, 1)):
            rr, cc = dict(rows), dict(cols)
            rr[i], cc[i] = ri, ci
            z, _ = counts(F, p, exceptional, activities, rr, cc)
            branches.append(z[k])
        total = sum(branches)
        if not total: raise ValueError("empty conditional support")
        draw = rng.randrange(total)
        for (ri, ci), mass in zip(((0, 0), (1, 0), (0, 1)), branches):
            if draw < mass:
                rows[i], cols[i] = ri, ci
                break
            draw -= mass
    return tuple(i for i, v in rows.items() if v), tuple(i for i, v in cols.items() if v)


def run_checks():
    rng = Random(61301)
    cases = prefix_cases = sampled = 0
    max_states = 0
    t0 = perf_counter()
    for n in (4, 5, 6, 7, 8):
        for trial in range(8):
            p = list(range(n)); rng.shuffle(p)
            H = sorted(rng.sample(range(n), min(3, n)))
            F = [[G() for _ in range(n)] for _ in range(n)]
            for i in range(n):
                if i in H:
                    F[i] = [G(rng.randint(-2, 2), rng.randint(-1, 1)) for _ in range(n)]
                else:
                    F[i][p[i]] = G(rng.choice((-2, -1, 1, 2)), rng.randint(-1, 1))
            activities = [rng.randint(1, 3) for _ in range(n)]
            got, ns = counts(F, p, H, activities)
            want = brute_counts(F, activities)
            assert got == want, (n, trial, got, want)
            cases += 1; max_states = max(max_states, ns)
            for prefix in range(3):
                state = [rng.choice(((0, 0), (1, 0), (0, 1))) for _ in range(prefix)]
                rows = {i: v[0] for i, v in enumerate(state)}
                cols = {i: v[1] for i, v in enumerate(state)}
                got, ns = counts(F, p, H, activities, rows, cols)
                want = brute_counts(F, activities, rows, cols)
                assert got == want, (n, trial, rows, cols, got, want)
                prefix_cases += 1; max_states = max(max_states, ns)
            if trial == 0:
                z, _ = counts(F, p, H, activities)
                k = max(j for j, v in enumerate(z) if v)
                I, J = exact_sample(F, p, H, k, rng, activities)
                assert len(I) == len(J) == k and not set(I) & set(J)
                assert determinant([[F[i][j] for j in J] for i in I]).abs2() > 0
                sampled += 1
    # Directed long cycle degeneracy and a dense-row repair both admitted.
    n = 8; p = list(range(1, n)) + [0]
    F = [[G() for _ in range(n)] for _ in range(n)]
    for i in range(n): F[i][p[i]] = G(1)
    z, _ = counts(F, p, [])
    assert z[-1] == 2
    F[0] = [G((j % 3) - 1, (j % 2)) for j in range(n)]
    z, _ = counts(F, p, [0])
    assert z == brute_counts(F)
    return {
        "status": "PASS", "seed": 61301,
        "gaussian_integer_matrices": cases,
        "exact_prefix_comparisons": prefix_cases,
        "support_only_samples": sampled,
        "largest_DP_dictionary": max_states,
        "special_cycle_checks": 2,
        "elapsed_seconds": perf_counter() - t0,
        "scope": "Finite exact bookkeeping against independent permutation determinants. No general mixing claim or asymptotic runtime benchmark."
    }


if __name__ == "__main__":
    result = run_checks()
    path = Path(__file__).with_name("near_monomial_checks.json")
    path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
