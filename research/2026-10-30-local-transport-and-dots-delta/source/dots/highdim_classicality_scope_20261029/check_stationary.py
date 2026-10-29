import numpy as np, math,json
from pathlib import Path
rng=np.random.default_rng(517)
rows=[]
for L in [2,3,4]:
 k=[2**j for j in range(L)];ds=[x+1 for x in k];off=np.cumsum([0]+ds);D=sum(ds)
 for eps in [0.,.2]:
  r=np.ones(L)*eps/L;r[-1]+=1-eps
  tails=np.cumsum(r[::-1])[::-1];Z=sum(tails);p=tails/Z
  tau=np.diag(np.concatenate([np.ones(ds[j])*r[j]/ds[j] for j in range(L)]))
  sigma=np.diag(np.concatenate([np.ones(ds[j])*p[j]/ds[j] for j in range(L)]))
  K=[]
  for j in range(1,L):
   half=k[j]//2
   for b in range(half+1):
    A=np.zeros((D,D),complex)
    for a in range(half+1):
     A[off[j-1]+a,off[j]+a+b]=math.sqrt(math.comb(half,a)*math.comb(half,b)/math.comb(k[j],a+b))
    K.append(A)
  for q,v in enumerate(np.diag(tau)):
   if v>0:
    for a in range(ds[0]):
     A=np.zeros((D,D),complex);A[q,a]=math.sqrt(v);K.append(A)
  app=lambda X:sum((A@X@A.conj().T for A in K),np.zeros((D,D),complex))
  tp=np.linalg.norm(sum((A.conj().T@A for A in K),np.zeros((D,D)))-np.eye(D))
  fixed=np.linalg.norm(app(sigma)-sigma)
  disturb=0.;power_err=0.;entropy_err=0.
  # Phi^L is the explicit sector-measure/reprepare channel below.
  outputs=[]
  for j in range(L):
   Y=tau.copy()
   for _ in range(L-j-1):Y=app(Y)
   outputs.append(Y)
  for trial in range(8):
   z=rng.normal(size=2)+1j*rng.normal(size=2);z/=np.linalg.norm(z)
   rho=np.zeros((D,D),complex)
   for j in range(L):
    v=np.array([math.sqrt(math.comb(k[j],a))*z[0]**(k[j]-a)*z[1]**a for a in range(ds[j])])
    rho[off[j]:off[j+1],off[j]:off[j+1]]=p[j]*np.outer(v,v.conj())
   out=app(rho)
   dist=sum(abs(np.linalg.eigvalsh(out-rho)))/2
   expect=p[0]*sum(r[j]*(1-1/ds[j]) for j in range(L))
   disturb=max(disturb,abs(dist-expect))
   A=rng.normal(size=(D,D))+1j*rng.normal(size=(D,D));X=A@A.conj().T;X/=np.trace(X)
   Y=X
   for _ in range(L):Y=app(Y)
   EY=sum(np.trace(X[off[j]:off[j+1],off[j]:off[j+1]])*outputs[j] for j in range(L))
   power_err=max(power_err,np.linalg.norm(Y-EY))
  if max(tp,fixed,disturb,power_err)>1e-12:raise AssertionError((L,eps,tp,fixed,disturb,power_err))
  rows.append(dict(L=L,epsilon=eps,dimension=D,tp=tp,fixed=fixed,disturbance_formula_error=disturb,EB_power_identity_error=power_err,minimum_fixed_eigenvalue=float(np.linalg.eigvalsh(sigma)[0]),minimum_prepared_eigenvalue=float(min(np.linalg.eigvalsh(Y)[0] for Y in outputs))))
Path(__file__).with_name('STATIONARY_CHECKS.json').write_text(json.dumps(rows,indent=2)+'\n')
print(json.dumps(rows,indent=2))
