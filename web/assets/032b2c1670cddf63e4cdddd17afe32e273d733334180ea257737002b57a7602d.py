#!/usr/bin/env python3
"""Reproduce the exact two-state endpoint-aliasing design calculation."""
import json
import math


T = 1.0
alpha = 0.05
q = 0.5 * (1.0 - math.exp(-2.0 * T))


def arm_from_endpoint(name, endpoint, total_rate, horizon=T):
    a = endpoint * total_rate / (1.0 - math.exp(-total_rate * horizon))
    b = total_rate - a
    occupancy = (a / total_rate) * (
        horizon - (1.0 - math.exp(-total_rate * horizon)) / total_rate
    )
    return {
        "name": name,
        "a": a,
        "b": b,
        "lambda": total_rate,
        "endpoint": a / total_rate * (1.0 - math.exp(-total_rate * horizon)),
        "occupancy": occupancy,
    }


u_fast = arm_from_endpoint("U_fast", q, 2.0)
u_slow = arm_from_endpoint("U_slow", q, 1.0)
v = arm_from_endpoint("V", 0.42, 2.0)

# p(t) = c(1-exp(-lambda*t)); solve the derivative of p_fast-p_slow.
c_fast = u_fast["a"] / u_fast["lambda"]
c_slow = u_slow["a"] / u_slow["lambda"]
lambda_fast = u_fast["lambda"]
lambda_slow = u_slow["lambda"]
ratio = c_slow * lambda_slow / (c_fast * lambda_fast)
t_star = -math.log(ratio) / (lambda_fast - lambda_slow)


def target_fraction(arm, time):
    return arm["a"] / arm["lambda"] * (1.0 - math.exp(-arm["lambda"] * time))


p_fast = target_fraction(u_fast, t_star)
p_slow = target_fraction(u_slow, t_star)
delta = abs(p_fast - p_slow)
gap_world_1 = u_fast["occupancy"] - v["occupancy"]
gap_world_2 = v["occupancy"] - u_slow["occupancy"]
choice_u = gap_world_1 / (gap_world_1 + gap_world_2)
regret = gap_world_1 * gap_world_2 / (gap_world_1 + gap_world_2)
founders = math.ceil(2.0 * math.log(1.0 / alpha) / (delta * delta))

result = {
    "model": "A<->B CTMC, constant rates, start in A, no birth/death or classification error",
    "horizon": T,
    "arms": [u_fast, u_slow, v],
    "optimal_intermediate_time_for_U_world_separation": t_star,
    "midpoint_fraction_U_fast": p_fast,
    "midpoint_fraction_U_slow": p_slow,
    "midpoint_separation": delta,
    "world_1_occupancy_gap_U_over_V": gap_world_1,
    "world_2_occupancy_gap_V_over_U": gap_world_2,
    "endpoint_only_minimax_regret": regret,
    "minimax_policy_probability_choose_U": choice_u,
    "alpha": alpha,
    "independent_founders_per_arm_for_midpoint_test_Hoeffding": founders,
}

print(json.dumps(result, indent=2))
