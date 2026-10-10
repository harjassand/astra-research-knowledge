from fractions import Fraction as F
from math import comb,isqrt
import json
m=3;c=F(1,8); t=1000;N=100
A=F(0);B=F(0)
for n in range(N):
 d=F(1,2**(n+1));C=comb(n+3,3)
 P=sum((-1)**(3-j)*comb(3,j)*comb(n,j) for j in range(min(3,n)+1))
 u=t*d/(1+t*d)
 v=t*t*c*C*d*d/((1+t*d)*(1+t*c*d))
 A+=u*((comb(n,3) if n>=3 else 0)+c*C-2)-v*(1+c)
 B+=2*u*P-2*v
scale=10**50;k=isqrt(2*scale*scale)
slo=F(k,4*scale);shi=F(k+1,4*scale)
assert slo*slo<F(1,8)<shi*shi
lo=A+min(B*slo,B*shi);hi=A+max(B*slo,B*shi)
ratio=F(N+4,N+3)**3
err1=F(5*t,2)*(N+3)**3*F(1,2**N)/(1-ratio/2)
err2=t*t*(N+3)**3*F(1,4**N)/(1-ratio/4)
err=err1+err2
assert hi+err < -2
out={'t':t,'m':m,'N':N,'coefficient_interval_float':[float(lo-err),float(hi+err)],'rational_certificate':'upper bound strictly below -2','tail_bound_float':float(err),'square_root_bracket_denominator':str(4*scale),'scope':'Negative second variation of logdet at product vacuum; implies violations for sufficiently small nonzero equal |3> amplitudes, not an entropy violation.'}
print(json.dumps(out,indent=2))
