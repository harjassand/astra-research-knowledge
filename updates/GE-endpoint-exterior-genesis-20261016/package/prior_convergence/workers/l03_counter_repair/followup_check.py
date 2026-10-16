"""Exact finite checks for the proposed overlap-moat B(P) repair.

Scope: q=8 crossed-plaquette counters.  The script checks specified finite
clean histories and exhausts all two-counter substitutions for those histories;
it does not prove a threshold theorem or an arbitrary-noise recursion.
"""

from __future__ import annotations

from collections import deque
from itertools import combinations, product
import json
from pathlib import Path


Q = 8


class Torus:
    def __init__(self, size: int):
        self.L = size
        self.tiles = tuple(
            (p, self.tile(x, y))
            for p in (0, 1)
            for x in range(p, size, 2)
            for y in range(p, size, 2)
        )
        self.tile_by_key = {(p, tile): tile for p, tile in self.tiles}
        self.tile_index = {key: i for i, key in enumerate(self.tiles)}
        self.incident = {v: tuple((p, tile) for p, tile in self.tiles if v in tile)
                         for v in range(size * size)}
        self.moat = {(p, tile): self._moat((p, tile)) for p, tile in self.tiles}
        self.neighbors_of_tiles = {
            (p, tile): tuple(v for v in range(size * size)
                             if any(v in u for _, u in self.moat[(p, tile)]))
            for p, tile in self.tiles
        }

    def idx(self, x: int, y: int) -> int:
        return (x % self.L) * self.L + (y % self.L)

    def coord(self, v: int):
        return divmod(v, self.L)

    def tile(self, x: int, y: int):
        return tuple(sorted(self.idx(x + dx, y + dy)
                            for dx, dy in product(range(2), repeat=2)))

    def _moat(self, key):
        # Distance in the tile-overlap graph, exactly as check_moat_repair.py.
        first = [(p, t) for p, t in self.tiles if set(t) & set(self.tile_by_key[key])]
        second = [(p, t) for p, t in self.tiles
                  if any(set(t) & set(u) for _, u in first)]
        return tuple(second)

    def valid_tile(self, state, p, tile) -> bool:
        vals = {state[v] % Q for v in tile}
        if len(vals) == 1:
            return True
        return any(vals == {a, (a + 1) % Q} and a % 2 != p for a in range(Q))

    def valid(self, state) -> bool:
        return all(self.valid_tile(state, p, tile) for p, tile in self.tiles)

    def affected_tiles(self, sites):
        sites = set(sites)
        return tuple((p, tile) for p, tile in self.tiles if sites.intersection(tile))

    def candidate_values(self, state, v):
        result = []
        for z in range(Q):
            trial = list(state)
            trial[v] = z
            if all(self.valid_tile(trial, p, tile) for p, tile in self.incident[v]):
                result.append(z)
        return tuple(result)

    def singleton_repairs(self, state, sites=None):
        if sites is None:
            sites = range(self.L * self.L)
        result = []
        for v in sites:
            choices = self.candidate_values(state, v)
            if len(choices) == 1 and choices[0] != state[v] % Q:
                result.append((v, choices[0]))
        return tuple(result)

    def b_candidates(self, state, key):
        p, tile = key
        if self.valid_tile(state, p, tile):
            return ()
        if any(self.singleton_repairs(state, tile)):
            return ()
        region = self.moat[key]
        out = []
        for nchange in (1, 2):
            for sites in combinations(tile, nchange):
                for values in product(range(Q), repeat=nchange):
                    if any(z == state[v] % Q for v, z in zip(sites, values)):
                        continue
                    trial = list(state)
                    for v, z in zip(sites, values):
                        trial[v] = z
                    changed = set(sites)
                    # All unmodified tiles of the clean two-site-fault
                    # exterior are valid; only test moat tiles touched either
                    # by the original fault support or by this B write.
                    if all(self.valid_tile(trial, r, u)
                           for r, u in region if changed.intersection(u)):
                        # General callers also use states with two independent
                        # fault clusters, so the explicit guard below checks
                        # every moat tile, not just the write footprint.
                        if all(self.valid_tile(trial, r, u) for r, u in region):
                            out.append((tuple(trial), (sites, values)))
        return tuple(out)

    def clean_successors(self, state):
        for p, tile in self.tiles:
            vals = {state[v] for v in tile}
            if len(vals) == 1:
                k = next(iter(vals))
                if k % 2 == p:
                    t = list(state)
                    for v in tile:
                        t[v] += 1
                    yield tuple(t), (p, tile)


