import numpy as np
from itertools import product
for m in range(1,9):
 eps=1/m**2;n=m+2;err=0.;egap=1e9;energyerr=0.
 for bits in product((0,1),repeat=m):
  alpha=1.;gamma=np.zeros(m);A=eps*np.eye(m);beta=np.zeros(m)
  for i,bit in enumerate(bits):
   A[i]-=eps*gamma;beta[i]=eps*alpha
   if bit==0:alpha=0.;gamma=np.eye(m)[i]
   else:gamma-=np.eye(m)[i]
  B=np.zeros((n,n));B[0,0]=B[-1,-1]=eps;B[1:-1,1:-1]=A;B[1:-1,0]=-beta;B[-1,0]=-eps*alpha;B[-1,1:-1]=-eps*gamma
  delta=eps/(4*(m+1)**2);egap=min(egap,np.linalg.eigvalsh((B+B.T)/2)[0]/delta)
  rng=np.random.default_rng(m+sum((i+1)*q for i,q in enumerate(bits)));u=rng.random(m)
  M=B+np.diag(np.r_[0,u,0]);src=np.eye(n)[0]*eps
  f=np.linalg.solve(M,src)[-1];exact=np.prod([u[i]/(eps+u[i]) if bit else eps/(eps+u[i]) for i,bit in enumerate(bits)]);err=max(err,abs(f-exact))
  vec=rng.normal(size=n);y=vec[0];dd=[]
  for i,bit in enumerate(bits):
   yy=vec[i+1] if bit==0 else y-vec[i+1];dd.append(y-yy);y=yy
  en=eps/2*(vec[0]**2+vec[-1]**2+(y-vec[-1])**2+np.dot(dd,dd));energyerr=max(energyerr,abs(vec@B@vec-en))
 print(m,egap,err,energyerr)
