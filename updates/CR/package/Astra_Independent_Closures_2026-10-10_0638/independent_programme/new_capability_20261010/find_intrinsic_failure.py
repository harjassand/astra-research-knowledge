import numpy as np,json,time
from itertools import combinations
from experiment import *
from lp_enclosure import solve_lp
rng=np.random.default_rng(601321)
for n in [5,6,7]:
 es=complete(n)
 for z in range(120):
  w=rng.choice([1.,2.,5.,10.,50.],len(es));p=rng.integers(-3,4,n).astype(float);p[-1]=-p[:-1].sum()
  if not any(p):continue
  A,K,T,f=native(n,es,w,p);lp=solve_lp(T,f,3)
  if lp['status']=='UNKNOWN':
   actual=exhaustive(A,K,w,p,T,f,3);cc=certificate(T,f,3,weight_search=300)
   out={'n':n,'edges':es,'weights':w.tolist(),'p':p.tolist(),'k':3,'lp':lp,'rho':cc.get('rho'),'actual_max_flow':float(max(np.max(abs(actual['hi'])),np.max(abs(actual['lo'])))),'positive_injection':float(p[p>0].sum()),'true_spectral_margin':actual['min_spectral_margin'],'actual_worst_per_edge':np.maximum(abs(actual['hi']),abs(actual['lo'])).tolist()}
   (ROOT/'intrinsic_failure.json').write_text(json.dumps(out,indent=2));print(json.dumps(out));raise SystemExit
print('none')
