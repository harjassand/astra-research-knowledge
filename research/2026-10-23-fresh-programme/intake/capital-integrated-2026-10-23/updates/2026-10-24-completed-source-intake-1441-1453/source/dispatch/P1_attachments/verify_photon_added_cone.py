#!/usr/bin/env python3
"""Exact algebra and a rational finite-record test of a positive physical cone.

No acquired experimental measurements. All core equalities and the reported
record distances are exact symbolic/rational arithmetic. Decimal values display
exact fractions. The density-operator approximation certificate is analytic.
"""

from decimal import Decimal, localcontext
from fractions import Fraction as F
import json
import sys
from pathlib import Path

sys.set_int_max_str_digits(0)


def display(q):
    with localcontext() as context:
        context.prec = 32
        decimal = str(Decimal(q.numerator) / Decimal(q.denominator))
    return {"numerator": str(q.numerator), "denominator": str(q.denominator),
            "decimal_display": decimal}


def symbolic_identities():
    # Bivariate integer polynomials after clearing D^(j+2),
    # D=1-z+theta*z. All four rates enter linearly, so their four
    # coefficient identities certify the general no-count expression.
    def add(*polys):
        out = {}
        for p in polys:
            for key,value in p.items():
                out[key] = out.get(key, 0)+value
        return {key:value for key,value in out.items() if value}
    def scale(p, a):
        return {key:a*value for key,value in p.items() if a*value}
    def mul(p, q):
        out = {}
        for (z1,t1),a in p.items():
            for (z2,t2),b in q.items():
                key = (z1+z2,t1+t2)
                out[key] = out.get(key, 0)+a*b
        return {key:value for key,value in out.items() if value}
    def mono(z=0,t=0,a=1):
        return {(z,t):a} if a else {}
    one, z, theta = mono(), mono(z=1), mono(t=1)
    D = add(one, scale(z,-1), mul(theta,z))
    omt = add(one,scale(theta,-1))
    def eq(p,q):
        assert not add(p,scale(q,-1))
    checks = []
    for j in range(9):
        gj = mul(mono(j,j+1), D)
        gj_over_theta = mul(mono(j,j), D)
        lower = mul(mono(j-1,j,a=j), mul(theta,mul(D,D))) if j else {}
        derivative_z = add(mul(mono(j-1,j+1,a=j),D) if j else {},
                           mul(mono(j,j+1,a=j+1),omt))
        derivative_theta = add(mul(mono(j,j,a=j+1),D), mono(j+1,j+1,a=-(j+1)))
        gain = mul(z,add(mul(z,derivative_z),gj))
        gain_basis = mono(j+1,j+1,a=j+1)
        loss_basis = add(lower,scale(mul(omt,gj),2*j+1),
                         mul(mul(omt,omt),gain_basis))
        eq(gain,gain_basis)
        eq(derivative_z,loss_basis)
        death = add(lower,scale(mul(theta,gj),-j))
        # b, d, kappa+, kappa- coefficient equations.
        eq(mul(add(z,scale(one,-1)),add(mul(z,derivative_z),gj)),
           scale(mul(theta,derivative_theta),-1))
        eq(mul(add(one,scale(z,-1)),derivative_z),
           add(mul(mul(theta,omt),derivative_theta),death))
        eq(scale(gain,-1),add(derivative_theta,scale(gj_over_theta,-(j+1))))
        eq(scale(derivative_z,-1),
           add(mul(mul(omt,omt),derivative_theta),scale(death,-1),
               scale(gj_over_theta,-(j+1)),gj))
        for theta0 in [F(1,4),F(3,4),F(1)]:
            assert pgf_photon_added(j,theta0,F(1)) == 1
        checks.append({"photon_addition_order": j,
                       "gain_identity": True, "loss_identity": True,
                       "both_mark_no_count_identity": True,
                       "normalization_including_Fock_boundary": True})
    return checks


def pgf_photon_added(j, theta, z):
    return z**j * (theta/(1-(1-theta)*z))**(j+1)


def two_loss_bits(pgf):
    # Loss 1, loss 2, and survival have probabilities 1/3 each per photon.
    # Actual bin survivals are 2/3 then 1/2, with gain off and efficiency 1.
    p00 = pgf(F(1, 3))
    p10 = pgf(F(2, 3))-p00
    p01 = p10
    p11 = 1-2*pgf(F(2, 3))+p00
    return [p00, p01, p10, p11]


