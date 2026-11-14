"""ROOT-owned exact, introduced hysteron diagnostics; no producer code or data.

Run serially with the standard library. All numerical examples are introduced.
This is neither a material qualification nor a general passive-realizability test.
"""

from fractions import Fraction as Q
from itertools import product
import json
import math


def number(x):
    return {"exact": str(x), "float": float(x)}


def matrix(rows):
    return [[number(x) for x in row] for row in rows]


def weighted_symmetry(j):
    """Find positive w with w_i J_ij = w_j J_ji, or an exact witness.

    The supplied matrix, including all relevant entries, is an INPUT.
    The traversal does not acquire a matrix from inaccessible material.
    """
    n = len(j)
    weights = [None] * n
    for i in range(n):
        for k in range(i):
            a, b = j[i][k], j[k][i]
            if (a == 0) != (b == 0) or a * b < 0:
                return {"feasible": False, "witness": [i, k],
                        "reason": "unmatched zero or opposite signs"}
    for root in range(n):
        if weights[root] is not None:
            continue
        weights[root] = Q(1)
        queue = [root]
        for i in queue:
            for k in range(n):
                if i == k or j[i][k] == 0:
                    continue
                proposed = weights[i] * j[i][k] / j[k][i]
                if weights[k] is None:
                    weights[k] = proposed
                    queue.append(k)
                elif weights[k] != proposed:
                    return {"feasible": False, "witness": [i, k],
                            "existing_weight": number(weights[k]),
                            "inconsistent_proposed_weight": number(proposed),
                            "reason": "inconsistent product around a graph cycle"}
    return {"feasible": True, "weights": [number(w) for w in weights]}


def local_fields(state, drive, j, offsets):
    return [drive - offsets[i] + sum(j[i][k] * state[k]
                                    for k in range(len(state)))
            for i in range(len(state))]


def unstable(state, drive, j, offsets, widths):
    f = local_fields(state, drive, j, offsets)
    return [i for i in range(len(state)) if -state[i] * f[i] > widths[i]]


def energy(state, drive, weights, offsets, coupling):
    n = len(state)
    return (-sum(weights[i] * (drive - offsets[i]) * state[i] for i in range(n))
            - sum(coupling[i][k] * state[i] * state[k]
                  for i in range(n) for k in range(i)))


def relax(initial, drive, j, offsets, widths, weights=None, coupling=None):
    state = tuple(initial)
    path, seen, drops, identities = [state], {state: 0}, [], []
    while True:
        active = unstable(state, drive, j, offsets, widths)
        if not active:
            return {"path": path, "cycle": False, "drops": drops,
                    "identities": identities}
        i = active[0]  # An explicit arbitration convention; no claim about races.
        old, new = state, list(state)
        new[i] *= -1
        state = tuple(new)
        if weights is not None:
            delta = (energy(state, drive, weights, offsets, coupling)
                     - energy(old, drive, weights, offsets, coupling))
            field = local_fields(old, drive, j, offsets)[i]
            identities.append(delta - 2 * weights[i] * old[i] * field)
            assert delta < -2 * weights[i] * widths[i]
            drops.append(-delta)
        path.append(state)
        if state in seen:
            return {"path": path, "cycle": True, "cycle_start": seen[state],
                    "drops": drops, "identities": identities}
        seen[state] = len(path) - 1


def geometric_example():
    k, span, geometric_scale = [Q(1), Q(3, 2), Q(5, 4)], [Q(1, 5), Q(3, 10), Q(1, 4)], Q(1, 10)
    pair = [[Q(0), Q(1, 2), Q(3, 5)],
            [Q(1, 2), Q(0), -Q(2, 3)],
            [Q(3, 5), -Q(2, 3), Q(0)]]
    j = [[pair[i][m] * geometric_scale * span[m] / k[i]
          for m in range(3)] for i in range(3)]
    w = [k[i] * span[i] for i in range(3)]
    assert all(w[i] * j[i][m] == w[m] * j[m][i]
               for i in range(3) for m in range(3))
    cycle_forward = j[0][1] * j[1][2] * j[2][0]
    cycle_reverse = j[1][0] * j[2][1] * j[0][2]
    assert cycle_forward == cycle_reverse
    return {"parameters_scope": "INTRODUCED dimensionless small-angle Eq.6 form only",
            "J": matrix(j), "geometric_weights": [number(x) for x in w],
            "weighted_symmetry": weighted_symmetry(j),
            "cycle_forward": number(cycle_forward),
            "cycle_reverse": number(cycle_reverse)}


def cycle_obstructions():
    j = [[Q(0), Q(1), Q(1)], [Q(1), Q(0), Q(1)], [Q(2), Q(1), Q(0)]]
    ratio = j[0][1] * j[1][2] * j[2][0] / (j[1][0] * j[2][1] * j[0][2])
    e = math.tanh(math.log(float(ratio)) / 6)
    multiplicative_radius = float(ratio) ** (1 / 6)
    all_positive_cycles = 0
    for state in product((-1, 1), repeat=3):
        for drive in (Q(-3), Q(-1), Q(0), Q(1), Q(3)):
            all_positive_cycles += relax(state, drive, j, [Q(0)] * 3, [Q(1)] * 3)["cycle"]
    active_j = [[Q(0), Q(2)], [-Q(2), Q(0)]]
    loop = relax((-1, -1), Q(0), active_j, [Q(0)] * 2, [Q(1)] * 2)
    assert loop["cycle"] and len(loop["path"]) == 5
    assert all(len(unstable(s, Q(0), active_j, [Q(0)] * 2, [Q(1)] * 2)) == 1
               for s in loop["path"])
    return {"positive_three_cycle_J": matrix(j), "cycle_ratio": number(ratio),
            "weighted_symmetry": weighted_symmetry(j),
            "minimum_uniform_relative_entry_error_to_symmetrizable": e,
            "symmetric_log_error_multiplicative_radius": multiplicative_radius,
            "all_positive_finite_survey": {"initial_state_drive_pairs": 40,
                                           "cycles": all_positive_cycles,
                                           "warning": "not a general convergence or material proof"},
            "opposite_sign_J": matrix(active_j),
            "opposite_sign_cycle_at_constant_zero_drive": loop["path"],
            "unique_unstable_hysteron_each_state": True,
            "scope": "Failure of this positive-weight quadratic energy form is not an all-passive-physics impossibility."}


