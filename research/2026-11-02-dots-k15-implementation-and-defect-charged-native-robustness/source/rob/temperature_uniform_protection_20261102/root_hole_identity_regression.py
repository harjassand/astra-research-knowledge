"""Finite matrix regression of the hole identity, not a phase/memory theorem."""
import itertools,json
from pathlib import Path
import numpy as np
from scipy.linalg import expm
I=np.eye(2);X=np.array([[0.,1.],[1.,0.]]);Z=np.diag([1.,-1.])
def tensor(xs):
 r=np.array([[1.]])
 for x in xs:r=np.kron(r,x)
 return r
ident=np.eye(8)
S=[tensor([Z,Z,I]),tensor([I,Z,Z])]
Vbasis=[tensor([X,I,I]),tensor([I,I,X]),tensor([I,X,I])]
C=[{0},{1},{0,1}]
def subsets(A):
 A=sorted(A)
 for bits in range(1<<len(A)):yield {a for i,a in enumerate(A) if bits>>i&1}
def components(A):
 left=set(A);out=[]
 while left:
  comp={left.pop()}
  while True:
   new={b for b in left if any(C[a]&C[b] for a in comp)}
   if not new:break
   comp|=new;left-=new
  out.append(comp)
 return out
def pinch(O):
 for s in S:O=(O+s@O@s)/2
 return O
rows=[]
for B in [1.,10.,50.]:
 for beta_v in [.01,.1,.3]:
  beta=1.;J=B/2;v=beta_v
  Hs=[J*(ident-s) for s in S];H0=sum(Hs)
  Vs=[v*x for x in Vbasis]
  exact=float(np.trace(expm(-(H0+sum(Vs)))))
  reconstructed=0.;raw_reconstructed=0.;max_norm_ratio=0.;max_hole_ratio=0.
  cache={}
  for A in subsets(set(range(3))):
   if not A:continue
   CA=set.union(*(C[a] for a in A));HC=sum(Hs[a] for a in CA)
   O=sum(((-1)**(len(A)-len(Bs)))*expm(-(HC+sum((Vs[b] for b in Bs),np.zeros((8,8))))) for Bs in subsets(A))
   cap=np.expm1(v)**len(A)
   max_norm_ratio=max(max_norm_ratio,float(np.linalg.norm(O,2))/cap)
   Zout=float(np.trace(expm(-(H0-HC))));Z0=float(np.trace(expm(-H0)))
   max_hole_ratio=max(max_hole_ratio,Zout/Z0/(2**len(CA)))
   cache[frozenset(A)]=(O,pinch(O))
  for A in subsets(set(range(3))):
   union=set().union(*(C[a] for a in A));Hout=sum((Hs[a] for a in range(2) if a not in union),np.zeros((8,8)))
   raw=expm(-Hout);pin=raw.copy()
   for comp in components(A):
    o,p=cache[frozenset(comp)];raw=raw@o;pin=pin@p
   raw_reconstructed+=float(np.trace(raw));reconstructed+=float(np.trace(pin))
  err=max(abs(exact-reconstructed),abs(exact-raw_reconstructed))
  assert err<2e-11,(B,v,err)
  assert max_norm_ratio<1+1e-7,(B,v,max_norm_ratio)
  assert max_hole_ratio<=1+1e-12
  rows.append(dict(B=B,beta_v=beta_v,exact_Z=exact,reconstructed_Z=reconstructed,error=err,max_operator_norm_fraction=max_norm_ratio,max_hole_capacity_fraction=max_hole_ratio))
result=dict(status='pass',cases=len(rows),scope='three-qubit commuting-reference hole/source exact identity only',rows=rows)
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
