"""Probe a possible joint two-counter validity repair; finite falsification only."""

from __future__ import annotations

from itertools import combinations, product
import json
from pathlib import Path

from counter_surface_search import s01, reachable_states


HERE = Path(__file__).resolve().parent


def edges(L):
    seen = set()
    for x in range(L):
        for y in range(L):
            i = x * L + y
            for a, b in ((x, (y + 1) % L), ((x + 1) % L, y)):
                seen.add(tuple(sorted((i, a * L + b))))
    return sorted(seen)


def pair_candidates(state, pair, incident):
    a, b = pair
    affected = set(incident[a]) | set(incident[b])
    neighbor_values = [state[i] for _, tile in affected
                       for i in tile if i not in pair]
    lo, hi = min(neighbor_values) - 2, max(neighbor_values) + 2
    candidates = []
    for x, y in product(range(lo, hi + 1), repeat=2):
        trial = list(state)
        trial[a], trial[b] = x, y
        if all(s01.valid_tile(trial, tile, p) for p, tile in affected):
            candidates.append((x, y))
    return candidates


def main():
    L = 4
    layers = (s01.tiles(L, 0), s01.tiles(L, 1))
    incident = {i: tuple((p, tile) for p in (0, 1)
                         for tile in layers[p] if i in tile)
                for i in range(L * L)}
    es = edges(L)
    states = reachable_states(layers)
    counts = {"deadlock_double_faults": 0, "pair_rescued": 0,
              "pair_unrescued": 0, "false_joint_repairs": 0,
              "false_untouched_pair_repairs": 0}
    first = {}
    for state in states:
        for fault_sites in combinations(range(L * L), 2):
            for deltas in product((-2, -1, 1, 2), repeat=2):
                after = list(state)
                for i, d in zip(fault_sites, deltas):
                    after[i] += d
                after = tuple(after)
                if list(s01.successors(after, layers)):
                    continue
                if any(len(c := s01.local_repair_candidates(after, i, incident)) == 1
                       and c[0] != after[i] for i in range(L * L)):
                    continue
                counts["deadlock_double_faults"] += 1
                options = []
                for pair in es:
                    # Let the ordinary one-site repair take priority. Require
                    # each site in the pair to lack any valid singleton repair.
                    if any(s01.local_repair_candidates(after, i, incident)
                           for i in pair):
                        continue
                    candidates = pair_candidates(after, pair, incident)
                    if len(candidates) == 1 and candidates[0] != tuple(after[i] for i in pair):
                        options.append((pair, candidates[0]))
                if options:
                    counts["pair_rescued"] += 1
                    first.setdefault("rescued", {
                        "before": state, "fault_sites": fault_sites,
                        "deltas": deltas, "after": after,
                        "options": options,
                    })
                else:
                    counts["pair_unrescued"] += 1
                    first.setdefault("unrescued", {
                        "before": state, "fault_sites": fault_sites,
                        "deltas": deltas, "after": after,
                    })
                for pair, candidate in options:
                    if any(candidate[j] != state[pair[j]] for j in (0, 1)):
                        counts["false_joint_repairs"] += 1
                        if not (set(pair) & set(fault_sites)):
                            counts["false_untouched_pair_repairs"] += 1
                        first.setdefault("false_joint_repair", {
                            "before": state, "fault_sites": fault_sites,
                            "deltas": deltas, "after": after,
                            "pair": pair, "candidate": candidate,
                        })
    result = {"scope": "L=4, clean states reachable with max counter 3; double faults at distinct sites, delta in +/-1,+/-2; nearest-neighbor pair repair only on no-singleton candidates",
              "counts": counts, "first_witnesses": first}
    (HERE / "PAIR_REPAIR_RESULTS.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
