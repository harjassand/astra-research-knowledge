#!/usr/bin/env python3
"""Exact scalar audit of exposed uniform-orbit averaging proposal."""
from fractions import Fraction as F
from pathlib import Path
import json


def main():
    # Uniform mean of 2bt on [0,T] equals bT.
    assert 2*F(1, 2) == 1
    # T^3=CD/(8b^2) implies (2bT)^2=CD/(2T).
    assert F(4, 8) == F(1, 2)
    general_cubic_constant = F(3)**3 / 8
    assert general_cubic_constant == F(27, 8)
    c4_cubic_constant = 4*general_cubic_constant
    assert c4_cubic_constant == F(27, 2)
    # Cube of [c4_cubic_constant^(2/3) * 2^(2/3)/3].
    squared_coefficient_cubed = c4_cubic_constant**2 * 4 / 27
    assert squared_coefficient_cubed == 27
    squared_coefficient = 3
    assert squared_coefficient**3 == squared_coefficient_cubed
    # The known nonpositive Gamma remains a scope obstruction only.
    bad_e_cubed = F(1, 8)
    bad_bound_upper = c4_cubic_constant*F(1, 30)*F(1, 8)
    assert bad_bound_upper == F(9, 160)
    assert bad_e_cubed > bad_bound_upper
    result = {
        "status": "EXACT_SCALAR_AVERAGING_IDENTITIES_PASS",
        "provenance": "Root exposed reviewer's averaging proposal after immutable independent baseline; independently checked without reading reviewer proof.",
        "original_general_cubic_constant": "27C/4",
        "improved_general_cubic_constant": "27C/8",
        "C4_cubic_constant": str(c4_cubic_constant),
        "C4_squared_rate_constant": squared_coefficient,
        "C4_squared_rate_exponent": "2/3",
        "same_Psi": True,
        "nonphysical_Gamma_e_cubed": str(bad_e_cubed),
        "nonphysical_Gamma_bound_upper": str(bad_bound_upper),
        "legal_counterexample": False,
        "general_proof_in": "ORBIT_AVERAGING_ADDENDUM.txt",
        "finite_replay_proves_general_theorem": False,
        "external_validation": "UNKNOWN"
    }
    p=Path(__file__).with_name('ORBIT_AVERAGING_REPLAY_RESULT.json')
    p.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({"status": result['status'], "output": str(p),
                      "C4_cubic_constant": str(c4_cubic_constant),
                      "K": squared_coefficient}))


if __name__=='__main__':
    main()
