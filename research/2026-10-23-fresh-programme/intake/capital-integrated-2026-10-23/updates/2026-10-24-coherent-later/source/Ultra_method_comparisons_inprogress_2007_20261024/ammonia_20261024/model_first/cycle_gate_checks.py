#!/usr/bin/env python3
"""Scoped microkinetic checks, not material acquisition or a plant forecast.

All artificial rates/affinities below are explicitly illustrative. Measured
Woo exchange rates are labelled and belong to different prepared Mn complexes.
No central Mo->B transfer rate is assigned.
"""
import json
import math
from fractions import Fraction
from pathlib import Path

KB_EV = 8.617333262145e-5
KB_J = 1.380649e-23
PLANCK = 6.62607015e-34
E_CHARGE = 1.602176634e-19
AVOGADRO = 6.02214076e23
FARADAY = E_CHARGE * AVOGADRO
M_NH3_G = 17.03052
M_H2_G = 2.01588


def ring3(u, w):
    """u_i: i->i+1; w_i: i+1->i modulo3. Exact tree formula."""
    u0, u1, u2 = u
    w0, w1, w2 = w
    trees = [w0*u2 + u1*u2 + w0*w1,
             u0*w1 + w2*w1 + u0*u2,
             w2*u1 + u0*u1 + w0*w2]
    denom = sum(trees)
    p = [v/denom for v in trees]
    currents = [u[i]*p[i] - w[i]*p[(i+1) % 3] for i in range(3)]
    formula = (math.prod(u)-math.prod(w))/denom
    if max(abs(x-formula) for x in currents) > 1e-10*max(1, abs(formula)):
        raise ArithmeticError("tree current and edge currents disagree")
    return {"u_per_s": u, "w_per_s": w, "stationary_probability": p,
            "cycle_affinity_over_kT": math.log(math.prod(u)/math.prod(w)),
            "current_per_s": formula}


def max_eyring_barrier(T, needed_rate, partner_activity=1.0):
    # kappa=1 optimistic ceiling, one elementary barrier only.
    return KB_EV*T*math.log((KB_J*T/PLANCK)*partner_activity/needed_rate)


