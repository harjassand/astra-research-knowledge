#!/usr/bin/env python3
"""Finite geometry check for the 1D Freudenthal (linear) interpolation lemma.

This tests interpolation inequalities only. It does not implement the LP, test
the statistical theorem, or establish asymptotic/high-dimensional behavior.
"""
from bisect import bisect_right
import random


def barycentric(grid, x):
    """Return neighboring grid indices and linear weights on [0,1]."""
    if x <= 0:
        return (0, 0.0), (1, 0.0)
    if x >= 1:
        return (len(grid) - 2, 0.0), (len(grid) - 1, 1.0)
    i = min(len(grid) - 2, bisect_right(grid, x) - 1)
    t = (x - grid[i]) / (grid[i + 1] - grid[i])
    return (i, 1.0 - t), (i + 1, t)


def mixture_at(grid, anchors, x):
    out = {}
    for i, weight in barycentric(grid, x):
        out[anchors[i]] = out.get(anchors[i], 0.0) + weight
    return out


def w1_line(a, b):
    """Exact 1D W1 formula for finite distributions represented by dicts."""
    atoms = sorted(set(a) | set(b))
    ca = cb = total = 0.0
    for left, right in zip(atoms, atoms[1:]):
        ca += a.get(left, 0.0)
        cb += b.get(left, 0.0)
        total += abs(ca - cb) * (right - left)
    return total


def interp_prob(grid, probabilities, x):
    return sum(weight * probabilities[i] for i, weight in barycentric(grid, x))


def main():
    rng = random.Random(20261009)
    m = 40
    step = 1.0 / m
    grid = [i * step for i in range(m + 1)]

    # One source/target anchor per vertex, each within step of its vertex.
    # Jitter <= step/4 also guarantees adjacent anchors are ordered and <=3 step apart.
    source = [min(1.0, max(0.0, g + rng.uniform(-step / 4, step / 4))) for g in grid]
    target = [min(1.0, max(0.0, g + rng.uniform(-step / 4, step / 4))) for g in grid]

    target_lip_max = 0.0
    displacement_max = 0.0
    for _ in range(10_000):
        y = rng.random()
        yp = rng.random()
        ty = mixture_at(grid, target, y)
        typ = mixture_at(grid, target, yp)
        gap = abs(y - yp)
        if gap:
            target_lip_max = max(target_lip_max, w1_line(ty, typ) / gap)
        displacement_max = max(
            displacement_max,
            sum(mass * abs(atom - y) for atom, mass in ty.items()),
        )

    # Bernoulli conditionals on target {0,1}; set vertex probabilities from
    # the acquired source anchors. Their adjacent W1 variation obeys L0*distance
    # for L0=1, and the interpolated kernel is a valid stochastic kernel.
    probs = [0.25 + 0.5 * x for x in source]
    edge_ratios = []
    for i in range(m):
        dist = abs(source[i + 1] - source[i])
        edge_ratios.append(abs(probs[i + 1] - probs[i]) / dist)
    source_lip_max = 0.0
    for _ in range(10_000):
        x = rng.random()
        xp = rng.random()
        gap = abs(x - xp)
        if gap:
            source_lip_max = max(
                source_lip_max,
                abs(interp_prob(grid, probs, x) - interp_prob(grid, probs, xp)) / gap,
            )

    assert max(edge_ratios) <= 1.0 + 1e-12
    assert target_lip_max <= 6.0 + 1e-10
    assert displacement_max <= 2.0 * step + 1e-12
    assert source_lip_max <= 6.0 + 1e-10
    print(f"seed=20261009 grid_vertices={len(grid)} random_pairs=10000")
    print(f"target_interpolant_max_observed_lipschitz={target_lip_max:.8f} theorem_bound=6")
    print(f"target_interpolant_max_observed_displacement={displacement_max:.8f} theorem_bound={2*step:.8f}")
    print(f"source_edge_max_ratio={max(edge_ratios):.8f} constraint_bound=1")
    print(f"source_interpolant_max_observed_lipschitz={source_lip_max:.8f} theorem_bound=6")
    print("PASS: interpolation-only finite diagnostic; no LP/statistical claim tested")


if __name__ == "__main__":
    main()
