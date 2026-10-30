"""Exact max-plus leading degrees of positive rate Schur elimination."""
import json
from tree_residual_matrix import HEIGHTS

def collar(K,width):
 h=HEIGHTS[K];inside=[(r,b) for r in range(width) for b in range(K+1)]
 boundary=[(r,b) for r in [-1,width] for b in range(4,K+1)]
 edges={s:{} for s in inside+boundary}
 def add(i,j,d):
  if i!=j:edges[i][j]=max(d,edges[i].get(j,-10**9))
 for r,b in inside:
  for bb,dn,deg,enabled in [(b+1,1,0,True),(b+3,2,1,b>0),(b-4,-3,3,b>=4)]:
   if not enabled:continue
   if not 0<=bb<=K or dn-h[bb]+h[b]!=0:add((r,b),'kill',deg)
   else:add((r,b),(r,bb),deg)
  if b>=4:
   add((r,b),(r-1,b),3);add((r,b),(r+1,b),3)
 for r,b in boundary:add((r,b),(0 if r==-1 else width-1,b),3)
 for v in inside:
  out=edges[v]; assert out,('not transient',v)
  denom=max(out.values())
  incoming=[(i,e[v]) for i,e in edges.items() if i!=v and v in e]
  for i,di in incoming:
   del edges[i][v]
   for j,dj in out.items():add(i,j,di+dj-denom)
  del edges[v]
 def name(v):
  if v=='kill':return 'kill'
  return ('L' if v[0]==-1 else 'R')+str(v[1])
 return {name(i)+'>'+name(j):d for i,e in edges.items() for j,d in e.items()}
out=[]
for K in [4,8,12]:
 old=collar(K,2);new=collar(K,3)
 out.append({'K':K,'equal_support':old.keys()==new.keys(),'equal_degrees':old==new,'old':old,'new':new})
print(json.dumps(out,indent=2,sort_keys=True))
