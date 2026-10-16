"""Exact one-state stopped quantum-jump episode and finite path check.

The service clock accepts an identity operation at rate lam. Onsite Z unitary
noise jumps at rate p while waiting. All clocks are independent/exogenous.
This is a quantitative counterexample to interpreting an all-path KL failure
as a nonzero lower bound on output error.
"""

from __future__ import annotations

import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def episode(lam: float, p: float, truncation: int = 100):
    assert lam > 0 and p >= 0
    step_fault = p / (lam + p)
    step_service = lam / (lam + p)
    finite_even = sum(step_service * step_fault**n
                      for n in range(truncation + 1) if n % 2 == 0)
    finite_odd = sum(step_service * step_fault**n
                     for n in range(truncation + 1) if n % 2 == 1)
    odd = p / (lam + 2 * p)
    even = (lam + p) / (lam + 2 * p)
    assert abs(even + odd - 1) < 1e-12
    assert abs(finite_even - even) <= step_fault ** (truncation + 1) + 1e-12
    assert abs(finite_odd - odd) <= step_fault ** (truncation + 1) + 1e-12
    return {
        "service_rate": lam,
        "onsite_unitary_Z_jump_rate": p,
        "path_Kraus_span_contains": ["I", "Z"] if p > 0 else ["I"],
        "full_qubit_KL_exact_recovery": p == 0,
        "accepted_even_Z_probability": even,
        "accepted_odd_Z_probability": odd,
        "unconditional_channel": "even*id + odd*Ad_Z",
        "unhalved_diamond_distance_to_id": 2 * odd,
        "probability_at_least_one_noise_jump_before_service": step_fault,
        "generic_bad_branch_diamond_upper_bound": 2 * step_fault,
        "finite_path_partial_weights": {"even": finite_even, "odd": finite_odd},
        "finite_path_tail_bound": step_fault ** (truncation + 1),
        "readout_at_time_T_noncompletion_probability": "exp(-lam*T)",
    }


if __name__ == "__main__":
    result = {
        "scope": "one unencoded qubit, exact Poisson unitary-jump model; no scalable code theorem",
        "examples": [episode(1.0, 0.01), episode(1.0, 0.1)],
    }
    (HERE / "WEIGHTED_EPISODE_RESULTS.json").write_text(
        json.dumps(result, indent=2) + "\n"
    )
    print(json.dumps(result, indent=2))
