"""Historical liveness branch in s03's earlier occupancy-guarded G row.

The qutrit unitary swaps |0> and |perp> on one chosen source A bank. In a
[[5,1,3]] code state the local |0> outcome has positive probability (indeed
1/2 for the standard pure code). Conditioning on that branch leaves the
chosen A source vacant while all counters and tokens are untouched. The
earlier G required occupancy, so no prescribed row could spend its token.
The revised G/H rows removed this raw occupancy guard; this script is a
regression witness for that repair choice, not an attack on the revised row.
"""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

SOURCE = Path(__file__).resolve().parent.parent / "s03_history_interface" / "finite_discharge_check.py"
spec = spec_from_file_location("s03_finite", SOURCE)
assert spec and spec.loader
f = module_from_spec(spec)
spec.loader.exec_module(f)


def run():
    counters = f.clean_state(set())
    token_spent = {anchor: False for anchor in f.ACTIVE}
    a_occupied = {anchor: True for anchor in f.ACTIVE}
    b_vacant = {anchor: True for anchor in f.ACTIVE}
    target = f.TARGET

    # A single allowed onsite qutrit unitary produces a nonzero vacancy
    # sector. The occupancy guard dephases, so this sector is an actual CP
    # transcript branch that must satisfy the claimed service theorem.
    a_occupied[target] = False
    assert f.gate_ready(counters, target)  # classical counters look ready
    enabled_g = [a for a in f.ACTIVE
                 if not token_spent[a] and f.gate_ready(counters, a)
                 and a_occupied[a]]
    assert target not in enabled_g
    assert not tuple(f.unique_repairs(counters))
    assert not f.emergency_ready(counters)

    # Fire all four disjoint gates; no later ideal jump can alter target A.
    for a in enabled_g:
        token_spent[a] = True
        for v in f.tile(*a, 0):
            counters[v] = 1
    assert not any(not token_spent[a] and f.gate_ready(counters, a)
                   and a_occupied[a] for a in f.ACTIVE)
    assert not tuple(f.unique_repairs(counters))
    assert not f.emergency_ready(counters)
    terminal_ready = all(token_spent.values()) and all(b_vacant.values())
    assert not terminal_ready
    print({
        "noise": "one onsite qutrit unitary swapping |0> and |perp> in target A",
        "conditioned_branch": "target A vacant; counters=0; target token LIVE",
        "after_all_other_gates": "no G, R, E, or T enabled; target token LIVE",
        "service": "noncompletion with positive probability despite no further faults",
    })


if __name__ == "__main__":
    run()
