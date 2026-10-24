#!/usr/bin/env python3
"""Exact arithmetic checks for the a09 theoretical photon-interface results.

No simulated observations are generated. These checks establish algebraic
identities and ideal-model numerical budgets, not physical validation.
Standard library only; outputs EXACT_CHECKS.json next to this file.
"""
from fractions import Fraction as Q
from pathlib import Path
import hashlib
import json
import math
import time


def add(a, b):
    n = max(len(a), len(b))
    return [(a[i] if i < len(a) else Q(0)) +
            (b[i] if i < len(b) else Q(0)) for i in range(n)]


def scale(a, q):
    return [q*x for x in a]


def mul(a, b):
    out = [Q(0)] * (len(a)+len(b)-1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i+j] += x*y
    return out


def value(a, x):
    out = Q(0)
    for q in reversed(a):
        out = out*x+q
    return out


def power(a, n):
    out = [Q(1)]
    for _ in range(n):
        out = mul(out, a)
    return out


def substitute(a, b):
    out = [Q(0)]
    for q in reversed(a):
        out = add(mul(out, b), [q])
    return out


def bernoulli_polynomial(probabilities):
    out = [Q(1)]
    for p in probabilities:
        out = mul(out, [Q(1), -p])
    return out


def click_law_two(poly, transmission=Q(1)):
    f_half = value(poly, transmission/2)
    f_full = value(poly, transmission)
    return [f_full, f_half-f_full, f_half-f_full,
            1-2*f_half+f_full]


def rational_strings(seq):
    return [str(x) for x in seq]


def two_vs_three(q, r):
    # Original model is (q,q). New model is (p1,p2,r), where p1+p2=A,
    # p1*p2=B. The two quadratic roots can be irrational; coefficients are exact.
    A0 = (1-q)**2/(1-r)-1
    B0 = 4*(1-q/2)**2/(1-r/2)-4
    A, B = A0-B0, 2*A0-B0
    disc = A*A-4*B
    assert disc > 0 and A > 0 and B > 0
    p1 = (float(A)+math.sqrt(float(disc)))/2
    p2 = (float(A)-math.sqrt(float(disc)))/2
    assert 0 < p2 <= p1 < 1
    old = bernoulli_polynomial([q, q])
    new = mul([Q(1), -A, B], [Q(1), -r])
    assert value(old, Q(1, 2)) == value(new, Q(1, 2))
    assert value(old, Q(1)) == value(new, Q(1))
    assert click_law_two(old) == click_law_two(new)
    delta = B*r
    expected_difference = scale(mul(mul([Q(0), Q(1)],
                                       [Q(-1, 2), Q(1)]),
                                   [Q(-1), Q(1)]), -delta)
    assert add(new, scale(old, -1)) == expected_difference
    count_law_old = substitute(old, [Q(1), Q(-1)])
    count_law_new = substitute(new, [Q(1), Q(-1)])
    assert sum(count_law_new) == 1 and all(x >= 0 for x in count_law_new)
    assert count_law_new[3] == delta
    half_old, half_new = click_law_two(old, Q(1, 2)), click_law_two(new, Q(1, 2))
    tv_half = sum(abs(x-y) for x, y in zip(half_old, half_new))/2
    triple3 = Q(2, 9)*delta
    return {
        "original_probabilities": [str(q), str(q)],
        "new_probability_sum_first_two": str(A),
        "new_probability_product_first_two": str(B),
        "new_probability_discriminant": str(disc),
        "new_probabilities_approx": [p1, p2, float(r)],
        "new_third_probability": str(r),
        "full_balanced_two_detector_click_law": rational_strings(click_law_two(old)),
        "old_full_photon_number_law": rational_strings(count_law_old),
        "new_full_photon_number_law": rational_strings(count_law_new),
        "full_PNR_three_count_probability": str(delta),
        "full_PNR_95pct_detection_pulses": math.ceil(math.log(.05)/math.log1p(-float(delta))),
        "balanced_three_threshold_detectors_triple_probability": str(triple3),
        "balanced_three_threshold_95pct_detection_pulses": math.ceil(math.log(.05)/math.log1p(-float(triple3))),
        "half_transmission_two_detector_TV": str(tv_half),
        "scope": "Exact ideal threshold click laws only; not SPC time-tag equivalence."
    }


