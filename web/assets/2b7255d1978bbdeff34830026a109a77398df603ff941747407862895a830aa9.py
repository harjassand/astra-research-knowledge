"""Exact support-compressed cycle rounding for bipartite PM marginals.

This is a proof-of-concept compiler.  Its signing routine is deliberately an
injected primitive; Li's 99-signing theorem is source-reported, not
implemented here.  All other operations use exact ``Fraction`` arithmetic.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import isqrt
from typing import Callable, Sequence

Edge = tuple[int, int]
Vec = tuple[Fraction, ...]
Signer = Callable[[Sequence[Vec]], Sequence[int]]


@dataclass(frozen=True)
class Atom:
    numerator: tuple[int, ...]
    weight: Fraction
    bound: Fraction
    scales: tuple[tuple[int, int], ...]


def _vertices(nl: int, e: Edge) -> tuple[int, int]:
    return e[0], nl + e[1]


def _cycle(nv: int, nl: int, edges: Sequence[Edge], active: Sequence[int]):
    """Return one simple cycle in edge-ID order, or None."""
    adj: list[list[tuple[int, int]]] = [[] for _ in range(nv)]
    for eid in active:
        u, v = _vertices(nl, edges[eid])
        adj[u].append((eid, v))
        adj[v].append((eid, u))
    state = [0] * nv
    parent = [-1] * nv
    parent_edge = [-1] * nv
    for root in range(nv):
        if state[root]:
            continue
        state[root] = 1
        stack = [(root, 0)]
        while stack:
            u, i = stack[-1]
            if i == len(adj[u]):
                state[u] = 2
                stack.pop()
                continue
            eid, v = adj[u][i]
            stack[-1] = (u, i + 1)
            if eid == parent_edge[u]:
                continue
            if state[v] == 0:
                state[v] = 1
                parent[v], parent_edge[v] = u, eid
                stack.append((v, 0))
            elif state[v] == 1:
                path = []
                z = u
                while z != v:
                    if z < 0 or parent[z] < 0:
                        raise ArithmeticError("DFS back edge did not close")
                    path.append(parent_edge[z])
                    z = parent[z]
                return tuple(list(reversed(path)) + [eid])
    return None


def _null_vector(points: Sequence[Vec]) -> list[Fraction]:
    """Find a nonzero rational affine dependence among > d+1 points in Q^d."""
    k = len(points)
    d = len(points[0]) if points else 0
    a = [[Fraction(1) for _ in range(k)]]
    a.extend([[points[j][i] for j in range(k)] for i in range(d)])
    pivot_cols: list[int] = []
    row = 0
    for col in range(k):
        pivot = next((r for r in range(row, len(a)) if a[r][col]), None)
        if pivot is None:
            continue
        a[row], a[pivot] = a[pivot], a[row]
        q = a[row][col]
        a[row] = [v / q for v in a[row]]
        for r in range(len(a)):
            if r != row and a[r][col]:
                q = a[r][col]
                a[r] = [u - q * v for u, v in zip(a[r], a[row])]
        pivot_cols.append(col)
        row += 1
        if row == len(a):
            break
    free = next((j for j in range(k) if j not in pivot_cols), None)
    if free is None:
        raise ArithmeticError("no affine dependence despite excess support")
    lam = [Fraction(0)] * k
    lam[free] = Fraction(1)
    for r, col in reversed(list(enumerate(pivot_cols))):
        lam[col] = -sum((a[r][j] * lam[j] for j in range(k) if j != col), Fraction(0))
    if not any(lam) or sum(lam, Fraction(0)) != 0:
        raise ArithmeticError("invalid affine dependence")
    return lam


def _compress(
    candidates: list[tuple[Vec, Fraction, object]], target: Vec
) -> list[tuple[Vec, Fraction, object]]:
    """Compress a feasible rational law to <=d+1 existing atoms, exactly."""
    d = len(target)
    if any(len(point) != d for point, _, _ in candidates):
        raise ValueError("candidate and target dimensions differ")
    candidates = [(v, w, tag) for v, w, tag in candidates if w > 0]
    if sum((w for _, w, _ in candidates), Fraction(0)) != 1:
        raise ArithmeticError("candidate weights do not sum to one")
    for j in range(d):
        if sum((w * v[j] for v, w, _ in candidates), Fraction(0)) != target[j]:
            raise ArithmeticError("candidate law does not have the requested mean")
    while len(candidates) > d + 1:
        pts = [v for v, _, _ in candidates]
        lam = _null_vector(pts)
        step = min(
            w / z
            for (_, w, _), z in zip(candidates, lam)
            if z > 0
        )
        updated = []
        for (v, w, tag), z in zip(candidates, lam):
            new_weight = w - step * z
            if new_weight > 0:
                updated.append((v, new_weight, tag))
        candidates = updated
    if sum((w for _, w, _ in candidates), Fraction(0)) != 1:
        raise ArithmeticError("compression changed total mass")
    for j in range(d):
        if sum((w * v[j] for v, w, _ in candidates), Fraction(0)) != target[j]:
            raise ArithmeticError("compression changed the barycenter")
    return candidates


def _ceil_norm(v: Vec) -> int:
    q = sum((x * x for x in v), Fraction(0))
    if q == 0:
        return 0
    u = isqrt(q.numerator // q.denominator)
    return u if u * u * q.denominator == q.numerator else u + 1


def _residual_endpoint_round(
    nl: int,
    nr: int,
    edges: Sequence[Edge],
    x: Vec,
    level: int,
) -> list[tuple[tuple[int, ...], Fraction]]:
    """Return a support-<=m+1 law of 2^level b-matchings with mean x."""
    m = len(edges)
    q = 1 << level
    floors = tuple((q * z).numerator // (q * z).denominator for z in x)
    start = tuple(q * z - f for z, f in zip(x, floors))
    law: list[tuple[Vec, Fraction, object]] = [(start, Fraction(1), None)]
    for _ in range(m):
        max_fractional = max(
            (sum(0 < z < 1 for z in point) for point, _, _ in law),
            default=0,
        )
        if max_fractional == 0:
            break
        branches = []
        for point, weight, _ in law:
            active = [e for e, z in enumerate(point) if 0 < z < 1]
            if not active:
                branches.append((point, weight, None))
                continue
            cyc = _cycle(nl + nr, nl, edges, active)
            if cyc is None or len(cyc) % 2:
                raise ArithmeticError("integer residual degrees require an even cycle")
            direction = tuple(1 if i % 2 == 0 else -1 for i in range(len(cyc)))
            lo = max((-point[e] if s > 0 else point[e] - 1) for e, s in zip(cyc, direction))
            hi = min((1 - point[e] if s > 0 else point[e]) for e, s in zip(cyc, direction))
            if not lo < 0 < hi:
                raise ArithmeticError("cycle has no two-sided feasible interval")
            p_lo = hi / (hi - lo)
            for step, prob in ((lo, p_lo), (hi, 1 - p_lo)):
                nxt = list(point)
                for e, s in zip(cyc, direction):
                    nxt[e] += step * s
                nxt = tuple(nxt)
                if any(not 0 <= z <= 1 for z in nxt):
                    raise ArithmeticError("endpoint branch left the unit cube")
                if sum(0 < z < 1 for z in nxt) >= sum(0 < z < 1 for z in point):
                    raise ArithmeticError("endpoint branch failed to freeze an edge")
                branches.append((nxt, weight * prob, None))
        law = _compress(branches, start)
    if any(any(0 < z < 1 for z in point) for point, _, _ in law):
        raise ArithmeticError("residual rounding exceeded |E| rounds")
    out = []
    for point, weight, _ in law:
        if any(z not in (0, 1) for z in point):
            raise ArithmeticError("nonintegral residual endpoint")
        y = tuple(f + int(z) for f, z in zip(floors, point))
        out.append((y, weight))
    return out


def _cycles_of_eulerian_support(nl: int, nr: int, edges: Sequence[Edge], active: Sequence[int]):
    remaining = set(active)
    cycles = []
    while remaining:
        cyc = _cycle(nl + nr, nl, edges, sorted(remaining))
        if cyc is None or len(cyc) % 2:
            raise ArithmeticError("odd support graph is not bipartite Eulerian")
        cycles.append(cyc)
        remaining.difference_update(cyc)
    return cycles


def sparse_bipartite_matching_law(
    nl: int,
    nr: int,
    edges: Sequence[Edge],
    marginals: Sequence[Fraction],
    feature_columns: Sequence[Sequence[Fraction]],
    level: int,
    signer: Signer,
) -> tuple[Atom, ...]:
    """Compile a rational PM point into <=m+1 exact-marginal safe atoms.

    Preconditions: bipartite graph, nl=nr, feasible rational PM marginals,
    rational feature columns of Euclidean norm <=1, and a signer satisfying
    the <99 Li guarantee on rational unit columns.  No optimization or
    matching-polytope oracle is used.
    """
    if nl != nr or nl < 1 or level < 0:
        raise ValueError("need equal nonempty shores and nonnegative level")
    m = len(edges)
    if len(marginals) != m or len(feature_columns) != m:
        raise ValueError("edge, marginal, and feature counts differ")
    x = tuple(Fraction(z) for z in marginals)
    A = tuple(tuple(Fraction(z) for z in col) for col in feature_columns)
    d = len(A[0]) if A else 0
    if any(len(col) != d for col in A):
        raise ValueError("feature columns must have a common dimension")
    if any(sum((z * z for z in col), Fraction(0)) > 1 for col in A):
        raise ValueError("feature columns must have Euclidean norm <=1")
    deg = [Fraction(0)] * (nl + nr)
    for (l, r), z in zip(edges, x):
        if not (0 <= l < nl and 0 <= r < nr) or not 0 <= z <= 1:
            raise ValueError("invalid actual edge or marginal")
        deg[l] += z
        deg[nl + r] += z
    if any(z != 1 for z in deg):
        raise ValueError("marginals must satisfy the bipartite PM degree equations")

    q = 1 << level
    initial = _residual_endpoint_round(nl, nr, edges, x, level)
    law = [Atom(y, w, Fraction(m, q), ()) for y, w in initial]
    for t in range(level, 0, -1):
        candidates = []
        for atom in law:
            odd = [e for e, z in enumerate(atom.numerator) if z % 2]
            if not odd:
                half = tuple(z // 2 for z in atom.numerator)
                candidates.append((tuple(Fraction(z, 1 << (t - 1)) for z in half), atom.weight,
                                   Atom(half, atom.weight, atom.bound, atom.scales + ((t, 0),))))
                continue
            cycles = _cycles_of_eulerian_support(nl, nr, edges, odd)
            cycle_vectors = []
            directions = []
            for cyc in cycles:
                delta = [0] * m
                for i, e in enumerate(cyc):
                    delta[e] = 1 if i % 2 == 0 else -1
                directions.append(tuple(delta))
                cycle_vectors.append(tuple(
                    sum((delta[e] * A[e][j] for e in range(m)), Fraction(0))
                    for j in range(d)
                ))
            scale = max((_ceil_norm(v) for v in cycle_vectors), default=0)
            if scale == 0:
                signs = (1,) * len(cycles)
            else:
                normalized = tuple(tuple(z / scale for z in v) for v in cycle_vectors)
                signs = tuple(signer(normalized))
                if len(signs) != len(cycles) or any(s not in (-1, 1) for s in signs):
                    raise ValueError("signer returned an invalid sign vector")
                signed = tuple(
                    sum((s * v[j] for s, v in zip(signs, cycle_vectors)), Fraction(0))
                    for j in range(d)
                )
                if any(abs(z) >= 99 * scale for z in signed):
                    raise ValueError("signer failed the strict <99 guarantee")
            signed_direction = tuple(
                sum((s * delta[e] for s, delta in zip(signs, directions)), 0)
                for e in range(m)
            )
            for orientation in (-1, 1):
                updated = tuple(
                    (z + orientation * dlt) // 2
                    for z, dlt in zip(atom.numerator, signed_direction)
                )
                if any((z + orientation * dlt) % 2 for z, dlt in zip(atom.numerator, signed_direction)):
                    raise ArithmeticError("odd-edge perturbation did not become even")
                if any(z < 0 for z in updated):
                    raise ArithmeticError("antipodal cycle branch left the feasible cone")
                next_bound = atom.bound + Fraction(99 * scale, 1 << t)
                child = Atom(updated, atom.weight / 2, next_bound,
                             atom.scales + ((t, scale),))
                candidates.append((tuple(Fraction(z, 1 << (t - 1)) for z in updated),
                                   atom.weight / 2, child))
        compressed = _compress(candidates, x)
        law = [tag for _, _, tag in compressed]
        # The target weights returned by compression replace, rather than
        # recursively enumerate, the branch weights stored in each tag.
        law = [Atom(a.numerator, w, a.bound, a.scales) for (_, w, _), a in zip(compressed, law)]

    final = []
    for atom in law:
        y = atom.numerator
        if any(z not in (0, 1) for z in y):
            raise ArithmeticError("final state is not a perfect matching")
        # Verify every degree and compute the exact feature error.
        dcheck = [0] * (nl + nr)
        for (l, r), z in zip(edges, y):
            dcheck[l] += z
            dcheck[nl + r] += z
        if any(z != 1 for z in dcheck):
            raise ArithmeticError("final state violates matching degrees")
        error = tuple(
            sum((A[e][j] * (y[e] - x[e]) for e in range(m)), Fraction(0))
            for j in range(d)
        )
        actual_error = max((abs(z) for z in error), default=Fraction(0))
        if actual_error > atom.bound:
            raise ArithmeticError("atom exceeded its charged cycle bound")
        final.append((y, atom.weight, atom.bound, atom.scales))
    if len(final) > m + 1:
        raise ArithmeticError("support compression exceeded |E|+1")
    if sum((w for _, w, _, _ in final), Fraction(0)) != 1:
        raise ArithmeticError("final law does not have unit mass")
    for e in range(m):
        if sum((w * y[e] for y, w, _, _ in final), Fraction(0)) != x[e]:
            raise ArithmeticError("final law failed an exact edge marginal")
    # Merge repeated matching incidence vectors so the returned list is the
    # actual support, rather than a list with repeated copies of one atom.
    merged: dict[tuple[int, ...], tuple[Fraction, Fraction, tuple[tuple[int, int], ...]]] = {}
    for y, w, b, s in final:
        if y in merged:
            old_w, old_b, old_s = merged[y]
            if b > old_b:
                merged[y] = (old_w + w, b, s)
            else:
                merged[y] = (old_w + w, old_b, old_s)
        else:
            merged[y] = (w, b, s)
    return tuple(Atom(y, w, b, s) for y, (w, b, s) in merged.items())
