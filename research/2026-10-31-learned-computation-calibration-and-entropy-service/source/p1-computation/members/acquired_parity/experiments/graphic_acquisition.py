#!/usr/bin/env python3
"""Acquire a bounded-degree 3-connected graph from an exact binary matrix.

No graph, vertex labels, embedding, or decomposition is supplied to the learner.
The recognizer is complete when the column matroid is that of a simple
3-vertex-connected graph of maximum degree <= degree_cap, with >=4 vertices.
Acceptance is gated by an exact incidence-rowspace certificate and explicit
simple/3-connected checks. Failure outside the promise is UNKNOWN, not a proof
of nongraphicness.

The planar branch reconstructs the dual with the same bounded-degree method,
then certifies its face walks and an orientable sphere rotation system. For a
cubic primal, it computes the affine cut-code partition by a four-vertex
Fisher gadget and an exact rational Pfaffian. The baseline independently sums
the dual code. This file uses only the Python standard library.
"""

from collections import defaultdict, deque
from fractions import Fraction as Q
from itertools import combinations
from math import prod, comb
from random import Random
from time import perf_counter
import json


def basis(rows):
    b = {}
    for x in rows:
        while x:
            p = x.bit_length() - 1
            if p in b:
                x ^= b[p]
            else:
                b[p] = x
                break
    for p in sorted(b):
        for q in list(b):
            if q != p and ((b[q] >> p) & 1):
                b[q] ^= b[p]
    return tuple(b[p] for p in sorted(b, reverse=True))


def nullspace(rows, n):
    rr = basis(rows)
    pivots = {r.bit_length() - 1 for r in rr}
    ans = []
    for f in range(n):
        if f in pivots:
            continue
        x = 1 << f
        for r in rr:
            p = r.bit_length() - 1
            if (r & x).bit_count() & 1:
                x ^= 1 << p
        ans.append(x)
    return ans


def columns(rows, n):
    return [sum(((r >> e) & 1) << i for i, r in enumerate(rows))
            for e in range(n)]


def bit_members(mask):
    while mask:
        b = mask & -mask
        yield b.bit_length() - 1
        mask ^= b


def matroid_connected(cols, removed=0):
    """Fundamental-circuit components, including singleton loops/coloops."""
    live = [e for e in range(len(cols)) if not ((removed >> e) & 1)]
    if not live:
        return False
    parent = {e: e for e in live}

    def find(e):
        while parent[e] != e:
            parent[e] = parent[parent[e]]
            e = parent[e]
        return e

    b = {}
    for e in live:
        v, relation = cols[e], 1 << e
        while v:
            p = v.bit_length() - 1
            if p in b:
                u, r = b[p]
                v ^= u
                relation ^= r
            else:
                b[p] = (v, relation)
                break
        if not v:
            parts = list(bit_members(relation))
            anchor = find(parts[0])
            for j in parts[1:]:
                parent[find(j)] = anchor
    return len({find(e) for e in live}) == 1


def graph_connected(nv, edges, removed=frozenset()):
    vertices = set(range(nv)) - set(removed)
    if not vertices:
        return False
    adj = [[] for _ in range(nv)]
    for u, v in edges:
        if u not in removed and v not in removed:
            adj[u].append(v)
            adj[v].append(u)
    seen = {next(iter(vertices))}
    queue = list(seen)
    for u in queue:
        for v in adj[u]:
            if v not in seen:
                seen.add(v)
                queue.append(v)
    return seen == vertices


def incidence(nv, edges):
    return [sum(1 << e for e, ends in enumerate(edges) if v in ends)
            for v in range(nv)]