def clean_states(torus: Torus, max_height: int):
    start = (0,) * (torus.L * torus.L)
    seen = {start}
    todo = deque([start])
    while todo:
        state = todo.popleft()
        yield state
        for nxt, _ in torus.clean_successors(state):
            if max(nxt) <= max_height and nxt not in seen:
                seen.add(nxt)
                todo.append(nxt)


def gate_delta(torus: Torus, clean, final):
    changed = {v for v in range(torus.L * torus.L)
               if final[v] % Q != clean[v] % Q}
    if not changed:
        return "none"
    if len(changed) != 4:
        return None
    for p, tile in torus.tiles:
        if changed != set(tile) or len({clean[v] for v in tile}) != 1:
            continue
        k = clean[tile[0]]
        if k % 2 == p and all(final[v] % Q == (k + 1) % Q for v in tile):
            return ("forward", p, tile)
        if k % 2 != p and all(final[v] % Q == (k - 1) % Q for v in tile):
            return ("inverse", p, tile)
    return None


def exact_two_fault_scan(size: int, states, pair_scope=None, scope_note=None):
    torus = Torus(size)
    counts = {
        "clean_states": 0,
        "two_fault_states": 0,
        "states_with_correct_singleton": 0,
        "states_with_false_singleton": 0,
        "states_needing_B": 0,
        "no_correct_singleton_and_no_common_B": 0,
        "B_outputs": 0,
        "invalid_B_outputs": 0,
        "non_gate_valid_B_outputs": 0,
        "multiple_common_B_tiles": 0,
        "multiple_B_candidates_any_common_tile": 0,
    }
    first = {}
    for state_index, clean in enumerate(states, 1):
        counts["clean_states"] += 1
        if state_index == 1 or state_index % 25 == 0:
            print(f"two-fault scan L={size}: clean state {state_index}/{len(states)}",
                  flush=True)
        pairs = (pair_scope if pair_scope is not None
                 else combinations(range(size * size), 2))
        for a, b in pairs:
            original = (clean[a] % Q, clean[b] % Q)
            for za in range(Q):
                if za == original[0]:
                    continue
                for zb in range(Q):
                    if zb == original[1]:
                        continue
                    observed = list(clean)
                    observed[a], observed[b] = za, zb
                    observed = tuple(x % Q for x in observed)
                    counts["two_fault_states"] += 1

                    affected_sites = set()
                    for v in (a, b):
                        for _, tile in torus.incident[v]:
                            affected_sites.update(tile)
                    repairs = torus.singleton_repairs(observed, affected_sites)
                    correct = [(v, z) for v, z in repairs
                               if v in (a, b) and z == clean[v] % Q]
                    false = [(v, z) for v, z in repairs
                             if not (v in (a, b) and z == clean[v] % Q)]
                    if correct:
                        counts["states_with_correct_singleton"] += 1
                    else:
                        counts["states_needing_B"] += 1

                    if false:
                        counts["states_with_false_singleton"] += 1
                        first.setdefault("false_singleton", {
                            "clean": list(clean), "fault_sites": [a, b],
                            "fault_values": [za, zb], "repairs": false,
                        })
                    if correct:
                        continue

                    common = [(p, tile) for p, tile in torus.tiles
                              if a in tile and b in tile
                              and not torus.valid_tile(observed, p, tile)]
                    enabled = []
                    for key in common:
                        opts = torus.b_candidates(observed, key)
                        if opts:
                            enabled.append((key, opts))
                    if len(enabled) > 1:
                        counts["multiple_common_B_tiles"] += 1
                    if not enabled:
                        counts["no_correct_singleton_and_no_common_B"] += 1
                        first.setdefault("no_common_B", {
                            "clean": list(clean), "fault_sites": [a, b],
                            "fault_values": [za, zb], "repairs": repairs,
                            "common_invalid_tiles": common,
                        })
                        continue
                    if any(len(opts) > 1 for _, opts in enabled):
                        counts["multiple_B_candidates_any_common_tile"] += 1
                    for key, opts in enabled:
                        for final, label in opts:
                            counts["B_outputs"] += 1
                            if not torus.valid(final):
                                counts["invalid_B_outputs"] += 1
                                first.setdefault("invalid_B_output", {
                                    "clean": list(clean), "observed": list(observed),
                                    "fault_sites": [a, b], "tile": key,
                                    "write": label, "final": list(final),
                                })
                            elif gate_delta(torus, clean, final) is None:
                                counts["non_gate_valid_B_outputs"] += 1
                                first.setdefault("non_gate_valid_B_output", {
                                    "clean": list(clean), "observed": list(observed),
                                    "fault_sites": [a, b], "tile": key,
                                    "write": label, "final": list(final),
                                })
    return {"scope": (scope_note or
                       f"L={size}, q=8, all clean states supplied to scan; arbitrary distinct-site residue substitutions"),
            "counts": counts, "first_witnesses": first}


