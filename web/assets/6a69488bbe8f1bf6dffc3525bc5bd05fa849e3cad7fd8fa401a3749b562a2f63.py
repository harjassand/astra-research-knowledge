#!/usr/bin/env python3
"""Find a small exact matrix-space equivalence obstruction over F_2.

Searches 3-dimensional subspaces C <= M_3(F_2) for which C and C^t have
identical rank and evaluation/singularity profiles, matching two-sided
adjoint dimensions, but are not equivalent under independent left/right GL_3.
The final orbit test is exhaustive over GL_3(F_2)^2.
"""
from itertools import combinations
from itertools import product
import random


N = 3
MASK = (1 << N) - 1


def mat_mul(a, b):
    out = 0
    for i in range(N):
        for j in range(N):
            bit = 0
            for k in range(N):
                bit ^= ((a >> (N * i + k)) & 1) & ((b >> (N * k + j)) & 1)
            out |= bit << (N * i + j)
    return out


def transpose(a):
    out = 0
    for i in range(N):
        for j in range(N):
            out |= ((a >> (N * i + j)) & 1) << (N * j + i)
    return out


def rank_bits(rows, ncols):
    rows = [x for x in rows if x]
    piv = 0
    for col in range(ncols):
        found = next((i for i in range(piv, len(rows)) if (rows[i] >> col) & 1), None)
        if found is None:
            continue
        rows[piv], rows[found] = rows[found], rows[piv]
        for i in range(len(rows)):
            if i != piv and ((rows[i] >> col) & 1):
                rows[i] ^= rows[piv]
        piv += 1
        if piv == len(rows):
            break
    return piv


def det(a):
    rows = [sum(((a >> (N * i + j)) & 1) << j for j in range(N)) for i in range(N)]
    return rank_bits(rows, N) == N


def inverse(a):
    rows = []
    for i in range(N):
        left = sum(((a >> (N * i + j)) & 1) << j for j in range(N))
        rows.append(left | (1 << (N + i)))
    piv = 0
    for col in range(N):
        found = next((i for i in range(piv, N) if (rows[i] >> col) & 1), None)
        if found is None:
            return None
        rows[piv], rows[found] = rows[found], rows[piv]
        for i in range(N):
            if i != piv and ((rows[i] >> col) & 1):
                rows[i] ^= rows[piv]
        piv += 1
    return sum(((rows[i] >> (N + j)) & 1) << (N * i + j) for i in range(N) for j in range(N))


GL = [(a, inverse(a)) for a in range(1 << (N * N)) if det(a)]


def span(gens):
    vals = {0}
    for g in gens:
        vals |= {x ^ g for x in list(vals)}
    return tuple(sorted(vals))


def subspaces_of_f2_3():
    subs = {frozenset({0})}
    for gens in combinations(range(1, 1 << N), 1):
        subs.add(frozenset(span(gens)))
    for gens in combinations(range(1, 1 << N), 2):
        subs.add(frozenset(span(gens)))
    for gens in combinations(range(1, 1 << N), 3):
        subs.add(frozenset(span(gens)))
    return sorted((tuple(sorted(s)) for s in subs), key=lambda s: (len(s), s))


SUBSPACES = subspaces_of_f2_3()


def mat_vec(a, v):
    out = 0
    for i in range(N):
        bit = 0
        for j in range(N):
            bit ^= ((a >> (N * i + j)) & 1) & ((v >> j) & 1)
        out |= bit << i
    return out


def eval_profile(code):
    bydim = {}
    for s in SUBSPACES:
        images = [mat_vec(a, v) for a in code for v in s]
        bydim.setdefault((len(s).bit_length() - 1), []).append(rank_bits(images, N))
    return tuple((d, tuple(sorted(vals))) for d, vals in sorted(bydim.items()))


def pair_eval_spectrum(code):
    counts = [0] * (2 * N + 1)
    for x in range(1 << N):
        for y in range(1 << N):
            values = [mat_vec(a, x) | (mat_vec(a, y) << N) for a in code]
            counts[rank_bits(values, 2 * N)] += 1
    return tuple(counts)