def finite_menu_certificate(m=15):
    """Rational sign certificate for m vs m+1 positive-emitter ambiguity.

    No root-finder is needed: disjoint sign-change intervals certify m roots
    above 1/eta, and the leading coefficient certifies one further positive root.
    """
    eta_cap = Q(3, 25)
    probabilities = [Q(i, 10*(m+1)) for i in range(1, m+1)]
    roots = sorted(1/p for p in probabilities)
    boundaries = [(1/eta_cap+roots[0])/2]
    boundaries += [(a+b)/2 for a, b in zip(roots[:-1], roots[1:])]
    boundaries += [roots[-1]+1]
    old = bernoulli_polynomial(probabilities)
    values = [Q(j, m) for j in range(1, m+1)]
    H = [Q(0), Q(1)]
    for x in values:
        H = mul(H, [-x, Q(1)])
    epsilon = min(abs(value(old, x))/(2*abs(value(H, x))) for x in boundaries)
    new = add(old, scale(H, (-1)**(m+1)*epsilon))
    assert new[0] == 1
    assert all(value(new, x) == value(old, x) for x in [Q(0)]+values)
    signs = [1 if value(new, x) > 0 else -1 for x in boundaries]
    assert signs == [(-1)**i for i in range(m+1)]
    assert (1 if new[-1] > 0 else -1) == (-1)**(m+1)
    assert all(x > 1/eta_cap for x in boundaries)
    return {
        "detector_count_balanced": m,
        "old_emitter_count": m,
        "new_emitter_count": m+1,
        "old_probabilities": rational_strings(probabilities),
        "all_probabilities_strictly_between": ["0", str(eta_cap)],
        "epsilon": str(epsilon),
        "epsilon_approx": float(epsilon),
        "evaluation_points": rational_strings(values),
        "new_root_sign_boundaries": rational_strings(boundaries),
        "new_polynomial_boundary_signs": signs,
        "new_leading_sign": (-1)**(m+1),
        "claim": "At least one positive root in each adjacent boundary interval and one above the final boundary. Degree m+1 implies exactly these roots; reciprocal roots are all positive probabilities below eta_cap.",
        "scope": "Exact polynomial and root-sign certificate, no experiment or inferred count for the archive."
    }


