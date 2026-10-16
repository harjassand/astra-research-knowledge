"""Finite adversarial checks of a radius-two tile-overlap emergency decoder.

The intended mathematical result is local and independent of torus size. This
script checks representative modulo-8 histories on 6x6 tori; it is not proof.
"""

from itertools import combinations, product
import random

from check_execution_surface import tiles, successors

L = 6
Q = 8
LAYERS = (tiles(L, 0), tiles(L, 1))
TILES = tuple((p, tile) for p in (0, 1) for tile in LAYERS[p])
INCIDENT = {
    v: tuple((p, tile) for p, tile in TILES if v in tile)
    for v in range(L * L)
}


def valid_tile(s, p, tile):
    vals = {s[v] % Q for v in tile}
    return len(vals) == 1 or any(
        vals == {a, (a + 1) % Q} and a % 2 != p for a in range(Q)
    )


def valid(s):
    return all(valid_tile(s, p, tile) for p, tile in TILES)


def candidate_values(s, v):
    out = []
    for z in range(Q):
        t = list(s)
        t[v] = z
        if all(valid_tile(t, p, tile) for p, tile in INCIDENT[v]):
            out.append(z)
    return tuple(out)


def one_site_repairs(s):
    for v in range(L * L):
        vals = candidate_values(s, v)
        if len(vals) == 1 and vals[0] != s[v]:
            t = list(s)
            t[v] = vals[0]
            yield tuple(t), ("R", v, vals[0])


def overlap(a, b):
    return bool(set(a) & set(b))


def moat(p, tile):
    first = [(r, u) for r, u in TILES if overlap(tile, u)]
    second = [(r, u) for r, u in TILES if any(overlap(u, v) for _, v in first)]
    return tuple(second)


MOATS = {(p, tile): moat(p, tile) for p, tile in TILES}


def emergency_candidates(s, p, tile):
    if valid_tile(s, p, tile):
        return
    if any(len(candidate_values(s, v)) == 1 and candidate_values(s, v)[0] != s[v]
           for v in tile):
        return
    region = MOATS[p, tile]
    for nchange in (1, 2):
        for sites in combinations(tile, nchange):
            for vals in product(range(Q), repeat=nchange):
                if any(z == s[v] for v, z in zip(sites, vals)):
                    continue
                t = list(s)
                for v, z in zip(sites, vals):
                    t[v] = z
                t = tuple(t)
                if all(valid_tile(t, r, u) for r, u in region):
                    yield t, ("B", p, tile, sites, vals)


def emergency_repairs(s):
    for p, tile in TILES:
        yield from emergency_candidates(s, p, tile)


def one_gate_delta(h, t):
    changed = {v for v in range(L * L) if h[v] % Q != t[v]}
    if not changed:
        return "none"
    if len(changed) != 4:
        return None
    for p, tile in TILES:
        if changed != set(tile):
            continue
        if len({h[v] for v in tile}) != 1:
            continue
        k = h[tile[0]]
        if k % 2 == p and all(t[v] == (k + 1) % Q for v in tile):
            return ("skipped", p, tile, k)
        if k % 2 != p and all(t[v] == (k - 1) % Q for v in tile):
            return ("replayed", p, tile, k - 1)
    return None


def main():
    rng = random.Random(260120818)
    h = (0,) * (L * L)
    attempts = 0
    recoveries = 0
    debts = 0
    for _ in range(1000):
        for _ in range(rng.randint(1, 12)):
            moves = list(successors(h, LAYERS))
            h, _ = rng.choice(moves)
        v, w = rng.sample(range(L * L), 2)
        s = list(h)
        for site in (v, w):
            old = s[site] % Q
            s[site] = rng.choice([z for z in range(Q) if z != old])
        s = tuple(x % Q for x in s)
        attempts += 1
        for _ in range(3):
            if valid(s):
                break
            moves = list(one_site_repairs(s))
            if not moves:
                moves = list(emergency_repairs(s))
            if not moves:
                print("TRAP", "h", h, "faults", v, w, "state", s)
                return 1
            s, _ = rng.choice(moves)
        if not valid(s):
            print("TOO_MANY_REPAIRS", h, v, w, s)
            return 1
        debt = one_gate_delta(h, s)
        if debt is None:
            print("NONLOCAL_DEBT", "h", h, "faults", v, w, "state", s)
            return 1
        recoveries += 1
        debts += debt != "none"
    print("PASS", "two-site trials", attempts, "recovered", recoveries,
          "single-gate debts", debts)


if __name__ == "__main__":
    raise SystemExit(main())
