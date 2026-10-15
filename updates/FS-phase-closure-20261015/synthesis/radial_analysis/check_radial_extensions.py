"""Independent exact algebra for the new radial analysis.

These checks do not formalize positivity, compactness, the multiplier theorem,
Morrey embedding, weak dual attainment, or the classification's gauge argument.
No supplied verifier output is imported and no supplied file is modified.
"""
from pathlib import Path
import hashlib
import json
import subprocess
import sympy as S

OUT=Path(__file__).resolve().parent
BASE=OUT.parents[1]
SOURCE=BASE/'sources'/'phase_density'
PIN='846f185763ed3a27310fad4ce9471ba324d1e5f4'
REPO=Path('/Users/harjas/Documents/ChatGPT/ultra/work/astra-capital-phase-closure-20261015')
records=[]


def zero(expr):
    assert S.cancel(S.expand(expr))==0, expr


def passed(name, **details):
    records.append(dict(name=name,status='PASS',**details))
    print('PASS:',name,flush=True)


A,L,C,t=S.symbols('A L C t',real=True)
zero(A+L+C-A/3-(3*(L+4*A/3)**2/(8*A)+C-3*L**2/(8*A)))
sharp=(t-S.Rational(1,3))**4
assert S.expand(sharp.subs(t,1)-sharp.subs(t,0)-S.diff(sharp,t).subs(t,0))==S.Rational(1,3)
passed('quartic Bregman completion and exact sharpness example')

x,y=S.symbols('x y',real=True)
r=S.Function('r')(x,y)
j1=S.Function('j1')(x,y)
j2=S.Function('j2')(x,y)
f=S.Function('f')(x,y)
a_dot_j=(S.diff(r,x)*j1+S.diff(r,y)*j2)/r
divj=S.diff(j1,x)+S.diff(j2,y)
radial_euler=-S.diff(r**3*j1,x)-S.diff(r**3*j2,y)+r**3*(4*f-a_dot_j)
zero(radial_euler-4*r**3*(f-a_dot_j-divj/4))
passed('weak radial Euler expression equals constant density dual residual')

eta=S.Function('eta')(x,y)
eps=S.symbols('epsilon',positive=True)
test=eta**4/(r+eps)**3
for coordinate in (x,y):
    zero(S.diff(test,coordinate)-(4*eta**3*S.diff(eta,coordinate)/(r+eps)**3
                                  -3*eta**4*S.diff(r,coordinate)/(r+eps)**4))
passed('legal epsilon reciprocal test differentiation')

w=S.symbols('w',real=True)
w0,w1=1-w,w
zero(w0*w1**4+w1*w0**4-w0*w1*(w0**3+w1**3))
z0,z1=S.symbols('z0 z1',real=True)
zt=w0*z0+w1*z1
zero(w0*(z0-zt)+w1*(z1-zt))
zero(w0*(z0-zt)**4+w1*(z1-zt)**4-w0*w1*(w0**3+w1**3)*(z1-z0)**4)
passed('strict perspective-deficit weights and linear cancellation')

aa,bb,cc,dd=S.symbols('a b c d',real=True)
entries=(aa,bb,cc,dd)
monomials=[]
for i in range(5):
    for j in range(5-i):
        for k in range(5-i-j):
            ell=4-i-j-k
            monomials.append(aa**i*bb**j*cc**k*dd**ell)
for p in monomials:
    zero(p.subs({z:-z for z in entries}, simultaneous=True)-p)
assert len(monomials)==35
passed('quartic sign symmetry for all 35 homogeneous monomials')

alpha,gamma,LL,MM,NN=S.symbols('alpha gamma L M N',real=True)
u=aa*aa+cc*cc
v=bb*bb+dd*dd
ww=aa*bb+cc*dd
q=aa*dd-bb*cc
F=alpha*u*u+gamma*q*q+q*(LL*u+MM*v+NN*ww)
ss,tt,xx,yy,tau=S.symbols('s t X Y tau',real=True)
H=S.Matrix([ss,tt])*S.Matrix([[xx,yy]])
E12=S.Matrix([[0,1],[0,0]])
E11=S.Matrix([[1,0],[0,0]])


def along(poly,base,direction):
    matrix=base+tau*direction
    return S.expand(poly.subs(dict(zip(entries,list(matrix))),simultaneous=True))


