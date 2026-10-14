#!/usr/bin/env python3
"""Standalone exact verification of the sharp anisotropic quartic theorem.

Run: python verify_sharp_scalar.py
Dependency: SymPy. No numerical SDP solver, pickle, JSON input, or network is used.
The heat-flow/Stokes passage from this algebra to quasiconvexity is proved in
ASTRA_SHARP_QUARTIC_THEOREM.md. All positivity checks below use rational bounds.
"""
from __future__ import annotations
import itertools
import json
from pathlib import Path
import sympy as s

L=s.Symbol('L',real=True)
mp=48*L**6-2545*L**4+29712*L**2-97344
modulus=s.Poly(mp,L,domain=s.QQ)
left=s.Rational(295538664457927,10**14)
right=s.Rational(295538664457928,10**14)

def reduce_field(expression):
    return s.rem(s.Poly(s.expand(expression),L,domain=s.QQ),modulus).as_expr()

def interval_polynomial(expression,lo=left,hi=right):
    lower=upper=s.Rational(0)
    for coefficient in s.Poly(expression,L,domain=s.QQ).all_coeffs():
        products=(lower*lo,lower*hi,upper*lo,upper*hi)
        lower,upper=min(products)+coefficient,max(products)+coefficient
    return lower,upper

tau0,tau1,tau2,tau3,tau4,tau5=s.symbols('tau0:6',real=True)
taus=(tau0,tau1,tau2,tau3,tau4,tau5)
S=s.Matrix([
[12,10-tau0/2,25-tau0/2-tau4-3*tau5,2*L+tau3,-3*L,-3*L-tau2],
[10-tau0/2,8,tau0/2+tau4+3*tau5-9,2*L+tau2,-L+tau1+tau2,-L],
[25-tau0/2-tau4-3*tau5,tau0/2+tau4+3*tau5-9,tau0,tau1,tau2,tau3],
[2*L+tau3,2*L+tau2,tau1,11-2*tau5,1-tau4,tau4],
[-3*L,-L+tau1+tau2,tau2,1-tau4,7,tau5],
[-3*L-tau2,-L,tau3,tau4,tau5,4]])
tau_values=[
(254064*L**4-12066397*L**2+87457992)/s.Integer(107712),
L*(2551152*L**4-120422989*L**2+869186184)/s.Integer(4582656),
-L*(30008208*L**4-1412052067*L**2+10194361080)/s.Integer(50409216),
L*(2383152*L**4-111980897*L**2+796906920)/s.Integer(3877632),
(64560*L**4-3046321*L**2+22009128)/s.Integer(71808),
-(641424*L**4-30344323*L**2+215742840)/s.Integer(646272)]
Se=S.subs(dict(zip(taus,tau_values))).applyfunc(reduce_field)

assert modulus.is_irreducible
assert mp.subs(L,left)*mp.subs(L,right)<0
assert modulus.count_roots(left,right)==1
assert modulus.count_roots(s.Rational(295,100),s.Rational(296,100))==1
print('PASS: unique specified real algebraic endpoint.',flush=True)
# Exact PSD certificate: positive lower-right block, vanishing Schur complement.
T=Se[2:,2:];B=Se[:2,2:];C=Se[:2,:2]
minor_polynomials=[reduce_field(T[:k,:k].det(method='domain-ge')) for k in range(1,5)]
minor_bounds=[interval_polynomial(p) for p in minor_polynomials]
assert all(lo>0 for lo,hi in minor_bounds)
adjT=T.adjugate().applyfunc(reduce_field)
assert (minor_polynomials[-1]*C-B*adjT*B.T).applyfunc(reduce_field)==s.zeros(2)
print('PASS: four exact positive principal minors and zero Schur complement.',flush=True)
print('Principal-minor enclosures:',[(float(lo),float(hi)) for lo,hi in minor_bounds],flush=True)

