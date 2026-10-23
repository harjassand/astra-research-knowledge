#!/usr/bin/env python3
"""Exact supplementary checks for finite_palette_challenge.md; stdlib only."""
from fractions import Fraction as Q
from pathlib import Path
from itertools import combinations
import json,time,resource
start=time.perf_counter(); cpu=time.process_time()
def dot(a,b): return sum((x*y for x,y in zip(a,b)),Q(0))
def matmul(A,B): return [[dot(r,col) for col in zip(*B)] for r in A]
def trans(A): return list(map(list,zip(*A)))
def eye(n): return [[Q(int(i==j)) for j in range(n)] for i in range(n)]
def inv(A):
 n=len(A); W=[r[:]+s[:] for r,s in zip(A,eye(n))]
 for k in range(n):
  p=next(i for i in range(k,n) if W[i][k]); W[k],W[p]=W[p],W[k]
  f=W[k][k]; W[k]=[x/f for x in W[k]]
  for i in range(n):
   if i!=k:
    f=W[i][k]; W[i]=[a-f*b for a,b in zip(W[i],W[k])]
 return [r[n:] for r in W]
checks=[]
for c in (3,4,6,8):
 for N in (1,3,11):
  G=[[Q(1) if i==j else -Q(1,c-1) for j in range(c)] for i in range(c)]
  assert all(sum(r)==0 for r in G)
  center=[Q(1)]*c
  action2=sum(center[i]*G[i][j]*center[j] for i in range(c) for j in range(c))
  assert action2==0
  action2+=Q(c-1,N)
  assert action2==Q(c-1,N)
  for s in range(1,c):
   T=[r[:s] for r in G[:s]]
   H=[[T[i][j]-Q(c-s,c-1)*int(i==j) for j in range(s)] for i in range(s)]
   # H=(1/(c-1))*(sI-11^T): exact sum-of-squares form.
   for i in range(s):
    for j in range(s): assert H[i][j]==Q(s*int(i==j)-1,c-1)
  checks.append({'name':'simplex_star_and_local_gram','c':c,'N':N,'action_norm_squared':str(action2)})
# Rational palette in R3: p3=(-1,-1,-1)/3. Subsets of size3 are independent.
P=eye(3)+[[Q(-1,3)]*3]
# Every proper subpalette has Gram >= I/12; certify via positive exact LDL pivots.
for size in range(1,4):
 for inds in combinations(range(4),size):
  A=[P[i] for i in inds]; G=matmul(A,trans(A))
  H=[[G[i][j]-Q(1,12)*int(i==j) for j in range(size)] for i in range(size)]
  for k in range(size):
   piv=H[k][k]; assert piv>0
   for i in range(k+1,size):
    for j in range(k+1,size): H[i][j]-=H[i][k]*H[k][j]/piv
checks.append({'name':'all_rational_proper_subpalette_gram_bounds','palette_rows':4,'dimension':3,'certified_sigma_squared_lower':'1/12'})
colors=[0,3,2,1,2,3] # disjoint path (0-1-2) and edge(3-4); isolated5
edges=[(0,1),(1,2),(3,4)]; n=len(colors)
D=[[Q(0) for j in range(n)] for i in range(n)]
for i in range(n): D[i][i]=Q(i-2,7)
for k,(i,j) in enumerate(edges): D[i][j]=D[j][i]=Q(k+1,5)
X=[P[c][:] for c in colors]; Y=matmul(D,X)
counts=[{} for _ in range(n)]
for i,j in edges:
 counts[i][colors[j]]=counts[i].get(colors[j],0)+1
 counts[j][colors[i]]=counts[j].get(colors[i],0)+1
aggregates=[]; selected=set()
for i in range(n):
 T=sorted(set([colors[i]])|set(counts[i])); A=[P[c] for c in T]; At=trans(A)
 R=matmul(At,inv(matmul(A,At))); a=matmul([Y[i]],R)[0]
 aggregates.append(dict(zip(T,a)))
 assert a[T.index(colors[i])]==D[i][i]
 selected.add((i,colors[i]))
for i,j in edges:
 if counts[i][colors[j]]==1: leaf,other=i,j
 else: assert counts[j][colors[i]]==1; leaf,other=j,i
 cell=(leaf,colors[other]); assert cell not in selected; selected.add(cell)
 assert aggregates[leaf][colors[other]]==D[i][j]
checks.append({'name':'rational_local_frame_noiseless_decoder','n':n,'edges':len(edges),'selected_cells':len(selected)})
report={'passed':True,'checks':checks,'wall_seconds':time.perf_counter()-start,'cpu_seconds':time.process_time()-cpu,'peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,'scope':'Exact supplementary finite identities; universal result is analytic proof.'}
p=Path(__file__).resolve().parents[1]/'results'/'finite_palette_checks.json';p.parent.mkdir(exist_ok=True);p.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
