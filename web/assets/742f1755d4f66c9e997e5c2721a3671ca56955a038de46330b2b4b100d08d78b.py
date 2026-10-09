#!/usr/bin/env python3
"""Exact, standard-library-only certificate for the double-windmill star-union construction.

The certificate establishes a restricted auxiliary counterexample, NOT a
counterexample to Frankl's union-closed sets conjecture.

Run: python3 certificate.py
"""
from collections import Counter
from fractions import Fraction


def construction(k):
    assert k >= 1
    # Central vertices are 0=u and 1=v. Each petal is a triangle.
    edges = [(0, 1)]
    for hub in (0, 1):
        for i in range(k):
            a = 2 + 2 * k * hub + 2 * i
            b = a + 1
            edges.extend(((hub, a), (hub, b), (a, b)))
    vertices = 4 * k + 2
    assert len(edges) == 6 * k + 1
    assert len(set(tuple(sorted(e)) for e in edges)) == len(edges)
    return vertices, edges


def exact_counts_from_generators(k):
    n, edges = construction(k)
    stars = [0] * n
    for j, (u, v) in enumerate(edges):
        stars[u] |= 1 << j
        stars[v] |= 1 << j
    # Every ground element occurs in exactly two generators.
    assert all(sum(bool(star & (1 << j)) for star in stars) == 2
               for j in range(len(edges)))
    # All generators form an antichain (hence an irredundant system).
    assert all(not (stars[a] & ~stars[b] == 0)
               for a in range(n) for b in range(n) if a != b)
    # Enumerate all unions of the stars, independently of the graph method.
    family = {0}
    for s in stars:
        family |= {A | s for A in family}
    central = sum(bool(A & 1) for A in family)
    # The first triangle-internal edge is index 3. This is abundant.
    internal = sum(bool(A & (1 << 3)) for A in family)
    return stars, family, central, internal


def exact_counts_from_isolate_free_subsets(k):
    n, edges = construction(k)
    nbr = [0] * n
    for a, b in edges:
        nbr[a] |= 1 << b
        nbr[b] |= 1 << a
    isofree = []
    for mask in range(1 << n):
        if all(not (mask & (1 << v)) or mask & nbr[v]
               for v in range(n)):
            isofree.append(mask)
    both_hubs = sum(mask & 3 == 3 for mask in isofree)
    # Independent direct verification of each closure-member complement
    # via induced edges of the corresponding isolated-vertex-free set.
    induced_edge_sets = set()
    for mask in isofree:
        induced_edge_sets.add(sum(1 << j for j, (a, b) in enumerate(edges)
                                  if mask & (1 << a) and mask & (1 << b)))
    assert len(induced_edge_sets) == len(isofree)
    return isofree, both_hubs, induced_edge_sets


def main():
    for k in (1, 2, 3, 4):
        n, edges = construction(k)
        stars, family, central, internal = exact_counts_from_generators(k)
        iso, both, induced = exact_counts_from_isolate_free_subsets(k)
        formula_n = 16**k + 2*8**k + 4**k - 2**(k+1)
        formula_central = 2*8**k + 4**k - 2**(k+1)
        assert len(family) == len(iso) == len(induced) == formula_n
        assert both == 16**k
        assert central == formula_central == len(family) - both
        assert internal * 2 >= len(family)  # Exhibit an abundant element.
        universe = (1 << len(edges)) - 1
        assert {universe ^ A for A in family} == induced
        if k <= 2:
            # Redundant but independent check of closure under every pairwise union.
            assert all(A | B in family for A in family for B in family)
        print(f'k={k}: graph_vertices={n}, ground_edges={len(edges)}, '
              f'generator_count={len(stars)}, |family|={len(family)}, '
              f'central_frequency={central}, central_fraction={Fraction(central,len(family))}, '
              f'triangle_edge_frequency={internal}, both_hubs={both}, VERIFIED')
    print('PASS: all finite checks, incidence checks, antichain checks, and formulas agree.')
    print('NOTE: original Frankl conjecture is NOT refuted; triangle-internal edges are abundant.')


if __name__ == '__main__':
    main()
