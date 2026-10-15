#!/usr/bin/env python3
"""Exact finite resistor checks and explicitly nominal Li charge-budget arithmetic.

The network checks are fixtures for the independent variational proof. They do
not prove the continuum theorem, measure a battery, or validate its premises.
Only Python's standard library is used. `python -O` preserves every check.
"""

from fractions import Fraction as F
import json
import math
from pathlib import Path
import random


def check(condition, message):
    if not condition:
        raise RuntimeError(message)


def solve(matrix, rhs):
    """Exact Gaussian elimination; reject singular systems."""
    n = len(rhs)
    augmented = [list(row) + [value] for row, value in zip(matrix, rhs)]
    for j in range(n):
        pivot = next((k for k in range(j, n) if augmented[k][j]), None)
        check(pivot is not None, "singular resistor network")
        augmented[j], augmented[pivot] = augmented[pivot], augmented[j]
        scale = augmented[j][j]
        augmented[j] = [x / scale for x in augmented[j]]
        for k in range(n):
            if k != j and augmented[k][j]:
                factor = augmented[k][j]
                augmented[k] = [x - factor * y for x, y in zip(augmented[k], augmented[j])]
    return [augmented[k][-1] for k in range(n)]


def network(z, edges, sigma_max):
    """Boundary nodes 0,1 at z=0,1; edges=(i,j,length,area,sigma)."""
    check(z[0] == 0 and z[1] == 1, "wrong slab boundaries")
    internal = list(range(2, len(z)))
    locations = {node: i for i, node in enumerate(internal)}
    matrix = [[F(0) for _ in internal] for _ in internal]
    rhs = [F(0) for _ in internal]
    volume, trial = F(0), F(0)
    conductances = []
    for i, j, length, area, sigma in edges:
        check(length > 0 and length >= abs(z[i] - z[j]), "unphysical edge length")
        check(area > 0 and 0 < sigma <= sigma_max, "invalid material")
        g = sigma * area / length
        conductances.append((i, j, g))
        volume += area * length
        trial += g * (z[i] - z[j]) ** 2
        for node, other in ((i, j), (j, i)):
            if node in locations:
                k = locations[node]
                matrix[k][k] += g
                if other in locations:
                    matrix[k][locations[other]] -= g
                elif other == 1:
                    rhs[k] += g
    values = solve(matrix, rhs)
    potential = {0: F(0), 1: F(1), **dict(zip(internal, values))}
    conductance = sum(
        g * (potential[i] - potential[j]) ** 2 for i, j, g in conductances
    )
    bound = sigma_max * volume
    check(0 <= conductance <= trial <= bound, "variational/volume bound failed")
    return {"G": str(conductance), "trial_energy": str(trial), "bound": str(bound),
            "volume": str(volume), "ratio": float(conductance / bound)}


def random_network(rng):
    n = rng.randint(3, 10)
    z = [F(0), F(1)] + [F(rng.randint(1, 19), 20) for _ in range(n - 2)]
    pairs = {(0, k) for k in range(2, n)} | {(1, k) for k in range(2, n)}
    for _ in range(rng.randint(n, 3 * n)):
        i, j = sorted(rng.sample(range(n), 2))
        pairs.add((i, j))
    edges = []
    for i, j in sorted(pairs):
        length = abs(z[i] - z[j]) + F(rng.randint(1, 10), 20)
        edges.append((i, j, length, F(rng.randint(1, 9), 7), F(rng.randint(1, 7))))
    return network(z, edges, F(7))


def quantity(value):
    return {"rational": str(value), "decimal": float(value)}


def main():
    # Evaluated nominal bulk values at 293 K, NOT certified specimen-wide bounds.
    # Chi, JPCRD 8, 339 (1979), doi:10.1063/1.555598, tables 1 and 3.
    density = F(534)                     # kg/m^3
    resistivity = F(928, 10**10)         # 9.28e-8 ohm m
    sigma = 1 / resistivity
    # Explicit nominal composition; CIAAW gives [6.938,6.997] for standard Ar(Li).
    molar_mass = F(694, 100000)          # 0.00694 kg/mol
    # F = exact SI defining constants NA * e.
    faraday = F("6.02214076e23") * F("1.602176634e-19")
    charge_density = density * faraday / molar_mass
    straight = network([F(0), F(1), F(1, 4), F(3, 4)], [
        (0, 2, F(1, 4), F(3), F(7)),
        (2, 3, F(1, 2), F(3), F(7)),
        (3, 1, F(1, 4), F(3), F(7)),
    ], F(7))
    check(straight["G"] == straight["bound"], "straight rod must saturate")
    rng = random.Random(20261015)
    fixtures = [random_network(rng) for _ in range(300)]
    budgets = []
    for d_um in [10, 20, 100, 1000, 10000]:
        d = F(d_um, 10**6)
        for G in [F(1, 1000), F(1), F(10)]:
            volume = G * d * d / sigma
            charge = charge_density * volume
            radius = math.sqrt(float(G * d / (math.pi * float(sigma))))
            budgets.append({
                "d_um": d_um, "Gcrit_S": float(G),
                "Vcrit_m3": quantity(volume), "mass_kg": quantity(density * volume),
                "Qcrit_C": quantity(charge),
                "straight_rod_radius_um": radius * 1e6,
                "latency_at_1A_s": float(charge),
                "latency_at_1mA_s": float(charge / F(1, 1000)),
                "latency_at_1uA_s": float(charge / F(1, 10**6)),
            })
    # Exact idealized countermodels, not simulated physical specimens.
    delta_volume = F(1, 10**17)
    cancellation = {
        "positive_branch_charge_C": str(charge_density * delta_volume),
        "negative_branch_charge_C": str(-charge_density * delta_volume),
        "measured_net_charge_C": "0",
        "downstream_volume_gain_m3": str(delta_volume),
    }
    creep = {"external_charge_C": "0", "guard_charge_C": "0",
             "downstream_volume_gain_m3": str(delta_volume),
             "G_if_straight_10um_S": str(sigma * delta_volume / F(1, 10**10))}
    results = {
        "status": "CONDITIONAL_THEOREM_FIXTURES_ONLY; NO_LABORATORY_EVIDENCE",
        "nominal_parameters": {"density_kg_m3": quantity(density),
            "resistivity_ohm_m": quantity(resistivity),
            "sigma_S_m": quantity(sigma), "molar_mass_kg_mol": quantity(molar_mass),
            "faraday_C_mol": quantity(faraday), "charge_density_C_m3": quantity(charge_density)},
        "straight_equality_fixture": straight,
        "exact_random_graph_checks": {"seed": 20261015, "count": len(fixtures),
            "maximum_ratio": max(x["ratio"] for x in fixtures)},
        "nominal_budget_grid": budgets,
        "countermodels": {"net_current_cancellation": cancellation, "creep": creep},
        "interpretation": "A failed sufficient certificate does not prove physical impossibility."
    }
    destination = Path(__file__).with_name("GUARD_BOUND_RESULTS.json")
    destination.write_text(json.dumps(results, indent=2) + "\n")
    print(json.dumps({"saved": str(destination),
        "exact_graph_checks": len(fixtures), "straight_equality": straight,
        "nominal_10um_1S": next(x for x in budgets if x["d_um"] == 10 and x["Gcrit_S"] == 1),
        "creep_countermodel": creep}, indent=2))


if __name__ == "__main__":
    main()
