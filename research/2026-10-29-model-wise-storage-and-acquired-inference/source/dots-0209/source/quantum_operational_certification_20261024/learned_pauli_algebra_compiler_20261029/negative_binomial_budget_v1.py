"""Exact-integer negative-binomial budget, no floating-point acceptance decisions."""
import math,json
from fractions import Fraction

def tail_ratio(m,t,probe_num,den):
 if not (m>=0 and t>=0 and 0<probe_num<=den):raise ValueError('Invalidparameters')
 if m==0:return 0,1
 N=m+t;a=probe_num;b=den-a
 numerator=sum(math.comb(N,j)*a**j*b**(N-j) for j in range(m))
 return numerator,den**N

def budget(m,probe_num,den,epsilon_num,epsilon_den):
 if not (0<epsilon_num<epsilon_den):raise ValueError('Requireepsilonin(0,1)')
 def ok(t):a,b=tail_ratio(m,t,probe_num,den);return a*epsilon_den<=b*epsilon_num
 if ok(0):return 0
 high=1
 while not ok(high):high*=2
 low=0
 while high-low>1:
  mid=(low+high)//2
  if ok(mid):high=mid
  else:low=mid
 assert ok(high) and not ok(high-1)
 return high

def run():
 records=[]
 for m,an,den,en,ed in [(1,1,2,1,100),(2,1,2,1,1000),(32,1,4,1,1000000),(128,1,4,1,1000000),(128,1,10,1,1000000)]:
  t=budget(m,an,den,en,ed);a,b=tail_ratio(m,t,an,den);aa,bb=tail_ratio(m,t-1,an,den) if t else(0,1)
  # Markov mq/[p(t+1)] <=epsilon; only comparator, notusedforacceptance.
  markov=max(0,(m*(den-an)*ed+an*en-1)//(an*en)-1)
  records.append(dict(m=m,probe_probability=f'{an}/{den}',epsilon=f'{en}/{ed}',minimum_t=t,exact_tail_float=float(Fraction(a,b)),previous_tail_float=float(Fraction(aa,bb)),markov_t=markov,min_outer_length=4*t+1,exact_integer_comparison=True))
 print(json.dumps(dict(definition='NB failuresbeforemprobesuccesses; tailP[F>t]',records=records),indent=2))
if __name__=='__main__':run()
