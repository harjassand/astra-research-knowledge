#!/usr/bin/env python3
"""Exact source-leaf control variate certificate for the supplied PDE toy."""
from __future__ import annotations

from fractions import Fraction as Q
import json
import math
from pathlib import Path

from derive_weighted_certificate import add, cosine, l1, powp, resolvent, scale, sine


def encode(q: Q) -> dict[str, object]:
    return {"numerator": q.numerator, "denominator": q.denominator,
            "decimal": float(q)}


def evaluate_float(p, x: float) -> float:
    return math.fsum(float(r) * math.cos(k * x) - float(i) * math.sin(k * x)
                     for k, (r, i) in p.items())


def build() -> dict[str, object]:
    # This is the exact trigonometric polynomial e0 from the incoming package.
    e0 = {}
    e0 = add(e0, cosine(1, Q(3, 68)))
    e0 = add(e0, cosine(7, Q(1, 50)))
    e0 = add(e0, sine(13, Q(1, 108)))
    N_e0 = add(add(scale(powp(e0, 2), Q(150)),
                   scale(powp(e0, 3), Q(100))),
               scale(powp(e0, 4), Q(25)))
    r1 = scale(N_e0, Q(-1))

    E = l1(e0)
    vmin, vmax = 1 - E, 1 + E
    lam = 1 + 100 * vmin**3
    rate = 1 + 100 * vmax**3
    B2, B3, B4 = 150 * vmax**2, 100 * vmax, Q(25)
    h = Q(11, 1000)
    R = 25 * (6 * E**2 + 4 * E**3 + E**4)
    Gamma = 2 * B2 * h + 3 * B3 * h**2 + 4 * B4 * h**3
    p_source = R / (rate * h)
    offspring_mean = 1 - (lam - Gamma) / rate
    expected_nodes = 1 / (1 - offspring_mean)
    q = resolvent(r1, rate=rate)

    assert 0 < p_source < 1
    assert Gamma < lam
    assert q
    q05_float = evaluate_float(q, 0.5)
    q0_exact = sum((real for real, _ in q.values()), Q(0))

    # Standard Bernstein bound for independent corrected trees.  The original
    # package's Hoeffding bound is 2h^2/epsilon^2 * log(2/delta).
    delta = 0.05
    sample_rows = []
    for eps in (1e-3, 1e-4, 1e-5):
        old = (2 * float(h) ** 2 / eps**2) * math.log(2 / delta)
        new = (2 * float(h) ** 2 * float(1 - p_source) / eps**2 +
               4 * float(h) / (3 * eps)) * math.log(2 / delta)
        sample_rows.append({"epsilon": eps, "delta": delta,
                            "package_Hoeffding_samples_upper": math.ceil(old),
                            "corrected_Bernstein_samples_upper": math.ceil(new),
                            "ratio": new / old})

    return {
        "method": "exact rational Fourier algebra and exact rational inequalities",
        "predictor": "incoming nonlinear package Predictor B, v1=1+e0",
        "query": "u(0.5), same point as incoming package",
        "residual": "r1=-150 e0^2-100 e0^3-25 e0^4",
        "rate": encode(rate),
        "tangent_lower_lambda": encode(lam),
        "nonlinear_slope_Gamma_h": encode(Gamma),
        "offspring_mean_upper": encode(offspring_mean),
        "radius": encode(h),
        "global_residual_bound_R": encode(R),
        "root_source_probability": encode(p_source),
        "root_source_probability_decimal": float(p_source),
        "root_source_complement": encode(1 - p_source),
        "proposal_tree_node_bound": encode(expected_nodes),
        "weak_source_control": {
            "q_lambda(x)": "sum_k r1_hat[k] exp(i k x)/(rate+k^2) = ((rate-d^2)^-1 r1)(x)",
            "q_at_x0_exact": encode(q0_exact),
            "q_at_x05_float_only": q05_float,
            "fourier_degree": max(abs(k) for k in q),
            "fourier_coefficients": [
                {"k": k, "real": encode(r), "imag": encode(i)}
                for k, (r, i) in sorted(q.items())
            ],
        },
        "variance_theorem": {
            "corrected_sample": "W=Z-I_root_source*r1(Y)/R",
            "identity": "E[ I_root_source*r1(Y)/R ] = q_lambda(x)/h",
            "boundedness": "W=0 on the root source event; otherwise W=Z and |W|<=1",
            "variance_upper": "Var(W)<=E[W^2]<=1-p_source",
            "bernstein_tail": "P(|h mean(W)-h E W|>=epsilon)<=2 exp(-M epsilon^2/(2 h^2(1-p_source)+(4h epsilon/3)))",
            "tree_work": "The tree and its offspring law are unchanged, so E[nodes]<=rate/(lambda-Gamma(h)); q_lambda evaluation is one target-specific precomputation, not a sampled field.",
        },
        "sample_count_comparison": sample_rows,
        "scope": "The exact theorem assumes ideal endpoint draws and exact evaluation as the supplied theorem does. The float q(0.5) is diagnostic only; interval arithmetic/finite-precision error must be charged in an implementation.",
    }


if __name__ == "__main__":
    result = build()
    path = Path(__file__).with_name("source_control_certificate.json")
    path.write_text(json.dumps(result, indent=2) + "\n")
    summary = {k: v for k, v in result.items() if k != "weak_source_control"}
    summary["q_lambda_x05_float_only"] = result["weak_source_control"]["q_at_x05_float_only"]
    print(json.dumps(summary, indent=2))