def main():
    # Exact formula balances retain the two distinct ligand inventories.
    species = {
        'A': {'Mo': 1, 'amido_ligand': 3},
        'AN': {'Mo': 1, 'amido_ligand': 3, 'terminal_N': 1},
        'B3': {'Ru': 1, 'PNP_skeleton': 1, 'variable_H': 3},
        'BN': {'Ru': 1, 'PNP_skeleton': 1, 'terminal_N': 1},
        'B5': {'Ru': 1, 'PNP_skeleton': 1, 'variable_H': 5},
        'N2': {'terminal_N': 2},
        'H2': {'variable_H': 2},
        'NH3': {'terminal_N': 1, 'variable_H': 3},
    }
    steps = {
        'C': {'A': -2, 'N2': -1, 'AN': 2},
        'T_unacquired': {'AN': -1, 'B3': -1, 'A': 1, 'BN': 1, 'H2': Fraction(3, 2)},
        'H': {'BN': -1, 'H2': -4, 'B5': 1, 'NH3': 1},
        'R_directional_reset_unacquired': {'B5': -1, 'B3': 1, 'H2': 1},
    }
    balances = {}
    net = {}
    for label, coeffs in steps.items():
        residual = {}
        for name, coefficient in coeffs.items():
            for atom, count in species[name].items():
                residual[atom] = residual.get(atom, 0) + coefficient*count
            multiplier = 1 if label == 'C' else 2
            net[name] = net.get(name, 0) + multiplier*coefficient
        assert all(v == 0 for v in residual.values()), (label, residual)
        balances[label] = {k: str(v) for k, v in residual.items()}
    net = {k: str(v) for k, v in net.items() if v != 0}
    assert net == {'N2': '-1', 'H2': '-3', 'NH3': '2'}, net
    # A reversible model can carry forward current through an uphill edge.
    # Scaling both directions preserves every affinity and destroys throughput.
    rings = []
    for epsilon in [1.0, 1e-3, 1e-6, 1e-9]:
        x = ring3([100.0, 0.1*epsilon, 100.0],
                  [1.0, 10.0*epsilon, 1.0])
        x["transfer_prefactor_multiplier"] = epsilon
        rings.append(x)

    # Binding shifts in eV/N, hypothetical ledger only.
    bA0, bA1, bB_receive, bB_release, delta = -1.0, -0.4, -0.5, -0.1, -0.17
    chemistry = [bA0, bB_receive-bA1, delta-bB_release]
    switch = [bA1-bA0, bB_release-bB_receive]
    assert math.isclose(sum(chemistry)+sum(switch), delta, abs_tol=1e-12)

    # Matched current-density target from the supplied Science2026 abstract;
    # site inventory is an explicitly chosen illustration, not measured here.
    j, FE, sites_cm2 = 0.100, 0.98, 1e15
    mol_rate = FE*j/(3*FARADAY)
    per_site = mol_rate*AVOGADRO/sites_cm2
    barriers = [{"T_K": T,
                 "unimolecular_barrier_eV_at_unit_transmission":
                     max_eyring_barrier(T, per_site),
                 "bimolecular_standard_barrier_eV_at_B_20mM":
                     max_eyring_barrier(T, per_site, 0.020)}
                for T in [298.15, 400.0, 573.0]]

    moles_tonne = 1e6/M_NH3_G
    ev_to_gj_tonne = FARADAY*moles_tonne/1e9
    photon_nm = 450.0
    photon_ev = PLANCK*299792458/(photon_nm*1e-9)/E_CHARGE
    h2_kg_tonne = 1.5*M_H2_G/M_NH3_G*1000

    # Finite-carrier attrition: independent loss per completed turnover.
    cycles = 300*3600  # 300h at1/NH3 per carrier per second, hypothetical.
    max_loss = -math.expm1(math.log(0.5)/cycles)
    pressure_T = 323.15
    pressure_ratio = 1000
    compression_j_mol = 2.5*KB_J*AVOGADRO*pressure_T*math.log(pressure_ratio)

    out = {
        "scope": "equations and conditional benchmarks; no acquired Mo-to-B rate",
        "exact_candidate_formula_residuals": balances,
        "candidate_closed_net_stoichiometry": net,
        "conditional_H2_gate_recycle": {
            "T_K": pressure_T, "high_to_low_pressure_ratio": pressure_ratio,
            "H2_recycled_mol_per_mol_NH3": 2.5,
            "minimum_compression_kJ_mol_NH3": compression_j_mol/1000,
            "minimum_compression_GJ_tonne_NH3": compression_j_mol*moles_tonne/1e9,
            "minimum_compression_MWh_tonne_NH3": compression_j_mol*moles_tonne/3.6e9,
            "warning": "illustrative gas swing, not measured required pressure ratio"},
        "illustrative_uphill_transfer_ring": rings,
        "illustrative_gate_ledger_eV_per_N": {
            "bA_capture": bA0, "bA_transfer": bA1,
            "bB_receive": bB_receive, "bB_release": bB_release,
            "overall_delta": delta,
            "chemical_step_dG": chemistry,
            "reversible_switch_work": switch,
            "sum_chemistry_plus_switch": sum(chemistry)+sum(switch)},
        "conditional_flux_target": {
            "j_A_cm2": j, "FE": FE, "chosen_sites_cm2": sites_cm2,
            "NH3_mol_s_cm2": mol_rate, "NH3_mmol_h_cm2": mol_rate*3.6e6,
            "required_turnovers_per_s": per_site,
            "optimistic_eyring_limits": barriers},
        "measured_Mn_exchange_rate_scope": {
            "source": "Woo etal JACS1991 DOI10.1021/ja00022a040",
            "three_electron_exchange_k_Minv_sinv_at20C": 5600,
            "two_electron_chloride_exchange_k_Minv_sinv_at22C": 0.010,
            "illustrative_partner_B_M": 0.020,
            "corresponding_pseudo_first_order_rates_sinv": [112, 0.0002],
            "warning": "different Mn porphyrin reactions; neither is Mo->B or a closed NH3 loop"},
        "energy_conversions": {
            "one_eV_per_NH3_GJ_per_tonne": ev_to_gj_tonne,
            "one_eV_per_NH3_MWh_per_tonne": ev_to_gj_tonne/3.6,
            "one_volt_at_three_electrons_per_NH3_GJ_per_tonne": 3*ev_to_gj_tonne,
            "450nm_photon_eV": photon_ev,
            "one_450nm_incident_photon_per_NH3_GJ_per_tonne": photon_ev*ev_to_gj_tonne,
            "one_450nm_incident_photon_per_NH3_MWh_per_tonne": photon_ev*ev_to_gj_tonne/3.6,
            "H2_kg_per_tonne_NH3": h2_kg_tonne,
            "H2_input_MWh_per_tonne_if50kWh_per_kg": h2_kg_tonne*50/1000,
            "photon_formula": "incident_light=(hc/lambda)*n_photons_per_NH3; electric_LED=incident_light/LED_efficiency; no universal quantum-yield assumption"},
        "conditional_attrition": {
            "rate_per_s": 1, "duration_hours": 300,
            "maximum_loss_probability_per_turnover_to_keep_half_inventory": max_loss,
            "warning": "independent irreversible loss model; carrier repair/recovery changes it"}}
    p = Path(__file__).with_name('cycle_gate_checks.json')
    p.write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps(out, indent=2))


if __name__ == '__main__':
    main()
