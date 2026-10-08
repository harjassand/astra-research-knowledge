#!/usr/bin/env python3
"""Exact prime-field replay for the Cycle 6 shared-color construction."""

from itertools import product
import json


def first_good_t(q):
    return next(t for t in range(1, q) if (t * t) % q != 1)


def verify(q, D):
    t = first_good_t(q)
    ti = pow(t, -1, q)
    eps = {0: 0, 1: 0, 2: 1, 3: 1, 4: 0, 5: 0, 6: 1}

    # Each block is a list of (label, alpha, beta, orientation, offset).
    # The three blocks overlap in a nontrivial cycle of shared labels.
    blocks = [
        [(0, 0, 0, "alpha", 0), (1, 0, 1, "alpha", 0),
         (2, 1, 0, "alpha", 0), (3, 1, 1, "alpha", 0)],
        [(2, 0, 0, "beta", 1), (3, 1, 0, "beta", 1),
         (4, 0, 1, "beta", 1), (5, 1, 1, "beta", 1)],
        [(0, 1, 0, "alpha", 1), (2, 0, 0, "alpha", 1),
         (4, 1, 1, "alpha", 1), (6, 0, 1, "alpha", 1)],
    ]

    def scalar_x(i, u, v):
        return ti if (eps[i] + u + v) % 2 == 0 else 1

    triangle_count = 0
    for block in blocks:
        seen = set()
        for i, alpha, beta, orientation, offset in block:
            assert (alpha, beta) not in seen
            seen.add((alpha, beta))
            assert eps[i] == ((alpha if orientation == "alpha" else beta) + offset) % 2
            for u, v in product(range(2), repeat=2):
                x = scalar_x(i, u, v)
                j = (alpha + v) % 2
                k = (beta + u) % 2
                if orientation == "alpha":
                    l = t if (u + j + offset) % 2 == 0 else 1
                    r = 1
                else:
                    l = 1
                    r = ti if (v + k + offset) % 2 == 0 else 1
                assert (l * x * pow(r, -1, q)) % q == 1
                triangle_count += 1
        assert seen == set(product(range(2), repeat=2))

    rectangle_count = 0
    rectangle_scalars = set()
    for i in eps:
        for u, up, v, vp in product(range(2), repeat=4):
            if u == up or v == vp:
                continue
            w = (scalar_x(i, u, v)
                 * pow(scalar_x(i, up, v), -1, q)
                 * scalar_x(i, up, vp)
                 * pow(scalar_x(i, u, vp), -1, q)) % q
            assert (1 - w) % q != 0
            assert w in (pow(t, 2, q), pow(t, -2, q))
            rectangle_scalars.add(w)
            rectangle_count += 1

    return {
        "field": f"F_{q}",
        "t": t,
        "dimension": D,
        "blocks": len(blocks),
        "distinct_labels": len(eps),
        "shared_triangle_equations": triangle_count,
        "ordered_rectangles": rectangle_count,
        "rectangle_scalars": sorted(rectangle_scalars),
        "rank_I_minus_W": D,
    }


def build_prime_block(p, labels, epsilon, orientation, offset):
    """Build a bijection F_p^2 whose chosen coordinate is epsilon+offset."""
    fibers = {e: [] for e in range(p)}
    for i in labels:
        fibers[epsilon[i]].append(i)
    assert all(len(fibers[e]) == p for e in range(p))
    coordinates = {}
    for e in range(p):
        chosen = (e - offset) % p
        for other, i in enumerate(sorted(fibers[e])):
            coordinates[i] = ((chosen, other) if orientation == "alpha"
                              else (other, chosen))
    assert len(set(coordinates.values())) == p * p
    return (labels, coordinates, orientation, offset)


def verify_odd_prime_coloring(q, p, zeta, D):
    """Replay three overlapping p-by-p blocks over a prime coefficient field."""
    assert pow(zeta, p, q) == 1
    assert all(pow(zeta, k, q) != 1 for k in range(1, p))
    epsilon = {i: i % p for i in range(2 * p * p)}
    blocks = [
        build_prime_block(p, list(range(p * p)), epsilon, "alpha", 0),
        build_prime_block(p, list(range(p * p // 2, 3 * p * p // 2)),
                          epsilon, "beta", 1),
        build_prime_block(p, list(range(p * p, 2 * p * p)),
                          epsilon, "alpha", 2 % p),
    ]

    def scalar_x(i, u, v):
        exponent = (epsilon[i] + u + v) % p
        return pow(zeta, exponent * exponent, q)

    triangle_count = 0
    for labels, coords, orientation, offset in blocks:
        assert len(coords) == p * p
        for i in labels:
            alpha, beta = coords[i]
            for u, v in product(range(p), repeat=2):
                x = scalar_x(i, u, v)
                j = (alpha + v) % p
                k = (beta + u) % p
                if orientation == "alpha":
                    exponent = -((j + offset + u) % p) ** 2
                    l = pow(zeta, exponent, q)
                    r = 1
                else:
                    l = 1
                    exponent = ((k + offset + v) % p) ** 2
                    r = pow(zeta, exponent, q)
                assert (l * x * pow(r, -1, q)) % q == 1
                triangle_count += 1

    rectangle_count = 0
    rectangle_scalars = set()
    for i in epsilon:
        for u, up, v, vp in product(range(p), repeat=4):
            if u == up or v == vp:
                continue
            w = (scalar_x(i, u, v)
                 * pow(scalar_x(i, up, v), -1, q)
                 * scalar_x(i, up, vp)
                 * pow(scalar_x(i, u, vp), -1, q)) % q
            exponent = (2 * (up - u) * (vp - v)) % p
            assert w == pow(zeta, exponent, q)
            assert exponent != 0 and (1 - w) % q != 0
            rectangle_scalars.add(w)
            rectangle_count += 1

    return {
        "coefficient_field": f"F_{q}",
        "coordinate_prime": p,
        "primitive_root": zeta,
        "dimension": D,
        "blocks": len(blocks),
        "shared_labels": len(epsilon),
        "triangle_equations": triangle_count,
        "ordered_rectangles": rectangle_count,
        "rectangle_scalars": sorted(rectangle_scalars),
        "rank_I_minus_W": D,
    }


if __name__ == "__main__":
    result = {
        "binary_blocks": [verify(q, D) for q in (5, 7, 11) for D in (1, 2)],
        "odd_prime_blocks": [
            verify_odd_prime_coloring(7, 3, 2, D)
            for D in (1, 2)
        ] + [
            verify_odd_prime_coloring(11, 5, 4, D)
            for D in (1, 2)
        ],
    }
    print(json.dumps(result, indent=2))
