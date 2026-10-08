"""Enumerate local influences in a four-spin Ising star."""

from itertools import product
import json
import math


M = 3
B = math.atanh(0.5)
A = 6.0
SPINS = tuple(product((-1, 1), repeat=M + 1))


def p_plus(x, i):
    if i == 0:
        local_field = A + B * sum(x[1:])
    else:
        local_field = B * x[0]
    return 1.0 / (1.0 + math.exp(-2.0 * local_field))


influence = [[0.0] * (M + 1) for _ in range(M + 1)]
for i in range(M + 1):
    for j in range(M + 1):
        if i == j:
            continue
        vals = []
        for x in SPINS:
            y = list(x)
            y[j] *= -1
            y = tuple(y)
            vals.append(abs(p_plus(x, i) - p_plus(y, i)))
        influence[i][j] = max(vals)

row_sums = [sum(row) for row in influence]
col_sums = [sum(influence[i][j] for i in range(M + 1))
            for j in range(M + 1)]
weights = [1.0] + [1.0 / M] * M
weighted_ratios = [
    sum(weights[i] * influence[i][j] for i in range(M + 1)) / weights[j]
    for j in range(M + 1)
]

# A pair differing only at the center has local conditional TV 0 at the
# center and 1/2 at each leaf. Its continuous-time Hamming drift is sum(TV)-1.
initial_pair_drift = -1.0 + M * 0.5
weighted_pair_drift = -weights[0] + M * weights[1] * 0.5

z_min = A - (M - 1) * B
closed_form_center_influence = math.sinh(2 * B) / (
    math.cosh(2 * z_min) + math.cosh(2 * B)
)

result = {
    "model": "3-leaf Ising star; dimensionless coupling atanh(1/2), center field 6, leaf fields 0",
    "influence_matrix_output_site_by_changed_site": influence,
    "row_sums": row_sums,
    "column_sums": col_sums,
    "max_row_sum": max(row_sums),
    "weights": weights,
    "weighted_influence_ratios": weighted_ratios,
    "weighted_contraction_margin": 1.0 - max(weighted_ratios),
    "unweighted_hamming_generator_drift_for_center_disagreement": initial_pair_drift,
    "weighted_hamming_generator_drift_for_center_disagreement": weighted_pair_drift,
    "closed_form_center_from_leaf_influence": closed_form_center_influence,
}
print(json.dumps(result, indent=2, sort_keys=True))

assert max(row_sums) < 1.0
assert col_sums[0] > 1.0
assert initial_pair_drift > 0.0
assert max(weighted_ratios) <= 0.5
assert math.isclose(influence[0][1], closed_form_center_influence,
                    rel_tol=1e-10, abs_tol=1e-12)
