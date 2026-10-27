"""Independent actual-source vs shared-resolvent integral check, including nonflat sigma."""
import numpy as np
from scipy.integrate import quad
rng=np.random.default_rng(261026128)
def f(a):
 e=np.linalg.eigvalsh((a+a.conj().T)/2);assert e.min()>-1e-10
 e=e[e>1e-14];return np.dot(e,np.log(e))
maxerror=0.;count=0;minlinear=1.
for k in [1,2,3,5]:
 for rep in range(6):
  sig=rng.dirichlet(np.full(k,.4))
  if k==2 and rep==0:sig=np.array([.999,.001])
  p=[.15,.5,.85][rep%3];q=1-p;b=q/p;theta=[.1,.7,1.][rep%3]
  G=rng.normal(size=(3,k))+1j*rng.normal(size=(3,k));G*=np.sqrt(theta)/np.linalg.norm(G)
  n=3*k+1;flag=np.r_[G.reshape(-1),np.sqrt(1-theta)]
  A=np.zeros((3*n,3*n),complex)
  for j in range(k):
   v=np.zeros((3,n),complex)
   for i in range(3):v[i,k*i+j]=1/np.sqrt(3)
   v=v.reshape(-1);A+=p*sig[j]*np.outer(v,v.conj())
  A+=q*np.kron(np.eye(3),np.outer(flag,flag.conj()))/3
  ar=A.reshape(3,n,3,n);R=np.einsum('aiaj->ij',ar);L=np.kron(np.eye(3),R)-ar.transpose(2,1,0,3).reshape(3*n,3*n)
  delta=f(A)+f(R)-f(L)+np.log(4/3)
  def integrand(t):
   K=(G*(sig/(t+sig)))@G.conj().T;es=np.maximum(np.linalg.eigvalsh(K),0);T=es.sum();z=t/b
   alpha=1/(2*(z+1));beta=1/(3*(3*z+1));gamma=3/(z+3)
   F=2*np.log1p(-alpha*(T-es)).sum()-3*np.log1p(-beta*es).sum()-np.log1p(-gamma*T)
   h=4*z*(z-1)/((z+3)*(3*z+1)*(z+1))
   assert F-h*T>=-1e-12
   return F
  integral=p*quad(integrand,0,np.inf,epsabs=2e-10,epsrel=2e-9,limit=300)[0]/3
  def linear(t):
   z=t/b;h=4*z*(z-1)/((z+3)*(3*z+1)*(z+1))
   return h*np.sum(np.sum(abs(G)**2,axis=0)*sig/(t+sig))
  lin=quad(linear,0,np.inf,epsabs=1e-11,limit=300)[0]
  assert lin>0;minlinear=min(minlinear,lin)
  error=abs(delta-integral);maxerror=max(maxerror,error);assert error<1e-7
  count+=1
print({'status':'PASS','actual_sources':count,'max_entropy_integral_discrepancy':maxerror,'minimum_linear_integral':minlinear})
