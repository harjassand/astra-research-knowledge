"""Bounded LP proposals for the actual weighted-design entropy inequality.

Finite moment cubature plus a 3-phase twirl is an actual projective2design
when its rational moments are qualified. Floating LP status is no proof.
"""
from pathlib import Path
import json,time
import numpy as np
from scipy.optimize import linprog
HERE=Path(__file__).resolve().parent
START=time.perf_counter();runs=[];best=None
for n in [12,24,48]:
 integer=np.array([(i,j,n-i-j)for i in range(n+1)for j in range(n+1-i)])
 y=integer/n
 eq=np.array([np.ones(len(y)),y[:,0],y[:,1],y[:,0]**2,y[:,0]*y[:,1],y[:,1]**2])
 rhs=np.array([1,1/3,1/3,1/6,1/12,1/6])
 for t in [.5,1,2,4,8]:
  for ratio in [0,.25,.5,.75,1]:
   k=np.array([t,t*ratio,0]);z=np.exp(2*(y@k-t))
   r=linprog(-z,A_eq=eq,b_eq=rhs,bounds=(0,None),method='highs')
   assert r.success
   reference=(np.exp(k-t).sum()/3)**2
   value=z@r.x;logratio=float(np.log(value/reference))
   result={'denominator':n,'k':k.tolist(),'log_exp_ratio':logratio,
    'moment_residual_max':float(np.max(np.abs(eq@r.x-rhs))),
    'support':[[integer[i].tolist(),float(r.x[i])]for i in np.flatnonzero(r.x>1e-9)]}
   runs.append(result)
   if best is None or logratio>best['log_exp_ratio']:best=result
out={'status':'FLOATING_LP_PROPOSALS_ONLY','runs':runs,'best':best,
 'seconds_after_imports':time.perf_counter()-START,
 'scope':'Finite rational-simplex grids and25 diagonal K values per grid. No universal theorem or certified entropy counterexample.'}
(HERE/'PROPOSALS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'best':best,'seconds':out['seconds_after_imports']},indent=2))