def finite_physical_mixture(cells):
    # Vacuum, gain exp(-integrated gain)=3/4, conditioned on one OR click.
    # Its physical density is exactly the UNIFORM positive mixture
    # (1/nu) int_0^nu sigma_{1,1/(1+v)} dv, nu=1/3.
    # Midpoint states have rational theta and EXACT equal rational weights.
    nu = F(1, 3)
    rates = [1/(1+nu*F(2*j+1, 2*cells)) for j in range(cells)]
    def pgf(z):
        return sum((pgf_photon_added(1, r, z) for r in rates), F(0))/cells
    actual = two_loss_bits(lambda z: F(3, 4)*z/(1-F(1, 4)*z))
    approx = two_loss_bits(pgf)
    assert actual == [F(3, 11), F(18, 55), F(18, 55), F(4, 55)]
    assert sum(approx) == 1 and all(x >= 0 for x in approx)
    record_tv = sum((abs(x-y) for x,y in zip(actual,approx)), F(0))/2
    # Analytic physical trace-distance bound:
    # D <= sqrt(2) asinh(sqrt(1/3))/(2*cells).
    # asinh(1/sqrt(3))=log(3)/2, sqrt(2)<1.415, log(3)<1.099.
    # Both elementary strict bounds follow by squaring / exponential series.
    assert F(1415, 1000)**2 > 2
    x = F(1099, 1000)
    # Positive Taylor partial sum certifies exp(1.099)>3, hence log(3)<1.099.
    exp_lower, term = F(1), F(1)
    for n in range(1, 16):
        term *= x/n
        exp_lower += term
    assert exp_lower > 3
    physical_trace_upper = F(1415*1099, 1000*1000*4*cells)
    assert record_tv < physical_trace_upper
    gaussian_mean = F(4, 3)  # Exact mean of the click-conditioned density.
    gaussian = two_loss_bits(lambda z: 1/(1+gaussian_mean*(1-z)))
    gaussian_tv = sum((abs(x-y) for x,y in zip(actual,gaussian)), F(0))/2
    # No positive Poisson mixture can give P(unequal bits)>1/2.
    # The actual probability is 36/55: this is a finite physical test.
    assert actual[1]+actual[2] == F(36, 55)
    conditional_classical_gap = F(36, 55)-F(1, 2)
    whole_record_gap = conditional_classical_gap/4
    return {
        "positive_physical_components": cells,
        "photon_addition_order": 1,
        "all_weights_and_rates_rational": True,
        "actual_conditional_loss_word_probabilities": [display(x) for x in actual],
        "approx_conditional_loss_word_probabilities": [display(x) for x in approx],
        "exact_conditional_record_tv": display(record_tv),
        "analytic_physical_trace_distance_upper": display(physical_trace_upper),
        "all_future_protocols_record_upper_from_this_current_state": display(physical_trace_upper),
        "complete_three_bit_record_tv": display(record_tv/4),
        "same_mean_thermal_conditional_record_tv": display(gaussian_tv),
        "conditional_positive_P_family_gap": display(conditional_classical_gap),
        "complete_three_bit_positive_P_interface_gap": display(whole_record_gap),
        "qualifications": [
            "Complete-law gap applies to models constrained to the same positive Poisson-mixture loss interface after the gain-click branch.",
            "The atomic mixture approximates a genuine physical density; trace-distance contraction covers any common future quantum protocol.",
            "Efficient propagation outside the proved phase-insensitive gain/loss instrument class is not asserted.",
            "Gain exposure log(4/3), loss exposures log(3/2) and log(2), preparation and detectors are supplied access premises."
        ]
    }


def run():
    result = {"scope": "Exact algebra and finite-record computation; not experimental data",
              "symbolic_checks": symbolic_identities(),
              "finite_record": finite_physical_mixture(1024)}
    path = Path(__file__).with_name("PHOTON_ADDED_EXACT_DIAGNOSTIC.json")
    path.write_text(json.dumps(result, indent=2)+"\n")
    concise = {k:(v["decimal_display"] if isinstance(v, dict) and "decimal_display" in v else v)
               for k,v in result["finite_record"].items()
               if k not in {"approx_conditional_loss_word_probabilities", "actual_conditional_loss_word_probabilities"}}
    print(json.dumps({"symbolic_order_cases": len(result["symbolic_checks"]),
                      "finite_record": concise, "output": str(path)}, indent=2))


if __name__ == "__main__":
    run()
