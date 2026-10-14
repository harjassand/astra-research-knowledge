#!/usr/bin/env python3
"""Independent Fraction-arithmetic checks for the reduced-constraint illustration.

This verifies the finite-dimensional reduced-constraint illustration only. It
does not satisfy the full quartic integration identity and is not a sharpness
example for planar rank-one-convex quartics.
"""
from fractions import Fraction as F
import json
from pathlib import Path


def q(x):
    r, w, v, s = x
    return w*w + 2*r*v - s*s


def P(x):
    return x[2]*x[2] + x[3]*x[3]


def C(x):
    return x[0]*x[1]*x[1]


def norm4(x):
    return sum(t*t for t in x)**2


rows = []
for eps in (F(1, 2), F(1, 4), F(1, 8), F(1, 16), F(1, 32)):
    p = eps**4
    rare = (1/eps, 1/eps, F(0), F(0))
    v_common = -eps**2/(2*(1-p))
    common = (F(1), F(0), v_common, F(0))
    mean_q = p*q(rare) + (1-p)*q(common)
    delta = p*P(rare) + (1-p)*P(common)
    mean_C = p*C(rare) + (1-p)*C(common)
    m4 = p*norm4(rare) + (1-p)*norm4(common)
    m4_minus_5 = m4 - 5
    exact_m4_minus_5 = p*(-1 + 1/(2*(1-p)) + p/(16*(1-p)**3))
    bracket = -1 + 1/(2*(1-p)) + p/(16*(1-p)**3)
    assert mean_q == 0
    assert delta == eps**4/(4*(1-eps**4))
    assert mean_C == eps
    assert m4_minus_5 == exact_m4_minus_5
    assert bracket < 0
    assert m4 <= 5
    assert mean_C**4/delta == 4*(1-eps**4)
    rows.append({
        "epsilon": str(eps),
        "probability_rare": str(p),
        "common_v": str(v_common),
        "E_q": str(mean_q),
        "delta_EP": str(delta),
        "E_C": str(mean_C),
        "E_norm4": str(m4),
        "E_norm4_minus_5": str(m4_minus_5),
        "moment_excess_bracket": str(bracket),
        "E_C4_over_delta": str(mean_C**4/delta),
    })

# Uniform exact bound on the bracket for 0 < p <= 1/16:
# 1/(2(1-p)) <= 8/15 and p/(16(1-p)^3) <= 16/3375.
uniform_positive_terms = F(8, 15) + F(16, 3375)
assert uniform_positive_terms == F(1816, 3375) < 1

# The tuple cannot be integrated as the directional jet of a quartic: for
# any A=(a_r,a_w,a_v,a_s), D_A C=a_r*w^2+2*a_w*r*w has v^2 coefficient 0,
# while P+lambda*q has v^2 coefficient 1 for every lambda.
directional_C_v2_coefficient = F(0)
Q_v2_coefficient = F(1)
assert directional_C_v2_coefficient != Q_v2_coefficient

# Exact directional identity for the model: U=span(e_r,e_w), q|U=w^2,
# so q-null R in U has form (rho,0,0,0). Since C(r,w,v,s)=r*w^2 is affine
# in r, its second directional derivative in every such R is zero.
result = {
    "model": "q=w^2+2*r*v-s^2; P=v^2+s^2; U=ker(P); C=r*w^2",
    "q_signature": "(2,2)",
    "q_restricted_to_U": "w^2 with radical span(e_r)",
    "directional_closure": "D^2C(Y)[R,R]=0 for every Y and q-null R in U",
    "fourth_moment_excess_identity": "E|X|^4-5=p*(-1+1/(2*(1-p))+p/(16*(1-p)^3))",
    "uniform_bracket_upper_bound": str(uniform_positive_terms - 1),
    "fourth_moment_bound": "E|X|^4 < 5 uniformly for 0<eps<=1/2 by the exact bracket bound",
    "quartic_integration_identity": "fails: D_A C has v^2 coefficient 0 for every A; P+lambda*q has v^2 coefficient 1 for every lambda",
    "scaling_identity": "delta=eps^4/(4*(1-eps^4)), E[C]=eps, E[C]^4/delta=4*(1-eps^4) -> 4",
    "scope": "reduced balanced-moment and cubic-vanishing constraints only; fails full quartic integration identity; no ROC or compatible-gradient realization is asserted",
    "checks": rows,
}
Path(__file__).with_name("independent_quant_checks.json").write_text(
    json.dumps(result, indent=2) + "\n", encoding="utf-8"
)
print("PASS: 5 exact finite-law cases; E[q]=0, E[P]=eps^4/(4(1-eps^4)), E[C]=eps, exact E|X|^4-5 identity")
print("PASS: uniform rational bracket bound 1816/3375 < 1; hence E|X|^4<5 for 0<eps<=1/2")
print("PASS: E[C]^4/E[P]=4(1-eps^4) -> 4; reduced constraints alone do not force exponent >1/4")
print("PASS: exact v^2 coefficient mismatch rules out the quartic integration identity for this tuple")
