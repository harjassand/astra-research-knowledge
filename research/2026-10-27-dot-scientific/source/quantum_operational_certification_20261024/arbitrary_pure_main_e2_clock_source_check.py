"""Actual arbitrary pure main/source F and elementary-symmetric scalar clock."""
import numpy as np
from scipy.integrate import quad
exec(open('gls_common_clock_accepted_entropy_check.py').read().split('rng=')[0])
def FF(e):
 e=np.asarray(e);tt=sum(e)
 return 2*sum(np.log1p((tt-e)/2))-3*sum(np.log1p(e/3))-np.log1p(tt)
rng=np.random.default_rng(262322)
for n,rankmain,rankreset in [(3,3,3),(4,3,4),(6,3,4),(4,2,3),(5,1,4)]:
 P=.3*(rng.normal(size=(n,rankmain))+1j*rng.normal(size=(n,rankmain)))
 Psi=np.hstack([P,np.zeros((n,3-rankmain))]);B=.4*(rng.normal(size=(n,rankreset))+1j*rng.normal(size=(n,rankreset)));Y=B@B.conj().T
 om=Psi.T.reshape(-1);X=np.outer(om,om.conj())+np.kron(np.eye(3),Y);actual=dd(X,n)
 def vals(s):
  K=Psi.conj().T@np.linalg.solve(Y+s*np.eye(n),Psi);eig=np.maximum(np.linalg.eigvalsh(K),0)
  e2=(eig[0]*eig[1]+eig[0]*eig[2]+eig[1]*eig[2]);r=np.sqrt(e2/3)
  orig=FF(eig);bal=FF([r]*3)
  assert orig>=bal-1e-9
  return orig,bal
 direct=quad(lambda s:vals(s)[0],0,np.inf,epsabs=3e-9)[0]
 balanced=quad(lambda s:vals(s)[1],0,np.inf,epsabs=3e-9)[0]
 assert abs(actual-direct)<5e-8,(actual,direct)
 assert balanced>=-1e-8
 if rankmain==3:
  for z in [.1+.2j,-.3+.1j,-3+.4j]:
   HH=z*Psi.conj().T@np.linalg.solve(Y+z*np.eye(n),Psi)
   ee=np.linalg.eigvals(HH);g=np.exp((sum(np.log(ee))+np.log(np.trace(np.linalg.inv(HH)))-np.log(3))/2)
   e2=(np.trace(HH)**2-np.trace(HH@HH))/2
   assert abs(g*g-e2/3)<2e-10 and g.imag>=-1e-10
 print('PASS original arbitrary-main/reference F integral and e2 balance',n,rankmain,rankreset,actual,balanced)
print('No numerical result substitutes for scalar-measure branch/source-limit proof')
