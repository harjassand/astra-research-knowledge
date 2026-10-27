"""Exact signed-pencil and positive-log constant for index27/4."""
import sympy as s,json
from fractions import Fraction as Q
from functools import lru_cache
from pathlib import Path
z=s.symbols('z',positive=True);n=s.Rational(27,4);a=n-1;b=3*a/(n+3);rho=a/(2*n);cut=3*a/(2*n-3)
w=2*b/(z*(z+b))-a/(z*(z+a));K=s.factor(w-rho/z**2)
expected=-(n-1)**2*(z-1)*((2*n-3)*z-3*n+3)/(2*n*z*z*(n+z-1)*((n+3)*z+3*n-3))
assert s.cancel(K-expected)==0
J=s.factor(K*z*z/(z-1)**2)
apart=-s.Rational(529,648)/(z+s.Rational(23,13))+s.Rational(529,729)/(z+s.Rational(23,4))+s.Rational(529,5832)/(z-1)
assert s.cancel(J-apart)==0
assert -s.Rational(529,648)+s.Rational(529,729)+s.Rational(529,5832)==0
assert cut==s.Rational(23,14)
ratio=(cut+b)**9/((cut+a)**8*(cut-1))
assert ratio==s.Rational(2**8*3**9*23,13**9)
@lru_cache(None)
def ul(q):
 t=(q-1)/(q+1);p=t;out=Q(0);N=12
 for j in range(N):out+=2*p/(2*j+1);p*=t*t
 er=2*t**(2*N+1)/((2*N+1)*(1-t*t));return out,out+er
l2=ul(Q(2))
def logq(q):
 k=0
 while q<1:q*=2;k-=1
 while q>2:q/=2;k+=1
 lo,hi=ul(q)
 return (lo+k*l2[0],hi+k*l2[1]) if k>=0 else (lo+k*l2[1],hi+k*l2[0])
R=Q(2**8*3**9*23,13**9);lo,hi=logq(R);clo=Q(23,54)+Q(529,5832)*lo;chi=Q(23,54)+Q(529,5832)*hi
assert clo>Q(1,64)
assert Q(27,46)*Q(1,64)>Q(1,112)
assert (9-n)/(8*n)==s.Rational(1,24)
assert s.Rational(8,9)*(1-s.Rational(1,24))==(n-1)/n
out={'index':'27/4','positive_kernel_interval':'(1,23/14)','rho':'23/54','exact_c':'23/54+(529/5832)log(115893504/10604499373)','exact_c_lower':'1/64','c_enclosure_diagnostics':[float(clo),float(chi)],'source_floor':'minU>=1/24','white_ratio':'λ>=||main||/23','quantitative_gap_safe_coefficient':'1/112','status':'PASS exact rational identities and logarithm receiving'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
