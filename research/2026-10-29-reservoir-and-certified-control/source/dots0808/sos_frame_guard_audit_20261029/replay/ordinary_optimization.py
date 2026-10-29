"""Same-bank conventional optimization; no source matrices or true frames imported."""
import sys,json,time,numpy as np
from pathlib import Path
from fractions import Fraction as F
from scipy.optimize import minimize
P=Path(__file__).parent;sys.path.insert(0,str(P/'inputs'))
import received_quartic_sos_oracle as alg
bank=json.loads((P/'inputs/bank_one_axis.json').read_text());rows=[]
for edge in range(3):
 cert=json.loads((P/f'inputs/oracle_one_axis_edge{edge}.json').read_text());raw=alg.bank_polynomial(bank,edge);scale=cert['scale'];f={e:F(c,scale) for e,c in raw.items()};calls=[0];old=alg.value_grad
 def counted(coeff,q):calls[0]+=1;return old(coeff,q)
 alg.value_grad=counted;start=time.perf_counter();qr,upper=alg.find_candidate(f,seed=190+edge);secs=time.perf_counter()-start;alg.value_grad=old
 assert [str(q) for q in qr]==cert['rational_quaternion']
 # 24 predeclared starts; each analytic objective+gradient call costs five monomial
 # passes in existing implementation. Give function-only NM at most that pass budget.
 rng=np.random.default_rng(190+edge);starts=list(np.eye(4))+[rng.normal(size=4) for _ in range(20)];budget=5*calls[0];per=budget//24;coeff=np.array([float(f[e]) for e in alg.exps]);ncall=[0]
 def value(x):
  ncall[0]+=1;q=x/np.linalg.norm(x);return float(coeff@np.prod(q[None,:]**alg.E,axis=1))
 best=(float('inf'),None);runs=[];start=time.perf_counter()
 for q in starts:
  q=q/np.linalg.norm(q);res=minimize(value,q,method='Nelder-Mead',options={'maxfev':per,'xatol':1e-10,'fatol':1e-12});q=res.x/np.linalg.norm(res.x)
  if res.fun<best[0]:best=(float(res.fun),q)
  runs.append({'evaluations':int(res.nfev),'terminated_successfully':bool(res.success),'objective':float(res.fun)})
 nmsecs=time.perf_counter()-start;nmqr=alg.rational_candidate(best[1]);nmupper=alg.exact_eval(f,nmqr);assert ncall[0]<=budget
 rows.append({'edge':edge,'ordinary_SLSQP':{'rational_quaternion':[str(q) for q in qr],'identical_to_certified_candidate':True,'objective_plus_gradient_calls':calls[0],'monomial_pass_budget':budget,'runtime_seconds':secs,'normalized_empirical_loss':float(upper*scale/(4*bank['probe_calls']))},'ordinary_Nelder_Mead':{'rational_quaternion':[str(q) for q in nmqr],'function_evaluations':ncall[0],'monomial_pass_budget':budget,'runtime_seconds':nmsecs,'normalized_empirical_loss':float(nmupper*scale/(4*bank['probe_calls'])),'starts':runs},'certified_global_lower':cert['normalized_mean_loss_lower']})
res={'scope':'Same acquired bank only. SLSQP is exactly the candidate generator already used by SOS, with certification omitted. Function-only NM receives a declared equal monomial-pass budget to SLSQP gradient evaluations, not a claim of identical wallclock/hardware cost; all runtimes reported. No oracle source or hidden frame used.','rows':rows};(P/'ordinary_candidates.json').write_text(json.dumps(res,indent=2)+'\n');print([(r['edge'],r['ordinary_SLSQP']['normalized_empirical_loss'],r['ordinary_Nelder_Mead']['normalized_empirical_loss']) for r in rows])
