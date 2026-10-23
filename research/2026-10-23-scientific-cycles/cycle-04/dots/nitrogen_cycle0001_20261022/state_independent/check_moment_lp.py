"""Independent scaled LP + dual certificate for supplied fixed mean and T.
This check does not recalculate parent caloric or global entropy bookkeeping.
"""
import json
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
import check_contraction as c
D=Path(__file__).resolve().parent
parent=json.loads((D.parent/'state_contraction/moment_bounds.json').read_text())
T=c.mp.mpf(str(parent['same_H_bath_T_K']));mean=parent['mean_excitation_eV']
E=np.array([float(x-c.N[0]) for x in c.N]);A=np.vstack([np.ones(60),E]);b=np.array([1.,mean]);rows=[]
for variant in ['literal','corrected_index']:
 a,_=c.smooth(variant=='literal')
 kv=np.array([float(c.mp.fsum(c.mp.exp(a[0][v][w]+a[1][v][w]/T+a[2][v][w]/T**2)/3 for w in range(48))) for v in range(60)])
 # The minimum is tiny relative to maximum. Scaling alone can mask it;
 # independently certify the parent proposed line over every state.
 pr=next(x for x in parent['rows'] if x['variant']==variant)
 for sense in ['min','max']:
  scale=pr[sense+'_forward_k_cm3_s'];sign=1 if sense=='min' else -1
  fit=linprog(sign*kv/scale,A_eq=A,b_eq=b,bounds=(0,None),method='highs',options={'dual_feasibility_tolerance':1e-9,'primal_feasibility_tolerance':1e-9})
  assert fit.success,fit.message
  support=np.flatnonzero(fit.x>1e-12).tolist()
  # Verify affine dual envelope in 60 digits from the maximizing/minimizing pair.
  i,j=support; ki=c.mp.mpf(str(kv[i]));kj=c.mp.mpf(str(kv[j]));ei=c.N[i]-c.N[0];ej=c.N[j]-c.N[0]
  slope=(kj-ki)/(ej-ei);intercept=ki-slope*ei
  slacks=[sign*(c.mp.mpf(str(kv[v]))-(intercept+slope*(c.N[v]-c.N[0]))) for v in range(60)]
  objective=float(fit.x@kv)
  rows.append(dict(variant=variant,sense=sense,success=fit.success,support=support,probabilities=fit.x[support].tolist(),forward_k_cm3_s=objective,relative_difference_from_parent=objective/pr[sense+'_forward_k_cm3_s']-1,normalization_residual=float(fit.x.sum()-1),mean_residual_eV=float(fit.x@E-mean),dual_affine_intercept=str(intercept),dual_affine_slope=str(slope),minimum_signed_dual_slack=str(min(slacks)),maximum_solver_dual_infeasibility=float(max(0,-min(fit.lower.marginals)))))
out=dict(scope=__doc__,input_temperature_K=str(T),input_mean_excitation_eV=mean,rows=rows,limits=['Static finite-table optimization only; no reachable population, achievable gain, or physical rate bound.','Near-dissociation and high-v fit applicability not independently validated.','Parent global entropy pass is not independently recomputed by this LP certificate.'])
(D/'moment_lp_receipt.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