def k_eval_spectrum(code, k):
    counts = [0] * (N + 1)
    for xs in product(range(1 << N), repeat=k):
        values = []
        for a in code:
            out = 0
            for j, x in enumerate(xs):
                out |= mat_vec(a, x) << (N * j)
            values.append(out)
        counts[rank_bits(values, N * k)] += 1
    return tuple(counts)


def rank_profile(code):
    counts = [0] * (N + 1)
    for a in code:
        counts[rank_bits([sum(((a >> (N * i + j)) & 1) << j for j in range(N)) for i in range(N)], N)] += 1
    return tuple(counts)


def adjoint_dimension(code):
    # Variables are entries of X then Y; equations are XA=AY for all A in code.
    eqs = []
    for a in code:
        for i in range(N):
            for j in range(N):
                row = 0
                for k in range(N):
                    row ^= ((a >> (N * k + j)) & 1) << (N * i + k)
                    row ^= ((a >> (N * i + k)) & 1) << (N * N + N * k + j)
                eqs.append(row)
    return 2 * N * N - rank_bits(eqs, 2 * N * N)


def signature(code):
    trans = tuple(sorted(transpose(a) for a in code))
    return (rank_profile(code), eval_profile(code), adjoint_dimension(code),
            rank_profile(trans), eval_profile(trans))


def equivalent(c, d):
    target = set(d)
    for p, _ in GL:
        for q, qi in GL:
            image = {mat_mul(mat_mul(p, a), qi) for a in c}
            if image == target:
                return True
    return False


def orbit_key(c):
    return min(tuple(sorted(mat_mul(mat_mul(p, a), qi) for a in c))
               for p, _ in GL for _, qi in GL)


def stabilizer_size(c):
    target = set(c)
    return sum({mat_mul(mat_mul(p, a), qi) for a in c} == target
               for p, _ in GL for _, qi in GL)


def rand_code(rng):
    while True:
        gens = [rng.randrange(1 << (N * N)) for _ in range(N)]
        if len(span(gens)) == (1 << N):
            return span(gens)


def main():
    rng = random.Random(20261009)
    seen = {}
    print(f"|GL_3(F_2)|={len(GL)}; subspaces of F_2^3={len(SUBSPACES)}")
    for i in range(5000):
        c = rand_code(rng)
        d = tuple(sorted(transpose(a) for a in c))
        sig = signature(c)
        if sig not in seen:
            seen[sig] = c
        if sig == signature(d) and c != d and not equivalent(c, d):
            print(f"transpose obstruction found at sample {i}")
            print(f"C={c}")
            print(f"C^t={d}")
            print("basis of C:")
            basis = []
            for a in c:
                if len(span(basis + [a])) > len(span(basis)):
                    basis.append(a)
                if len(basis) == N:
                    break
            for a in basis:
                print("  " + str([[((a >> (N * r + s)) & 1) for s in range(N)] for r in range(N)]))
            print(f"rank profile={rank_profile(c)}")
            print(f"evaluation profile={eval_profile(c)}")
            print(f"transpose evaluation profile={eval_profile(d)}")
            print(f"pair evaluation spectrum(C)={pair_eval_spectrum(c)}")
            print(f"pair evaluation spectrum(C^t)={pair_eval_spectrum(d)}")
            for k in (1, 2, 3, 4):
                print(f"{k}-tuple eval spectrum(C)={k_eval_spectrum(c, k)}")
                print(f"{k}-tuple eval spectrum(C^t)={k_eval_spectrum(d, k)}")
            print(f"adjoint dimension={adjoint_dimension(c)}")
            print(f"matrix-code stabilizer sizes: {stabilizer_size(c)}, {stabilizer_size(d)}")
            print(f"signature(C)==signature(C^t): {signature(c) == signature(d)}")
            print(f"orbit_key(C)={orbit_key(c)}")
            print(f"orbit_key(C^t)={orbit_key(d)}")
            return
    print("no transpose obstruction found in 5000 samples")


if __name__ == "__main__":
    main()
