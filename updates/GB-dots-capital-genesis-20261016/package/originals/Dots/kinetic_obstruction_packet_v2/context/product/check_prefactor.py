from fractions import Fraction as R
from decimal import Decimal,localcontext
import json
B=lambda n:R('2.676')*n*(n-1)+R('108.102')
M=lambda n,d:R('.040')*n*(n-1)*(n-2)+(R('37.881')+d*R('8.2207'))*n
out={};P={}
for d,bound in [(2,R(1,10)),(3,R(3,50))]:
 alpha={15:R(0),16:R(1)}; beta={15:R(0),16:R(0)}
 for n in range(16,163):
  alpha[n+1]=((B(n)+M(n,d))*alpha[n]-M(n,d)*alpha[n-1])/B(n)
  beta[n+1]=((B(n)+M(n,d))*beta[n]-M(n,d)*beta[n-1]-1)/B(n)
 z=-beta[163]/alpha[163]
 T={n:alpha[n]*z+beta[n] for n in range(15,164)}
 assert T[15]==T[163]==0 and all(T[n]>0 for n in range(16,163))
 assert T[50]<bound
 for n in range(16,163):assert B(n)*(T[n+1]-T[n])+M(n,d)*(T[n-1]-T[n])==-1
 slopes={16:R(1)}
 for n in range(16,163):slopes[n+1]=M(n,d)*slopes[n]/B(n)
 H=sum(slopes[n] for n in range(16,51))/sum(slopes.values());assert 0<H<R(1,10**25)
 P[d]=1-H
 with localcontext() as c:
  c.prec=35
  out[d]={'T50_descriptive':str(Decimal(T[50].numerator)/Decimal(T[50].denominator)),'strict_mean_upper':str(bound),'all_147_exact_residuals_minus_one':True,'all_147_positive':True,'upper_exit_less_than':'1/10^25'}
assert 4*R(1,10)/P[2]+4*R(3,50)/P[3]<R(13,20)
assert P[2]**4*P[3]**4>1-R(8,10**25)
assert 8*R(3,4)**7>1
q=R(999995,1000000)
assert 1-R(4,10**6)-R(1,10**20)>q
assert q-R(21,32)==R(343745,10**6)>R(34,100)
out['conditional_mean_sum_upper']='13/20'
out['static_prefactor_floor']='(1-8/10^25)*exp(7*lambda/20)'
out['static_additive_floor']='343745/1000000 > 34/100'
print(json.dumps(out,indent=2))
