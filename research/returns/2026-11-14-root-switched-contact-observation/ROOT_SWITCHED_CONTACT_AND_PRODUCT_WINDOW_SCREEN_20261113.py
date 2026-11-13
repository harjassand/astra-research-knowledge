#!/usr/bin/env python3
"""Independent introduced switched-contact, chemical-window and printing screens."""
import json
import math
from pathlib import Path

# P1: two root ports. B's contact must be physically opened independently.
ra_good, rb_good = 0.06, 0.02
ra_bad, rb_bad = 0.4, 0.03
rs_good, rs_bad = ra_good+rb_good, ra_bad+rb_bad
g_equal = 1/rs_good
g_shunt_bad = g_equal-1/rs_bad
r_shunt_bad = 1/g_shunt_bad
measurement_error_s = 0.02
shunt_state_drift_bound_s = 0.01
def switch_result(rs, gp_closed, gp_open):
    gc, go = 1/rs+gp_closed, gp_open
    lower = gc-go-2*measurement_error_s-shunt_state_drift_bound_s
    return {
        "closed_conductance_S":gc, "open_B_conductance_S":go,
        "apparent_closed_resistance_ohm":1/gc,
        "series_conductance_lower_bound_S":lower,
        "conditional_series_resistance_upper_bound_ohm":None if lower<=0 else 1/lower,
    }
contact = {
    "conditions":"Linear passive network; physical B contact independently opened; A/contact body unchanged; all other shunt conductance changes independently bounded. No switch hardware is supplied.",
    "old_loop_bound_ohm":0.095*20/(20-0.095),
    "closed_only_equal_port_examples":{
        "healthy_A_B_ohm":[ra_good,rb_good],
        "bad_A_B_ohm":[ra_bad,rb_bad],
        "bad_shunt_ohm":r_shunt_bad,
        "both_closed_port_resistance_ohm":1/g_equal,
    },
    "declared_errors":{"each_conductance_measurement_S":measurement_error_s,
                       "shunt_change_bound_S":shunt_state_drift_bound_s},
    "fixed_shunt_switched_examples":{
        "healthy":switch_result(rs_good,0,0),
        "failed":switch_result(rs_bad,g_shunt_bad,g_shunt_bad),
    },
    "state_dependent_shunt_counterexample":{
        "healthy":switch_result(rs_good,0,0),
        "failed":switch_result(rs_bad,g_shunt_bad,0),
        "violates_declared_drift_bound":g_shunt_bad>shunt_state_drift_bound_s,
        "limit":"If opening B also removes the shunt, the same two observations can falsely pass. The known drift premise is a physical operation, not an inferred sensor result.",
    },
}

# P3: ONE rectangular pulse, at most one intended growth followed by unwanted growth.
# Failed, unextended and extra-added chains are all outside the exact-one outcome.
def one_add_probability(a,u,t):
    if abs(a-u)<1e-10*max(a,u):
        return a*t*math.exp(-a*t)
    return a*math.exp(-u*t)*(-math.expm1(-(a-u)*t))/(a-u)
def optimum(a,u,n):
    t=math.log(a/u)/(a-u) if a!=u else 1/a
    g=one_add_probability(a,u,t)
    ratio=u/a
    analytic=math.exp(ratio*math.log(ratio)/(1-ratio)) if ratio!=1 else math.exp(-1)
    no_add=math.exp(-a*t)
    return {"a_per_s":a,"u_per_s":u,"T_opt_s":t,
            "exact_one_probability":g,"analytic_identity_error":abs(g-analytic),
            "no_add_probability":no_add,
            "extra_add_probability":1-no_add-g,
            "n":n,"all_exact_n_probability":g**n,
            "total_pulse_time_s":n*t,
            "probability_balance_error":abs(g+no_add+(1-no_add-g)-1)}
lo,hi=1e-12,1-1e-12
n=20
target=math.log(0.90)
for _ in range(120):
    r=(lo+hi)/2
    val=n*r*math.log(r)/(1-r)
    if val>target: lo=r
    else: hi=r
