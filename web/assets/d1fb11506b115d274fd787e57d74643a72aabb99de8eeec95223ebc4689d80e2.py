#!/usr/bin/env python3
"""Check likelihood coarsening with a non-faithful net-average reference."""
import json
import math
import numpy as np

d = 3
e = [np.eye(d, dtype=complex)[:, j] for j in range(d)]
P = [np.outer(v, v.conj()) for v in e]
centers = [P[0], P[1]]
n = len(centers)
sigma = sum(centers) / n

# The full-domain EB map measures in the basis and prepares the same basis state.
effects = P
prepared = P
assert np.linalg.norm(sum(effects) - np.eye(d)) < 1e-12

def probabilities(state):
    return np.array([np.trace(m @ state).real for m in effects])

p0 = probabilities(sigma)
pis = [probabilities(rho) for rho in centers]
ratios = []
for i in range(n):
    row = []
    for y in range(len(effects)):
        # If p0(y)=0, domination rho_i <= n sigma forces p_i(y)=0 too.
        assert p0[y] == 0 or pis[i][y] <= n * p0[y] + 1e-12
        assert p0[y] != 0 or abs(pis[i][y]) < 1e-12
        row.append(0.0 if p0[y] == 0 else pis[i][y] / p0[y])
    ratios.append(row)

delta = 0.5
groups = {}
for y in range(len(effects)):
    key = tuple(math.floor(ratios[i][y] / delta + 1e-12) for i in range(n))
    groups.setdefault(key, []).append(y)

coarse_effects = []
coarse_prepared = []
for ids in groups.values():
    coarse_effects.append(sum((effects[y] for y in ids), np.zeros((d, d), complex)))
    mass = float(sum(p0[y] for y in ids))
    if mass == 0:
        # The cell has zero probability on every net center; any state is valid.
        coarse_prepared.append(P[0])
    else:
        coarse_prepared.append(sum((p0[y] * prepared[y] for y in ids),
                                   np.zeros((d, d), complex)) / mass)
assert np.linalg.norm(sum(coarse_effects) - np.eye(d)) < 1e-12

def output(state, ms, states):
    probs = [float(np.trace(m @ state).real) for m in ms]
    return sum((probs[j] * states[j] for j in range(len(ms))),
               np.zeros((d, d), complex))

net_errors = []
for rho in centers:
    diff = output(rho, effects, prepared) - output(rho, coarse_effects, coarse_prepared)
    net_errors.append(float(np.linalg.svd(diff, compute_uv=False).sum() / 2))

# An off-support nearby state confirms that the coarse channel is still TP and
# the ordinary 2a extension is available despite sigma being rank deficient.
near = 0.99 * P[0] + 0.01 * P[2]
near_error = float(np.linalg.svd(output(near, coarse_effects, coarse_prepared) - near,
                                 compute_uv=False).sum() / 2)
cover_radius = float(np.linalg.svd(near - P[0], compute_uv=False).sum() / 2)

k = math.ceil(n / delta) + 1
assert len(groups) <= k ** n
assert max(net_errors) < 1e-12
assert near_error <= 2 * cover_radius + delta / 2 + 1e-12

print(json.dumps({
    "dimension": d,
    "cover_size": n,
    "reference_rank": int(np.linalg.matrix_rank(sigma)),
    "original_outcomes": len(effects),
    "coarse_outcomes": len(groups),
    "zero_reference_mass_outcomes": int(np.sum(p0 == 0)),
    "mesh": delta,
    "theoretical_outcome_bound": k ** n,
    "net_trace_errors": net_errors,
    "nearby_state_cover_radius": cover_radius,
    "nearby_state_trace_error": near_error,
    "extension_bound": 2 * cover_radius + delta / 2,
    "status": "finite diagnostic passed; the general result is proved in revisions/01_cross_phase_finite_cover_compression.txt"
}, indent=2))
