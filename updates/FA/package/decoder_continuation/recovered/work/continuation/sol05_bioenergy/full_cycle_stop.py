#!/usr/bin/env python3
"""Elemental/energy stop theorem and one oxygen-independent control pivot.

Pure accounting. No biological experiment, assay protocol, fitted kinetics,
or physical validation. Conditional numerical inputs are frozen inherited
references, never treated as measured performance.
"""
import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


receipts = json.loads((HERE / 'SOURCE_RECEIPTS.json').read_text())
for receipt in receipts['files']:
    assert sha256(HERE / receipt['local_path']) == receipt['sha256']
reference = json.loads((HERE / 'carrier_reference.json').read_text())
h = reference['hardware']
volume = 1 + h['guard_volume_L_per_L_translation']
sweep = reference['fixed_hardware_carrier_sweep']
initial = next(c for c in sweep if c['carrier_pool_mM'] == 50)
terminal = next(c for c in sweep if c['carrier_pool_mM'] == 25)
campaign = next(c for c in reference['purge_lifetime_design_cases']
                if c['acetate_cap_design_mM'] == 10
                and c['carrier_recovery_design'] == 0
                and c['final_carrier_pool_mM'] == 25)
Q = campaign['ATP_produced_at_source_mmol_L_translation']
P = campaign['PArg_phosphate_lost_in_purge_mmol_L_translation']
I0, I1 = 50 * volume, 25 * volume
Ilost = I0 - I1
A = Q - P
assert abs(A - campaign['fresh_energy_delivered_mmol_L_translation_excluding_seed']) < 1e-9
assert abs(Q - (10 * volume / .25) * math.log(2)) < 1e-9
assert abs(Ilost - campaign['carrier_lost_mmol_L_translation']) < 1e-9

# Exact rational proof certificate for the crucial sign. From
# log(2)=2*atanh(1/3), bound each denominator in the tail by 3:
# log(2) < 2/3 + (2/3)*(1/27)/(1-1/9) = 25/36 < 5/7.
# Thus Ilost/Q=5/(8 log(2)) > 9/10 > 7/8.
log2_upper = Fraction(2, 3) + Fraction(2, 3) * Fraction(1, 27) / (1 - Fraction(1, 9))
assert log2_upper == Fraction(25, 36)
ratio_lower = Fraction(5, 8) / log2_upper
assert ratio_lower == Fraction(9, 10)
assert ratio_lower > Fraction(7, 8)
carbon_gap_lower_per_source_ATP = 6 * (Fraction(1, 8) + ratio_lower - 1)
assert carbon_gap_lower_per_source_ATP == Fraction(3, 20)

proof_certificate = {
    'status': 'INTERNALLY_RECONSTRUCTED_ANALYTIC_PROOF_WITH_EXACT_RATIONAL_SIGN_CERTIFICATE',
    'contract': {
        'initial_carrier_mM': 50,
        'terminal_carrier_fraction_at_least': .5,
        'effective_reactor_volume_L': volume,
        'acetate_cap_mM': 10,
        'acetate_molecules_per_source_ATP': .25,
        'carrier_recovery': 0,
        'carrier_carbon_atoms': 6,
        'carrier_nitrogen_atoms': 4,
        'ideal_candidate_ATP_per_uncharged_C6_feed': 8,
        'comparator_ATP_per_C6_feed_at_least': 1,
        'fresh_service': 'useful delivered ATP + final stored energy - initial stored energy',
        'starting_waste_state': 'Purge phase already at waste cap; no startup storage credit. See separate full-startup theorem below.',
        'other_common_materials': 'Cancelled at identical full C/N/salt/product demand; candidate-only losses cannot be negative',
        'comparator_feasibility': 'The carbon theorem is conditional on this yield being available within the separately matched mass/salt/time constraints; those physical constraints are not acquired here'
    },
    'log2_strict_upper_rational': str(log2_upper),
    'carrier_lost_per_source_ATP_strict_lower_rational': str(ratio_lower),
    'carbon_excess_strict_lower_atoms_per_source_ATP': str(carbon_gap_lower_per_source_ATP),
    'scope': 'Purge-phase carbon-intensity stop only. A fresh reactor can initially store waste, so this one-ATP theorem must not be advertised as a complete startup campaign.'
}

