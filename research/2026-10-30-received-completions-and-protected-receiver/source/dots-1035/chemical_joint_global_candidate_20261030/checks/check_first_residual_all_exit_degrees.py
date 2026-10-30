"""Leading degrees of exact fixed-residual hitting probabilities, not actual recurrence."""
import json

def h(b):
 if b<=3:return b
 return [3,4,5][(b-4)%3]+2*((b-4)//3)
def probs(K):
 edges={i:{} for i in range(K+1)}
 for b in range(K+1):
  for bb,dn,d,ok in [(b+1,1,0,True),(b+3,2,1,b>0),(b-4,-3,3,b>=4)]:
   if not ok:continue
   delta=dn-h(bb)+h(b)
   target='up' if delta>0 else 'down' if delta<0 else 'safe' if bb>K else bb
   edges[b][target]=max(d,edges[b].get(target,-10**6))
  edges['s'+str(b)]={b:0}
 for v in range(K+1):
  out=edges[v];den=max(out.values())
  for i in list(edges):
   if i==v or v not in edges[i]:continue
   d=edges[i].pop(v)
   for j,dj in out.items():
    if j!=i:edges[i][j]=max(edges[i].get(j,-10**6),d+dj-den)
  del edges[v]
 return {i:{'up':e.get('up'),'safe':e.get('safe')} for i,e in edges.items()}
print(json.dumps([{'K':K,'up_degrees':probs(K)} for K in [7,8,12,16,24,48]],indent=2))
