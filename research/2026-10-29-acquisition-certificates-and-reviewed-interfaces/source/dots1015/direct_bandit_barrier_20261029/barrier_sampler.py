"""Finite rational approximation to log-barrier FTRL probabilities."""
from fractions import Fraction as F

def distribution(cumulative,eta,horizon):
 if not cumulative or horizon<1 or not F(0)<eta<=1:raise ValueError('invalid learner parameters')
 L=list(map(F,cumulative));eta=F(eta);M=len(L);D=8*M*horizon
 low=min(L);c=[eta*(x-low) for x in L];lo=F(1);hi=F(M)
 # Fixed public count; exact root is bracketed, including endpoint equality.
 steps=((M-1)*D).bit_length() if M>1 else 0
 for _ in range(steps):
  mid=(lo+hi)/2
  if sum(1/(x+mid) for x in c)>1:lo=mid
  else:hi=mid
 assert hi-lo<=F(1,D)
 lower=[1/(x+hi) for x in c];weights=[(D*x.numerator)//x.denominator+2 for x in lower];total=sum(weights)
 assert D<=total<=D+2*M
 q=[F(w,total) for w in weights]
 return q,dict(D=D,weights=weights,total=total,root_lower=str(lo),root_upper=str(hi),steps=steps)

def update(cumulative,arm,flip,q,rho):
 if flip not in (0,1):raise ValueError('flip must be binary')
 out=list(map(F,cumulative));out[arm]+=F(flip)/(F(rho)*q[arm]);return out
