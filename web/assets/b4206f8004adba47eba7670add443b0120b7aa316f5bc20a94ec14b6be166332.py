#!/usr/bin/env python3
"""Reproduce the finite-founder acquisition-bound example in v3.txt.

This is a calculation check for one finite model, not a biological validation.
Uses only the Python standard library.
"""
from collections import deque
from math import exp, log

B = 100
s = 0.99
c = 0.02
eta = 0.01
eps = 0.25
mu_edge = 0.01

# A binary transition table has row coordinate r in {1,2,3}, with
# K(1|e)=r/4 and K(0|e)=1-r/4. The target is the q=3/4 persistence table.
tables = [(r0, r1) for r0 in range(1, 4) for r1 in range(1, 4)]
target = (1, 3)

def neighbors(theta):
    out = []
    for row in range(2):
        for delta in (-1, 1):
            x = list(theta)
            x[row] += delta
            if 1 <= x[row] <= 3:
                out.append(tuple(x))
    return out

# The generic mutation kernel assigns mu_edge to each one-transfer neighbor
# and its residual mass to staying put.
degrees = {theta: len(neighbors(theta)) for theta in tables}
qself_min = min(1.0 - mu_edge * degree for degree in degrees.values())

# Verify the entire mutation graph is connected and compute its maximum
# shortest-path distance to the target.
dist = {target: 0}
queue = deque([target])
while queue:
    theta = queue.popleft()
    for nxt in neighbors(theta):
        if nxt not in dist:
            dist[nxt] = dist[theta] + 1
            queue.append(nxt)
assert set(dist) == set(tables)
ell = max(dist.values())
assert ell == 4 and qself_min == 0.96

retention = s * exp(-c)
alpha = 1.0 - (1.0 - retention * eta * eps) ** B
p_target = retention * qself_min * eps
mean_target = B * p_target
assert mean_target > 1.0

# Smallest fixed point of q=(1-p+p*q)^B, iterating from zero.
q_ext = 0.0
for _ in range(1_000_000):
    q_next = (1.0 - p_target + p_target * q_ext) ** B
    if abs(q_next - q_ext) < 1e-15:
        q_ext = q_next
        break
    q_ext = q_next
else:
    raise RuntimeError("extinction-root iteration did not converge")

path_probability = alpha ** ell
survival_after_target = 1.0 - q_ext
combined_lower_bound = path_probability * survival_after_target

q_env = 0.75
h = -(q_env * log(q_env) + (1.0 - q_env) * log(1.0 - q_env))
mutual_information = log(2.0) - h
conservative_growth_advantage = mutual_information + log(qself_min)
assert conservative_growth_advantage > 0

print(f"table_count={len(tables)}")
print(f"max_mutation_distance={ell}")
print(f"min_self_mutation_probability={qself_min:.12g}")
print(f"per-step_path_success_lower_bound={alpha:.12g}")
print(f"target_embedded_offspring_probability_lower_bound={p_target:.12g}")
print(f"target_embedded_mean_lower_bound={mean_target:.12g}")
print(f"target_GW_extinction_root={q_ext:.12g}")
print(f"conditional_target_survival_lower_bound={survival_after_target:.12g}")
print(f"finite-founder_acquisition_and_survival_lower_bound={combined_lower_bound:.12g}")
print(f"predictive_mutual_information_nats={mutual_information:.12g}")
print(f"conservative_growth_advantage_after_mutation_nats={conservative_growth_advantage:.12g}")
