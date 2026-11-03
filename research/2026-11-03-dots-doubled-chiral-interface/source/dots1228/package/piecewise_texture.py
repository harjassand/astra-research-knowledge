"""Explicit periodic, globally-U(1)-covariant barycentric SU(2) texture.
Rotor phases are in turns. Vertex subsets use the global branching order.
No continuous choice is asserted across rounded-edge walls.
"""
import numpy as np,itertools
TWOPI=2*np.pi
def short(x):return x-np.floor(x+.5)
def vortex(phi,face):
 a,b,c=sorted(face)
 return int(np.floor(phi[c]-phi[b]+.5)-np.floor(phi[c]-phi[a]+.5)+np.floor(phi[b]-phi[a]+.5))
def bary_value(phi,subset):
 s=tuple(sorted(subset));k=len(s);a=s[0]
 if k<=2:
  angle=phi[a]+sum(short(phi[v]-phi[a]) for v in s)/k
  return np.array([np.exp(1j*TWOPI*angle),0j])
 pierced=[f for f in itertools.combinations(s,3) if vortex(phi,f)]
 if not pierced:
  angle=phi[a]+sum(short(phi[v]-phi[a]) for v in s)/k
  return np.array([np.exp(1j*TWOPI*angle),0j])
 if k==3:return np.array([0j,np.exp(1j*TWOPI*phi[a])])
 assert len(pierced)==2
 a,b=[f[0] for f in pierced];angle=phi[a]+short(phi[b]-phi[a])/2
 return np.array([0j,np.exp(1j*TWOPI*angle)])
def evaluate(phi,tetra,bary,normalize=True):
 order=np.argsort(-np.asarray(bary));lam=np.asarray(bary)[order]
 mu=np.arange(1,5)*(lam-np.r_[lam[1:],0])
 q=sum(mu[k-1]*bary_value(phi,[tetra[order[j]] for j in range(k)]) for k in range(1,5))
 return q/np.linalg.norm(q) if normalize else q

def matrix(q):
 z,w=q
 return np.array([[z,w],[-w.conjugate(),z.conjugate()]])
if __name__=='__main__':
 rng=np.random.default_rng(81);minimum=1;cov=0;periodic=0
 for _ in range(50000):
  p=rng.random(4);l=rng.dirichlet(np.ones(4));q=evaluate(p,range(4),l,False);minimum=min(minimum,np.linalg.norm(q))
  alpha=rng.random();cov=max(cov,np.linalg.norm(evaluate(p+alpha,range(4),l)-np.exp(1j*TWOPI*alpha)*q/np.linalg.norm(q)))
  shifts=rng.integers(-3,4,4);periodic=max(periodic,np.linalg.norm(evaluate(p+shifts,range(4),l)-q/np.linalg.norm(q)))
 print('sample minimum raw norm',minimum,'conservative analytic bound',np.cos(3*np.pi/8)/np.sqrt(2),'max covariance error',cov,'max periodicity error',periodic)
