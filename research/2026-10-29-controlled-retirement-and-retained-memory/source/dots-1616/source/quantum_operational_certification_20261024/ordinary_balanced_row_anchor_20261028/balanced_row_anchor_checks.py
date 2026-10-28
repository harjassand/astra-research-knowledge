from pathlib import Path
from fractions import Fraction as F
import numpy as np, math, itertools, json, hashlib
rng=np.random.default_rng(635817)
# Finite fourth-design moments: exact rational coordinates, exact probabilities.
xs=[];ws=[]
for j in range(4):
 xs.append([F(i==j) for i in range(4)]);ws.append(F(1,12))
for signs in itertools.product([-1,1],repeat=4):
 xs.append([F(s,2) for s in signs]);ws.append(F(1,24))
assert sum(ws)==1
exact_mom=0
for i,j in itertools.product(range(4),repeat=2):
 assert sum(w*x[i]*x[j] for w,x in zip(ws,xs))==F(i==j,4);exact_mom+=1
for i,j,l,t in itertools.product(range(4),repeat=4):
 expect=F((i==j)*(l==t)+(i==l)*(j==t)+(i==t)*(j==l),24)
 assert sum(w*x[i]*x[j]*x[l]*x[t] for w,x in zip(ws,xs))==expect;exact_mom+=1
X=np.array(xs,float);weights=np.array(ws,float);x0=np.array([1,2,2,4],float)/5;kap=.01
conditional_res=0.;ratio_excess=0.;ratio_cases=0
for _ in range(240):
 u=rng.normal(size=4);u/=np.linalg.norm(u)
 pop=sum(w*np.outer(x,x)*(u@x)**2 for w,x in zip(weights,X))*4
 conditional_res=max(conditional_res,np.linalg.norm(pop-(np.eye(4)+2*np.outer(u,u))/6))
 while abs(u@x0)**2<kap:u=rng.normal(size=4);u/=np.linalg.norm(u)
 lam=10.**(-rng.uniform(0,16));a=u@x0;ss=u/a
 for noise in [1e-7,.01,.3,3.]:
  v=u+noise*rng.normal(size=4);v/=np.linalg.norm(v);e=1-(u@v)**2
  sh=v/(v@x0) if abs(v@x0)**2>=kap/4 else x0
  lhs=lam*a*a*np.sum((sh-ss)**2);rhs=32*lam*max(e,0)/kap
  ratio_excess=max(ratio_excess,lhs-rhs);assert lhs<=rhs+1e-12*lam
  assert np.linalg.norm(sh)<=2/math.sqrt(kap)+1e-12
  ratio_cases+=1
# Actual physical channels: coherent product-row isometry followed by unobserved diagonal noise.
H=np.array([[1,1,1,1],[1,1,-1,-1],[1,-1,1,-1],[1,-1,-1,1]],float)/2
U=np.zeros((8,8),complex)
for s,t,l in itertools.product(range(4),range(4),range(2)):U[2*s+l,2*t+l]=(np.eye(4) if l==0 else H)[s,t]
assert np.linalg.norm(U.conj().T@U-np.eye(8))<1e-12
us=np.array([(np.eye(4) if l==0 else H)[s] for s in range(4) for l in range(2) for a in range(2)])
lams=np.array([(1-.5*(a==l))/3 for s in range(4) for l in range(2) for a in range(2)])
assert np.min((us@x0)**2)>=kap-1e-15
assert np.linalg.norm(sum(w*np.outer(u,u) for w,u in zip(lams,us))-np.eye(4))<1e-12
sqrt=lambda A:(lambda ev,v:(v*np.sqrt(np.maximum(ev,0)))@v.conj().T)(*np.linalg.eigh((A+A.conj().T)/2))
def lossstate(kraus,x):
 V=np.kron(x.reshape(4,1),np.eye(2));AA=[K@V for K in kraus]
 J=sum(np.outer(a.reshape(-1),a.reshape(-1).conj()) for a in AA)/2
 rho=sum(a@a.conj().T for a in AA)/2
 return (2*np.kron(rho,np.eye(2))-J)/3
