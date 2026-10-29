import numpy as np,json
from pathlib import Path
rng=np.random.default_rng(202610291139);I=np.eye(2);pa=[np.array([[0,1],[1,0]]),np.array([[0,-1j],[1j,0]]),np.diag([1,-1])]
def kron(xs):
 a=np.ones((1,1),complex)
 for x in xs:a=np.kron(a,x)
 return a
def su2():
 q=rng.normal(size=4);q/=np.linalg.norm(q);return q[0]*I-1j*sum(q[j+1]*pa[j] for j in range(3))
s=np.array([0,1,-1,0])/np.sqrt(2);v=np.zeros(16);v[3]=v[12]=1/np.sqrt(3)
for j in [5,6,9,10]:v[j]=-1/(2*np.sqrt(3))
E=np.column_stack([np.kron(s,s),v]);assert np.linalg.norm(E.conj().T@E-np.eye(2))<1e-14
rows=[]
for trial in range(100):
 V=[su2() for _ in range(4)];W=kron(V);Wr=kron([x@V[0].conj().T for x in V]);C=kron([V[0]]*4)
 rows.append([float(np.linalg.norm(W-Wr@C)),float(np.linalg.norm(C@E-E)),float(np.linalg.norm(W@E-Wr@E))])
assert np.max(rows)<1e-12
out={'trials':100,'max_W_factorization_residual':np.max(rows,axis=0)[0],'max_collective_singlet_invariance_residual':np.max(rows,axis=0)[1],'max_relative_encoder_residual':np.max(rows,axis=0)[2],'scope':'Floating diagnostic of exact group factorization and singlet invariance, random nonidentity reference gauges; not hardware.'}
Path(__file__).with_name('GAUGE_CHECKS.json').write_text(json.dumps(out,indent=2)+'\n');print(out)
