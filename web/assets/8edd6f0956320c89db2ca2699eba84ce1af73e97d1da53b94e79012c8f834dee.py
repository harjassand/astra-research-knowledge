"""Exhaustively find the shortest binary strings with identical bigram spectra and endpoints."""
from collections import defaultdict


def key(s: str):
    counts = tuple(sum(s[i : i + 2] == g for i in range(len(s) - 1))
                   for g in ("00", "01", "10", "11"))
    return s[0], s[-1], counts


for n in range(2, 13):
    first = {}
    for value in range(1 << n):
        s = f"{value:0{n}b}"
        k = key(s)
        if k in first and first[k] != s:
            print(f"n={n}: {first[k]} and {s}; key={k}")
            raise SystemExit(0)
        first[k] = s
print("No collision through n=12")
