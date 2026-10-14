"""Exact synthetic checks for the two-pool isotope port-audit example.

No experimental data are loaded or claimed. Run with Python 3 standard library.
"""

import json
from fractions import Fraction as F


def frac(x):
    return str(x)


k = F(1, 100)
b0 = F(2)
c0 = F(2)
b1 = F(3)
c1 = F(3, 2)

# B -> P and C -> Q each have unit first-order exit rate. B <-> C
# exchanges at rate k per molecule in either direction.
h = k / (1 + 2 * k)
t = ((1 - h, h), (h, 1 - h))  # rows P,Q; columns feed B,C

assert all(sum(t[row][col] for row in range(2)) == 1 for col in range(2))
assert h / (1 - 2 * h) == k

baseline_net_exchange = k * (b0 - c0)
baseline_each_way_gross = k * b0
baseline_q_label_from_b = b0 * t[1][0]
candidate_net_exchange = k * (b1 - c1)

assert baseline_net_exchange == 0
assert baseline_each_way_gross == F(1, 50)
assert baseline_q_label_from_b == F(1, 51)
assert candidate_net_exchange == F(3, 200)

# A task-specific hidden-exchange tolerance at the proposed setpoint.
leak_budget = F(1, 200)
max_safe_concentration_split = leak_budget / k
assert max_safe_concentration_split == F(1, 2)
assert b1 - c1 > max_safe_concentration_split

# For a dimensionless log-activity split u around B=C=b, the two-way
# mass-action model predicts v(u) = 2*k*b*sinh(u/2). Check one finite
# split exactly by setting exp(u/2)=3/2; the derivative at u=0 is k*b.
t_split = F(3, 2)
response_direct = k * (b0 * t_split - b0 / t_split)
response_from_gross = baseline_each_way_gross * (t_split - 1 / t_split)
assert response_direct == response_from_gross == F(1, 60)

print(json.dumps({
    "status": "synthetic_exact_fraction_check_only",
    "exchange_rate_k": frac(k),
    "port_transfer_T_rows_P_Q_cols_B_C": [[frac(x) for x in row] for row in t],
    "cross_output_fraction_h": frac(h),
    "baseline_net_B_to_C": frac(baseline_net_exchange),
    "baseline_each_way_gross": frac(baseline_each_way_gross),
    "baseline_Q_label_from_fully_labeled_B_feed": frac(baseline_q_label_from_b),
    "candidate_net_B_to_C": frac(candidate_net_exchange),
    "leak_budget": frac(leak_budget),
    "max_safe_abs_B_minus_C_under_model": frac(max_safe_concentration_split),
    "candidate_passes_model_leak_budget": False,
    "finite_log_activity_split_exp_u_over_2": frac(t_split),
    "finite_split_net_exchange": frac(response_direct),
}, indent=2))
