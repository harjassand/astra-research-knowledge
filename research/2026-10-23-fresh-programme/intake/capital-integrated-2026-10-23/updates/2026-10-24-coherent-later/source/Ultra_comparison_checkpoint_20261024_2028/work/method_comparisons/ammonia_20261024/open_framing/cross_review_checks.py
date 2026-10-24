#!/usr/bin/env python3
"""Post-checkpoint independent accounting checks; no material/rate acquisition.

Does not import or execute the peer script and does not modify frozen files.
All source operating-point combinations and generous recovery cases are labelled.
"""
import hashlib
import json
import math
from fractions import Fraction as Q
from pathlib import Path

HERE = Path(__file__).resolve().parent
F = 96485.33212
R = 8.31446261815324
M_NH3 = 0.017031  # kg/mol, same as frozen open calculation
M_H2 = 0.002016
KB_EV = 8.617333262145e-5
KB = 1.380649e-23
H = 6.62607015e-34
NA = 6.02214076e23


def ring(u, w):
    # Exact rational derivation via stationary tree probabilities.
    t = [w[0]*u[2]+u[1]*u[2]+w[0]*w[1],
         u[0]*w[1]+w[2]*w[1]+u[0]*u[2],
         w[2]*u[1]+u[0]*u[1]+w[0]*w[2]]
    d = sum(t)
    p = [v/d for v in t]
    js = [u[i]*p[i]-w[i]*p[(i+1) % 3] for i in range(3)]
    closed = (math.prod(u)-math.prod(w))/d
    assert all(v == closed for v in js)
    # The three exact equalities are also the stationary master equations.
    assert sum(p) == 1
    return {"stationary_probabilities": [str(v) for v in p],
            "current_exact_per_s": str(closed), "current_per_s": float(closed),
            "affinity_over_kT": math.log(float(math.prod(u)/math.prod(w)))}


