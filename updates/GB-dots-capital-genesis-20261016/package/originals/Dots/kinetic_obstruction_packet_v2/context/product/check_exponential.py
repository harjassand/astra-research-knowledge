from fractions import Fraction as F
from math import factorial
from decimal import Decimal, localcontext
import json

def birth(n):return F('2.676')*n*(n-1)+F('108.102')
def death(n,d):return F('.040')*n*(n-1)*(n-2)+(F('37.881')+d*F('8.2207'))*n
# Independent shooting recurrence, not the producer's tridiagonal elimination.
out={}
for d,upper in [(2,12),(3,3)]:
 alpha={15:F(0),16:F(1)};beta={15:F(1),16:F(0)}
 for n in range(16,163):
  b=birth(n);mu=death(n,d)
  alpha[n+1]=((b+mu-15)*alpha[n]-mu*alpha[n-1])/b
  beta[n+1]=((b+mu-15)*beta[n]-mu*beta[n-1])/b
 assert alpha[163]!=0
 z=(1-beta[163])/alpha[163]
 H={n:alpha[n]*z+beta[n] for n in range(15,164)}
 assert H[15]==H[163]==1
 assert all(H[n]>1 for n in range(16,163))
 for n in range(16,163):
  assert birth(n)*(H[n+1]-H[n])+death(n,d)*(H[n-1]-H[n])+15*H[n]==0
 assert H[50]<upper
 with localcontext() as ctx:
  ctx.prec=35
  out[d]={'independent_method':'exact shooting recurrence','boundary_values_exact':'H(15)=H(163)=1','all_147_interior_values_strictly_greater_than_one':True,'all_147_residuals_exactly_zero':True,'H50_descriptive':str(Decimal(H[50].numerator)/Decimal(H[50].denominator)),'H50_strict_rational_upper':upper}
# Shorter independent Taylor certificate. All omitted terms are positive.
K=0;S=F(0)
while S<=3000000:
 S+=F(15**K,factorial(K));K+=1
assert S>3000000
out['exp15_lower_certificate']={'last_taylor_degree':K-1,'exact_partial_sum':str(S),'strict_lower':3000000}
e=F(1,10**20);L2=1-F(12,3000000)-e;L3=1-F(3,3000000)-e
P=L2**4*L3**4
assert P>F(49999,50000)
with localcontext() as ctx:
 ctx.prec=40
 out['product_lower_descriptive']=str(Decimal(P.numerator)/Decimal(P.denominator))
 out['margin_above_49999_over_50000_descriptive']=str(Decimal((P-F(49999,50000)).numerator)/Decimal((P-F(49999,50000)).denominator))
out['exact_product_comparison_passed']=True
print(json.dumps(out,indent=2))
