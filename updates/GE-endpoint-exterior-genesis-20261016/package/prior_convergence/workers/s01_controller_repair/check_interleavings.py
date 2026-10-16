"""Randomized two-fault interleaving falsification for the modified controller.

No probabilistic or scalable theorem follows from passing this search.
"""

import random

from check_execution_surface import successors
from check_moat_repair import (
    L, Q, TILES, LAYERS, INCIDENT, valid, valid_tile,
    one_site_repairs, emergency_repairs, one_gate_delta,
)


def clean_gate_moves(s):
    for p, tile in TILES:
        vals = {s[x] for x in tile}
        if len(vals) != 1 or next(iter(vals)) % 2 != p:
            continue
        if not all(valid_tile(s, r, u) for x in tile for r, u in INCIDENT[x]):
            continue
        t = list(s)
        for x in tile:
            t[x] = (t[x] + 1) % Q
        yield tuple(t), (p, tile)


def inject(s, v, rng):
    out = list(s)
    out[v] = rng.choice([z for z in range(Q) if z != s[v]])
    return tuple(out)


def exercise(rng, max_steps=60):
    h = (0,) * (L * L)
    for _ in range(rng.randrange(20)):
        h, _ = rng.choice(list(successors(h, LAYERS)))
    s = tuple(x % Q for x in h)
    first, second = rng.randrange(L * L), rng.randrange(L * L)
    s = inject(s, first, rng)
    second_time = rng.randrange(20)
    near_gates = 0
    repairs = 0
    for time in range(max_steps):
        if time == second_time:
            s = inject(s, second, rng)
        ghost = tuple(x % Q for x in h)
        dirty = {x for x in range(L * L) if s[x] != ghost[x]}
        assert len(dirty) <= 2, (time, dirty)
        gates = list(clean_gate_moves(s))
        rs = list(one_site_repairs(s))
        bs = list(emergency_repairs(s)) if not rs else []
        if time >= second_time and not dirty:
            return "exact", near_gates, repairs
        if not gates and not rs and not bs:
            raise AssertionError(("trap", time, h, s, first, second))
        # Give repairs adequate selection weight while retaining G interleavings.
        actions = [("G", z) for z in gates] + [("R", z) for z in rs] * 2 + [("B", z) for z in bs] * 2
        kind, (t, meta) = rng.choice(actions)
        if kind == "G":
            p, tile = meta
            assert not dirty.intersection(tile), ("dirty gate", h, s, tile, dirty)
            ghost_gate = [next_h for next_h, (r, u) in successors(h, LAYERS)
                          if r == p and u == tile]
            assert len(ghost_gate) == 1, ("wrong ghost gate", h, s, p, tile)
            if any(x in u for x in tile for r, u in TILES if dirty.intersection(u)):
                near_gates += 1
            h = ghost_gate[0]
        elif kind == "R":
            _, site, value = meta
            assert value == h[site] % Q, ("wrong R", h, s, meta)
            repairs += 1
        else:
            debt = one_gate_delta(h, t)
            assert debt is not None, ("nonlocal B", h, s, meta, t)
            repairs += 1
            return "bulk_debt" if debt != "none" else "bulk_exact", near_gates, repairs
        s = t
    raise AssertionError(("timeout", h, s, first, second))


def main():
    rng = random.Random(260120818)
    stats = {}
    near = 0
    for _ in range(2000):
        result, n, repairs = exercise(rng)
        stats[result] = stats.get(result, 0) + 1
        near += n
        assert repairs <= 2
    print("PASS", stats, "accepted near-boundary G events", near)


if __name__ == "__main__":
    main()
