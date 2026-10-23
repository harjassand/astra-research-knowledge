"""Bounded native corrected-mechanism and conservative-energy checks."""
import sys,json,time,resource,hashlib,math
from pathlib import Path
from fractions import Fraction
import numpy as np
R=Path(__file__).resolve().parent;S=R.parents[1]/'nitrogen_quench_recovery_20261021';sys.path.insert(0,str(S));import cantera as ct
from paper_model import gas_model
from helper import ThermoKernel

def native_corrected(k):
 g=gas_model()
 for i in range(g.n_species):
  s=g.species(i);old=s.thermo;s.thermo=ct.NasaPoly2(old.min_temp,old.max_temp,old.reference_pressure,k.nasa[i]);g.modify_species(i,s)
 return g

def main():
 t=time.perf_counter();k=ThermoKernel();g=native_corrected(k);old=gas_model();rng=np.random.default_rng(20261021)
 T=[];Y=[];P=[]
 for p in [.5,.8,1,1.2,2]:
  for temp in [200.,300.,999.999999,1000.,1000.000001,2200.,2700.,3100.,3500.]:
   for yy in list(np.eye(6))+[np.ones(6)/6]:T.append(temp);Y.append(yy);P.append(p*101325)
 for _ in range(500):
  T.append(rng.uniform(200,3500));Y.append(rng.dirichlet(np.ones(6)*.2));P.append(rng.uniform(.5,2)*101325)
 T=np.array(T);Y=np.array(Y).T;P=np.array(P);a=k.evaluate(T,Y,P,strict=True,return_rates=True);n=len(T)
 b={q:np.empty(n) for q in ['rho','cp','cv','internal_energy','enthalpy','viscosity','conductivity']}
 b.update({q:np.empty((6,n)) for q in ['mass_production','h_species']});b.update({q:np.empty((7,n)) for q in ['forward','reverse']})
 for j in range(n):
  g.TPY=T[j],P[j],Y[:,j]
  for q,attr in [('rho','density'),('cp','cp_mass'),('cv','cv_mass'),('internal_energy','int_energy_mass'),('enthalpy','enthalpy_mass'),('viscosity','viscosity'),('conductivity','thermal_conductivity')]:b[q][j]=getattr(g,attr)
  b['mass_production'][:,j]=g.net_production_rates*g.molecular_weights;b['h_species'][:,j]=g.partial_molar_enthalpies/g.molecular_weights;b['forward'][:,j]=g.forward_rates_of_progress;b['reverse'][:,j]=g.reverse_rates_of_progress
 gross=b['forward']+b['reverse'];mgross=k.W[:,None]*(abs(k.nu)@gross)
 metrics={q:{'max_absolute_error':float(np.max(abs(a[q]-b[q]))),'max_relative_error_over_max1_abs':float(np.max(abs(a[q]-b[q])/np.maximum(1,abs(b[q]))))} for q in b if q not in ['forward','reverse','mass_production']}
 metrics['mass_production_error_over_gross_species_flux']=float(np.max(abs(a['mass_production']-b['mass_production'])/np.maximum(1e-300,mgross)))
 metrics['forward_relative_error']=float(np.max(abs(a['forward_rates_of_progress']-b['forward'])/np.maximum(1e-300,b['forward'])))
 metrics['reverse_relative_error']=float(np.max(abs(a['reverse_rates_of_progress']-b['reverse'])/np.maximum(1e-300,b['reverse'])))
 inv=k.temperature_from_internal_energy(a['internal_energy'],Y,strict=True)
 ru=k.evaluate_rho_u(a['rho'],a['rho']*a['internal_energy'],Y,strict=True)
 inversion={'max_T_error_K':float(max(abs(inv['T']-T))),'max_original_energy_residual_J_kg':float(max(abs(inv['diagnostics']['energy_residual_original_J_kg']))),'rho_u_pressure_error_Pa':float(max(abs(ru['pressure']-P))),'max_iterations':int(max(inv['diagnostics']['energy_iterations']))}
 # Analytic exact-rational Bernstein positivity of cp/R-1 polynomial on each branch.
 bounds=[]
 for i,name in enumerate(k.species_names):
  for lo,hi,co in [(200,1000,k.nasa[i,8:13]),(1000,3500,k.nasa[i,1:6])]:
   aa=[Fraction(float(v)) for v in co];aa[0]-=1
   power=[sum(aa[j]*math.comb(j,l)*lo**(j-l)*(hi-lo)**l for j in range(l,5)) for l in range(5)]
   bern=[sum(power[j]*Fraction(math.comb(i2,j),math.comb(4,j)) for j in range(i2+1)) for i2 in range(5)]
   v=min(bern);bounds.append({'species':name,'range_K':[lo,hi],'exact_lower_bound_cv_over_R_species':str(v),'lower_bound_float':float(v),'positive':v>0})
 # Exact formula bounds on rate perturbations: delta log kr = nu^T (da6/T-da7).
 changes=k.manifest['corrections'];dh=np.array([c['delta_high_a6_K'] for c in changes]);ds=np.array([c['delta_high_a7'] for c in changes])
 D1=k.nu.T@(dh/1000-ds);D2=k.nu.T@(dh/3100-ds);logmax=np.maximum(abs(D1),abs(D2));rbound=np.expm1(logmax)
 correction={'max_species_enthalpy_change_J_kg':max(abs(c['delta_high_h_J_kg']) for c in changes),'max_species_entropy_change_J_kg_K':max(abs(c['delta_high_s_J_kg_K']) for c in changes),'max_log_reverse_rate_change_300_3100K':list(map(float,logmax)),'relative_reverse_rate_change_bound_300_3100K':list(map(float,rbound)),'max_relative_reverse_rate_bound':float(max(rbound)),'scope':'Analytic endpoint bound on absolute log ratio, because correction is affine in1/T above1000K and zero below; both low branch and all forward rate constants unchanged. Not a bound on integrated trajectory error.'}
 # Demonstrate difference from original native operator, not just self-match.
 corrected_vs_original=[]
 for temp in [300.,1000.,1000.0001,1800.,2700.,3100.]:
  yy=np.ones(6)/6;old.TPY=temp,101325,yy;g.TPY=temp,101325,yy
  corrected_vs_original.append({'T_K':temp,'max_species_delta_h_J_kg':float(max(abs((g.partial_molar_enthalpies-old.partial_molar_enthalpies)/g.molecular_weights))),'max_log_reverse_constant_ratio':float(max(abs(np.log(g.reverse_rate_constants/old.reverse_rate_constants))))})
 invalid=[]
 tests=[('zero_pressure',lambda:k.evaluate(300,Y[:,0],0)),('outside_pressure',lambda:k.evaluate(300,Y[:,0],3*101325)),('nan_pressure',lambda:k.evaluate(300,Y[:,0],np.nan)),('negative_density',lambda:k.evaluate_rho_u(-1,1,Y[:,0])),('nan_energy',lambda:k.temperature_from_internal_energy(np.nan,Y[:,0])),('impossible_energy',lambda:k.temperature_from_internal_energy(1e12,Y[:,0])),('strict_negative_Y',lambda:k.evaluate(300,[-1,.2,.2,.2,.2,.2],strict=True)),('strict_clamp',lambda:k.temperature_from_internal_energy(1e12,Y[:,0],strict=True,trial_clamp=True)),('negative_atol',lambda:k.temperature_from_internal_energy(1,Y[:,0],atol=-1)),('invalid_iterations',lambda:k.temperature_from_internal_energy(1,Y[:,0],max_iter=True)),('loose_tolerance_domain_bypass',lambda:k.temperature_from_internal_energy(1e12,Y[:,0],atol=1e20))]
 for name,fn in tests:
  try:fn();invalid.append({'name':name,'rejected':False})
  except (ValueError,RuntimeError,FloatingPointError) as e:invalid.append({'name':name,'rejected':True,'error':str(e)})
 trial=k.temperature_from_internal_energy(1e12,Y[:,0],trial_clamp=True)
 bad=[]
 if metrics['mass_production_error_over_gross_species_flux']>1e-10:bad.append('rates')
 if inversion['max_T_error_K']>1e-7:bad.append('energy inversion')
 if not all(v['positive'] for v in bounds):bad.append('cv positivity')
 if not all(v['rejected'] for v in invalid):bad.append('invalid input rejection')
 if not trial['diagnostics']['energy_clamped'][0]:bad.append('trial clamp diagnostic')
 source_sha=hashlib.sha256((R.parents[1]/'nitrogen_regenerator_20261021/vector_kernel/cache.npz').read_bytes()).hexdigest()
 if source_sha!=k.manifest['original_cache_sha256']:bad.append('immutable source changed')
 result={'states':n,'pressure_range_Pa':[float(P.min()),float(P.max())],'metrics':metrics,'inversion':inversion,'cv_exact_rational_Bernstein_bounds':bounds,'model_correction_bounds':correction,'corrected_vs_original_native':corrected_vs_original,'invalid_tests':invalid,'trial_clamp_energy_residual_original_J_kg':float(trial['diagnostics']['energy_residual_original_J_kg'][0]),'failures':bad,'all_declared_gates_pass':not bad,'source_cache_unchanged':source_sha==k.manifest['original_cache_sha256'],'wall_s':time.perf_counter()-t,'rss_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
 (R/'validation.json').write_text(json.dumps(result,indent=2)+'\n');np.savez_compressed(R/'validation_states.npz',T=T,Y=Y,P=P,inverseT=inv['T']);print(json.dumps(result,indent=2));return 1 if bad else 0
if __name__=='__main__':raise SystemExit(main())
