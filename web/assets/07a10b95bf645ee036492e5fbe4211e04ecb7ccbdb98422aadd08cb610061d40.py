"""Exact small verifier for F=monomial+UV^T hard-BCS determinant counts.

The proof constructs a 5^s-bond Jordan-Wigner MPO and contracts its squared
norm against cycle MPS tensors. This script executes only tiny rank1/rank2
fixtures. It is not optimized for large fixed s.
"""
from itertools import product
from random import Random
from time import perf_counter
from pathlib import Path
import json
from near_monomial_dp import G, permutation_cycles, brute_counts, add


def matrix_zero(): return [[G() for _ in range(4)] for _ in range(4)]


def matrix_identity():
    M = matrix_zero()
    for i in range(4): M[i][i] = G(1)
    return M


def matmul(A, B):
    M = matrix_zero()
    for i in range(4):
        for k in range(4):
            if not A[i][k]: continue
            for j in range(4):
                if B[k][j]: M[i][j] += A[i][k] * B[k][j]
    return M


def scale(M, z): return [[x * z for x in row] for row in M]


ID = matrix_identity()
Z = matrix_zero()
CA = matrix_zero(); CB = matrix_zero()
for a, b in product((0, 1), repeat=2):
    idx = a + 2 * b
    Z[idx][idx] = G(-1 if (a + b) % 2 else 1)
    if not a: CA[1 + 2 * b][idx] = G(1)
    if not b: CB[a + 2][idx] = G(-1 if a else 1)


def one_factor(U, V):
    alpha = {(0, 0): Z, (0, 1): scale(CA, U), (1, 1): ID}
    beta = {(0, 0): Z, (0, 1): scale(CB, V), (1, 1): ID}
    edges = [(0, 0, ID)]
    for (u, uu), A in alpha.items():
        for (v, vv), B in beta.items():
            M = matmul(A, B)
            if any(any(row) for row in M): edges.append((1 + 2 * u + v, 1 + 2 * uu + vv, M))
    return edges


def local_mpo(Urow, Vrow):
    states = [((), (), ID)]
    for u, v in zip(Urow, Vrow):
        nxt = []
        for a, b, A in states:
            for x, y, B in one_factor(u, v):
                M = matmul(A, B)
                if any(any(row) for row in M): nxt.append((a + (x,), b + (y,), M))
        states = nxt
    # Organize sparse physical matrix elements by old virtual state and input.
    out = {}
    for a, b, M in states:
        for inp in range(4):
            for physical in (0, 1, 2):  # hard projection excludes physical11
                if M[physical][inp]:
                    out.setdefault((a, inp, physical), []).append((b, M[physical][inp]))
    return out


def counts(p, d, U, V, activities=None, row_constraints=None, col_constraints=None):
    n = len(p); s = len(U[0]) if U else 0; maxk = n // 2
    def conv(x): return x if isinstance(x, G) else G(x)
    d = [conv(x) for x in d]
    U = [[conv(x) for x in row] for row in U]
    V = [[conv(x) for x in row] for row in V]
    acts = activities if activities is not None else [1] * n
    rc, cc = row_constraints or {}, col_constraints or {}
    starts = list(product((0, 1), repeat=s))
    ends = set(product((0, 4), repeat=s))
    base = {(a, b, 0): G(1) for a in starts for b in starts}
    maxstates = 0
    for cyc in permutation_cycles(p):
        result = {}
        for starta, startb in product((0, 1), repeat=2):
            cur = {(a, b, starta, startb, k): z * (-1 if (starta + startb) % 2 else 1)
                   for (a, b, k), z in base.items()}
            for i in cyc:
                mpo = local_mpo(U[i], V[i])
                nxt = {}
                for (a, b, preva, prevb, k), z in cur.items():
                    for outa, outb in product((0, 1), repeat=2):
                        inpa, inpb = outa + 2 * preva, outb + 2 * prevb
                        ga = d[i] if outa else G(1)
                        gb = d[i].conjugate() if outb else G(1)
                        coefficient = z * ga * gb * (-1 if (preva * outa + prevb * outb) % 2 else 1)
                        if not coefficient: continue
                        for physical in (0, 1, 2):
                            row, col = physical & 1, physical >> 1
                            if k + row > maxk: continue
                            if i in rc and row != rc[i]: continue
                            if i in cc and col != cc[i]: continue
                            factor = acts[i] if row else 1
                            for aa, ka in mpo.get((a, inpa, physical), []):
                                for bb, kb in mpo.get((b, inpb, physical), []):
                                    add(nxt, (aa, bb, outa, outb, k + row),
                                        coefficient * ka * kb.conjugate() * factor)
                cur = nxt; maxstates = max(maxstates, len(cur))
            for (a, b, outa, outb, k), z in cur.items():
                if outa == starta and outb == startb: add(result, (a, b, k), z)
        base = result
    out = [G() for _ in range(maxk + 1)]
    for (a, b, k), z in base.items():
        if a in ends and b in ends: out[k] += z
    assert all(z.im == 0 and z.re >= 0 for z in out), out
    return [z.re for z in out], {"rank_terms": s, "max_states": maxstates}


def full_matrix(p, d, U, V):
    n = len(p); s = len(U[0])
    F = [[G() for _ in range(n)] for _ in range(n)]
    for i in range(n):
        F[i][p[i]] += d[i]
        for j in range(n):
            for a in range(s): F[i][j] += U[i][a] * V[j][a]
    return F


def run_checks():
    rng = Random(61303); t0 = perf_counter(); cases = prefixes = 0; largest = 0
    for n, s, trials in ((4, 0, 3), (4, 1, 4), (5, 1, 4), (6, 1, 4), (4, 2, 2)):
        for trial in range(trials):
            p = list(range(n)); rng.shuffle(p)
            d = [G(rng.choice((-1, 1)), rng.randint(-1, 1)) for _ in range(n)]
            U = [[G(rng.randint(-1, 1), rng.randint(-1, 1)) for _ in range(s)] for _ in range(n)]
            V = [[G(rng.randint(-1, 1), rng.randint(-1, 1)) for _ in range(s)] for _ in range(n)]
            F = full_matrix(p, d, U, V)
            acts = [rng.randint(1, 2) for _ in range(n)]
            got, stats = counts(p, d, U, V, acts)
            want = brute_counts(F, acts)
            assert got == want, (n, s, trial, got, want)
            cases += 1; largest = max(largest, stats['max_states'])
            for size in (1, 2):
                pref = [rng.choice(((0, 0), (1, 0), (0, 1))) for _ in range(size)]
                rc = {i: x[0] for i, x in enumerate(pref)}
                cc = {i: x[1] for i, x in enumerate(pref)}
                got, _ = counts(p, d, U, V, acts, rc, cc)
                assert got == brute_counts(F, acts, rc, cc), (n, s, trial, rc, cc)
                prefixes += 1
    return {"status": "PASS", "seed": 61303, "gaussian_integer_matrices": cases,
            "exact_prefix_comparisons": prefixes, "largest_DP_state_count": largest,
            "elapsed_seconds": perf_counter() - t0,
            "scope": "Tiny exact JW/MPO sign and coefficient checks versus independent determinant enumeration; no large-rank runtime or general counting claim."}


if __name__ == '__main__':
    result = run_checks()
    Path(__file__).with_name('rank_monomial_checks.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
