import numpy as np, json
from pathlib import Path
Z=np.diag([1.,-1.]); I=np.eye(2); plus=np.ones(2)/np.sqrt(2)
def tn(a): return np.linalg.svd(a,compute_uv=False).sum()
def U(t): return np.diag(np.exp(-1j*t*np.array([1.,-1.])))
def psi(p): return np.sqrt(1-p)*np.kron(plus,[1,0])+np.sqrt(p)*np.kron(Z@plus,[0,1])
def out(p,t,K):
 v=np.kron(U(t),I)@psi(p); rho=np.outer(v,v.conj());return sum(np.kron(k,I)@rho@np.kron(k.conj().T,I) for k in K)
def loss(p,t,K):
 v=psi(p);return tn(out(p,t,K)-np.outer(v,v.conj()))/2
rng=np.random.default_rng(280612)
checks=0; max_cancel=0.; min_slack=1.
for p in [.05,.25,.49]:
 for d in [.001,.03,.2,.6]:
  v=psi(p); target=np.outer(v,v.conj())
  a=loss(p,0,[U(d)]); avg=(out(p,0,[U(d)])+out(p,0,[U(-d)]))/2
  err=max(abs(a-abs(np.sin(d))),abs(tn(avg-target)/2-np.sin(d)**2));max_cancel=max(max_cancel,err);assert err<1e-12
  for _ in range(100):
   x=rng.normal(size=(8,2))+1j*rng.normal(size=(8,2));q,_=np.linalg.qr(x);K=[q[2*i:2*i+2,:] for i in range(4)]
   slack=loss(p,d,K)+loss(p,-d,K)-p*np.sin(2*d);min_slack=min(min_slack,slack);assert slack>=-1e-12;checks+=1
for n in [1,2,10,100,10000]:
 d=1/(4*np.sqrt(n));tv=np.sqrt(-np.expm1(2*n*np.log(np.cos(2*d))))
 assert tv<=.5+1e-12
 assert np.sin(2*d)>=1/(np.pi*np.sqrt(n))
result={'status':'PASS_AUTHOR_FINITE_CHECKS_NOT_PROOF','arbitrary_CPTP_decoder_checks':checks,'minimum_pairwise_slack':float(min_slack),'max_exact_cancellation_residual':float(max_cancel),'scope':'Analytical proof governs; sampled decoder checks and scalar/cancellation fixtures only.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
