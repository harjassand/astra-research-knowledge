import numpy as np,itertools,json
from piecewise_texture import bary_value
from numpy.polynomial.legendre import leggauss
D='producer-workspace/chiral_hamiltonian_interface_20261102'
z=np.load(D+'cubic_move.npz',allow_pickle=True);T=[(tuple(t),int(s)) for t,s in z['T']]
def quadrature(N):
 a,w=leggauss(N);a=(a+1)/2;w=w/2;points=[];weights=[]
 for i,j,k in itertools.product(range(N),repeat=3):
  u,v,q=a[i],a[j],a[k];points.append([1-u,u*(1-v),u*v*(1-q),u*v*q]);weights.append(w[i]*w[j]*w[k]*u*u*v)
 return np.array(points),np.array(weights)
for nq in [4,8,12]:
 bary,weights=quadrature(nq)
 for label,phi in [('a',z['phi_a']),('b',z['phi_b'])]:
  total=0;nonzero=0
  for t,s in T:
   for p in itertools.permutations(range(4)):
    sign=s*(-1)**sum(p[i]>p[j] for i in range(4) for j in range(i+1,4))
    qs=[bary_value(phi,[t[p[j]] for j in range(k)]) for k in range(1,5)]
    Q=np.array([[q[0].real,q[0].imag,q[1].real,q[1].imag] for q in qs]);det=np.linalg.det(Q)
    if abs(det)<1e-15:continue
    nonzero+=1;norm2=np.sum((bary@Q)**2,axis=1);total+=sign*det*np.dot(weights,norm2**-2)/(2*np.pi**2)
  print('quad',nq,'endpoint',label,'degree',total,'nonzero sub-tets',nonzero,flush=True)
