#!/usr/bin/env python3
"""Exact Fraction checker for the positive-rational endotactic lift.

The pointwise comparison works in any finite dimension and at any rational
direction.  The exhaustive fan check is exact for d=2: it checks one rational
representative of every open arrangement sector, every boundary ray, and the
origin.  The general proof in the accompanying note is what covers all real
directions and dimensions.
"""

from dataclasses import dataclass
from fractions import Fraction as F
from functools import cmp_to_key
from itertools import product
from math import gcd, lcm

Vec = tuple[F, ...]


def vec(xs):
    return tuple(F(x) for x in xs)


def add(*xs):
    if not xs:
        return ()
    return tuple(sum((x[j] for x in xs), F(0)) for j in range(len(xs[0])))


def sub(x, y):
    return tuple(a - b for a, b in zip(x, y))


def neg(x):
    return tuple(-a for a in x)


def dot(x, y):
    return sum((a * b for a, b in zip(x, y)), F(0))


@dataclass(frozen=True)
class Edge:
    name: str
    nu: Vec
    P: tuple[Vec, ...]
    Q: tuple[Vec, ...]


def validate(edges):
    if not edges:
        raise ValueError("the finite edge set must be nonempty")
    d = len(edges[0].nu)
    for e in edges:
        if len(e.nu) != d or not e.P or not e.Q:
            raise ValueError("all vectors need one dimension; supports are nonempty")
        if any(len(x) != d for x in (*e.P, *e.Q)):
            raise ValueError("support exponent dimension mismatch")
        if len(set(e.P)) != len(e.P) or len(set(e.Q)) != len(e.Q):
            raise ValueError("supports must be canonicalized (merge duplicate exponents)")
    return d


def lifted_edges(edges):
    """Return all labelled monomial arrows (parent edge index, source, term tag).

    Positive coefficients are omitted because they do not change support or
    any directional source comparison.  Repeated source vectors are retained.
    """
    d = validate(edges)
    out = []
    for i, e in enumerate(edges):
        other_Q = [f.Q for j, f in enumerate(edges) if j != i]
        for choices in product(e.P, *other_Q):
            gamma = add(*choices)
            tag = tuple(choices)
            out.append((i, gamma, tag))
    assert out and all(len(gamma) == d for _, gamma, _ in out)
    return out


def min_dot(r, support):
    return min(dot(r, alpha) for alpha in support)


def tropical_endotactic(edges, r):
    active = [i for i, e in enumerate(edges) if dot(r, e.nu) != 0]
    if not active:
        return True
    tau = {
        i: min_dot(r, edges[i].P) - min_dot(r, edges[i].Q)
        for i in active
    }
    best = min(tau.values())
    # The session's sign convention: minimum-tau active edges must have r.nu>0.
    return all(dot(r, edges[i].nu) > 0 for i in active if tau[i] == best)


def lifted_endotactic(edges, r):
    """Ordinary N33 essential-source condition, tested at w=-r."""
    w = neg(r)
    lifted = lifted_edges(edges)
    active = [row for row in lifted if dot(w, edges[row[0]].nu) != 0]
    if not active:
        return True
    top = max(dot(w, gamma) for _, gamma, _ in active)
    return all(
        dot(w, edges[i].nu) < 0
        for i, gamma, _ in active
        if dot(w, gamma) == top
    )


def verify_direction(edges, r):
    """Check the source-minimum identity and Boolean criterion equivalence."""
    r = vec(r)
    validate(edges)
    if len(r) != len(edges[0].nu):
        raise ValueError("direction dimension mismatch")
    lifted = lifted_edges(edges)
    C = sum((min_dot(r, e.Q) for e in edges), F(0))
    for i, e in enumerate(edges):
        got = min(dot(r, gamma) for j, gamma, _ in lifted if j == i)
        expected = (
            min_dot(r, e.P)
            + sum((min_dot(r, f.Q) for j, f in enumerate(edges) if j != i), F(0))
        )
        tau_plus_C = min_dot(r, e.P) - min_dot(r, e.Q) + C
        assert got == expected == tau_plus_C, (e.name, r, got, expected, tau_plus_C)
    tropical = tropical_endotactic(edges, r)
    ordinary = lifted_endotactic(edges, r)
    assert tropical == ordinary, (r, tropical, ordinary)
    return tropical