def small_rowspace_words(annihilator_cols, degree_cap, counts):
    """Meet in the middle; output every nonzero word of weight <= cap once.

    For each size k, split its ordered support after floor(k/2). A pair of
    half supports gives a rowspace word iff their annihilator syndromes agree.
    Requiring all left indices < all right indices prevents duplicates.
    Worst-case work remains polynomial O(m^cap) for fixed cap. On the graphic
    fixtures the number of matching half syndromes is much smaller.
    """
    n = len(annihilator_cols)
    halves, grouped = {}, {}
    for size in range((degree_cap + 1) // 2 + 1):
        data, groups = [], defaultdict(list)
        for inds in combinations(range(n), size):
            mask, syndrome = 0, 0
            for e in inds:
                mask |= 1 << e
                syndrome ^= annihilator_cols[e]
            item = (mask, syndrome, inds[0] if inds else n,
                    inds[-1] if inds else -1)
            data.append(item)
            groups[syndrome].append(item)
        halves[size], grouped[size] = data, groups
        counts["half_subsets_generated"] += len(data)
    for size in range(1, degree_cap + 1):
        left, right = size // 2, (size + 1) // 2
        for rm, syndrome, rmin, _ in halves[right]:
            for lm, _, _, lmax in grouped[left].get(syndrome, ()):
                counts["half_pairs_checked"] += 1
                if lmax < rmin:
                    counts["rowspace_words_checked"] += 1
                    yield lm | rm


def acquire_graph(rows, n, degree_cap):
    """Polynomial for fixed cap; returns a fully checked graph certificate."""
    rr = basis(rows)
    annihilator_cols = columns(nullspace(rr, n), n)
    matroid_cols = columns(rr, n)
    cocircuits, stars = [], []
    counts = {"half_subsets_generated": 0, "half_pairs_checked": 0,
              "rowspace_words_checked": 0}
    for mask in small_rowspace_words(annihilator_cols, degree_cap, counts):
        # The rowspace vectors supported in S form a space of dimension
        # r-rank(K restricted to E\S). Since 1_S is already in the rowspace,
        # dimension one is equivalent to support minimality over GF(2).
        if len(basis(r & ~mask for r in rr)) != len(rr) - 1:
            continue
        cocircuits.append(mask)
        if matroid_connected(matroid_cols, removed=mask):
            stars.append(mask)
    edge_vertices = [[v for v, s in enumerate(stars) if (s >> e) & 1]
                     for e in range(n)]
    if any(len(ends) != 2 for ends in edge_vertices):
        return None
    edges = [tuple(ends) for ends in edge_vertices]
    nv = len(stars)
    if nv < 4 or len(set(edges)) != n or any(u == v for u, v in edges):
        return None
    if basis(incidence(nv, edges)) != rr:
        return None
    if not graph_connected(nv, edges):
        return None
    for k in (1, 2):
        for removed in combinations(range(nv), k):
            if not graph_connected(nv, edges, frozenset(removed)):
                return None
    return {"vertices": nv, "edges": edges, "stars": stars,
            "matrix_rank": len(rr), "possible_small_subsets":
                sum(comb(n, k) for k in range(1, degree_cap + 1)),
            "cocircuits_examined": len(cocircuits),
            "rowspace_certificate": list(rr), **counts}


def cycle_from_edges(edges, chosen):
    adj = defaultdict(list)
    for e in bit_members(chosen):
        u, v = edges[e]
        adj[u].append(v)
        adj[v].append(u)
    if len(adj) < 3 or any(len(ns) != 2 for ns in adj.values()):
        return None
    start = min(adj)
    cycle, prev, now = [start], None, start
    while True:
        nxt = next(v for v in adj[now] if v != prev)
        if nxt == start:
            break
        if nxt in cycle:
            return None
        cycle.append(nxt)
        prev, now = now, nxt
    return cycle if len(cycle) == len(adj) else None


def acquire_sphere_embedding(primal, dual):
    """Recover oriented faces from a dual incidence certificate; verify sphere."""
    edges, nv = primal["edges"], primal["vertices"]
    n = len(edges)
    if len(dual["edges"]) != n:
        return None
    faces = [cycle_from_edges(edges, s) for s in dual["stars"]]
    if any(f is None for f in faces) or nv - n + len(faces) != 2:
        return None
    incidences = defaultdict(list)
    edge_id = {tuple(sorted(e)): i for i, e in enumerate(edges)}
    for f, cycle in enumerate(faces):
        for u, v in zip(cycle, cycle[1:] + cycle[:1]):
            e = edge_id[tuple(sorted((u, v)))]
            incidences[e].append((f, 1 if u < v else -1))
    if len(incidences) != n or any(len(x) != 2 for x in incidences.values()):
        return None
    face_adj = [[] for _ in faces]
    for data in incidences.values():
        (f, a), (g, b) = data
        factor = -a * b
        face_adj[f].append((g, factor))
        face_adj[g].append((f, factor))
    signs = {0: 1}
    queue = [0]
    for f in queue:
        for g, factor in face_adj[f]:
            value = signs[f] * factor
            if g in signs and signs[g] != value:
                return None
            if g not in signs:
                signs[g] = value
                queue.append(g)
    if len(signs) != len(faces):
        return None
    faces = [f if signs[i] == 1 else list(reversed(f))
             for i, f in enumerate(faces)]
    successor = [dict() for _ in range(nv)]
    for f in faces:
        for i, v in enumerate(f):
            u, w = f[i - 1], f[(i + 1) % len(f)]
            if u in successor[v] and successor[v][u] != w:
                return None
            successor[v][u] = w
    rotation = {}
    for v, nxt in enumerate(successor):
        start = min(nxt)
        seq, now = [], start
        while now not in seq:
            seq.append(now)
            now = nxt[now]
        if now != start or len(seq) != len(nxt):
            return None
        rotation[v] = seq
    if len(faces_from_rotation(rotation)) != len(faces):
        return None
    return {"rotation": rotation, "faces": faces,
            "euler_characteristic": 2}


def faces_from_rotation(rotation):
    unseen = {(u, v) for u, ns in rotation.items() for v in ns}
    faces = []
    while unseen:
        start = min(unseen)
        u, v = start
        f = []
        while True:
            if (u, v) not in unseen:
                raise ValueError("Invalid rotation walk")
            unseen.remove((u, v))
            f.append((u, v))
            ns = rotation[v]
            w = ns[(ns.index(u) - 1) % len(ns)]
            u, v = v, w
            if (u, v) == start:
                break
        faces.append(f)
    return faces


def fisher_cubic(graph, embedding, weights):
    """High-temperature gadget; nonnegative factors, no identically-zero edge."""
    nv, edges = graph["vertices"], graph["edges"]
    er = {tuple(sorted(e)): i for i, e in enumerate(edges)}
    port, centers, rotation, decorated_weights = {}, {}, {}, {}
    for v in range(nv):
        ns = embedding["rotation"][v]
        if len(ns) != 3:
            raise ValueError("Executed Pfaffian branch is scoped to cubic primal")
        centers[v] = 4 * v
        for i, w in enumerate(ns):
            port[v, w] = 4 * v + i + 1
    for v in range(nv):
        ns = embedding["rotation"][v]
        ps = [port[v, w] for w in ns]
        c = centers[v]
        rotation[c] = ps
        for i, w in enumerate(ns):
            p = ps[i]
            rotation[p] = [port[w, v], ps[(i + 1) % 3], c, ps[(i - 1) % 3]]
            decorated_weights[tuple(sorted((p, c)))] = Q(1)
            decorated_weights[tuple(sorted((p, ps[(i + 1) % 3])))] = Q(1, 3)
    prefactor = Q(2) ** nv
    for e, (u, v) in enumerate(edges):
        w0, w1 = map(Q, weights[e])
        if w0 < 0 or w1 < 0 or w0 + w1 == 0:
            raise ValueError("Nonnegative factor with at least one positive value required")
        a, b = (w0 + w1) / 2, (w0 - w1) / 2
        prefactor *= a
        decorated_weights[tuple(sorted((port[u, v], port[v, u])))] = b / a
    n = 4 * nv
    faces = faces_from_rotation(rotation)
    if n - len(decorated_weights) + len(faces) != 2:
        raise AssertionError("Fisher rotation is not a sphere embedding")
    matching = []
    for v in range(nv):
        ps = [port[v, w] for w in embedding["rotation"][v]]
        matching.extend([(centers[v], ps[0]), (ps[1], ps[2])])
    return n, decorated_weights, faces, prefactor, matching


def kasteleyn_matrix(n, edge_weights, faces):
    """Acquire an odd orientation for each bounded face via a dual tree."""
    keys = sorted(edge_weights)
    index = {e: i for i, e in enumerate(keys)}
    edge_faces = defaultdict(list)
    parity = []
    for f, walk in enumerate(faces):
        count = 0
        for u, v in walk:
            e = index[tuple(sorted((u, v)))]
            edge_faces[e].append(f)
            count ^= int(u < v)
        parity.append(count)
    if any(len(fs) != 2 for fs in edge_faces.values()):
        raise AssertionError("Nonclosed embedding")
    adj = [[] for _ in faces]
    for e, (f, g) in edge_faces.items():
        if f != g:
            adj[f].append((g, e))
            adj[g].append((f, e))
    parent = {0: None}
    order = [0]
    for f in order:
        for g, e in adj[f]:
            if g not in parent:
                parent[g] = (f, e)
                order.append(g)
    if len(order) != len(faces):
        raise AssertionError("Disconnected dual")
    signs = [1] * len(keys)
    for f in reversed(order[1:]):
        g, e = parent[f]
        if parity[f] != 1:
            signs[e] *= -1
            parity[f] ^= 1
            parity[g] ^= 1
    if any(p != 1 for p in parity):
        raise AssertionError("Orientation certificate failed")
    matrix = [[Q(0) for _ in range(n)] for _ in range(n)]
    orientation = {}
    for e, (u, v) in enumerate(keys):
        orientation[u, v] = signs[e]
        matrix[u][v] = signs[e] * edge_weights[u, v]
        matrix[v][u] = -matrix[u][v]
    return matrix, orientation


def pfaffian(matrix):
    a = [r[:] for r in matrix]
    n, result = len(a), Q(1)
    for k in range(0, n, 2):
        p = next((j for j in range(k + 1, n) if a[k][j]), None)
        if p is None:
            return Q(0)
        if p != k + 1:
            a[p], a[k + 1] = a[k + 1], a[p]
            for r in a:
                r[p], r[k + 1] = r[k + 1], r[p]
            result = -result
        pivot = a[k][k + 1]
        result *= pivot
        for i in range(k + 2, n):
            for j in range(i + 1, n):
                a[i][j] -= (a[k][i] * a[k + 1][j] - a[k][j] * a[k + 1][i]) / pivot
                a[j][i] = -a[i][j]
    return result


def matching_orientation_sign(matching, orientation):
    pairs = sorted(tuple(sorted(p)) for p in matching)
    sign = prod(orientation[u, v] for u, v in pairs)
    crossings = sum(u < x < v < y for i, (u, v) in enumerate(pairs)
                    for x, y in pairs[i + 1:])
    return sign * (-1 if crossings & 1 else 1)


def planar_cut_partition(graph, embedding, weights, affine_offset=0):
    if any(Q(w0) == 0 and Q(w1) == 0 for w0, w1 in weights):
        return Q(0), {"pfaffian_dimension": 4 * graph["vertices"],
                      "zero_factor": True}
    adjusted = [tuple(reversed(w)) if ((affine_offset >> e) & 1) else w
                for e, w in enumerate(weights)]
    n, ew, faces, pre, matching = fisher_cubic(graph, embedding, adjusted)
    mat, orientation = kasteleyn_matrix(n, ew, faces)
    pm = matching_orientation_sign(matching, orientation) * pfaffian(mat)
    # Connected graph has exactly two spin representatives for every cut.
    return pre * pm / 2, {"pfaffian_dimension": n, "decorated_edges": len(ew),
                         "orientation_faces": len(faces)}


def minfill_cut_partition(graph, weights, affine_offset=0):
    """Ordinary retained exact binary variable elimination on the same graph."""
    nv, edges = graph["vertices"], graph["edges"]
    factors, adjacency = [], [set() for _ in range(nv)]
    for e, (u, v) in enumerate(edges):
        w = weights[e]
        if (affine_offset >> e) & 1:
            w = w[::-1]
        factors.append(((u, v), (w[0], w[1], w[1], w[0])))
        adjacency[u].add(v)
        adjacency[v].add(u)
    active, width = set(range(nv)), 0
    for _ in range(nv):
        def score(v):
            ns = list(adjacency[v])
            fill = sum(b not in adjacency[a] for a, b in combinations(ns, 2))
            return fill, len(ns), v
        v = min(active, key=score)
        ns = adjacency[v]
        width = max(width, len(ns))
        for a, b in combinations(ns, 2):
            adjacency[a].add(b)
            adjacency[b].add(a)
        for a in ns:
            adjacency[a].remove(v)
        active.remove(v)
        bucket = [f for f in factors if v in f[0]]
        factors = [f for f in factors if v not in f[0]]
        outvars = tuple(sorted({x for vs, _ in bucket for x in vs} - {v}))
        positions = {x: i for i, x in enumerate(outvars)}
        maps = [(tuple(-1 if x == v else positions[x] for x in vs), tab)
                for vs, tab in bucket]
        outtab = []
        for assignment in range(1 << len(outvars)):
            subtotal = Q(0)
            for value in (0, 1):
                term = Q(1)
                for mapping, tab in maps:
                    key = sum((value if p == -1 else (assignment >> p) & 1) << j
                              for j, p in enumerate(mapping))
                    term *= tab[key]
                subtotal += term
            outtab.append(subtotal)
        factors.append((outvars, tuple(outtab)))
    assert all(not vs for vs, _ in factors)
    return prod(tab[0] for _, tab in factors) / 2, width


def dual_enumeration_partition(rows, n, weights, affine_offset=0):
    dual = nullspace(rows, n)
    total = Q(0)
    for mask in range(1 << len(dual)):
        h = 0
        for j in bit_members(mask):
            h ^= dual[j]
        term = Q(-1 if ((h & affine_offset).bit_count() & 1) else 1)
        for e, (w0, w1) in enumerate(weights):
            term *= w0 - w1 if (h >> e) & 1 else w0 + w1
        total += term
    return total / (1 << len(dual))


def brute_cut_partition(rows, n, weights, affine_offset=0):
    rr = basis(rows)
    total = Q(0)
    for mask in range(1 << len(rr)):
        y = affine_offset
        for j in bit_members(mask):
            y ^= rr[j]
        total += prod(weights[e][(y >> e) & 1] for e in range(n))
    return total


def hidden_matrix(nv, edges, seed):
    """Fixture generator only; no graph data is passed to acquire_graph."""
    rr = list(basis(incidence(nv, edges)))
    rng = Random(seed)
    for _ in range(20 * len(rr)):
        i, j = rng.sample(range(len(rr)), 2)
        rr[i] ^= rr[j]
    rng.shuffle(rr)
    return rr


def cube_fixture():
    return 8, [(u, u ^ (1 << b)) for u in range(8) for b in range(3)
               if u < (u ^ (1 << b))]


def truncated_octahedron_fixture():
    # Original octahedron vertices 0/1, 2/3, 4/5 are opposite pairs.
    oe = [(u, v) for u in range(6) for v in range(u + 1, 6) if u // 2 != v // 2]
    directed = [(u, v) for e in oe for u, v in (e, e[::-1])]
    vid = {p: i for i, p in enumerate(directed)}
    edges = {tuple(sorted((vid[u, v], vid[v, u]))) for u, v in oe}
    for u in range(6):
        ns = [v for v in range(6) if u // 2 != v // 2]
        for v, w in combinations(ns, 2):
            if v // 2 != w // 2:
                edges.add(tuple(sorted((vid[u, v], vid[u, w]))))
    return len(directed), sorted(edges)


def truncated_icosahedron_fixture():
    # Icosahedron: two pentagonal rings plus a pole at each end.
    oe = set()
    for i in range(5):
        a, b = 1 + i, 6 + i
        oe.update({(0, a), tuple(sorted((a, 1 + (i + 1) % 5))),
                   (b, 11), tuple(sorted((b, 6 + (i + 1) % 5))),
                   (a, b), (a, 6 + (i - 1) % 5)})
    oe = sorted(oe)
    edge_set = set(oe)
    directed = [(u, v) for e in oe for u, v in (e, e[::-1])]
    vid = {p: i for i, p in enumerate(directed)}
    edges = {tuple(sorted((vid[u, v], vid[v, u]))) for u, v in oe}
    for u in range(12):
        ns = [v for v in range(12) if tuple(sorted((u, v))) in edge_set]
        for v, w in combinations(ns, 2):
            if tuple(sorted((v, w))) in edge_set:
                edges.add(tuple(sorted((vid[u, v], vid[u, w]))))
    return len(directed), sorted(edges)


def run_case(name, fixture, dual_cap):
    nv, source_edges = fixture()
    m = len(source_edges)
    rows = hidden_matrix(nv, source_edges, 191 + nv)
    start = perf_counter()
    graph = acquire_graph(rows, m, 3)
    primal_time = perf_counter() - start
    assert graph is not None
    start = perf_counter()
    dual = acquire_graph(nullspace(rows, m), m, dual_cap)
    assert dual is not None
    embedding = acquire_sphere_embedding(graph, dual)
    assert embedding is not None
    planar_time = perf_counter() - start
    couplings = [(-2, -1, 1, 2, 3)[e % 5] for e in range(m)]
    weights = [(Q(2) ** -j, Q(2) ** j) for j in couplings]
    offset = (1 << 0) | (1 << (m - 1))
    start = perf_counter()
    z, stats = planar_cut_partition(graph, embedding, weights, offset)
    pf_time = perf_counter() - start
    start = perf_counter()
    ve_value, ve_width = minfill_cut_partition(graph, weights, offset)
    ve_time = perf_counter() - start
    assert z == ve_value
    baseline_time = None
    if m - len(rows) <= 18:
        start = perf_counter()
        expected = dual_enumeration_partition(rows, m, weights, offset)
        baseline_time = perf_counter() - start
        assert z == expected
    if len(rows) <= 10:
        assert z == brute_cut_partition(rows, m, weights, offset)
        # A first-face inconsistent parity clamp must have exactly zero mass.
        clamped = list(weights)
        face = embedding["faces"][0]
        edge_id = {tuple(sorted(e)): i for i, e in enumerate(graph["edges"])}
        for k, (u, v) in enumerate(zip(face, face[1:] + face[:1])):
            e = edge_id[tuple(sorted((u, v)))]
            value = int(k == 0)  # odd xor around a cycle
            clamped[e] = tuple(w if b == value else Q(0) for b, w in enumerate(weights[e]))
        assert planar_cut_partition(graph, embedding, clamped)[0] == 0
        # A compatible clamp is checked against brute force as well.
        clamped = list(weights)
        clamped[0] = (weights[0][0], Q(0))
        assert planar_cut_partition(graph, embedding, clamped, offset)[0] == brute_cut_partition(rows, m, clamped, offset)
    # Known nongraphic Fano input must not become a false graph certificate.
    fano = [0b1010101, 0b1100110, 0b1111000]
    assert acquire_graph(fano, 7, 3) is None
    return {"case": name, "vertices": nv, "terms": m, "rank": len(basis(rows)),
            "d": m - len(basis(rows)), "hidden_matrix_mean_row_weight":
                sum(r.bit_count() for r in rows) / len(rows),
            "primal_acquisition_s": primal_time,
            "planar_embedding_acquisition_s": planar_time,
            "pfaffian_execution_s": pf_time, "dual_enumeration_s": baseline_time,
            "minfill_elimination_s": ve_time, "minfill_width": ve_width,
            "primal_half_subsets_paid": graph["half_subsets_generated"],
            "dual_half_subsets_paid": dual["half_subsets_generated"],
            "primal_half_pairs_paid": graph["half_pairs_checked"],
            "dual_half_pairs_paid": dual["half_pairs_checked"],
            "exact_partition": str(z), "verified": True, **stats}


if __name__ == "__main__":
    results = [run_case("hidden_cube", cube_fixture, 4),
               run_case("hidden_truncated_octahedron", truncated_octahedron_fixture, 6),
               run_case("hidden_truncated_icosahedron", truncated_icosahedron_fixture, 6)]
    print(json.dumps(results, indent=2))
