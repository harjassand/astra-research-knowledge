"""Float beta quantiles propose endpoints; exact integer inequalities certify them.
Floating values cannot make the interval invalid. Failure falls back to bisection.
"""
from fractions import Fraction as F
from math import floor,ceil,isfinite
from scipy.stats import beta
from sampler_frozen_phenomenological import cdf_num,exact_cp as exact_bisection

def exact_cp(x,n,alpha=F(1,1000),bits=20):
 D=1<<bits;denom=D**n;an=alpha.numerator;ad=2*alpha.denominator
 try:
  if x==0:lo=0
  else:
   guess=beta.ppf(float(alpha/2),x,n-x+1)
   if not isfinite(guess):raise ValueError
   lo=max(0,min(D,floor(D*guess)))
   if (denom-cdf_num(n,x-1,lo,D))*ad>an*denom:raise ValueError
  if x==n:hi=D
  else:
   guess=beta.ppf(float(1-alpha/2),x+1,n-x)
   if not isfinite(guess):raise ValueError
   hi=max(0,min(D,ceil(D*guess)))
   if cdf_num(n,x,hi,D)*ad>an*denom:raise ValueError
  return F(lo,D),F(hi,D)
 except (ValueError,OverflowError,ArithmeticError):return exact_bisection(x,n,alpha,bits)

if __name__=='__main__':
 import time,json
 t=time.perf_counter();r=exact_cp(898,10000);print(json.dumps({'interval':[str(x) for x in r],'seconds':time.perf_counter()-t}))
