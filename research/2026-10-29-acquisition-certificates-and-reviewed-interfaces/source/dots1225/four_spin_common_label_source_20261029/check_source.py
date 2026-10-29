"""Exact signed-permutation moment; floating common-source Gram/protected-sector checks."""
import itertools,numpy as np,json
from pathlib import Path
I=np.eye(2);pa=[np.array([[0,1],[1,0]],complex),np.array([[0,-1j],[1j,0]]),np.diag([1,-1])]
rots=[]
for perm in itertools.permutations(range(3)):
 for signs in itertools.product([-1,1],repeat=3):
  R=np.zeros((3,3),int)
  for a,b in enumerate(perm):R[a,b]=signs[a]
  if round(np.linalg.det(R))==1:rots.append(R)
assert len(rots)==24
moment=sum(np.einsum('ca,db->cadb',R,R) for R in rots)
assert np.array_equal(moment,8*np.einsum('cd,ab->cadb',np.eye(3,dtype=int),np.eye(3,dtype=int)))
H=1j*np.array([[1,1],[1,-1]],complex)/np.sqrt(2);S=np.diag([np.exp(-1j*np.pi/4),np.exp(1j*np.pi/4)])
def rot(U):return np.array([[round(np.trace(a@U@b@U.conj().T).real/2) for b in pa] for a in pa])
lifts={tuple(rot(I).ravel()):I};todo=[I]
while todo:
 U=todo.pop()
 for gen in [H,S]:
  V=gen@U;k=tuple(rot(V).ravel())
  if k not in lifts:lifts[k]=V;todo.append(V)
assert len(lifts)==24 and set(lifts)==set(tuple(r.ravel()) for r in rots)
def kron(xs):
 out=np.ones((1,1),complex)
 for x in xs:out=np.kron(out,x)
 return out
Vs=[I]+[.6*I-.8j*pa[j] for j in range(3)];W=kron(Vs);R=[np.array([[np.trace(a@v@b@v.conj().T).real/2 for b in pa] for a in pa]) for v in Vs];units=[W@kron([u]*4)@W.conj().T for u in lifts.values()]
rows=[]
for j in [1,2,3]:
 P=[]
 for a,b in itertools.product(range(3),repeat=2):
  factors=[I]*4;factors[j]=pa[a];factors[0]=pa[b];P.append(kron(factors))
 comm=np.vstack([np.column_stack([(u@p-p@u).ravel() for p in P]) for u in units]);Hgram=comm.conj().T@comm/(24*32)
 c=(R[j]@R[0].T).ravel()/np.sqrt(3);err=np.linalg.norm(Hgram-(np.eye(9)-np.outer(c,c)));assert err<1e-12;rows.append(dict(edge=j,gram_residual=float(err)))
# Singlet-sector projector from collective total-spin quadratic Casimir.
J=[]
for a in pa:J.append(sum(kron([a if k==j else I for k in range(4)]) for j in range(4))/2)
Casimir=sum(x@x for x in J);vals,V=np.linalg.eigh(Casimir);E=V[:,abs(vals)<1e-10];assert E.shape==(16,2)
EW=W@E;res=max(np.linalg.norm(u@EW-EW) for u in units);assert res<1e-12
out=dict(exact_group_size=24,exact_integer_second_moment=True,star_gram_checks=rows,protected_dimension=2,common_source_protection_residual=float(res),scope='Ideal finite common4spin source construction; Gram and protected-subspace matrices checked numerically, second moment exactly in integers; no native hardware.')
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
