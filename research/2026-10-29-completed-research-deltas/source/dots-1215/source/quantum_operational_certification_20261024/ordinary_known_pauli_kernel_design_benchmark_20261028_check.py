from pathlib import Path
import numpy as np,math,json,hashlib
root=Path(__file__).resolve().parent;rng=np.random.default_rng(28101027)
I=np.eye(2);X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]]);Z=np.diag([1.,-1.]);Ps=[I,X,Y,Z]
phi=np.array([1,0,0,1],complex)/math.sqrt(2);bells=[np.outer(np.kron(P,I)@phi,(np.kron(P,I)@phi).conj()) for P in Ps]
inputs=[(I+s*P)/2 for P in [X,Y,Z] for s in [-1,1]]
physical=0;maxloss=0.;maxT=0.
for G in [1,2,3]:
 As=[]
 for _ in range(4*G):
  M=rng.normal(size=(4,4));As.append(M@M.T)
 total=sum(As);e,V=np.linalg.eigh(total);inv=(V/e**.5)@V.T;As=[inv@A@inv for A in As]
 assert np.max(abs(sum(As)-np.eye(4)))<1e-12
 for _ in range(8):
  x=rng.normal(size=4);x/=np.linalg.norm(x);pp=np.array([x@A@x for A in As]).reshape(G,4);ww=pp.sum(axis=1)
  lam=(ww[:,None]-pp)/3
  T=np.zeros((4*G,4*G),complex)
  for g in range(G):T[4*g:4*g+4,4*g:4*g+4]=sum(lam[g,a]*bells[a] for a in range(4))
  T6=np.zeros_like(T)
  for P in inputs:
   for g in range(G):
    out=sum(pp[g,a]*(Ps[a]@P@Ps[a].conj().T) for a in range(4))
    T6[4*g:4*g+4,4*g:4*g+4]+=np.kron(out,(I-P).T)/6
  maxT=max(maxT,np.max(abs(T-T6)));assert np.max(abs(T-T6))<1e-12
  ell=sum(ww-pp.max(axis=1));ell2=3*sum(lam.min(axis=1));maxloss=max(maxloss,abs(ell-ell2));assert abs(ell-ell2)<1e-12
  # Execute the formula for the actual optimal block-Pauli Choi decoder.
  CT=np.zeros_like(T)
  for g in range(G):CT[4*g:4*g+4,4*g:4*g+4]=2*bells[int(np.argmin(lam[g]))]
  assert abs(1.5*np.trace(T@CT).real-ell)<1e-12
  physical+=1
selection=0;maxratio=0.
for G in [1,2,4,8]:
 for gamma in [.1,.5,1.]:
  for eps in [.001,.02,.2]:
   t=gamma*eps/(168*G)
   for rep in range(10):
    prob=rng.dirichlet(np.ones(4*G),size=7).reshape(7,G,4)
    if rep%2==0:
     weights=rng.dirichlet(np.ones(G));prob[0]=0
     for g in range(G):prob[0,g,int(rng.integers(4))]=weights[g]
    lam=(prob.sum(axis=2)[:,:,None]-prob)/3
    err=np.sqrt(t*lam)+t;est=lam+rng.uniform(-1,1,size=lam.shape)*err
    xs=int(np.argmin(3*est.min(axis=2).sum(axis=1)));corr=est[xs].argmin(axis=1)
    actual=3*sum(lam[xs,g,corr[g]] for g in range(G));best=3*lam.min(axis=2).sum(axis=1).min()
    bound=(1+gamma/2)*best+21*G*t/gamma
    assert actual<=bound+1e-12
    maxratio=max(maxratio,(actual-(1+gamma/2)*best)/(21*G*t/gamma));selection+=1
p=root/'ordinary_known_pauli_kernel_design_benchmark_20261028.md'
o={'status':'PASS_AUTHOR_KNOWN_KERNEL_BENCHMARK','source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'physical_POVM_Pauli_source_cases':physical,'max_ordinary_T_identity_residual':float(maxT),'max_full_CPTP_optimum_identity_residual':float(maxloss),'finite_decision_bound_cases':selection,'maximum_additive_budget_fraction':float(maxratio),'scope':'Known flag/Pauli dictionary, no spectral floor; not generic unknown-direction acquisition or hardware.'}
(root/'ordinary_known_pauli_kernel_design_benchmark_20261028_check.json').write_text(json.dumps(o,indent=2)+'\n');print(json.dumps(o,indent=2))