def all_distance4_alternatives(size: int, clean):
    """Exhaustively test connected supports up to four, plus singleton cases.

    This is a diagnostic over a supplied clean configuration.  Disconnected
    supports are recorded via the support-component argument in FOLLOWUP.md.
    """
    torus = Torus(size)
    n = size * size
    tile_neighbors = {v: set() for v in range(n)}
    for _, tile in torus.tiles:
        for v in tile:
            tile_neighbors[v].update(set(tile) - {v})

    def connected(sites):
        ss = set(sites)
        seen = {sites[0]}
        stack = [sites[0]]
        while stack:
            v = stack.pop()
            for w in tile_neighbors[v] & ss - seen:
                seen.add(w)
                stack.append(w)
        return len(seen) == len(ss)

    found = []
    counts = {"supports_tested": 0, "assignments_tested": 0,
              "valid_alternatives": 0, "non_gate_alternatives": 0}
    for k in range(1, 5):
        for sites in combinations(range(n), k):
            if k > 1 and not connected(sites):
                continue
            counts["supports_tested"] += 1
            affected = torus.affected_tiles(sites)
            domains = [tuple(z for z in range(Q) if z != clean[v] % Q)
                       for v in sites]
            for values in product(*domains):
                trial = list(clean)
                for v, z in zip(sites, values):
                    trial[v] = z
                counts["assignments_tested"] += 1
                if not all(torus.valid_tile(trial, p, tile) for p, tile in affected):
                    continue
                counts["valid_alternatives"] += 1
                debt = gate_delta(torus, clean, trial)
                if debt is None:
                    counts["non_gate_alternatives"] += 1
                    found.append({"sites": sites, "values": values,
                                  "final": tuple(trial), "debt": debt})
    return {"scope": f"L={size}, q=8, supplied clean state, connected supports up to 4; all tile predicates checked",
            "counts": counts, "non_gate_witnesses": found[:10]}


