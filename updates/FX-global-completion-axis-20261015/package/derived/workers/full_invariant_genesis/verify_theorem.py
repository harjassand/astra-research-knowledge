"""Exact algebra for REPORT.md; analytic inequalities still require reading.

No optimization, external packages beyond SymPy, or floating arithmetic.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sympy as s

HERE = Path(__file__).resolve().parent
checks = []


def zero(name, value):
    if isinstance(value, s.MatrixBase):
        entries = list(value)
    elif isinstance(value, (tuple, list)):
        entries = value
    else:
        entries = [value]
    for entry in entries:
        assert s.cancel(s.expand(entry)) == 0, (name, entry)
    checks.append(name)


def equal(name, left, right):
    zero(name, left - right)


def truth(name, statement):
    assert statement, name
    checks.append(name)


a,b,c,d = av = s.symbols('a b c d', real=True)
e,f,p,q = dirs = s.symbols('e f p q', real=True)
alpha,k,ell,m = s.symbols('alpha k ell m', real=True)
u = a*a+c*c
v = b*b+d*d
w = a*b+c*d
j = a*d-b*c
H = s.expand((u+v-2*j)**2)
G = s.expand(k*w*w+ell*v*j+m*v*v)
F = alpha*H+G
x = s.Matrix(av)
R = s.Matrix((e*p,e*q,f*p,f*q))
mon = [u*u,v*v,u*v,w*w,u*w,v*w,u*j,v*j,w*j]
fc = s.symbols('f0:9', real=True)
F9 = sum(ci*mi for ci,mi in zip(fc,mon))
P9 = s.expand((R.T*s.hessian(F9,av)*R)[0]/2)
point = {a:1,b:0,c:0,d:1,e:1,f:0,p:1,q:0}
conditions = [P9.subs(point)] + [s.diff(P9,t).subs(point) for t in av+dirs]
contact_matrix = s.linear_eq_to_matrix(conditions,fc)[0]
truth('contact stationarity rank five', contact_matrix.rank() == 5)

basis = s.Matrix([
    [1,0,0,0],
    [1,0,0,1],
    [6,0,0,0],
    [-4,1,0,0],
    [0,0,0,0],
    [0,0,0,0],
    [-4,0,0,0],
    [-4,0,1,0],
    [0,0,0,0],
])
zero('the four generators satisfy all contact conditions', contact_matrix*basis)
truth('contact generators independent', basis.rank() == 4)
poly_monomials = sorted(set().union(*(set(s.Poly(z,av).monoms()) for z in mon)))
coefficient_matrix = s.Matrix([[s.Poly(z,av).coeff_monomial(nu) for z in mon]
                              for nu in poly_monomials])
truth('nine invariant quartic monomials independent', coefficient_matrix.rank() == 9)
for index, generator in enumerate((H,w*w,v*j,v*v)):
    equal('generator reconstruction '+str(index),
          sum(basis[row,index]*mon[row] for row in range(9)),generator)

PI = s.expand((R.T*s.hessian(G,av)*R)[0].subs({a:1,b:0,c:0,d:1})/2)
L = ell+2*m
D = 2*k*m-k*ell-ell*ell
tau = 2*k+L
PI_expected = k*f*f*p*p+2*e*f*(k+ell)*p*q+((k+L)*e*e+3*L*f*f)*q*q
equal('all-direction conformal acoustic identity',PI,PI_expected)
acoustic_2 = s.hessian(PI,(p,q))/2
equal('conformal acoustic determinant',acoustic_2.det(),f*f*(D*e*e+3*k*L*f*f))
equal('H Hessian zero on conformal I',s.hessian(H,av).subs({a:1,b:0,c:0,d:1}),s.zeros(4))

eps,z = s.symbols('epsilon z',real=True)
e22 = s.Matrix((0,0,0,1))
Pe22 = s.expand((e22.T*s.hessian(F,av)*e22)[0]/2)
L_boundary = Pe22.subs({a:1+eps,b:0,c:0,d:1-eps}).subs(m,-ell/2)
equal('L zero boundary exact acoustic obstruction',L_boundary,6*ell*eps+(24*alpha-6*ell)*eps*eps)

Rz = s.Matrix((1,z*k,-z*(k+ell),-z*z*k*(k+ell)))
equal('D zero curve rank one',Rz[0]*Rz[3]-Rz[1]*Rz[2],0)
Pz = s.expand((Rz.T*s.hessian(F,av)*Rz)[0]/2)
D_boundary = s.expand(Pz.subs({a:1,b:-z*z/2,c:-z*z/2,d:1}).subs(m,ell*(k+ell)/(2*k)))
for degree in (0,1,2):
    equal('D zero curve coefficient '+str(degree),D_boundary.coeff(z,degree),0)
equal('D zero curve negative cubic',D_boundary.coeff(z,3),-2*k*k)
PzI = s.expand(Pz.subs({a:1,b:0,c:0,d:1}).subs(m,ell*(k+ell)/(2*k)))
equal('D zero acoustic quartic at I',PzI,3*k*ell*(k+ell)**2*(2*k+ell)*z**4)
gradient_linear = [s.expand(s.diff(Pz,t).subs({a:1,b:0,c:0,d:1})).coeff(z,1)
                   for t in av]
zero('D zero gradient coefficient explanation',
     [s.cancel(gradient_linear[i].subs(m,ell*(k+ell)/(2*k))-expected)
      for i,expected in enumerate((0,2*k*k,2*k*k,0))])

xa,xb,xc,xd = xv = s.symbols('xa xb xc xd',real=True)
X = s.Matrix(xv)
detX = xa*xd-xb*xc
Q = (k+L)*xb*xb+2*(k+ell)*xb*xc+k*xc*xc+3*L*xd*xd
quadratic = (X.T*s.hessian(G,av).subs({a:1,b:0,c:0,d:1})*X)[0]/2
equal('controlled quadratic form modulo determinant',quadratic-3*ell*detX,Q)
Kbc = s.Matrix(((k+L,k+ell),(k+ell,k)))
equal('controlled two-dimensional determinant',Kbc.det(),D)
equal('controlled two-dimensional trace',s.trace(Kbc),tau)
kappa = 3*L*D/(D+3*L*tau)
equal('positive kappa harmonic formula',1/kappa,1/(3*L)+tau/D)
equal('kappa less than determinant over trace',D/tau-kappa,D*D/(tau*(D+3*L*tau)))
equal('kappa less than d coefficient',3*L-kappa,9*L*L*tau/(D+3*L*tau))

er = s.Matrix(s.symbols('ea eb ec ed',real=True))
cubic_stationarity = sum(s.diff(G,a,a,t).subs({a:1,b:0,c:0,d:1})*er[i]
                         for i,t in enumerate(av))
equal('contact cubic tensor flatness for every E',cubic_stationarity,0)
Gcoeffs = s.Poly(G,av).coeffs()
truth('expanded G has ten separate monomials',len(Gcoeffs)==10)
truth('polarization coefficient pattern',
      sorted(map(str,Gcoeffs)) == sorted(map(str,[k,2*k,k,ell,ell,-ell,-ell,m,2*m,m])))

u1,u2,v1,v2 = s.symbols('u1 u2 v1 v2',real=True)
un=u1*u1+u2*u2
vn=v1*v1+v2*v2
dot=u1*v1+u2*v2
gap=((u1+v1)**2+(u2+v2)**2)**2-un*un-4*un*dot
equal('joint quadratic-quartic H Bregman identity',gap-un*vn-vn*vn/5,
      5*(dot+s.Rational(2,5)*vn)**2+un*vn-dot*dot)
equal('one-third quartic H Bregman identity',gap-vn*vn/3,
      6*(dot+vn/3)**2+2*(un*vn-dot*dot))
equal('C norm squared and determinant identity',(xa-xd)**2+(xb+xc)**2,
      xa*xa+xb*xb+xc*xc+xd*xd-2*detX)
hh,tt = s.symbols('hh tt',real=True)
equal('anticonformal normalization',(2*hh)**2+(2*tt)**2,2*(2*hh*hh+2*tt*tt))

MM,kk = s.symbols('M kappa',positive=True)
A0=2592*MM*MM/kk+8*MM
B0=512*MM*MM/kk+3*MM
K4=s.Rational(625,4)
alpha_star=401296*MM*MM/kk+s.Rational(9391,4)*MM
equal('explicit completion constant arithmetic',alpha_star,A0/2+5*K4*B0)
equal('Beurling to C L4 constant',(s.Rational(25,2))**2,K4)
equal('gradient margin constant',s.Rational(1,3)/K4,s.Rational(4,1875))
equal('strict contact-set coefficient at sufficient alpha',
      2*alpha_star-2592*MM*MM/kk-6*MM,
      800000*MM*MM/kk+s.Rational(9379,2)*MM)
equal('rank-one C norm identity',
      ((e*p-f*q)**2+(e*q+f*p)**2),
      (e*e+f*f)*(p*p+q*q))
CB=s.Matrix((a-d,b+c))
CR=s.Matrix((e*p-f*q,e*q+f*p))
equal('H acoustic exact derivative',
      (R.T*s.hessian(H,av)*R)[0]/2,
      2*(CB.dot(CB))*(CR.dot(CR))+4*(CB.dot(CR))**2)

example={k:s.Integer(1),ell:s.Integer(-1),m:s.Rational(3,4)}
equal('example L',L.subs(example),s.Rational(1,2))
equal('example D',D.subs(example),s.Rational(3,2))
equal('example kappa',kappa.subs(example),s.Rational(3,7))
example_M=s.Integer(11)
example_alpha=s.cancel(alpha_star.subs({MM:example_M,kk:s.Rational(3,7)}))
equal('example exact sufficient alpha',example_alpha,s.Rational(1359900751,12))
integer_alpha=s.Integer(113325063)
equal('example H reserve',integer_alpha-example_alpha,s.Rational(5,12))
equal('example Jensen margin',(integer_alpha-example_alpha)*s.Rational(4,1875),s.Rational(1,1125))
FI=F.subs({a:1,b:0,c:0,d:1}).subs(example)
equal('example negative value at I',FI,-s.Rational(1,4))
acousticF=(R.T*s.hessian(F,av)*R)[0]
equal('example e11 contact',acousticF.subs(point).subs(example),0)
equal('example outside inherited shear face',
      acousticF.subs({a:1,b:0,c:0,d:1,e:1,f:0,p:0,q:1}).subs(example),3)

receipt={
    'status':'PASS',
    'scope':'Exact symbolic identities and rational constant checks only; analytic proof is REPORT.md and is not formally verified.',
    'checks':checks,
    'check_count':len(checks),
    'example':{
        'k':'1','ell':'-1','m':'3/4','alpha':'113325063',
        'sufficient_alpha':'1359900751/12','gradient_margin':'1/1125',
        'F_at_I':'-1/4',
    },
    'report_sha256':hashlib.sha256((HERE/'REPORT.md').read_bytes()).hexdigest(),
    'verifier_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'sympy_version':s.__version__,
}
(HERE/'EXACT_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({'status':'PASS','check_count':len(checks),'receipt':str(HERE/'EXACT_RECEIPT.json')},indent=2))