# Full fresh-start campaign: do not throw away the initially empty waste
# reservoir. General conservation, for any admissible nonselective bleed,
# gives omega*Q <= W*V + W*integral(flow dt), and carrier decay gives
# integral(flow dt)=V*log(T0/T1). This dominates the former at-cap model.
# Positive receiver reverse-kinase flux requires PArg/T > 1/(1+K/Rr).
# Even if guard PArg is ignored, uniform purge therefore loses at least
# (T0-T1)/(1+K/Rr) phosphoryl equivalents from the product chamber.
K = Fraction(287, 50)       # 5.74, the inherited pH-7.8 equilibrium anchor.
receiver_ratio = Fraction(1, 3)
f_min = 1 / (1 + K / receiver_ratio)
assert f_min == Fraction(50, 911)
P_min = Fraction(25) * f_min
V_upper = Fraction(11, 10)
assert 1 <= volume <= float(V_upper)
startup_gap_lower = 6 * (-Fraction(5, 12) * V_upper + P_min/2)
assert startup_gap_lower == Fraction(4979, 3644)
assert startup_gap_lower > 0
rounded_K_upper = Fraction(6)
rounded_f_min = 1/(1 + rounded_K_upper/receiver_ratio)
rounded_gap_lower = 6 * (-Fraction(5, 12)*V_upper + 25*rounded_f_min/2)
assert rounded_gap_lower == Fraction(91, 76)
assert rounded_gap_lower > 0
Q_buffer = 10 * volume / .25
Q_startup = Q_buffer + Q
A_startup = Q_startup - P
assert P > float(P_min)
startup_comparisons = []
for yB in (1., 2., 2.53, 3., 4.):
    candidate_C = 6 * Q_startup / 8 + 6 * Ilost
    baseline_C = 6 * A_startup / yB
    delta = 1/yB - 1/8
    W_crit = .25 * 25 * (1 + float(f_min)/(volume*yB)) / (delta*(1+math.log(2)))
    startup_comparisons.append({
        'comparator_ATP_per_C6_feed': yB,
        'candidate_minimum_C_mmol_atoms_L': candidate_C,
        'comparator_C_mmol_atoms_L': baseline_C,
        'carbon_gain_mmol_atoms_L_positive_favors_candidate': baseline_C-candidate_C,
        'waste_cap_upper_for_the_thermodynamic_carbon_stop_mM': W_crit,
        'scope': 'Maximum startup waste storage plus inherited quasi-steady purge-phase phosphate loss. Rate, salt and full comparator feasibility remain separate.'
    })
assert startup_comparisons[0]['carbon_gain_mmol_atoms_L_positive_favors_candidate'] > 0
assert all(c['carbon_gain_mmol_atoms_L_positive_favors_candidate'] < 0 for c in startup_comparisons[1:])
startup_certificate = {
    'status': 'NEW_INTERNALLY_RECONSTRUCTED_FULL_STARTUP_CONSERVATION_STOP',
    'initial_waste': 'zero; full available waste storage credited',
    'arbitrary_purge_schedule': 'Allowed while uniform effective carrier removal and waste <= 10 mM are maintained',
    'effective_volume_contract_L': '[1, 11/10]',
    'product_compartment_volume_L': 1,
    'carrier_mM': '50 -> 25',
    'receiver_ATP_ADP_ratio': '1/3',
    'kinase_equilibrium_K': '287/50 = 5.74',
    'positive_reverse_receiver_kinase_throughout_carrier_loss': True,
    'carrier_and_PArg_phosphate_recovery': 0,
    'terminal_seed_salvage': 'Perfect remaining carrier and stored energy salvage credited',
    'candidate_ideal_yield': '8 ATP per C6 feed; all charged donors outside this feed must be charged separately',
    'minimum_PArg_phosphate_loss_mmol_L_strict_lower_rational': str(P_min),
    'carbon_excess_vs_2_ATP_C6_mmol_atoms_L_strict_lower_rational': str(startup_gap_lower),
    'robust_variant_K_at_most': str(rounded_K_upper),
    'robust_variant_carbon_excess_strict_lower_rational': str(rounded_gap_lower),
    'conclusion': 'Net carbon intensity is strictly above 3 carbon atoms per fresh ATP for this contract, even with full startup waste storage. This is a restricted resource stop, not a measured equal-condition process comparison.',
    'sensitivity': 'A larger waste tolerance, different kinase equilibrium, selective/decharged-carrier recovery or altered hardware is a different contract.'
}

