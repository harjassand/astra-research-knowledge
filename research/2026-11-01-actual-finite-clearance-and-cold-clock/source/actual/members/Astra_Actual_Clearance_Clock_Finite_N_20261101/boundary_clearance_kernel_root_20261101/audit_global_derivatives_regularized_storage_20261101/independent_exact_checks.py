#!/usr/bin/env python3
"""Source-bound exact algebra and rational certificates; no dependency experiments."""
from pathlib import Path
from fractions import Fraction as F
from math import factorial
import hashlib,json
import sympy as s

HERE=Path(__file__).resolve().parent; ROOT=HERE.parent
EXPECTED={
 'GLOBAL_L_WEIGHTED_CLOCK_DERIVATIVES.md':'20dff0a1775870b93aa81a12bb88125892f242a0986438b3ce9e63e0c4d83ccb',
 'REGULARIZED_WEIGHTED_SOURCE_BUDGET.md':'38973f8baacbadb5c8fdf63cac93e2aed49b7831883cd4c3943aff3e3ac10b2b',
}
hashes={n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in EXPECTED}
assert hashes==EXPECTED

def exp_upper(x,n=6):
    """Positive Taylor terms and geometric bound on the remaining term ratios."""
    x=F(x)
    head=sum((x**i/F(factorial(i)) for i in range(n+1)),F(0))
    return head+(x**(n+1)/F(factorial(n+1)))/(1-x/F(n+2))
assert exp_upper(F(13,16))<F(5,2)
assert exp_upper(F(1))<3

l,z=s.symbols('l z',positive=True)
tail_bl=s.integrate((l+s.Rational(3,4)*z*z)**-3,(z,0,s.oo))
tail_bll=s.integrate(3*(l+s.Rational(3,4)*z*z)**-4,(z,0,s.oo))
assert s.simplify(tail_bl-s.sqrt(3)*s.pi/8*l**s.Rational(-5,2))==0
assert s.simplify(tail_bll-5*s.sqrt(3)*s.pi/16*l**s.Rational(-7,2))==0
mixed_const=s.integrate(s.Rational(1,8)*(s.Rational(1,2)+s.Rational(3,4)*z*z)**-4,(z,0,s.oo))
mixed_linear=s.integrate(s.Rational(3,2)*z*(s.Rational(1,2)+s.Rational(3,4)*z*z)**-4,(z,0,s.oo))
assert s.simplify(mixed_const-5*s.sqrt(6)*s.pi/48)==0
assert mixed_linear==s.Rational(8,3)
assert F(1,4)+F(5,4)+F(8,3)==F(25,6)
assert 3*F(25,6)<13 and 3*12*F(25,6)==150
assert F(3,2)+(F(15,8)+2)*150*F(1,4)==F(2349,16)<148
assert F(45,2)<25 and 25*3<81
assert F(3,2)+3+F(1,2)==5
assert F(1)+F(1,4)==F(5,4)

# Independent literal full-channel reconstruction of regularized storage.
A,B,C,D,E,H,w,L=s.symbols('A B C D E H w L',positive=True)
k=s.Rational(8,5)
rates=[1,A,A*(A-1),A*C,A*(A-1),A*D,A*(A-1),A*E,A*E,2*C*D,C*D,A*B]
deltas=[(1,0,0,0,0),(-1,0,0,0,0),(-1,0,1,0,0),(1,0,-1,0,0),
        (-1,0,0,1,0),(1,0,0,-1,0),(-1,0,0,0,1),(1,0,0,0,-1),
        (-1,0,1,1,-1),(1,0,-1,-1,1),(1,1,-1,-1,0),(-1,-1,1,1,0)]
phi=H*H/w**2
W=H*H*(A/w**2+k/w)
marks=[]
for h in deltas:
 target=H*H*((A+h[0])/(w+h[4])**2+k/(w+h[4]))
 marks.append(s.factor((target-W)/phi))
dp=w*w/(w+1)**2-1
dm=w*w/(w-1)**2-1
ap=w/(w+1);am=w/(w-1)
for h,m in zip(deltas,marks):
 expected=(s.Integer(h[0]) if h[4]==0 else
           h[0]+(A+h[0])*dp-k*ap if h[4]==1 else
           h[0]+(A+h[0])*dm+k*am)
 assert s.factor(m-expected)==0
