#!/usr/bin/env python3
"""Exact constants supporting the separate storage/compatibility audit.

Finite algebra only: analytic trace compactness, continuity and law-limit
arguments are supplied in the accompanying proof review.
"""
from pathlib import Path
import json
import hashlib
import sympy as s

root=Path(__file__).resolve().parent
certpath=root.parent/'nonlinear_qc/G_EXACT_HEAT_CERTIFICATE.json'
raw=certpath.read_bytes()
assert hashlib.sha256(raw).hexdigest()=='4004e6144335150a5b3569dfb7b4d0b836f2776497c271e7f31b2faf52830000'
cert=json.loads(raw)
checks=[]
def record(name,detail):
    checks.append({'name':name,'status':'PASS','detail':detail})

a,b,c,d=s.symbols('a b c d',real=True)
xx=(a,b,c,d)
pairs=cert['omega_pair_order']
mons=cert['quadratic_coefficient_order']
idx=pairs.index([0,2])
omega02=sum(s.Rational(co)*xx[i]*xx[j] for co,(i,j) in zip(cert['omega_coefficients'][idx],mons))
cut=s.expand(omega02.subs({b:0,d:0}))
assert s.expand(cut-s.Rational(788811,20000)*a*a-s.Rational(98601,2500)*c*c)==0
y=s.symbols('y',real=True)
circle=cut.subs({a:s.cos(y),c:s.sin(y)})/4
circulation=s.integrate(circle,(y,0,2*s.pi))/(2*s.pi)
assert circulation==s.Rational(1577619,160000)>0
reverse=-cut.subs({a:s.cos(y),c:-s.sin(y)})/4
assert s.integrate(reverse,(y,0,2*s.pi))/(2*s.pi)==-circulation
record('actual primitive circulation',str(circulation))

t,L=s.symbols('t L',positive=True)
return_cost=s.integrate((L**-2+(1-t/L)**2)**2,(t,0,L))
assert s.simplify(return_cost-L**-3-s.Rational(2,3)/L-L/5)==0
assert return_cost.subs(L,1)==s.Rational(28,15)
assert return_cost.subs(L,2)==s.Rational(103,120)
assert return_cost.subs(L,1)>return_cost.subs(L,2)
record('fixed return is not storage',{'unit_width':'28/15','width_two':'103/120'})

I=s.eye(2); J=s.diag(1,-1)
law=[(36*I,s.Rational(1,2594)),(-36*I,s.Rational(1,2594)),(J,s.Rational(648,1297)),(-J,s.Rational(648,1297))]
u,v,j=a*a+c*c,b*b+d*d,a*d-b*c
G=3*(u+v-2*j)**2+s.Rational(35,24)*u*u+j*j-s.Rational(5,2)*j*u
assert sum(p for A,p in law)==1
assert sum((p*A for A,p in law),s.zeros(2))==s.zeros(2)
meanG=sum(p*G.subs({a:A[0,0],b:A[0,1],c:A[1,0],d:A[1,1]}) for A,p in law)
moment=sum(p*sum(x*x for x in A)**2 for A,p in law)
assert meanG==-s.Rational(1350,1297)
assert moment==5184==(6*s.sqrt(2))**4
record('lifted-law fourth moment',{'G_mean':str(meanG),'fourth_moment':str(moment),'L4_norm':'6sqrt(2)'})

derivative_terms=[s.Integer(48),s.Rational(35,6),s.Integer(1),s.Integer(5)]
assert sum(derivative_terms)==s.Rational(359,6)<60
assert s.integrate(60*t**3,(t,0,1))==15
gap=s.Rational(1350,1297)
rzero=gap/(60*19**3)
rall=gap/(60*19**3+15)
assert rzero==s.Rational(45,17792246)
assert rall==s.Rational(90,35585789)
assert 0<rall<rzero<1
record('zero-mean and all-affine W4 radii',{'zero_mean':str(rzero),'all_affine':str(rall),'radial_quartic_constant':15})

ss=s.symbols('s',positive=True)
assert s.simplify(ss**-3*ss**4)==ss
AU=s.symbols('A_U',nonnegative=True)
assert s.simplify(s.sqrt(2*ss)*s.sqrt(AU*ss)-s.sqrt(2*AU)*ss)==0
Mat=s.Matrix([[a,b],[c,d]])
Refl=s.Matrix([[-a,b],[-c,d]])
assert sum(x*x for x in Mat)==sum(x*x for x in Refl)
record('fold modulus scaling and reversal', 'tau=s gives s from the cutoff cost; smooth-base L2 term is linear; first-column reflection preserves derivative norm.')

out={'status':'EXACT_PASS','groups':len(checks),'checks':checks,
     'certificate_sha256':hashlib.sha256(raw).hexdigest(),
     'scope':'Exact constants and finite identities only; independent analytic proof is in SUPPLEMENT_STORAGE_COMPATIBILITY_REVIEW.md; no external certification.'}
root.joinpath('SUPPLEMENT_STORAGE_COMPATIBILITY_CHECKS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='checks'},indent=2))
