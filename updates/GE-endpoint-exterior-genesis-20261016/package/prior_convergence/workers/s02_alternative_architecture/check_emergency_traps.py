"""Falsification aid for local emergency release under two c+bank faults.

Samples clean modulo-8 states on a 4x4 torus, changes two sites' counters
and bank parities, and asks whether *any* repair move is enabled. This is a
one-step trap search, not a convergence or causal-confinement proof.
"""

from itertools import product
import argparse
import random

from check_bank_parity_decoder import (
    L, Q, INCIDENT, TILES, clean_modulo_states, valid_tile,
)


def tile_candidates(s, tile, bank=None):
    options = []
    for v in tile:
        opposite = next((p, u) for p, u in INCIDENT[v] if u != tile)
        allowed = []
        for z in range(Q):
            if bank is not None and z % 2 != bank[v]:
                continue
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
            yield tuple(t)


def site_candidate(s, v):
    out = []
    for z in range(Q):
        t = list(s)
        t[v] = z
        if all(valid_tile(t, p, tile) for p, tile in INCIDENT[v]):
            out.append(z)
    return out


def enabled(s, bank):
    rv = set()
    for v in range(L * L):
        opts = site_candidate(s, v)
        if len(opts) == 1 and opts[0] != s[v] and opts[0] % 2 == bank[v]:
            rv.add(v)
    if rv:
        return True, ("R_v", sorted(rv))
    for p, tile in TILES:
        if valid_tile(s, p, tile):
            continue
        if len(list(tile_candidates(s, tile, bank))) == 1:
            return True, ("R_P", p, tile)
        if any(True for _ in tile_candidates(s, tile)):
            return True, ("A_P", p, tile)
    for v in range(L * L):
        if all(valid_tile(s, p, tile) for p, tile in INCIDENT[v]) and bank[v] != s[v] % 2:
            return True, ("F_v", v)
    return False, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--trials", type=int, default=2000)
    ap.add_argument("--known-trap", action="store_true")
    args = ap.parse_args()
    if args.known_trap:
        s = (1, 0, 7, 0) + (0,) * 12
        bank = (1, 0, 1, 0) + (0,) * 12
        yes, why = enabled(s, bank)
        if yes:
            print("KNOWN_TRAP_NOT_REPRODUCED", why)
            return 1
        print("KNOWN_TRAP_REPRODUCED", "invalid_tiles",
              [(p, tile) for p, tile in TILES if not valid_tile(s, p, tile)])
        return 0
    rng = random.Random(260120818)
    clean = list(clean_modulo_states())
    trials = args.trials
    for i in range(trials):
        h = rng.choice(clean)
        v, w = rng.sample(range(L * L), 2)
        s = list(h)
        bank = [x % 2 for x in h]
        for site in (v, w):
            s[site] = rng.choice([z for z in range(Q) if z != s[site]])
            bank[site] = rng.randrange(2)
        s = tuple(s)
        bank = tuple(bank)
        if not all(valid_tile(s, p, tile) for p, tile in TILES) or any(
            s[x] % 2 != bank[x] for x in range(L * L)
        ):
            yes, why = enabled(s, bank)
            if not yes:
                print("TRAP", "trial", i, "h", h, "fault_sites", (v, w),
                      "s", s, "bank", bank)
                return 1
    print("NO_ONE_STEP_TRAP_IN_SAMPLES", trials)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
