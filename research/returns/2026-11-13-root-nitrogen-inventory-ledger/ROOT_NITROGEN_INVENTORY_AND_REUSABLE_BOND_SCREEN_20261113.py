"""ROOT bounded nitrogen-inventory and reusable-bond mechanism calculations.
Introduced diagnostic models; no material/device qualification or producer-code use.
Run with Python stdlib. Writes this script's own JSON only.
"""
from pathlib import Path
import json, math

F = 96485.33212
A = 0.05**2
q = 0.006/1e-4
charge = q*A
# A chemistry bookkeeping ceiling, not measured corrosion:
cu_mass = charge*0.063546/(2*F)
cu_thickness = cu_mass/(8960*A)

def plate(E, nu, h, p, G):
    D = E*h**3/(12*(1-nu**2))
    a = (128*D*G/p**2)**0.25
    return {"E_Pa_introduced":E,"nu_introduced":nu,"h_m":h,"D_Nm":D,
            "p_Pa_introduced":p,"G_modeI_J_m2_introduced_NOT_lap_transfer":G,
            "critical_blister_radius_m":a,
            "circular_blister_formula":"G=p^2*a^4/(128*D); fixed uniform pressure, clamped thin elastic plate",
            "limits":"No edge crack, mixed-mode law, plasticity, residual stress, interface thickness or validated real joint."}

# Exact enumeration of 100 scalar springs is useful for identifying the load-sharing opening.
# Capacity/height scatter/compliance below are introduced, not source-fitted PFSA properties.
N = 100
gaps = [40e-6*(i/(N-1)-0.5) for i in range(N)]
cap = 15.0
target = 1000.0

def spring_array(k, plateau=None, dead=()):
    def reactions(x):
        return [0.0 if i in dead else
                (min(plateau,max(0.0,k*(x-g))) if plateau is not None else max(0.0,k*(x-g)))
                for i,g in enumerate(gaps)]
    lo,hi=0.0,0.01
    for _ in range(100):
        mid=(lo+hi)/2
        if sum(reactions(mid))<target:lo=mid
        else:hi=mid
    x=(lo+hi)/2; r=reactions(x)
    return {"k_per_patch_N_m_introduced":k,"plateau_N_introduced":plateau,
            "dead_patch_indices":list(dead),"load_N":sum(r),"max_local_N":max(r),
            "min_live_N":min(v for v in r if v>0),"displacement_m":x,
            "individual_capacity_N_introduced":cap,"all_live_within_capacity":max(r)<=cap,
            "limits":"One-dimensional static tension; no real adhesive, moments, lateral loads, dynamics or manufacturable spring/stop supplied."}

