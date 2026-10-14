"""Floating-point diagnostics for the scoped three-snapshot ring calculation.

This verifies formulas, not the universal affinity or reflection proof.  It uses
only the Python standard library.  No laboratory or Monte Carlo data is used.
"""

import math


def matmul(left, right):
    return [
        [sum(left[i][k] * right[k][j] for k in range(3)) for j in range(3)]
        for i in range(3)
    ]


def transition_by_uniformization(generator, time, escape, terms=50):
    step = [
        [float(i == j) + generator[i][j] / escape for j in range(3)]
        for i in range(3)
    ]
    power = [[float(i == j) for j in range(3)] for i in range(3)]
    result = [[0.0] * 3 for _ in range(3)]
    weight = math.exp(-escape * time)
    for n in range(terms):
        for i in range(3):
            for j in range(3):
                result[i][j] += weight * power[i][j]
        power = matmul(power, step)
        weight *= escape * time / (n + 1)
    return result


q = 1 / 20
t = 3 / 10
s = 1 + q
omega = math.sqrt(3) * (1 - q) / 2
generator = [[-s, 1, q], [q, -s, 1], [1, q, -s]]
transition = transition_by_uniformization(generator, t, s)
g1 = transition[1][1] + transition[1][2]
g2 = transition[2][1] + transition[2][2]
a = (g1 + g2) / 2
b = g1 * g2
D = (2 / 3) * (a * a - b)

closed_a = 2 / 3 + math.exp(-3 * s * t / 2) * math.cos(omega * t) / 3
closed_D = 2 * math.exp(-3 * s * t) * math.sin(omega * t) ** 2 / 9
assert abs(a - closed_a) < 1e-14
assert abs(D - closed_D) < 1e-14
assert all(abs(sum(row) - 1) < 1e-14 for row in transition)

score_min = -a * (1 - a)
score_range = max(a, 1 - a)
floor = -math.log1p(-D / (-score_min)) / t
target_sigma = (1 - q) * math.log(1 / q)
independent_windows = math.ceil(
    2 * score_range**2 * math.log(40) / D**2
)

print(f"a={a:.16g}")
print(f"b={b:.16g}")
print(f"D={D:.16g}")
print(f"refined_floor={floor:.16g}")
print(f"target_ring_sigma={target_sigma:.16g}")
print(f"iid_window_planning_budget={independent_windows}")
