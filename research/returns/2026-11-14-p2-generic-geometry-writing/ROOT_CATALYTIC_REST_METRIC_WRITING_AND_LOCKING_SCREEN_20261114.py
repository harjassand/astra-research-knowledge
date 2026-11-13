#!/usr/bin/env python3
"""Independent introduced mechanics/kinetics screens, not a fitted material.

Exchange changes a material rest metric while retaining a load path. It need not
change equilibrium crosslink count. These are separate models with declared
boundary conditions; an optical cure fit is NOT transferred to an exchange
network or a recycling resin. No installation, source fetch or producer code.
"""
import json, math
from pathlib import Path

# Catalyst-only equilibrium screen, with dimensionless state and introduced rates.
kf, kr = 4., 1.
xeq = kf/(kf+kr)
def reaction(x, catalyst, duration):
    return xeq+(x-xeq)*math.exp(-catalyst*(kf+kr)*duration)
x1=reaction(.2, 1., 1.)
x2=reaction(x1, 0., 100.)
x3=reaction(x1, .1, 100.)

# Same introduced homogeneous section for uniform unloaded forming and a separate
# STRAIGHT small-deflection service load. Not a curved-structure qualification.
E, width, depth, density, L = 500e6,.040,.035,1200.,.5
I=width*depth**3/12
B=E*I
mass=density*width*depth*L
F=10.
w=density*width*depth*9.81
delta_F=F*L**3/(3*B)
delta_w=w*L**4/(8*B)
delta=delta_F+delta_w
theta_service=F*L**2/(2*B)+w*L**3/(6*B)
root_moment=F*L+w*L**2/2

# Maxwell-type rest curvature writing with supplied external end couples:
# M=B*(kappa-k0); k0'=a*(kappa-k0). Constant kappa-rate ramp, then hold.
a_on=.1
target=2.
ramp=60.
hold=30.
v=target/ramp
error_ramp=v/a_on*(-math.expm1(-a_on*ramp))
error_hold=error_ramp*math.exp(-a_on*hold)
written=target-error_hold
Mpeak=B*error_ramp
sigma_peak=E*depth/2*error_ramp
work=B*L*v*v/a_on*(ramp+math.expm1(-a_on*ramp)/a_on)
U_ramp=.5*B*L*error_ramp**2
U_hold=.5*B*L*error_hold**2
diss_ramp=work-U_ramp
diss_hold=U_ramp-U_hold
def endpoint(k):
    return (math.sin(k*L)/k, (1-math.cos(k*L))/k) if k else (L,0.)
pt=endpoint(target)
pa=endpoint(written)
endpoint_error=math.hypot(pa[0]-pt[0],pa[1]-pt[1])
assert abs(work-(diss_ramp+diss_hold+U_hold))<1e-10

# After withdrawal, independent straight service load held at fixed force.
# Integral of residual activity multiplies initial elastic deflection exactly in
# this linear Maxwell model: the rest curvature continues to creep.
a_dark=1e-7
k_off=.01
service_time=24*3600.
creep_budget=.001
def activity_integral(wait,k=k_off):
    return a_dark*service_time+(a_on-a_dark)/k*math.exp(-k*wait)*(
        -math.expm1(-k*service_time))
remaining=creep_budget/delta-a_dark*service_time
assert remaining>0
wait_required=max(0.,math.log((a_on-a_dark)/k_off*(
    -math.expm1(-k_off*service_time))/remaining)/k_off)
tail_cases=[]
for wait in [0.,120.,300.,wait_required,600.]:
    total=activity_integral(wait)
    tail_cases.append({"wait_s":wait,"activity_integral":total,
        "extra_24h_tip_creep_m":delta*total,
        "within_introduced_0p1rad_service_rotation_screen":(
            theta_service*(1+total)<=.1),
        "within_1mm_model_budget":delta*total<=creep_budget*(1+1e-12)})
max_dark=creep_budget/(delta*service_time)
contrast=a_on/max_dark
# Endpoint retargeting is a signed material-state operation, not one-way curing:
# if curvature -2 follows +2, the same constitutive law applies to changed error.
error_reverse_start=written-(-target)
reverse_hold_needed=math.log(error_reverse_start/.02)/a_on

# Independent optical exposure diagnostic. Source's own reported approximate
# thresholds are used only as a bounded exposure-window illustration; no fit of
# rate coefficients, real printer power or reusable exchange network follows.
dose_on=.239
dose_off=2.225
repeated=[]
for leakage in [1.,.1,.01]:
    for passes in [1,10,100]:
        lo=dose_on
        hi=dose_off/(passes*leakage)
        repeated.append({"introduced_passes":passes,
            "introduced_single_color_exposure_fraction":leakage,
            "minimum_selected_J_cm2":lo,
            "maximum_per_pass_J_cm2":hi,"has_window":lo<=hi,
            "scope":"Additive effective-dose assumption for one repeatedly "
                "exposed unwanted point; no mixing, depletion or reset."})

# Independent introduced inventories, not the full patent's species balance.
pag_growth=[]
for cycles in [1,10,100]:
    factor=1.03**cycles
    pag_growth.append({"cycles":cycles,"mass_factor_if_3wtpercent_per_current_"
        "batch_is_all_retained":factor,"original_fraction":1/factor})
