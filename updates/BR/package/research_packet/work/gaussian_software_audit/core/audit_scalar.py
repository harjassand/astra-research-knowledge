import sys, math, random, json, time
from pathlib import Path
from fractions import Fraction as F
ROOT=Path(__file__).resolve().parents[2]/'gaussian_transfer'
sys.path.insert(0,str(ROOT))
from bigint_sampler_arb import DyadicUnimodal, _as_iv, _parameter_bits, binomial, poisson, negative_binomial
from flint import arb,ctx
eta=F(1,5)
checks=0; cases=0; worst=F(0); largest_envelope=F(0); least_acceptance=F(1)

def check_law(M, mode, lr, weights, inp):
 global checks,cases,worst,largest_envelope,least_acceptance
 law=DyadicUnimodal(M,mode,lr,eta,inp)
 assert weights[mode]==max(weights)
 A=[]
 for k,w in enumerate(weights):
  l,u=law.bounds(k)
  exact=law.scale*w/weights[mode]
  assert l<=exact<=u,(M,mode,k,l,exact,u)
  assert u-l<=2
  A.append(l);checks+=1
 sumw=sum(weights); suma=sum(A)
 tv=sum(abs(F(a,suma)-w/sumw) for a,w in zip(A,weights))/2
 assert tv<=eta/16
 assert F(suma,law.total)>F(1,5)
 assert F(4,5)**law.max_attempts<=eta/16
 assert law.total<=3*law.scale*sumw/weights[mode]+2*(M+1)
 worst=max(worst,tv)
 largest_envelope=max(largest_envelope,F(law.total,law.scale)/(sumw/weights[mode]))
 least_acceptance=min(least_acceptance,F(suma,law.total))
 cases+=1

for n in range(1,31):
 for p in [F(1,1000),F(1,8),F(1,3),F(1,2),F(9,10),F(999,1000)]:
  m=min(n,math.floor((n+1)*p))
  def lr(k,m):
   return arb(m+1).lgamma()+arb(n-m+1).lgamma()-arb(k+1).lgamma()-arb(n-k+1).lgamma()+(k-m)*(_as_iv(p).log()-_as_iv(1-p).log())
  ws=[F(math.comb(n,k))*p**k*(1-p)**(n-k) for k in range(n+1)]
  check_law(n,m,lr,ws,_parameter_bits(n,p))
for r in [F(1,32),F(1,2),F(1),F(3,2),F(7,3),F(5)]:
 for p in [F(1,3),F(1,2),F(9,10),F(999,1000)]:
  mean=r*(1-p)/p; M=math.ceil(4*mean/eta);m=max(0,math.floor((r-1)*(1-p)/p))
  def lr(k,m):
   rr=_as_iv(r)
   return (k+rr).lgamma()-arb(k+1).lgamma()-(m+rr).lgamma()+arb(m+1).lgamma()+(k-m)*_as_iv(1-p).log()
  ws=[F(1)]
  for k in range(M):ws.append(ws[-1]*(r+k)*(1-p)/(k+1))
  check_law(M,m,lr,ws,_parameter_bits(M,r,p))
for rate in [F(1,1000),F(1,7),F(1,2),F(1),F(3,2),F(3),F(17,3)]:
 M=math.ceil(4*rate/eta);m=math.floor(rate)
 def lr(k,m):return arb(m+1).lgamma()-arb(k+1).lgamma()+(k-m)*_as_iv(rate).log()
 ws=[F(1)]
 for k in range(M):ws.append(ws[-1]*rate/(k+1))
 check_law(M,m,lr,ws,_parameter_bits(M,rate))

# Python's standard randrange can use arbitrarily many getrandbits calls,
# even for a one-point target; this probe emits a finite rejection run.
class LongReject(random.Random):
 def __init__(self,N):super().__init__(0);self.N=N;self.calls=0
 def getrandbits(self,k):
  self.calls+=1
  if self.calls<=self.N:return (1<<k)-1
  return 0
rng=LongReject(10000)
law=DyadicUnimodal(0,0,lambda k,m:arb(0),F(1,100),0)
assert law.draw(rng)==0
cap_probe={'getrandbits_calls':rng.calls,'outer_attempts':law.last_attempts,'max_outer_attempts':law.max_attempts}

# Large exact integer and rational inputs exercise cancellation and exponent ranges.
extremes=[]
for B in [128,512,2048]:
 for name,fn,args in [('binomial_symmetric',binomial,(1<<B,F(1,2))),('binomial_sparse',binomial,(1<<B,F(1,1<<B))),('nb_tinyshape',negative_binomial,(F(1,1<<B),F(1,2))),('nb_nearcritical',negative_binomial,(F(1,2),F(1,1<<B))),('poisson_tiny',poisson,(F(1,1<<B),)),('nb_huge_shape_rare_failure',negative_binomial,(F(1<<B),1-F(1,1<<B))),('poisson_huge',poisson,(F(1<<B),)),('binomial_huge_nearone',binomial,(1<<B,1-F(1,1<<B)))]:
  t=time.perf_counter();x=fn(*args,random.Random(8721),F(1,10**8));elapsed=time.perf_counter()-t
  assert isinstance(x,int) and x>=0
  extremes.append({'kind':name,'input_bits':B,'output_bits':x.bit_length(),'seconds':elapsed})
result={'cases':cases,'exact_ratio_checks':checks,'max_rounding_tv':float(worst),'max_envelope_to_true_mass':float(largest_envelope),'min_actual_acceptance':float(least_acceptance),'cap_probe':cap_probe,'extremes':extremes}
print(json.dumps(result,indent=2))
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
