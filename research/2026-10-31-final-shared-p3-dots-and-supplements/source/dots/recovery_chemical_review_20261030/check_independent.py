import itertools,json
import numpy as np
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import spsolve
# Independently enumerate transitions by source/product complex arithmetic.
complexes=[(2,0,0),(1,0,1),(0,1,1),(0,0,2)]
edges=[(0,1),(1,0),(1,2),(2,1),(0,3),(3,1)]
def falling(x,k):
 p=1
 for j in range(k):p*=x-j
 return p if x>=k else 0

def prop(x,y):return np.prod([falling(xx,yy) for xx,yy in zip(x,y)])
rows=[]
for n in (2,5,12,24,40):
 states=[(a,c,n-a-c) for a in range(n+1) for c in range(n-a+1) if n-a-c>0]
 idx={x:i for i,x in enumerate(states)}
 L=lil_matrix((len(states),len(states)),dtype=float)
 rhs=np.zeros((len(states),4))
 for x,i in idx.items():
  a,c,d=x;A=a+2;kill=a*(a-1);tot=kill
  rhs[i,2]=kill/(a-1)**2 if kill else 0
  rhs[i,3]=1/((a+2)*(a+1))
  for e,(sy,ty) in enumerate(edges):
   rate=prop(x,complexes[sy])
   if not rate:continue
   z=tuple(xx-yy+zz for xx,yy,zz in zip(x,complexes[sy],complexes[ty]));tot+=rate
   assert min(z)>=0 and sum(z)==n
   if z[2]==0:
    assert e==1 and d==1
    rhs[i,0]+=rate;rhs[i,1]+=rate/(3+z[0])**2;rhs[i,2]+=rate/(3+z[0])**2
   else:L[i,idx[z]]-=rate
  L[i,i]+=tot
 sol=spsolve(L.tocsr(),rhs)
 ff=np.array([(3+x[0])**-2 for x in states]); fg=np.array([(3+x[0])**-3 for x in states]);fm=np.array([(3+x[0])**-4 for x in states])
 rows.append(dict(n=n,states=len(states),max_probability=float(sol[:,0].max()),max_profile_ratio=float((sol[:,2]/ff).max()),max_gain_ratio=float((sol[:,1]/fg).max()),max_time_ratio=float((sol[:,3]/fm).max()),max_residual=float(np.max(abs(L@sol-rhs)))))
# Exact rank over rationals and independent graph reachability.
import sympy as sp
for a0,q in [(2,5),(3,7),(7,12)]:
 m=a0+2
 full=[(m,0,0,q),(a0+1,0,1,q),(a0,1,1,q),(a0,0,2,q),(0,0,0,0),(1,0,0,1)]
 ee=edges+[(4,5),(5,0),(0,4)]
 mat=sp.Matrix([[full[t][j]-full[s][j] for s,t in ee] for j in range(4)])
 assert mat.rank()==4
 for s in range(6):
  reach={s}
  for _ in range(6):reach|={t for u,t in ee if u in reach}
  assert len(reach)==6
json.dump({'independent_shells':rows,'exact_rank_cases':3,'all_active_dormant_entrances_verified':'reaction2 at d1','scope':'finite diagnostics only'},open('recovery_chemical_review_20261030/check_independent.json','w'),indent=2)
print(json.dumps(rows,indent=2))