stock_base=.05
stock_acid=.05
per_switch=.01
finite_pairs=min(stock_base,stock_acid)/per_switch

# Numerical quadrature independently checks the analytic external work.
steps=10000
dt=ramp/steps
quad=0.
for j in range(steps+1):
    time=j*dt
    err=v/a_on*(-math.expm1(-a_on*time))
    q=B*L*err*v
    quad+=q*dt*(.5 if j in (0,steps) else 1.)
assert abs(quad/work-1)<1e-7
assert x1>.5 and x2>.5 and x3>.5
assert abs(delta*activity_integral(wait_required)-creep_budget)<1e-12
result={
 "scope":"INTRODUCED independent screens; no working material or qualified writer",
 "catalyst_only_equilibrium":{"kf":kf,"kr":kr,"equilibrium_x":xeq,
   "start_x":.2,"after_activation_x":x1,"after_zero_catalyst_x":x2,
   "after_reactivation_same_rates_x":x3,"introduced_gel_threshold":.5,
   "conclusion":"Changing a shared catalyst multiplier changes speed, not "
      "equilibrium. It can freeze a state but cannot reverse this reaction "
      "toward the other side of its fixed equilibrium. Exchange can instead "
      "control flow without changing crosslink count."},
 "introduced_section":{"E_Pa":E,"width_m":width,"depth_m":depth,
   "density_kg_m3":density,"length_m":L,"EI_N_m2":B,"body_mass_kg":mass,
   "excluded":"Writer, fixtures, activation, source stock, sensors, support, "
      "connections, heat management, maintenance, preparation, residual stress"},
 "uniform_unloaded_forming":{"rate_on_s_inv":a_on,"target_curvature_m_inv":target,
   "ramp_s":ramp,"hold_s":hold,"peak_end_couple_N_m":Mpeak,
   "peak_surface_stress_Pa":sigma_peak,
   "retained_rest_curvature_m_inv":written,
   "unloaded_endpoint_error_m":endpoint_error,"external_work_J":work,
   "elastic_energy_before_hold_J":U_ramp,"elastic_energy_after_hold_J":U_hold,
   "dissipation_ramp_J":diss_ramp,"dissipation_hold_J":diss_hold,
   "quadrature_external_work_J":quad,
   "introduced_reverse_hold_to_0p02_per_m_error_s":reverse_hold_needed,
   "scope":"Externally imposed planar uniform curvature and end couples. No "
       "head, arbitrary 3D rest metric, temperature, damage or actuation law."},
 "separate_straight_service":{"tip_force_N":F,"self_weight_N_per_m":w,
   "initial_tip_deflection_from_force_m":delta_F,
   "initial_tip_deflection_from_self_weight_m":delta_w,
   "initial_tip_deflection_total_m":delta,"initial_tip_rotation_rad":theta_service,
   "root_moment_N_m":root_moment,"E_needed_for_10mm_with_this_mass_Pa":
       E*delta/.01,"warning":"Straight linear load case only; not all programmed "
       "shapes, connections or nonlinear geometric stability."},
 "relocking_and_loaded_retention":{"a_dark_s_inv":a_dark,
   "introduced_off_decay_s_inv":k_off,"service_time_s":service_time,
   "extra_tip_creep_budget_m":creep_budget,
   "maximum_dark_rate_if_no_activation_tail_s_inv":max_dark,
   "necessary_on_to_dark_rate_ratio_if_no_tail":contrast,
   "dark_rate_used_24h_creep_m":delta*a_dark*service_time,
   "model_min_wait_in_independent_support_s":wait_required,"cases":tail_cases,
   "scope":"No optical on/off ratio, contact sensor or real reaction rate "
       "measured. Waiting requires actual retained support and source reset."},
 "separate_exposure_window":{"source_thresholds_at_its_own_resin_and_Raman_"
    "conditions_J_cm2":{"dual_color":dose_on,"UV_only":dose_off},
    "current_source_followup_held":True,
    "not_transferred_to_exchange_or_recycling_chemistry":True,"cases":repeated},
 "separate_inventory_diagnostics":{"per_batch_fresh_PAG_mass_fraction":.03,
   "conditional_retained_additive_growth":pag_growth,
   "introduced_photobase_stock_mol":stock_base,"introduced_photoacid_stock_mol":
      stock_acid,"introduced_equivalents_consumed_per_switch_mol":per_switch,
   "maximum_complete_open_close_pairs_without_replenishment_or_regeneration":
      finite_pairs,"scope":"Finite uncaging/neutralization accounting, not "
      "a measured source cycle limit. Genuine reversible catalysis can differ."},
 "checks":{"section_and_work_identity":"PASS","work_quadrature":"PASS",
   "tail_wait_identity":"PASS","constant_equilibrium_direction":"PASS"},
}
out=Path(__file__).with_suffix(".json")
out.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
print(json.dumps({"output":str(out),"body_mass_kg":mass,"EI":B,
 "endpoint_error_mm":endpoint_error*1000,"peak_writer_moment_Nm":Mpeak,
 "writer_work_J":work,"service_deflection_mm":delta*1000,
 "minimum_on_off_ratio_no_tail":contrast,"wait_required_s":wait_required,
 "checks":"PASS"},sort_keys=True))
