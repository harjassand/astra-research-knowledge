#!/usr/bin/env python3
"""Exact rational examples of information limitations; no physical simulation."""
from fractions import Fraction as F
import json
from pathlib import Path


def mul(a, b):
    return [[sum(x * y for x, y in zip(row, col)) for col in zip(*b)] for row in a]


def encode(a):
    return [[str(x) for x in row] for row in a]


def main():
    # Equal-mass response cannot distinguish the desired/undesired split,
    # even when the total amount is known exactly.
    a = [[F(1), F(1)]]
    q1, q2 = [[F(3)], [F(1)]], [[F(1)], [F(3)]]
    assert mul(a, q1) == mul(a, q2)
    assert q1[0] != q2[0]

    # Even rank-two optical measurements across multiple interventions do not
    # identify concentrations when both pure response vectors are unknown.
    # This column-stochastic transform also preserves every sample's total.
    spectra = [[F(1), F(2)], [F(2), F(1)]]
    concentrations = [[F(4), F(3)], [F(2), F(4)]]
    transform = [[F(9, 10), F(1, 10)], [F(1, 10), F(9, 10)]]
    inverse = [[F(9, 8), F(-1, 8)], [F(-1, 8), F(9, 8)]]
    changed_spectra = mul(spectra, transform)
    changed_concentrations = mul(inverse, concentrations)
    assert mul(transform, inverse) == [[F(1), F(0)], [F(0), F(1)]]
    assert mul(spectra, concentrations) == mul(changed_spectra, changed_concentrations)
    assert all(x > 0 for row in changed_spectra + changed_concentrations for x in row)
    assert [sum(c) for c in zip(*concentrations)] == [sum(c) for c in zip(*changed_concentrations)]
    assert concentrations[0] != changed_concentrations[0]

    # One known independent channel would suffice for the specified TWO-product
    # problem. This matrix is an assumption, not an acquired instrument.
    calibrated = [[F(1), F(1)], [F(3, 4), F(1, 4)]]
    reconstruction = [[F(-1, 2), F(2)]]
    assert mul(reconstruction, calibrated) == [[F(1), F(0)]]

    # The same bond reporter cannot distinguish a third molecule that contains
    # the tagged desired bond but differs elsewhere in its structure.
    expanded = [[F(1), F(1), F(1)], [F(3, 4), F(1, 4), F(3, 4)]]
    desired_only = [[F(1)], [F(0)], [F(0)]]
    other_same_bond = [[F(0)], [F(0)], [F(1)]]
    assert mul(expanded, desired_only) == mul(expanded, other_same_bond)

    result = {
        "status": "EXACT_FINITE_INFORMATION_EXAMPLES_ONLY",
        "equal_mass": {"response": encode(a), "q1": encode(q1), "q2": encode(q2), "same_observation": encode(mul(a, q1))},
        "unknown_spectrum_ambiguity": {
            "spectra": encode(spectra), "concentrations": encode(concentrations),
            "transform": encode(transform), "changed_spectra": encode(changed_spectra),
            "changed_concentrations": encode(changed_concentrations),
            "same_observation": encode(mul(spectra, concentrations)),
            "sample_totals_preserved": True,
        },
        "calibrated_independent_channel": {"assumed_response": encode(calibrated), "desired_readout_weights": encode(reconstruction)},
        "incomplete_structure_counterexample": {"assumed_response": encode(expanded), "same_observation": encode(mul(expanded, desired_only))},
        "physical_validation": "NONE",
        "novelty": "Standard linear algebra and matrix factorization reasoning; no novelty claim",
        "inference_cost": "UNKNOWN",
    }
    destination = Path(__file__).with_name("INFORMATION_BOUNDARY_CHECK.json")
    destination.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"status": result["status"], "output": str(destination.resolve())}))


if __name__ == "__main__":
    main()
