#!/usr/bin/env python3
"""Exact tropical witness search for the Wolf 2000 yeast glycolysis model.

State coordinates augment ATP and NAD with their conserved complements ADP and
NADH. Rational functions are split into positive gross channels. All arithmetic
in the witness check is exact.
"""

from fractions import Fraction as F
import random

NAMES = ("s1", "at", "adp", "s2", "s3", "nad", "nadh", "s4", "s5", "s6", "s6o")
D = len(NAMES)
unit = lambda i, c=1: tuple(F(c) if j == i else F(0) for j in range(D))

def vec(**kw):
    out = [F(0)] * D
    for key, value in kw.items():
        out[NAMES.index(key)] = F(value)
    return tuple(out)

def exp(**kw):
    out = [F(0)] * D
    for key, value in kw.items():
        out[NAMES.index(key)] = F(value)
    return tuple(out)

def scale(a, c):
    return tuple(F(c) * x for x in a)

def dot(a, b):
    return sum((x * y for x, y in zip(a, b)), F(0))

edges = [
    ("v0_feed", vec(s1=1), [exp()], [exp()]),
    ("v1_hill", vec(s1=-1, at=-2, adp=2, s2=1),
     [exp(s1=1, at=1)], [exp(), exp(at=4)]),
    ("v2", vec(s2=-1, s3=2), [exp(s2=1)], [exp()]),
    ("v3_forward", vec(s3=-1, nad=-1, nadh=1, s4=1, at=1, adp=-1),
     [exp(s3=1, nad=1, adp=1)], [exp(adp=1), exp(nadh=1)]),
    ("v3_reverse", vec(s3=1, nad=1, nadh=-1, s4=-1, at=-1, adp=1),
     [exp(s4=1, at=1, nadh=1)], [exp(adp=1), exp(nadh=1)]),
    ("v4", vec(s4=-1, s5=1, at=1, adp=-1),
     [exp(s4=1, adp=1)], [exp()]),
    ("v5", vec(s5=-1, s6=1), [exp(s5=1)], [exp()]),
    ("v6", vec(s6=-1, nad=1, nadh=-1),
     [exp(s6=1, nadh=1)], [exp()]),
    ("v7_atpase", vec(at=-1, adp=1), [exp(at=1)], [exp()]),
    ("v8", vec(s3=-1, nad=1, nadh=-1),
     [exp(s3=1, nadh=1)], [exp()]),
    ("v9", vec(s6o=-1), [exp(s6o=1)], [exp()]),
    ("v10_export", vec(s6=-1, s6o=F(1, 10)),
     [exp(s6=1)], [exp()]),
    ("v10_import", vec(s6=1, s6o=F(-1, 10)),
     [exp(s6o=1)], [exp()]),
]

def tau(edge, w):
    _, _, num, den = edge
    return max(dot(a, w) for a in num) - max(dot(b, w) for b in den)

def check(w):
    vals = [(e[0], dot(e[1], w), tau(e, w)) for e in edges]
    active = [item for item in vals if item[1] != 0]
    if not active:
        return None
    top = max(item[2] for item in active)
    bad = [item for item in active if item[2] == top and item[1] > 0]
    return (bad, vals) if bad else None

def main():
    rng = random.Random(20261008)
    trials = 500_000
    for t in range(1, trials + 1):
        w = tuple(F(rng.randint(-8, 8)) for _ in range(D))
        if all(x == 0 for x in w):
            continue
        result = check(w)
        if result:
            bad, vals = result
            print("REFUTED exact witness", tuple(map(str, w)))
            print("outward top channels:", bad)
            print("all (channel, projected change, tropical order):")
            for row in vals:
                print(row)
            return
    print(f"NO WITNESS in {trials} random integer directions; this is not a certificate")

if __name__ == "__main__":
    main()
