"""Adversarial finite checks for the crossed-plaquette execution surface.

The reference local invariants and repair-candidate rule are imported from s01.
These are finite falsification checks, not a proof of a recursive controller.
"""

from __future__ import annotations

from collections import deque
from importlib.util import module_from_spec, spec_from_file_location
from itertools import combinations, product
import json
import random
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "s01_controller_repair" / "check_execution_surface.py"
spec = spec_from_file_location("s01_surface", SOURCE)
assert spec and spec.loader
s01 = module_from_spec(spec)
spec.loader.exec_module(s01)


def reachable_states(layers, max_height=3):
    start = (0,) * 16
    seen = {start}
    queue = deque([start])
    while queue:
        state = queue.popleft()
        for nxt, _ in s01.successors(state, layers):
            if max(nxt) <= max_height and nxt not in seen:
                seen.add(nxt)
                queue.append(nxt)
    return sorted(seen)


def valid_mod(values, parity, q):
    residues = {x % q for x in values}
    return len(residues) == 1 or any(
        residues == {a, (a + 1) % q} and a % 2 != parity
        for a in range(q)
    )


def modulo_moves(state, layers, incident, q):
    state = tuple(x % q for x in state)
    repairs = []
    for site in range(len(state)):
        candidates = []
        for z in range(q):
            trial = list(state)
            trial[site] = z
            if all(valid_mod((trial[i] for i in tile), p, q)
                   for p, tile in incident[site]):
                candidates.append(z)
        if len(candidates) == 1 and candidates[0] != state[site]:
            repairs.append((site, candidates[0]))
    gates = []
    for p in (0, 1):
        for tile in layers[p]:
            values = {state[i] for i in tile}
            if len(values) == 1 and next(iter(values)) % 2 == p:
                if all(valid_mod((state[j] for j in u), r, q)
                       for i in tile for r, u in incident[i]):
                    gates.append((p, tile))
    return repairs, gates


def first_witnesses():
    L = 4
    layers = (s01.tiles(L, 0), s01.tiles(L, 1))
    incident = {i: tuple((p, tile) for p in (0, 1)
                         for tile in layers[p] if i in tile)
                for i in range(L * L)}
    states = reachable_states(layers)
    outcomes = {}
    counts = {"tested_double_faults": 0, "valid_double_faults": 0,
              "false_repair": 0, "deadlock": 0}
    for state in states:
        for sites in combinations(range(16), 2):
            for deltas in product((-2, -1, 1, 2), repeat=2):
                after = list(state)
                for site, delta in zip(sites, deltas):
                    after[site] += delta
                after = tuple(after)
                counts["tested_double_faults"] += 1
                valid = s01.valid_state(after, layers)
                if valid:
                    counts["valid_double_faults"] += 1
                    outcomes.setdefault("valid_double_fault", {
                        "before": state, "sites": sites, "deltas": deltas,
                        "after": after,
                    })
                repairs = []
                for site in range(16):
                    candidates = s01.local_repair_candidates(after, site, incident)
                    if len(candidates) == 1 and candidates[0] != after[site]:
                        repairs.append((site, candidates[0]))
                        if site not in sites or candidates[0] != state[site]:
                            counts["false_repair"] += 1
                            outcomes.setdefault("false_repair", {
                                "before": state, "sites": sites,
                                "deltas": deltas, "after": after,
                                "repair": (site, candidates[0]),
                            })
                gates = list(s01.successors(after, layers))
                if not gates and not repairs:
                    counts["deadlock"] += 1
                    outcomes.setdefault("deadlock", {
                        "before": state, "sites": sites,
                        "deltas": deltas, "after": after,
                    })
    # Four onsite faults mimicking a clean atomic four-wire commit at the
    # classical surface, while the quantum gate channel is absent.
    start = (0,) * 16
    tile = layers[0][0]
    pseudo = list(start)
    for site in tile:
        pseudo[site] += 1
    pseudo = tuple(pseudo)
    actual, event = next((nxt, label) for nxt, label in s01.successors(start, layers)
                         if label[1] == tile)
    assert pseudo == actual and s01.valid_state(pseudo, layers)
    outcomes["silent_four_fault_gate_skip"] = {
        "before": start, "faulted_sites": tile, "after": pseudo,
        "matching_clean_event": event,
        "quantum_history": "four control-only faults; gate channel absent",
    }
    # A larger torus gives the same obstruction, so the L=4 example is not
    # solely a short periodic seam artefact. This is a deterministic trace.
    L6 = 6
    layers6 = (s01.tiles(L6, 0), s01.tiles(L6, 1))
    rng = random.Random(843)
    clean6 = (0,) * (L6 * L6)
    trace6 = []
    for _ in range(58):
        clean6, move = rng.choice(list(s01.successors(clean6, layers6)))
        trace6.append(move)
    assert len(list(s01.successors(clean6, layers6))) == 1
    faulty6 = list(clean6)
    faulty6[0] -= 2
    faulty6[1] -= 2
    faulty6 = tuple(faulty6)
    incident6 = {i: tuple((p, tile) for p in (0, 1)
                          for tile in layers6[p] if i in tile)
                 for i in range(L6 * L6)}
    assert not list(s01.successors(faulty6, layers6))
    assert not any(len(c := s01.local_repair_candidates(faulty6, i, incident6)) == 1
                   and c[0] != faulty6[i] for i in range(L6 * L6))
    pair_completions = []
    for x, y in product(range(-2, 12), repeat=2):
        trial = list(faulty6)
        trial[0], trial[1] = x, y
        if s01.valid_state(tuple(trial), layers6):
            pair_completions.append((x, y))
    assert pair_completions == [(clean6[0], clean6[1])]
    outcomes["L6_absorbing_two_fault_state"] = {
        "clean_trace": trace6, "before": clean6,
        "faulted_sites": (0, 1), "deltas": (-2, -2), "after": faulty6,
        "enabled_gates": 0, "enabled_single_site_repairs": 0,
        "joint_valid_pair_completions_in_test_range": pair_completions,
    }
    modulo_checks = {}
    for q in (8, 10, 12, 16, 32):
        repair_moves, gate_moves = modulo_moves(faulty6, layers6, incident6, q)
        assert not repair_moves and not gate_moves
        modulo_checks[q] = {"repairs": repair_moves, "gates": gate_moves}
    outcomes["L6_absorbing_two_fault_state"]["modulo_checks"] = modulo_checks
    result = {"scope": "L=4 integer counters, reachable heights <=3; two faults at distinct sites with deltas in {-2,-1,+1,+2}",
              "states": len(states), "counts": counts, "first_witnesses": outcomes}
    return result


if __name__ == "__main__":
    result = first_witnesses()
    output = HERE / "COUNTER_SURFACE_RESULTS.json"
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
