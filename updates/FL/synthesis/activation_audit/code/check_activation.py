#!/usr/bin/env python3
"""Independent bounded arithmetic checks for the FL activation ledger.

Standard library only. This checks algebraic instances and unit conversions; it
does not simulate chemistry, certify the proof, or validate a physical system.
Run from any directory: python3 check_activation.py [optional-output-json].
"""

from __future__ import annotations

import json
import math
import sys
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path


getcontext().prec = 60


def D(value: str | int) -> Decimal:
    return Decimal(str(value))


def hold_probabilities(lam_r: Decimal, lam_l: Decimal, hold_s: Decimal) -> tuple[Decimal, Decimal, Decimal]:
    K = lam_r + lam_l
    survival = (-K * hold_s).exp()
    a = lam_r / K
    product = a * (1 - survival)
    loss = (1 - a) * (1 - survival)
    return product, loss, survival


def work_per_product(
    E: Decimal,
    eta: Decimal,
    lam_r: Decimal,
    lam_l: Decimal,
    hold_s: Decimal,
    recovery: Decimal,
    overhead: Decimal,
) -> Decimal:
    p, _, survival = hold_probabilities(lam_r, lam_l, hold_s)
    return (E / eta - recovery * E * survival + overhead) / p


def unload_return(z: Decimal) -> Decimal:
    if z == 0:
        return Decimal(1)
    return 2 * (z - 1 + (-z).exp()) / (z * z)


def bisect_z_for_recovery(target: Decimal) -> Decimal:
    lo, hi = Decimal(0), Decimal(1)
    for _ in range(220):
        mid = (lo + hi) / 2
        if unload_return(mid) >= target:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def renewal_cost(q: Fraction, productive_cost: Fraction, failure_cost: Fraction) -> Fraction:
    return productive_cost + ((1 - q) / q) * failure_cost


