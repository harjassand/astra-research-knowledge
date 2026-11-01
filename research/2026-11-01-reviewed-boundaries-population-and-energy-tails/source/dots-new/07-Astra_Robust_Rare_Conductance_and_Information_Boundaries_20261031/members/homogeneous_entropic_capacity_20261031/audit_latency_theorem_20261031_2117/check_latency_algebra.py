#!/usr/bin/env python3
"""Independent exact algebra checks; no candidate implementation imported."""
from fractions import Fraction as Q
from pathlib import Path
import hashlib,json
import sympy as S
HERE=Path(__file__).resolve().parent
x,y,u,m,g,K=S.symbols('x y u m g K', positive=True)
v=lambda a:1+(1-a*a)**2
checks=[]
def eq(n,a,b=0):
 assert S.cancel(a-b)==0,(n,S.cancel(a-b));checks.append(n)
def truth(n,a):
 assert a,n;checks.append(n)
eq('barrier expansion',v(x),2-2*x*x+x**4)
eq('well expansion',v(-1+x),1+x*x*(2-x)**2)
eq('longitudinal radial derivative',y*S.diff(v(y),y),4*y*y*(y*y-1))
eq('minimum longitudinal derivative certificate',y*S.diff(v(y),y)+1,(2*y*y-1)**2)
# For a=1/sqrt(u)<=1/4, |x|<=a, barrier x^2<=1/u and
# well |2-x|<=9/4 give 81/(16u)<6/u. Check arithmetic margins.
truth('well constant margin',Q(81,16)<6)
truth('interval ordering at u16',-1+Q(1,4)<-Q(1,4))
truth('well interval fits restricted initial basin',-1+Q(1,4)<=-Q(3,4))
truth('barrier interval fits slab',Q(1,4)<Q(1,2))
truth('initial y range precedes barrier interval',-Q(3,4)<-Q(1,4))
truth('mean exponential penalty',2+6==8)
truth('weighted exponential penalty',8+6==14)
truth('product prefactor',4*2==8)
eq('radial density power',m/2-1-S.Rational(3,2),m/2-S.Rational(5,2))
for dim in range(1,33):
 exponent=Q(dim,2)-Q(5,2)
 truth('divergence threshold m'+str(dim),(exponent>=-1)==(dim>=3))
# Exact Lyapunov drift coefficient for K=3/2, including gamma-inverse weight.
# LV=-2 [y v' + 2K v]u +2+2Km; lower bracket is at least2.
eq('full drift bracket',y*S.diff(v(y),y)+3*v(y),7*y**4-10*y*y+6)
eq('full drift margin certificate',y*S.diff(v(y),y)+3*v(y)-2,7*(y*y-S.Rational(5,7))**2+S.Rational(3,7))
# Frozen one-dimensional candidate t'=-A; A'=u v' A+1, hence Lt=-1.
A=S.symbols('A')
eq('one dimensional generator residual',-(u*S.diff(v(y),y)*A+1)-u*S.diff(v(y),y)*(-A),-1)
# Gaussian homogeneous scalar Jensen asymptotics at the common interior maximum.
f=v(y)/2
j=2/(4-v(y))
eq('R0 normalized maximum',f.subs(y,0),1)
eq('Rplus normalized maximum',j.subs(y,0),1)
eq('R0 log quadratic',S.diff(S.log(f),y,2).subs(y,0)/2,-1)
eq('Rplus log quadratic',S.diff(S.log(j),y,2).subs(y,0)/2,-1)
eq('pointwise Jensen resistance slack',4-v(y)*(4-v(y)),(2-v(y))**2)
# Rational representative checks complement, but do not replace, interval reasoning.
for N in [4,5,8,16,32,64]:
 uu=Q(N*N);a=Q(1,N)
 for numerator in range(-N,N+1):
  xx=Q(numerator,N*N)
  truth('barrier bound '+str((N,numerator)),v(xx)>=2-2/uu)
  truth('well bound '+str((N,numerator)),v(-1+xx)<=1+6/uu)
# Every original source remains at the corrected received hash.
row=json.loads((HERE/'review_inputs.json').read_text())
b=(HERE.parent/row['source']).read_bytes()
truth('corrected source binding',hashlib.sha256(b).hexdigest()==row['accepted_sha256'] and len(b)==row['bytes'])
report={'status':'PASS','exact_assertions':len(checks),'scope':'theorem algebra only; no simulated latency or candidate executable acceptance','checks':checks}
(HERE/'check_results.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='checks'},indent=2))
