"""Small dense diagnostics only; not proof or an efficient large-source simulator."""
import json
from pathlib import Path
import numpy as np
from scipy.linalg import expm
rng=np.random.default_rng(31871)
n=4; d=2
P0=np.zeros((n,n))
for x in range(n):
 for r in range(2): P0[((x<<1)&3)|r,x]+=.5
pi=np.ones(n)/n;Pi=np.outer(pi,np.ones(n))
assert np.allclose(P0@P0,Pi)
R=np.eye(n)[:,[1,3,0,2]]
alpha=1e-4;P1=(1-alpha)*P0+alpha*R
eta=np.linalg.norm(P1-P0,1)
Z=np.diag([1.,-1.]);X=np.array([[0.,1.],[1.,0.]])
Hs=[.06*Z,.08*X,-.06*Z,-.08*X];b=.08;m=2;T=.7
V=np.zeros((16,16),complex)
for x,H in enumerate(Hs):V[4*x:4*x+4,4*x:4*x+4]=-1j*(np.kron(np.eye(2),H)-np.kron(H.T,np.eye(2)))
def gen(P,lam):return lam*np.kron(P-np.eye(n),np.eye(4))+np.sqrt(lam)*V
def norm(v):return sum(np.linalg.svd(v[4*x:4*x+4].reshape((2,2),order='F'),compute_uv=False).sum() for x in range(n))
inputs=[]
for j in range(12):
 blocks=[]
 for x in range(n):
  A=rng.normal(size=(2,2))+1j*rng.normal(size=(2,2));blocks.append(A@A.conj().T)
 total=sum(np.trace(A).real for A in blocks)
 inputs.append(np.concatenate([(A/total).reshape(-1,order='F') for A in blocks]))
rows=[]
for lam in [0,1,100,1000,10000,100000]:
 delta=expm(T*gen(P1,lam))-expm(T*gen(P0,lam))
 observed=max(norm(delta@v) for v in inputs)
 bound=min(2.,eta*(72*m+4096*b*b*m*m*T))
 assert observed<=bound+1e-8
 rows.append({'lambda':lam,'max_sampled_CQ_trace_distance':float(observed),'all_rate_bound':bound})
report={'scope':'Dense diagnostic on 12 CQ states; not a complete-norm proof or practical advantage test','eta':eta,'m':m,'b':b,'T':T,'rows':rows}
Path(__file__).with_name('cq_robustness_checks.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
