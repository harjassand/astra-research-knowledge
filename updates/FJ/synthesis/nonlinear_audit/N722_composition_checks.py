"""Independent exact identities for composing FJ bounded corrections with N722.

This is a small, dependency-free audit.  It proves rational scale/certificate
identities and records analytic exact cases; it is not a finite-bit sampler.
"""

from fractions import Fraction as Q
import json


def main() -> dict:
    # Three certified coordinate radii and a rational target scale.
    h = (Q(1, 8), Q(1, 16), Q(3, 32))
    sigma = Q(1, 4)
    radius_squared = sum((hi / sigma) ** 2 for hi in h)
    assert radius_squared == Q(29, 64)

    # Exact quartic source certificate from the copied verifier, written here
    # independently so the N722 cost composition can be checked in fractions.
    q = Q(5425, 12928)
    node_bound = 1 / (1 - q)
    assert node_bound == Q(12928, 7503)

    # Exact Poisson-2 identity at the three boundary values of the clipped
    # mean.  Acceptance is exp(w_hat - 1), with mean J=2 acquired vectors per
    # started trial; the worst boundary w_hat=-1 attains the 2e^2 bound.
    poisson_cases = {
        "w_hat=-1": {"acceptance": "exp(-2)", "expected_vectors_per_accepted_factor": "2 exp(2)"},
        "w_hat=0": {"acceptance": "exp(-1)", "expected_vectors_per_accepted_factor": "2 exp(1)"},
        "w_hat=1": {"acceptance": "1", "expected_vectors_per_accepted_factor": "2"},
    }

    # A deliberately value/cost-correlated exact renewal example.  Success
    # costs 100 with probability 1/10, failure costs 1 otherwise.  Starting a
    # new trial is predictable, so E[sum costs to success]=E[C]/P(success).
    p = Q(1, 10)
    c_success, c_failure = Q(100), Q(1)
    mean_trial_cost = p * c_success + (1 - p) * c_failure
    mean_total_cost = mean_trial_cost / p
    explicit_renewal_cost = c_success + (1 - p) / p * c_failure
    assert mean_trial_cost == Q(109, 10)
    assert mean_total_cost == explicit_renewal_cost == Q(109)

    # Exact series-ratio envelopes for the even/odd sinh offspring-degree
    # inversions.  Since 0<h<log(2)<1, the ratios are below these rational
    # bounds uniformly in h.
    even_ratio_bound = Q(1, 12)
    odd_ratio_bound = Q(1, 20)
    even_scan_bound = 1 / (1 - even_ratio_bound) ** 2
    odd_scan_bound = 1 / (1 - odd_ratio_bound) ** 2

    return {
        "scope": "exact rational/analytic identities; ideal real-arithmetic theorem only",
        "bounded_vector_example": {
            "h": [str(x) for x in h],
            "sigma": str(sigma),
            "R_squared": str(radius_squared),
            "R": "sqrt(29)/8",
            "coordinate_bound": "|X_i| <= h_i/sigma",
            "mean": "E[X_i]=(u(x_i)-v(x_i))/sigma",
        },
        "quartic_predictor_A": {
            "offspring_mean_bound_q": str(q),
            "expected_nodes_per_coordinate_sample": str(node_bound),
            "expected_source_nodes_for_r_coordinates": "r * 12928/7503",
            "outer_expected_vector_acquisitions": "<= 2*e^2*m",
            "composed_expected_source_nodes": "<= 2*e^2*m*r*12928/7503",
        },
        "Poisson_factory_boundary_cases": poisson_cases,
        "correlated_cost_renewal_check": {
            "success_probability": str(p),
            "success_cost": str(c_success),
            "failure_cost": str(c_failure),
            "expected_cost_per_trial": str(mean_trial_cost),
            "expected_cost_to_success": str(mean_total_cost),
        },
        "sinh_inverse_cdf": {
            "even_weight_ratio_upper_bound": str(even_ratio_bound),
            "odd_weight_ratio_upper_bound": str(odd_ratio_bound),
            "even_expected_terms_upper_bound": str(even_scan_bound),
            "odd_expected_terms_upper_bound": str(odd_scan_bound),
            "recurrence": "w_(m+2)/w_m = h^2/((m+1)(m+2))",
        },
        "analytic_exact_cases": [
            "R=0: return N(0,I) with zero oracle acquisitions.",
            "Symmetric oracle X law equal to its reflection: clip is odd, so w_hat(y)=0 for every y; the accepted factor is exactly its centered Gaussian proposal, and the m-factor sum is exactly N(0,I).",
            "Deterministic X=a: w(y)=<y,a>, w_hat(y)=clip(<y,a>); the only discrepancy is the explicitly localized Gaussian projection tail |<y,a>|>1.",
            "For any fixed candidate y with w_hat(y)=-1, only J=0 trials accept; success probability is exactly exp(-2), giving equality in the per-factor 2e^2 expected-acquisition bound.",
        ],
    }


if __name__ == "__main__":
    print(json.dumps(main(), indent=2))