def normalize_ray(v):
    """Primitive integer representative of a nonzero rational ray."""
    den = 1
    for x in v:
        den = lcm(den, x.denominator)
    ints = [int(x * den) for x in v]
    g = 0
    for x in ints:
        g = gcd(g, abs(x))
    if g == 0:
        raise ValueError("zero is not a ray")
    return tuple(F(x // g) for x in ints)


def half_plane(v):
    return 0 if (v[1] > 0 or (v[1] == 0 and v[0] >= 0)) else 1


def compare_angle(u, v):
    hu, hv = half_plane(u), half_plane(v)
    if hu != hv:
        return -1 if hu < hv else 1
    cross = u[0] * v[1] - u[1] * v[0]
    if cross > 0:
        return -1
    if cross < 0:
        return 1
    return 0


def arrangement_rays_2d(edges):
    """All distinct rays cut out by support/sign/order hyperplanes.

    Include reaction-sign forms nu; all within-factor support differences;
    and every possible tau linear-piece difference
    (alpha-beta)-(alpha'-beta').  This over-refines the actual fan, safely.
    """
    if validate(edges) != 2:
        raise ValueError("the exhaustive arrangement implementation is for d=2")
    normals = set()
    for e in edges:
        normals.add(e.nu)
        for support in (e.P, e.Q):
            for a, b in product(support, repeat=2):
                normals.add(sub(a, b))
    pieces = []
    for e in edges:
        pieces.extend(sub(a, b) for a in e.P for b in e.Q)
    for a, b in product(pieces, repeat=2):
        normals.add(sub(a, b))

    rays = set()
    for a in normals:
        if a == (F(0), F(0)):
            continue
        r = normalize_ray((-a[1], a[0]))
        rays.add(r)
        rays.add(neg(r))
    return sorted(rays, key=cmp_to_key(compare_angle))


def exhaustive_all_directions_2d(edges):
    """Exact all-real-direction verdict for a rational 2D finite network."""
    rays = arrangement_rays_2d(edges)
    tested = {vec((0, 0))}
    if not rays:
        tested.update((vec((1, 0)), vec((0, 1))))
    else:
        tested.update(rays)
        for j, u in enumerate(rays):
            v = rays[(j + 1) % len(rays)]
            cross = u[0] * v[1] - u[1] * v[0]
            if cross > 0:
                interior = add(u, v)
            elif cross == 0 and dot(u, v) < 0:
                # The sole-line case gives a half-plane of angle pi.
                interior = (-u[1], u[0])
            else:
                raise AssertionError(("bad cyclic ray order", u, v, cross))
            tested.add(interior)
    verdicts = {verify_direction(edges, r) for r in tested}
    # Boolean property is constant on every tested face/cell; a network is
    # all-direction tropically endotactic iff every cell verdict is true.
    return all(verdicts), len(tested), len(rays)


def count_duplicate_sources(edges):
    rows = lifted_edges(edges)
    all_dupes = len(rows) - len({gamma for _, gamma, _ in rows})
    within_parent = sum(
        max(0, sum(i == j for j, _, _ in rows) - len({g for j, g, _ in rows if j == i}))
        for i in range(len(edges))
    )
    return all_dupes, within_parent


def grid_directions_2d(radius=3):
    return [vec((i, j)) for i in range(-radius, radius + 1)
            for j in range(-radius, radius + 1)]


def main():
    q_common = (vec((0, 0)), vec((1, 0)), vec((0, 1)))
    birth_death = [
        Edge("birth-X", vec((1, 0)), (vec((0, 0)),), q_common),
        Edge("death-X", vec((-1, 0)), (vec((1, 0)),), q_common),
    ]
    tie_and_collision = [
        Edge("plus-X", vec((1, 0)), (vec((0, 0)), vec((1, 0))), q_common),
        Edge("minus-X", vec((-1, 0)), (vec((0, 0)), vec((1, 0))), q_common),
        Edge("plus-Y", vec((0, 1)), (vec((0, 0)), vec((0, 1))), q_common),
    ]

    for r in grid_directions_2d(3):
        verify_direction(birth_death, r)
        verify_direction(tie_and_collision, r)

    pass_result = exhaustive_all_directions_2d(birth_death)
    collision_result = exhaustive_all_directions_2d(tie_and_collision)
    all_dupes, within_parent = count_duplicate_sources(tie_and_collision)
    assert pass_result[0] is True
    assert collision_result[0] is False
    assert all_dupes > 0 and within_parent > 0

    # Exact edge cases: support ties, a tau tie between active opposite arrows,
    # a neutral third reaction, and a direction where every reaction is neutral.
    assert verify_direction(tie_and_collision, vec((0, 1))) is True
    assert verify_direction(tie_and_collision, vec((1, 0))) is False
    assert verify_direction(tie_and_collision, vec((0, 0))) is True

    print("PASS: exact source-minimum identities and ordinary/tropical criteria agree")
    print(f"PASS: finite grid comparisons={2 * len(grid_directions_2d(3))}")
    print(f"PASS: 2D all-direction fan birth/death={pass_result}")
    print(f"PASS: 2D all-direction fan tie/collision fixture={collision_result}")
    print(f"PASS: duplicate lifted source occurrences={all_dupes}; within-parent collisions={within_parent}")
    print("Status: exact finite checks of these rational fixtures; universal claim rests on the written algebraic proof.")


if __name__ == "__main__":
    main()
