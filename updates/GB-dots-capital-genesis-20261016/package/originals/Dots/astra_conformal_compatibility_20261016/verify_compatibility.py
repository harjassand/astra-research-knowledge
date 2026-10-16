#!/usr/bin/env python3
"""Exact algebra and compatible-fixture checks. Analytic interpolation is proved
in RESEARCH_REPORT.md, not certified by these finite tests.
Requires Python 3.10+ and SymPy. No optimizer, network, or inherited Gram needed.
Assertions are deliberately not used as acceptance conditions.
"""
from __future__ import annotations
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib, json, sys
import sympy as s
ROOT=Path(__file__).resolve().parent
checks=[]
def check(name: str, condition: bool, detail=None):
    if not bool(condition): raise RuntimeError('FAILED: '+name)
    checks.append({'name':name,'status':'PASS','detail':detail})
    print('PASS',name,flush=True)
def zero(expr): return s.cancel(s.expand(expr))==0

a,b,c,d,r,k=s.symbols('a b c d r k',real=True)
u=a*a+c*c;v=b*b+d*d;j=a*d-b*c
H=(u+v-2*j)**2
alpha=3*r/(8*(r+2));beta=r*(r-1)/6;t=(2*r+1)/3
J=alpha*H+beta*u*u+j*j+r*u*j
sigma=r+1;kap=r*(r+2)/3;q=sigma*a+d
C=s.diff(J,a)+s.diff(J,d)
Qraw=(s.diff(J,a,2)+2*s.diff(J,a,d)+s.diff(J,d,2))/2
check('general conformal quadratic coefficient',zero(Qraw-q*q-kap*c*c-(r+2)*j))
U=2*a*q-(r+2)*a*a+r*c*c-2*b*c
check('general cubic defect decomposition',zero(C-(q*U-kap*a*(a*a+c*c))))
check('cubic vanishes to third order on the formal defect plane',zero(C.subs({c:0,d:-sigma*a})+kap*a**3))
J1=s.expand(J.subs(r,1));C1=s.expand(C.subs(r,1))
check('r=1 cubic coefficients',zero(C1-(a**3+5*a*a*d-4*a*b*c+a*c*c+2*a*d*d-2*b*c*d+c*c*d)))
# Independent acoustic Schur verification, for r>0.
z=s.symbols('z',real=True); xx=s.Matrix([a,b,c,d]); R=s.Matrix([1,z,0,0])
ac=(R.T*s.hessian(J,xx)*R)[0]
M=s.hessian(ac,xx)/2
P=s.Matrix([[1,0,1,0],[0,-1,0,1],[0,1,0,1],[1,0,-1,0]])/2
MM=(P.T*M*P).applyfunc(s.cancel)
Ac=MM[:2,:2]
Ac_expected=s.Matrix([[(r+1)**2/2,-z*(r+1)/2],[-z*(r+1)/2,(3*z*z+r*(r+2))/6]])
check('positive-core conformal acoustic block',all(zero(x) for x in Ac-Ac_expected))
Sch=(MM[2:,2:]-MM[2:,:2]*Ac.inv()*MM[:2,2:]).applyfunc(s.factor)
br=r*(5*r+4)/(24*(r+1)**2);cr=alpha/(r+1)**2
Sch_expected=4*s.Matrix([[(alpha-cr)*z*z+3*(alpha-br),(2*alpha-alpha/(r+1))*z],[(2*alpha-alpha/(r+1))*z,3*alpha*z*z]])
check('positive-core acoustic Schur complement',all(zero(x) for x in Sch-Sch_expected))
check('acoustic determinant and positive parameter factors',zero(Sch.det()-48*alpha*(alpha-cr)*z**4) and zero(Ac.det()-r*(r+1)**2*(r+2)/12) and zero(alpha-cr-3*r*r/(8*(r+1)**2)) and zero(alpha-br-r*(2*r+1)**2/(24*(r+1)**2*(r+2))))
# Pointwise calibration audit with all A,B and all r,k.
e,f,g,h=s.symbols('e f g h',real=True)
B=s.Matrix([[e,f],[g,h]]);A=s.Matrix([[a,b],[c,d]]);V=A-B
ub=e*e+g*g;vb=f*f+h*h;wb=e*f+g*h;jb=e*h-f*g;w=a*b+c*d
Cdef=lambda X:s.Matrix([X[0,0]-X[1,1],X[0,1]+X[1,0]])
cd=Cdef(V*B.adjugate())
check('Gram-difference calibration identity',zero((A.T*A-B.T*B).det()-(j-jb)**2+(cd.T*cd)[0]))
Mk=s.Matrix([[t*t,1-k,2*t],[1-k,1,-2],[2*t,-2,4+2*k+1/alpha]])
Lk=s.Matrix([[t*t*ub+(1-k)*vb+2*t*jb,k*wb],[k*wb,(1-k)*ub+vb-2*jb]])
lam=(2+8*alpha+4*alpha*k)*jb+(r-4*alpha)*ub-4*alpha*vb
subsB={a:e,b:f,c:g,d:h}; JB=J.subs(subsB);DJB=s.Matrix([s.diff(J,x).subs(subsB) for x in xx]);vv=s.Matrix([a-e,b-f,c-g,d-h]);zz=s.Matrix([u-ub,v-vb,j-jb])
res=J-JB-(DJB.T*vv)[0]-lam*V.det()
rhs=alpha*(zz.T*Mk*zz)[0]+2*alpha*k*(w-wb)**2+2*alpha*sum((V[i,:]*Lk*V[i,:].T)[0] for i in range(2))
check('full inherited supporting identity reconstructed',zero(res-rhs))
check('rational calibration minors',all(zero(Mk[:i,:i].det().subs(k,s.Rational(2,3))-target) for i,target in enumerate([t*t,4*r*(r+1)/9,16*(r+1)/27],start=1)))
# Nonpolyconvex-support obstruction at I.
ss=s.symbols('s',real=True)
Ivals={a:1,b:0,c:0,d:1}
VI=s.Matrix([ss,0,0,-(r+1)*ss]);JI=J.subs(Ivals);gradI=s.Matrix([s.diff(J,x).subs(Ivals) for x in xx])
resI=J.subs({a:1+ss,b:0,c:0,d:1-(r+1)*ss})-JI-(gradI.T*VI)[0]-(r+2)*(-sigma*ss*ss)
expected=-r*(r+2)*ss**3/3+(alpha*(r+2)**4+(r+2)*(r+3)/6)*ss**4
check('forced pointwise support has the negative cubic',zero(resI-expected))
# Finite-type algebra: 20 cubic monomials; two independent conditions.
mon=[a**i*b**j0*c**ell*d**(3-i-j0-ell) for i in range(4) for j0 in range(4-i) for ell in range(4-i-j0)]
Sig=s.symbols('sigma',nonzero=True,real=True)
coeff=s.symbols('p0:'+str(len(mon))); PP=sum(ci*mi for ci,mi in zip(coeff,mon))
rest=s.Poly(s.expand(PP.subs({c:0,d:-Sig*a})),a,b)
conditions=s.Matrix([rest.coeff_monomial(b**3),rest.coeff_monomial(a*b*b)])
condM=conditions.jacobian(coeff)
check('cubic compensation selection rule has codimension two',len(mon)==20 and condM.rank()==2,{'dimension':18,'algebraic_part_only':True})
# Local Jacobian identity and convex heat budget.
ax,ay,cx,cy,th,X,Y=s.symbols('ax ay cx cy theta X Y',real=True)
qx=Sig*ax+cy
check('horizontal cubic flux differs by an exact Jacobian',zero(a*ax*qx-a*ay*cx-Sig*a*ax*ax-a*(ax*cy-ay*cx)))
K=(1+th)*a**4/12+a*a*b*b/2+b**4/(3*th)
zz2=s.Matrix([X,Y]);D=s.hessian(K,[a,b])-s.diag(a*a,a*a)
check('convex quartic budget has exact positive-square remainder',zero((zz2.T*D*zz2)[0]-(th*a*a*X*X+4*a*b*X*Y+4*b*b*Y*Y/th+b*b*X*X)))
# One-phase upper bound.
sv,tv=s.symbols('sv tv',real=True)
check('single-wave cubic ratio at most one half',zero((1+tv*tv)*((2+sv*tv)**2+sv*sv)-4*(1+sv*tv)**2-((1-tv*tv)*sv-2*tv)**2))
# Exact trigonometric moments of the selection-rule counterexample.
# Laurent polynomials in e^{ix}, e^{iy} with rational coefficients.
def add(*D):
 out={}
 for dd in D:
  for k0,v0 in dd.items():out[k0]=out.get(k0,F(0))+v0
 return {k0:v0 for k0,v0 in out.items() if v0}
