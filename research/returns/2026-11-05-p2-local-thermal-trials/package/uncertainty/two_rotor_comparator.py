"""Evaluate proved two-rotor formulas; no exponentially long simulation."""
from __future__ import annotations
import json
import math
from pathlib import Path
from scipy.special import i0e

ROOT = Path(__file__).resolve().parent


def main():
    beta = mass_hidden = gamma = amplitude = 1.
    epsilon = .01
    entropy = math.log(2)+amplitude**2/2
    local_wait = entropy/(4*gamma*epsilon**2)
    cases = []
    for barrier in [5., 10., 20., 30., 50.]:
        b = beta*barrier
        zy = 2*math.pi*float(i0e(b/2))
        crossing = 2*math.exp(-b)/(zy*math.sqrt(2*math.pi*beta*mass_hidden))
        lower = 1/(32*math.exp(amplitude**2)*crossing)
        exact_rhs = .5-math.sqrt(2*math.exp(amplitude**2)*crossing*lower)
        assert abs(exact_rhs-.25) < 1e-14
        assert 4/math.e/math.sqrt(b) <= zy <= math.pi*math.sqrt(math.pi)/math.sqrt(b)
        cases.append({
            "beta_B": b,
            "Z_y": zy,
            "stationary_outward_crossing_flux": crossing,
            "global_TV_quarter_lower_time": lower,
            "clean_local_TV_001_wait": local_wait,
            "global_lower_over_local_bound": lower/local_wait,
            "conditional_Gibbs_y_sampler_expected_proposals": 2*math.pi/zy,
        })
    result = {
        "scope": "Floating evaluation of proved bounds, no path simulation or hardware execution.",
        "parameters": {"beta":beta,"hidden_mass":mass_hidden,"gamma":gamma,
                       "reference_shift_a":amplitude,"local_TV_error":epsilon},
        "reference_inclusive_initial_KL": entropy,
        "initial_density_L2_squared": 2*math.exp(amplitude**2),
        "cases":cases,
        "interpretation": "Exponential separation from global equilibration, not a proved speedup over the best equally informed local approach. Clock, finite metrology, backaction, initialization and reuse costs remain additional.",
    }
    (ROOT/"two_rotor_comparator_results.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))


if __name__ == "__main__":
    main()
