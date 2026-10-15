"""Exact rational regenerative-pump fixture. All rates are SYNTHETIC.

This verifies algebra under ideal exclusive gates, not a membrane prediction.
Row-vector convention: p_next = p @ P.
"""
from fractions import Fraction as F
from pathlib import Path
import json
import math

BASE = Path(__file__).resolve().parents[1]
N = 3  # empty, Li-bound, Na-bound


def eye():
    return [[F(i == j) for j in range(N)] for i in range(N)]


def mm(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(N))
             for j in range(N)] for i in range(N)]


def vm(p, a):
    return [sum(p[i] * a[i][j] for i in range(N)) for j in range(N)]


def phase(species, h, relaxation=F(1, 2)):
    # One reversible binding edge to one reservoir; the other species is inert.
    m = eye()
    m[0][species] = relaxation * h
    m[0][0] = 1 - m[0][species]
    m[species][0] = relaxation * (1 - h)
    m[species][species] = 1 - m[species][0]
    return m


def solve(a, b):
    a = [list(r) + [v] for r, v in zip(a, b)]
    for col in range(N):
        pivot = next(i for i in range(col, N) if a[i][col])
        a[col], a[pivot] = a[pivot], a[col]
        d = a[col][col]
        a[col] = [v / d for v in a[col]]
        for i in range(N):
            if i != col:
                d = a[i][col]
                a[i] = [v - d * w for v, w in zip(a[i], a[col])]
    return [r[-1] for r in a]


def run(phases):
    p_cycle = eye()
    for _, _, _, p in phases:
        p_cycle = mm(p_cycle, p)
    a = [[p_cycle[i][j] - F(i == j) for i in range(N)]
         for j in range(N - 1)] + [[F(1)] * N]
    pi = solve(a, [F(0), F(0), F(1)])
    assert vm(pi, p_cycle) == pi
    assert all(x > 0 for x in pi)
    p = pi
    transfer_right = [F(0), F(0), F(0)]
    trace = []
    for label, species, reservoir, kernel in phases:
        p_next = vm(p, kernel)
        uptake = p_next[species] - p[species]
        if reservoir == "R":
            transfer_right[species - 1] -= uptake
        trace.append(dict(phase=label, reservoir=reservoir, before=[str(x) for x in p],
                          after=[str(x) for x in p_next],
                          uptake_from_named_reservoir=str(uptake)))
        p = p_next
    assert p == pi
    assert transfer_right[0] == -transfer_right[1]
    assert transfer_right[2] == 0
    return dict(period_kernel=[[str(x) for x in r] for r in p_cycle],
                periodic_start=[str(x) for x in pi], trace=trace,
                right_reservoir_transfer=[str(x) for x in transfer_right],
                q=transfer_right[0])


phases = [
    ("A: Li load at L", 1, "L", phase(1, F(3, 4))),
    ("B: Li release at R", 1, "R", phase(1, F(1, 4))),
    ("C: Na load at R", 2, "R", phase(2, F(3, 4))),
    ("D: Na release at L", 2, "L", phase(2, F(1, 4))),
]
forward = run(phases)
# A chronology reversal is not a general antiport-reversal operation.
chronology_reverse = run(list(reversed(phases)))
assert forward["q"] * chronology_reverse["q"] > 0
side_reverse = run([(name.rsplit(" at ", 1)[0] + " at " +
                     ("L" if reservoir == "R" else "R"), sp,
                     "L" if reservoir == "R" else "R", p)
                    for name, sp, reservoir, p in phases])
assert side_reverse["q"] == -forward["q"]

q = forward["q"]
period_matrix = [[F(x) for x in row] for row in forward["period_kernel"]]
kappa = max(sum(abs(x - y) for x, y in zip(a, b)) / 2
            for a in period_matrix for b in period_matrix)
assert kappa == F(9, 16)
li_reward = [F(1, 16), F(5, 16), F(0)]
assert sum(F(x) * y for x, y in zip(forward["periodic_start"], li_reward)) == q
RT = 8.31446261815324 * 298.15
gradient_ratio = 11 / 9  # finite-gradient illustrative design arithmetic only
dmu = RT * math.log(gradient_ratio)
delta_E = dmu + 2 * RT * math.log(3)
# Per mole of carrier sites per cycle; excludes unknown physical gate actuation.
work = 2 * float(q) * delta_E
chemical = 2 * float(q) * dmu
assert work >= chemical > 0
results = dict(
    scope="Exact algebra; synthetic phase kernels, no acquired species rates",
    forward=forward,
    chronological_reverse=chronology_reverse,
    side_reverse=side_reverse,
    robustness=dict(dobrushin_coefficient=str(kappa),
                    stationary_TV_amplification=str(1 / (1-kappa)),
                    Li_right_reward_by_start_state=[str(x) for x in li_reward],
                    Li_reward_oscillation="5/16",
                    Li_output_perturbation_bound="epsilon_reward + (5/7)*epsilon_period_kernel",
                    preparation_TV_after_N="(9/16)^N",
                    note="Requires acquired full state model and uniform error bounds; no empirical bounds exist."),
    energy=dict(temperature_K=298.15, symmetric_activity_ratio=gradient_ratio,
                modeled_well_work_J_per_mol_sites=work,
                chemical_output_J_per_mol_sites=chemical,
                modeled_dissipation_J_per_mol_sites=work-chemical,
                omitted_costs="Gate actuation, electrodes, switching losses, hydraulics, acquisition, reset preparation, lifetime"),
)
for item in [forward, chronology_reverse, side_reverse]:
    item["q"] = str(item["q"])
(BASE / "evidence" / "exact_cycle_results.json").write_text(
    json.dumps(results, indent=2) + "\n")
print(json.dumps(dict(q=str(q), pi=forward["periodic_start"],
                     chronology_reverse_q=chronology_reverse["q"],
                     side_reverse_q=side_reverse["q"],
                     modeled_energy=results["energy"]), indent=2))
