"""Small dense checks of the acquired frame algebra, not gate synthesis."""
import json
from pathlib import Path
import numpy as np
rng=np.random.default_rng(61031)
paulis=[np.array([[0,1],[1,0]],complex),np.diag([1.,-1.]),np.array([[0,-1j],[1j,0]])]
def tensor(bits):
 out=np.array([1.])
 for v in reversed(bits):out=np.kron(out,v)
 return out
def to_physical(v,n):
 out=np.empty_like(v)
 for z in range(1<<n):
  bit=0;x=0
  for j in range(n):bit^=(z>>j)&1;x|=bit<<j
  out[x]=v[z]
 return out
rows=[]
for n in [1,2,3,4,6,8]:
 qs=np.array([21/20 if rng.integers(2) else 20/21 for _ in range(n-1)])
 ts=(qs-1)/(qs+1);phis=[np.sqrt([q/(1+q),1/(1+q)]) for q in qs]
 perps=[np.array([p[1],-p[0]]) for p in phis];us=[p*np.array([1.,-1.]) for p in phis]
 plus=np.array([1.,1.])/np.sqrt(2);minus=np.array([1.,-1.])/np.sqrt(2)
 psi=to_physical(tensor([plus]+phis),n);W=[]
 for j in range(n):
  states=[minus]+[(us[e] if e<j-1 else perps[e] if e==j-1 else phis[e]) for e in range(n-1)]
  W.append(to_physical(tensor(states),n))
 W=np.array(W).T;d=1<<n
 V=np.array([psi*np.array([1-2*((x>>i)&1) for x in range(d)]) for i in range(n)]).T
 S=np.zeros((n,n))
 for j in range(n-1):S[j,j+1]=ts[j]
 D=np.diag(np.r_[1.,np.sqrt(1-ts*ts)])
 R=D@np.linalg.inv(np.eye(n)-S)
 errors={'frame_orthogonality':np.linalg.norm(W.T@W-np.eye(n)),'dark_orthogonality':np.linalg.norm(W.T@psi),'synthesis':np.linalg.norm(W@R-V),'covariance':np.linalg.norm(R.T@R-V.T@V)}
 # Verify that the highest occupied bond in the phi basis identifies the mark.
 for j in range(n):
  coords=[minus]+[(np.array([ts[e],np.sqrt(1-ts[e]**2)]) if e<j-1 else np.array([0.,1.]) if e==j-1 else np.array([1.,0.])) for e in range(n-1)]
  a=tensor(coords)
  wrong=sum(abs(a[z])**2 for z in range(d) if max([e for e in range(1,n) if (z>>e)&1],default=0)!=j)
  assert wrong<1e-20
 K=sum(np.kron(np.diag([1-2*((x>>i)&1) for x in range(d)]),paulis[i%3]/np.sqrt(n)) for i in range(n))
 inp=np.kron(psi[:,None],np.eye(2));stack=np.vstack([paulis[i%3]/np.sqrt(n) for i in range(n)])
 errors['offdiagonal_action']=np.linalg.norm(K@inp-np.kron(W@R,np.eye(2))@stack)
 # Actual heat-bath parent energy from exact conditional probabilities.
 pi=psi*psi;H=np.zeros((d,d))
 for i in range(n):
  for x in range(d):
   if (x>>i)&1:continue
   y=x^(1<<i);r0=pi[y]/(pi[x]+pi[y]);r1=1-r0
   v=np.zeros(d);v[x]=np.sqrt(r0);v[y]=-np.sqrt(r1);H+=np.outer(v,v)
 inj=inp.conj().T@K@np.kron(H,np.eye(2))@K@inp
 injection=float(np.linalg.eigvalsh(inj)[-1]);off=float(np.linalg.norm(K@inp,2)**2)
 assert injection<=1+1e-12 and off<=41/39+1e-12
 assert max(errors.values())<1e-11
 rows.append({'n':n,'max_algebra_residual':float(max(errors.values())),'actual_injection_norm_squared':injection,'injection_certificate':1,'actual_PQ_norm_squared':off,'PQ_certificate':41/39,'global_LCU_normalization_squared':n,'Neumann_LCU_normalization_upper':40/39})
 print(json.dumps(rows[-1]),flush=True)
Path(__file__).with_name('domain_wall_frame_checks.json').write_text(json.dumps({'scope':'Small dense diagnostic; scalable circuit proof separate','rows':rows},indent=2)+'\n')
