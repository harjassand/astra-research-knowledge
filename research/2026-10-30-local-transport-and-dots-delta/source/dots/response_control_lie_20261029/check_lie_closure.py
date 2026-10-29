"""Exact finite-field lower-bound certificates for real Gaussian-integer Lie closures.
Analytical upper bounds are supplied by the accompanying proof. No floating rank test.
"""
import numpy as np, json,hashlib
from pathlib import Path
p=1009
I=np.eye(2,dtype=complex); X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]],complex);Z=np.diag([1,-1]).astype(complex);P=[I,X,Y,Z]
def anc(q):return P[1:] if q==2 else [np.kron(a,b) for i,a in enumerate(P) for j,b in enumerate(P) if i or j]
def pair(A):return (np.rint(A.real).astype(np.int64)%p,np.rint(A.imag).astype(np.int64)%p)
def flat(A):return np.concatenate([A[0].ravel(),A[1].ravel()])
def unflat(v,n):return v[:n*n].reshape(n,n),v[n*n:].reshape(n,n)
def bracket(A,B):
 ar,ai=A;br,bi=B
 return ((ar@br-ai@bi-br@ar+bi@ai)%p,(ar@bi+ai@br-br@ai-bi@ar)%p)
def closure(q,responses,expected):
 n=q*len(responses[0]);seeds=[pair(1j*np.kron(h,a)) for h in anc(q) for a in responses]
 rows=[];piv=[];mats=[];tested=0
 def insert(A):
  v=flat(A).copy()%p
  for row,k in zip(rows,piv):
   c=int(v[k])
   if c:v=(v-c*row)%p
  nz=np.flatnonzero(v)
  if not len(nz):return
  k=int(nz[0]);v=(v*pow(int(v[k]),-1,p))%p
  rows.append(v);piv.append(k);mats.append(unflat(v,n))
 for A in seeds:insert(A)
 cursor=0
 while cursor<len(mats):
  A=mats[cursor];cursor+=1
  for B in seeds:insert(bracket(A,B));tested+=1
 assert len(rows)==expected,(q,n,len(rows),expected)
 # Jacobi implies stability under all original generators suffices for Lie closure.
 return dict(ancilla=q,carrier=n//q,dimension=len(rows),expected=expected,prime=p,seed_count=len(seeds),generator_brackets_tested=tested,pivots_sha256=hashlib.sha256(json.dumps(piv).encode()).hexdigest(),exact_modular_lower_bound=True)
def block(A,B):
 z=np.zeros((len(A)+len(B),len(A)+len(B)),complex);z[:len(A),:len(A)]=A;z[len(A):,len(A):]=B;return z
rows=[]
cases=[('two_level_accessor_obstruction',2,[I,X,Z],10),('full_M2_four_level_accessor',4,[I,X,Z],63),('three_distinct_scalar_blocks',4,[np.eye(3),np.diag([0,1,2])],45),('scalar_plus_M2_independent_blocks',4,[np.eye(3),block(np.zeros((1,1)),X),block(np.zeros((1,1)),Z)],78),('equivalent_M2_multiplicity_two',4,[np.eye(4),np.kron(X,I),np.kron(Z,I)],63),('inequivalent_two_M2_blocks',4,[np.eye(4),block(X,2*X),block(Z,2*Z)],126)]
for name,q,res,e in cases:
 r=closure(q,res,e);r['name']=name;rows.append(r);print(name,r['dimension'],flush=True)
out={'scope':'Exact modular lower bounds on real Lie dimensions; matching upper bounds from algebraic theorem. No compiled controls or time/gap estimate.','cases':rows}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