c12=along(F,E12,H).coeff(tau,2)
zero(c12-(gamma*xx**2*tt**2-2*MM*xx*yy*ss*tt-NN*xx**2*ss*tt))
q0=S.symbols('q0',real=True)
shear=along(F.subs({MM:0,NN:0}),S.diag(1,q0),S.Matrix([[0,0],[1,0]])).coeff(tau,2)
zero(shear-(2*alpha+LL*q0))
passed('mu classification repair: rank-one point constraints and general-background shear')

bad=F.subs({alpha:1,gamma:1,LL:1,MM:0,NN:0})
c_bad12=along(bad,E12,H).coeff(tau,2)
c_bad11=along(bad,E11,H).coeff(tau,2)
zero(c_bad12-xx**2*tt**2)
zero(c_bad11-((yy*tt+xx*ss)**2+5*xx**2*ss**2+2*xx**2*tt**2))
assert along(bad,S.diag(1,-3),S.Matrix([[0,0],[1,0]])).coeff(tau,2)==-1
passed('exact insufficiency of acoustic checks only at e12 and e11', negative_coefficient='-1')

amp=x
density=x**4
flux=4/(x+eps)**3
conjugate=3/(x+eps)**4
residual=-S.diff(flux,x)/4-conjugate
zero(residual)
primitive=density/(x+eps)**3
zero(S.diff(primitive,x)-(flux*S.diff(density,x)+density*S.diff(flux,x))/4)
boundary=S.simplify(primitive.subs(x,1)-primitive.subs(x,0))
assert boundary==(1+eps)**(-3)
assert S.integrate(amp**4,(x,0,1))==S.Rational(1,5)
assert S.integrate(S.diff(amp,x)**4,(x,0,1))==1
assert S.limit(boundary,eps,0,dir='+')==1
passed('zero-boundary exact primal and smooth dual sequence',mass='1/5',minimum='1',dual_boundary=str(boundary))

zz=S.symbols('z',positive=True)
assert (4*zz**3)*zz-zz**4==3*zz**4
assert S.integrate(x**(-4),(x,S.Symbol('delta',positive=True),1)).has(S.Symbol('delta',positive=True))
passed('Fenchel optimizer and nonintegrable x^-3 flux asymptotic')

G=3*(u+v-2*q)**2+S.Rational(35,24)*u*u+q*q-S.Rational(5,2)*q*u
sa,ta,xb,yb=S.symbols('sa ta xb yb',real=True)
rankone=S.Matrix([sa,ta])*S.Matrix([[xb,yb]])
G_rank=S.expand(G.subs(dict(zip(entries,list(rankone))),simultaneous=True))
target=3*((sa*sa+ta*ta)*(xb*xb+yb*yb))**2+S.Rational(35,24)*(sa*sa+ta*ta)**2*xb**4
zero(G_rank-target)
assert G.subs({aa:0,bb:1,cc:0,dd:0})==3
passed('retained G has exact positive rank-one lower value mu=3')

yy=S.symbols('y',real=True)
phi=S.sin(2*yy)**2
mass_phi=S.integrate(phi**4,(yy,0,S.pi/2))
energy_phi=S.integrate(S.diff(phi,yy)**4,(yy,0,S.pi/2))
assert mass_phi==35*S.pi/256
assert energy_phi==3*S.pi
assert S.simplify(energy_phi/mass_phi)==S.Rational(768,35)<81
passed('exact reduced-phase nonconvexity trial integrals', endpoint_upper='768/35',midpoint_exact='81')

head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip()
assert head==PIN, (head,PIN)
source_files=[SOURCE/'PHASE_DENSITY_COMPATIBILITY.md',SOURCE/'CHECKPOINT.md',SOURCE/'verify_directional_density.py']
local_files=[OUT/'PROOF.txt',OUT/'RESEARCH_REPORT.txt',Path(__file__).resolve()]
receipt={
    'date':'2026-10-15',
    'status':'PASS',
    'check_groups':len(records),
    'records':records,
    'verified_repo':str(REPO),
    'verified_repo_head':head,
    'old_checkout_observed_head':'4201df05f180ecc25ef9c41a9cc53ad41fa8165b',
    'source_sha256':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in source_files},
    'local_sha256':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in local_files},
    'scope':'finite exact algebra only; not formalization of the analytic theorems',
    'historical_novelty':'UNKNOWN',
    'external_mathematical_review':'UNKNOWN',
}
(OUT/'EXACT_CHECK_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(f'{len(records)} check groups passed; receipt saved.',flush=True)