def adversarial_clean_states(size: int):
    torus = Torus(size)
    zero = (0,) * (size * size)
    states = {"zero": zero}
    # A maximal first even layer and its immediate opposite-layer frontier.
    first_layer = tuple((p, tile) for p, tile in torus.tiles if p == 0)
    one_layer = list(zero)
    for _, tile in first_layer:
        for v in tile:
            one_layer[v] = 1
    states["all_even_tiles_fired_once"] = tuple(one_layer)

    # A legal fair progression to and beyond counter wrap.  At every step,
    # choose among enabled tiles touching a globally minimum-height site.
    state = zero
    for _ in range(10000):
        if min(state) >= Q + 1:
            break
        min_h = min(state)
        moves = [(nxt, label) for nxt, label in torus.clean_successors(state)
                 if any(state[v] == min_h for v in label[1])]
        if not moves:
            moves = list(torus.clean_successors(state))
        if not moves:
            break
        # Deterministic tie-break makes this reproducible and produces a
        # strongly nonuniform wavefront before the min-height phases catch up.
        state, _ = min(moves, key=lambda pair: (max(pair[0]), sum(pair[0]), pair[1]))
    states["wrap_wavefront"] = state

    # Reach the first strongly nonuniform radius-2 wavefront, then carry it
    # across q=8 while keeping the same height spread.
    reachable = tuple(clean_states(torus, 3))
    wave = max(reachable, key=lambda h: (max(h) - min(h), max(h), len(set(h))))
    for _ in range(10000):
        if min(wave) >= Q - 2:
            break
        m = min(wave)
        moves = [(nxt, label) for nxt, label in torus.clean_successors(wave)
                 if any(wave[v] == m for v in label[1])]
        if not moves:
            moves = list(torus.clean_successors(wave))
        if not moves:
            break
        wave, _ = min(moves, key=lambda pair: (max(pair[0]), sum(pair[0]), pair[1]))
    states["wrap_gradient"] = wave

    # Greedy high-gradient schedule: repeatedly fire the enabled tile with
    # greatest max-minus-min local height until a broad front spans the torus.
    state = zero
    for _ in range(300):
        moves = list(torus.clean_successors(state))
        if not moves:
            break
        state, _ = max(moves, key=lambda pair: (
            max(state[v] for v in pair[1][1]) - min(state[v] for v in pair[1][1]),
            sum(pair[0]), pair[1]))
    states["high_gradient"] = state
    return states


def main():
    results = {}
    l4_states = tuple(clean_states(Torus(4), 3))
    results["two_fault_L4"] = exact_two_fault_scan(4, l4_states)
    l6_torus = Torus(6)
    l6_states = tuple(clean_states(l6_torus, 1))
    canonical_pairs = tuple(
        pair for p in (0, 1)
        for tile in [next(t for r, t in l6_torus.tiles
                          if r == p and t == l6_torus.tile(p, p))]
        for pair in combinations(tile, 2)
    )
    results["two_fault_L6_one_layer"] = exact_two_fault_scan(
        6, l6_states, pair_scope=canonical_pairs,
        scope_note=("L=6, q=8; all 512 clean states of the first even-tile layer; "
                    "all six pair positions in one canonical tile of each parity "
                    "and all 49 residue substitutions; translations by even "
                    "vectors cover every co-tiled pair. Pairs sharing no tile "
                    "are covered by the unchanged-neighborhood singleton lemma."))

    distance = {}
    for size in (4, 6):
        distance[str(size)] = {}
        for name, clean in adversarial_clean_states(size).items():
            distance[str(size)][name] = all_distance4_alternatives(size, clean)
    results["distance4_selected_clean_states"] = distance

    target = Path(__file__).with_name("FOLLOWUP_RESULTS.json")
    target.write_text(json.dumps(results, indent=2) + "\n")
    print(json.dumps({
        "two_fault_scans": {
            k: v["counts"] for k, v in results.items() if k.startswith("two_fault_")
        },
        "distance4_counts": {
            L: {name: result["counts"] for name, result in sub.items()}
            for L, sub in results["distance4_selected_clean_states"].items()
        },
    }, indent=2))


if __name__ == "__main__":
    main()
