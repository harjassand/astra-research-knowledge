"""Exact finite checks for the Q-colour shared-key sparse-shift interface.

These are finite implementation/interface checks, not asymptotic proof.
All probabilities have an integer common denominator; no sampling is used.
"""

from collections import Counter
from itertools import product
from math import comb
from pathlib import Path
import json


def verify(Q, reciprocal_p, keys, word):
    distinct = sorted(set(keys))
    first = [keys.index(key) for key in distinct]
    s = len(distinct)
    den = reciprocal_p * (Q - 1)
    weights = [(reciprocal_p - 1) * (Q - 1)] + [1] * (Q - 1)
    rep_distributions = [Counter() for _ in range(Q)]
    full_distributions = [Counter() for _ in range(Q)]
    assignments = 0
    for shifts in product(range(Q), repeat=s):
        shift_map = dict(zip(distinct, shifts))
        final = [(color + shift_map[key]) % Q for color, key in zip(word, keys)]
        weight = 1
        for shift in shifts:
            weight *= weights[shift]
        reps = [final[index] for index in first]
        for target in range(Q):
            count_rep = reps.count(target)
            count_full = final.count(target)
            assert count_full >= count_rep
            rep_distributions[target][count_rep] += weight
            full_distributions[target][count_full] += weight
        assignments += 1
    normalizer = den ** s
    for target in range(Q):
        assert sum(rep_distributions[target].values()) == normalizer
        assert sum(full_distributions[target].values()) == normalizer
        # Each representative succeeds with probability at least 1/den.
        # Check every exact lower CDF against Binomial(s,1/den).
        for cutoff in range(s + 1):
            actual = sum(weight for count, weight in rep_distributions[target].items()
                         if count <= cutoff)
            control = sum(comb(s, count) * (den - 1) ** (s - count)
                          for count in range(cutoff + 1))
            assert actual <= control, (Q, reciprocal_p, keys, word, target, cutoff)
    return assignments, Q * (s + 1)


def main():
    words_checked = assignments_checked = cdf_checks = 0
    key_words = [(0, 0, 1, 1), (0, 1, 0, 1), (0, 0, 1, 2)]
    for Q in range(2, 7):
        for reciprocal_p in (8, 20):
            for keys in key_words:
                for word in product(range(Q), repeat=len(keys)):
                    assignments, checks = verify(Q, reciprocal_p, keys, word)
                    words_checked += 1
                    assignments_checked += assignments
                    cdf_checks += checks
    # Curated longer paths: distinct keys and mixed-colour double occurrences.
    for Q in range(2, 9):
        for reciprocal_p in (8, 20):
            for keys in [(0, 1, 2, 3, 4, 5), (0, 1, 0, 2, 1, 2)]:
                for word in [tuple(0 for _ in keys), tuple(i % Q for i in range(len(keys))),
                             tuple((i * i + 1) % Q for i in range(len(keys)))]:
                    assignments, checks = verify(Q, reciprocal_p, keys, word)
                    words_checked += 1
                    assignments_checked += assignments
                    cdf_checks += checks
    result = {
        "status": "PASS",
        "palette_sizes_exhaustive": [2, 3, 4, 5, 6],
        "palette_sizes_curated": [2, 3, 4, 5, 6, 7, 8],
        "reciprocal_p": [8, 20],
        "word_key_interfaces_checked": words_checked,
        "shift_assignments_checked": assignments_checked,
        "exact_lower_cdf_checks": cdf_checks,
        "checks": ["Common key applies identical modular shift at every occurrence",
                   "Final colour count dominates first-occurrence representative count",
                   "Representative lower CDF is dominated by Binomial(s,p/(Q-1))"],
        "scope": "Finite shared-key shift-law checks only; not an asymptotic theorem certificate"
    }
    output = Path(__file__).with_name("FINITE_CHECKS.json")
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
