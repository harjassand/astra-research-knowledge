#!/usr/bin/env python3
"""Exact illustrative accounting for the metered-recombination candidate.

No measured input is present. These receipts check finite arithmetic and the
explicit countermodels in REPORT.md, not physical feasibility or novelty.
"""

from fractions import Fraction as F
import json
from pathlib import Path


FARADAY = F("96485.33212")  # SI value rounded here; not an uncertainty bound.
H_WATER_298 = F("285830")   # J/mol, NIST standard liquid-water reference.


def fstr(x):
    return {"rational": str(x), "decimal": float(x)}


def terminal_record(i, recombination, shuttle, cell_v=F("1.8")):
    """Units: i is mol electron-pairs/time, outputs same time unit.

    Shuttle transports terminal charge without net chemical products.
    Net gas, terminal power and total heat cannot partition shuttle/recombination.
    """
    splitting = i - shuttle
    h2 = splitting - recombination
    assert min(splitting, h2, recombination, shuttle) >= 0
    electrical = 2 * FARADAY * i * cell_v
    return {
        "hydrogen": h2,
        "oxygen": h2 / 2,
        "net_water_consumed": h2,
        "external_charge": 2 * FARADAY * i,
        "electrical_energy": electrical,
        "total_heat": electrical - H_WATER_298 * h2,
    }


def thermal_rhs(temp, bath, p, c, k, reaction):
    return (p + reaction - k * (temp - bath)) / c


def main():
    a = terminal_record(F(1), F(1, 100), F(0))
    b = terminal_record(F(1), F(0), F(1, 100))
    assert a == b

    # The ODE is identical for every T,P under the stated q(T) transformation.
    c, k, delta_k, bath = F(4), F(2), F(3, 7), F(80)
    thermal_checks = []
    for temp in [F(80), F(81), F(83, 1), F(85)]:
        for p in [F(0), F(1), F(7, 5)]:
            reaction = F(1, 10) + (temp - bath) ** 2 / 100
            reaction_alt = reaction + delta_k * (temp - bath)
            lhs = thermal_rhs(temp, bath, p, c, k, reaction)
            rhs = thermal_rhs(temp, bath, p, c, k + delta_k, reaction_alt)
            assert lhs == rhs
            thermal_checks.append({"T": str(temp), "P": str(p), "dTdt": str(lhs)})

    # All values below are declared design arithmetic, not data or forecasts.
    scaling = []
    for jx in [F("0.0001"), F("0.001"), F("0.01"), F("0.1")]:
        q = H_WATER_298 * jx / (2 * FARADAY)
        scaling.append({"H2_loss_equivalent_A_cm2": fstr(jx),
                        "recombination_W_cm2_at_298K_liquid_reference": fstr(q)})

    resistance = []
    for blocked in [F("0.001"), F("0.01"), F("0.05"), F("0.1")]:
        ra0, j = F("0.1"), F(1)
        added = ra0 * blocked / (1 - blocked)
        resistance.append({"blocked_area_fraction": fstr(blocked),
                           "added_area_resistance_ohm_cm2": fstr(added),
                           "added_ohmic_W_cm2_at_1A_cm2": fstr(j*j*added)})

    # Example sufficient lower bound. hmax is a hypothetical acquired budget.
    q_minus, error_budget, hmax, seconds, area = F(60), F(12), F(300000), F(3600), F(1)
    nrec_lower = max(F(0), (q_minus - error_budget) / hmax)
    assert nrec_lower == F(1, 6250)
    j_lower = 2 * FARADAY * nrec_lower / (seconds * area)
    # Additional escaped H2 and finite initial inventory/generation corrections.
    escaped_lower, initial_inventory_upper, generated_upper = F(1, 10000), F(1, 50000), F(0)
    cross_lower = max(F(0), escaped_lower + nrec_lower - initial_inventory_upper - generated_upper)

    result = {
        "evidence_type": "exact_synthetic_accounting_only",
        "laboratory_data": False,
        "terminal_countermodel_equal": a == b,
        "terminal_countermodel_record": {key: fstr(val) for key, val in a.items()},
        "thermal_equivalence_checks": thermal_checks,
        "heat_scaling": scaling,
        "area_blocking_scaling": resistance,
        "illustrative_sufficient_bound": {
            "Qminus_J": fstr(q_minus), "B_J": fstr(error_budget),
            "hmax_J_mol": fstr(hmax), "window_s": fstr(seconds),
            "Nrec_lower_mol": fstr(nrec_lower),
            "H2_loss_equivalent_current_density_A_cm2": fstr(j_lower),
            "escaped_H2_lower_mol": fstr(escaped_lower),
            "initial_H2_inventory_upper_mol": fstr(initial_inventory_upper),
            "external_H2_generation_upper_mol": fstr(generated_upper),
            "net_crossing_lower_mol": fstr(cross_lower),
        },
        "constant_limitations": "Faraday value rounded; 298.15 K liquid-water heat is only a reference scale; operating-temperature/phase hmax must be acquired.",
    }
    dest = Path(__file__).with_name("ACCOUNTING_RESULTS.json")
    dest.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"status": "PASS", "output": str(dest),
                      "j_rec_lower_example_A_cm2": float(j_lower),
                      "net_crossing_lower_example_mol": float(cross_lower)}, indent=2))


if __name__ == "__main__":
    main()