comparisons = []
for yB in (1., 2., 2.53, 3., 4.):
    candidate_C = 6 * Q / 8 + 6 * Ilost
    baseline_C = 6 * A / yB
    # Same end-pool state and source/profile shape: Q scales by 1/(1-rho),
    # whereas lost carrier and lost phosphoryl inventory remain fixed.
    required_recovery = 1 - Q * (1/yB - 1/8) / (Ilost + P/yB)
    comparisons.append({
        'comparator_ATP_per_C6_feed': yB,
        'fresh_service_mmol_ATP_L': A,
        'candidate_fuel_C_mmol_atoms_L': 6 * Q / 8,
        'candidate_lost_carrier_C_mmol_atoms_L': 6 * Ilost,
        'candidate_minimum_total_C_mmol_atoms_L': candidate_C,
        'comparator_fuel_C_mmol_atoms_L': baseline_C,
        'carbon_gain_mmol_atoms_L_positive_favors_candidate': baseline_C - candidate_C,
        'finite_half_pool_recovery_strictly_above_for_carbon_gain': max(0., required_recovery),
        'note': 'Ideal candidate yield, perfect salvage of remaining carrier/energy, no catalyst/hardware acquisition charged: favorable to candidate. Comparator yield is a resource coordinate, not an asserted matched kinetic coefficient.'
    })
assert all(c['carbon_gain_mmol_atoms_L_positive_favors_candidate'] < 0 for c in comparisons)

product_N_per_fresh_ATP = 1.3 / 4  # Explicit energy-only protein proxy.
nitrogen_ratio = 4 * Ilost / (product_N_per_fresh_ATP * A)
finite_N_recovery = 1 - Q / (P + 4 * Ilost / (.1 * product_N_per_fresh_ATP))
nitrogen = {
    'status': 'CONDITIONAL_ELEMENTAL_CONSERVATION_NOT_PROTEIN_OUTPUT',
    'lost_carrier_N_mmol_atoms_L': 4 * Ilost,
    'energy_only_product_N_atoms_per_ATP_design': product_N_per_fresh_ATP,
    'purge_phase_carrier_N_loss_divided_by_energy_only_product_N': nitrogen_ratio,
    'full_startup_carrier_N_loss_divided_by_energy_only_product_N': 4*Ilost/(product_N_per_fresh_ATP*A_startup),
    'purge_phase_finite_half_pool_recovery_minimum_for_ten_percent_extra_N_budget': finite_N_recovery,
    'generic_constraint': '4*(initial carrier - recovered terminal carrier) <= extra nitrogen budget',
    'nitrogen_free_product': 'For G3P, product nitrogen demand is zero; carrier loss remains an extra charged nitrogen input. Catalyst nitrogen and all other nitrogen inputs must be matched separately.'
}

theta0 = initial['stored_PArg_mmol_L_translation'] / I0
steady = []
for cap in (10., 50., 100.):
    for yB in (1., 2., 2.53, 3., 4.):
        loss0 = .25 * 50 / cap
        rho = 1 - (1/yB - 1/8) / ((1 + theta0/yB) * loss0)
        steady.append({'acetate_cap_mM_design': cap,
                       'comparator_ATP_per_C6_feed': yB,
                       'initial_state_carrier_recovery_strictly_above_for_carbon_gain': max(0., rho)})

# Strong same-F/M/O envelope from the inherited correctly massed relay.
kS, kN, Y, M = 60., 30., 2., 1.
R = initial['ATP_mmol_L_translation_h']
kI = 1 / (2/R - 1/kS)
frontier = []
for feed in (1., 5., 10., 20., 40.):
    nox = min(feed, M / (1/kS + 1/kN))
    guard_x = min(feed, M / (1/kS + Y/(2*kI)))
    frontier.append({'pyruvate_feed_mmol_L_h': feed,
                     'NOX_ATP_mmol_L_h_design': nox,
                     'guard_ATP_mmol_L_h_design': (1 + Y/2) * guard_x})
