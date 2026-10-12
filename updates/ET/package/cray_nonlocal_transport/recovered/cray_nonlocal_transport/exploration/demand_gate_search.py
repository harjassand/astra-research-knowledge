"""Explore source-demand compatibility, weaker than prescribed path compatibility."""
import json,time
from pathlib import Path
from collections import defaultdict
import numpy as np
from scipy.optimize import milp, Bounds, LinearConstraint
from scipy.sparse import coo_matrix
R=Path(__file__).parent; start=time.perf_counter()
comp=np.load(R/'graph_6x3.npz')['comp']; ncomp=int(comp.max())+1
ofs=[(x,y)for y in range(-1,2)for x in range(-1,2)if(x,y)!=(0,0)]
def rot(v):return sum(((v>>i)&1)<<ofs.index((-y,x))for i,(x,y)in enumerate(ofs))
def ref(v):return sum(((v>>i)&1)<<ofs.index((-x,y))for i,(x,y)in enumerate(ofs))
def orb(v):
 z=set()
 for _ in range(4):z.update([v,ref(v)]);v=rot(v)
 return frozenset(z)
orbits=sorted(set(orb(v)for v in range(256)),key=min);m=len(orbits)
where={v:i for i,o in enumerate(orbits)for v in o}
pair={(i,i):i for i in range(m)}
for i in range(m):
 for j in range(i+1,m):pair[i,j]=len(pair)
k=len(pair)
left=[sum(((a>>i)&1)<<((x+1)+6*(y+1))for i,(x,y)in enumerate(ofs))for a in range(256)]
right=[sum(((a>>i)&1)<<((x+4)+6*(y+1))for i,(x,y)in enumerate(ofs))for a in range(256)]
coef=defaultdict(int)
for a in range(256):
 for b in range(256):
  i,j=sorted((where[a],where[b]));col=pair[i,j]
  s=left[a]|right[b]|(1<<7);t=s^(1<<7)^(1<<10)
  coef[int(comp[s]),col]+=1;coef[int(comp[t]),col]-=1
coef={a:b for a,b in coef.items()if b}
rowmap={r:i for i,r in enumerate(sorted({r for r,c in coef}))}
rows=[rowmap[r]for r,c in coef];cols=[c for r,c in coef];data=list(coef.values())
lo=[0]*len(rowmap);hi=[0]*len(rowmap)
for (i,j),col in pair.items():
 if i==j:continue
 row=len(lo);rows.extend([row,row]);cols.extend([col,i]);data.extend([1,-1]);lo.append(-np.inf);hi.append(0)
 row=len(lo);rows.extend([row,row]);cols.extend([col,j]);data.extend([1,-1]);lo.append(-np.inf);hi.append(0)
 row=len(lo);rows.extend([row,row,row]);cols.extend([col,i,j]);data.extend([-1,1,1]);lo.append(-np.inf);hi.append(1)
A=coo_matrix((data,(rows,cols)),shape=(len(lo),k)).tocsc()
print('orbits',m,'variables',k,'nonzero component constraints',len(rowmap),'totalconstraints',len(lo),flush=True)
out=[]
for p in [.3,.4,.5,.65]:
 c=np.zeros(k)
 for i,o in enumerate(orbits):c[i]=-sum(p**v.bit_count()*(1-p)**(8-v.bit_count())for v in o)
 result=milp(c,integrality=np.r_[np.ones(m),np.zeros(k-m)],bounds=Bounds(0,1),constraints=LinearConstraint(A,lo,hi),options={'time_limit':8})
 if result.x is None:print('no incumbent',p);continue
 gate=sorted(v for i,o in enumerate(orbits)if result.x[i]>.5 for v in o)
 mass=np.zeros(ncomp,dtype=np.int64)
 for a in gate:
  for b in gate:
   s=left[a]|right[b]|(1<<7);t=s^(1<<7)^(1<<10)
   mass[comp[s]]+=1;mass[comp[t]]-=1
 assert np.all(mass==0)
 counts=[sum(v.bit_count()==n for v in gate)for n in range(9)]
 prob=-sum(c[:m]*(result.x[:m]>.5))
 print(p,'prob',prob,'counts',counts,'status',result.message,flush=True)
 out.append({'p':p,'prob':prob,'counts':counts,'allowed':gate,'status':result.message})
(R/'demand_gate_search_results.json').write_text(json.dumps(out,indent=2))
print('wall',time.perf_counter()-start)
