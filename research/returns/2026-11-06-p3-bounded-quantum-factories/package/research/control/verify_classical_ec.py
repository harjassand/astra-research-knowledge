"""Exhaustive local audit of repetition-five two-refresh EC.

MAJ5 is abstracted as its Boolean function and arbitrary private output
flips. An internal physical macro fault is confined to one voter, so this
covers the local fault argument. Recursive regularity is proved in text.
"""
from itertools import product
from pathlib import Path
import json


def build_ec():
    gates = []
    inputs = list(range(5))
    for stage in range(2):
        start = 5 + 25 * stage
        gates += [("reset", (start + j,)) for j in range(25)]
        for lane in range(5):
            for voter in range(5):
                gates.append(("cx", (inputs[lane], start + 5 * voter + lane)))
        gates += [("maj5", tuple(start + 5 * v + x for x in range(5))) for v in range(5)]
        inputs = [start + 5 * v for v in range(5)]
    return gates, inputs


GATES, OUTPUTS = build_ec()


def run(word, fault_gate=None, mask=0):
    state = list(word) + [0] * 50
    for index, (op, wires) in enumerate(GATES):
        if op == "reset":
            state[wires[0]] = 0
        elif op == "cx":
            state[wires[1]] ^= state[wires[0]]
        elif op == "maj5":
            state[wires[0]] = int(sum(state[w] for w in wires) >= 3)
        if index == fault_gate:
            for bit, wire in enumerate(wires):
                state[wire] ^= (mask >> bit) & 1
    return tuple(state[x] for x in OUTPUTS)


faults = [(None, 0)] + [(i, m) for i, (_, w) in enumerate(GATES) for m in range(1, 1 << len(w))]
validity_checks = correction_checks = 0
for word in product((0, 1), repeat=5):
    assert run(word) == (int(sum(word) >= 3),) * 5
    for fault, mask in faults:
        out = run(word, fault, mask)
        assert min(sum(out), 5 - sum(out)) <= 1, (word, fault, mask, out)
        validity_checks += 1
        for b in (0, 1):
            if sum(x != b for x in word) <= 1:
                assert sum(x != b for x in out) <= 1, (word, fault, mask, out)
                correction_checks += 1


def maj_anf(a, b, c, d, e):
    b, c, d, e = b ^ a, c ^ a, d ^ a, e ^ a
    return a ^ (b & c & d) ^ (b & c & e) ^ (b & d & e) ^ (c & d & e) ^ (b & c & d & e)


for bits in product((0, 1), repeat=5):
    assert maj_anf(*bits) == int(sum(bits) >= 3)

receipt = {
    "status": "passed", "repetition_size": 5, "refresh_rounds": 2,
    "abstract_operations": len(GATES), "abstract_work_bits": 55,
    "arbitrary_input_validity_cases": validity_checks,
    "one_incoming_error_plus_one_fault_cases": correction_checks,
    "majority_anf_inputs_checked": 32,
    "fault_model": "one operation with arbitrary flips on any subset of its output wires",
    "scope": "local deterministic gadget properties; recursive regularity/export proved in text",
}
Path(__file__).with_name("classical_ec_verification.json").write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt))
