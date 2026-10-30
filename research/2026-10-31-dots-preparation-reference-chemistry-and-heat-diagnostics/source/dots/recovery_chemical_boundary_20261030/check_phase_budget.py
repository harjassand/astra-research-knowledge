from collections import deque
from pathlib import Path
import json

def H(b,m,q):
 if b==0:return 0
 j,v=divmod(b-1,q-1);return j*(m-1)+v+1

def check(m,q):
 # State is B, integer residual change, rare degree, whether initial phase left.
 start=(q,0,0,False);seen={start};todo=deque([(start,[])])
 while todo:
  (b,r,cost,left),path=todo.popleft()
  if r>0 and (b>=q or (left and b==q)):
   return dict(m=m,q=q,pass_check=False,path=path,state=[b,r,cost,left])
  if left and b==q:continue
  edges=[]
  if b<q:
   edges.append(('I0' if b==0 else 'L',b+1,1,0 if b==0 else 1))
  # High immigration has degree m and cannot enter a cost<m witness.
  if b>0:edges.append(('H' if b>=q else 'Tlow',b+q-1,m-1,m-1 if b>=q else 0))
  if b>=q:edges.append(('clear',b-q,-m,0))
  for label,bb,da,dc in edges:
   cc=cost+dc
   if cc>=m:continue
   rr=r+da-H(bb,m,q)+H(b,m,q)
   nxt=(bb,rr,cc,left or bb!=q)
   if nxt not in seen:
    seen.add(nxt);todo.append((nxt,path+[label]))
 return dict(m=m,q=q,pass_check=True,states=len(seen))
results=[check(m,q) for q in range(5,15) for m in range(4,q)]
out={'scope':'Exact finite phase-word enumeration below degree m. Algebraic proof remains required for arbitrary m,q. A-feasibility is relaxed, so no feasible witness is excluded.','all_pass':all(x['pass_check'] for x in results),'cases':results}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'all_pass':out['all_pass'],'cases':len(results),'max_states':max(x.get('states',0) for x in results)},indent=2))
