"""Two-fault absorbing program split in the current s01 transition table.

This is separate from its counter-only two-fault theorem. All counters and
colors remain clean. Two onsite writes set two tile program copies to the same
wrong word, giving a 2–2 tie that neither G nor A can resolve.
"""
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

SOURCE = Path(__file__).resolve().parent.parent / "s01_controller_repair" / "check_execution_surface.py"
spec = spec_from_file_location("s01_execution", SOURCE)
assert spec and spec.loader
s01 = module_from_spec(spec)
spec.loader.exec_module(s01)


def run():
    L = 4
    layers = (s01.tiles(L, 0), s01.tiles(L, 1))
    target = layers[0][0]
    counter = [0] * (L * L)
    program = {p: {tile: ["w"] * 4 for tile in layers[p]} for p in (0, 1)}
    program[0][target][0:2] = ["wprime", "wprime"]

    # Three unaffected even tiles complete, leaving the target as the only
    # pending even tile. These are exactly the clean accepted gate events.
    for tile in layers[0]:
        if tile == target:
            continue
        assert all(counter[v] == 0 for v in tile)
        for v in tile:
            counter[v] = 1
    state = tuple(counter)
    assert s01.valid_state(state, layers)

    # Every odd tile on this torus intersects the target, so it cannot run.
    assert all(not (set(tile).isdisjoint(target)) for tile in layers[1])
    assert all(len({state[v] for v in tile}) > 1 for tile in layers[1])
    assert tuple(s01.successors(state, layers)) == ((tuple(1 if i in target else state[i] for i in range(16)), (0, target)),)

    # The remaining counter-ready gate is blocked by its exact 2–2 program
    # split. A(v,0) requires all other three copies equal, which never holds.
    copies = program[0][target]
    assert copies == ["wprime", "wprime", "w", "w"]
    assert max(copies.count("w"), copies.count("wprime")) == 2
    assert all(len(set(copies[:i] + copies[i + 1:])) > 1 for i in range(4))
    assert not any(s01.local_repair_candidates(state, i, {
        j: tuple((p, tile) for p in (0, 1) for tile in layers[p] if j in tile)
        for j in range(16)
    }) == (z,) and z != state[i] for i in range(16) for z in range(8))
    assert s01.valid_state(state, layers)  # no invalid tile enables B

    print({
        "faults": "two onsite program-copy writes on one even tile",
        "copies": copies,
        "counters_after_all_other_even_gates": [state[i:i + 4] for i in range(0, 16, 4)],
        "remaining_counter_ready_gates": 1,
        "enabled_program_gates": 0,
        "enabled_program_repairs_on_target": 0,
        "enabled_counter_repairs_or_bulk": 0,
        "service": "absorbing under ideal attempts",
    })


if __name__ == "__main__":
    run()
