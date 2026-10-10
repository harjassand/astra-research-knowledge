import numpy as np,json
from fractions import Fraction
from pathlib import Path
folder=Path(__file__).parent
# Internal H: blocks A=0..3, B=4..6, C=7..10, D=11..14,
# plus source u=15. Four cyclic blocks A -> B -> C -> D -> A;
# A has the directed 4-cycle internally; u -> A.
b=16;a=4
H=np.zeros((b,b),dtype=np.int64)
blocks=[range(0,4),range(4,7),range(7,11),range(11,15)]
for i in range(4):
 for u in blocks[i]:
  for v in blocks[(i+1)%4]:H[u,v]=1
for u in range(4):H[u,(u+1)%4]=1
H[15,range(4)]=1
# Outer directed 4-cycle, each vertex substituted by H,
# complete arcs between each copy and next copy.
A=np.kron(np.eye(4,dtype=np.int64),H)
for i in range(4):A[i*b:(i+1)*b,((i+1)%4)*b:((i+1)%4)*b+b]=1
n=len(A);r=int(A[0].sum());M=A.T.astype(float)/r-np.eye(n);M[-1]=1;rhs=np.zeros(n);rhs[-1]=1;p=np.linalg.solve(M,rhs)
B=(A@A>0)&(A==0);np.fill_diagonal(B,False);s=B.sum(1)
print('n,r',n,r,'dout',set(A.sum(1)),'digons',int(np.sum(A*A.T)),'triangles',int(np.trace(A@A@A)),'min pi',min(p),'stationarity residual',np.max(np.abs(p@A-r*p)))
print('Epi s',p@s,'ratio',p@s/r,'gap',p@s-r)
print('block1 p',p[:b]);print('s',s[:b]);print('H second',(((H@H)>0)&(H==0)).sum(1))
import sympy as sp
Mh=sp.eye(b)-sp.Matrix(H.T)/r
rho=Mh.inv()*sp.ones(b,1)/r # uniform injection b/r over b states =1/r
assert sum(rho)==1
exact=sum(rho[i]*int(s[i]) for i in range(b));print('exact',exact,'gap',exact-r)
record={'n':n,'r':r,'A':A.tolist(),'s':s.tolist(),'pi_exact':[str(rho[i%b]/4) for i in range(n)],'weighted_second_exact':str(exact),'gap_exact':str(exact-r),'construction':'Four copies of H, complete arcs to next copy in a directed 4-cycle. H is A4 -> B3 -> C4 -> D4 -> A4 plus internal directed C4 on A4 and source u -> A4.'}
json.dump(record,open(folder/'stationary_counterexample_n64_r20.json','w'),indent=2)
