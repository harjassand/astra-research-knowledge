#!/usr/bin/env python3
"""Small diagnostic for finite-net coarsening of a measure-and-prepare channel."""
import json
import math
import numpy as np

I = np.eye(2, dtype=complex)
sx = np.array([[0, 1], [1, 0]], dtype=complex)
sy = np.array([[0, -1j], [1j, 0]], dtype=complex)
sz = np.diag([1, -1]).astype(complex)
paulis = [sx, sy, sz]

# Three net states around sigma=I/2, all with Bloch norm <= theta.
theta = 0.6
bloch = [np.array([0.12, 0.10, 0.08]), np.array([-0.08, 0.10, -0.12]),
         np.array([0.10, -0.12, 0.08])]
states = [(I + sum(v[k] * paulis[k] for k in range(3))) / 2 for v in bloch]
sigma = I / 2

# Six-outcome POVM E_{axis,sign}=(I+sign*sigma_axis)/6.
effects = [(I + sign * p) / 6 for p in paulis for sign in (-1, 1)]
assert np.linalg.norm(sum(effects) - I) < 1e-12
# Arbitrary prepared qubit states; this makes a valid EB channel.
prepared = [(I + sign * p) / 2 for p in paulis for sign in (1, -1)]
assert all(np.linalg.eigvalsh(s).min() >= -1e-12 for s in prepared)

def probs(state):
    return np.array([float(np.trace(e @ state).real) for e in effects])

p0 = probs(sigma)
pi = [probs(state) for state in states]
ratios = [p / p0 for p in pi]
assert all(np.all(q >= 1 - theta - 1e-12) and np.all(q <= 1 + theta + 1e-12)
           for q in ratios)

delta = 0.40
# Quantize each net state's likelihood ratio. One joint key groups outcomes.
keys = []
for y in range(len(effects)):
    keys.append(tuple(math.floor((ratios[i][y] - 1 + delta / 2) / delta + 1e-12)
                      for i in range(len(states))))
groups = {}
for y, key in enumerate(keys):
    groups.setdefault(key, []).append(y)

coarse_effects = []
coarse_prepared = []
for ids in groups.values():
    coarse_effects.append(sum((effects[y] for y in ids), np.zeros((2, 2), complex)))
    mass = float(sum(p0[y] for y in ids))
    coarse_prepared.append(sum((p0[y] * prepared[y] for y in ids),
                               np.zeros((2, 2), complex)) / mass)
assert np.linalg.norm(sum(coarse_effects) - I) < 1e-12

def original_output(state):
    p = probs(state)
    return sum((p[y] * prepared[y] for y in range(len(effects))),
               np.zeros((2, 2), complex))

def coarse_output(state):
    p = [float(np.trace(e @ state).real) for e in coarse_effects]
    return sum((p[j] * coarse_prepared[j] for j in range(len(groups))),
               np.zeros((2, 2), complex))

errors = []
for state in states:
    diff = original_output(state) - coarse_output(state)
    errors.append(float(np.linalg.svd(diff, compute_uv=False).sum() / 2))

K = math.ceil(2 * theta / delta) + 1
assert len(groups) <= K ** len(states)
assert max(errors) <= delta / 2 + 1e-10

print(json.dumps({
    "dimension": 2,
    "theta": theta,
    "cover_size": len(states),
    "original_outcomes": len(effects),
    "coarse_outcomes": len(groups),
    "per_coordinate_mesh": delta,
    "theoretical_outcome_bound": K ** len(states),
    "max_net_state_trace_distance": max(errors),
    "claimed_bound": delta / 2,
    "status": "finite diagnostic passed; analytic statement is proved in INITIAL.txt"
}, indent=2))
