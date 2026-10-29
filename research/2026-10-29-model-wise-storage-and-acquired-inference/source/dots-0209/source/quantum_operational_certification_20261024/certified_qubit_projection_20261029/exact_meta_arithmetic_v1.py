"""Rational EXP3 arithmetic and capped exact-probability private coins.
Born measurements are inputs, not simulated or reconstructed by this kernel.
"""
from fractions import Fraction as F
from math import isqrt

def _series(x,n):
 term=F(1);total=term
 for k in range(1,n+1):term*=-x/k;total+=term
 return total

def exp_factor(n,d,bits=64):
 """For x=n/d in[0,2/3], return dyadic q<=exp(-x), and proved relative debit.
 Integer division first bounds x on a fixed grid, so later rational work
 does not inherit the large weight denominators.
 """
 assert 0<=n and 0<d and 3*n<=2*d
 D=1<<bits;k=(n*D)//d
 lo=F(k,D);hi=lo if k*d==n*D else F(k+1,D)
 # Alternating decreasing terms bracket exp(-x). 33/32 terms keep truncation
 # below2^-128 on the permitted interval; its actual rational debit is kept.
 lower=_series(hi,33);upper=_series(lo,32)
 qint=(lower.numerator*D)//lower.denominator
 q=F(qint,D);rho=(upper-q)/lower
 assert 0<q<=lower<=upper and rho<F(1,2)
 # Round the debit UP to a fixed dyadic grid; its accumulated denominator
 # therefore remains fixed instead of multiplying across observations.
 rho=F((rho.numerator*D+rho.denominator-1)//rho.denominator,D)
 return qint,rho

def rational_coin(n,d,rng,cap=128):
 """Outcome0 has ideal probability n/d. Cap failure<=2^-cap, returned explicitly."""
 assert 0<=n<=d and d>0
 b=(d-1).bit_length()
 for attempt in range(1,cap+1):
  u=rng.getrandbits(b)
  if u<d:return (0 if u<n else 1),False,attempt*b
 return 0,True,cap*b

class ExactMeta:
 def __init__(self,N,bits=64,cap=128):
  self.s=isqrt(N);assert self.s*self.s==N
  self.N=N;self.bits=bits;self.cap=cap;self.weights=[9,1]
  self.rho_sum=F(0);self.max_rho=F(0);self.max_weight_bits=4;self.coin_bits=0;self.coin_failures=0;self.updates=0
 def probability(self):
  a,b=self.weights;total=a+b
  # ((1-1/s)*a/total+1/(2s)), deliberately unreduced.
  return 2*(self.s-1)*a+total,2*self.s*total
 def select(self,rng):
  n,d=self.probability();i,failed,used=rational_coin(n,d,rng,self.cap)
  self.coin_bits+=used;self.coin_failures+=failed
  return i
 def update(self,i,loss):
  assert i in [0,1] and loss in [0,1]
  if not loss:return
  n,d=self.probability();ni=n if i==0 else d-n
  q,rho=exp_factor(d,3*self.s*ni,self.bits)
  self.weights[i]*=q;self.weights[1-i]<<=self.bits
  # Remove common powers of two only, no expensive gcd on growing products.
  shift=min((w&-w).bit_length()-1 for w in self.weights)
  self.weights=[w>>shift for w in self.weights]
  self.max_weight_bits=max(self.max_weight_bits,max(w.bit_length() for w in self.weights))
  self.max_rho=max(self.max_rho,rho);self.rho_sum+=rho;self.updates+=1
 def budgets(self):
  # eta=1/(4sqrtN); sum relative-factor debits in potential proof <=2sumrho.
  return {'loss_updates':self.updates,'maximum_weight_bits':self.max_weight_bits,'private_random_bits':self.coin_bits,'actual_cap_failures':self.coin_failures,'max_relative_factor_debit':str(self.max_rho),'extra_average_regret_bound':str(8*self.s*self.rho_sum/self.N),'whole_trajectory_coin_coupling_bound':str(F(self.N,1<<self.cap))}
