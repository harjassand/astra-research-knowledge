"""Finite actual RX ell=3 one-square syndrome test of inverse-noise compensation.
Not a large-code logical-lifetime test or full recursive memory decoder test.
"""
import sys,json,numpy as np
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'recursive_initialization'/'helpers'))
from actual_rx_rung import build
c=build(3);n=len(c['qs']);Z=c['Z'];m=len(Z)
cols=[sum(((z>>i)&1)<<j for j,z in enumerate(Z)) for i in range(n)]
valid={0}
for v in cols:valid|={s^v for s in list(valid)}
S=np.array(sorted(valid));ix={int(s):j for j,s in enumerate(S)}
perms=[np.array([ix[int(s)^v] for s in S]) for v in cols]
E=np.array([int(s).bit_count() for s in S])
res=[]
for beta in [0.5,1.,2.,4.]:
 p=np.exp(-beta*E);p/=sum(p)
 for q in [1e-7,1e-5,1e-3,1e-2]:
  pre=p.copy();invstates=[p.copy()]
  for perm in perms[::-1]:
   pre=((1-q)*pre-q*pre[perm])/(1-2*q);invstates.append(pre.copy())
  cur=pre.copy();maxerr=0.
  for k,perm in enumerate(perms):
   cur=(1-q)*cur+q*cur[perm]
   maxerr=max(maxerr,float(np.max(np.abs(cur-invstates[n-k-1]))))
  res.append(dict(beta=beta,q=q,n=n,valid_syndromes=len(S),min_pre=float(min(pre)),
    min_prefix=float(min(map(np.min,invstates))),sum_pre=float(sum(pre)),
    final_l1=float(sum(abs(cur-p))),prefix_identity_max=maxerr,
    max_ratio=float(max(pre/p)),min_ratio=float(min(pre/p))))
assert max(x['final_l1'] for x in res)<1e-12
assert max(x['prefix_identity_max'] for x in res)<1e-12
out=ROOT/'calibrated_terminal_inverse_results.json'
out.write_text(json.dumps(res,indent=2));print(json.dumps(res,indent=2))
