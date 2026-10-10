#!/usr/bin/env python3
"""Small, dependency-free checks for the burst-noise investigation.

This is an analytic contract check, not a device simulation or decoder benchmark.
It evaluates (1) the normalized-state entanglement-fidelity ceiling for a
global replacer event and (2) ideal Hahn-echo phase accumulation for the
reported quasi-static quasiparticle-frequency profile.
"""

from decimal import Decimal, getcontext
import json
from pathlib import Path

getcontext().prec = 60


def global_replacer_bound(k: int, q: Decimal, cycles: int) -> dict:
    """Upper-bound entanglement fidelity for an unrecoverable global event.

    A global replacer event maps the physical register to I/2**n independent
    of the encoded input. For k logical qubits, the event branch has Choi
    overlap 1/4**k with the maximally entangled target. If each cycle has an
    independent event probability q, any event during the computation makes
    that input-reference entanglement unrecoverable.
    """
    d = Decimal(2) ** k
    no_event = (Decimal(1) - q) ** cycles
    event = Decimal(1) - no_event
    branch_fidelity = Decimal(1) / (d * d)
    total_bound = no_event + event * branch_fidelity
    return {
        "logical_qubits": k,
        "event_probability_per_cycle": str(q),
        "cycles": cycles,
        "probability_no_global_event": str(no_event),
        "probability_at_least_one_global_event": str(event),
        "event_branch_entanglement_fidelity": str(branch_fidelity),
        "total_entanglement_fidelity_upper_bound": str(total_bound),
        "entanglement_infidelity_lower_bound": str(Decimal(1) - total_bound),
    }


def hahn_echo_phase(delta_f_hz: Decimal, recovery_s: Decimal,
                    cycle_s: Decimal) -> dict:
    """Integrate a 1/(1+t/tau) frequency shift with and without ideal echo."""
    tau = recovery_s
    t = cycle_s
    two_pi = Decimal("6.2831853071795864769252867665590057683943387987502")
    total_cycles = t / tau
    unrefocused_cycles = delta_f_hz * tau * (Decimal(1) + total_cycles).ln()
    echo_cycles = delta_f_hz * tau * (
        Decimal(2) * (Decimal(1) + total_cycles / Decimal(2)).ln()
        - (Decimal(1) + total_cycles).ln()
    )
    unrefocused_phase = two_pi * unrefocused_cycles
    echo_phase = two_pi * echo_cycles
    ratio = abs(unrefocused_phase / echo_phase) if echo_phase else None
    return {
        "initial_frequency_shift_hz": str(delta_f_hz),
        "recovery_time_s": str(recovery_s),
        "cycle_time_s": str(cycle_s),
        "unrefocused_phase_rad": str(unrefocused_phase),
        "ideal_echo_phase_rad": str(echo_phase),
        "phase_suppression_factor_idealized": str(ratio),
        "assumptions": [
            "shift profile delta_f(t)=delta_f(0)/(1+t/tau)",
            "shift is already in its slowly varying recovery regime",
            "instantaneous, noiseless pi pulse at the cycle midpoint",
            "no gate, measurement, reset, leakage, or T1 errors",
        ],
    }


def main() -> None:
    global_cases = [
        global_replacer_bound(1, Decimal("0.000001"), 1_000),
        global_replacer_bound(1, Decimal("0.000001"), 1_000_000),
        global_replacer_bound(1, Decimal("0.000001"), 10_000_000),
        global_replacer_bound(4, Decimal("0.000001"), 1_000_000),
    ]
    echo_case = hahn_echo_phase(
        Decimal("2000000"), Decimal("0.001"), Decimal("0.000001")
    )
    # Exact endpoint checks for the probability bound.
    assert Decimal(global_replacer_bound(1, Decimal(0), 100)[
        "entanglement_infidelity_lower_bound"
    ]) == 0
    assert Decimal(global_replacer_bound(1, Decimal(1), 1)[
        "total_entanglement_fidelity_upper_bound"
    ]) == Decimal("0.25")
    # In the supplied slow-profile example, ideal echo strongly suppresses
    # phase, but this is explicitly not an end-to-end fault-tolerance result.
    assert Decimal(echo_case["phase_suppression_factor_idealized"]) > Decimal(3900)

    result = {
        "status": "completed",
        "global_replacer_checks": global_cases,
        "idealized_qp_phase_echo_check": echo_case,
        "scope": "analytic boundary and control-integral checks only",
    }
    out = Path(__file__).with_name("results.json")
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