def main():
    f, v, hydrogen_work = 0.81, 0.1, 50.0
    gross_h2 = 4/f
    # Conditional generous endpoint: every non-ammonia electron evolves H2,
    # all that H2 is returned at the same anode-feed state without extra work.
    net_h2_endpoint = gross_h2*(1-(1-f))
    exported = 8*F*v/f/(3600000*M_NH3)
    baseline_h2 = 1.5*M_H2/M_NH3*hydrogen_work
    gross = gross_h2*M_H2/M_NH3*hydrogen_work-exported
    recovered_endpoint = net_h2_endpoint*M_H2/M_NH3*hydrogen_work-exported
    mean_v = 0.07446533048243643
    mean_exported = exported*mean_v/v
    h2 = {
        "scope": "Source gross charge, conditional HER recovery endpoints; not a whole-plant interval",
        "NH3_FE": f, "full_cell_export_V": v,
        "gross_anodic_H2_mol_per_NH3": gross_h2,
        "gross_anodic_H2_kg_per_kg_NH3": gross_h2*M_H2/M_NH3,
        "generous_all_side_HER_perfect_recovery_fresh_H2_mol_per_NH3": net_h2_endpoint,
        "generous_endpoint_fresh_H2_kg_per_kg_NH3": net_h2_endpoint*M_H2/M_NH3,
        "source_actual_FE_H2_and_recovery": "UNKNOWN; single-pass NH3 FE does not determine this",
        "H2_sensitivity_kWh_per_kg_H2": hydrogen_work,
        "gross_charge_electrical_export_kWh_per_kg_NH3": exported,
        "H2_work_minus_export_endpoints_kWh_per_kg_NH3": [recovered_endpoint, gross],
        "matched_HB_H2_only_kWh_per_kg_NH3": baseline_h2,
        "conditional_HB_overhead_threshold_endpoints_kWh_per_kg_NH3":
            [recovered_endpoint-baseline_h2, gross-baseline_h2],
        "source_mean_voltage_export_using_assumed_same_FE_kWh_per_kg_NH3": mean_exported,
        "mean_voltage_H2_work_minus_export_endpoints":
            [recovered_endpoint+exported-mean_exported, gross+exported-mean_exported],
        "warning": "Side nitrogen products may recycle; purges, H2 losses and recovery work are absent. Endpoints are not acquired minima or maxima."
    }
    no_cases = []
    for label, voltage, fe in [
        ("conditional optimistic combination; exact 1.9 V / 93% figure point not verified",1.9,.93),
        ("indexed primary main explicit highest-yield point: 0.51 mmol/cm2/h",2.1,.57),
        ("approximate voltage-sweep point; FE about 78%, not raw digitization",1.9,.78)]:
        electricity = 5*F*voltage/fe/(3600000*M_NH3)
        no_cases.append({"status":label,"voltage":voltage,"NH3_FE":fe,
                         "electricity_kWh_per_kg_NH3":electricity,
                         "plus_0.42MJ_absorbed_NO_optimistic_sum":electricity+420000/(3600000*M_NH3)})

    rings = []
    for eps in [Q(1), Q(1,1000000)]:
        result = ring([Q(100),Q(1,10)*eps,Q(100)], [Q(1),Q(10)*eps,Q(1)])
        result["prefactor_epsilon"] = str(eps)
        rings.append(result)
    pressure = {"scope":"Conditional reversible ideal isothermal compression only",
                "T_K":323.15,"pressure_ratio":1000,
                "internal_2p5H2_kJ_per_mol_NH3":2.5*R*323.15*math.log(1000)/1000,
                "total_if_fresh_also_at_low_pressure_4H2_kJ_per_mol_NH3":4*R*323.15*math.log(1000)/1000}

    # Variable H inventory and N inventory: all ligand carbon skeletons fixed.
    species = {'A':(1,0,0,0), 'AN':(1,0,1,0),
               'B3':(0,1,0,3), 'BN':(0,1,1,0), 'B5':(0,1,0,5),
               'H2':(0,0,0,2), 'N2':(0,0,2,0), 'NH3':(0,0,1,3)}
    steps = [dict(A=-2,N2=-1,AN=2),
             dict(AN=-2,B3=-2,A=2,BN=2,H2=3),
             dict(BN=-2,H2=-8,B5=2,NH3=2),
             dict(B5=-2,B3=2,H2=2)]
    net = {}
    for step in steps:
        residual = [sum(n*species[s][i] for s,n in step.items()) for i in range(4)]
        assert residual == [0,0,0,0], residual
        for s,n in step.items(): net[s] = net.get(s,0)+n
    net = {s:n for s,n in net.items() if n}
    assert net == {'N2':-1,'H2':-3,'NH3':2}

    target = .98*.1/(3*F)*NA/1e15
    barriers = []
    for fraction in [1,.1,.01]:
        barriers.append({"active_B3_fraction_of_20mM_total":fraction,
                         "conditional_elementary_bimolecular_max_barrier_eV_298K":
                         KB_EV*298.15*math.log((KB*298.15/H)*.020*fraction/target)})
    hashes = {name:hashlib.sha256((HERE/name).read_bytes()).hexdigest() for name in
              ['CONSTRUCTION_AND_OBSTRUCTION.txt','analyse_operation.py','operation_calculations.json']}
    out = {"fresh_H2_repair":h2,"NO_OER_separate_cases":no_cases,
           "independent_exact_stationary_ring":rings,
           "integer_molecular_cycle_net":net,
           "coarse_T_H2_coefficient":str(Q(3,2)),
           "isolated_T_is_integer_molecular_event":False,
           "pressure":pressure,"free_receiver_population_effect":barriers,
           "hidden_intermediate_negative_bound":"If c_BN<L and measured k_exit<=k_max, at quasi-steady state v_T<=k_max*L. No exit bound means no useful flux bound from nondetection alone.",
           "frozen_owned_file_SHA256":hashes}
    (HERE/'cross_review_checks.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))


if __name__ == '__main__':
    main()
