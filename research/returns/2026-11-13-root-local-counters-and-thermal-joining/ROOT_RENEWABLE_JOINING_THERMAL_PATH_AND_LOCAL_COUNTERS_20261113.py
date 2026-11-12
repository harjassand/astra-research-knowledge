"""ROOT owned thermal-path and ionic-segmentation calculations.
All unreferenced properties introduced. No producer code or experiment.
"""
import math,json
from pathlib import Path
# Geometry of the available proposed folded supports, not a qualified material.
kappa=20.;w=.00030;t=.00040;leg=.001
G=2*100*4*kappa*w*t/(2*leg)
rho=7800.;cp=500.
C_islands=2*100*.002*.002*t*rho*cp
C_links=.00147*cp
rho_alloy=9500.;cp_alloy=150.;L_alloy=25000.
V_alloy=144e-6*.0001
m_alloy=rho_alloy*V_alloy
Ccontact=C_islands+C_links+m_alloy*cp_alloy
latent=m_alloy*L_alloy
Tm=62.
Cb=175.;Gb=.10;Gc=.02
def run(ambient,power,g=G,target=90.):
    h=0.;tb=ambient;energy=0.;time=0.;ambient_loss=0.
    solid_limit=Ccontact*(Tm-ambient)
    def temp(h):
        if h<solid_limit:return ambient+h/Ccontact
        if h<=solid_limit+latent:return Tm
        return Tm+(h-solid_limit-latent)/Ccontact
    def step(dt,p):
        nonlocal h,tb,energy,time,ambient_loss
        tc=temp(h);q=g*(tc-tb);qa=Gc*(tc-ambient)
        ambient_loss+=dt*(qa+Gb*(tb-ambient))
        h+=dt*(p-q-qa);tb+=dt*(q-Gb*(tb-ambient))/Cb
        energy+=p*dt;time+=dt
    events=[]
    for cycle_stage in ["join","release"]:
        before=energy;begin=time
        while temp(h)<target and time-begin<120.:
            step(.002,power)
        reached=temp(h)>=target
        # Qualification/restore cooling time is also a paid physical interval.
        cool_start=time
        while temp(h)>ambient+1. and time-cool_start<120.:
            step(.01,0.)
        events.append({"stage":cycle_stage,"reached_target":reached,
          "heat_s":cool_start-begin,"heat_plus_cool_s":time-begin,
          "purchased_heating_J":energy-before,"cool_to_ambient_plus1_s":time-cool_start,
          "cooled_within120s":temp(h)<=ambient+1.,"contact_final_C":temp(h),"body_final_C":tb})
        if cycle_stage=="join":
            # Propagate the finite body state throughout an actual 24h hold.
            # No artificial temperature reset or free sink is imposed.
            for _ in range(172800):step(.5,0.)
    balance=energy-ambient_loss-h-Cb*(tb-ambient)
    assert abs(balance)<1e-6, balance
    return {"ambient_C":ambient,"heater_W":power,"G_W_K":g,"target_C":target,
       "events":events,"two_event_heat_J":energy,
       "introduced_other_module_energy_J":350.,
       "potential_accepted_total_J_at_4pct_reject":(energy+350.)/.96,
       "within_nominal_energy_and_stage_time":all(e["reached_target"] and e["heat_plus_cool_s"]<=120. and e["cooled_within120s"] for e in events) and (energy+350.)/.96<=1000.,
       "thermal_energy_balance_residual_J":balance,
       "final_finite_body_C":tb,
       "scope":"Two lumped nodes and introduced constant material maps; no actual heater, supply, phase kinetics, wetting, strength/creep or reset qualification."}
cases=[run(amb,p,g) for amb in [20.,40.] for p in [3.6,20.,100.,200.] for g in [G,G/4]]
ionic=[]
for n in [1,2,3,6]:
    ionic.append({"segments":n,"optimistic_R_ohm":7.98/n**2,
      "optimistic_peak_channel_center_V":6.89/n**2,
      "optimistic_min_channel_heat_J":120.8/n**2,
      "condition":"Independent local counter access with unchanged useful current/flow/area. Counter insulation, current crowding and fabrication are not supplied."})
area_loss_limit=1-.95**(1/(500/.96))
creep=[]
for alloy_h in [10e-6,100e-6]:
    stress=500/(144e-6)
    creep.append({"alloy_thickness_m":alloy_h,"normal_stress_Pa":stress,
      "linear_Maxwell_eta_min_Pas_for_0_2mm_creep_in24h":stress*alloy_h*86400/.0002,
      "scope":"Required effective viscosity in this invented linear scalar creep law, not a measured alloy viscosity or fracture model."})
out={"geometry":{"thermal_G_both_faces_W_K":G,"contact_C_J_K":Ccontact,"latent_J":latent,
 "introduced_alloy_mass_kg":m_alloy,"islands_C_J_K":C_islands,"links_C_J_K":C_links,
 "thermal_model":"Two reservoirs, explicit finite body heat capacity and ambient conductance; heater energy integrated. 90C is a source experimental preparation temperature, not a proven optimal operating target."},
 "cases":cases,"ionic_segmentation":ionic,
 "restoration":{"area_loss_limit_per_attempt_for500accepted_4pctreject":area_loss_limit,
 "signed_drift_limit_m_per_attempt_for_1um_campaign":1e-6/(500/.96),
 "scope":"No proof that remaining area equals capacity or signed mean bounds local drift."},
 "creep_required":creep,
 "scope":"Owned conditional engineering mechanisms only. No actual fast renewable metal seam, 500-cycle mixed-load interface, full economic advantage or hardware experiment."}
assert abs(G-.96)<1e-12
assert abs(ionic[2]["optimistic_min_channel_heat_J"]-120.8/9)<1e-12
p=Path(__file__).with_suffix(".json");p.write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({"output":str(p),"geometry":out["geometry"],"cases":[{k:c[k] for k in ["ambient_C","heater_W","G_W_K","two_event_heat_J","potential_accepted_total_J_at_4pct_reject","within_nominal_energy_and_stage_time"]} for c in cases],"restoration":out["restoration"],"creep":creep},indent=2))
