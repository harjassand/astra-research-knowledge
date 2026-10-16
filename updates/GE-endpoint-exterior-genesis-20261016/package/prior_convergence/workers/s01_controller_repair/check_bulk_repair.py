"""Search whether local safe bulk completion resolves two counter faults.

Finite falsification, with no inference to an infinite-lattice theorem.
"""

from collections import deque
from itertools import combinations, product
import random

from check_modulo_surface import (
    L, Q, LAYERS, INCIDENT, candidates, clean_states, valid_mod,
)

ALL_TILES = tuple((p, tile) for p in (0, 1) for tile in LAYERS[p])


def violation_count(s):
    return sum(not valid_mod((s[i] for i in tile), p) for p, tile in ALL_TILES)


def incident_tiles(touched):
    return tuple((p, tile) for p, tile in ALL_TILES if any(v in touched for v in tile))


def repairs(s, allow_low=False):
    """Only moves strictly reducing the number of invalid plaquettes."""
    before = violation_count(s)
    if not before:
        return
    for v in range(L * L):
        opts = candidates(s, v)
        if len(opts) == 1 and opts[0] != s[v]:
            t = list(s)
            t[v] = opts[0]
            t = tuple(t)
            if violation_count(t) < before:
                yield t, ("single", v, opts[0])
    for p, tile in ALL_TILES:
        vals = {s[i] for i in tile}
        if len(vals) != 2:
            continue
        for a in range(Q):
            if a % 2 != p or vals != {a, (a + 1) % Q}:
                continue
            targets = [(a + 1) % Q]
            if allow_low:
                targets.append(a)
            affected = incident_tiles(tile)
            for z in targets:
                t = list(s)
                for v in tile:
                    t[v] = z
                t = tuple(t)
                if all(valid_mod((t[i] for i in u), r) for r, u in affected):
                    if violation_count(t) < before:
                        yield t, ("bulk", p, tile, z)


def explore(start, allow_low=False):
    """All repair outcomes; failures are irreparable leaves."""
    todo = deque([(start, ())])
    seen = {start}
    traps = []
    endpoints = set()
    while todo:
        s, path = todo.popleft()
        if not violation_count(s):
            endpoints.add(s)
            continue
        moves = list(repairs(s, allow_low=allow_low))
        if not moves:
            traps.append((s, path))
        for t, label in moves:
            if t not in seen:
                seen.add(t)
                todo.append((t, path + (label,)))
    return traps, endpoints


def main():
    rng = random.Random(260120818)
    states = list(clean_states())
    trials = []
    for h in states[:10]:
        s = tuple(x % Q for x in h)
        for v, w in combinations(range(L * L), 2):
            for dv, dw in product((-2, -1, 1, 2), repeat=2):
                t = list(s)
                t[v] = (t[v] + dv) % Q
                t[w] = (t[w] + dw) % Q
                trials.append((h, v, w, dv, dw, tuple(t)))
    rng.shuffle(trials)
    for allow_low in (False, True):
        checked = 0
        for h, v, w, dv, dw, t in trials:
            traps, endpoints = explore(t, allow_low=allow_low)
            checked += 1
            if traps:
                print("TRAP", "allow_low", allow_low, "checked", checked,
                      "h", h, "faults", (v, dv), (w, dw),
                      "start", t, "trap", traps[0])
                break
        else:
            print("PASS", "allow_low", allow_low, "checked", checked)


if __name__ == "__main__":
    main()
