import numpy as np,json
from pathlib import Path
from mps_sampler import sample,MPOMPS
from compact import CompactMPS
out=[]
for early in [False,True]:
 for phy in [False,True]:
  for seed in range(40):
   _,s=sample(8,[[(0,1),(2,3),(4,5),(6,7)],[(0,4),(1,5),(2,6),(3,7)],[(1,2),(5,6)],[]]*15,.3,.2,np.random.default_rng(seed),error_budget=1e-7,validate=True,ordering='spectral',mpo=True,physical=phy,early=early,compact=True)
   out.append(dict(early=early,physical=phy,seed=seed,**s))
H=np.array([[1,1],[1,-1]])/np.sqrt(2);CX=np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]])
bridge=[]
for forced in [0,1]:
 c=CompactMPS(MPOMPS(0,tol=1e-12),3,[0,1,2]);c.one(0,H);c.pair(0,1,CX);c.pair(0,2,CX);c.one(1,H);before=c.vector();b,p=c.measure(1,np.random.default_rng(0),forced);after=c.vector();expected=before.copy();idx=np.arange(8);expected[((idx>>1)&1)!=forced]=0;expected/=np.linalg.norm(expected)
 bridge.append(dict(outcome=b,probability=p,active_ids=c.ids,amplitude_error=float(np.max(abs(after-expected))),surviving_bond=c.ts[0].shape[2]))
Path(__file__).with_name('compact_validation.json').write_text(json.dumps(dict(trajectories=out,virtual_bridge=bridge),indent=2));print(len(out),max(s['conditional_TV'] for s in out),max(s['born_error'] for s in out),bridge)
