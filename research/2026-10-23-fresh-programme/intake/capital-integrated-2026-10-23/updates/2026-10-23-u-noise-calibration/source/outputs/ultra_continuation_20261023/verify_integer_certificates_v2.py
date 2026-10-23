"""Separate standard-library-only verifier with arbitrary-precision integers.
Verifies finite expansion certificates, not the scientific transfer proof.
"""
import json,time
from pathlib import Path
import argparse
parser=argparse.ArgumentParser();parser.add_argument('--designs',type=Path,required=True);args=parser.parse_args()
ROOT=Path(__file__).resolve().parent;start=time.perf_counter();verified=[]
for item in json.loads(args.designs.read_text()):
 n=item['n'];hs=item['H']
 if type(n) is not int or n<2 or n%2:raise ValueError('positive even dimension required')
 if len(hs)!=8:raise ValueError('exactly eight involutions required')
 k=item['certificate']['power']
 if type(k) is not int or not 1<=k<=20:raise ValueError('certificate power must be integer in [1,20]')
 if type(item['certificate']['max_abs_row_sum_integer']) is not int:raise ValueError('integer row sum required')
 if any(type(x) is not int for h in hs for row in h for x in row):raise ValueError('literal integer entries required')
 pairs=[(i,j) for i in range(n) for j in range(i+1,n)];idx={p:i for i,p in enumerate(pairs)};m=len(pairs);T=[{} for _ in pairs]
 for H in hs:
  if not (len(H)==n and all(len(r)==n for r in H)):raise ValueError("certificate check failed")
  if not (all(H[i][j] in (-1,0,1) and H[i][j]==H[j][i] for i in range(n) for j in range(n))):raise ValueError("certificate check failed")
  if not (all(H[i][i]==0 and sum(x!=0 for x in H[i])==1 for i in range(n))):raise ValueError("certificate check failed")
  p=[next(j for j,x in enumerate(row) if x) for row in H];sg=[H[i][p[i]] for i in range(n)]
  if not (all(p[p[i]]==i and sg[i]*sg[p[i]]==1 for i in range(n))):raise ValueError("certificate check failed")
  for row,(i,j) in enumerate(pairs):
   a,b=p[i],p[j];col=idx[min(a,b),max(a,b)];v=sg[i]*sg[j]*(1 if a<b else -1);T[row][col]=T[row].get(col,0)+v
 if not (all(v==T[j].get(i,0) for i,r in enumerate(T) for j,v in r.items())):raise ValueError("certificate check failed")
 k=item['certificate']['power'];P=[[int(i==j) for j in range(m)] for i in range(m)]
 for _ in range(k):
  nxt=[]
  for r in T:
   row=[0]*m
   for z,v in r.items():
    if v:
     for j,x in enumerate(P[z]):row[j]+=v*x
   nxt.append(row)
  P=nxt
 maxrow=max(sum(abs(x) for x in row) for row in P)
 if not (maxrow==item['certificate']['max_abs_row_sum_integer'] and maxrow<=7**k):raise ValueError("certificate check failed")
 verified.append({'n':n,'power':k,'max_abs_row_sum':maxrow,'bound':7**k})
r={'verified':verified,'arithmetic':'Python arbitrary-precision integers; no NumPy','scientific_scope':'Exact finite channel certificate only; not independent proof review or physical validation','wall_seconds':time.perf_counter()-start};(ROOT/'integer_verification.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
