import numpy as np
from math import exp
rng=np.random.default_rng(13827);cases=0
for n in [4,6]:
 for p in [.01,.1,.7,1.]:
  V=np.eye(n)[:,:3];P=V@V.T;v=V.T.reshape(-1)/np.sqrt(3);phi=np.outer(v,v);q=1-p
  for amp in [.001,.01,.05]:
   z=rng.normal(size=n)+1j*rng.normal(size=n);z[:3]*=amp;z/=np.linalg.norm(z);tau=np.outer(z,z.conj());J=p*phi+q*np.kron(np.eye(3)/3,tau);om=np.kron(np.eye(3)/3,p*P/3+q*tau);T=(J+3*om)/4;H=4*T-6*om;ev,U=np.linalg.eigh(H);chi=U[:,-1];E=np.outer(chi,chi.conj());I=np.eye(3*n)
   w=max(np.trace(E@T).real,np.trace(E@om).real)
   if w>p:continue
   def adj(s,a,X):
    c=np.cos(a);t=np.sin(a)
    return c*c*X+t*t*np.trace(s@X)*I-1j*c*t*(s@X-X@s)
   for delta in [-1.,-.2,-.01,1e-4,.02,.3,1.]:
    actual=adj(T,4*delta,adj(om,-6*delta,E));upper=(1+800*delta**2)*E+800*delta**2*p*I
    assert np.linalg.eigvalsh(upper-actual)[0]>-1e-11;cases+=1
for xi in [.0001,.1,.5]:
 for L in [1,2,10,100]:
  for p in [.0001,.1,1.]:
   a=exp(xi/(80*L));b=p*(a-1);eta=(xi/(100*L))**2;beta=eta+xi/(256*L)
   for r0 in [0.,.0001,.1,1.]:
    m=1.;r=r0
    for k in range(L):r,m=a*r+b*m,r+beta*m
    assert m<=3*r0+5*b+beta**L+1e-12
print('PASS',cases,'signed-pair operator cases and144 conservative positive recurrences')
