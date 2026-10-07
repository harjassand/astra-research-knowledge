#!/usr/bin/env python3
"""Exact certificate for a two-mode shared-scalar statistical memory codec.

The diagnostic uses rational Laurent polynomials to verify the exact moments
of U(t)=cos(2*pi*t), V(t)=cos(4*pi*t), t uniform on the circle.  It also emits
an exact rational mesh size for the periodic triangular-hat codec.  The proof
of its TV guarantee uses only pi < 22/7 and the stated C^2 interpolation
bound, so no floating quadrature or finite-grid inference is involved.

The codec is an ideal continuous-reference construction: the encoder samples
a label from exact hat probabilities and the decoder samples a continuous
triangular density.  Finite-bit simulation/output costs are not included.
"""

from __future__ import annotations

import argparse
import json
from fractions import Fraction as F
from math import isqrt


Poly = dict[int, F]  # Laurent exponent -> exact coefficient


def clean(p: Poly) -> Poly:
    return {k: v for k, v in p.items() if v}


def add(p: Poly, q: Poly) -> Poly:
    out = dict(p)
    for k, v in q.items():
        out[k] = out.get(k, F(0)) + v
    return clean(out)


def scale(p: Poly, a: F) -> Poly:
    return clean({k: a * v for k, v in p.items()})


def mul(p: Poly, q: Poly) -> Poly:
    out: Poly = {}
    for i, a in p.items():
        for j, b in q.items():
            out[i + j] = out.get(i + j, F(0)) + a * b
    return clean(out)


def cosine(k: int) -> Poly:
    # cos(2*pi*k*t) = (z^k + z^-k)/2, z=exp(2*pi*i*t).
    return {k: F(1, 2), -k: F(1, 2)}


def integral(p: Poly) -> F:
    return p.get(0, F(0))


def ceil_sqrt_fraction(q: F) -> int:
    if q < 0:
        raise ValueError("square-root argument must be nonnegative")
    if q == 0:
        return 0
    # Find the least n with n^2 * denominator >= numerator.
    n = isqrt(q.numerator // q.denominator)
    while n * n * q.denominator < q.numerator:
        n += 1
    while n > 0 and (n - 1) * (n - 1) * q.denominator >= q.numerator:
        n -= 1
    return n


def fraction_string(x: F) -> str:
    return f"{x.numerator}/{x.denominator}"


def verify_exact_joint_posterior() -> dict[str, object]:
    u = cosine(1)
    v = cosine(2)
    one: Poly = {0: F(1)}
    relation_residual = add(v, scale(add(scale(mul(u, u), F(2)), scale(one, F(-1))), F(-1)))
    assert relation_residual == {}

    eu, ev = integral(u), integral(v)
    eu2, ev2 = integral(mul(u, u)), integral(mul(v, v))
    euv = integral(mul(u, v))
    eu2v = integral(mul(mul(u, u), v))
    eu4 = integral(mul(mul(u, u), mul(u, u)))
    var_u2 = eu4 - eu2 * eu2
    var_v = ev2 - ev * ev
    cov_u2_v = eu2v - eu2 * ev

    assert (eu, ev) == (F(0), F(0))
    assert (eu2, ev2, euv) == (F(1, 2), F(1, 2), F(0))
    assert (eu2v, eu4, var_u2, var_v, cov_u2_v) == (
        F(1, 4), F(3, 8), F(1, 8), F(1, 2), F(1, 4)
    )
    assert cov_u2_v * cov_u2_v == var_u2 * var_v  # exact correlation +1

    rho = F(1, 4)
    fisher_diagonal = rho * rho * eu2
    fisher_off_diagonal = rho * rho * euv
    assert fisher_diagonal == F(1, 32)
    assert fisher_off_diagonal == F(0)

    return {
        "reference": "uniform t on [0,1) with endpoints identified",
        "features": ["U=cos(2*pi*t)", "V=cos(4*pi*t)"],
        "exact_relation": "V=2*U^2-1",
        "means": [fraction_string(eu), fraction_string(ev)],
        "covariance_matrix": [
            [fraction_string(eu2), fraction_string(euv)],
            [fraction_string(euv), fraction_string(ev2)],
        ],
        "covariance_rank": 2,
        "nonlinear_dependence_witness": {
            "cov(U^2,V)": fraction_string(cov_u2_v),
            "var(U^2)": fraction_string(var_u2),
            "var(V)": fraction_string(var_v),
            "correlation(U^2,V)": "+1 exactly",
        },
        "likelihood": "f_v(t)=1+(1/4)*(v1*U(t)+v2*V(t)), ||v||_2<=1",
        "fisher_gram": [
            [fraction_string(fisher_diagonal), fraction_string(fisher_off_diagonal)],
            [fraction_string(fisher_off_diagonal), fraction_string(fisher_diagonal)],
        ],
        "uniform_density_lower_bound": "f_v(t)>5/8, using sqrt(2)<3/2",
        "joint_feature_law": "singular on the parabola V=2*U^2-1",
    }


def certify_codec(epsilon: F) -> dict[str, object]:
    if epsilon <= 0:
        raise ValueError("epsilon must be positive")

    # For f_v=1+rho(v1 cos(2*pi*t)+v2 cos(4*pi*t)), rho=1/4,
    # ||f_v''||_infinity <= pi^2*sqrt(17) < 5*pi^2 < 5*(22/7)^2.
    second_derivative_bound = F(5 * 22 * 22, 7 * 7)
    tv_constant = F(5, 48) * second_derivative_bound
    j = max(3, ceil_sqrt_fraction(tv_constant / epsilon))
    tv_bound = tv_constant / (j * j)
    assert tv_bound <= epsilon

    return {
        "codec": "periodic triangular hats on J equally spaced circle nodes",
        "epsilon": fraction_string(epsilon),
        "second_derivative_bound_M2": fraction_string(second_derivative_bound),
        "uniform_TV_bound": f"{fraction_string(tv_constant)}/J^2",
        "J": j,
        "exact_TV_certificate": fraction_string(tv_bound),
        "label_alphabet_size": j,
        "ideal_memory_bits": f"log2({j})",
        "fixed_binary_label_bits": j.bit_length() if j & (j - 1) else j.bit_length() - 1,
        "proof": [
            "Each hat has integral 1/J; encoder chooses node j with probability phi_j(t).",
            "Decoder density given j is J*phi_j(y), so the uniform reference is preserved exactly.",
            "The conditional triangular mean is its node and variance is 1/(6*J^2).",
            "Taylor averaging contributes at most M2/(12*J^2); linear interpolation contributes M2/(8*J^2).",
            "Thus sup-norm error is at most 5*M2/(24*J^2), hence TV at most 5*M2/(48*J^2).",
        ],
        "cost_boundary": "continuous label sampling and continuous decoder output are idealized; finite-bit randomization, output precision, and calibration are excluded",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--epsilon", default="1/1000", help="positive rational TV tolerance")
    parser.add_argument("--output", default="", help="optional JSON output path")
    args = parser.parse_args()
    result = {
        "status": "exact rational diagnostic and analytic codec certificate",
        "joint_posterior": verify_exact_joint_posterior(),
        "codec_certificate": certify_codec(F(args.epsilon)),
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(rendered)
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
