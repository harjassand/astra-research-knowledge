"""Bounded exact checks for the Cartesian translation development.

Finite algebra only; no optimizer output, source mutation, or formalization
of compactness, multiplier arguments, duality, or Gamma convergence.
"""
from pathlib import Path
import hashlib
import json
import subprocess
import sympy as S

OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[1]
WORK=Path('/Users/harjas/Documents/ChatGPT/ultra/work/astra-capital-direction-transport-20261015')
PIN='b7cada92d2eb304578be5ed974f1e44b10a89928'
records=[]


def zero(expr):
    assert S.cancel(S.expand(expr))==0, expr


def passed(name, **details):
    records.append(dict(name=name,status='PASS',**details))
    print('PASS:',name,flush=True)


eps=S.symbols('epsilon',positive=True)
a0,ax,ay,g0,gx,gy,v0,vx,vy=S.symbols('a0 ax ay g0 gx gy v0 vx vy',real=True)
h=a0-g0
q=eps*v0/(1+eps*g0)
qx=eps*(vx*(1+eps*g0)-eps*v0*gx)/(1+eps*g0)**2
qy=eps*(vy*(1+eps*g0)-eps*v0*gy)/(1+eps*g0)**2
A=S.Matrix([ax,ay,vx,vy])
B=S.Matrix([0,0,(ax-gx)*v0+h*vx,(ay-gy)*v0+h*vy])
C=S.Matrix([0,0,-gx*h*v0-g0*(ax-gx)*v0-g0*h*vx,
              -gy*h*v0-g0*(ay-gy)*v0-g0*h*vy])
Aeps=S.Matrix([ax,ay,vx+q*(ax-gx)+h*qx,vy+q*(ay-gy)+h*qy])
for i in range(4):
    series=S.series(Aeps[i],eps,0,3).removeO()
    zero(series-A[i]-eps*B[i]-eps**2*C[i])
passed('actual boundary-preserving gradient through second order')

z=S.symbols('z0:4',real=True)
pb=S.symbols('b0:4',real=True)
pc=S.symbols('c0:4',real=True)
du0,du1,eta0=S.symbols('du0 du1 eta0',real=True)
Dz=S.Matrix([du0,du1,0,0])
DB=S.Matrix([0,0,v0*du0+eta0*vx,v0*du1+eta0*vy])
mon=[]
for i in range(5):
    for j in range(5-i):
        for k in range(5-i-j):
            ell=4-i-j-k
            mon.append(z[0]**i*z[1]**j*z[2]**k*z[3]**ell)
assert len(mon)==35
for f in mon:
    grad=S.Matrix([S.diff(f,t)for t in z])
    Hess=S.hessian(f,z)
    shifted=S.expand(f.subs({z[i]:z[i]+eps*pb[i]+eps**2*pc[i]for i in range(4)},simultaneous=True))
    zero(shifted.coeff(eps,1)-(grad.dot(S.Matrix(pb))))
    zero(shifted.coeff(eps,2)-(grad.dot(S.Matrix(pc))+(S.Matrix(pb).T*Hess*S.Matrix(pb))[0]/2))
    firstvariation=0
    for i in range(4):
        df_shift=S.expand(grad[i].subs({z[j]:z[j]+eps*pb[j]for j in range(4)},simultaneous=True))
        firstvariation+=df_shift*(Dz[i]+eps*DB[i])
    target=(Dz.T*Hess*S.Matrix(pb))[0]+grad.dot(DB)
    zero(S.expand(firstvariation).coeff(eps,1)-target)
passed('uniform C1 Taylor coefficients for all 35 quartic monomials')

aa,bb,gg,vv=S.symbols('a b g v',real=True)
mass_a=(1+eps*aa)**4*(1+eps**2*vv**2/(1+eps*gg)**2)**2
mass_b=mass_a.subs(aa,bb)
constraint=(mass_a-mass_b)/(4*eps)
series=S.series(constraint,eps,0,4).removeO().expand()
zero(series.coeff(eps,0)-(aa-bb))
zero(series.coeff(eps,1)-S.Rational(3,2)*(aa**2-bb**2))
zero(series.coeff(eps,2)-(aa**3-bb**3+2*vv**2*(aa-bb)))
zero(series.coeff(eps,3)-(S.Rational(1,4)*(aa**4-bb**4)+3*vv**2*(aa**2-bb**2)-4*gg*vv**2*(aa-bb)))
zero(S.diff(constraint,aa)-(1+eps*aa)**3*(1+eps**2*vv**2/(1+eps*gg)**2)**2)
passed('exact normalized mass derivative and first three correction coefficients')

c,d,t=S.symbols('c d t',positive=True)
assert S.simplify((4*c*t**3)*t-c*t**4)==3*c*t**4
opt=(d/(4*c))**S.Rational(1,3)
zero(S.diff(d*S.Symbol('T')-c*S.Symbol('T')**4,S.Symbol('T')).subs(S.Symbol('T'),opt))
zero(d*opt-c*opt**4-S.Rational(3,4)*(1/(4*c))**S.Rational(1,3)*d**S.Rational(4,3))
passed('exact quartic residual conjugate and rate exponents')

