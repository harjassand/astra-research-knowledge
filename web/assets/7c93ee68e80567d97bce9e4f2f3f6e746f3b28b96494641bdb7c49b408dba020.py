#!/usr/bin/env python3
"""Exact arithmetic checks for cycle-3 cancer hidden-state examples.

These are mathematical constructions, not fitted biological parameters.
"""
from fractions import Fraction as F
import json


def moments(outcomes, coord=0, order=1):
    return sum(p * (pair[coord] ** order) for pair, p in outcomes)


def mean_cov_pair(outcomes):
    ex = [sum(p * pair[i] for pair, p in outcomes) for i in (0, 1)]
    exx = [[sum(p * pair[i] * pair[j] for pair, p in outcomes)
            for j in (0, 1)] for i in (0, 1)]
    cov = [[exx[i][j] - ex[i] * ex[j] for j in (0, 1)]
           for i in (0, 1)]
    return ex, cov


# A parent with 100 ecDNA copies has 200 copies available after replication.
# Daughter labels are randomized; both kernels conserve the total of 200.
ec_a = [((60, 140), F(1, 32)), ((140, 60), F(1, 32)),
        ((100, 100), F(15, 16))]
ec_b = [((90, 110), F(1, 2)), ((110, 90), F(1, 2))]

ec_results = {}
for name, law in (("A", ec_a), ("B", ec_b)):
    mean, covariance = mean_cov_pair(law)
    # For K <= 90, L is the number of low-copy daughters from one mitosis.
    low_count = sum(p * sum(k <= 90 for k in pair) for pair, p in law)
    any_low = sum(p for pair, p in law if any(k <= 90 for k in pair))
    # Independent establishment probability q=1/2 for each low-copy daughter.
    q_est = sum(p * (1 - F(1, 2) ** sum(k <= 90 for k in pair))
                for pair, p in law)
    variance = moments(law, 0, 2) - mean[0] ** 2
    fourth_central = sum(p * (pair[0] - mean[0]) ** 4 for pair, p in law)
    fourth_cumulant = fourth_central - 3 * variance ** 2
    tail_one_daughter = sum(p for pair, p in law if pair[0] <= 90)
    ec_results[name] = {
        "mean_pair": [str(x) for x in mean],
        "cov_pair": [[str(x) for x in row] for row in covariance],
        "marginal_variance": str(variance),
        "marginal_fourth_cumulant": str(fourth_cumulant),
        "expected_low_daughters_per_mitosis": str(low_count),
        "probability_any_low_daughter": str(any_low),
        "establishment_probability_per_mitosis_q_half": str(q_est),
        "randomly_labeled_daughter_low_tail": str(tail_one_daughter),
    }

# Exact binomial operating characteristics for a random daughter call.
def binom_tail(n, p, k):
    if p == 0:
        return F(1) if k == 0 else F(0)
    if p == 1:
        return F(1)
    ans = F(0)
    for j in range(k, n + 1):
        ans += F(__import__("math").comb(n, j)) * p**j * (1-p)**(n-j)
    return ans


# 95% sensitivity and 99% specificity for the binary "daughter <=90" call.
sens, spec = F(95, 100), F(99, 100)
p0 = sens * F(1, 32) + (1 - spec) * F(31, 32)
p1 = sens * F(1, 2) + (1 - spec) * F(1, 2)
n, cutoff = 6, 2
test = {
    "sensitivity": str(sens),
    "specificity": str(spec),
    "observed_rate_A": str(p0),
    "observed_rate_B": str(p1),
    "n_independent_divisions": n,
    "reject_B_if_count_at_least": cutoff,
    "type_I_A": str(binom_tail(n, p0, cutoff)),
    "power_B": str(binom_tail(n, p1, cutoff)),
}

# A PGCC burst comparison with equal mean K=4, post-burst q_R=1/2,
# and competing burst/death probabilities both 1/2.
pgcc_a_h = F(1, 2) ** 4
pgcc_b_h = F(3, 4) + F(1, 4) * F(1, 2) ** 16
pgcc = {
    "law_A_h_q": str(pgcc_a_h),
    "law_A_p_establish": str(F(1, 2) * (1 - pgcc_a_h)),
    "law_B_h_q": str(pgcc_b_h),
    "law_B_p_establish": str(F(1, 2) * (1 - pgcc_b_h)),
    "risk_ratio_A_over_B": str((F(1, 2) * (1-pgcc_a_h)) /
                                (F(1, 2) * (1-pgcc_b_h))),
}

result = {
    "status": "exact finite construction; not biologically fitted",
    "ecDNA_partition": ec_results,
    "idealized_binomial_test": test,
    "PGCC_equal_mean_burst_law": pgcc,
}
print(json.dumps(result, indent=2))