rstar=(lo+hi)/2
pulse_cases = {
    "introduced_reference":optimum(.1,.0003,20),
    "both_rates_100x_slower":optimum(.001,.000003,20),
    "background_only_100x_lower_UNCONSTRUCTED_SELECTIVE_GATE":optimum(.1,.000003,20),
    "background_only_10x_lower_UNCONSTRUCTED_SELECTIVE_GATE":optimum(.1,.00003,20),
}
chemical={
    "scope":"Separate introduced single-rectangular-pulse model, not a reconstruction or refutation of P3's multipulse ODE. No material rate fit or whole-chain assay is supplied.",
    "formula":"g(T)=a*(exp(-u*T)-exp(-a*T))/(a-u); gmax=r**(r/(1-r)), r=u/a.",
    "optimal_timer_cases":pulse_cases,
    "uniform_pulse_90percent_at_20_threshold":{
        "max_u_over_a":rstar,"min_a_over_u":1/rstar,
        "check_probability":math.exp(n*rstar*math.log(rstar)/(1-rstar)),
        "scope":"Restrictive equal independent steps, all prefixes and extra additions included; physical protection, wash, different pulse shapes, rejection or other chemistry changes the problem.",
    },
    "chemical_collapse_and_duplex_clearance_are_distinct":{
        "introduced_collapse_rate_per_s":1000,"introduced_duplex_clear_rate_per_s":.01,
        "time_s":100,"arm_remaining_fraction":math.exp(-1000*100),
        "duplex_remaining_fraction":math.exp(-.01*100),
        "limit":"Fast destruction of a sulfur arm does not itself clear recognition occupancy or protect the newly exposed chemical end.",
    },
    "rate_ratio_limits":[
        "Uniform dilution slowing a and u together preserves the optimized exact-one probability while lengthening the pulse.",
        "A selective reduction of u at fixed a creates a positive numerical window, but the specific chemical protection/localization and its deprotection/renewal must be physically built.",
        "No failure of all molecular synthesis or of the producer's different model follows.",
    ],
}

# A genuinely different physical operation: field-based fabrication and clearing.
# Dose values and transport coefficients are introduced, not extracted from VAM data.
def dose_window(positive_gain, negative_gain,on_dose=100,off_dose=80):
    lower=on_dose/positive_gain
    upper=off_dose/negative_gain
    return {"on_required_exposure":lower,"off_allowed_exposure_strictly_less_than":upper,
            "nonempty_scalar_window":lower<upper}
clearing=[]
for radius in (50e-6,25e-6):
    for viscosity in (1.0,100.0):
        length,pressure=0.01,100000.
        q=math.pi*radius**4*pressure/(8*viscosity*length)
        vol=math.pi*radius**2*length
        clearing.append({"radius_m":radius,"viscosity_Pa_s":viscosity,
                         "length_m":length,"pressure_Pa":pressure,
                         "flow_m3_per_s":q,"channel_volume_m3":vol,
                         "ten_displacements_s":10*vol/q})
wall=[]
for d in (1e-10,1e-12):
    # Symmetric initially uniform slab, both faces ideal perfect sinks.
    # First-mode remaining average ~8/pi^2 exp(-pi^2 D t/thickness^2).
    thickness=1e-3
    t=thickness**2/(math.pi**2*d)*math.log((8/math.pi**2)/.001)
    wall.append({"introduced_diffusivity_m2_per_s":d,"wall_thickness_m":thickness,
                 "first_mode_time_to_0_001_remaining_s":t,
                 "scope":"Ideal slab/perfect sinks, no reaction, swelling, binding or finite exterior capacity. No actual resin permeability or readiness claim."})
vam={
    "scope":"Independent introduced dose and transport diagnostics, not an implementation of the primary VAM paper.",
    "dose_window_clear":dose_window(.9,.45),
    "dose_window_with_introduced_positive_occlusion":dose_window(.09,.45),
    "flow_clearing":clearing,
    "sealed_cavity":"No imposed through-flow without a connected inlet/outlet or another constructed transport mechanism. Diffusion, sacrificial openings and different fluid-filled useful devices remain possible.",
    "wall_diffusion":wall,
    "limits":"Laminar cylindrical flow with fixed dimensions/viscosity; no cure inside channel, deformation, pinning, contamination or safe pressure qualification. Dose scalar obstruction is not an all-projection or all-printing theorem.",
}
result={"status":"INTRODUCED CONDITIONAL MODELS; NO WORKING INVENTION OR NOVELTY CLAIM",
        "contact":contact,"chemical":chemical,"different_manufacturing_operation":vam,
        "verification":{
            "closed_port_identity_error_ohm":abs(1/(1/rs_bad+g_shunt_bad)-rs_good),
            "switched_counterexample_pair_error_S":max(
                abs(contact["state_dependent_shunt_counterexample"]["healthy"][k]-
                    contact["state_dependent_shunt_counterexample"]["failed"][k])
                for k in ("closed_conductance_S","open_B_conductance_S")),
            "pulse_probability_identity_max_error":max(v["analytic_identity_error"] for v in pulse_cases.values()),
            "threshold_90percent_error":abs(math.exp(n*rstar*math.log(rstar)/(1-rstar))-.9),
        }}
out=Path(__file__).with_suffix(".json")
out.write_text(json.dumps(result,indent=2,sort_keys=True,allow_nan=False)+"\n")
print(json.dumps({"output":str(out),"verification":result["verification"],
                  "contact":contact,"chemical":chemical,"vam":vam},sort_keys=True))
