"""Numerical diagnostics of actual jets; not a compatible QC witness."""
import numpy as np
rho=np.sqrt(3)-1
G=np.array([[1+rho/2,rho,-rho],[rho,2,-rho],[-rho,-rho,1+rho]])
def vals(a,P,Q):
 X=a[0]+1j*a[1];Y=a[2]+1j*a[3];R=1
 L7=X*Q+2*Y*P
 q=np.array([np.conj(X)*P+2*np.conj(Y)*Q,Y+X*np.conj(Q)+np.conj(Y)*Q,X*np.conj(Q)+2*np.conj(Y)*Q])
 return rho/2*abs(L7)**2+np.vdot(q,G@q).real,2*q[2].real
# density E/16, min over A. Need stabilization 4nu >= result.
def threshold(h):
 P=h[0]+1j*h[1];Q=h[2]+1j*h[3]
 basis=np.eye(4);K=np.zeros((4,4));b=np.zeros(4)
 for i in range(4):K[i,i],b[i]=vals(basis[i],P,Q)
 for i in range(4):
  for j in range(i):
   tmp=vals(basis[i]+basis[j],P,Q)[0];K[i,j]=K[j,i]=(tmp-K[i,i]-K[j,j])/2
 b=b/2
 try:return b@np.linalg.solve(K,b)
 except np.linalg.LinAlgError:return b@np.linalg.pinv(K)@b
rng=np.random.default_rng(74)
best=(-1,None)
for i in range(3000):
 h=rng.normal(size=4)*10**rng.uniform(-4,3)
 v=threshold(h)
 if v>best[0]:best=(v,h)
print('random best',best,flush=True)
h=best[1].copy();steps=np.array([1.,.3,.1,.03,.01,.003,.001,.0003])*max(1,np.max(np.abs(h)))
for step in steps:
 for it in range(100):
  changed=False
  for j in range(4):
   for sign in [-1,1]:
    hh=h.copy();hh[j]+=sign*step;v=threshold(hh)
    if v>best[0]:best=(v,hh);h=hh;changed=True
  if not changed:break
print('coordinate best',best,'nu',best[0]/4,flush=True)
