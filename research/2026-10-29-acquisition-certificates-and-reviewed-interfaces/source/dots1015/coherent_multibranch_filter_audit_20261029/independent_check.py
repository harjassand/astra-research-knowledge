import numpy as np,itertools,json
from pathlib import Path
rng=np.random.default_rng(708);I=np.eye(2);P=[I,np.array([[0,1],[1,0]]),np.array([[0,-1j],[1j,0]]),np.diag([1,-1])];ps=[np.kron(a,b) for a in P for b in P];d=4;mi=2;mo=3
v=rng.normal(size=(36,8))+1j*rng.normal(size=(36,8));v=np.linalg.qr(v)[0];ks=v.reshape(3,12,8)
def cj(a):
 v=np.asarray(a).reshape(-1,96);return v.T@v.conj()
conj=[[np.kron(p,np.eye(mo))@k@np.kron(p,np.eye(mi)) for k in ks] for p in ps];bar=np.mean(conj,axis=0);good=cj(bar);tw=sum(cj(a) for a in conj)/16;target=(good+tw)/2
branch=sum((cj([(conj[i][a]+conj[j][a])/2 for a in range(3)]) for i in range(16) for j in range(16)),np.zeros((96,96),complex))/256
check=np.zeros_like(branch)
for pad in ps:
 for q in ps:
  filtered=[(k+np.kron(q,np.eye(mo))@k@np.kron(q,np.eye(mi)))/2 for k in ks]
  check+=cj([np.kron(pad,np.eye(mo))@k@np.kron(pad,np.eye(mi)) for k in filtered])/256
# Choi effects and explicit correlated/reference positivity tests are implied by map equality;
# independently check effect scalar on L and complete channel trace preservation.
def effect(J):return np.trace(J.reshape(12,8,12,8),axis1=0,axis2=2).T
E=effect(target);Hm=np.einsum('amam->am',np.zeros((1,1,1,1))) if False else np.trace(E.reshape(4,2,4,2),axis1=0,axis2=2)/4
res={'k':2,'memory_in':mi,'memory_out':mo,'branch_residual':float(abs(branch-target).max()),'check_residual':float(abs(check-target).max()),'scalar_effect_residual':float(abs(E-np.kron(np.eye(4),Hm)).max()),'source_TP_residual':float(abs(sum(k.conj().T@k for k in ks)-np.eye(8)).max())}
assert max(v for k,v in res.items() if k.endswith('residual'))<1e-12
Path(__file__).with_name('independent_checks.json').write_text(json.dumps(res,indent=2)+'\n');print(res)
