"""Finite search for the crossed-plaquette execution-counter proposal.

This is a finite falsification aid, not a proof of a scalable controller.
The integer counter version avoids modulo-wrap artifacts in the search.
"""

from collections import deque
from itertools import product
import argparse
import random


def tiles(L, parity):
    result = []
    for x in range(parity, L, 2):
        for y in range(parity, L, 2):
            result.append(tuple(sorted(((x + dx) % L) * L + (y + dy) % L
                                       for dx, dy in product(range(2), repeat=2))))
    return tuple(result)


def valid_tile(state, tile, parity):
    vals = [state[i] for i in tile]
    lo, hi = min(vals), max(vals)
    return lo == hi or (hi == lo + 1 and lo % 2 != parity)


def valid_state(state, layers):
    return all(valid_tile(state, tile, p) for p in (0, 1) for tile in layers[p])


def successors(state, layers):
    for p in (0, 1):
        for tile in layers[p]:
            vals = [state[i] for i in tile]
            if len(set(vals)) == 1 and vals[0] % 2 == p:
                new = list(state)
                for i in tile:
                    new[i] += 1
                yield tuple(new), (p, tile)


def local_repair_candidates(state, site, incident):
    ps = incident[site]
    neighbors = [state[j] for p, tile in ps for j in tile if j != site]
    low, high = min(neighbors) - 2, max(neighbors) + 2
    out = []
    for c in range(low, high + 1):
        trial = list(state)
        trial[site] = c
        if all(valid_tile(trial, tile, p) for p, tile in ps):
            out.append(c)
    return tuple(out)


def check_state(state, layers, incident, deltas):
    if not valid_state(state, layers):
        return "clean state fails tile invariant", state
    for site in range(len(state)):
        for d in deltas:
            trial = list(state)
            trial[site] += d
            trial = tuple(trial)
            if valid_state(trial, layers):
                return "undetected one-site counter fault", (state, site, d, trial)
            candidates = local_repair_candidates(trial, site, incident)
            if candidates != (state[site],):
                return "true site lacks unique repair", (state, site, d, candidates)
            for neighbor in range(len(state)):
                if neighbor == site:
                    continue
                c = local_repair_candidates(trial, neighbor, incident)
                if len(c) == 1 and c[0] != state[neighbor]:
                    return "false neighboring repair", (state, site, d, neighbor, c)
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--L", type=int, default=4)
    ap.add_argument("--max-height", type=int, default=3)
    ap.add_argument("--random-traces", type=int, default=1000)
    ap.add_argument("--random-length", type=int, default=100)
    args = ap.parse_args()
    L = args.L
    assert L >= 4 and L % 2 == 0
    layers = (tiles(L, 0), tiles(L, 1))
    incident = {}
    for site in range(L * L):
        incident[site] = tuple((p, tile) for p in (0, 1)
                               for tile in layers[p] if site in tile)
        assert len(incident[site]) == 2
    start = (0,) * (L * L)
    seen = {start}
    todo = deque([start])
    checked = 0
    while todo:
        s = todo.popleft()
        failure = check_state(s, layers, incident, (-2, -1, 1, 2))
        if failure:
            print("FAIL", failure)
            return 1
        checked += 1
        for nxt, _ in successors(s, layers):
            if max(nxt) <= args.max_height and nxt not in seen:
                seen.add(nxt)
                todo.append(nxt)
    rng = random.Random(20261016)
    for _ in range(args.random_traces):
        s = start
        for _ in range(args.random_length):
            moves = list(successors(s, layers))
            if not moves:
                break
            s, _ = rng.choice(moves)
            failure = check_state(s, layers, incident, (-2, -1, 1, 2))
            if failure:
                print("FAIL", failure)
                return 1
            checked += 1
    print(f"PASS L={L}, exhaustive states={len(seen)}, checked samples={checked}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