# An explicit universal exterior-derivative identity, prior to endpoint substitution.
a,b,c,d=s.symbols('a b c d',real=True)
h0,h1,h2,h3,h4,h5=s.symbols('h0 h1 h2 h3 h4 h5',real=True)
A=s.Matrix([a,b,c,d]);B1=s.Matrix([h0,h1,h3,h4]);B2=s.Matrix([h1,h2,h4,h5])
u=a*a+c*c;v=b*b+d*d;w=a*b+c*d;q=a*d-b*c
F=u*u+v*v+4*w*w+s.Rational(7,2)*q*q+L*q*(u+v)
alpha=s.Matrix([0,
(20-tau0)*a**3/3+(4*L-tau1)*a*a*d+(20-tau0)*a*b*b+(-8*L+2*tau1)*a*b*c+2*tau5*a*c*c+2*tau5*a*d*d,
(-2*L+2*tau3)*a**3/3+(-tau0/2-3*tau5+10)*a*a*d+(-6*L-2*tau2)*a*b*b+(tau0+6*tau5-20)*a*b*c+(-2*L+2*tau3)*a*c*c+(-6*L-2*tau2)*a*d*d+(tau0/2+tau5-10)*b*b*d+(-4*L-2*tau1-4*tau2)*b*c*d,
(-2*L-tau1-2*tau2)*a*a*b+(-tau0/2-tau5+10)*a*a*c+(-tau0-2*tau5+20)*a*b*d+(-4*L-2*tau1-4*tau2)*a*c*d+(-2*L+2*tau3)*b**3/3+(tau0/2+3*tau5-10)*b*b*c+(-6*L-2*tau2)*b*c*c+(-2*L+2*tau3)*b*d*d+(20-tau0)*c**3/3+(20-tau0)*c*d*d])
Da=alpha.jacobian(A)
# Compact geometric primitive, independently compared with the coordinate one.
theta=s.Matrix([-c,-d,a,b])
zeta=s.Matrix([-b,a,-d,c])
theta_a=s.Matrix([-c,d,a,-b])
Acoef=-(6*L+tau1+3*tau2-tau3)/4
Bcoef=-(tau0+4*tau5-20)/2
Ccoef=(20-tau0)/4
Dcoef=L-tau1-tau2
Ecoef=(4*L+tau1+3*tau2+tau3)/4
compact=Acoef*(u+v)*theta+Bcoef*q*theta+Ccoef*(u+v)*zeta+Dcoef*q*zeta+Ecoef*(u-v)*theta_a
Dc=compact.jacobian(A)
assert ((Dc.T-Dc)-(Da.T-Da)).applyfunc(s.expand)==s.zeros(4)
exterior=(B1.T*(Dc.T-Dc)*B2)[0]
print('PASS: compact geometric primitive agrees exactly with the coordinate exterior derivative.',flush=True)
HF=s.hessian(F,A);E=(B1.T*HF*B1+B2.T*HF*B2)[0]
x=s.Matrix([a,c]);y=s.Matrix([b,d]);X=s.Matrix([h0,h3]);Y=s.Matrix([h1,h4]);Z=s.Matrix([h2,h5])
def cross(v,w):return v[0]*w[1]-v[1]*w[0]
zp=s.Matrix([x.dot(X),x.dot(Z),y.dot(Y),cross(x,Y),cross(y,X),cross(y,Z)])
zm=s.Matrix([-y.dot(Z),-y.dot(X),-x.dot(Y),cross(y,Y),cross(x,Z),cross(x,X)])
identity=s.expand(E+exterior-(zp.T*S*zp+zm.T*S*zm)[0])
assert identity==0
print('PASS: universal compatible-jet heat identity, symbolically before specializing L or tau.',flush=True)
assert s.expand(zp.dot(zp)+zm.dot(zm)-(u+v)*(X.dot(X)+Y.dot(Y)+Z.dot(Z)))==0
# Necessity at the same endpoint: exact acoustic null vector.
j=s.Symbol('j',real=True);vL=L*L
jp=(248-21*vL)*(1+j)**2-(64*vL-160)*j
GB=s.groebner([mp,jp],j,L,order='lex',domain=s.QQ)
M=s.Matrix([[12+8*j,16*j,-2*j],[16,8+12*j,-1-3*j],[-2*vL,-vL*(1+3*j),4+7*j]])
rhs=s.Matrix([-3-j,-2,-1]);abc=M.adjugate()*rhs;D=M.det()
assert (M*abc-D*rhs).applyfunc(s.expand)==s.zeros(3,1)
a0,b0,c0=abc
assert s.expand(c0+24*(vL*(j-1)**2+4*j*j-2*j+4))==0
# c0<0 and D>0; together with 0<j<1 this also proves the two forced
# scalar kernel vectors are independent.
fourth=vL*(3+j)*a0+2*vL*j*b0+j*c0+(7+4*j)*D
assert GB.reduce(s.expand(fourth))[1]==0
assert s.expand(D+12*((6*vL-56)*j**3+(vL-4)*j**2+(4*vL-40)*j+vL-32))==0
for expression in [248-21*vL,64*vL-160,(64*vL-160)-4*(248-21*vL)]:
    assert interval_polynomial(expression)[0]>0
