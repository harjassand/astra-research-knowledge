"""Exact-binomial-verified upper confidence limits for a FROZEN sampler's abort rate.
SciPy proposes a rational grid endpoint; integer arithmetic verifies coverage.
"""
from fractions import Fraction as F
from math import ceil
from scipy.stats import beta

def cdf_le_alpha(n,x,p,alpha):
 if x>=n:return False
 if p>=1:return True
 a,b=p.numerator,p.denominator;c=b-a
 term=c**n;num=term
 for j in range(x):
  numerator=term*(n-j)*a;denominator=(j+1)*c
  assert numerator%denominator==0
  term=numerator//denominator;num+=term
 return num*alpha.denominator<=alpha.numerator*(b**n)

def upper(n,x,alpha=F(1,100),resolution=10**6):
 if not 0<=x<=n:raise ValueError('Invalid counts')
 if n==0 or x==n:return F(1)
 guess=float(beta.ppf(1-float(alpha),x+1,n-x))
 a=min(resolution,max(1,ceil(guess*resolution)))
 while a<resolution:
  p=F(a,resolution)
  if cdf_le_alpha(n,x,p,alpha):return p
  a+=1
 return F(1)

def anytime_checkpoint(n,x,index,eta=F(1,100)):
 """At checkpoint j>=1 spend eta/[j(j+1)], so all checks jointly covered.
 Algorithm must be frozen; new independent trials. index=j is valid only for
 predetermined sample-count checkpoints n_j. For arbitrary adaptive checking,
 set index=n, spending across EVERY possible sample count. Stop at any tested checkpoint.
 """
 if index<1:raise ValueError('Index starts at1')
 alpha=eta/(index*(index+1))
 return upper(n,x,alpha),alpha

if __name__=='__main__':
 import json
 from pathlib import Path
 cases=[]
 for n,x in [(5,0),(5,2),(30,0),(30,1),(100,0),(1000,0),(5000,0),(1000,3)]:
  u=upper(n,x);ua,alpha=anytime_checkpoint(n,x,4)
  cases.append(dict(n=n,aborts=x,fixed99pct_upper=str(u),fixed99pct_upper_float=float(u),checkpoint4_anytime99pct_upper=str(ua),checkpoint_alpha=str(alpha),integer_binomial_verified=True))
 Path(__file__).with_suffix('.json').write_text(json.dumps(cases,indent=2));print(json.dumps(cases,indent=2))
