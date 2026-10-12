#!/usr/bin/env python3
"""Finite checks for S5.md, using only the Python standard library."""
from fractions import Fraction
from itertools import combinations, product
import json
import random
from pathlib import Path


def consistent(rows):
    basis = {}
    for a, b in rows:
        while a:
            p = a.bit_length() - 1
            if p not in basis:
                basis[p] = a, b
                break
            c, d = basis[p]
            a, b = a ^ c, b ^ d
        if not a and b:
            return False
    return True


def parity(a, x):
    return (a & x).bit_count() & 1


def connected(n, edges, edge_mask, s=0, t=1):
    seen = {s}
    while True:
        old = len(seen)
        for i, (u, v) in enumerate(edges):
            if edge_mask >> i & 1 and (u in seen or v in seen):
                seen.update((u, v))
        if len(seen) == old:
            return t in seen


def flow_helpers(n, edges, s=0, t=1):
    rows = []
    next_var = len(edges)
    for v in range(n):
        xs = [i for i, e in enumerate(edges) if v in e]
        b = int(v == s or v == t)
        if len(xs) <= 3:
            if xs or b:
                rows.append((sum(1 << x for x in xs), b))
            continue
        y = next_var
        next_var += 1
        rows.append(((1 << xs[0]) ^ (1 << xs[1]) ^ (1 << y), 0))
        for x in xs[2:-2]:
            new_y = next_var
            next_var += 1
            rows.append(((1 << y) ^ (1 << x) ^ (1 << new_y), 0))
            y = new_y
        rows.append(((1 << y) ^ (1 << xs[-2]) ^ (1 << xs[-1]), b))
    return rows, next_var


def reinforce(helpers, num_core_vars, k=1):
    out = []
    z = num_core_vars
    for a, b in helpers:
        xs = [j for j in range(num_core_vars) if a >> j & 1]
        assert 1 <= len(xs) <= 3
        split = min(2, max(1, len(xs) - 1))
        p = sum(1 << j for j in xs[:split])
        q = a ^ p
        for _ in range(k):
            out.extend(((p ^ (1 << z), 0), (q ^ (1 << z), b)))
            z += 1
    return out, z


def random_unsat(rows, probs=None):
    if probs is None:
        count = 0
        for keep in range(1 << len(rows)):
            count += not consistent(r for j, r in enumerate(rows) if keep >> j & 1)
        return Fraction(count, 1 << len(rows))
    answer = Fraction(0)
    for keep in range(1 << len(rows)):
        weight = Fraction(1)
        subset = []
        for j, (r, p) in enumerate(zip(rows, probs)):
            if keep >> j & 1:
                subset.append(r)
                weight *= p
            else:
                weight *= 1 - p
        if not consistent(subset):
            answer += weight
    return answer


def xor_set(a, b):
    result = 0
    for x in (0, 1):
        for y in (0, 1):
            if a >> x & 1 and b >> y & 1:
                result |= 1 << (x ^ y)
    return result


def combine(d1, d2, operation):
    out = [Fraction(0) for _ in range(4)]
    for a, pa in enumerate(d1):
        for b, pb in enumerate(d2):
            out[operation(a, b)] += pa * pb
    return out


def laminar_unsat(rows, probs):
    local = {}
    p_empty_ok = Fraction(1)
    for (a, b), p in zip(rows, probs):
        if a == 0:
            if b:
                p_empty_ok *= 1 - p
            continue
        dist = local.setdefault(a, [Fraction(0), Fraction(0), Fraction(0), Fraction(1)])
        row_dist = [Fraction(0), Fraction(0), Fraction(0), 1 - p]
        row_dist[1 << b] += p
        local[a] = combine(dist, row_dist, lambda x, y: x & y)
    supports = list(local)
    for a, b in combinations(supports, 2):
        assert not a & b or a & b == a or a & b == b
    children = {a: [] for a in supports}
    roots = []
    for a in supports:
        supersets = [b for b in supports if a != b and a & b == a]
        if supersets:
            parent = min(supersets, key=int.bit_count)
            children[parent].append(a)
        else:
            roots.append(a)
    cached = {}
    for a in sorted(supports, key=int.bit_count):
        covered = 0
        for c in children[a]:
            covered |= c
        dist = [Fraction(0) for _ in range(4)]
        dist[3 if a ^ covered else 1] = Fraction(1)
        for c in children[a]:
            dist = combine(dist, cached[c], xor_set)
        cached[a] = combine(dist, local[a], lambda x, y: x & y)
    p_consistent = p_empty_ok
    for a in roots:
        p_consistent *= 1 - cached[a][0]
    return 1 - p_consistent


