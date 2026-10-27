"""Exact binomial-tail corroboration for the rare-acceptance certificate."""
import math
from scipy.stats import binom
count=0
for n in [50,200,1000,10000]:
 for kmin in [1,5,20,n/3]:
  for z in [1e-6,.001,.01,.1,.4,.8]:
   mu=n*z
   lower=max(math.ceil(kmin),math.floor(2*mu)+1)
   prob=binom.sf(lower-1,n,z)
   bound=math.exp(-kmin/6)
   assert prob<=bound+1e-14
   count+=1
for k in [1,5,20,100,1000,10000]:
 for theta in [.1,.7,.875]:
  prob=binom.sf(math.ceil(15*k/16)-1,k,theta)
  assert prob<=math.exp(-k/128)+1e-13
 for theta in [59/61,.98,1.]:
  # Strict failure of J/k >=15/16.
  prob=binom.cdf(math.ceil(15*k/16)-1,k,theta)
  assert prob<=math.exp(-k/800)+1e-13
assert 59/61-15/16>1/40
assert 59/2160>1/40
print('PASS',count,'exact count-tail cases,36 conditional binomial tails, and discovery constants.')
