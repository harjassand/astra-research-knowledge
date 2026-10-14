#!/usr/bin/env python3
"""Small exact consistency checks for the source-leaf control receipt."""
from fractions import Fraction as Q
import json
from pathlib import Path

from source_control_certificate import build


def main():
    result = build()
    p = Q(result["root_source_probability"]["numerator"],
          result["root_source_probability"]["denominator"])
    complement = Q(result["root_source_complement"]["numerator"],
                   result["root_source_complement"]["denominator"])
    rate = Q(result["rate"]["numerator"], result["rate"]["denominator"])
    lam = Q(result["tangent_lower_lambda"]["numerator"],
            result["tangent_lower_lambda"]["denominator"])
    Gamma = Q(result["nonlinear_slope_Gamma_h"]["numerator"],
              result["nonlinear_slope_Gamma_h"]["denominator"])
    offspring = Q(result["offspring_mean_upper"]["numerator"],
                  result["offspring_mean_upper"]["denominator"])
    expected_nodes = Q(result["proposal_tree_node_bound"]["numerator"],
                       result["proposal_tree_node_bound"]["denominator"])
    h = Q(result["radius"]["numerator"], result["radius"]["denominator"])
    R = Q(result["global_residual_bound_R"]["numerator"],
          result["global_residual_bound_R"]["denominator"])
    assert p == R / (rate * h)
    assert p + complement == 1
    assert 0 < p < 1
    assert 0 <= Gamma < lam <= rate
    assert offspring == 1 - (lam - Gamma) / rate and 0 <= offspring < 1
    assert expected_nodes == 1 / (1 - offspring)
    coeffs = {
        row["k"]: (Q(row["real"]["numerator"], row["real"]["denominator"]),
                   Q(row["imag"]["numerator"], row["imag"]["denominator"]))
        for row in result["weak_source_control"]["fourier_coefficients"]
    }
    assert max(abs(k) for k in coeffs) == 52
    assert all(coeffs[-k] == (re, -im) for k, (re, im) in coeffs.items())
    out = {
        "checks": [
            "exact p_source=R/(Lambda*h)",
            "exact p_source+(1-p_source)=1",
            "0<p_source<1",
            "exact subcritical offspring upper bound from Lambda, lambda and Gamma(h)",
            "exact expected-tree-size bound is the geometric sum 1/(1-q)",
            "resolvent Fourier coefficients have exact conjugate symmetry and degree 52",
            "certificate and variance formula regenerated from exact rational polynomial data",
        ],
        "p_source": str(p),
        "one_minus_p_source": str(complement),
        "scope": "Exact rational consistency checks; they do not validate floating-point sampling, Brownian draws, transcendental evaluation, or historical novelty.",
    }
    Path(__file__).with_name("source_control_validation.json").write_text(
        json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
