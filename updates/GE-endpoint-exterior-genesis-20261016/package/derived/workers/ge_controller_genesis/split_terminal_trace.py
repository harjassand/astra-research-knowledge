#!/usr/bin/env python3
"""Reject one naive decomposition; not a no-go for every compiler."""
from pathlib import Path
import json


def data_move_without_phase_commit(state):
    # T's source is selected by the still-old phase. The unowned-destination
    # claim would be false after the first move but before phase commit.
    phase, a, b = state
    if phase % 2 == 0:
        recovered = "U_0(rho)" if a == "rho" else "|0_L>"
        return phase, "vacuum", recovered
    recovered = "U_1(rho)" if b == "rho" else "|0_L>"
    return phase, recovered, "vacuum"


def main():
    trace = [(0, "rho", "vacuum")]
    trace.append(data_move_without_phase_commit(trace[-1]))
    assert trace[-1] == (0, "vacuum", "U_0(rho)")
    trace.append(data_move_without_phase_commit(trace[-1]))
    assert trace[-1] == (0, "vacuum", "|0_L>")
    result = {
        "status": "NAIVE_SPLIT_REJECTED",
        "primitive_noise_faults": 0,
        "events": ["canonical entry", "recover-and-move before phase write",
                   "same recover-and-move fires again before phase write"],
        "trace_phase_A_B": trace,
        "failure": "Second data move clears the live B owner while still believing A owns the packet. Unknown rho is lost.",
        "scope": "Only this separate-move/separate-phase decomposition. A lock/escrow/compiler could avoid the trace, but its noisy proof is absent."}
    (Path(__file__).resolve().parent / "SPLIT_TERMINAL_TRACE.json").write_text(
        json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
