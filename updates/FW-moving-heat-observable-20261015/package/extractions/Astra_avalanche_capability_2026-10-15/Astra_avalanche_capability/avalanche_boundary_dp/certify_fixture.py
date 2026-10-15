from pathlib import Path
"""Interval-arithmetic prototype for the exact binary strengths, F=5/8,T=1/20.
Uses installed mpmath interval exp and arithmetic; no downloaded code.
"""
from fractions import Fraction as Q
import mpmath as mp
import numpy as np,time,json
mp.iv.dps=40
I=mp.iv.mpf

def iq(q):
 q=Q(q);return I(q.numerator)/I(q.denominator)

def run():
 s=sorted([Q(float(x)) for x in np.random.RandomState(0).rand(5)],reverse=True);n=len(s);F=Q(5,8);T=Q(1,20)
 js=[0]+[sum(x>F/m for x in s) for m in range(1,n+1)]
 bucket=[[] for _ in range(n+1)]
 for m,j in enumerate(js):
  if j>=m:bucket[j].append(m)
 ok=[[c==0 or s[j]<=F/c for c in range(n+1)] for j in range(n)]
 lam=[mp.iv.exp(-iq(x/T)) for x in s];psi=[I(0)]+[mp.iv.exp(-iq(F/(m*T))) for m in range(1,n+1)]
 def g(u):
  p=[mp.iv.exp(-l*iq(u)) for l in lam];q=[1-x for x in p]
  a=[I(0) for _ in range(n+1)];v=[I(1)]+[I(0) for _ in range(n)]
  for m in bucket[0]:a[m]=v[m]
  for j in range(1,n+1):
   v=[q[j-1]*v[c]+(p[j-1]*v[c-1] if c else 0) for c in range(n+1)]
   for m in bucket[j]:a[m]=v[m]
  h=[I(1) for _ in range(n+1)];ans=I(0)
  for m in bucket[n]:ans+=psi[m]*a[m]*h[m]
  for j in range(n-1,-1,-1):
   gated=[h[c] if ok[j][c] else I(0) for c in range(n+1)]
   h=[q[j]*gated[c]+(p[j]*gated[c+1] if c<n else 0) for c in range(n+1)]
   for m in bucket[j]:ans+=psi[m]*a[m]*h[m]
  return ans
 start=time.perf_counter();left=Q(1,1000);U=Q(10**8);ratio=Q(101,100)
 gl=g(left);lo=iq(left)*gl;hi=iq(left)*psi[n];evals=1
 while left<U:
  right=min(U,left*ratio);gr=g(right);width=iq(right-left)
  lo+=width*gr;hi+=width*gl;left=right;gl=gr;evals+=1
 tail=psi[n]*sum(mp.iv.exp(-l*iq(U))/l for l in lam);hi+=tail
 result={'lower_sum_interval':str(lo),'upper_sum_interval':str(hi),'tail_upper_interval':str(tail),'evaluations':evals,'seconds':time.perf_counter()-start,'mpmath_version':mp.__version__,'decimal_precision':40,'strengths_exact_rationals':[str(x) for x in s],'F':'5/8','T':'1/20','u0':'1/1000','U':'100000000','ratio':'101/100'}
 print(json.dumps(result,indent=2));open(str(Path(__file__).resolve().parent.parent / 'avalanche_boundary_dp/certified_fixture.json'),'w').write(json.dumps(result,indent=2))
if __name__=='__main__':run()
