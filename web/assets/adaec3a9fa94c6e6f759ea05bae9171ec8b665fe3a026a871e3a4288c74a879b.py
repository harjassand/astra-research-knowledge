"""Finite checks of balanced Brunnian compiler and diagonal amplification.

These tests do not materialize the Astra group or validate its nonsofic proof.
Only Python's standard library is used.
"""
from collections import Counter
from fractions import Fraction
from itertools import permutations, product
import json
from pathlib import Path
import random


def inverse(word):
    return [-x for x in reversed(word)]


def reduce_word(word):
    out = []
    for x in word:
        if out and out[-1] == -x:
            out.pop()
        else:
            out.append(x)
    return out


def balanced(start, size, original_count):
    if size == 1:
        return [2 + start % original_count]
    half = size // 2
    left = balanced(start, half, original_count)
    right = balanced(start + half, half, original_count)
    shifted_right = [1] * half + right + [-1] * half
    return left + shifted_right + inverse(left) + inverse(shifted_right)


def compose(a, b):
    return tuple(a[b[i]] for i in range(len(a)))


def perm_inverse(p):
    out = [0] * len(p)
    for i, x in enumerate(p):
        out[x] = i
    return tuple(out)


def evaluate(word, values):
    identity = tuple(range(len(values[1])))
    out = identity
    inv = {x: perm_inverse(p) for x, p in values.items()}
    for x in word:
        out = compose(out, values[x] if x > 0 else inv[-x])
    return out


def distance(a, b):
    return Fraction(sum(x != y for x, y in zip(a, b)), len(a))


def diagonal(p, exponent):
    points = list(product(range(len(p)), repeat=exponent))
    index = {x: i for i, x in enumerate(points)}
    return tuple(index[tuple(p[j] for j in x)] for x in points)


records = []
kill_checks = 0
for original_count in range(1, 33):
    size = 1 << (original_count - 1).bit_length()
    word = balanced(0, size, original_count)
    counts = Counter(abs(x) for x in word if abs(x) != 1)
    assert len(word) == 3 * size * size - 2 * size
    assert max(counts.values()) <= 2 * size
    assert reduce_word(word)
    for i in range(original_count):
        assert not reduce_word([x for x in word if abs(x) != i + 2])
        kill_checks += 1
    records.append({"M": original_count, "N": size,
                    "raw_length": len(word),
                    "reduced_length": len(reduce_word(word)),
                    "max_original_occurrences": max(counts.values())})

rng = random.Random(20261007)
hamming_checks = 0
degree = 64
identity = tuple(range(degree))
for original_count in range(1, 9):
    size = 1 << (original_count - 1).bit_length()
    word = balanced(0, size, original_count)
    counts = Counter(abs(x) for x in word if abs(x) != 1)
    for _ in range(20):
        shift = list(identity)
        rng.shuffle(shift)
        values = {1: tuple(shift)}
        for i in range(original_count):
            p = list(identity)
            # Sparse moves make the occurrence bound non-vacuous in many cases.
            for _ in range(rng.randrange(4)):
                a, b = rng.sample(range(degree), 2)
                p[a], p[b] = p[b], p[a]
            values[i + 2] = tuple(p)
        move = distance(evaluate(word, values), identity)
        for i in range(original_count):
            assert move <= counts[i + 2] * distance(values[i + 2], identity)
            hamming_checks += 1

amplification_checks = 0
for degree in (2, 3, 4):
    perms = list(permutations(range(degree)))
    for exponent in (1, 2, 3):
        lifts = {p: diagonal(p, exponent) for p in perms}
        for p in perms:
            for q in perms:
                d = distance(p, q)
                assert distance(lifts[p], lifts[q]) == 1 - (1 - d) ** exponent
                assert distance(lifts[p], lifts[q]) <= exponent * d
                assert lifts[compose(p, q)] == compose(lifts[p], lifts[q])
                amplification_checks += 1

output = {"status": "PASS", "scope": "finite compiler and metric identities only",
          "kill_checks": kill_checks, "hamming_occurrence_checks": hamming_checks,
          "diagonal_amplification_checks": amplification_checks,
          "word_records": records}
path = Path(__file__).with_suffix(".json")
path.write_text(json.dumps(output, indent=2) + "\n")
print(json.dumps({k: v for k, v in output.items() if k != "word_records"}))
