import numpy as np
from scipy.optimize import milp, Bounds, LinearConstraint
from scipy.sparse import coo_matrix
import json,time
from pathlib import Path
from gadget_explore import graph
ROOT=Path(__file__).parent
start=time.perf_counter()
sites,ix,nxt,comp,cs=graph(6,3)
np.savez_compressed(ROOT/'graph_6x3.npz',comp=np.array([comp[s] for s in range(1<<18)],dtype=np.int32))
# offsets relative to port at(1,1)
off=[(x,y) for y in range(-1,2) for x in range(-1,2) if (x,y)!=(0,0)]
def rotate(v):
 return sum(((v>>i)&1)<<off.index((-y,x)) for i,(x,y) in enumerate(off))
def reflect(v):
 return sum(((v>>i)&1)<<off.index((-x,y)) for i,(x,y) in enumerate(off))
def orbit(v):
 s=set()
 for k in range(4):s.update([v,reflect(v)]);v=rotate(v)
 return frozenset(s)
orbits=sorted(set(orbit(v) for v in range(256)),key=lambda o:min(o))
left=[ix[(x+1,y+1)] for x,y in off];right=[ix[(x+4,y+1)] for x,y in off]
leftnum=[sum(((v>>j)&1)<<i for j,i in enumerate(left)) for v in range(256)]
rightnum=[sum(((v>>j)&1)<<i for j,i in enumerate(right)) for v in range(256)]
compat=np.ones((256,256),bool)
for a in range(256):
 for b in range(256):
  s=leftnum[a]|rightnum[b]|(1<<ix[(1,1)])
  t=s^(1<<ix[(1,1)])^(1<<ix[(4,1)])
  compat[a,b]=comp[s]==comp[t]
rows=[];cols=[];data=[];ub=[]
for i,a in enumerate(orbits):
 for j,b in enumerate(orbits[i:],start=i):
  if any(not compat[x,y] or not compat[y,x] for x in a for y in b):
   row=len(ub);rows.append(row);cols.append(i);data.append(1)
   if i!=j: rows.append(row);cols.append(j);data.append(1)
   ub.append(0 if i==j else 1)
mat=coo_matrix((data,(rows,cols)),shape=(len(ub),len(orbits))).tocsc()
resout={'orbits':len(orbits),'constraints':len(ub),'densities':[]}
for p in [.1,.2,.25,.3,.35,.4,.45,.5,.6]:
 weights=np.array([sum(p**v.bit_count()*(1-p)**(8-v.bit_count()) for v in o) for o in orbits])
 res=milp(-weights,integrality=np.ones(len(orbits)),bounds=Bounds(0,1),constraints=LinearConstraint(mat,-np.inf,np.array(ub)),options={'time_limit':5})
 allowed=sorted(v for x,o in zip(res.x,orbits) if x>.5 for v in o)
 prob=sum(p**v.bit_count()*(1-p)**(8-v.bit_count()) for v in allowed)
 counts={k:sum(v.bit_count()==k for v in allowed) for k in range(9)}
 out={'p':p,'good_probability':prob,'bad_probability':1-prob,'counts':counts,'allowed':allowed,'optimal':res.success}
 resout['densities'].append(out)
 print(p,prob,'bad',1-prob,'counts',counts,'optimal',res.success,flush=True)
resout['wall_seconds']=time.perf_counter()-start
(ROOT/'gate_search_results.json').write_text(json.dumps(resout,indent=2))
print('wall',resout['wall_seconds'])