assert abs(frontier[-1]['guard_ATP_mmol_L_h_design'] - R) < 1e-10
assert abs(frontier[-1]['NOX_ATP_mmol_L_h_design'] - 20) < 1e-10

# Actual, distinct source-reported assay points. Never combine the low-mass
# high-feed rate with the high-mass limiting-feed yield.
pivot = {
    'status': 'ONE_PIVOT_COMPLETED_AS_PRIMARY_EVIDENCE_AND_RESOURCE_SCREEN_NOT_A_NEW_OPERATION',
    'primary_doi': '10.1021/acssynbio.4c00877',
    'primary_url': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC12012885/',
    'benign_product_demand': 'One ATP phosphoryl transfer per glycerol-3-phosphate; identical glycerol/product recovery demand must be charged to every route',
    'reaction_O2_demand': 0,
    'strict_anoxic_functional_protein_assay': 'not supplied by this paper',
    'distinct_assay_points': [
        {'point': 'one_step_high_feed_peak', 'producer_g_L': .805, 'consumer_g_L': .3,
         'peak_G3P_mM_h_reported': 16.5, 'peak_reported_deviation': .8,
         'peak_per_producer_mass_descriptive_mmol_h_g': 16.5/.805,
         'initial_C6_feed_mM_reported': 200, 'phosphate_mM_reported': 100,
         'yield_at_this_mass_and_feed': 'not supplied as a measured one-ATP-per-hexose yield',
         'horizon': 'Reaction stopped after approximately eight hours; peak rate cannot be extrapolated as a steady rate'},
        {'point': 'one_step_limiting_feed_yield', 'producer_g_L': 2.505, 'consumer_g_L': .3,
         'C6_feed_mM_reported': 25, 'ATP_per_C6_reported': 1.02,
         'yield_reported_deviation': .02, 'phosphate_mM_reported': 110,
         'peak_rate': 'not assigned from the distinct low-mass high-feed assay'},
        {'point': 'complete_limiting_feed_yield', 'producer_g_L': 4.505, 'consumer_g_L': .3,
         'C6_feed_mM_reported': 25, 'ATP_per_C6_reported': 2.53,
         'yield_reported_deviation': .07, 'peak_G3P_mM_h_reported': 7.2,
         'peak_per_producer_mass_descriptive_mmol_h_g': 7.2/4.505,
         'phosphate_mM_reported': 110}
    ],
    'matched_gate_result': {
        'mass': 'Low-mass peak fits a 1 g/L producer budget; the limiting-feed yield points do not. Linear scale-down is unvalidated.',
        'carbon': 'Excess 200 mM fuel and its unconsumed recovery cannot be treated as a 25 mM fuel experiment. A one-yield carbon theorem is conditional on a feasible matched point.',
        'nitrogen': 'Catalyst and any carrier inventories/losses must be counted. Common producer mass does not prove common elemental N composition.',
        'salts': '100-110 mM phosphate, nucleotide state, pH/free-Mg and sugar products differ from the inherited relay design; equal-condition rates are unacquired.',
        'product': 'G3P is a directly measured benign product; no transfer to oxygen-sensitive protein output or translation is assumed.',
        'decision': 'No new enabled production operation. Preserve the strong actual control and the same-condition acquisition gap.'
    }
}

# A two-function witness shows why two isolated rate anchors do not identify
# a common positive throughput. This is an identifiability statement, not a
# claim that the true biochemistry has these artificial step supports.
identified_common = {
    'status': 'UNKNOWN_SAME_CONDITION_CONTINUOUS_RATE',
    'new_counterevidence_to_blanket_donor_rejection': {
        'doi': '10.1111/j.1365-2958.2009.06658.x',
        'reported_NADH_pulse_uM': 20,
        'figure': '4B',
        'scope': 'Distinct IMV preparation; transient ATP synthesis ceases after donor oxidation. No borrowed steady specific activity.'},
    'native_PDH_anchor_doi': '10.1128/JB.00104-08',
    'native_PDH_complete_inhibition_reported_NADH_uM': 60,
    'IMV_2019_anchor_doi': '10.1038/s41598-019-38564-0',
    'IMV_2019_NADH_comparison_uM': 500,
    'conclusion': 'The 20 uM pulse prevents a universal concentration-disjointness rejection. None of these isolated assays acquires a native-PDH/IMV/relay joint point at one full chemical state.'
}

