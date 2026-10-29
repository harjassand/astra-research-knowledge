import numpy as np,json
from pathlib import Path
rng=np.random.default_rng(24398);rows=[]
for d in [2,3,5,9]:
 for case in range(30):
  b=rng.uniform(-1,1,d);z=rng.normal(size=(d,d))+1j*rng.normal(size=(d,d));X=(z+z.conj().T)/2;w=float(rng.uniform(.03,.7));L=64
  values=[]
  for u in np.arange(L)*w/L:
   ids=np.floor((b-u)/w).astype(int);Y=X*(ids[:,None]==ids[None,:]);values.append(np.linalg.norm(X-Y,'nuc'))
  comm=(b[:,None]-b[None,:])*X
  bound=np.sqrt(d*(np.linalg.norm(comm,'fro')*np.linalg.norm(X,'fro')/w+np.linalg.norm(X,'fro')**2/L))
  avg=np.mean(values);assert avg<=bound+1e-10
  # Exact continuous-offset HS square, no Monte Carlo.
  lhs=np.sum(np.abs(X)**2*np.minimum(1,np.abs(b[:,None]-b[None,:])/w));rhs=np.linalg.norm(comm,'fro')*np.linalg.norm(X,'fro')/w
  assert lhs<=rhs+1e-10
  rows.append(dict(d=d,case=case,mean_trace_disturbance=float(avg),bound=float(bound),exact_mean_hs_square=float(lhs)))
Path(__file__).with_suffix('.json').write_text(json.dumps({'scope':'120 matrix diagnostics, not physical QPE or decoder','cases':rows},indent=2)+'\n');print('PASS',len(rows))
