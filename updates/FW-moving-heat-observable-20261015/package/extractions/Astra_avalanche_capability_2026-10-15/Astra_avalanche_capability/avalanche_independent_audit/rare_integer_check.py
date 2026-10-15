"""Standalone rare-bound arithmetic cross-check. Requires Python, numpy, mpmath.
Run: python rare_integer_check.py
No production module imports. Exact dyadic endpoints are printed/saved.
"""
from fractions import Fraction as Q
from pathlib import Path
import json
import numpy as np
import mpmath as mp
mp.iv.dps=140
mp.mp.dps=160
BITS=1024
M=1<<BITS

def interval(q):
 q=Q(q);return mp.iv.mpf(q.numerator)/q.denominator

def exact(t):
 sign,man,exponent,bc=t
 return (-1 if sign else 1)*Q(man)*Q(2)**exponent

def fmt(q):return mp.nstr(mp.mpf(q.numerator)/q.denominator,125)

def check(n,f0,T,t,m):
 s=sorted(map(Q,np.random.RandomState(0).random_sample(n)),reverse=True);F=n*f0
 clock=interval(t)*mp.iv.exp(interval(F/(m*T)))
 ps=[]
 for v in s:
  p=mp.iv.exp(-mp.iv.exp(-interval(v/T))*clock)
  l,h=map(exact,p._mpi_);lo=l*M;hi=h*M
  ps.append((lo.numerator//lo.denominator,-(-hi.numerator//hi.denominator)))
 def dp(upper):
  h=[M]*(n+1)
  for j in range(n-1,-1,-1):
   p=ps[j][0 if upper else 1]
   gated=[h[c] if c<m or s[j]*c<=F else 0 for c in range(j+2)]
   h=[((M-p)*gated[c]+p*gated[c+1]+(M-1 if upper else 0))//M for c in range(j+1)]
  return Q(h[0],M)
 lo,hi=dp(False),dp(True)
 assert lo<=hi
 return {'n':n,'f0':str(f0),'T':str(T),'t':str(t),'m':m,'fixed_point_bits':BITS,'input_interval_digits':mp.iv.dps,'bound_quantity_lower':fmt(lo),'bound_quantity_upper':fmt(hi),'absolute_width':fmt(hi-lo),'relative_width':fmt((hi-lo)/lo),'upper_numerator':str(hi.numerator),'upper_denominator':str(hi.denominator)}

if __name__=='__main__':
 rows=[check(400,f0,T,t,m) for f0,T,m in [(Q(7,40),Q(3,20),166),(Q(3,20),Q(1,10),142)] for t in [Q(1,10),Q(1,100)]]
 output=json.dumps(rows,indent=2);Path(__file__).with_name('rare_integer_1024_results.json').write_text(output+'\n');print(output)