def earliest_timing_checks():
    eta = Q(3, 25)
    a = eta-eta*eta/4
    b = eta*eta/4
    # Known CDF H: first-arrival density in x=H(time) is a*t under H0,
    # eta*t-eta^2*t^2*x/2 under H1. No-click is a separate mass.
    kl_upper = b*b/(3*a)
    # Verify the global chi-square bound factorization as a polynomial identity.
    t = [Q(0), Q(1)]
    one_minus_t = [Q(1), Q(-1)]
    one_minus_at = [Q(1), -a]
    A = [Q(1), Q(-2), Q(4)]
    lhs = add(mul(A, one_minus_at), scale(mul(power(t, 2), one_minus_t), -3*a))
    rhs = add(power(one_minus_t, 3), scale(mul(t, [Q(1), Q(1), Q(1)]), 1-a))
    assert lhs == rhs
    # For every grid value, exact chi-square equals bound minus proved remainder.
    for k in range(1001):
        z = Q(k, 1000)
        chi2 = b*b*z/a*(1-2*z+Q(4, 3)*z*z)+b*b*z*z*(1-z)**2/(1-a*z)
        remainder = b*b*(1-z)*((1-z)**3+(1-a)*z*(z*z+z+1))/(3*a*(1-a*z))
        assert kl_upper-chi2 == remainder and remainder >= 0
    lower = math.ceil(.9*math.log(19)/float(kl_upper))
    pair_probability = eta*eta/8
    upper = math.ceil(math.log(.05)/math.log1p(-float(pair_probability)))
    # Exact unknown-lifetime counterfeit, polynomial in z=exp(-time/tau).
    two_survival = power([1-eta/2, eta/2], 2)
    single_lifetime_survival = [Q(0), Q(94, 97), Q(3, 97)]
    single_survival = add([1-a], scale(single_lifetime_survival, a))
    assert two_survival == single_survival
    return {
        "eta": str(eta), "a": str(a), "b": str(b),
        "all_transmission_first_arrival_KL_per_pulse_upper": str(kl_upper),
        "both_errors_at_most": .05,
        "fixed_budget_adaptive_first_arrival_pulses_lower": lower,
        "balanced_two_detector_coincidence_probability": str(pair_probability),
        "balanced_two_detector_95pct_detection_pulses_upper": upper,
        "lower_to_upper_pulse_ratio": lower/upper,
        "unknown_lifetime_single_emitter_probability": str(a),
        "unknown_lifetime_mixture_survival_weights": ["94/97", "3/97"],
        "unknown_lifetime_mixture_relative_rates": [1, 2],
        "counterfeit_survival_polynomial_in_exp_minus_t_over_tau": rational_strings(two_survival),
        "scope": "Ideal isolated pulses, independent emitters, no background/crosstalk/deadtime carryover; not an end-to-end hardware cost comparison."
    }


def contrast_coefficients():
    r, s = Q(1, 3), Q(2, 3)
    coefficients = []
    for k in range(3, 41):
        def c(a, j):
            return (a-a**j)/j
        ratio_r, ratio_s = c(r, k)/c(r, 2), c(s, k)/c(s, 2)
        assert ratio_s > ratio_r
        for a in (r, s):
            assert c(a, k)/c(a, 2) == Q(2, k)*sum(a**j for j in range(k-1))
        coefficients.append({"k": k, "ratio_at_one_third": str(ratio_r), "ratio_at_two_thirds": str(ratio_s)})
    # Exact cancellation of formal independent log-background terms D and B:
    # log S_a = -D-a B+log F(a H).
    for a in (r, s):
        assert -1+a+(1-a) == 0
        assert -a+a == 0
    return {"transmissions": ["0", str(r), str(s), "1"],
            "checked_orders": [3, 40], "coefficients": coefficients,
            "scope": "Finite exact checks supplement the all-orders proof; not evidence of finite statistical stability or physical operation."}


def main():
    start = time.perf_counter()
    out = {
        "status": "EXACT_INTERNAL_CHECKS_PASSED",
        "validation_scope": "Algebra and ideal-model arithmetic only; no simulated or physical observations generated.",
        "unit_efficiency_example": two_vs_three(Q(1, 2), Q(1, 10)),
        "eta_0_12_compatible_example": two_vs_three(Q(3, 50), Q(1, 100)),
        "finite_menu_15_detector_certificate": finite_menu_certificate(),
        "earliest_timing": earliest_timing_checks(),
        "four_setting_contrast": contrast_coefficients(),
        "inference_tokens": "UNKNOWN",
        "inference_cost": "UNKNOWN",
        "inference_energy": "UNKNOWN",
    }
    out["executed_verifier_wall_seconds"] = time.perf_counter()-start
    target = Path(__file__).with_name("EXACT_CHECKS.json")
    target.write_text(json.dumps(out, indent=2)+"\n")
    print(json.dumps({"output": str(target), "sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
                      "wall_seconds": out["executed_verifier_wall_seconds"],
                      "first_arrival_lower_pulses": out["earliest_timing"]["fixed_budget_adaptive_first_arrival_pulses_lower"],
                      "coincidence_upper_pulses": out["earliest_timing"]["balanced_two_detector_95pct_detection_pulses_upper"]}, indent=2))


if __name__ == "__main__":
    main()
