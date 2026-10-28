from pathlib import Path
import numpy as np,json,hashlib,itertools
from fractions import Fraction as F
rng=np.random.default_rng(635819)
he=lambda A:(A+A.conj().T)/2
x0=np.array([1,2,2,4],float)/5
H=np.array([[1,1,1,1],[1,1,-1,-1],[1,-1,1,-1],[1,-1,-1,1]],float)/2
U=np.zeros((8,8),complex)
for s,t,l in itertools.product(range(4),range(4),range(2)):U[2*s+l,2*t+l]=(np.eye(4) if l==0 else H)[s,t]
ps=[np.array([1,0]),np.array([0,1]),np.array([1,1])/np.sqrt(2),np.array([1,-1])/np.sqrt(2),np.array([1,1j])/np.sqrt(2),np.array([1,-1j])/np.sqrt(2)]
def Z(kraus,x):
 V=np.kron(x.reshape(4,1),np.eye(2));cols=[]
 for psi in ps:
  tag=np.array([-psi[1],psi[0]])
  for K in kraus:cols.append(np.kron(K@V@psi,tag)/np.sqrt(6))
 return np.column_stack(cols)
errs={'normalization':0.,'diagonal_polynomial':0.,'compatible_purification_bound_excess':0.,'weighted_ratio_bound_excess':0.,'task_root_transfer_excess':0.}
rows=[];models=0;probes=0
for eps in [1e-5,.001,.01,.03]:
 for model in range(8):
  Q0=rng.normal(size=(8,8))+1j*rng.normal(size=(8,8));A=he(Q0);ev,vec=np.linalg.eigh(A);rot=(vec*np.exp(1j*eps*ev))@vec.conj().T
  pp=rng.dirichlet(np.ones(3));kraus=[np.sqrt(p)*rot@np.diag(np.exp(1j*rng.uniform(-np.pi,np.pi,8)))@U for p in pp]
  zz=[Z(kraus,np.eye(4)[j]) for j in range(4)];gs=[np.column_stack([z[i] for z in zz]) for i in range(16)]
  bs=[he(g.conj().T@g).real for g in gs];pairs=[np.linalg.eigh(b) for b in bs]
  lam=np.array([e[-1] for e,v in pairs]);us=np.array([v[:,-1] for e,v in pairs]);tails=np.array([max(0,np.trace(b)-l) for b,l in zip(bs,lam)]);tail=tails.sum()
  kappa=float(np.min((us@x0)**2)/2);assert kappa>0
  Z0=Z(kraus,x0);T0=Z0@Z0.conj().T;srow=us/(us@x0)[:,None];w=np.diag(T0).real
  vv=us+.03*rng.normal(size=us.shape);vv/=np.linalg.norm(vv,axis=1)[:,None]
  sh=np.array([v/(v@x0) if abs(v@x0)**2>=kappa/4 else x0 for v in vv])
  e=np.maximum(0,1-np.sum(us*vv,axis=1)**2);good=tails<=lam/4
  er=sum(w*np.sum((sh-srow)**2,axis=1));eb=32/kappa*sum(lam[good]*e[good])+54*tail/kappa
  errs['weighted_ratio_bound_excess']=max(errs['weighted_ratio_bound_excess'],er-eb)
  VV,_=np.linalg.qr(rng.normal(size=(16,8))+1j*rng.normal(size=(16,8)));ks=[VV[2*j:2*j+2] for j in range(8)]
  C=sum(np.outer(K.T.reshape(-1),K.T.reshape(-1).conj()) for K in ks)
  for _ in range(6):
   x=rng.normal(size=4);x/=np.linalg.norm(x);zx=Z(kraus,x);T=zx@zx.conj().T;rr=srow@x;ref=rr[:,None]*Z0
   errs['normalization']=max(errs['normalization'],abs(np.trace(T).real-1))
   errs['diagonal_polynomial']=max(errs['diagonal_polynomial'],np.linalg.norm(np.diag(T).real-np.array([x@b@x for b in bs])))
   excess=np.linalg.norm(zx-ref)-2*np.sqrt(tail/kappa);errs['compatible_purification_bound_excess']=max(errs['compatible_purification_bound_excess'],excess)
   ell=1.5*np.trace(C.T@T).real;elp=1.5*np.trace(C.T@(ref@ref.conj().T)).real
   errs['task_root_transfer_excess']=max(errs['task_root_transfer_excess'],abs(np.sqrt(max(0,ell))-np.sqrt(max(0,elp)))-np.sqrt(12*tail/kappa))
   probes+=1
  rows.append({'rotation_scale':eps,'tau_row':float(tail),'balanced_kappa_for_test':kappa,'well_shaped_rows':int(sum(good))});models+=1
exact=0
for ga,ep,ka,d,L in itertools.product([F(1),F(1,7)],[F(1),F(1,19)],[F(1),F(1,200)],[4,16],[4,30]):
 N=2**38*d*L/(ka*ga*ep);m=ka*ga*ep/2**22
 assert F(9*2**21*d*L,1)/(ka*N)+72*m/ka<=ga*ep/8192
 assert 24*522<=2**14
 assert F(24,8192)+F(6,32768)<F(1,256)
 assert F(1,256)+F(1,128)<F(1,64)
 exact+=1
assert max(errs.values())<1e-10,errs
p=Path(__file__).with_name('WEIGHTED_NEAR_RANK_ONE_ROW_TAIL_EXTENSION.md')
out={'status':'PASS author compatible-physical-lift checks; independent receiving pending','source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'physical_perturbed_models':models,'encoder_probes':probes,'exact_budget_cases':exact,'max_residuals':errs,'model_rows':rows,'source_calls':0,'scope':'Known physical source Kraus fixtures rotated away from exact row rank one; one shared explicit six-state purification used across encoders. No pilot/source simulations, unknown PSD-completion substitution, finite-rank certificate or production optimizer.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:out[k] for k in ['status','source_sha256','physical_perturbed_models','encoder_probes','exact_budget_cases','max_residuals']},indent=2))