def bounded_degree_family(n):
    weights = [Q(1) + Q(i % 3, 5) for i in range(n)]
    offsets = [Q(i % 5 - 2, 5) for i in range(n)]
    widths = [Q(1, 4) + Q(i % 2, 20) for i in range(n)]
    coupling = [[Q(0)] * n for _ in range(n)]
    for i in range(n):
        m = (i + 1) % n
        coupling[i][m] = coupling[m][i] = Q(1, 2) if i % 2 == 0 else -Q(1, 3)
    j = [[coupling[i][m] / weights[i] for m in range(n)] for i in range(n)]
    results, quantum = [], 2 * min(weights[i] * widths[i] for i in range(n))
    all_states = list(product((-1, 1), repeat=n))
    for drive in (Q(-2), -Q(1, 2), Q(0), Q(1, 2), Q(2)):
        energies = [energy(s, drive, weights, offsets, coupling) for s in all_states]
        budget = (max(energies) - min(energies)) / quantum
        cheap_range = (2 * sum(weights[i] * abs(drive - offsets[i]) for i in range(n))
                       + 2 * sum(abs(coupling[i][m]) for i in range(n) for m in range(i)))
        assert max(energies) - min(energies) <= cheap_range
        max_flips, count, min_excess, max_identity = 0, 0, None, Q(0)
        for state in all_states:
            r = relax(state, drive, j, offsets, widths, weights, coupling)
            assert not r["cycle"]
            max_flips = max(max_flips, len(r["path"]) - 1)
            count += len(r["drops"])
            for d in r["drops"]:
                min_excess = d - quantum if min_excess is None else min(min_excess, d - quantum)
            for d in r["identities"]:
                max_identity = max(max_identity, abs(d))
        assert max_flips <= budget
        results.append({"drive": number(drive), "initial_states": len(all_states),
                        "total_flips": count, "maximum_trajectory_flips": max_flips,
                        "energy_range_over_min_drop_bound": number(budget),
                        "nonenumerative_range_bound": number(cheap_range),
                        "nonenumerative_flip_bound": number(cheap_range / quantum),
                        "minimum_drop_above_global_quantum": None if min_excess is None else number(min_excess),
                        "max_exact_flip_identity_error": number(max_identity)})

    drive = Q(-2)
    state = tuple(-1 for _ in range(n))
    assert not unstable(state, drive, j, offsets, widths)
    initial_energy = energy(state, drive, weights, offsets, coupling)
    work, dissipated = Q(0), Q(0)
    ledger = []
    for next_drive in (Q(2), Q(-2), Q(2), Q(-2)):
        dw = -(next_drive - drive) * sum(weights[i] * state[i] for i in range(n))
        work += dw
        r = relax(state, next_drive, j, offsets, widths, weights, coupling)
        dissipated += sum(r["drops"])
        state, drive = r["path"][-1], next_drive
        ledger.append({"drive": number(drive), "field_work": number(dw),
                       "flip_dissipation": number(sum(r["drops"])), "flips": len(r["drops"])})
    final_energy = energy(state, drive, weights, offsets, coupling)
    assert state == tuple(-1 for _ in range(n))
    assert work - dissipated == final_energy - initial_energy == 0
    return {"n": n, "matrix_entries_supplied": n * n,
            "finite_survey": results, "closed_drive_cycle": ledger,
            "cycle_work": number(work), "cycle_dissipation": number(dissipated),
            "energy_balance_error": number(work - dissipated - final_energy + initial_energy),
            "scope": "Exact synthetic discrete-energy checks, not physical time, shock dynamics, wear, noise, or useful output."}


def main():
    result = {
        "status": "INTRODUCED_BOUNDED_DIAGNOSTICS_NOT_A_MATERIAL_OR_NEW_FIELD",
        "geometric_threshold_example": geometric_example(),
        "obstructions_and_scope": cycle_obstructions(),
        "bounded_degree_families": [bounded_degree_family(n) for n in (4, 6, 8)],
        "general_switching_field_input_counts": [
            {"n": n, "independent_fields_in_general_table": n * (2 ** n)}
            for n in (10, 20, 40)],
        "limits": [
            "All numerical parameters and update conventions are introduced.",
            "The source's fixed small-angle equal-pair spring form is a restricted construction.",
            "Arbitrary finite-angle geometry, nonpairwise coupling and hidden states need not share its fixed weights.",
            "Supplied model entries, known state and synthetic driving are not acquired from hidden material.",
            "Graph realizability and constant-drive loop failures already appear in the primary literature.",
            "No novelty, scalable synthesis, general learning procedure, hardware, advantage or 90-level consequence is established."
        ]
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
