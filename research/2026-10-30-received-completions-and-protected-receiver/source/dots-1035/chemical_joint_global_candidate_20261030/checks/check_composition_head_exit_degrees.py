"""Exact positive-Schur exponents at fixed s=B-g_(A+C)."""
import json, math

def fall(n,k): return math.prod(range(n-k+1,n+1)) if n>=k else 0
def g(n):return 4*(n//3)+n%3

def compute(K):
 states=[(a,n-a) for n in range(K+1) for a in range(n+1)]
 edges={x:{} for x in states}
 for a,c in states:
  n=a+c;source=(a,c)
  reactions=[(a+1,c,1,0,True),(a+2,c,3,1,a>0),(a-3,c,-4,4,a>=3),
   (a+1,c-1,0,4,6*fall(c,3)+a*fall(c,2)+7*fall(a,2)*c>0),
   (a-1,c+1,0,4,12*a*fall(c,2)+fall(a,2)*c+fall(a,3)>0)]
  for aa,cc,db,d,ok in reactions:
   if not ok:continue
   nn=aa+cc;delta=db-g(nn)+g(n)
   target='up' if delta>0 else 'down' if delta<0 else 'safe' if nn>K else (aa,cc)
   edges[source][target]=max(d,edges[source].get(target,-10**6))
  edges['s'+str(source)]={source:0}
 for v in states:
  out=edges[v];assert out
  den=max(out.values())
  for i in list(edges):
   if i==v or v not in edges[i]:continue
   d=edges[i].pop(v)
   for j,dj in out.items():
    if j!=i:edges[i][j]=max(edges[i].get(j,-10**6),d+dj-den)
  del edges[v]
 return {i:{'up':e.get('up'),'safe':e.get('safe')} for i,e in edges.items()}
print(json.dumps([{'K':K,'degrees':compute(K)} for K in [5,8,11]],indent=2))
