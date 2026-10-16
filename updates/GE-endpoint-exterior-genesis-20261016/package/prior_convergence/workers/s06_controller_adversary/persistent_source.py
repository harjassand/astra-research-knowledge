"""Finite-state multiuse program fault with unbounded quantum output fanout.

This is a countermodel for an unrepaired reused program register, not a claim
that the crossed-plaquette construction has chosen this storage implementation.
"""

from __future__ import annotations

import json
import math
from pathlib import Path


HERE = Path(__file__).resolve().parent


def instance(n: int, q: int = 8):
    assert n >= 1 and q >= 2
    # Each fresh |0> data packet meets the same site. Program 0 requests I;
    # program 1 requests H. The one onsite X fault flips 0 -> 1 and no listed
    # ideal transition repairs it. Commit counters progress with every gate.
    correct_counter = 0
    faulted_counter = 0
    program = 1  # after one onsite unitary fault
    output_labels = []
    for _ in range(n):
        assert program == 1
        output_labels.append("|+> rather than |0>")
        correct_counter = (correct_counter + 1) % q
        faulted_counter = (faulted_counter + 1) % q
    assert correct_counter == faulted_counter
    return {
        "fresh_packets": n,
        "primitive_onsite_program_faults": 1,
        "wrong_quantum_outputs": n,
        "counter_residue_clean_and_faulted": correct_counter,
        "all_execution_counters_remain_identical": True,
        "ideal_vs_faulted_output_squared_overlap": 2.0 ** (-n),
        "unhalved_trace_distance_of_pure_outputs": 2.0 * math.sqrt(1.0 - 2.0 ** (-n)),
        "output_labels": output_labels,
    }


if __name__ == "__main__":
    result = {
        "scope": "abstract constant-support multiuse station with an unprotected reused program bit; no encoded program repair or threshold claim",
        "examples": [instance(1), instance(4), instance(8)],
    }
    (HERE / "PERSISTENT_SOURCE_RESULTS.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
