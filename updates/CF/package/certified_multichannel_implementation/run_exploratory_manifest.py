"""Bounded empirical sweep from exact rational coefficient input. NOT CERTIFIED.

Each solver is charged for rational parsing/rescaling. Candidate additionally
rebuilds the discriminant and approximates its roots on every cold row. Numerical
module import startup is recorded once, separately from per-row cold setup.
"""
import time
startup=time.perf_counter()
import json,hashlib,platform,resource,math
from pathlib import Path
import sympy as sp
import numpy as np
import prototype_numpy as candidate
import baseline_cf4 as baseline
startup_seconds=time.perf_counter()-startup
BASE=Path(__file__).parent

def acquisition(row,want_roots):
 start=time.perf_counter();t,u,lam=sp.symbols('t u lam');eta=sp.Rational(row['eta']);omega=sp.Rational(row['omega'])
 C=[sp.Matrix([[sp.Rational(x) for x in r] for r in a]) for a in row['coefficients_ascending_t']]
 H=sum((C[j]*t**j for j in range(len(C))),sp.zeros(3))
 A=(omega*eta*H.subs(t,sp.Rational(1,2)+eta*u)).applyfunc(sp.expand)
 k=sp.Rational(2)**row['frequency_offset']
 expected=k*sp.Matrix([[u*u-1,1,sp.Rational(1,3)],[1,u/3,2],[sp.Rational(1,3),2,-u*u-u/3+1]])
 assert A==expected
 # Runtime adaptation is valid for precisely the supplied rational family.
 roots=None;degree=None
 if want_roots:
  poly=(A/k).charpoly(lam).as_expr();disc=sp.Poly(sp.discriminant(poly,lam),u);degree=disc.degree()
  roots=[complex(x) for x in sp.nroots(disc,n=25,maxsteps=100)]
 return roots,{'seconds':time.perf_counter()-start,'exact_input_rescaling_checked':True,'discriminant_degree':degree,'root_method':'SymPy nroots, approximate only' if want_roots else None,'root_working_decimal_digits':25 if want_roots else None}

manifest=json.loads((BASE/'benchmark_manifest.json').read_text());budget=110.;started=time.perf_counter();results=[]
for row in manifest['rows']:
 B=row['B'];f=row['frequency_offset'];s=row['precision_bits'];out={'id':row['id'],'sweeps':row['sweeps'],'target_operator_tolerance':float(sp.Rational(row['operator_tolerance'])),'certified':False}
 # Simple engineering guard, not an endpoint-error certificate.
 action_est=2.**f*(2.**(3*(B-1)+1)/3+2.**B*(2.**(B-1)+5))
 bits_needed=s+math.ceil(math.log2(1+action_est))+10
 if bits_needed>53:
  out.update(status='not_run_precision_guard',reason='double-precision exploratory implementation cannot safely represent the estimated scalar phases at this requested tolerance',engineering_phase_bits_estimate=bits_needed)
  results.append(out);continue
 if time.perf_counter()-started>budget:
  out.update(status='not_run_total_budget');results.append(out);continue
 roots,acq=acquisition(row,True);L=34 if s>=28 else 26
 r,U=candidate.run(B,f,s,min(30.,budget-(time.perf_counter()-started)),L=L,N=6,acquired_roots=roots)
 r['acquisition']=acq;r['cold_row_seconds']=r['seconds']+acq['seconds'];r['working_mantissa_bits']=53;r['certification_cost']=None
 out['candidate']=r
 if r['status']=='complete_uncertified':
  if B<=4:
   V,ref=candidate.reference(B,f,rtol=2.3e-14 if s>=28 else 2e-12)
   out['independent_reference']={**ref,'observed_operator_disagreement':float(np.linalg.norm(U-V,2))}
  if time.perf_counter()-started<budget:
   _,ba=acquisition(row,False)
   br,V=baseline.run(B,f,s,min(30.,budget-(time.perf_counter()-started)),safety=1.)
   br.update(acquisition=ba,cold_row_seconds=br['seconds']+ba['seconds'],working_mantissa_bits=53,certification_cost=None)
   if br['status']=='complete_uncertified':br['observed_operator_disagreement_from_candidate']=float(np.linalg.norm(U-V,2))
   out['baseline']=br
 out['status']='empirical_only';results.append(out)
 (BASE/'exploratory_manifest_checkpoint.json').write_text(json.dumps(results,indent=2)+'\n')
 print(json.dumps({'id':row['id'],'candidate_status':r['status'],'candidate_seconds':r['cold_row_seconds'],'baseline_status':out.get('baseline',{}).get('status'),'baseline_seconds':out.get('baseline',{}).get('cold_row_seconds')}),flush=True)

summary={'purpose':'bounded empirical mechanism sweep, not certified theorem execution','certified':False,'manifest_sha256':hashlib.sha256((BASE/'benchmark_manifest.json').read_bytes()).hexdigest(),'module_startup_seconds':startup_seconds,'sweep_elapsed_seconds':time.perf_counter()-started,'sweep_budget_seconds':budget,'prior_exploratory_native_seconds_approximate':60.,'python_version':platform.python_version(),'numpy_version':np.__version__,'sympy_version':sp.__version__,'resident_memory_high_water_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'root_enclosures_certified':False,'phase_systems_baseline_available':False,'rows':results}
(BASE/'exploratory_manifest_results.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps({k:v for k,v in summary.items() if k!='rows'},indent=2))
