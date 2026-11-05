"""Exhaustive local check of the new classical repetition EC gadget.

This checks only the deterministic one-fault gadget conditions. It does not
replace the recursive extended-rectangle proof or the accepted tree theorem.
"""

from itertools import product
import json
from pathlib import Path


def make_ec():
    gates = [("reset", (3 + k,)) for k in range(9)]
    for lane in range(3):
        for voter in range(3):
            gates.append(("cx", (lane, 3 + 3 * voter + lane)))
    for voter in range(3):
        a, b, c = [3 + 3 * voter + j for j in range(3)]
        gates.extend([("cx", (a, b)), ("cx", (a, c)), ("ccx", (b, c, a))])
    return gates


GATES = make_ec()
OUTPUTS = [3, 6, 9]


def run(word, fault_gate=None, fault_mask=0):
    state = list(word) + [0] * 9
    for index, (op, wires) in enumerate(GATES):
        if op == "reset":
            state[wires[0]] = 0
        elif op == "cx":
            state[wires[1]] ^= state[wires[0]]
        elif op == "ccx":
            state[wires[2]] ^= state[wires[0]] & state[wires[1]]
        else:
            raise AssertionError(op)
        if index == fault_gate:
            for bit, wire in enumerate(wires):
                state[wire] ^= (fault_mask >> bit) & 1
    return tuple(state[k] for k in OUTPUTS)


clean_checked = 0
fault_checked = 0
for word in product((0, 1), repeat=3):
    majority = int(sum(word) >= 2)
    assert run(word) == (majority,) * 3
    clean_checked += 1

for logical in (0, 1):
    for index, (_, wires) in enumerate(GATES):
        for mask in range(1, 1 << len(wires)):
            output = run((logical,) * 3, index, mask)
            assert sum(x != logical for x in output) <= 1, (
                logical, index, mask, output
            )
            fault_checked += 1

receipt = {
    "status": "passed",
    "native_gates": len(GATES),
    "classical_work_bits": 12,
    "fault_free_input_words_checked": clean_checked,
    "single_gate_arbitrary_output_flip_cases_checked": fault_checked,
    "checked_claim": "fault-free majority correction and clean-input one-fault output weight <= 1",
    "scope_limit": "local deterministic gadget audit, not proof of recursive exRec counting",
}
Path(__file__).with_name("repetition3_local_ec_verification.json").write_text(
    json.dumps(receipt, indent=2) + "\n"
)
print(json.dumps(receipt))
