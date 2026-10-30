#!/usr/bin/env python3
import heapq,json
L=18; R=5
V={(x,y) for x in range(-L,L+1) for y in range(-L,L+1)}
nb=lambda p:[(p[0]+dx,p[1]+dy) for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)] if (p[0]+dx,p[1]+dy) in V]
color=lambda p:(p[0]+p[1])%2
w=lambda p,z:color(p) # black->white cost0, white->black cost1
metric=lambda p,z:(abs(p[0]-z[0])+abs(p[1]-z[1])+color(p))//2
F={(0,0),(1,0),(-1,0),(0,1),(0,-1)}; C=V-F
c={p:(p[0]+p[1])//2 for p in F};c[0,0]=99
u={p:10**9 for p in C};heap=[]
for f in F:
 for p in nb(f):
  if p in C and c[f]+w(f,p)<u[p]:u[p]=c[f]+w(f,p);heapq.heappush(heap,(u[p],p))
while heap:
 cost,p=heapq.heappop(heap)
 if cost!=u[p]:continue
 for z in nb(p):
  if z in C and cost+w(p,z)<u[z]:u[z]=cost+w(p,z);heapq.heappush(heap,(u[z],z))
h={p:(p[0]+p[1])//2 for p in C};deficit=sum(u[p]-h[p] for p in C);updates=0;sweeps=0
while any(h[p]!=u[p] for p in C):
 changed=0
 for p in sorted(C):
  if h[p]<u[p] and all(h[p]+1<=(h[z] if z in C else c[z])+w(z,p) for z in nb(p)):
   h[p]+=1;updates+=1;changed+=1
 assert changed
 sweeps+=1
S=[p for p in C if metric((0,0),p)==R]; ball={p for p in V if metric((0,0),p)<=R}
violation=max(u[z]-u[p]-metric(p,z) for p in S for z in S)
ext={p:min(u[z]+metric(z,p) for z in S) for p in ball}
edgeviol=max(ext[z]-ext[p]-w(p,z) for p in ball for z in nb(p) if z in ball)
assert updates==deficit and violation<=0 and edgeviol<=0 and all(ext[p]==u[p] for p in S)
print(json.dumps({'scope':'Checkerboard ordered-layer directed-cost fixture only','physical_sites':len(V),'sphere_sites':len(S),'directed_R':R,'total_deficit':deficit,'legal_increments':updates,'sweeps':sweeps,'directed_sphere_violation':violation,'extension_constraint_violation':edgeviol,'extension_matches_sphere':True},indent=2))
