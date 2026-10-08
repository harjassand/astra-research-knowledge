#!/usr/bin/env python3
"""Exact small-chain check of Hcrit=K-4JW and its configuration form."""
from fractions import Fraction
from itertools import combinations
import json
from pathlib import Path


def check():
    tested = 0
    max_dimension = 0
    for L in range(2, 11):
        S = L - 1
        for q in range(S + 1):
            configs = list(combinations(range(1, L), q))
            index = {x: i for i, x in enumerate(configs)}
            d = len(configs)
            max_dimension = max(max_dimension, d)
            K = [[Fraction(0) for _ in range(d)] for _ in range(d)]
            W = [sum(1 for a, b in zip(x, x[1:]) if b == a + 1)
                 for x in configs]
            deg = [0] * d
            boundary = [int(1 in x) + int(S in x) for x in configs]
            for r, x in enumerate(configs):
                K[r][r] = Fraction(4 * q)
                for a, site in enumerate(x):
                    for step in (-1, 1):
                        ysite = site + step
                        if not (1 <= ysite <= S) or ysite in x:
                            continue
                        y = tuple(sorted(x[:a] + (ysite,) + x[a + 1:]))
                        c = index[y]
                        if c > r:
                            # XX+YY has matrix element 2, hence -2J here.
                            K[r][c] = K[c][r] = Fraction(-2)
                            deg[r] += 1
                            deg[c] += 1
            Hcrit = [[K[r][c] - (4 * W[r] if r == c else 0)
                      for c in range(d)] for r in range(d)]
            form = [[Fraction(0) for _ in range(d)] for _ in range(d)]
            for r in range(d):
                form[r][r] = Fraction(2 * deg[r] + 2 * boundary[r])
            for r in range(d):
                for c in range(r + 1, d):
                    if K[r][c] != 0:
                        form[r][c] = form[c][r] = Fraction(-2)
            assert Hcrit == form, (L, q, Hcrit, form)
            for V in (Fraction(-3), Fraction(0), Fraction(7, 3)):
                # Exact decomposition H(V)=Hcrit+(4+V)W.
                lhs = [[K[r][c] + (V * W[r] if r == c else 0)
                        for c in range(d)] for r in range(d)]
                rhs = [[Hcrit[r][c] + ((4 + V) * W[r] if r == c else 0)
                        for c in range(d)] for r in range(d)]
                assert lhs == rhs, (L, q, V)
            tested += 1
    return {
        "status": "PASS",
        "chain_lengths_L": [2, 10],
        "sectors_checked": tested,
        "largest_sector_dimension": max_dimension,
        "potential_values": ["-3", "0", "7/3"],
        "scope": "finite exact algebra check only; not the asymptotic continuum theorem",
    }


if __name__ == "__main__":
    out = check()
    dest = Path(__file__).with_name("form_identity_check.json")
    dest.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))
