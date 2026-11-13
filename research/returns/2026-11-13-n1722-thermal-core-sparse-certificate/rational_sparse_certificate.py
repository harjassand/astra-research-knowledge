"""Exact rational checks for the displayed finite sparse-current formula.
This checks constants/scalar consequences, not the contour/flow theorem itself.
"""
from fractions import Fraction as F
from math import factorial,isqrt
from pathlib import Path
import json
# Elementary outward certificates: e^.7>2, e^6>400.
assert sum(F(7,10)**k/factorial(k) for k in range(5))>2
assert sum(F(6)**k/factorial(k) for k in range(16))>400
q=F(1,100)
rho=8*q**4*(121/(1-q)+44*q/(1-q)**2+4*q*(1+q)/(1-q)**3)
assert rho<F(1,100000)
# Source q5=4 exp[-4(2-sqrt5/2)] <59/500, no floating arithmetic.
sqrt5_upper=F(223607,100000);assert sqrt5_upper**2>5
x=4*(2-sqrt5_upper/2)
assert sum(x**k/factorial(k) for k in range(18))>F(2000,59)
q5=F(59,500);a=F(49999,50000)
def ceil_log2(x):
 assert x>=1
 k=0
 while 2**k<x:k+=1
 return k
def ceil(x):return -((-x.numerator)//x.denominator)
rows=[]
for R in [20,40,80,200,1000,10000]:
 theta=F(4);phi=theta/R;L=8*R;n=L*L;K=5*R*R;M=10*R;kappa=F(1)
 r=1
 while 6*n*q5**(2*r)/(1-q5)>F(1,100):r+=1
 u=6*n*q5**(2*r)/(1-q5)
 assert 3*(r+2)<=R and 4*r<L and M<K+1 and u<F(1,2)
 Gamma=8*theta*R/a+8*theta
 q1=ceil_log2(n*M*M);q2=ceil_log2(1/kappa+2*n)
 root1=isqrt(K+1);root2=isqrt(K+1-M)
 # log(1/(1-u))<log2<.7; log2 powers likewise.
 upper=F(7,10)*(q1+6*(M-1)+q2+1)+ceil(Gamma)+2*phi*M-8*theta*(root1+root2)
 assert upper<0
 magnitude=(-upper.numerator)//upper.denominator
 rows.append(dict(R=R,L=L,n=n,r=r,M=M,kappa=str(kappa),rho_upper_exact=str(rho),u_upper_exact=str(u),log_fraction_upper_exact=str(upper),certified_current_fraction_upper=f'exp(-{magnitude})'))
Path(__file__).with_suffix('.json').write_text(json.dumps(rows,indent=2));print(json.dumps(rows,indent=2))