def verify():
    counters = {}
    graph_masks = 0
    graph_count = 0
    for n in (2, 3, 4):
        possible = list(combinations(range(n), 2))
        for graph_mask in range(1 << len(possible)):
            edges = [e for i, e in enumerate(possible) if graph_mask >> i & 1]
            helpers, _ = flow_helpers(n, edges)
            graph_count += 1
            for open_mask in range(1 << len(edges)):
                closed = [(1 << i, 0) for i in range(len(edges)) if not open_mask >> i & 1]
                assert consistent(helpers + closed) == connected(n, edges, open_mask)
                graph_masks += 1
    # Explicit degree-four parity splitting case, plus multiedges.
    for n, edges in ((5, [(0, i) for i in range(1, 5)]),
                     (2, [(0, 1)] * 4)):
        helpers, _ = flow_helpers(n, edges)
        for open_mask in range(1 << len(edges)):
            closed = [(1 << i, 0) for i in range(len(edges)) if not open_mask >> i & 1]
            assert consistent(helpers + closed) == connected(n, edges, open_mask)
            graph_masks += 1
    counters.update(graphs=graph_count + 2, graph_open_masks=graph_masks)

    gadget_cases = 0
    for arity in (1, 2, 3):
        for b in (0, 1):
            helper = ((1 << arity) - 1, b)
            gadget, nv = reinforce([helper], arity)
            assert len({a for a, _ in gadget}) == len(gadget)
            for x in range(1 << arity):
                for keep in range(4):
                    has_extension = any(
                        all(parity(a, x | (z << arity)) == rhs
                            for j, (a, rhs) in enumerate(gadget) if keep >> j & 1)
                        for z in (0, 1))
                    expected = keep != 3 or parity(helper[0], x) == b
                    assert has_extension == expected
                    gadget_cases += 1
    counters['gadget_assignment_masks'] = gadget_cases

    exact_examples = []
    examples = [
        (2, [(0, 1)], 1),
        (2, [(0, 1)], 2),
        (3, [(0, 1), (0, 2), (1, 2)], 1),
        (4, list(combinations(range(4), 2)), 1),
        (5, [(0, i) for i in range(1, 5)], 1),
        (2, [(0, 1)] * 4, 1),
    ]
    for n, edges, k in examples:
        helpers, nc = flow_helpers(n, edges)
        gadget, nv = reinforce(helpers, nc, k)
        edge_rows = [(1 << i, 0) for i in range(len(edges))]
        final = edge_rows + gadget
        assert max(a.bit_count() for a, _ in final) <= 3
        assert len({a for a, _ in final}) == len(final)
        q = random_unsat(final)
        alpha = 1 - Fraction(3, 4) ** k
        effective = random_unsat(edge_rows + helpers,
                                 [Fraction(1, 2)] * len(edges) + [alpha] * len(helpers))
        u = Fraction(sum(not connected(n, edges, keep) for keep in range(1 << len(edges))),
                     1 << len(edges))
        assert q == effective
        assert alpha ** len(helpers) * u <= q <= u
        exact_examples.append(dict(n=n, m=len(edges), k=k, helpers=len(helpers),
                                   rows=len(final), variables=nv, U=str(u), q=str(q)))
    counters['all_random_examples'] = exact_examples

    rng = random.Random(1052026)
    family = [1, 2, 4, 8, 3, 12, 15]
    laminar_cases = 0
    for _ in range(80):
        rows = [(rng.choice(family), rng.randrange(2)) for _ in range(rng.randrange(1, 10))]
        if rng.randrange(2):
            rows.append((0, rng.randrange(2)))
        probs = [rng.choice([Fraction(1, 2), Fraction(1, 3), Fraction(2, 3)]) for _ in rows]
        assert laminar_unsat(rows, probs) == random_unsat(rows, probs)
        laminar_cases += 1
    counters['laminar_direct_enumeration_cases'] = laminar_cases
    counters['status'] = 'PASS'
    return counters


if __name__ == '__main__':
    result = verify()
    print(json.dumps(result, indent=2))
    Path(__file__).with_name('S5_verification.json').write_text(json.dumps(result, indent=2) + '\n')