errs={'row_factor_identity':0.,'diagonal_effect_identity':0.,'decoder_partial_trace':0.,'root_risk_bound_excess':0.}
cases=0
for model in range(16):
 pp=rng.dirichlet(np.ones(3));kraus=[np.sqrt(p)*np.diag(np.exp(1j*rng.uniform(-math.pi,math.pi,8)))@U for p in pp]
 assert np.linalg.norm(sum(K.conj().T@K for K in kraus)-np.eye(8))<1e-12
 T0=lossstate(kraus,x0);basew=np.diag(T0).real
 z=.002+.04*rng.random();tau=(1-z)*T0+z*np.eye(16)/16
 f=np.trace(sqrt(sqrt(T0)@tau@sqrt(T0))).real;m=max(0,1-f)
 noisy=us+.015*rng.normal(size=us.shape);noisy/=np.linalg.norm(noisy,axis=1)[:,None]
 sh=np.array([v/(v@x0) if abs(v@x0)**2>=kap/4 else x0 for v in noisy]);ss=us/(us@x0)[:,None]
 Erow=sum(w*np.sum((a-b)**2) for w,a,b in zip(basew,sh,ss))
 ZZ=rng.normal(size=(16,8))+1j*rng.normal(size=(16,8));VV,_=np.linalg.qr(ZZ)
 ds=[VV[2*j:2*j+2,:] for j in range(8)]
 C=sum(np.outer(D.T.reshape(-1),D.T.reshape(-1).conj()) for D in ds)
 pt=np.einsum('iaja->ij',C.reshape(8,2,8,2));errs['decoder_partial_trace']=max(errs['decoder_partial_trace'],np.linalg.norm(pt-np.eye(8)))
 assert np.linalg.eigvalsh(C).max()<=2+1e-12
 for _ in range(8):
  x=rng.normal(size=4);x/=np.linalg.norm(x);T=lossstate(kraus,x);rr=ss@x;rh=sh@x
  pred=rr[:,None]*T0*rr[None,:];est=rh[:,None]*tau*rh[None,:]
  errs['row_factor_identity']=max(errs['row_factor_identity'],np.linalg.norm(T-pred))
  errs['diagonal_effect_identity']=max(errs['diagonal_effect_identity'],np.linalg.norm(np.diag(T).real-lams*(us@x)**2))
  ell=1.5*np.trace(C.T@T).real;eh=1.5*np.trace(C.T@est).real
  bound=math.sqrt(3*Erow)+math.sqrt(24*m/kap)
  errs['root_risk_bound_excess']=max(errs['root_risk_bound_excess'],abs(math.sqrt(max(0,ell))-math.sqrt(max(0,eh)))-bound)
  cases+=1
# Exact deterministic budget/constant checks (no enormous source bank is run).
scalar=0
for gam,eps,kappa,d,L in itertools.product([F(1),F(1,8)],[F(1),F(1,32)],[F(1),F(1,100)],[4,16],[4,30]):
 N=(2**32*d*L/(kappa*gam*eps));N=(N.numerator+N.denominator-1)//N.denominator
 Erow=F(2**17*d*L,1)/(kappa*N);m=kappa*gam*eps/2**20
 assert 6*Erow+48*m/kappa<=gam*eps/4096
 assert F(27,4096)<F(1,128)
 assert F(1,128)+F(1,128)==F(1,64)
 assert F(2,64)+F(1,2)<1
 scalar+=1
assert conditional_res<1e-12 and ratio_excess<1e-12
assert max(errs.values())<1e-10,errs
p=Path(__file__).with_name('BALANCED_RANK_ONE_ROW_ANCHOR_ACQUISITION.md')
out={'status':'PASS author finite identities and physical models; independent receiving pending','source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'exact_design_moments':exact_mom,'conditional_moment_cases':240,'weighted_ratio_cases':ratio_cases,'physical_models':16,'physical_encoder_probes':cases,'exact_budget_cases':scalar,'conditional_moment_max_residual':conditional_res,'weighted_ratio_max_excess':ratio_excess,'physical_max_residuals':errs,'source_calls':0,'scope':'No pilot/source-acquisition simulation, production tomography, SDP or hardware. Physical channel and arbitrary coherent CPTP decoder identities, finite-design moments, rare-mass-independent ratio inequalities and deterministic caps are checked. Rank-one diagonal and known balanced-basis promises are not inferred from these fixtures.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
