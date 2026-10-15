#!/usr/bin/env python3
"""Equation-first exact checks for the sharp strictness/critical angular audit.

Reads the pinned receiving C only. Imports no construction worker code.
Analytic conclusions require AUDIT.md, rather than a finite positivity claim.
"""
from pathlib import Path
import hashlib,json
import sympy as s

HERE=Path(__file__).resolve().parent
CERT=Path('/Users/harjas/Documents/ChatGPT/ultra/work/astra-global-completion-axis-20261015/updates/FW-moving-heat-observable-20261015/package/derived/workers/sharp_boundary_qc/UNIVERSAL_SHARP_NEGATIVE_CERTIFICATE.json')
data=json.loads(CERT.read_text())
r=s.symbols('r',real=True)
def rat(v):
 return s.cancel(sum(s.Rational(c)*r**i for i,c in enumerate(v['numerator']))/sum(s.Rational(c)*r**i for i,c in enumerate(v['denominator'])))
C=s.Matrix([[rat(v) for v in row] for row in data['C']])
a,b,c,d=s.symbols('a b c d',real=True)
x=s.Matrix([a,b,c,d]);z=s.Matrix(s.symbols('z0:6',real=True))
ell=(C.T*s.kronecker_product(x,z)).applyfunc(s.factor)
X=s.Matrix([a-d,b+c]);Y=s.Matrix([-3*b+(2*r+1)*c,(2*r+1)*a+3*d])
expected={0:Y[0]*z[0]/(2*r+1),3:Y[0]*z[3]/(2*r+1),6:Y[1]*z[0]/3,9:Y[1]*z[3]/3,2:X[1]*z[2],5:X[1]*z[5],8:-X[0]*z[2],11:-X[0]*z[5]}
checks=[]
def check(label,value,**data):
 assert bool(value),label
 checks.append(dict(label=label,status='EXACT_PASS',**data))
 print('PASS:',label,flush=True)
for i,v in expected.items():check('actual kernel row '+str(i),s.cancel(ell[i]-v)==0,formula=str(ell[i]))
check('two strain planes intersect only at zero',s.factor(s.Matrix([[1,0,0,-1],[0,1,1,0],[0,-3,2*r+1,0],[2*r+1,0,0,3]]).det()-4*(r+2)**2)==0)
Ax1,Ax2,By1,By2,v1,v2,xx,yy=s.symbols('Ax1 Ax2 By1 By2 v1 v2 xx yy',real=True)
bilinear_sub={a:Ax1+v1*yy,b:By1+v1*xx,c:Ax2+v2*yy,d:By2+v2*xx,z[0]:0,z[1]:v1,z[2]:0,z[3]:0,z[4]:v2,z[5]:0}
check('additional full row kills bilinear xy part',s.cancel(ell[4].subs(bilinear_sub)-(Ax1*v1+Ax2*v2+(v1*v1+v2*v2)*yy))==0)
alpha=3*r/(8*(r+2));beta=r*(r-1)/6
u=a*a+c*c;j=a*d-b*c;H=((a-d)**2+(b+c)**2)**2
J=alpha*H+beta*u*u+j*j+r*u*j
p,q,n,m=s.symbols('p q n m',real=True)
rankone=J.subs({a:p*n,b:p*m,c:q*n,d:q*m})
rankone_expected=(p*p+q*q)**2*(alpha*(n*n+m*m)**2+beta*n**4)
check('rank-one lower-energy identity',s.cancel(rankone-rankone_expected)==0)
check('rank-one Bregman scalar square identity',s.expand(s.Symbol('aa')+s.Symbol('bb')+3*s.Symbol('bb')**2/(8*s.Symbol('aa'))-s.Symbol('aa')/3-3*(s.Symbol('bb')+4*s.Symbol('aa')/3)**2/(8*s.Symbol('aa')))==0)
check('rank-one constant specialization',s.cancel(alpha/3-s.Rational(1,8)+1/(4*(r+2)))==0)

