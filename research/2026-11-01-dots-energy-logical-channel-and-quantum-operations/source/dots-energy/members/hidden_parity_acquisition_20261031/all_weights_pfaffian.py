"""Established matching/FKT evaluation after gauge acquisition.

This adapter admits every even ternary tensor, including zero entries. A
six-vertex city realizes an arbitrary even signature after an even pivot flip.
Orientation and reference-sign logic follow the attributed N1077 backend.
No new Pfaffian or holographic-contraction algorithm is claimed.
"""
from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent/'prior_n1077'))
from fields import Rational
from fisher import pfaffian

EVEN = [0, 3, 5, 6]


def construct(tensors, incidence, edges):
    n = len(tensors)
    rotations, values, references = {}, {}, []
    masks, scalar = [], Q(1)
    def edge(a, b, w=1):
        values[tuple(sorted((a, b)))] = Q(w)
    for v, t in enumerate(tensors):
        if any(t[i] for i in range(8) if i not in EVEN):
            raise ValueError('Pfaffian adapter requires certified even tensors')
        nz = [i for i in EVEN if t[i]]
        if not nz:
            return None
        mask = nz[0]
        masks.append(mask)
        anchor = Q(t[mask])
        scalar *= anchor
        shifted = [Q(t[i ^ mask])/anchor for i in range(8)]
        selected = [i for i in range(3) if mask & (1 << (2-i))]
        for i in range(3):
            terminal, inner = 6*v+i, 6*v+3+i
            edge(terminal, inner)
            rotations[inner] = [terminal, 6*v+3+(i+1) % 3, 6*v+3+(i-1) % 3]
            if i not in selected:
                references.append(tuple(sorted((terminal, inner))))
        for i, j in combinations(range(3), 2):
            bitmask = (1 << (2-i)) | (1 << (2-j))
            edge(6*v+3+i, 6*v+3+j, shifted[bitmask])
        if len(selected) == 2:
            references.append(tuple(sorted((6*v+3+selected[0], 6*v+3+selected[1]))))
    next_vertex = 6*n
    for e, (u, v) in enumerate(edges):
        i, j = incidence[u].index(e), incidence[v].index(e)
        a, b = 6*u+i, 6*v+j
        fa, fb = (masks[u] >> (2-i)) & 1, (masks[v] >> (2-j)) & 1
        if fa == fb:
            edge(a, b)
            rotations[a] = [b, a+3]
            rotations[b] = [a, b+3]
            if fa:
                references.append(tuple(sorted((a, b))))
        else:
            middle = next_vertex
            next_vertex += 1
            edge(a, middle)
            edge(middle, b)
            rotations[a] = [middle, a+3]
            rotations[b] = [middle, b+3]
            rotations[middle] = [a, b]
            references.append(tuple(sorted((a if fa else b, middle))))
    flat = [v for e in references for v in e]
    assert len(flat) == next_vertex and len(set(flat)) == next_vertex
    assert next_vertex % 2 == 0
    return rotations, values, references, scalar


def orient(rotations, references):
    edge_list = sorted({tuple(sorted((u, v))) for u, ns in rotations.items() for v in ns})
    edge_index = {e:i for i,e in enumerate(edge_list)}
    component, components = {}, []
    for u in rotations:
        if u in component:
            continue
        cid = len(components)
        comp = [u]
        component[u] = cid
        for a in comp:
            for b in rotations[a]:
                if b not in component:
                    component[b] = cid
                    comp.append(b)
        components.append(comp)
    seen, faces, face_components = set(), [], []
    for u, ns in rotations.items():
        for v in ns:
            if (u, v) in seen:
                continue
            face, dart = [], (u, v)
            while dart not in seen:
                seen.add(dart)
                face.append(dart)
                a, b = dart
                neighbors = rotations[b]
                dart = (b, neighbors[(neighbors.index(a)-1) % len(neighbors)])
            assert dart == (u, v)
            faces.append(face)
            face_components.append(component[u])
    for cid, comp in enumerate(components):
        edge_count = sum(len(rotations[v]) for v in comp)//2
        if len(comp)-edge_count+face_components.count(cid) != 2:
            raise ValueError('rotation is not a planar embedding')
    rows, omitted = [], set()
    for face, cid in zip(faces, face_components):
        if cid not in omitted:
            omitted.add(cid)
            continue
        mask, rhs = 0, 1
        for a, b in face:
            mask ^= 1 << edge_index[tuple(sorted((a, b)))]
            rhs ^= int(a > b)
        rows.append((mask, rhs))
    pivots = {}
    for mask, rhs in rows:
        while mask:
            col = (mask & -mask).bit_length()-1
            if col not in pivots:
                pivots[col] = (mask, rhs)
                break
            a, b = pivots[col]
            mask ^= a
            rhs ^= b
        else:
            assert rhs == 0
    solution = 0
    for col in sorted(pivots, reverse=True):
        mask, rhs = pivots[col]
        if ((mask & solution).bit_count() & 1) != rhs:
            solution ^= 1 << col
    assert all(((mask & solution).bit_count() & 1) == rhs for mask, rhs in rows)
    arrows = {e: 1 if (solution >> i) & 1 else -1 for i, e in enumerate(edge_list)}
    sign = 1
    for e in references:
        sign *= arrows[e]
    for i, (a, b) in enumerate(references):
        for c, d in references[i+1:]:
            if a < c < b < d or c < a < d < b:
                sign = -sign
    return arrows, sign


def contract(tensors, incidence, edges, retained=None):
    city = construct(tensors, incidence, edges)
    if city is None:
        return Q(0)
    rotations, values, references, scalar = city
    # A caller may retain topology/sign for unchanged pivot masks. This test
    # implementation instead charges orientation every query.
    arrows, sign = orient(rotations, references)
    n = len(rotations)
    a = [[Q(0)]*n for _ in range(n)]
    for (u, v), w in values.items():
        a[u][v] = arrows[u, v]*w
        a[v][u] = -a[u][v]
    return scalar*sign*pfaffian(a, Rational())


if __name__ == '__main__':
    import json, random, time
    import sympy as sp
    from acquire import cube_graph, make_hidden, generate_task, apply_certificate, brute_contract
    from strong_retained_comparison import one_instance_acquire
    inc, edges, points = cube_graph()
    hidden = make_hidden(inc, edges)
    rng = random.Random(110)
    raw, _ = generate_task(hidden, rng)
    cert = one_instance_acquire(inc, edges, raw)
    records = []
    for case in range(12):
        raw, canonical = generate_task(hidden, rng)
        if case >= 3:
            for v, t in enumerate(canonical):
                t = sp.MutableDenseMatrix(t)
                t[EVEN[(v+case) % 4]] = 0
                if case >= 7:
                    t[EVEN[(v+case+1) % 4]] = 0
                if case == 11:
                    t *= 0
                canonical[v] = t
                raw[v] = hidden[v]*t
        transformed = apply_certificate(cert, raw)
        start = time.perf_counter()
        z = contract(transformed, inc, edges)
        elapsed = time.perf_counter()-start
        exact_raw = brute_contract(raw, inc, edges)
        assert z == exact_raw, (case, z, exact_raw)
        records.append(dict(case=case, partition=str(z), pfaffian_seconds=elapsed))
    Path('all_weights_results.json').write_text(json.dumps(records, indent=2)+'\n')
    print(json.dumps(records, indent=2))
