import numpy as np,json,itertools
from pathlib import Path
p=Path(__file__).parent;rng=np.random.default_rng(202610290539)
I=np.eye(2);pauli=[np.array([[0,1],[1,0]]),np.array([[0,-1j],[1j,0]]),np.diag([1,-1])]
S=np.array([[1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]],complex)
B=np.array([[1,0,1,0],[0,1,0,1],[0,1,0,-1],[1,0,-1,0]],complex)/np.sqrt(2)
signs=np.array([1,1,1,-1]);assert np.linalg.norm(S@B-B@np.diag(signs))<1e-12
T=[np.kron(a,b) for a in pauli for b in pauli];D=4
# Nonunital source that resets the whole triplet sector and preserves the singlet.
Ks=[np.outer(B[:,0],B[:,j].conj()) for j in range(3)]+[np.outer(B[:,3],B[:,3].conj())]
assert np.linalg.norm(sum(K.conj().T@K for K in Ks)-np.eye(4))<1e-12
assert np.linalg.norm(sum(K@K.conj().T for K in Ks)-np.eye(4))>1
A=np.linalg.qr(rng.normal(size=(16,4))+1j*rng.normal(size=(16,4)))[0];general=list(A.reshape(4,4,4))
def haar():
 q=rng.normal(size=4);q/=np.linalg.norm(q);return q[0]*I-1j*sum(q[j+1]*pauli[j] for j in range(3))
def coeff(U):
 W=np.kron(U,I);swap=W@S@W.conj().T
 x=np.array([np.trace((2*swap-np.eye(4))@t).real/4 for t in T]);R=x.reshape(3,3)
 assert np.linalg.norm(R.T@R-np.eye(3))<1e-12 and abs(np.linalg.det(R)-1)<1e-12
 return x,swap,W@B
rows=[];features=[]
for name,source in [('identity',[np.eye(4)]),('nonunital_common_swap',Ks),('arbitrary_CPTP',general)]:
 comm=[[t@K-K@t for K in source] for t in T]
 H=np.array([[sum(np.trace(a.conj().T@b).real for a,b in zip(ci,cj))/(16*D) for cj in comm] for ci in comm])
 assert np.linalg.eigvalsh(H).min()>-1e-12 and np.trace(H)<=3+1e-12
 xstar=np.eye(3).reshape(-1);maxerr=0.;maxquad=0.
 if name!='arbitrary_CPTP':assert np.linalg.norm(H@xstar)<1e-12
 for k in range(100):
  x,swap,bells=coeff(haar());features.append(np.outer(x,x).reshape(-1))
  direct=sum(abs(np.vdot(bells[:,j],K@bells[:,i]))**2 for K in source for i,j in itertools.product(range(4),repeat=2) if signs[i]!=signs[j])/4
  com=sum(np.linalg.norm(swap@K-K@swap)**2 for K in source)/(4*D)
  quad=x@H@x;maxerr=max(maxerr,abs(direct-com),abs(direct-quad))
  assert 0<=direct<=1+1e-12 and maxerr<1e-12
  if name!='arbitrary_CPTP':maxquad=max(maxquad,quad-3*np.linalg.norm(x-xstar)**2);assert maxquad<1e-12
 rows.append({'source':name,'max_Bell_sign_commutator_quadratic_discrepancy':float(maxerr),'H_min_eigenvalue':float(np.linalg.eigvalsh(H).min()),'H_trace':float(np.trace(H)),'common_swap_H_kernel_residual':float(np.linalg.norm(H@xstar))})
F=np.array(features);rank=np.linalg.matrix_rank(F,tol=1e-9);arank=np.linalg.matrix_rank(F-F[:1],tol=1e-9);assert rank==35 and arank==34
out={'status':'PASS_NUMERICAL_PHYSICAL_POSITIVE_PROBE_AND_GEOMETRY_CHECK','CPTP_sources':rows,'feature_linear_rank':int(rank),'feature_affine_rank':int(arank),'sampled_feature_rows':len(F),'scope':'Numerical mathematical checks of actual Bell-sign probability, including nonunital channel; not laboratory shots or a completed bandit controller.'};(p/'positive_probe_checks.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