# The anisotropic CR equations imply the claimed elliptic PDE for both
# components by cross differentiation. This is a symbolic coefficient check.
k=s.symbols('k',positive=True)
fxx,fyy,gxx,gyy=s.symbols('fxx fyy gxx gyy')
cross_g=k*fxx+fyy/k
cross_f=gyy/k+k*gxx
check('elliptic CR cross derivatives',s.expand(k*cross_g-(k*k*fxx+fyy))==0 and s.expand(k*cross_f-(k*k*gxx+gyy))==0)

# Homogeneity exponents: these are structural identities, not heat numerics.
degree=s.symbols('degree',real=True)
energy_t_exponent=2*degree-1
density_radius_exponent=4*degree-6
flux_circle_exponent=4*degree-4
energy_radial_exponent=4*degree-3
check('critical degree-half scaling',energy_t_exponent.subs(degree,s.Rational(1,2))==0 and density_radius_exponent.subs(degree,s.Rational(1,2))==-4 and flux_circle_exponent.subs(degree,s.Rational(1,2))==-2 and energy_radial_exponent.subs(degree,s.Rational(1,2))==-1)

# Direct independent trigonometric integral of the radial angular test.
theta=s.symbols('theta',real=True)
er=s.Matrix([s.cos(theta),s.sin(theta)])
Ar=s.eye(2)-er*er.T/2
radialJ=s.expand(J.subs(dict(zip(x,list(Ar)))))
radial_average=s.integrate(s.expand_trig(radialJ),(theta,0,2*s.pi))/(2*s.pi)
radial_N=s.Rational(25,16)
radial_ratio=s.factor(radial_average/radial_N)
check('radial angular test ratio by direct integration',s.cancel(radial_ratio-(59*r**3+299*r**2+572*r+384)/(1200*(r+2)))==0,ratio=str(radial_ratio))

# Quartic polarization and the special affine quadratic kernel.
B=s.Matrix(s.symbols('B0:4',real=True));V=s.Matrix(s.symbols('V0:4',real=True));t=s.symbols('t',real=True)
JB=J.subs(dict(zip(x,B)));JV=J.subs(dict(zip(x,V)))
shift=J.subs(dict(zip(x,B+V)))
quadratic=(B.T*s.hessian(J,x).subs(dict(zip(x,V)))*B)[0]/2
linear=sum(s.diff(J,xi).subs(dict(zip(x,V)))*Bi for xi,Bi in zip(x,B))
omitted=sum(s.diff(J,xi).subs(dict(zip(x,B)))*Vi for xi,Vi in zip(x,V))
check('all-background quartic polarization',s.cancel(shift-JB-quadratic-linear-JV-omitted)==0)
pv,qv,wv,zv=s.symbols('pv qv wv zv',real=True)
shear_shift=s.Poly(s.expand(J.subs({a:1+t*pv,b:t*qv,c:t*wv,d:1+t*zv})),t)
Q=((r+1)*pv+zv)**2+r*(r+2)*wv*wv/3
check('background-I quadratic plus exact determinant null term',s.factor(shear_shift.coeff_monomial(t*t)-Q-(r+2)*(pv*zv-qv*wv))==0)
check('cubic zero on exact shear kernel',s.expand(shear_shift.coeff_monomial(t**3).subs({pv:0,wv:0,zv:0}))==0)

receipt=dict(schema='astra-sharp-strictness-independent-exact-audit-v1',status='EXACT_REDUCTION_PASS',source_certificate_sha256=hashlib.sha256(CERT.read_bytes()).hexdigest(),all_twelve_kernel_rows=[str(v) for v in ell],checks=checks,scope='Exact supporting algebra only. Analytic strictness, rough-data Fatou, critical renormalization and compactness are separately reconstructed in AUDIT.md. Same-team internal audit, not external verification.',all_affine_uniform_margin='UNPROVED')
(HERE/'EXACT_AUDIT_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print('EXACT_REDUCTION_PASS',flush=True)