k=s.Symbol('k',real=True)
P=s.Matrix([[12+8*k*k,16*k],[16*k,8+12*k*k]])
Zb=s.Matrix([[4+7*k*k,k],[k,7+4*k*k]])
assert s.expand(P.det()-(96*(k*k-s.Rational(1,4))**2+90))==0
assert s.expand(Zb.det()-(28+64*k*k+28*k**4))==0
print('PASS: critical rank-one null identity and strict positive even part.',flush=True)
# Acoustic matrix calculated independently from the quartic Hessian.
bs=s.Matrix([1,k,0,0])
acoustic_expression=s.expand((bs.T*HF*bs)[0])
Mac=s.Matrix([[12+8*k*k,16*k,-2*L*k,L*(3+k*k)],
 [16*k,8+12*k*k,-L*(1+3*k*k),2*L*k],
 [-2*L*k,-L*(1+3*k*k),4+7*k*k,k],
 [L*(3+k*k),2*L*k,k,7+4*k*k,]])
assert s.expand(acoustic_expression-(A.T*Mac*A)[0])==0
print('PASS: acoustic matrix independently differentiated from F_L.',flush=True)
# Interior coercivity decomposition and the known non-polyconvex witness.
N4=(u+v)**2;H3=(u+v)**2+4*w*w
assert s.expand(F.subs(L,0)-(N4/2+H3/2+s.Rational(3,2)*q*q))==0
Fminus=F.subs(L,-s.Rational(29,10));FI=Fminus.subs({a:1,b:0,c:0,d:1});FJ=Fminus.subs({a:1,b:0,c:0,d:-1})
assert FI==-s.Rational(3,10) and FJ==s.Rational(113,10)
assert s.Rational(2,100)*7**4*FI+s.Rational(98,100)*FJ==-s.Rational(833,250)
print('PASS: quantitative interior decomposition and non-polyconvexity witness.',flush=True)
# Auxiliary obstruction to positive input-coordinate transforms of isotropic atoms.
S0,T0,W0,D0,h0s,h1s,h2s,cs=s.symbols('S0 T0 W0 D0 h0s h1s h2s cs',real=True)
linear=h0s*S0+h1s*T0+h2s*W0
atom=linear**2+2*cs*D0*linear+(s.Rational(3,2)*cs**2-s.Rational(1,2)*(h0s**2-h1s**2-h2s**2))*D0**2
assert s.expand(atom-((linear+cs*D0)**2-s.Rational(1,2)*(h0s**2-h1s**2-h2s**2-cs**2)*D0**2))==0
assert s.Rational(5,12)<s.Rational(841,1600)
print('PASS: auxiliary isotropic-atom identity and separating rational inequality.',flush=True)

result={'status':'PASS','root_interval':[str(left),str(right)],
'root_polynomial':str(mp),'universal_polynomial_identity':True,'compact_primitive_identity':True,
'schur_complement_identity':True,'T_minor_bounds':[[str(a),str(b)] for a,b in minor_bounds],
'acoustic_null_identity':True,'acoustic_matrix_direct_differentiation':True,
'interior_decomposition':True,'nonpolyconvex_witness':True,
'limitations':['No formal proof-assistant elaboration','No historical priority clearance','Not the entire left-SO(2) quartic cone']}
Path(__file__).with_name('sharp_scalar_verification.json').write_text(json.dumps(result,indent=2))
# Machine-readable data for independent implementations; not required to run this verifier.
def encode(expression):
    p=s.Poly(reduce_field(expression),L);return [str(p.nth(i)) for i in range(6)]
cert={'field_polynomial_ascending':['-97344','0','29712','0','-2545','0','48'],
'root_interval':[str(left),str(right)],'tau_polynomials_ascending':[encode(t) for t in tau_values],
'S':[[encode(Se[i,j]) for j in range(6)] for i in range(6)],
'T_leading_principal_minors':[encode(m) for m in minor_polynomials]}
Path(__file__).with_name('sharp_scalar_certificate.json').write_text(json.dumps(cert,indent=2))
print('ALL EXACT SHARP-SCALAR CHECKS PASSED.',flush=True)
