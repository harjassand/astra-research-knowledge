"""Exact finite diagnostics for the adaptive-observable acquisition report.

These checks verify fixtures and identities; the report supplies the proof.
Run with Python 3 using only the standard library.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
import math
import random

OUT = Path(__file__).resolve().parents[1] / "results" / "exact_checks.json"


def parity(v):
    return v.bit_count() % 2


def law(L, s, lam):
    return {(x, y): (1 + lam * (-1) ** (y ^ parity(s & x))) / (2 ** (L + 1))
            for x in range(2 ** L) for y in (0, 1)}


def hmm_probability(L, s, lam, bits):
    # States (i, a, z): current clock, parity before current bit, current bit.
    # Two label states (L+1, 0, y) close each block and restart the source.
    states = {(1, 0, 0): F(1, 2), (1, 0, 1): F(1, 2)}
    for k, observed in enumerate(bits):
        filtered = {q: p for q, p in states.items() if q[2] == observed}
        if k == len(bits) - 1:
            return sum(filtered.values(), F(0))
        nxt = {}
        for (i, a, z), prob in filtered.items():
            if i <= L:
                updated = a ^ (((s >> (i - 1)) & 1) * z)
                if i < L:
                    choices = [((i + 1, updated, zp), F(1, 2)) for zp in (0, 1)]
                else:
                    choices = [((L + 1, 0, yp), (1 + lam * (-1) ** (yp ^ updated)) / 2)
                               for yp in (0, 1)]
            else:
                choices = [((1, 0, zp), F(1, 2)) for zp in (0, 1)]
            for q, p in choices:
                nxt[q] = nxt.get(q, F(0)) + prob * p
        states = nxt


def solve(rows, labels, L):
    pivots = {}
    for row, label in zip(rows, labels):
        while row:
            i = row.bit_length() - 1
            if i not in pivots:
                pivots[i] = (row, label)
                break
            row ^= pivots[i][0]
            label ^= pivots[i][1]
        else:
            if label != 0:
                return None, len(pivots)
    if len(pivots) < L:
        return None, len(pivots)
    secret = 0
    for i in sorted(pivots):
        row, label = pivots[i]
        bit = label ^ parity(row & secret)
        secret |= bit << i
    assert all(parity(row & secret) == y for row, y in zip(rows, labels))
    return secret, L


counts = {"hmm_word_probabilities": 0, "pairwise_tv": 0, "batch_gram_entries": 0,
          "acquired_feature_matrices": 0, "raw_sample_trials": 0,
          "batch_decoder_coordinate_means": 0}
for L in range(1, 5):
    for lam in (F(1, 2), F(1)):
        laws = [law(L, s, lam) for s in range(2 ** L)]
        for s, dist in enumerate(laws):
            assert sum(dist.values()) == 1
            for (x, y), p in dist.items():
                bits = tuple((x >> i) & 1 for i in range(L)) + (y,)
                assert hmm_probability(L, s, lam, bits) == p
                counts["hmm_word_probabilities"] += 1
            for t in range(s):
                tv = sum(abs(dist[z] - laws[t][z]) for z in dist) / 2
                assert tv == lam / 2
                counts["pairwise_tv"] += 1
            for cut in range(1, L + 1):
                if not (s & ((1 << cut) - 1)):
                    continue
                # H = E [[1], [prefix parity]] [1, y_sign*suffix_parity].
                H = [[F(0), F(0)], [F(0), F(0)]]
                for (x, y), p in dist.items():
                    a = (-1) ** parity((s & ((1 << cut) - 1)) & x)
                    b = (-1) ** (y ^ parity((s >> cut) & (x >> cut)))
                    for i, av in enumerate((1, a)):
                        for j, bv in enumerate((1, b)):
                            H[i][j] += p * av * bv
                assert H == [[F(1), F(0)], [F(0), lam]]
                counts["acquired_feature_matrices"] += 1

# Direct tensor enumeration checks the central identity without invoking its formula.
for L in (1, 2, 3):
    base = list(law(L, 0, F(1)))
    for lam in (F(1, 2), F(1)):
        for b in range(1, 4 if L <= 2 else 3):
            batch = list(product(base, repeat=b))
            likelihoods = []
            for s in range(2 ** L):
                likelihoods.append([math.prod(1 + lam * (-1) ** (y ^ parity(s & x))
                                              for x, y in z) - 1 for z in batch])
            variance = (1 + lam * lam) ** b - 1
            for s in range(2 ** L):
                for t in range(2 ** L):
                    inner = sum(a * c for a, c in zip(likelihoods[s], likelihoods[t])) / len(batch)
                    assert inner == (variance if s == t else 0)
                    counts["batch_gram_entries"] += 1

batch_decoder_results = []
for L in (1, 2):
    b = L + 2
    designs = list(product(range(2 ** L), repeat=b))
    for s in range(2 ** L):
        sums = [F(0) for _ in range(L)]
        full = 0
        for rows in designs:
            labels = [parity(s & row) for row in rows]
            got, rank = solve(rows, labels, L)
            if got is not None:
                assert got == s
                full += 1
                for i in range(L):
                    sums[i] += (-1) ** ((got >> i) & 1)
        c = F(full, len(designs))
        assert c >= F(3, 4)
        for i in range(L):
            mean = sums[i] / len(designs)
            assert mean == c * (-1) ** ((s >> i) & 1)
            assert abs(mean) >= F(3, 4)
            counts["batch_decoder_coordinate_means"] += 1
    batch_decoder_results.append({"L": L, "b": b, "full_rank_probability": str(c),
                                  "robust_tolerance": "1/4"})

rng = random.Random(20261008)
raw_results = []
for L in (8, 16, 32, 64):
    delta = F(1, 1024)
    N = L + 10
    successes = 0
    for _ in range(100):
        s = rng.randrange(2 ** L)
        rows = [rng.randrange(2 ** L) for _ in range(N)]
        labels = [parity(s & row) for row in rows]
        got, rank = solve(rows, labels, L)
        assert got is None or got == s
        successes += got == s
        counts["raw_sample_trials"] += 1
    raw_results.append({"L": L, "N": N, "successes_of_100": successes,
                        "theorem_failure_upper_bound": str(2 ** L * F(1, 2) ** N)})

result = {"status": "PASS", "counts": counts, "raw_results": raw_results,
          "batch_decoder_results": batch_decoder_results,
          "scope": "Exact finite fixtures plus seeded raw-data diagnostics; universal proofs are in REPORT.txt."}
OUT.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
