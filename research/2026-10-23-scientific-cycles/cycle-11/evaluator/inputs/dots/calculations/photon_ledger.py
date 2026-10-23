"""Finite photon accounting; no kinetic trajectory, fit or plant model."""
from pathlib import Path
import math,json,time,resource
start=time.perf_counter()
ROOT=Path(__file__).resolve().parent
v=json.loads((ROOT/'inputs.json').read_text())
h=6.62607015e-34;c=299792458.;NA=6.02214076e23
E=h*c/(v['wavelength_nm']*1e-9)*NA
f=v['fixture']; R=f['radius_um']*1e-4; V=4*math.pi*R**3/3/1000
N=f['concentration_M']*V
P=f['sample_power_W']; ep=v['effective_epsilon_phi_Minv_cminv']
def row(ep):
 b=math.log(10)*ep*f['concentration_M']; action=b*2*R
 rate=P/E*action; k=rate/N; y=v['conditional_net_disappearance_fraction']; t=-math.log1p(-y)/k
 # Independent direct source Eq1 uses wavelength and speed consistently in cm.
 k_eq1=P/R**2*(3*(v['wavelength_nm']*1e-7)/(2*math.pi*h*(c*100)))*(1000*math.log(10)/NA)*ep
 assert math.isclose(k,k_eq1,rel_tol=2e-15)
 slab_area=V*1000/(2*R)
 assert math.isclose(slab_area*2*R/1000,V,rel_tol=1e-15)
 return {'epsilon_phi':ep,'effective_events_per_incident_photon_upper':action,'initial_effective_event_rate_mol_s_upper':rate,
  'ideal_firstorder_rate_s':k,'ideal_half_life_min':math.log(2)/k/60,
  'incident_J_per_mol_effective_event_lower':E/action,
  'conditional_90pct_net_loss_time_s':t,'conditional_J_per_mol_net_loss_lower':P*t/(N*y),
  'matched_volume_same_path_slab_area_cm2':slab_area,'matched_volume_same_path_slab_rate_equal':True,
  'one_cm_path_throughput_ratio_if_same_coefficient_capture_and_thin_limit':v['ordinary_long_path_cm']/(2*R),
  'one_cm_path_event_energy_lower_J_per_mol':E/(b*v['ordinary_long_path_cm']),
  'necessary_path_cm_for_0p1_effective_events_per_photon':v['target_effective_events_per_photon']/b}
rows=[row(ep-v['quoted_plusminus']),row(ep),row(ep+v['quoted_plusminus'])]
scale=[]
for s in v['source_meroni_geometry_sensitivity']:
 r=s['radius_um']*1e-4;p=s['reported_power_W']*s['sample_fraction_assumption']
 k=p/r**2*(3*(v['wavelength_nm']*1e-7)/(2*math.pi*h*c*100))*(1000*math.log(10)/NA)*ep
 scale.append(dict(s,model_initiation_rate_s=k,status='scale sensitivity only; nitrate plateau-fit rate is a different observable'))
# Algebraic hostile checks: faster fraction is not greater throughput.
r30=rows[1]['initial_effective_event_rate_mol_s_upper']
r15=P/E*math.log(10)*ep*f['concentration_M']*(R)
k30=rows[1]['ideal_firstorder_rate_s']; n15=N/8
assert math.isclose(r15/r30,0.5) and math.isclose((r15/n15)/k30,4)
assert E/(math.log(10)*ep*f['concentration_M']*2*R)>1e12
out={'photon_energy_J_per_mol':E,'fixture_inventory_mol':N,'rows_low_central_high_quoted_coefficient':rows,
 'meroni_power_scale_sensitivity':scale,'halving_R_fixed_P_C':{'fractional_rate_ratio':4,'molar_rate_ratio':0.5},
 'interpretation':'No original-N closure, nitrate quantum yield, plant SEC, optical absorption epsilon alone, or universal surface exclusion is inferred.',
 'cost':{'body_wall_seconds':time.perf_counter()-start,'peak_RSS_KiB_Linux':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'total_research_cost':'unknown'}}
(ROOT/'results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
