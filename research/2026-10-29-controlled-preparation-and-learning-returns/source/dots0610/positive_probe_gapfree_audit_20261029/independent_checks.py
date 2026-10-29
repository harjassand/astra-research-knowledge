import numpy as np,json,itertools,math
from scipy.linalg import expm
from pathlib import Path
rng=np.random.default_rng(295395);I=np.eye(2);X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]]);Z=np.diag([1.,-1.]);sig=[X,Y,Z];ops=[np.kron(a,b) for a in sig for b in sig]
bells=np.array([[1,0,0,1],[1,0,0,-1],[0,1,1,0],[0,1,-1,0]],complex).T/np.sqrt(2)
def kraus():
 ks=[rng.normal(size=(4,4))+1j*rng.normal(size=(4,4)) for _ in range(3)];v=sum(k.conj().T@k for k in ks);e,U=np.linalg.eigh(v);w=(U/np.sqrt(e))@U.conj().T;return [k@w for k in ks]
def rot(q):
 u=q[0]*I-1j*sum(q[i+1]*sig[i] for i in range(3));C=np.array([[np.trace(sig[a]@u@sig[b]@u.conj().T).real/2 for b in range(3)]for a in range(3)]);return u,C
rows=[]
for c in range(30):
 ks=kraus();q=rng.normal(size=4);q/=np.linalg.norm(q);u,C=rot(q);V=np.kron(u,I);S=(np.eye(4)+sum(C[a,b]*np.kron(sig[a],sig[b]) for a in range(3) for b in range(3)))/2
 probs=0
 for j in range(4):
  v=V@bells[:,j];rho=sum(k@np.outer(v,v.conj())@k.conj().T for k in ks);sgn=-1 if j==3 else 1;probs+=np.trace((np.eye(4)-sgn*S)/2@rho).real/4
 comm=sum(np.linalg.norm(S@k-k@S,'fro')**2 for k in ks)/16
 cs=[[O@k-k@O for O in ops] for k in ks]
 H=np.array([[sum(np.vdot(row[a],row[b]).real for row in cs)/64 for b in range(9)]for a in range(9)])
 pred=C.ravel()@H@C.ravel()
 assert abs(probs-comm)<1e-12 and abs(pred-probs)<1e-12
 assert np.linalg.eigvalsh(H).min()>-1e-12 and np.trace(H)<=3+1e-12
 rows.append({'case':c,'actual_sign_flip':probs,'quadratic_residual':abs(pred-probs),'trace_H':np.trace(H)})
# Exact common swap algebra, including retained-bath induced nonunital channel.
J=[np.kron(a,I)+np.kron(I,a) for a in sig];U=expm(-1j*(np.kron(J[0],X)+.7*np.kron(J[1],Y)))
ks=[U.reshape(4,2,4,2)[:,a,:,0] for a in range(2)]
S=(np.eye(4)+sum(np.kron(a,a) for a in sig))/2
zero=sum(np.linalg.norm(S@k-k@S,'fro')**2 for k in ks)/16
assert zero<1e-25
# Finite action span, affine issue, and conditional stochastic linear estimator.
Cs=[]
for k in itertools.product(range(-1,2),repeat=3):
 den=1+sum(x*x for x in k);q=np.array([1-sum(x*x for x in k),*[2*x for x in k]])/den;Cs.append(rot(q)[1])
tri=np.triu_indices(9);features=[]
for C in Cs:
 f=np.outer(C.ravel(),C.ravel());v=f[tri].copy();v[tri[0]!=tri[1]]*=np.sqrt(2);features.append(v)
A=np.array(features);u,s,v=np.linalg.svd(A,full_matrices=False);r=sum(s>1e-10);basis=v[:r].T;A=A@basis
weights=rng.dirichlet(np.ones(len(A)),size=80);xs=weights@A;mix=rng.dirichlet(np.ones(80));S2=np.einsum('i,ij,ik->jk',mix,xs,xs);ell=rng.normal(size=r)
# Build actual valid quadratic physical loss from previous H.
hv=H[tri].copy();hv[tri[0]!=tri[1]]*=np.sqrt(2);ell=basis.T@hv;qs=A@ell
assert qs.min()>-1e-12 and qs.max()<1+1e-12
estimate=sum(mix[j]*np.linalg.solve(S2,xs[j])*(weights[j]@qs) for j in range(len(xs)))
res=np.linalg.norm(estimate-ell);assert res<1e-9
rho=.07;thinned=sum(mix[j]*np.linalg.solve(S2,xs[j])*(rho*weights[j]@qs) for j in range(len(xs)));assert np.linalg.norm(thinned-rho*ell)<1e-9
out={'positive_probe_cases':rows,'common_zero_with_bath':zero,'finite_net_linear_rank':int(r),'affine_rank':int(np.linalg.matrix_rank(A-A[0],tol=1e-10)),'bernoulli_estimator_unbiased_residual':res,'scope':'Exact-channel expectation checks and finite convex-rounding estimator identities, not execution of tilted continuous-density bandit learner.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2));print({k:v for k,v in out.items() if k!='positive_probe_cases'})