def mul(A0,B0):
 out={}
 for p0,v0 in A0.items():
  for q0,w0 in B0.items():
   k0=(p0[0]+q0[0],p0[1]+q0[1]);out[k0]=out.get(k0,F(0))+v0*w0
 return {k0:v0 for k0,v0 in out.items() if v0}
def scale0(A0,t0):return{k0:v0*t0 for k0,v0 in A0.items()}
def cos0(p0):return{p0:F(1,2),(-p0[0],-p0[1]):F(1,2)}
ca=add(cos0((1,1)),cos0((1,2)))
cb=add(cos0((1,1)),cos0((0,1)),scale0(cos0((1,2)),F(2)))
cc=add(cos0((1,1)),scale0(cos0((1,2)),F(1,2)))
ab2=mul(ca,mul(cb,cb)).get((0,0),F(0));cc2=mul(cc,cc).get((0,0),F(0))
check('actual compatible anisotropic fixture violates the forbidden cubic estimate',ab2==F(3,2) and cc2==F(5,8),{'a_b_squared_mean':str(ab2),'psi_xx_squared_mean':str(cc2),'q':'0','scaling':'a=epsilon*a0,b=b0,c=-sigma*epsilon^2*c0,d=-sigma*a'})
bker=add(cos0((0,1)),cos0((0,2)))
check('the zeroth-order kernel cubic is not compensated',mul(bker,mul(bker,bker)).get((0,0),F(0))==F(3,4))
# Explicit compatible counterexample to the chosen stress-norm contraction.
m=8;n=4
EP=lambda k0:s.binomial(2*k0,k0)/s.Integer(2)**k0
sc=s.Rational(1,256)
F2=EP(2*m)*sc**2;F4=EP(4*m)*sc**4
Fp4=m**4*(4*EP(4*m-2)-4*EP(4*m-1)+EP(4*m))*sc**4
F2Fp2=m**2*(2*EP(4*m-1)-EP(4*m))*sc**4
pressure=(F4-F2**2)/4+F2Fp2/(8*n*n)
fourA=3*F4/16+F2Fp2/(8*n*n)+3*Fp4/(16*n**4)
gap=s.factor(pressure-fourA)
check('exact compatible carrier defeats the canonical sharp stress bound',gap>0,{'gap':str(gap),'pressure_ratio_diagnostic':float(pressure/fourA),'cubic_integral':'0','scope':'stress-norm failure, not a Jensen violation'})
# Exact genuinely compatible P1 resonance fixture; independent recomputation.
path=ROOT/'EXACT_RESONANCE_FIXTURE.json'
data=json.loads(path.read_text());N=data['N'];den=data['node_denominator'];R0=F(data['coordinate_x_scale']);nodes=data['nodes']
field=[[[F(nodes[ii][x][y],den) for y in range(N)] for x in range(N)] for ii in range(2)]
AA=CC=QQ=DJ=F(0);av=[F(0)]*4
for x,y in product(range(N),repeat=2):
 o=[field[ii][x][y] for ii in range(2)];xe=[field[ii][(x+1)%N][y] for ii in range(2)];ye=[field[ii][x][(y+1)%N] for ii in range(2)];xy=[field[ii][(x+1)%N][(y+1)%N] for ii in range(2)]
 for tri in range(2):
  dx=[N*R0*(xe[ii]-o[ii] if tri==0 else xy[ii]-ye[ii]) for ii in range(2)]
  dy=[N*(xy[ii]-xe[ii] if tri==0 else ye[ii]-o[ii]) for ii in range(2)]
  aa,bb,cc,dd=dx[0],dy[0],dx[1],dy[1];uu=aa*aa+cc*cc;jj=aa*dd-bb*cc;qq=2*aa+dd
  AA+=((aa-dd)**2+(bb+cc)**2)**2/8+jj*jj+uu*jj
  CC+=uu*(aa+dd)+2*jj*qq;QQ+=qq*qq+cc*cc;DJ+=jj
  av=[z0+w0 for z0,w0 in zip(av,[aa,bb,cc,dd])]
