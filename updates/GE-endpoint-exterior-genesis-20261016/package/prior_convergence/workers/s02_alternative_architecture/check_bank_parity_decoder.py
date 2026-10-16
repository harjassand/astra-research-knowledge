"""Finite falsification aid for the crossed-surface bank-parity receiver.

This checks whether the collective R_P rule has a unique counter-vector
candidate after two same-tile counter faults, *without* telling the decoder
which two sites were faulty. It is not a scalable proof or a physical decoder.
"""

from collections import deque
from itertools import combinations, product
from pathlib import Path
import argparse
import random
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "s01_controller_repair"))
from check_execution_surface import successors, tiles  # noqa: E402

L = 4
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


def candidates(s, tile, bank_parity):
    """All four-counter repairs locally valid and compatible with bank parity."""
    options = []
    for v in tile:
        opposite = next((p, u) for p, u in INCIDENT[v] if u != tile)
        allowed = []
        for z in range(bank_parity[v], Q, 2):
            t = list(s)
            t[v] = z
            if valid_tile(t, *opposite):
                allowed.append(z)
        options.append(allowed)
    for zs in product(*options):
        t = list(s)
        for v, z in zip(tile, zs):
            t[v] = z
        if all(valid_tile(t, p, u) for v in tile for p, u in INCIDENT[v]):
            yield tuple(t), zs


def clean_states(max_height):
    start = (0,) * (L * L)
    seen = {start}
    todo = deque([start])
    while todo:
        s = todo.popleft()
        yield s
        for t, _ in successors(s, LAYERS):
            if max(t) <= max_height and t not in seen:
                seen.add(t)
                todo.append(t)


def clean_modulo_states():
    start = (0,) * (L * L)
    seen = {start}
    todo = deque([start])
    while todo:
        s = todo.popleft()
        yield s
        for t, _ in successors(s, LAYERS):
            t = tuple(x % Q for x in t)
            if t not in seen:
                seen.add(t)
                todo.append(t)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-height", type=int, default=3)
    ap.add_argument("--random-wrap-states", type=int, default=0)
    ap.add_argument("--all-modulo", action="store_true")
    args = ap.parse_args()
    cases = 0
    invalid_cases = 0
    valid_undetected = 0
    wrong_or_ambiguous = []
    states = list(clean_modulo_states() if args.all_modulo
                  else clean_states(args.max_height))
    if args.random_wrap_states:
        rng = random.Random(260120818)
        h = (0,) * (L * L)
        for _ in range(args.random_wrap_states):
            for _ in range(20):
                moves = list(successors(h, LAYERS))
                h, _ = rng.choice(moves)
            states.append(h)
    for h in states:
        s0 = tuple(x % Q for x in h)
        bank_parity = tuple(x % 2 for x in h)
        for p, tile in TILES:
            for pair in combinations(tile, 2):
                for zs in product(range(Q), repeat=2):
                    if any(z == s0[v] for v, z in zip(pair, zs)):
                        continue
                    s = list(s0)
                    for v, z in zip(pair, zs):
                        s[v] = z
                    s = tuple(s)
                    cases += 1
                    if valid_tile(s, p, tile):
                        if all(s[v] % 2 == bank_parity[v] for v in pair) and all(
                            valid_tile(s, r, u) for r, u in TILES
                        ):
                            valid_undetected += 1
                            if valid_undetected <= 3:
                                print("UNDETECTED", h, p, tile, pair, zs, s)
                        continue
                    invalid_cases += 1
                    found = list(candidates(s, tile, bank_parity))
                    if len(found) != 1 or found[0][0] != s0:
                        wrong_or_ambiguous.append((h, p, tile, pair, zs, s, found[:3]))
                        if len(wrong_or_ambiguous) == 3:
                            print("FAIL", "cases", cases, "invalid", invalid_cases)
                            for item in wrong_or_ambiguous:
                                print(item)
                            return 1
    print("PASS", "clean states", len(states),
          "two-site cases", cases, "invalid", invalid_cases,
          "wrong_or_ambiguous", len(wrong_or_ambiguous),
          "valid_undetected", valid_undetected)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
