#!/usr/bin/env python3
"""Verify the sharp anisotropic quartic certificate with exact arithmetic.

Usage: python verify_sharp.py [sharp_certificate.json]
Requires SymPy. No numerical solver, repository files, or network access is used.
The analytic heat-flow/Stokes argument is given in the accompanying research note.
"""
from __future__ import annotations
import itertools
import json
import sys
from pathlib import Path
import sympy as s

BASE=Path(__file__).resolve().parent
source=Path(sys.argv[1]) if len(sys.argv)>1 else BASE/'sharp_certificate.json'
data=json.loads(source.read_text())
L=s.Symbol('L',real=True)
mp=sum(s.Rational(c)*L**i for i,c in enumerate(data['minimal_polynomial_ascending']))
modulus=s.Poly(mp,L,domain=s.QQ)

def field_reduce(expression):
    """Canonical representative in Q[L]/(mp), with exact rational coefficients."""
    return s.rem(s.Poly(s.expand(expression),L,domain=s.QQ),modulus).as_expr()

def decode_poly(coefficients):
    return sum(s.Rational(c)*L**i for i,c in enumerate(coefficients))

def decode_matrix(encoded):
    return s.Matrix([[decode_poly(entry) for entry in row] for row in encoded])

def interval_polynomial(expression,left,right):
    """Outward-exact rational interval enclosure by Horner arithmetic."""
    lo=hi=s.Rational(0)
    for coefficient in s.Poly(expression,L,domain=s.QQ).all_coeffs():
        products=(lo*left,lo*right,hi*left,hi*right)
        lo,hi=min(products)+coefficient,max(products)+coefficient
    return lo,hi

left,right=map(s.Rational,data['root_interval'])
assert s.Rational(295,100)<left<right<s.Rational(296,100)
assert mp.subs(L,left)*mp.subs(L,right)<0
assert modulus.count_roots(left,right)==1
assert modulus.count_roots(s.Rational(295,100),s.Rational(296,100))==1
print('PASS: unique endpoint root is isolated by rational endpoints.',flush=True)
R=decode_matrix(data['R']);T=decode_matrix(data['T']);uu=decode_matrix(data['u']);vv=decode_matrix(data['v'])
assert R.shape==(6,4) and T.shape==(4,4) and uu.shape==vv.shape==(3,1)
assert R[2:,:]==s.eye(4) and T==T.T
weight_u=s.Rational(data['alpha_weight']);weight_v=s.Rational(data['beta_weight'])
assert weight_u>0 and weight_v>0
minor_bounds=[]
for k in range(1,5):
    minor=field_reduce(T[:k,:k].det(method='domain-ge'))
    assert field_reduce(minor-decode_poly(data['T_leading_principal_minors'][k-1]))==0
    lo,hi=interval_polynomial(minor,left,right)
    assert lo>0
    minor_bounds.append([str(lo),str(hi)])
print('PASS: all four leading principal minors of T are strictly positive.',flush=True)
# Only this reduction, not rounded eigenvalues, is used in the positivity proof.
S=(R*T*R.T).applyfunc(field_reduce)
U=(weight_u*uu*uu.T).applyfunc(field_reduce)
V=(weight_v*vv*vv.T).applyfunc(field_reduce)
a,b,c,d=s.symbols('a b c d',real=True)
h0,h1,h2,h3,h4,h5=s.symbols('h0 h1 h2 h3 h4 h5',real=True)
A=s.Matrix([a,b,c,d]);B1=s.Matrix([h0,h1,h3,h4]);B2=s.Matrix([h1,h2,h4,h5])
u=a*a+c*c;v=b*b+d*d;w=a*b+c*d;q=a*d-b*c
F=u*u+v*v+4*w*w+s.Rational(7,2)*q*q+L*q*(u+v)
HF=s.hessian(F,A);E=(B1.T*HF*B1+B2.T*HF*B2)[0]
alpha=s.zeros(4,1)
for term in data['primitive']:
    coeff=decode_poly(term['coefficient'])
    alpha[term['differential_index']]+=coeff*s.prod(A[i] for i in term['monomial_indices'])
