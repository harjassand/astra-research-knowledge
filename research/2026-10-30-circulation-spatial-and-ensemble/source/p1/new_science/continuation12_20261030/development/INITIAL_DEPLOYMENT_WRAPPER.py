#!/usr/bin/env python3
"""Export the fixed-gate deployment rule after the one preserved calibration.

This runs no new validation and claims no physical deployment. The callable
selection rule returns the actual reference on any failed qualification.
"""
from __future__ import annotations
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FIXED_TV_GATE = 0.16
VALIDATION_FAILURE_PROBABILITY = 0.01


def choose_policy(candidate, reference, tv_upper):
    accepted = math.isfinite(tv_upper) and 0 <= tv_upper <= FIXED_TV_GATE
    chosen = candidate if accepted else reference
    return {str(r): tuple(word) for r, word in chosen.items()}, accepted


def execute_post_prefix(call_operation, retained_r, chosen_policy):
    """Consume a supplied post-prefix specimen through its actual call port.

    Fresh conditional input, the common prefix, noninvasive label read and
    actual operation precision are the documented physical supplier duties.
    This function adds no hidden readout or initializer.
    """
    for operation in chosen_policy[str(retained_r)]:
        call_operation(operation)


def main():
    source = ROOT / "ENSEMBLE_ECHO_LEARNING_CHECK_RESULTS.json"
    result = json.loads(source.read_text())
    validation = result["validation"]
    assert validation["requested_TV"] == FIXED_TV_GATE
    assert validation["confidence"] == 1 - VALIDATION_FAILURE_PROBABILITY
    chosen, accepted = choose_policy(result["selected_words"], result["reference_words"],
                                    validation["joint_all_future_TV_upper"])
    assert accepted == validation["passed"]
    exported = {
        "scope": "Executed selection/export of a completed protocol; no new validation or physical deployment.",
        "fixed_gate": FIXED_TV_GATE,
        "failure_probability": VALIDATION_FAILURE_PROBABILITY,
        "observed_99_percent_confidence_bound": validation["joint_all_future_TV_upper"],
        "unconditional_joint_calibration_record_TV_bound": FIXED_TV_GATE + VALIDATION_FAILURE_PROBABILITY,
        "accepted": accepted,
        "post_prefix_words": {r: list(w) for r, w in chosen.items()},
        "fallback": "The reference on every branch whenever the fixed gate fails.",
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    (ROOT / "QUALIFIED_DEPLOYMENT_RULE.json").write_text(json.dumps(exported, indent=2) + "\n")
    print(json.dumps(exported, indent=2))


if __name__ == "__main__":
    main()
