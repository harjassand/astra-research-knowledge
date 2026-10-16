"""Trace a counterfeit occupied packet through a one-use CNOT rail.

The script records data effects and the extra stuck real packet. It does not
classify every downstream gate as a separate faulty location: an EC interface
could absorb this trace as propagation from one bad preparation/first gate.
"""

from __future__ import annotations

import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
VACANT = None


def run(n: int, phantom: bool):
    assert n >= 1
    real_predecessor = 0
    control_inputs = [VACANT] * (n + 1)
    target_inputs = [0] * n
    target_outputs = [VACANT] * n
    tokens = ["LIVE"] * n
    trace = []
    if phantom:
        # One bare-qutrit onsite unitary exchanges |vacant> and |1> here.
        control_inputs[0] = 1
        trace.append("onsite fault: vacant first control input -> |1>")
    else:
        control_inputs[0] = real_predecessor
        real_predecessor = VACANT
        trace.append("predecessor moves real |0> into first control input")
    for i in range(n):
        assert tokens[i] == "LIVE"
        assert control_inputs[i] is not VACANT
        assert target_inputs[i] is not VACANT
        assert control_inputs[i + 1] is VACANT
        c = control_inputs[i]
        target_outputs[i] = target_inputs[i] ^ c
        control_inputs[i + 1] = c
        control_inputs[i] = VACANT
        tokens[i] = "SPENT"
        trace.append(f"CNOT_{i + 1}: control {c}, target output {target_outputs[i]}")
    if phantom:
        assert control_inputs[0] is VACANT
        control_inputs[0] = real_predecessor
        real_predecessor = VACANT
        trace.append("predecessor moves real |0> into spent first input; it is stuck")
    return {
        "target_outputs": target_outputs,
        "terminal_control": control_inputs[n],
        "extra_real_control_at_spent_input": control_inputs[0] if phantom else None,
        "all_CNOT_tokens_spent": all(x == "SPENT" for x in tokens),
        "trace": trace,
    }


if __name__ == "__main__":
    n = 6
    clean = run(n, False)
    bad = run(n, True)
    assert clean["target_outputs"] == [0] * n
    assert bad["target_outputs"] == [1] * n
    assert bad["extra_real_control_at_spent_input"] == 0
    result = {
        "scope": "bare qutrit one-shot rail; explicit finite control trace only",
        "N": n,
        "clean": clean,
        "one_onsite_fault": bad,
        "interpretation": "A counterfeit packet and extra stuck real packet require a lineage/EC/final-hold rule. The N wrong target values alone are ordinary propagation and do not prove N bad exRecs.",
    }
    (HERE / "PHANTOM_CHAIN_RESULTS.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
