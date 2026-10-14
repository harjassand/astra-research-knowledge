"""Compare source runtime binary floats with exact rational analytic envelopes."""
from fractions import Fraction as Q
import json
import nonlinear_query_plain as source


def show(x):
    return {"fraction": f"{x.numerator}/{x.denominator}",
            "decimal": float(x)}


def relation(binary_float, exact):
    got = Q.from_float(float(binary_float))
    if got < exact:
        side = "below_exact_envelope"
    elif got > exact:
        side = "above_exact_envelope"
    else:
        side = "exact"
    return {"runtime_float": repr(float(binary_float)), "relation": side,
            "delta": show(got - exact)}


def run():
    E = 10 * (Q(45, 100) / 102 + Q(3, 10) / 150 + Q(1, 4) / 270)
    vlo, vhi = 1 - E, 1 + E
    R = 25 * (6 * E**2 + 4 * E**3 + E**4)
    exact = {
        "amp": E,
        "residual_envelope": R,
        "tangent_lower": 1 + 100 * vlo**3,
        "tangent_upper": 1 + 100 * vhi**3,
        "B2": 150 * vhi**2,
        "B3": 100 * vhi,
        "B4": Q(25),
    }
    cert = source.certificate(1)
    runtime = {
        "amp": 10 * (.45 / 102 + .30 / 150 + .25 / 270),
        "residual_envelope": cert.residual_bound,
        "tangent_lower": cert.tangent_lower,
        "tangent_upper": cert.proposal_rate,
        "B2": cert.b2,
        "B3": cert.b3,
        "B4": cert.b4,
    }
    comparisons = {name: relation(runtime[name], exact[name]) for name in exact}
    h = Q(11, 1000)
    exact_slack = (exact["tangent_lower"] * h - exact["residual_envelope"] -
                   exact["B2"] * h**2 - exact["B3"] * h**3 - exact["B4"] * h**4)
    exact_slope = (2 * exact["B2"] * h + 3 * exact["B3"] * h**2 +
                   4 * exact["B4"] * h**3)
    float_params = {name: Q.from_float(float(runtime[name])) for name in runtime}
    hf = Q.from_float(float(cert.radius))
    binary_param_slack = (float_params["tangent_lower"] * hf -
                          float_params["residual_envelope"] -
                          float_params["B2"] * hf**2 -
                          float_params["B3"] * hf**3 -
                          float_params["B4"] * hf**4)
    binary_param_slope = (2 * float_params["B2"] * hf +
                          3 * float_params["B3"] * hf**2 +
                          4 * float_params["B4"] * hf**3)
    return {
        "method": "source copy runtime floats converted to exact rationals; no tolerance",
        "source_float_certificate": {
            "slack_reported": cert.envelope_slack,
            "slope_reported": cert.nonlinear_slope,
            "exact_recomputed_slack_from_binary_parameters": show(binary_param_slack),
            "exact_recomputed_slope_from_binary_parameters": show(binary_param_slope),
        },
        "mathematical_rational_certificate": {
            "radius": "11/1000",
            "exact_slack": show(exact_slack),
            "exact_slope": show(exact_slope),
        },
        "runtime_bound_comparisons": comparisons,
        "scope": "Detects rounding directions in certificate constants; does not prove the actual trigonometric residual attains an envelope or that floating sampler probabilities were violated.",
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