Da=alpha.jacobian(A)
exterior=(B1.T*(Da.T-Da)*B2)[0]
x=s.Matrix([a,c]);y=s.Matrix([b,d]);X=s.Matrix([h0,h3]);Y=s.Matrix([h1,h4]);Z=s.Matrix([h2,h5])
def cross(v,w):return v[0]*w[1]-v[1]*w[0]
zp=s.Matrix([x.dot(X),x.dot(Z),y.dot(Y),cross(x,Y),cross(y,X),cross(y,Z)])
zm=s.Matrix([-y.dot(Z),-y.dot(X),-x.dot(Y),cross(y,Y),cross(x,Z),cross(x,X)])
xc=a+s.I*c;yc=b+s.I*d;Xc=h0+s.I*h3;Yc=h1+s.I*h4;Zc=h2+s.I*h5
sp=s.Matrix([xc*Xc+s.I*yc*Zc,xc*Zc+s.I*yc*Xc,yc*Yc+s.I*xc*Yc])
sm=s.Matrix([xc*Xc-s.I*yc*Zc,xc*Zc-s.I*yc*Xc,yc*Yc-s.I*xc*Yc])
spin=lambda z,G:(s.re(z).T*G*s.re(z)+s.im(z).T*G*s.im(z))[0]
squares=(zp.T*S*zp+zm.T*S*zm)[0]+spin(sp,U)+spin(sm,V)
variables=tuple(A)+tuple([h0,h1,h2,h3,h4,h5])
diff=s.Poly(s.expand(E+exterior-squares),*variables)
coefficient_checks=0
for monomial,coefficient in diff.terms():
    assert field_reduce(coefficient)==0,(monomial,coefficient)
    coefficient_checks+=1
print('PASS: full compatible-jet polynomial identity (all coefficients reduced exactly).',flush=True)
# Exact necessity: the critical acoustic matrix has a nonzero null vector.
j=s.Symbol('j',real=True);vL=L**2
jp=(248-21*vL)*(1+j)**2-(64*vL-160)*j
GB=s.groebner([mp,jp],j,L,order='lex',domain=s.QQ)
M=s.Matrix([[12+8*j,16*j,-2*j],[16,8+12*j,-1-3*j],[-2*vL,-vL*(1+3*j),4+7*j]])
rhs=s.Matrix([-3-j,-2,-1]);abc=M.adjugate()*rhs;D=M.det()
assert M*abc==s.expand(D)*rhs or (M*abc-D*rhs).applyfunc(s.expand)==s.zeros(3,1)
a0,b0,c0=abc
fourth=vL*(3+j)*a0+2*vL*j*b0+j*c0+(7+4*j)*D
assert GB.reduce(s.expand(fourth))[1]==0
assert s.expand(D+12*((6*vL-56)*j**3+(vL-4)*j**2+(4*vL-40)*j+vL-32))==0
# 8<vL<9 and 0<j<1 make the bracket <5-23=-18; hence D>216.
znum=248-21*vL;zden=64*vL-160
for expression in [znum,zden,zden-4*znum]:
    assert interval_polynomial(expression,left,right)[0]>0
# The L=0 acoustic matrix is positive definite: two 2x2 blocks.
k=s.Symbol('k',real=True)
P=s.Matrix([[12+8*k*k,16*k],[16*k,8+12*k*k]])
Zblock=s.Matrix([[4+7*k*k,k],[k,7+4*k*k]])
assert s.expand(P.det()-(96*(k*k-s.Rational(1,4))**2+90))==0
assert s.expand(Zblock.det()-(28+64*k*k+28*k**4))==0
print('PASS: exact critical acoustic null vector and strict positivity at L=0.',flush=True)
# F0-.5|A|^4 is explicitly polyconvex. This supplies quantitative interior coercivity.
norm4=(u+v)**2;H3=(u+v)**2+4*w*w
assert s.expand(F.subs(L,0)-(s.Rational(1,2)*norm4+s.Rational(1,2)*H3+s.Rational(3,2)*q*q))==0
print('PASS: quantitative interior polyconvex decomposition.',flush=True)
result={'status':'PASS','arithmetic':'exact rational polynomial arithmetic and rational interval bounds',
'root_interval':[str(left),str(right)],'heat_identity_coefficient_checks':coefficient_checks,
'T_minor_interval_bounds':minor_bounds,'critical_acoustic_identity':True,'interior_decomposition':True,
'not_checked':'Historical novelty, all nine coefficients of the left-SO(2) family, formal proof-assistant elaboration.'}
(BASE/'sharp_verification.json').write_text(json.dumps(result,indent=2))
print('All sharp-family certificate checks passed.',flush=True)
