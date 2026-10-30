"""An exact unrestricted minor-support obstruction on a parameter interval.

This is a non-polyconvexity statement; quasiconvexity outside the admitted
source arcs is not inferred. All interval signs use exact Bernstein values.
"""
from pathlib import Path
from fractions import Fraction as R
from math import comb
import sympy as S
import json

HERE=Path(__file__).resolve().parent
u,t=S.symbols('u t',real=True);a,b,c,d=S.symbols('a b c d',real=True)
H=1+3*u*u;beta=(1-3*u*u)/H;r=4-12*u/H
T=a*a+b*b+c*c+d*d;q=a*d-b*c;X=a*a+c*c-b*b-d*d
F=T*T+4*(r-1)*q*q+4*beta*q*X
A=S.Matrix([1,0,0,1])
rp=S.Matrix([0,1,-2*u,0]);rm=S.Matrix([1,0,0,-2])

def cut(direction):
    expr=S.Poly(S.expand(F.subs(dict(zip((a,b,c,d),direction+t*A)),simultaneous=True)),t)
    c0,c1,c2=(expr.nth(i) for i in range(3))
    det=direction[0]*direction[3]-direction[1]*direction[2]
    return S.factor((c2-c1*c1/(4*c0))/det)

upper=cut(rp);lower=cut(rm);gap=S.factor(lower-upper)
expected=-4*(2817*u**4-2733*u**3+1371*u**2+u-2)/((1+3*u*u)*(147*u*u-192*u+97))
assert S.cancel(gap-expected)==0
assert S.cancel(upper-(24-68*u/H))==0
end=R(1,26)
def bernstein(coeffs):
    n=len(coeffs)-1
    return [sum((R(coeffs[j])*end**j*R(comb(i,j),comb(n,j)) for j in range(i+1)),R(0)) for i in range(n+1)]
num_coeffs=[-2,1,1371,-2733,2817]
den_coeffs=[97,-192,147]
num=bernstein(num_coeffs);den=bernstein(den_coeffs)
assert all(x<0 for x in num) and all(x>0 for x in den)
# The endpoint u=0 uses an actual positive-determinant direction, separately.
endpoint_upper=R(24)+R(8,100)
endpoint_lower=R(2336,97)
assert cut(S.Matrix([0,1,-S.Rational(1,100),0])).subs(u,0)==S.Rational(endpoint_upper.numerator,endpoint_upper.denominator)
assert lower.subs(u,0)==S.Rational(endpoint_lower.numerator,endpoint_lower.denominator)
assert endpoint_lower-endpoint_upper==R(6,2425)>0
out={'nonpc_interval':'0 < u <= 1/26',
     'base_A':['1','0','0','1'],
     'Rplus':['0','1','-2*u','0'],'Rminus':['1','0','0','-2'],
     'upper_bound':str(upper),'lower_bound':str(lower),'strict_support_gap':str(gap),
     'numerator_Bernstein_coefficients':list(map(str,num)),
     'positive_denominator_Bernstein_coefficients':list(map(str,den)),
     'interval_signs_exact':True,
     'endpoint_u0':{'Rplus':['0','1','-1/100','0'],'Rminus':['1','0','0','-2'],
                    'upper':str(endpoint_upper),'lower':str(endpoint_lower),
                    'strict_gap':str(endpoint_lower-endpoint_upper)},
     'scope':'Unrestricted scalar minor-support contradictions. The whole closed interval 0<=u<=1/26 is non-polyconvex; this does not prove its whole quasiconvexity.'}
(HERE/'nonpc_interval_result.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
