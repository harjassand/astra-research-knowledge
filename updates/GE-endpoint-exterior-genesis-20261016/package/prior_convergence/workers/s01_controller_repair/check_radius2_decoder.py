"""Challenge a proposed radius-two plaquette decoder after two site faults."""

from itertools import combinations, product
import random

from check_bulk_repair import L, Q, LAYERS, ALL_TILES, incident_tiles, violation_count
from check_modulo_surface import candidates, clean_states, valid_mod


def bulk_candidates(s, p, tile):
    affected = incident_tiles(tile)
    for nchange in (1, 2):
        for changed in combinations(tile, nchange):
            for zs in product(range(Q), repeat=nchange):
                if any(z == s[v] for v, z in zip(changed, zs)):
                    continue
                t = list(s)
                for v, z in zip(changed, zs):
                    t[v] = z
                t = tuple(t)
                if all(valid_mod((t[i] for i in u), r) for r, u in affected):
                    yield t, changed, zs


def main():
    rng = random.Random(42)
    states = list(clean_states())
    trials = 0
    for _ in range(5000):
        h = rng.choice(states)
        s = tuple(x % Q for x in h)
        v, w = rng.sample(range(L * L), 2)
        z = rng.choice([x for x in range(Q) if x != s[v]])
        y = rng.choice([x for x in range(Q) if x != s[w]])
        t = list(s)
        t[v], t[w] = z, y
        t = tuple(t)
        for p, tile in ALL_TILES:
            if valid_mod((t[i] for i in tile), p):
                continue
            if any(len(candidates(t, a)) == 1 and candidates(t, a)[0] != t[a]
                   for a in tile):
                continue
            found = next(bulk_candidates(t, p, tile), None)
            if found and not ({v, w} <= set(tile)):
                print("OFF_TARGET_BULK", "clean", h, "faults", (v, z), (w, y),
                      "tile", p, tile, "candidate", found,
                      "remaining_violation", violation_count(found[0]))
                return
        trials += 1
    print("NO_OFF_TARGET_BULK_IN_RANDOM_TRIALS", trials)


if __name__ == "__main__":
    main()
