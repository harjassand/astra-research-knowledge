#!/usr/bin/env python3
"""Exact rational check of a local covariance solve and geometric error bound.
This tests the algebraic lemma, not source-model identification or execution cost.
"""
from fractions import Fraction as F
from random import Random
from pathlib import Path
import json

def coefficient(ts,l):
 n=len(ts)+1
 B=[[F(0) for _ in range(n)] for _ in range(n)]
 if n>1:B[0][1]=ts[0];B[-1][-2]=ts[-1]
 for i in range(1,n-1):
  a,b=ts[i-1],ts[i];plus=(a+b)/(1+a*b);minus=(a-b)/(1-a*b)
  B[i][i-1]=(plus+minus)/2;B[i][i+1]=(plus-minus)/2
 C=[]
 for j in range(n):
  v=F(1)
  for t in ts[min(j,l):max(j,l)]:v*=t
  C.append(v)
 A=[[F(i==j)-B[i][j] for j in range(n)]+[C[i]] for i in range(n)]
 for i in range(n):
  p=A[i][i];assert p
  A[i]=[x/p for x in A[i]]
  for j in range(i+1,n):
   p=A[j][i];A[j]=[a-p*b for a,b in zip(A[j],A[i])]
 x=[F(0)]*n
 for i in range(n-1,-1,-1):x[i]=A[i][-1]-sum(A[i][j]*x[j] for j in range(i+1,n))
 return x[l],max(sum(abs(v) for v in row) for row in B)
rng=Random(943);rows=[];k=F(19,20);r=1-k
for case in range(8):
 n=13;l=6
 ts=[F(rng.randrange(-10,11),410) for _ in range(n-1)]
 full,row=coefficient(ts,l);assert row<=r
 for R in range(6):
  lo=max(0,l-R);hi=min(n-1,l+R)
  small,srow=coefficient(ts[lo:hi],l-lo);assert srow<=r
  error=abs(full-small);bound=2*r**(R+1)/k;assert error<=bound
  rows.append(dict(case=case,radius=R,local_sites=hi-lo+1,error_exact=str(error),bound_exact=str(bound),error_float=float(error),bound_float=float(bound)))
out=dict(scope=__doc__,cases=len(rows),rows=rows)
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(dict(cases=len(rows),max_error_bound_ratio=max(x['error_float']/x['bound_float'] for x in rows),radius4_bound=str(2*r**5/k)),indent=2))
