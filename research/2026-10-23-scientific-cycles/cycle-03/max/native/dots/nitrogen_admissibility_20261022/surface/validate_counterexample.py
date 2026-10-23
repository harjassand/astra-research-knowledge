"""Independent integrator/energy inversion checks of the small counterexample."""
from pathlib import Path
import json,time,resource
import numpy as np
from scipy.optimize import brentq
import coupled_counterexample as c
start=time.monotonic(); baseline=json.loads((c.OUT/'coupled_counterexample.json').read_text())
rows=[]
for item in baseline['completions']:
 lam=item['lambda_dimensionless_hypothetical']
 rr,data=c.calculate(lam,method='Radau',rtol=2e-11,max_step=.002)
 Tenergy=np.array([brentq(lambda T:c.energy(nn,T)-c.Ustart,750,810,xtol=1e-10) for nn in data['n'].T])
 at=np.array([[2,0,1,0,1,1],[0,2,0,1,1,2]])
 entropy_reaction=[]
 homogeneous_balance=[]
 for nn,tt in zip(data['n'].T,data['T']):
  net,f,rev,lk=c.m.K.signed_rates(np.array([tt]),(nn/(1000*c.V))[:,None]);
  good=(f[:,0]>0)&(rev[:,0]>0)
  rate_entropy=np.sum(net[:,0][good]*np.log(f[:,0][good]/rev[:,0][good]))*1000*c.V*c.R
  entropy_reaction.append(rate_entropy)
  homogeneous_balance.append(at@(c.m.K.nu@net[:,0]))
 rows.append({'lambda':lam,'independent_method':'Radau','independent_rtol':2e-11,'independent_max_step_s':.002,'retention_fraction':rr['retained_NOx_fraction'],'abs_retention_difference_vs_BDF':abs(rr['retained_NOx_fraction']-item['retained_NOx_fraction']),
 'max_temperature_difference_vs_exact_total_energy_inversion_K':float(max(abs(data['T']-Tenergy))),
 'max_element_residual_mol_atoms_m2':rr['max_element_residual_mol_atoms_m2'],
 'minimum_accepted_species_mol_m2':rr['minimum_accepted_species_mol_m2'],
 'min_homogeneous_entropy_production_W_m2_K':float(min(entropy_reaction)),
 'max_homogeneous_element_source_residual_kmol_m3_s':float(np.max(np.abs(homogeneous_balance))),
 'max_forward_NO_collision_probability':rr['max_forward_NO_collision_probability'],
 'max_reverse_N2_collision_probability':rr['max_reverse_N2_collision_probability'],
 'max_reverse_O2_collision_probability':rr['max_reverse_O2_collision_probability']})
result={'checks':rows,'wall_s':time.monotonic()-start,'rss_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'limits':['Integrator cross-check is not a rigorous global error bound or positivity theorem.','Very small signed trace values use the existing trial extension; no significant negative concentration is silently projected.','Neither numerical agreement nor entropy consistency qualifies any surface rate for actual zirconia.']}
(c.OUT/'validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
