"""Scoped checks for the scout's randomized exact learner and energy identity.

No external libraries. The learner sees only n,m and the full matrix oracle.
Hidden models are consulted only after acquisition for exact certificates.
"""
from fractions import Fraction as F
from itertools import product
from collections import deque
from pathlib import Path
import json
import math
import random
import time


def zeros(r, c=None):
    return [[F(0) for _ in range(r if c is None else c)] for _ in range(r)]


def dot(a, b):
    return sum((x*y for x, y in zip(a, b)), F(0))


def rowmul(v, a):
    return [sum((v[k]*a[k][j] for k in range(len(v))), F(0))
            for j in range(len(a[0]))]


def transpose(a):
    return [list(v) for v in zip(*a)]


def mmul(a, b):
    bt = transpose(b)
    return [[dot(row, col) for col in bt] for row in a]


def pivots(a):
    if not a:
        return []
    a = [row[:] for row in a]
    r = 0
    out = []
    for j in range(len(a[0])):
        pivot = next((i for i in range(r, len(a)) if a[i][j]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        scale = a[r][j]
        a[r] = [v/scale for v in a[r]]
        for i in range(len(a)):
            if i != r and a[i][j]:
                scale = a[i][j]
                a[i] = [x-scale*y for x, y in zip(a[i], a[r])]
        out.append(j)
        r += 1
        if r == len(a):
            break
    return out


def solve(a, b):
    n = len(b)
    a = [row[:] + [value] for row, value in zip(a, b)]
    for j in range(n):
        p = next(i for i in range(j, n) if a[i][j])
        a[j], a[p] = a[p], a[j]
        s = a[j][j]
        a[j] = [v/s for v in a[j]]
        for i in range(n):
            if i != j:
                s = a[i][j]
                a[i] = [x-s*y for x, y in zip(a[i], a[j])]
    return [a[i][-1] for i in range(n)]


def coords(basis, vector):
    if not basis:
        return [] if not any(vector) else None
    p = pivots(basis)
    c = solve(transpose([[row[j] for j in p] for row in basis]),
              [vector[j] for j in p])
    recovered = [sum((c[i]*basis[i][j] for i in range(len(c))), F(0))
                 for j in range(len(vector))]
    return c if recovered == vector else None


def closure(initial, transitions):
    basis = []
    pending = deque([initial])
    while pending:
        row = pending.popleft()
        if coords(basis, row) is None:
            basis.append(row)
            pending.extend(rowmul(row, a) for a in transitions)
    return basis


def hankel_rank(model):
    alpha, mats, beta = model
    reach = closure(alpha, mats)
    observe = closure(beta, [transpose(a) for a in mats])
    return len(pivots([[dot(r, c) for c in observe] for r in reach]))


def equivalent(left, right):
    u, a, v = left
    uu, aa, vv = right
    total = len(u) + len(uu)
    blocks = []
    for mat, other in zip(a, aa):
        b = zeros(total)
        for i in range(len(u)):
            for j in range(len(u)):
                b[i][j] = mat[i][j]
        for i in range(len(uu)):
            for j in range(len(uu)):
                b[len(u)+i][len(u)+j] = other[i][j]
        blocks.append(b)
    return all(dot(r, v+vv) == 0
               for r in closure(u+[-x for x in uu], blocks))


def matrix_oracle(model):
    alpha, mats, beta = model
    n, m = len(mats), len(alpha)
    ledger = {"calls": 0, "max_dimension": 0, "returned_entries": 0}

    def oracle(xs):
        d = len(xs[0])
        assert len(xs) == n
        assert all(xs[i][r][q] == 0 for i in range(n)
                   for r in range(d) for q in range(r+1))
        ledger["calls"] += 1
        ledger["max_dimension"] = max(ledger["max_dimension"], d)
        ledger["returned_entries"] += d*d
        out = zeros(d)
        for q in range(d):
            z = [[F(0) for _ in range(m)] for _ in range(d)]
            for r in range(d-1, -1, -1):
                z[r] = beta[:] if r == q else [F(0)]*m
                for i in range(n):
                    for h in range(r+1, d):
                        if xs[i][r][h]:
                            bz = [dot(row, z[h]) for row in mats[i]]
                            z[r] = [x+xs[i][r][h]*y for x, y in zip(z[r], bz)]
                out[r][q] = dot(alpha, z[r])
        return out
    return oracle, ledger


def acquire(n, m, oracle, seed, delta=0.01):
    rng = random.Random(seed)
    field_size = max(2, math.ceil(m*(m-1)/delta))
    probes = [[[F(rng.randrange(field_size)) for _ in range(n)]
               for _ in range(m-1)] for _ in range(m)]
    cache = {}

    def feature(p):
        if p in cache:
            return cache[p]
        k, result = len(p), []
        for probe in probes:
            xs = [zeros(m+k) for _ in range(n)]
            for t, letter in enumerate(p):
                xs[letter][t][t+1] = F(1)
            for t in range(m-1):
                for letter in range(n):
                    xs[letter][k+t][k+t+1] = probe[t][letter]
            response = oracle(xs)
            result.extend(response[0][k:k+m])
        cache[p] = result
        return result

    words, basis = [], []
    pending = deque([()])
    while pending:
        p = pending.popleft()
        vec = feature(p)
        if coords(basis, vec) is None:
            words.append(p)
            basis.append(vec)
            pending.extend(p+(i,) for i in range(n))
            if len(basis) > m:
                raise AssertionError("Exceeded supplied state bound")
    if not basis:
        return ([F(0)], [zeros(1) for _ in range(n)], [F(0)]), 0
    mats = [[coords(basis, feature(p+(i,))) for p in words] for i in range(n)]
    assert all(row is not None for a in mats for row in a)
    return (coords(basis, feature(())), mats, [row[0] for row in basis]), len(basis)


def word_model(w, n):
    d, mats = len(w), [zeros(len(w)+1) for _ in range(n)]
    for t, letter in enumerate(w):
        mats[letter][t][t+1] = F(1)
    return ([F(int(t == 0)) for t in range(d+1)], mats,
            [F(int(t == d)) for t in range(d+1)])


def fixtures():
    a, b = zeros(5), zeros(5)
    a[0][1] = a[3][4] = F(1)
    a[4][4] = F(-1)
    b[1][2] = b[0][3] = F(1)
    b[4][2] = F(-1)
    alias = ([F(1), F(0), F(0), F(0), F(0)], [a, b],
             [F(0), F(0), F(1), F(0), F(-1)])
    rev_alias = (alias[2], [transpose(x) for x in alias[1]], alias[0])
    return [
        ("constant", ([F(1)], [[[F(0)]], [[F(0)]]], [F(1)])),
        ("delayed_word", word_model((0, 1, 0, 1), 2)),
        ("cyclic_alias", alias),
        ("reversed_cyclic_alias", rev_alias),
        ("cancelled_nonzero_model", ([F(1), F(1)],
          [[[F(1), F(0)], [F(0), F(1)]], zeros(2)], [F(1), F(-1)])),
        ("hidden_unreachable", ([F(1), F(0), F(0)],
          [[[F(1), F(0), F(0)], [F(0), F(2), F(0)], [F(0), F(0), F(3)]], zeros(3)],
          [F(1), F(1), F(1)])),
        ("positive_stochastic", ([F(1, 2), F(1, 2)],
          [[[F(1, 3), F(1, 6)], [F(1, 4), F(1, 4)]],
           [[F(1, 4), F(1, 4)], [F(1, 6), F(1, 3)]]], [F(1), F(1)])),
        ("generic_cycles", ([F(1), F(2), F(-1)],
          [[[F(1, 2), F(1, 3), F(0)], [F(-1), F(0), F(2)], [F(0), F(1), F(1)]],
           [[F(0), F(1), F(0)], [F(1, 5), F(0), F(-1)], [F(2), F(0), F(0)]]],
          [F(1), F(0), F(1)]))]


def energy_checks():
    out = []
    rng = random.Random(4321)
    for n, dmat in [(2, 4), (3, 5)]:
        xs = [zeros(dmat) for _ in range(n)]
        for i in range(n):
            for r in range(dmat):
                for q in range(r+1, dmat):
                    xs[i][r][q] = F(rng.choice([-1, 0, 1]), n*dmat)
        # sum_i ||X_i||_F^2 <= 1 certifies sum_i X_i^T X_i <= I.
        normsum = sum((x*x for a in xs for row in a for x in row), F(0))
        assert normsum <= 1
        for degree in range(1, dmat+1):
            gram = zeros(dmat)
            energy = F(0)
            for w in product(range(n), repeat=degree):
                mat = [[F(int(i == j)) for j in range(dmat)] for i in range(dmat)]
                for letter in w:
                    mat = mmul(mat, xs[letter])
                energy += sum((x*x for row in mat for x in row), F(0))
                contribution = mmul(transpose(mat), mat)
                gram = [[x+y for x, y in zip(row, other)] for row, other in zip(gram, contribution)]
            # Explicit recursion is independently checked against enumerated words.
            rec = [[F(int(i == j)) for j in range(dmat)] for i in range(dmat)]
            for _ in range(degree):
                nxt = zeros(dmat)
                for a in xs:
                    contribution = mmul(mmul(transpose(a), rec), a)
                    nxt = [[x+y for x, y in zip(row, other)] for row, other in zip(nxt, contribution)]
                rec = nxt
            assert gram == rec and energy <= dmat
            out.append({"n": n, "dimension": dmat, "degree": degree,
                        "energy": str(energy), "bound": dmat})
    return out


def noisy_word_checks():
    out = []
    for n, d in [(2, 4), (2, 16), (3, 8), (3, 16)]:
        for seed in range(5):
            rng = random.Random(1000+seed+n*100+d)
            hidden = tuple(rng.randrange(n) for _ in range(d))
            sigma, delta = 1.0, 0.01
            repeats = max(1, math.ceil(8*sigma*sigma*math.log(2*d*(n-1)/delta)))
            episodes = 0

            def episode_oracle(controls):
                nonlocal episodes
                assert len(controls) == d
                assert all(len(row) == n and set(row) <= {0, 1} for row in controls)
                episodes += 1
                signal = 1
                for t in range(d):
                    signal *= controls[t][hidden[t]]
                return signal+rng.gauss(0, sigma)

            def mean_for(t, blocked):
                controls = [[1]*n for _ in range(d)]
                controls[t][blocked] = 0
                return sum(episode_oracle(controls) for _ in range(repeats))/repeats

            learned = []
            for t in range(d):
                found = n-1
                for letter in range(n-1):
                    if mean_for(t, letter) < 0.5:
                        found = letter
                        break
                learned.append(found)
            assert tuple(learned) == hidden
            out.append({"n": n, "d": d, "seed": seed, "repeats": repeats,
                        "episodes": episodes, "controlled_steps": d*episodes,
                        "recovered": True})
    return out


def main():
    started = time.monotonic()
    learned = []
    for name, target in fixtures():
        n, m = len(target[1]), len(target[0])
        actual_rank = hankel_rank(target)
        for seed in range(3):
            oracle, ledger = matrix_oracle(target)
            result, claimed_rank = acquire(n, m, oracle, seed)
            assert equivalent(target, result) and claimed_rank == actual_rank
            assert ledger["calls"] <= m*(1+n*actual_rank)
            assert ledger["max_dimension"] <= m+actual_rank
            learned.append({"fixture": name, "seed": seed, "n": n, "m": m,
                            "rank": actual_rank, "all_word_equality": True,
                            "minimal_rank": True, **ledger})
    report = {"status": "PASS", "exact_learner_checks": learned,
              "energy_checks": energy_checks(), "noisy_word_checks": noisy_word_checks(),
              "elapsed_seconds": time.monotonic()-started,
              "scope": "Finite diagnostics; theorems depend on the written proofs."}
    path = Path(__file__).with_suffix(".json")
    path.write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps({"status": report["status"], "learner_checks": len(learned),
                      "energy_checks": len(report["energy_checks"]),
                      "noisy_word_checks": len(report["noisy_word_checks"]),
                      "elapsed_seconds": report["elapsed_seconds"]}))


if __name__ == "__main__":
    main()
