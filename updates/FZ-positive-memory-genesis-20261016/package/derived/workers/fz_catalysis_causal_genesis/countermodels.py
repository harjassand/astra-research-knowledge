#!/usr/bin/env python3
"""Exact synthetic causal countermodels, plus supplied-data arithmetic scales.

No measured transient or fitted Pd kinetics is generated here. Originals are
read-only. Output is confined to this script's directory.
"""

from fractions import Fraction as F
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
SUPPLIED = Path('/Users/harjas/Downloads/astra_physical_evidence/results.json')


def exact(x):
    return {'rational': str(x), 'decimal': float(x)}


def common_fate(amount, ethane):
    return {'B': amount - ethane, 'C': ethane}


def lower_deficit(c0_lower, c1_upper, missing1=F(0), assignment=F(0), exposure=F(0)):
    return c0_lower - c1_upper - missing1 - assignment - exposure


def run():
    checks = []
    amount = F(100)

    # Unlabelled totals differ even though newly supplied material has the
    # same fate. Old material is additive and remains unlabelled.
    new_c = F(2)
    old_c0, old_c1 = F(8), F(0)
    ordinary0, ordinary1 = old_c0 + new_c, old_c1 + new_c
    assert ordinary0 == 10 and ordinary1 == 2
    assert new_c - new_c == 0
    checks.append('old_inventory_false_positive_removed_by_fresh_tag')
    old_inventory = {
        'scope': 'finite observation, not a closed periodic steady cycle',
        'ordinary_ethane_sham': exact(ordinary0),
        'ordinary_ethane_pulse': exact(ordinary1),
        'tagged_ethane_sham': exact(new_c),
        'tagged_ethane_pulse': exact(new_c),
        'fresh_deficit': exact(new_c - new_c),
    }

    # Same reaction with species-specific causal, unit-area downstream
    # filters. Inert tracer can be identical while hydrocarbon delay differs.
    reaction_c = F(10)
    immediate = F(1, 5)
    window0, window1 = reaction_c, immediate * reaction_c
    tail0, tail1 = F(0), (1 - immediate) * reaction_c
    assert window0 + tail0 == window1 + tail1 == reaction_c
    assert lower_deficit(window0, window1, tail1) == 0
    checks.append('unit_area_product_lag_cancels_under_complete_collection')
    transport = {
        'filter_sham': [{'delay': 0, 'mass': exact(F(1))}],
        'filter_pulse': [
            {'delay': 0, 'mass': exact(immediate)},
            {'delay': 20, 'mass': exact(1 - immediate)},
        ],
        'observation_window_end': 10,
        'fresh_C_short_window_sham': exact(window0),
        'fresh_C_short_window_pulse': exact(window1),
        'fresh_C_complete_sham': exact(window0 + tail0),
        'fresh_C_complete_pulse': exact(window1 + tail1),
        'finite_record_deficit_lower_with_tail_bound': exact(lower_deficit(window0, window1, tail1)),
        'inert_tracer_filter_identical_in_both_arms': True,
    }

    # A hidden fresh-tag inventory creates the same apparent suppression.
    b0 = b1 = F(90)
    measured_c0, measured_c1, retained1 = F(10), F(2), F(8)
    assert b0 + measured_c0 == amount
    assert b1 + measured_c1 + retained1 == amount
    assert lower_deficit(measured_c0, measured_c1, retained1) == 0
    checks.append('unrecovered_fresh_tag_prevents_false_certificate')
    storage = {
        'fresh_B_sham': exact(b0), 'fresh_C_sham': exact(measured_c0),
        'fresh_B_pulse': exact(b1), 'fresh_C_pulse_measured': exact(measured_c1),
        'fresh_C_pulse_retained': exact(retained1),
        'deficit_lower': exact(lower_deficit(measured_c0, measured_c1, retained1)),
    }

    # Concentration is not flux. This is an identifiability construction,
    # not a proposed physically likely flow change in the actual apparatus.
    cflux = F(10)
    q0, q1 = F(100), F(500)
    assert cflux / q0 == F(1, 10) and cflux / q1 == F(1, 50)
    checks.append('concentration_does_not_identify_molar_flux')
    concentration = {
        'true_C_flow_both': exact(cflux),
        'total_flow_sham': exact(q0), 'total_flow_pulse': exact(q1),
        'observed_C_fraction_sham': exact(cflux / q0),
        'observed_C_fraction_pulse': exact(cflux / q1),
    }

    # Two mechanisms share the entire fresh-carbon output vector and the
    # measured read current/potential. Only the hidden-state interpretation
    # changes. One law is electronic p_z; the other is p(q)=q/50 for finite
    # internal hydrogen states q=5,1. The latter can represent an H activity
    # maintained over this finite read by a finite buffer.
    probs = [F(1, 10), F(1, 50)]
    hydrogen_states = [F(5), F(1)]
    electronic, hydrogen = [], []
    for p, q in zip(probs, hydrogen_states):
        electronic.append(common_fate(amount, amount * p))
        hydrogen.append(common_fate(amount, amount * q / 50))
    assert electronic == hydrogen
    assert all(v['B'] + v['C'] == amount for v in electronic)
    checks.append('fresh_carbon_and_read_current_do_not_identify_state_location')
    hidden_state = {
        'fresh_B_input': exact(amount),
        'electronic_state_fates': [{k: exact(v) for k, v in arm.items()} for arm in electronic],
        'finite_H_state_fates': [{k: exact(v) for k, v in arm.items()} for arm in hydrogen],
        'finite_H_state_q': [exact(q) for q in hydrogen_states],
        'reaction_law_for_H_state': 'p_B_to_C(q) = q/50',
        'read_current_both': exact(F(0)),
        'terminal_read_potential_both': exact(F(3, 2)),
        'chemical_H_state_or_local_H_activity_measured': False,
    }

    # A finite H occupancy can change many subsequent fresh turnovers as
    # it re-equilibrates with the common gas feed. Electronic x and H
    # occupancy theta share theta_next=(theta+1)/2 and C=10*theta per
    # 100-unit fresh B packet. The extra gas H uptake is unobserved here.
    theta = F(1, 5)
    relaxation_rows = []
    for index in range(6):
        c_sham, c_pulse = F(10), F(10) * theta
        next_theta = (theta + 1) / 2
        relaxation_rows.append({
            'packet': index + 1, 'H_occupancy': exact(theta),
            'C_sham': exact(c_sham), 'C_pulse_both_state_models': exact(c_pulse),
            'H_store_recharge_for_capacity_1': exact(next_theta - theta),
        })
        assert common_fate(amount, c_pulse)['B'] + c_pulse == amount
        theta = next_theta
    integrated_deficit = sum(F(10) - F(row['C_pulse_both_state_models']['rational']) for row in relaxation_rows)
    initial_H_gap = F(4, 5)
    assert integrated_deficit == F(63, 4)
    assert integrated_deficit > initial_H_gap
    checks.append('finite_H_occupancy_can_amplify_over_many_fresh_turnovers')

    # Example of a real fresh-fate difference that survives explicit
    # finite uncertainty/tail/exposure budgets. These budgets are chosen
    # synthetic values; none is an acquired instrumental precision.
    robust = lower_deficit(F(99, 10), F(21, 10), F(1, 5), F(1, 5), F(1, 2))
    assert robust == F(69, 10) and robust > 0
    checks.append('explicit_finite_error_budget_can_certify_only_when_positive')

    # A finite reservoir can index any finite observed probability sequence
    # when no independent reservoir dynamics/capacity restriction is given.
    sequence = [F(1, 10), F(1, 50), F(1, 25), F(2, 25), F(1, 10)]
    q_path = list(range(len(sequence), 0, -1))
    reservoir_law = dict(zip(q_path, sequence))
    assert [reservoir_law[q] for q in q_path] == sequence
    checks.append('finite_horizon_hidden_state_relabelling_is_observationally_equivalent')

    raw = SUPPLIED.read_bytes()
    supplied = json.loads(raw)
    src = supplied['conditional_dynamic_test']
    fa = src['inferred_acetylene_feed_mol_s']
    d = src['extra_avoided_ethane_mol_per_cycle_beyond_zero_negative_phase']
    useful = supplied['rows']['preprint_optimal_dynamic_10s_0p1s']['net_ethylene_per_incoming_acetylene']
    scales = {
        'status': 'arithmetic_from_supplied_aggregate_reconstruction_not_new_measurement',
        'cross_version_absolute_normalization_reconciled': False,
        'A_10s_umol': fa * 10 * 1e6,
        'B_10s_umol': fa * 10 * 20 * 1e6,
        'all_C2_10s_umol': fa * 10 * 21 * 1e6,
        'hold_suppression_equivalent_amount_umol_not_single_pulse_prediction': d * 1e6,
        'if_all_deficit_is_B_origin_absolute_B_fate_change': d / (fa * 10 * 20),
        'total_carbon_gap_1p4pct_10s_umol_not_uncertainty_interval': 0.014 * fa * 10 * 21 * 1e6,
        'dynamic_net_B_10s_umol': useful * fa * 10 * 1e6,
        'closure_gap_over_dynamic_useful_gain': 0.014 * 21 / useful,
    }
    out = {
        'status': 'exact_synthetic_countermodels_and_supplied_arithmetic_only',
        'physical_experiment_performed': False,
        'validated_Pd_model': False,
        'new_operation_demonstrated': False,
        'source_results_path': str(SUPPLIED),
        'source_results_sha256': hashlib.sha256(raw).hexdigest(),
        'checks_passed': checks,
        'old_inventory_countermodel': old_inventory,
        'product_transport_countermodel': transport,
        'fresh_storage_countermodel': storage,
        'concentration_countermodel': concentration,
        'electronic_H_state_equivalence': hidden_state,
        'relaxing_electronic_H_state_equivalence': {
            'law': 'theta_next=(theta+1)/2; C=10*theta per 100 fresh B units; x_electronic=theta_H',
            'finite_H_capacity': exact(F(1)),
            'initial_H_inventory_gap': exact(initial_H_gap),
            'fresh_ethane_deficit_six_packets': exact(integrated_deficit),
            'gas_H_replenishment_or_surface_H_measured': False,
            'rows': relaxation_rows,
            'scope': 'synthetic chemical occupancy model; not inferred Pd kinetics',
        },
        'finite_reservoir_index_example': {
            'q_path': q_path, 'probability_path': [exact(p) for p in sequence],
            'scope': 'unrestricted hidden reservoir class, not an identified Pd mechanism',
        },
        'synthetic_robust_positive_deficit_lower': exact(robust),
        'supplied_arithmetic_scales': scales,
    }
    target = HERE / 'countermodels.json'
    target.write_text(json.dumps(out, indent=2) + '\n')
    print(json.dumps({'status': 'passed', 'exact_fixture_checks': len(checks), 'output': str(target)}))


if __name__ == '__main__':
    run()