G_on=2.0 # Introduced mode-dependent sensitivity, near source lap value but NOT a supplied mode-I law.
G_off=0.02 # Introduced, not a read source value.
C_hold=1e-8
C_release=1e-5
fracture = {
    "source_lap_compliance_relation":"F_c=sqrt(2*G_c*A/C_total); source geometry/compliance must match",
    "introduced_area_m2":A,
    "introduced_hold_compliance_m_N":C_hold,
    "introduced_release_compliance_m_N":C_release,
    "introduced_G_on_J_m2":G_on,"introduced_G_off_J_m2":G_off,
    "force_on_stiff_N":math.sqrt(2*G_on*A/C_hold),
    "force_off_same_stiff_N":math.sqrt(2*G_off*A/C_hold),
    "force_on_soft_N":math.sqrt(2*G_on*A/C_release),
    "force_off_soft_N":math.sqrt(2*G_off*A/C_release),
    "geometry_only_ratio":math.sqrt(C_release/C_hold),
    "chemistry_only_ratio":math.sqrt(G_on/G_off),
    "both_ratio":math.sqrt((G_on/G_off)*(C_release/C_hold)),
    "hold_at_1000N_requires_compliance_m_N":2*G_on*A/1000**2,
    "ideal_90deg_peel_force_on_N":G_on*0.05,
    "ideal_90deg_peel_force_off_N":G_off*0.05,
    "peel_limits":"Inextensible zero-bending steady tape peel only. Creating the peel geometry, edge access, bending, stretching, friction and reset are not free. Existing dry grippers already use peel release.",
    "limits":"Introduced two-state design sensitivity; no measured Goff, compliance-switch mechanism, mode transfer or new material."
}
nfeed=4.96; candidate=4.61298; extra_resin=0.291; retained_fluid=0.175
ledger = {"issued_feed_TAN_kg":nfeed,"model_potential_product_N_kg":candidate,
          "issued_recovery":0.9,"headroom_N_kg":candidate-.9*nfeed,
          "introduced_extra_resin_N_kg":extra_resin,"retained_wet_inventory_N_kg":retained_fluid,
          "extra_N_over_headroom":(extra_resin+retained_fluid)/(candidate-.9*nfeed),
          "potential_recovery":candidate/nfeed,
          "with_only_extra_resin_recovery":(candidate-extra_resin)/nfeed,
          "with_only_wet_inventory_recovery":(candidate-retained_fluid)/nfeed,
          "with_both_recovery":(candidate-extra_resin-retained_fluid)/nfeed,
          "model_metered_kWh":46.242,"kWh_per_potential_kgN":46.242/candidate,
          "free_analytical_kWh_per_potential_kgN":(46.242-8)/candidate,
          "ledger_USD_kgN":9.957,
          "free_capital_and_scheduled_renewal_service_USD_kgN":9.957-1.606-5.205,
          "also_free_power_USD_kgN":9.957-1.606-5.205-.232,
          "also_free_product_delivery_USD_kgN":9.957-1.606-5.205-.232-.308,
          "introduced_thermal_comparator_USD_kgN":2.02,
          "thirty_percent_advantage_threshold_USD_kgN":2.02*.70,
          "scope":"Fixed producer design/sensitivities and rounded financial categories, not all nitrogen-recovery architectures, measured guard affinity or a matched quote."}
# A budget to make replenishment consequential rather than an invisible reset:
# For 500 equal cycles with 95% inventory retention, irreversible loss fraction <= 1-0.95^(1/500).
loss_per_cycle=1-0.95**(1/500)
out={
    "scope":"Independent ROOT conditional models. No physical execution, acquired components, source substitution or qualified invention.",
    "nitrogen_inventory_and_cost":ledger,
    "electrode_charge": {"source_reference_charge_C_m2":q,"introduced_pad_area_m2":A,
        "charge_C":charge,"at_introduced_10V_one_pulse_J":10*charge,
        "two_equal_pulses_J":20*charge,
        "Cu2plus_all_charge_irreversible_mass_kg_cycle":cu_mass,
        "Cu2plus_all_charge_irreversible_thickness_m_cycle":cu_thickness,
        "at500cycles_thickness_m":500*cu_thickness,
        "limits":"All charge assigned to irreversible Cu2+ dissolution is a Faraday-law bookkeeping scenario, not measured corrosion. Reversal does not prove local material, oxidation, ion or water restoration; all auxiliary/reset energy unpaid here."},
    "compliance_and_peel":fracture,
    "blister_screens":[plate(70e9,.3,.001,500/A,G_on),plate(3e9,.38,132e-6,500/A,G_on)],
    "scalar_load_sharing":{"stiff_common_displacement":spring_array(1e6),
                           "soft_common_displacement":spring_array(1e5),
                           "introduced_force_limited":spring_array(1e6,12),
                           "force_limited_10_dead":spring_array(1e6,12,tuple(range(10)))},
    "closed_cycle":{"cycles":500,"minimum_retained_fraction":.95,
                    "maximum_equal_irreversible_fraction_cycle":loss_per_cycle,
                    "maximum_fraction_as_percent":100*loss_per_cycle,
                    "limits":"Conservative repeated fixed fraction law only; electrical charge balance and a low loss number do not construct local chemical or topographic renewal."}
}
p=Path(__file__).with_suffix('.json')
p.write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
print(json.dumps(out,indent=2,allow_nan=False))
