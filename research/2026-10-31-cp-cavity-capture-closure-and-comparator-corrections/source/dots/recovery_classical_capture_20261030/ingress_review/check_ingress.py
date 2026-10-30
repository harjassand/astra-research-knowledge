import json, math
import numpy as np
from scipy.linalg import expm
rows=[]
for g in (0.1, 1., 10.):
 for lam in (.001, .1, 1.):
  for T in (.001,.1,1.,10.):
   copy=np.zeros((4,4)); reset=np.zeros((4,4))
   for b in (0,1):
    for c in (0,1):
     j=2*b+c
     copy[2*b+b,j]=1
     for bp in (0,1): reset[2*bp+c,j]=.5
   Q=g*(copy-np.eye(4))+lam*(reset-np.eye(4))
   out=expm(T*Q)
   dist=.5*np.sum(np.abs(out[:,0]-out[:,2]))
   err=(1-dist)/2
   J=2*g
   tau=min(T,1/(2*J))
   bound=-math.expm1(-lam*tau)/4
   specific=-math.expm1(-(lam+g)*T)*lam/(2*(lam+g))
   assert err+1e-12>=specific>=bound-1e-12
   rows.append(dict(g=g,lam=lam,T=T,error=err,specific_first_reset_bound=specific,root_bound=bound))
# Without a bounded ingress rule, instantaneous external copy followed by
# isolated perfect retention keeps m exactly even if B is immediately reset.
I_copy=np.zeros((4,4))
for b in (0,1):
 for c in (0,1): I_copy[2*b+b,2*b+c]=1
unbounded=reset@I_copy
unbounded_dist=.5*np.sum(abs(unbounded[:,0]-unbounded[:,2]))
assert abs(unbounded_dist-1)<1e-12
print(json.dumps(dict(checked=len(rows),min_margin=min(r['error']-r['root_bound'] for r in rows),instantaneous_copy_counterexample_dist=unbounded_dist,rows=rows),indent=2))