output = {
    'status': 'QUANTITATIVE_RESTRICTED_STOP_THEOREM_AND_FAILED_MATCHED_CONTROL_PIVOT',
    'source_reference_sha256': sha256(HERE/'carrier_reference.json'),
    'proof_certificate': proof_certificate,
    'full_startup_proof_certificate': startup_certificate,
    'full_startup_campaign': {
        'maximum_source_ATP_from_initial_waste_storage_mmol_L': Q_buffer,
        'maximum_total_source_ATP_to_half_pool_mmol_L': Q_startup,
        'fresh_ATP_in_optimistic_startup_plus_inherited_purge_mmol_L': A_startup,
        'duration_h_with_inherited_constant_initial_model_rate_then_purge': Q_buffer/R + campaign['duration_h_model'],
        'carbon_excess_vs_two_ATP_hexose_using_inherited_PArg_loss_mmol_atoms_L': -startup_comparisons[1]['carbon_gain_mmol_atoms_L_positive_favors_candidate'],
        'new_proof_minimum_carbon_excess_without_using_BVP_profile_mmol_atoms_L': float(startup_gap_lower),
        'carbon_comparisons': startup_comparisons,
        'initial_storage_correction': 'The earlier purge-only one-ATP stop does not survive full empty-waste startup credit; its separate preserved result remains scoped to the at-cap purge phase.'
    },
    'fixed_hardware_half_pool': {
        'duration_h_inherited_conditional_model': campaign['duration_h_model'],
        'source_ATP_mmol_L': Q, 'fresh_ATP_service_excluding_seed_mmol_L': A,
        'carrier_lost_mmol_L': Ilost,
        'PArg_phosphate_lost_mmol_L': P,
        'initial_stored_energy_mmol_L': initial['stored_phosphate_mmol_L_translation'],
        'terminal_stored_energy_mmol_L': terminal['stored_phosphate_mmol_L_translation'],
        'start_capacity_mM_h_model': R,
        'terminal_capacity_mM_h_model': terminal['ATP_mmol_L_translation_h'],
        'best_case_baseline_yield_above_which_carbon_is_no_worse': A / (Q/8 + Ilost)
    },
    'purge_phase_carbon_comparisons': comparisons,
    'nitrogen_conservation': nitrogen,
    'initial_state_steady_carbon_thresholds': steady,
    'strong_NOX_frontier_design': {'kS': kS, 'kN': kN, 'kI': kI, 'cases': frontier,
                                  'scope': 'Same feed/mass/O2 algebra with design coefficients, not a fully matched measured physical comparator'},
    'common_redox_gate': identified_common,
    'oxygen_independent_pivot': pivot,
    'unexecuted': ['No biological experiment or hardware construction',
                   'No claimed strict-anoxic functional protein production',
                   'No membrane selectivity, catalyst lifetime or shared chemical operating point acquired',
                   'No novelty clearance or civilization-enabling capability',
                   'Prior service content restriction was not retried or bypassed']
}
(HERE/'results.json').write_text(json.dumps(output, indent=2, allow_nan=False)+'\n')
print(json.dumps({
    'status': output['status'],
    'purge_only_rational_carbon_excess_lower_bound_per_source_ATP': str(carbon_gap_lower_per_source_ATP),
    'full_startup_rational_carbon_excess_lower_bound_vs_two_ATP_C6': str(startup_gap_lower),
    'full_startup_rounded_K_upper_six_lower_bound': str(rounded_gap_lower),
    'full_startup_optimistic_fresh_ATP_mmol_L': A_startup,
    'full_startup_carbon_margin_vs_two_ATP_C6_mmol_atoms_L': startup_comparisons[1]['carbon_gain_mmol_atoms_L_positive_favors_candidate'],
    'fresh_ATP_mmol_L': A,
    'carbon_margin_vs_one_ATP_hexose_mmol_atoms_L': comparisons[0]['carbon_gain_mmol_atoms_L_positive_favors_candidate'],
    'purge_phase_carrier_N_over_energy_only_product_N': nitrogen_ratio,
    'source_files_unchanged': all(sha256(Path(r['source_path'])) == r['sha256'] for r in receipts['files'])
}, indent=2))
