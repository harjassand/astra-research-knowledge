"""Small exact-generator diagnostic for source-matched primal and dual cells.

Enumeration is used only for this finite check, not the proposed sampler.
"""

from itertools import product
from pathlib import Path
import json
import math
import numpy as np


def probability(bits, rho):
    k = sum(bits)
    return rho**k * (1 - rho) ** (len(bits) - k)


def poisson(q, g, stationary):
    assert abs(stationary @ g) < 1e-11
    return np.linalg.solve(-q + np.ones((len(g), 1)) @ stationary[None, :], g)


def cell(v, rho, strength):
    active = list(range(v + 1))
    interior = list(range(1, v - 1))
    support = list(range(-1, v + 2))
    ghosts = [i for i in support if i not in interior]
    persistent_states = list(product((0, 1), repeat=len(interior)))
    state_index = {bits: i for i, bits in enumerate(persistent_states)}
    p = np.array([probability(bits, rho) for bits in persistent_states])
    q_open = np.zeros((len(p), len(p)))
    j = np.zeros(len(p))
    a = 0.0
    for index, bits in enumerate(persistent_states):
        for ghost_bits in product((0, 1), repeat=len(ghosts)):
            eta = dict(zip(interior, bits)) | dict(zip(ghosts, ghost_bits))
            weight = probability(ghost_bits, rho)
            for left in range(v):
                rate = 1 + strength * eta[left - 1] * eta[left + 2]
                mark = eta[left] - eta[left + 1]
                changed = eta.copy()
                changed[left], changed[left + 1] = eta[left + 1], eta[left]
                target = state_index[tuple(changed[i] for i in interior)]
                if target != index:
                    q_open[index, target] += weight * rate
                j[index] += weight * rate * mark
                a += p[index] * weight * rate * mark**2
    np.fill_diagonal(q_open, -q_open.sum(axis=1))
    f = poisson(q_open, j, p)
    variance = a - 2 * np.dot(p * j, f)
    chi = rho * (1 - rho)
    primal = variance / (2 * chi * v)

    # Dual: freeze the TWO exterior bits for the whole run; the active cell
    # is the full issued-bond path Lambda+, including the positive face.
    inverse_energy = 0.0
    smallest_gap = math.inf
    for outside in product((0, 1), repeat=2):
        outside_weight = probability(outside, rho)
        for k in range(v + 2):
            states = [bits for bits in product((0, 1), repeat=v + 1) if sum(bits) == k]
            if len(states) == 1:
                continue
            indices = {bits: i for i, bits in enumerate(states)}
            q_closed = np.zeros((len(states), len(states)))
            g = np.zeros(len(states))
            for index, bits in enumerate(states):
                eta = dict(zip(active, bits)) | {-1: outside[0], v + 1: outside[1]}
                g[index] = eta[v] - eta[0]
                for left in range(v):
                    rate = 1 + strength * eta[left - 1] * eta[left + 2]
                    changed = list(bits)
                    changed[left], changed[left + 1] = changed[left + 1], changed[left]
                    target = indices[tuple(changed)]
                    if target != index:
                        q_closed[index, target] += rate
            np.fill_diagonal(q_closed, -q_closed.sum(axis=1))
            assert np.max(abs(q_closed - q_closed.T)) < 1e-12
            uniform = np.full(len(states), 1 / len(states))
            u = poisson(q_closed, g, uniform)
            sector_weight = math.comb(v + 1, k) * rho**k * (1 - rho) ** (v + 1 - k)
            inverse_energy += outside_weight * sector_weight * (uniform @ (g * u))
            smallest_gap = min(smallest_gap, float(np.linalg.eigvalsh(-q_closed)[1]))
    dual_inverse = inverse_energy / (chi * v)
    dual = 1 / dual_inverse
    random_walk_gap = 2 * (1 - math.cos(math.pi / (v + 1)))
    assert smallest_gap >= random_walk_gap - 1e-9
    assert 1 - 1e-10 <= dual <= primal + 1e-10 <= 1 + strength + 1e-9
    if strength == 0:
        assert abs(primal - 1) < 1e-10 and abs(dual - 1) < 1e-10
    return {
        "V": v, "rho": rho, "strength": strength,
        "primal_D": float(primal), "dual_D": float(dual),
        "primal_dual_gap": float(primal - dual),
        "smallest_conditional_gap": smallest_gap,
        "random_walk_gap_bound": random_walk_gap,
    }


def main():
    records = []
    for rho, strength in ((0.2, 0), (0.2, 1), (0.5, 1), (0.8, 1)):
        values = [cell(v, rho, strength) for v in (3, 9)]
        assert values[1]["primal_D"] <= values[0]["primal_D"] + 1e-9
        assert values[1]["dual_D"] >= values[0]["dual_D"] - 1e-9
        records.extend(values)
    result = {"scope": "finite enumeration diagnostic only; not a hydrodynamic proof or sampler benchmark", "records": records}
    Path(__file__).with_name("PRIMAL_DUAL_CELL_CHECK.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
