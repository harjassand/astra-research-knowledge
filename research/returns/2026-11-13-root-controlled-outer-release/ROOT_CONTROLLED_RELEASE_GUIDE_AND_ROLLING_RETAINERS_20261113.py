"""ROOT-owned controlled-release and guided-column calculations.
No producer execution, hardware or qualified constituent data.
"""
import math,cmath,json
from pathlib import Path
def linear_release(F,k,m,T,residual=0.):
    om=math.sqrt(k/m);delta=F-residual
    exact=abs(delta/k*2*math.sin(om*T/2)/(om*T)) if T else abs(delta/k)
    robust=abs(delta/k)*min(1.,2/(om*T)) if T else abs(delta/k)
    return {"F0_N":F,"k_N_m":k,"mass_kg":m,"ramp_s":T,"frequency_Hz":om/(2*math.pi),
      "ideal_exact_free_amplitude_m":exact,
      "unknown_phase_envelope_m":robust+abs(residual/k),
      "incremental_force_envelope_N":k*(robust+abs(residual/k)),
      "residual_outer_N":residual}
rows=[linear_release(2500.,2e6,m,T,50.) for m in [10.,20.,60.] for T in [.01,.05,.1,.5,1.]]
# A physically monotone but nonuniform ramp can resonate. Do not infer profile
# guarantees from duration alone. Selected T is five cycles only for this example.
T=.5;f=10.;om=2*math.pi*f;k=2e6;F=2500.;eps=50.
n=20000;dt=T/n
phasor=sum((-F/T+eps*om*math.cos(om*(i+.5)*dt))*cmath.exp(1j*om*(i+.5)*dt)*dt for i in range(n))/k
profile={"F0_N":F,"epsilon_N":eps,"T_s":T,"frequency_Hz":f,"effective_mass_kg":k/(om*om),
 "nonuniform_free_amplitude_m":abs(phasor),"analytic_m":eps*om*T/(2*k),
 "slope_max_N_s":-F/T+eps*om,
 "still_monotone":-F/T+eps*om<0,
 "uniform_ramp_freq_lower_bound_m":F/k*2/(om*T),
 "scope":"Constant scalar stiffness, undamped mode, bounded sinusoidal force variation. Not measured actuator ripple or a full-frame response."}
assert abs(abs(phasor)-profile["analytic_m"])<1e-12
energy=[]
for fmin in [2.,5.,10.,20.]:
 for T in [.1,.5,1.]:
  fac=min(1.,2/(2*math.pi*fmin*T));E=1.264;Er=.01
  energy.append({"freq_min_Hz":fmin,"ramp_s":T,"ideal_residual_energy_J":E*fac**2,
    "with_independently_bounded_residual_energy_0_01J_J":(math.sqrt(Er)+fac*math.sqrt(E))**2})
# A pinned/soft end joint's stability and the extra reaction carried by a guide.
P=8450.;ell=.27;kt=1000.
guides=[]
for a in [.05,.10,.15]:
 kg=max(0.,P*ell-kt)/(a*a)
 guides.append({"guide_arm_m":a,"minimum_guide_k_N_m_for_positive_tangent":kg,
  "guide_force_N_at_1mrad_on_threshold":kg*a*.001,
  "scope":"Small-angle single-column guide on one cut side; guide frame/reactions/contact/power-loss geometry not constructed."})
out={"scalar_ramps":rows,"ripple":profile,"modal_energy_envelopes":energy,
 "column":{"P_N":P,"unsupported_length_m":ell,"end_rotational_k_Nm_rad":kt,
 "no_guide_tangent_Nm_rad":kt-P*ell,"unbraced_length_threshold_m":kt/P,"guide_options":guides},
 "existing_release_component_scope":{"JAXA_LSRD_10K_load_N":10000,"diameter_m":.052,"length_m":.043,
 "mass_kg":.350,"catalogue_life_operations":20,"listed_actuation_s_max":.150,
 "scope":"Maker catalog only. No controlled force ramp, 500-cycle industrial life, shear/moment or cost supplied."},
 "fixed_ledgers":{"P2_existing_cost":13025.,"P2_manual":11678.,"P2_wafer_cost":11.26,
 "P2_wafer_cost_per_two_wafer_cartridge":22.52,
 "P2_ordinary_cartridge_cuts_to_avoid_for_parity_if_all_else_fixed":(13025.-11678.)/22.52,
 "P1_reusable_service_allowance_if_35USD_kit_replaced_and_all_else_fixed":35.-(54.41-45.10),
 "scope":"Architecture-specific marginal sensitivities only. No actual reusable release or full cost advantage."},
 "scope":"No all-time certificate for time-varying contact stiffness, impacts, structural collapse, hydraulic release, unknown modal frequencies or uncontrolled latch motion. Internal captured jam energy7.617J and hose/fluid energy1.36kJ are separate stocks and not erased by an outer-load ramp."}
p=Path(__file__).with_suffix(".json");p.write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({"output":str(p),"ripple":profile,"column":out["column"],"energy10Hz_halfsecond":next(e for e in energy if e["freq_min_Hz"]==10 and e["ramp_s"]==.5),"ledgers":out["fixed_ledgers"]},indent=2))
