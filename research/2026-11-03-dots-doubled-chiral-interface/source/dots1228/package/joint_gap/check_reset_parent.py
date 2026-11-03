"""Finite verification of collective reset parent; NOT free-slab interface proof."""
import numpy as np, json
from scipy.linalg import eigh
m=4;dim=2**m
c=[]
for j in range(m):
 a=np.zeros((dim,dim),complex)
 for n in range(dim):
  if (n>>j)&1: a[n^(1<<j),n]=(-1)**((n&((1<<j)-1)).bit_count())
 c.append(a)
N=sum(a.conj().T@a for a in c)
matchings=[[(0,1,1),(2,3,1)],[(0,2,1),(1,3,-1)],[(0,3,-1),(1,2,1)],[(0,1,-1),(2,3,-1)]]
Qs=[]
for pairs in matchings:
 A=np.zeros((m,m))
 for j,k,s in pairs:A[j,k]=s;A[k,j]=-s
 Q=sum(1j*A[j,k]*c[j].conj().T@c[k] for j in range(m) for k in range(m))
 Qs.append(Q)
Q=np.zeros((4*dim,4*dim),complex)
for x,q in enumerate(Qs):Q[x*dim:(x+1)*dim,x*dim:(x+1)*dim]=q
P=np.ones((2,2))/2
B=[np.kron(np.eye(4)-np.kron(P,np.eye(2)),np.eye(dim)),np.kron(np.eye(4)-np.kron(np.eye(2),P),np.eye(dim))]
e,V=eigh(Q); mask=np.abs(e[:,None]-e[None,:])<1e-8
rot=[V@((V.conj().T@b@V)*mask)@V.conj().T for b in B]
H=2*np.kron(np.eye(4),N)+sum(rot)
energies=eigh(H,eigvals_only=True)
psi=np.kron(np.ones(4)/2,np.eye(dim)[:,0])
out=dict(dimension=4*dim,ground_energy=float(energies[0]),gap=float(energies[1]-energies[0]),ground_multiplicity=int(np.count_nonzero(abs(energies)<1e-9)),symmetry_commutator=float(np.linalg.norm(H@Q-Q@H)),vacuum_residual=float(np.linalg.norm(H@psi)),number_commutator=float(np.linalg.norm(H@np.kron(np.eye(4),N)-np.kron(np.eye(4),N)@H)),scope='Finite check of shared-rotor conjugate-fiber model, not the free-slab interface')
assert out['ground_multiplicity']==1 and abs(out['gap']-1)<1e-8
assert max(out['symmetry_commutator'],out['vacuum_residual'],out['number_commutator'])<1e-8
open('producer-workspace/check_results.json','w').write(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
