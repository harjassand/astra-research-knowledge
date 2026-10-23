"""Inspect saved 100-us trajectory and evaluate one positive state natively.
No heater, mixing, cooling, or recycle ODE integration is executed.
"""
from pathlib import Path
import sys,ast,importlib.util,json,hashlib
import numpy as np
BASE=Path(__file__).resolve().parents[2]
D=BASE/'nitrogen_admissibility_20261022/recycle_quench'
sys.path.insert(0,str(BASE/'nitrogen_quench_recovery_20261021/deps'))
sys.path.insert(0,str(BASE/'nitrogen_finite_cycle_20261021/thermo_helper'))
from validate import native_corrected
sp=importlib.util.spec_from_file_location('_saved_check_signed',BASE/'nitrogen_finite_cycle_20261021/signed_trial_helper/helper.py')
m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);K=m.SignedTrialKernel();P=101325.
# Extract only the two pure pointwise property functions from the actual adapter.
# Importing the full source would run its heater at module scope, so do NOT do so.
source=D/'finite_mixing.py';tree=ast.parse(source.read_text())
functions=[node for node in tree.body if isinstance(node,ast.FunctionDef) and node.name in ['prop','enthalpy']]
assert len(functions)==2
ns={'K':K,'np':np,'P':P};exec(compile(ast.Module(body=functions,type_ignores=[]),str(source),'exec'),ns)
prop=ns['prop'];h=ns['enthalpy']
path=D/'mix_tau_0p0001_trajectory.npz';z=np.load(path)
x=z['progress'];state=z['mass_temperature'];j=int(np.argmin(abs(x-.5)));mass=state[:6,j];Y=mass/mass.sum();T=float(state[6,j]);assert np.all(Y>0)
hi,cp,rho,w=prop(T,Y)
g=native_corrected(K);g.TPY=T,P,Y
hn=g.partial_molar_enthalpies/g.molecular_weights;wn=g.net_production_rates*g.molecular_weights
gross=K.W*(abs(K.nu)@(g.forward_rates_of_progress+g.reverse_rates_of_progress))
point={
 'progress':float(x[j]),'T_K':T,'Y':Y.tolist(),
 'native_cantera_version':__import__('cantera').__version__,
 'max_species_h_absolute_difference_J_kg':float(max(abs(hi-hn))),
 'cp_relative_error':float(abs(cp-g.cp_mass)/g.cp_mass),
 'density_relative_error':float(abs(rho-g.density)/g.density),
 'mass_source_max_absolute_error_kg_m3_s':float(max(abs(w-wn))),
 'mass_source_max_error_over_gross_species_flux':float(max(abs(w-wn)/np.maximum(1e-300,gross))),
 'mass_source_adapter_kg_m3_s':w.tolist(),'mass_source_native_kg_m3_s':wn.tolist(),
}
yp=z['return_Y'];hr=h(300,yp);hh=h(float(state[6,0]),state[:6,0]/state[:6,0].sum())
Hres=[]
for xx,v in zip(x,state.T):
 mm=v[:6].sum();yy=v[:6]/mm;Hres.append(mm*h(float(v[6]),yy)-hh-.85*xx*hr)
ct=z['cool_t'];cy=z['cool_Y'];tm=float(state[6,-1]);ty=tm-1e4*ct;hm=h(tm,cy[:,0]);qr=[];q=[]
for tt,yy in zip(ty,cy.T):
 hi,cp,rho,w=prop(float(tt),yy)
 qr.append(1.85*(1e4*cp-hi@w/rho));q.append(1.85*(hm-h(float(tt),yy)))
qr=np.asarray(qr);q=np.asarray(q)
fresh=np.array([.79*K.W[0],.21*K.W[1],0,0,0,0]);fresh/=fresh.sum();tpre=min(tm,1700);pre=h(tpre,fresh)-h(300,fresh)
gaps=[]
for tt,qq in zip(ty,q):
 if 0<=qq<=pre:
  tc=float(K.temperature_from_enthalpy(h(tpre,fresh)-qq,fresh,P,strict=True)['T'][0]);gaps.append(float(tt-tc))
result={
 'scope':__doc__,'finite_source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
 'trajectory_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
 'pointwise_native_check':point,
 'saved_100us_path':{
  'mix_accepted_sample_count':len(x),'cool_accepted_sample_count':len(ct),
  'max_abs_mixing_enthalpy_balance_residual_J_kg_fresh':float(max(abs(np.asarray(Hres)))),
  'endpoint_mixing_enthalpy_balance_residual_J_kg_fresh':float(Hres[-1]),
  'minimum_signed_cooler_heat_removal_rate_J_per_kg_fresh_per_s':float(min(qr)),
  'maximum_signed_cooler_heat_removal_rate_J_per_kg_fresh_per_s':float(max(qr)),
  'negative_heat_removal_sample_count':int(sum(qr<0)),
  'cumulative_cooler_removed_heat_min_increment_J_kg_fresh':float(min(np.diff(q))),
  'minimum_sampled_pinch_K':float(min(gaps)),
  'negative_pinch_sample_count_below_minus_1e_minus_7_K':int(sum(np.asarray(gaps)<-1e-7)),
  'actual_mixer_exit_temperature_K':tm,
  'cooler_mass_inventory_kg_per_fresh_kg_s':1.85*(tm-300)/1e4,
 },
 'limitations':[
  'One positive-state source agreement is a narrow adapter check, not model validation.',
  'Saved-node heat/pinch checks do not prove behavior between accepted nodes or finite exchanger area.',
  'The zero-terminal-approach recuperator remains an infinite-area limit.',
  'The 100-us file is the parent tighter-rtol 2e-9 trajectory, preserved independently by its hash.',
 ]
}
(Path(__file__).resolve().parent/'finite_saved_checks.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