gw=s.factor(sum(r*m for r,m in zip(rates,marks)))
a2=A*(A-1)
source_gw=(1-A-3*a2+A*(C+D)-A*B+3*C*D)+dp*((A-1)*a2+2*(A+1)*C*D)+2*A*A*E*dm-k*a2*ap-2*k*C*D*ap+2*k*A*E*am
assert s.factor(gw-source_gw)==0
assert s.factor(dm-(2*w-1)/(w-1)**2)==0
assert 3-2*k*s.Rational(100,101)==-s.Rational(17,101)
assert s.expand((1-A-3*a2+A*(C+D)-A*B+3*C*D).subs(D,2*(L-A)-C)-(1+2*A+2*A*L-5*A*A-A*B+3*C*(2*(L-A)-C)))==0

def positive_rational_on_w1000(expr):
    num,den=s.fraction(s.factor(s.together(expr.subs(w,z+1000))))
    assert all(c>=0 for c in s.Poly(num,z).all_coeffs())
    assert all(c>0 for c in s.Poly(den,z).all_coeffs())
    return True
assert positive_rational_on_w1000(s.Rational(5,2)-w*dm)
assert positive_rational_on_w1000(ap-s.Rational(100,101))
assert positive_rational_on_w1000(s.Rational(100,99)-am)
assert positive_rational_on_w1000(2/w+dp)

# Every normalized mark is affine in A. Endpoint checks on 0<=A<=2w
# therefore prove the entire jump bound, including all actual enabled rows.
jump_certificates=[]
for da,de in sorted(set((h[0],h[4]) for h in deltas)):
 m=next(m for h,m in zip(deltas,marks) if (h[0],h[4])==(da,de))
 assert s.diff(m,A,2)==0
 for aa in [0,2*w]:
  assert positive_rational_on_w1000(8-m.subs(A,aa))
  assert positive_rational_on_w1000(8+m.subs(A,aa))
 jump_certificates.append({'delta_A':da,'delta_E':de,'normalized_mark':str(m),
                           'abs_bound_8_for_all_w_ge_1000_and_0_le_A_le_2w':True})
plus=F(1)+2*(2+F(1,1000))+F(8,5)
minus=F(1)+F(5,2)*(2+F(1,1000))+F(8,5)*F(100,99)
assert plus==F(3301,500)<8 and minus==F(301699,39600)<8
drift_cap=(F(2,100000)+F(1,2500)+F(16,495))/F(9,10)
assert drift_cap<F(1,20)
qfull=s.expand(sum(rates))
q_bound=1+A*B+A*(3*L+2*E)+3*C*D
assert s.expand((q_bound-qfull-A*(L-A)-2*A).subs(L,A+(C+D)/2))==0
assert (F(3,5000)+F(2,100))/F(9,10)==F(103,4500)<F(1,20)
assert F(303,17)*F(19,20)>=F(21,20)
assert F(303,17)*F(17,101)==3

t=s.symbols('t',positive=True)
assert all(c>=0 for c in s.Poly(s.expand((s.Rational(2,5)*t**3-4*t).subs(t,z+10)),z).all_coeffs())
bracket=64*(F(4,100)+F(303,17)*4)
assert bracket==F(1940288,425)<4600
freedman=F(4,1)/(2*(4600+F(16,3)))
assert freedman==F(3,6908)>=F(1,2500)
assert 4/(F(19,20)*F(9,10))==F(800,171)
assert 4/F(17,101)==F(404,17)

result={
 'status':'PASS_NO_REPAIR','source_sha256':hashes,
 'scope':'deterministic derivative ceilings and conditional actual stopped source budget only',
 'exp_13_over_16_rational_upper_bound':str(exp_upper(F(13,16))),
 'exp_1_rational_upper_bound':str(exp_upper(F(1))),
 'global_bl_integral':str(tail_bl),'global_bll_integral':str(tail_bll),
 'mixed_constant_tail_integral':str(mixed_const),'mixed_linear_tail_integral':str(mixed_linear),
 'small_l_bee_ceiling':'2349/16',
 'literal_storage_drift_residual':'0',
 'normalized_jump_certificates':jump_certificates,
 'plus_jump_triangle_bound':str(plus),'minus_jump_triangle_bound':str(minus),
 'uniform_drift_cap_coefficient':str(drift_cap),
 'uniform_bracket_over_T3':str(bracket),'freedman_exponent_over_T3':str(freedman),
 'A_occupation_coefficient':'800/171','CD_occupation_coefficient':'404/17',
 'all_assertions_passed':True,
}
(HERE/'INDEPENDENT_EXACT_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
