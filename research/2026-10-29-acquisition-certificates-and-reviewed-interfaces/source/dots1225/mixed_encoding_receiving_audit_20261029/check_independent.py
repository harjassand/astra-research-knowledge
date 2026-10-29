import itertools, math, json
import numpy as np
from fractions import Fraction as F
from pathlib import Path
out=[]
for r in (1,2,3):
 m=2*r; n=m-1; strings=list(itertools.product(range(r),repeat=m)); mats=[]; labels=[]
 # Build directly from permutations of distinct logical-junk basis labels,
 # rather than enumerate bit strings and test determinants.
 table={a:np.zeros((2**n,2),dtype=np.int64) for a in strings}
 for perm in itertools.permutations(range(m)):
  a=tuple(z%r for z in perm); bits=[z//r for z in perm]
  inversions=sum(perm[i]>perm[j] for i in range(m) for j in range(i+1,m))
  row=sum((1-bits[j]) << (n-1-j) for j in range(n))
  table[a][row,bits[-1]]+=(-1)**(inversions+sum(1-b for b in bits[:-1]))
 for a,M in table.items():
  if np.any(M):mats.append(M);labels.append(a)
 X=np.array([[0,1],[1,0]],dtype=np.int64); Z=np.diag([1,-1]); SX=np.zeros((2**n,2**n),dtype=np.int64);SZ=SX.copy()
 for j in range(n):
  for op,acc in ((X,SX),(Z,SZ)):
   term=np.array([[1]],dtype=np.int64)
   for k in range(n):term=np.kron(term,op if j==k else np.eye(2,dtype=np.int64))
   acc+=term
 for M in mats:assert np.array_equal(SX@M,M@X) and np.array_equal(SZ@M,M@Z)
 for A in mats:
  for B in mats:
   G=A.T@B; assert np.array_equal(G,G[0,0]*np.eye(2,dtype=np.int64))
 probs=[F(j+1,r*(r+1)//2) for j in range(r)]
 effect=sum(F(int((M.T@M)[0,0]),2**n*math.factorial(m))*math.prod(probs[j] for j in a) for a,M in zip(labels,mats))
 target=math.prod(probs)**2/2**m;assert effect==target
 # Coherent correlated junk superpositions, not diagonal mixtures.
 for seed in range(7):
  C=sum((1j**((j+seed)%4))*(j%3+1)*M for j,M in enumerate(mats))
  G=C.conj().T@C;assert np.array_equal(G,G[0,0]*np.eye(2))
 out.append(dict(r=r,nonzero=len(mats),exact_cross_gram_checks=len(mats)**2,nonuniform_success=str(effect),coherent_correlated_junk_checks=7))
# Exact full Weyl twirl on every matrix unit, avoiding roots of unity:
# phase averaging kills offdiagonal; shifts spread any surviving diagonal uniformly.
count=0
for k in range(2,8):
 for a,b in itertools.product(range(k),repeat=2):
  result=[[F(0) for _ in range(k)] for _ in range(k)]
  if a==b:
   for shift in range(k):result[(a+shift)%k][(a+shift)%k]+=F(1,k)
  expected=[[F(int(a==b and i==j),k) for j in range(k)] for i in range(k)]
  assert result==expected;count+=1
res=dict(exterior=out,exact_Weyl_matrix_units=count,scope='Exact integer intertwining/cross-Gram and rational IID normalization; coherent junk diagnostics; no hardware or general adaptive protocol simulation')
Path(__file__).with_suffix('.json').write_text(json.dumps(res,indent=2)+'\n'); print(json.dumps(res,indent=2))