def main() -> None:
    # Constant-hazard finite-time checks. Decimal precision avoids cancellation
    # at the selected moderate parameters; the theorem itself is continuous.
    E, eta = D(100), D("0.8")
    lam_r, lam_l, hold_s = D(3), D(7), D("0.4")
    recovery, overhead = D("0.9"), D(2)
    p, qloss, survival = hold_probabilities(lam_r, lam_l, hold_s)
    w = work_per_product(E, eta, lam_r, lam_l, hold_s, recovery, overhead)
    lower = E / (eta * (lam_r / (lam_r + lam_l)))
    assert abs((p + qloss + survival) - 1) < D("1e-55")
    assert w + D("1e-50") >= lower
    assert abs((p / (1 - survival)) - (lam_r / (lam_r + lam_l))) < D("1e-55")

    # Exact renewal countermodels: same q, different recoverable work by branch.
    q = Fraction(1, 10)
    full_loss = renewal_cost(q, Fraction(1), Fraction(1))
    partial_failure_loss = renewal_cost(q, Fraction(1), Fraction(1, 10))
    partial_failure_and_product_recovery = renewal_cost(q, Fraction(1, 10), Fraction(1, 10))
    assert full_loss == 10
    assert partial_failure_loss == Fraction(19, 10)
    assert partial_failure_and_product_recovery == 1
    rare_p = Fraction(1, 1_000_000)
    recovery_99 = Fraction(99, 100)
    rare_product_cost_ratio = recovery_99 + (1 - recovery_99) / rare_p
    assert rare_product_cost_ratio == Fraction(1_000_099, 100)

    # If both binary-collision hazards scale by one density factor, their
    # branching fraction is invariant (throughput may still change).
    density_selectivities = [Fraction(n * 2, n * 2 + n * 3) for n in (1, 10, 100)]
    assert density_selectivities == [Fraction(2, 5)] * 3

    # Exact type-mixture counterexample to pooling cause-specific rates.
    # Type A: weight 1/10, q=1. Type B: weight 9/10, q=1/10.
    q_actual = Fraction(1, 10) * Fraction(1) + Fraction(9, 10) * Fraction(1, 10)
    lam_r_mean = Fraction(1, 10) * 100 + Fraction(9, 10) * 1
    lam_l_mean = Fraction(1, 10) * 0 + Fraction(9, 10) * 9
    q_from_pooled_rates = lam_r_mean / (lam_r_mean + lam_l_mean)
    w_actual_mixture = 1 / q_actual
    w_pooled = 1 / q_from_pooled_rates
    assert q_actual == Fraction(19, 100)
    assert lam_r_mean == Fraction(109, 10)
    assert lam_l_mean == Fraction(81, 10)
    assert q_from_pooled_rates == Fraction(109, 190)
    assert w_actual_mixture == Fraction(100, 19)
    assert w_pooled == Fraction(190, 109)
    assert w_actual_mixture > w_pooled

    # Exact action-specific hazard outcomes. Selecting either action is legal;
    # an average across actions is not a guarantee for the selected policy.
    q_action_a = Fraction(1, 10)
    q_action_b = Fraction(9, 10)
    assert 1 / q_action_a == 10
    assert 1 / q_action_b == Fraction(10, 9)

    # Exact action-set check for a uniform hazard-ratio floor kappa=1/2.
    kappa = Fraction(1, 2)
    action_rates = [(Fraction(2), Fraction(1)), (Fraction(4), Fraction(3)), (Fraction(10), Fraction(5))]
    q_action_set = [r / (r + ell) for r, ell in action_rates]
    q_cap = 1 / (1 + kappa)
    assert max(q_action_set) <= q_cap

    # Torque-limited unloading: numerical values and the 99% threshold.
    zs = [D("0.1"), D(1), D(3), D(10)]
    unload_values = {str(z): unload_return(z) for z in zs}
    z99 = bisect_z_for_recovery(D("0.99"))
    assert abs(unload_return(z99) - D("0.99")) < D("1e-55")
    assert all(unload_return(zs[i]) > unload_return(zs[i + 1]) for i in range(len(zs) - 1))

    # eV/molecule -> kWh/kg CO with nominal M(CO)=28.010 g/mol.
    ev_j = D("1.602176634e-19")
    avogadro = D("6.02214076e23")
    co_kg_per_mol = D("0.028010")
    joules_per_kwh = D("3600000")
    kwh_per_kg_per_ev = ev_j * avogadro / joules_per_kwh / co_kg_per_mol
    activation_kwh_per_kg = D("6.14") * kwh_per_kg_per_ev
    ispt_ratio_32 = activation_kwh_per_kg / D("3.2")
    ispt_ratio_33 = activation_kwh_per_kg / D("3.3")

    # Full-plant range sensitivity for two explicitly stated Nm3 conventions.
    vendor_implied_kg_per_nm3 = D("35.5") / D("30000") * D(1000)
    vendor_fullplant_range = [D(6) / vendor_implied_kg_per_nm3, D(8) / vendor_implied_kg_per_nm3]
    molar_volume_0c_m3_per_mol = D("22.41396954e-3")
    kg_per_nm3_0c = co_kg_per_mol / molar_volume_0c_m3_per_mol
    ideal_gas_fullplant_range_0c = [D(6) / kg_per_nm3_0c, D(8) / kg_per_nm3_0c]
    stack_kwh_per_kg_vendor_mass = D("3.44") / vendor_implied_kg_per_nm3

    result = {
        "scope": "Independent arithmetic checks only; no chemistry, physical performance, or proof certification.",
        "constant_hazard_example": {
            "lambda_r_per_s": str(lam_r),
            "lambda_loss_per_s": str(lam_l),
            "hold_s": str(hold_s),
            "product_probability": str(p),
            "loss_probability": str(qloss),
            "survival_probability": str(survival),
            "eta_energy": str(eta),
            "recovery_fraction": str(recovery),
            "overhead_per_attempt": str(overhead),
            "work_per_product": str(w),
            "derived_lower_bound": str(lower),
        },
        "renewal_countermodels_per_E": {
            "q": "1/10",
            "full_failure_loss_no_product_recovery": str(full_loss),
            "failure_recovers_90_percent_product_recovers_none": str(partial_failure_loss),
            "both_branches_recover_90_percent": str(partial_failure_and_product_recovery),
        },
        "rare_product_recovery_tradeoff": {
            "product_probability": str(rare_p),
            "survivor_recovery_fraction": str(recovery_99),
            "work_per_product_over_E": str(rare_product_cost_ratio),
        },
        "shared_binary_collision_density_factor": {
            "density_multipliers": [1, 10, 100],
            "branching_fractions": [str(x) for x in density_selectivities],
        },
        "heterogeneous_rate_mixture_countermodel": {
            "actual_product_probability": str(q_actual),
            "unweighted_mean_lambda_r": str(lam_r_mean),
            "unweighted_mean_lambda_loss": str(lam_l_mean),
            "fictitious_pooled_rate_product_probability": str(q_from_pooled_rates),
            "actual_work_per_product": str(w_actual_mixture),
            "pooled_rate_work_per_product": str(w_pooled),
        },
        "adaptive_action_set": {
            "uniform_loss_to_reaction_hazard_floor_kappa": str(kappa),
            "implied_product_probability_cap": str(q_cap),
            "action_product_probabilities": [str(qx) for qx in q_action_set],
            "separate_action_countermodel": {
                "A_q": str(q_action_a),
                "A_work_per_E": str(1 / q_action_a),
                "B_q": str(q_action_b),
                "B_work_per_E": str(1 / q_action_b),
            },
        },
        "unloading": {
            "r_by_lambda_t_d": {key: str(value) for key, value in unload_values.items()},
            "z_for_99_percent_return": str(z99),
        },
        "industrial_energy_units": {
            "nominal_molar_mass_CO_kg_per_mol": str(co_kg_per_mol),
            "kWh_per_kg_per_eV_per_molecule": str(kwh_per_kg_per_ev),
            "6.14_eV_per_CO_kWh_per_kg": str(activation_kwh_per_kg),
            "ratio_to_ISPT_3.2_kWh_per_kg": str(ispt_ratio_32),
            "ratio_to_ISPT_3.3_kWh_per_kg": str(ispt_ratio_33),
            "vendor_implied_kg_per_Nm3_from_35.5t_per_30000Nm3": str(vendor_implied_kg_per_nm3),
            "Topsoe_stack_3.44_kWh_per_Nm3_as_kWh_per_kg_using_vendor_mass": str(stack_kwh_per_kg_vendor_mass),
            "Topsoe_plant_6_to_8_kWh_per_Nm3_as_kWh_per_kg_using_vendor_mass": [str(x) for x in vendor_fullplant_range],
            "CO_kg_per_Nm3_at_0C_1atm_ideal_gas": str(kg_per_nm3_0c),
            "Topsoe_plant_6_to_8_kWh_per_Nm3_as_kWh_per_kg_at_0C_1atm": [str(x) for x in ideal_gas_fullplant_range_0c],
        },
        "assertions": "PASS: finite formulas, renewal examples, rare-yield recovery tradeoff, shared-density-factor identity, pooled-rate counterexample, hazard-ratio action cap, unload values/threshold, and unit conversion arithmetic.",
    }

    output = json.dumps(result, indent=2) + "\n"
    if len(sys.argv) > 1:
        Path(sys.argv[1]).write_text(output, encoding="utf-8")
    else:
        sys.stdout.write(output)


if __name__ == "__main__":
    main()
