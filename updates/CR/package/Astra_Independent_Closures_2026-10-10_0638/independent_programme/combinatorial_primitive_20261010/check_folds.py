"""Exact sunflower-fold construction; standard-library only."""
from itertools import combinations, product
from math import ceil, log2
import json


def sunflower(rows):
    return all(len({row[j] for row in rows}) in (1, len(rows)) for j in range(len(rows[0])))


def tagged_witness_code(t, q):
    assert t >= 2 and q >= 3
    gadgets = [(i, a, b) for i in range(t) for a, b in combinations(range(q), 2)]
    m = 1
    while 2**m < len(gadgets) + m + 1:
        m += 1
    controls = {0} | {1 << j for j in range(m)}
    tags = iter(k for k in range(2**m) if k not in controls)
    rows, witnesses = [], {}
    for tag in sorted(controls):
        rows.append(tuple([0] * t + [(tag >> j) & 1 for j in range(m)]))
    for i, a, b in gadgets:
        tag = next(tags)
        helper = (i + 1) % t
        triple = []
        for main, aux in [(a, 0), (a, 1), (b, 2)]:
            row = [0] * t + [(tag >> j) & 1 for j in range(m)]
            row[i], row[helper] = main, aux
            triple.append(tuple(row))
        rows.extend(triple)
        witnesses[(i, a, b)] = triple
    return rows, witnesses, m


def fold_row(row, coord, a, b):
    return tuple(a if j == coord and x == b else x for j, x in enumerate(row))


def check(t, q):
    rows, witnesses, m = tagged_witness_code(t, q)
    assert len(rows) == len(set(rows))
    assert not any(sunflower(triple) for triple in combinations(rows, 3))
    for (i, a, b), triple in witnesses.items():
        folded = [fold_row(row, i, a, b) for row in triple]
        assert len(set(folded)) == 3
        assert sunflower(folded)
    for j in range(m):
        coord = t + j
        folded = [fold_row(row, coord, 0, 1) for row in rows]
        assert len(folded) > len(set(folded))
    # Surgery: drop third row from each gadget; then fold all active alphabets
    # by 0->0, all nonzero->1. Rows retained in any one tag differ in helper.
    keep = rows[:m + 1] + [r for triple in witnesses.values() for r in triple[:2]]
    binary = [tuple(int(x != 0) if i < t else x for i, x in enumerate(row)) for row in keep]
    assert len(binary) == len(set(binary))
    assert not any(sunflower(triple) for triple in combinations(binary, 3))
    return dict(t=t, q=q, tag_coordinates=m, rank=t+m, size=len(rows),
                alphabet_product=q**t * 2**m,
                all_single_symbol_folds_blocked=True,
                binary_surgery_retained=len(binary),
                binary_surgery_fraction=len(binary)/len(rows))

if __name__ == '__main__':
    records = [check(t, q) for t,q in [(2,3), (2,4), (3,3), (4,3)]]
    print(json.dumps(records, indent=2))