weight=2*N*N;AA/=weight;CC/=weight;QQ/=weight;DJ/=weight;av=[x/weight for x in av]
rho=CC*CC/(4*AA*QQ);bstar=-CC/(2*QQ);egap=AA-CC*CC/(4*QQ)
check('exact P1 compatibility and moments',DJ==0 and av==[0]*4 and AA==F(data['A4']) and CC==F(data['C3']) and QQ==F(data['Q2']))
check('resonant field exceeds one-wave bound but has positive optimized Jensen energy',F(2,3)<rho<1 and egap>0 and rho==F(data['ratio']) and bstar==F(data['optimized_conformal_background']),{'ratio':str(rho),'ratio_diagnostic':float(rho),'optimized_Jensen_gap':str(egap)})
# Hopf-invariant positivity, useful for the concentration normalization.
check('J1 Hopf quadratic representation',zero(8*J1-((u-v)**2+(2*(a*b+c*d))**2+4*(2*j)**2+2*(u-v)*(2*j))))
receipt={'schema':'astra-conformal-compatibility-exact-checks/1','status':'PASS','groups':len(checks),'checks':checks,'analytic_scope_warning':'Finite checks verify displayed algebra and specified compatible witnesses. The mixed-derivative interpolation, norm theorem, heat integration and density/compactness arguments require the separately written analytic proofs. No sharp all-gradient bound or positive-core QC is certified.','python':sys.version,'sympy':s.__version__,'self_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'fixture_sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
(ROOT/'VERIFICATION_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print('ALL',len(checks),'EXACT GROUPS PASS',flush=True)
