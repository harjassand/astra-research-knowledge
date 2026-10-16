"""Exact finite patch check for a two-counter history ambiguity.

This is a bounded, exhaustive calculation on one 6x6 torus.  It reuses only
the crossed-plaquette validity rule from s01; it is not a threshold theorem.
"""

from __future__ import annotations

from itertools import combinations, product
import json
from pathlib import Path


L = 6
Q = 8
PATCH_COORDS = {(x, y) for x in range(1, 5) for y in range(1, 5)}


def idx(x: int, y: int) -> int:
    return (x % L) * L + (y % L)


def tiles(parity: int):
    return tuple(
        tuple(sorted(idx(x + dx, y + dy)
                     for dx, dy in product(range(2), repeat=2)))
        for x in range(parity, L, 2)
        for y in range(parity, L, 2)
    )


LAYERS = (tiles(0), tiles(1))
ALL_TILES = tuple((p, tile) for p in (0, 1) for tile in LAYERS[p])
PATCH_SITES = tuple(sorted(idx(x, y) for x, y in PATCH_COORDS))
PATCH_BOUNDARY = tuple(sorted(
    idx(x, y) for x, y in PATCH_COORDS
    if x in (1, 4) or y in (1, 4)
))


def valid_mod(values, parity: int) -> bool:
    residues = {v % Q for v in values}
    if len(residues) == 1:
        return True
    return any(residues == {a, (a + 1) % Q} and a % 2 != parity
               for a in range(Q))


def valid_state(state) -> bool:
    return all(valid_mod((state[i] for i in tile), p)
               for p, tile in ALL_TILES)


def class_sums(state):
    """Return sums mod Q in order (00, 01, 10, 11)."""
    sums = [0, 0, 0, 0]
    for x in range(L):
        for y in range(L):
            color = 2 * (x % 2) + (y % 2)
            sums[color] += state[idx(x, y)]
    return tuple(v % Q for v in sums)


def sub_mod(a, b):
    return tuple((x - y) % Q for x, y in zip(a, b))


def balanced_tile_edit_delta(before, after) -> bool:
    delta = sub_mod(class_sums(after), class_sums(before))
    return len(set(delta)) == 1


def completions_within_two_faults(observed):
    """Enumerate all assignments in the fixed patch at Hamming distance <=2."""
    found = []
    outside = set(range(L * L)) - set(PATCH_SITES)
    assert all(observed[i] == 0 for i in outside)

    def consider(state, changed):
        if valid_state(state):
            found.append({
                "changed_sites": list(changed),
                "changed_count": len(changed),
                "state": list(state),
                "class_sums": class_sums(state),
                "reachable_by_full_tile_count_edits_from_observed":
                    balanced_tile_edit_delta(observed, state),
            })

    consider(observed, ())
    for (a,) in combinations(PATCH_SITES, 1):
        for za in range(Q):
            if za == observed[a]:
                continue
            state = list(observed)
            state[a] = za
            consider(tuple(state), (a,))
    for a, b in combinations(PATCH_SITES, 2):
        for za, zb in product(range(Q), repeat=2):
            if za == observed[a] or zb == observed[b]:
                continue
            state = list(observed)
            state[a], state[b] = za, zb
            consider(tuple(state), (a, b))
    return found


def main():
    # A clean even-tile commit at (2,2) is a valid one-gate history B.
    tile_coords = ((2, 2), (2, 3), (3, 2), (3, 3))
    tile = tuple(idx(x, y) for x, y in tile_coords)
    history_a = (0,) * (L * L)
    b = [0] * (L * L)
    for site in tile:
        b[site] = 1
    history_b = tuple(b)

    # Two sites from distinct parity classes are advanced.  The same observed
    # counter snapshot is two onsite counter faults from either clean history.
    observed_values = [0] * (L * L)
    for x, y in tile_coords[:2]:  # color classes (00) and (01)
        observed_values[idx(x, y)] = 1
    observed = tuple(observed_values)

    assert valid_state(history_a)
    assert valid_state(history_b)
    assert not valid_state(observed)
    assert sum(a != b for a, b in zip(history_a, observed)) == 2
    assert sum(a != b for a, b in zip(history_b, observed)) == 2
    assert all(history_a[i] == history_b[i] == observed[i]
               for i in PATCH_BOUNDARY)
    assert set(tile) <= set(PATCH_SITES)

    candidates = completions_within_two_faults(observed)
    assert any(c["state"] == list(history_a) for c in candidates)
    assert any(c["state"] == list(history_b) for c in candidates)

    result = {
        "scope": "exact q=8 check on one 6x6 torus; fixed 4x4 patch x,y in 1..4; all 2x2 tiles checked",
        "tile_coordinates": tile_coords,
        "patch_boundary_coordinates": sorted(
            (x, y) for x, y in PATCH_COORDS
            if x in (1, 4) or y in (1, 4)),
        "history_A": list(history_a),
        "history_B_after_one_even_tile_gate": list(history_b),
        "observed_midpoint": list(observed),
        "validity": {
            "A": valid_state(history_a),
            "B": valid_state(history_b),
            "observed": valid_state(observed),
        },
        "fault_distance_from_observed": {
            "A": sum(a != b for a, b in zip(history_a, observed)),
            "B": sum(a != b for a, b in zip(history_b, observed)),
        },
        "parity_class_sums": {
            "A": class_sums(history_a),
            "B": class_sums(history_b),
            "observed": class_sums(observed),
        },
        "A_edit_delta_from_observed": sub_mod(
            class_sums(history_a), class_sums(observed)),
        "B_edit_delta_from_observed": sub_mod(
            class_sums(history_b), class_sums(observed)),
        "A_reachable_by_full_tile_count_edits":
            balanced_tile_edit_delta(observed, history_a),
        "B_reachable_by_full_tile_count_edits":
            balanced_tile_edit_delta(observed, history_b),
        "all_valid_completions_within_two_counter_edits": candidates,
        "candidate_count": len(candidates),
        "count_edit_lemma": (
            "Every 2x2 tile increment/decrement changes each of the four "
            "coordinate-parity class sums by the same +/-1. Their pairwise "
            "differences mod q are invariant, so unequal class-sum deltas "
            "exclude every sequence of full-tile count edits."
        ),
    }
    target = Path(__file__).with_name("PATCH_COMPLETION_RESULTS.json")
    target.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