xi1,xi2,eta1,eta2,kappa=S.symbols('xi1 xi2 eta1 eta2 kappa',real=True)
F=((xi1-kappa*eta1)**2+(xi2-kappa*eta2)**2)**2+(eta1**2+eta2**2)**2
zero(F.subs({eta1:0,eta2:0})-(xi1**2+xi2**2)**2)
first_derivative=S.Matrix([S.diff(F,xi1),S.diff(F,xi2)])
assert first_derivative.subs({xi1:kappa*eta1,xi2:kappa*eta2})==S.zeros(2,1)
passed('convex sharp family mu1=1 and zero Cartesian mean multiplier')

s,b0,bx,by=S.symbols('s b0 bx by',real=True)
basegrad=S.Matrix([vx,vy])
bgrad=S.Matrix([bx,by])
grad_v2=2*v0*basegrad
grad_vb=v0*bgrad+b0*basegrad
first=s*bgrad-kappa**2*s**3*grad_v2-kappa*s**4*grad_vb
second=basegrad+kappa*s**3*grad_v2+s**4*grad_vb
energy=S.expand(first.dot(first)**2+second.dot(second)**2)
E0=basegrad.dot(basegrad)**2
Bpoint=8*v0*E0
ellpoint=4*basegrad.dot(basegrad)*basegrad.dot(grad_vb)
Hpoint=bgrad.dot(bgrad)**2+ellpoint
zero(energy.coeff(s,0)-E0)
for order in (1,2): zero(energy.coeff(s,order))
zero(energy.coeff(s,3)-kappa*Bpoint)
zero(energy.coeff(s,4)-Hpoint)
zero(energy.coeff(s,5))
for order in (5,6,7): zero(energy.subs(kappa,0).coeff(s,order))
passed('fractional development: epsilon=s^3, order s^3 drift and s^4 response')

etax,etay,etav=S.symbols('etax etay etav',real=True)
grad_veta=S.Matrix([v0*etax+etav*vx,v0*etay+etav*vy])
variation_first=S.Matrix([etax,etay])-kappa*s**3*grad_veta
variation_second=s**3*grad_veta
derivative=S.expand(4*first.dot(first)*first.dot(variation_first)
                    +4*second.dot(second)*second.dot(variation_second))
for order in (0,1,2): zero(derivative.coeff(s,order))
passed('sharp-family mass recovery has energy derivative O(epsilon)')

ma=(1+s**3*(kappa*v0+s*b0))**4*(1+s**6*v0**2)**2
mr=(1+s**3*kappa*v0)**4*(1+s**6*v0**2)**2
mc=S.expand((ma-mr)/(4*s**3))
zero(mc.coeff(s,1)-b0)
zero(mc.coeff(s,2))
zero(mc.coeff(s,3))
zero(mc.coeff(s,4)-3*kappa*v0*b0)
zero(mc.coeff(s,5)-S.Rational(3,2)*b0**2)
passed('exact-mass fractional limit enforces mean-zero response')

x,y=S.symbols('x y',real=True)
v=x*(1-x)*y*(1-y)
grad=S.Matrix([S.diff(v,x),S.diff(v,y)])
norm4=S.expand(grad.dot(grad)**2)


def integral(poly):
    ans=S.Rational(0)
    for (i,j),coefficient in S.Poly(S.expand(poly),x,y).terms():
        ans+=coefficient/S.Rational((i+1)*(j+1))
    return S.factor(ans)


mass1=integral(v)
mass2=integral(v*v)
assert mass1==S.Rational(1,36)
assert mass2==S.Rational(1,900)
btest=v*v-v/25
assert integral(btest)==0
E0_exact=integral(norm4)
A1=integral(v*norm4)
A2=integral(v*v*norm4)
B_exact=8*A1
ell_btest=12*A2-S.Rational(8,25)*A1
assert E0_exact>0 and B_exact>0 and ell_btest!=0
direct_ell=4*integral(grad.dot(grad)*grad.dot(S.Matrix([S.diff(v*btest,x),S.diff(v*btest,y)])))
zero(ell_btest-direct_ell)
passed('exact compatible bump and nonzero constrained stress force',
       E0=str(E0_exact),B=str(B_exact),mean_zero_test_force=str(ell_btest))

head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=WORK,text=True).strip()
assert head==PIN,(head,PIN)
source=ROOT/'sources/direction/DIRECTION_REDUCTION_LIMITS.md'
prior=WORK/'updates/FS-phase-closure-20261015/synthesis/phase_geometry/TRANSLATION_GAUGE_AND_SOFT_OPERATOR.md'
paths=[source,prior,OUT/'PROOF.txt',Path(__file__).resolve()]
receipt={
    'status':'PASS','groups':len(records),'records':records,
    'repo':str(WORK),'verified_pin':head,
    'source_read_scopes':[
        {'path':str(source),'scope':'full file; numbered reread lines 294-565, especially 309-464 and 472-552'},
        {'path':str(prior),'scope':'full file'},
        {'path':str(WORK/'frontier/dossiers/N840.txt'),'scope':'initial dossier and current scope, lines 1-90'},
        {'path':str(WORK/'AGENTS.md'),'scope':'full file'},
        {'path':str(WORK/'00_START_HERE.txt'),'scope':'full file'},
    ],
    'sha256':{str(p):hashlib.sha256(p.read_bytes()).hexdigest()for p in paths},
    'finite_scope':'exact bounded algebra; no formalization of analytic compactness, duality, multiplier or Gamma-development arguments',
    'novelty':'UNKNOWN','external_correctness':'UNKNOWN','source_repo_mutations':'none by this worker',
}
(OUT/'CHECK_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(f'{len(records)} exact check groups passed.',flush=True)
