"""Check the explicit symmetric-state preparation and growth-walk costs."""

import json
from math import comb
from pathlib import Path
import numpy as np


def sym_projector(n):
    out = np.zeros((2**n, 2**n))
    for k in range(n + 1):
        vec = np.array([int(i.bit_count() == k) for i in range(2**n)], float)
        vec /= np.sqrt(comb(n, k))
        out += np.outer(vec, vec)
    return out


def swap(n, i, j):
    out = np.zeros((2**n, 2**n))
    for k in range(2**n):
        bit_i, bit_j = (k >> i) & 1, (k >> j) & 1
        target = k if bit_i == bit_j else k ^ (1 << i) ^ (1 << j)
        out[target, k] = 1
    return out


def verify_sym(n):
    ident = np.eye(2**n)
    triplet_projectors = [(ident + swap(n, i, j)) / 2 for i in range(n) for j in range(i)]
    avg_singlet = sum(ident - p for p in triplet_projectors) / comb(n, 2)
    nonzero = np.linalg.eigvalsh(avg_singlet)
    gap = nonzero[nonzero > 1e-10].min()
    initial = np.kron(sym_projector(n-1) / n, np.eye(2) / 2)
    sym = sym_projector(n)
    rho = initial.copy()
    m = 6
    for _ in range(m):
        rho = sum(p @ rho @ p for p in triplet_projectors) / len(triplet_projectors)
    good = (n + 1) / (2 * n)
    bad = (n - 1) / (2 * n)
    q = (n - 2) / (n - 1)
    observed_bad_weight = float(np.trace((ident - sym) @ rho))
    return {
        "n": n,
        "random_pair_singlet_effect_gap": float(gap),
        "predicted_gap": 1 / (n-1),
        "m": m,
        "bad_all_triplet_weight": observed_bad_weight,
        "predicted_bad_weight": bad * q**m,
        "retained_good_weight": float(np.trace(sym @ rho)),
        "predicted_good_weight": good,
    }


def verify_walk(N):
    # States 1,...,N-1; a transition from 1 to 0 restarts at 1.
    P = np.zeros((N - 1, N - 1))
    for k in range(1, N):
        p = (k + 2) / (2 * k + 2)
        if k + 1 < N:
            P[k - 1, k] = p
        if k > 1:
            P[k - 1, k - 2] = 1 - p
        else:
            P[0, 0] = 1 - p
    resolvent = np.eye(N - 1) - P
    step_times = np.linalg.solve(resolvent, np.ones(N - 1))
    weighted = np.linalg.solve(resolvent, np.arange(1, N))
    predicted_steps = N * (N + 4) * (N - 1) / (3 * (N + 1))
    predicted_weighted = N * (N - 1) * (N + 2) / 6
    return {
        "N": N,
        "expected_steps_after_restarts": float(step_times[0]),
        "predicted_expected_steps": predicted_steps,
        "max_mean_remaining_steps": float(step_times.max()),
        "expected_sum_K": float(weighted[0]),
        "predicted_expected_sum_K": predicted_weighted,
    }


result = {
    "status": "ideal nondestructive s/t consumer resource identities; physical operation costs separate",
    "symmetrization": [verify_sym(n) for n in range(2, 7)],
    "growth_walk": [verify_walk(n) for n in (2, 3, 5, 10, 30)],
}
out = Path(__file__).with_name("stp_resource_results.json")
out.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
