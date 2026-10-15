#!/usr/bin/env python3
"""Independent exact polynomial checks for the contact-face audit.

No discovery code, numerical optimizer, or neighboring worker module is read.
The prose proof supplies the finite-dimensional cone and sign arguments.
"""
from pathlib import Path
import hashlib
import json
import sympy as s

ROOT = Path(__file__).resolve().parent
checks = []

def equal(label, lhs, rhs=0):
    value = s.factor(lhs-rhs)
    assert value == 0, (label, value)
    checks.append(label)

def matrix_equal(label, lhs, rhs):
    assert lhs.shape == rhs.shape, label
    for value in lhs-rhs:
        assert s.factor(value) == 0, (label, value)
    checks.append(label)

a,b,c,d,p,q,k,t,r,lam = s.symbols('a b c d p q k t r lambda', real=True)
al,be,ga,de = s.symbols('alpha beta gamma delta', real=True)
x=s.Matrix([a,b,c,d])
u=a*a+c*c
v=b*b+d*d
w=a*b+c*d
j=a*d-b*c
H=(u+v-2*j)**2
I={a:1,b:0,c:0,d:1}
e11=s.Matrix([1,0,0,0])
e12=s.Matrix([0,1,0,0])
e21=s.Matrix([0,0,1,0])
R=s.Matrix([p,q,0,0])

equal('quadratic invariant relation',u*v,w*w+j*j)
equal('H is the fourth power of a linear Euclidean norm',H,((a-d)**2+(b+c)**2)**2)

f=s.symbols('f0:9')
basis=[u*u,v*v,u*v,w*w,u*w,v*w,u*j,v*j,w*j]
G=sum(ff*bb for ff,bb in zip(f,basis))
polys=[s.Poly(bb,a,b,c,d) for bb in basis]
mons=sorted(set(mm for poly in polys for mm,_ in poly.terms()))
coeff_matrix=s.Matrix([[poly.coeff_monomial(mm) for poly in polys] for mm in mons])
assert coeff_matrix.rank()==9
checks.append('nine invariant quartics are independent')

eta=s.symbols('eta0:2', real=True)
xi=s.symbols('xi0:2', real=True)
direction=s.Matrix([eta[0]*xi[0],eta[0]*xi[1],eta[1]*xi[0],eta[1]*xi[1]])
AG=(direction.T*s.hessian(G,x)*direction)[0]
contact={**I,eta[0]:1,eta[1]:0,xi[0]:0,xi[1]:1}
contact_eq=[AG.subs(contact)]+[s.diff(AG,z).subs(contact) for z in [*x,*eta,*xi]]
lin,constant=s.linear_eq_to_matrix(contact_eq,f)
assert lin.rank()==5 and constant==s.zeros(len(contact_eq),1)
sol=(f[0],-f[7]/4,-f[3]-f[7]/2,f[3],0,0,f[6],f[7],0)
assert s.linsolve(contact_eq,f)==s.FiniteSet(sol)
checks.append('full contact and first derivative system has rank five and stated solution')

F=al*H+be*u*u+ga*j*j+de*u*j
face_map={f[0]:al+be,f[1]:al,f[2]:6*al+ga,f[3]:-4*al-ga,
          f[4]:0,f[5]:0,f[6]:-4*al+de,f[7]:-4*al,f[8]:0}
equal('four coefficient representation covers the contact span',G.subs(face_map),F)
HF=s.hessian(F,x)
equal('contact identically vanishes in four parameter span',(e12.T*HF.subs(I)*e12)[0])
acoustic=s.expand((R.T*HF*R)[0]/2)
M=s.hessian(acoustic,x)/2
equal('acoustic matrix representation',acoustic,(x.T*M*x)[0])
tangent=acoustic.subs({a:1,b:-k*t,c:k*t,d:1,p:t,q:1})
equal('first LMI necessary tangent identity',tangent,
      t*t*(6*be+de+2*de*(1-k)+ga*(1-k)**2)+t**4*k*k*(2*be+de))
X,Y=s.symbols('X Y', real=True)
cross=acoustic.subs({a:0,d:0,b:X-Y,c:Y,p:1,q:0})
equal('second LMI necessary anti diagonal identity',cross,
      2*al*X*X-de*X*Y+(2*be+de)*Y*Y)
M1=s.Matrix([[6*be+de,de],[de,ga]])
M2=s.Matrix([[8*al,de],[de,2*be+de]])
equal('second slice is congruent to second LMI',cross,
      (s.Matrix([[X/2,-Y]])*M2*s.Matrix([X/2,-Y]))[0])

sharp={al:3*r/(8*(r+2)),be:r*(r-1)/6,ga:1,de:r}
J=F.subs(sharp)
Ms=M.subs(sharp).applyfunc(s.factor)
P1=M1.subs(sharp)
P2=M2.subs(sharp)
matrix_equal('sharp first LMI outer product',P1,s.Matrix([r,1])*s.Matrix([[r,1]]))
equal('sharp second LMI determinant',P2.det())
matrix_equal('sharp second LMI kernel',P2*s.Matrix([r+2,-3]),s.zeros(2,1))
kernel_eq=list(M1*s.Matrix([1,-r]))+list(M2*s.Matrix([r+2,-3]))
kl,_=s.linear_eq_to_matrix(kernel_eq,[al,be,ga,de])
assert kl.rank()==3
checks.append('sharp coefficient perturbations preserving both block kernels have dimension one')

equal('sharp first acoustic leading minor',Ms[0,0],
      r*((2*r+1)**2*p*p+3*q*q)/(4*(r+2)))
equal('sharp second acoustic leading minor SOS identity',Ms[:2,:2].det(),
      3*r*r*(( (2*r+1)*p*p-3*q*q )**2+12*r*(r+2)*p*p*q*q)/(16*(r+2)**2))
equal('sharp third acoustic leading minor SOS identity',Ms[:3,:3].det(),
      3*q*q*r*r*(( (r+1)*(2*r+1)*p*p-3*q*q )**2
                  +3*r*(5*r+4)*p*p*q*q)/(16*(r+2)**2))
equal('sharp full acoustic determinant',Ms.det(method='domain-ge'),9*p**4*q**4*r**4/16)
M_p0=Ms.subs({p:0,q:1})
M_q0=Ms.subs({p:1,q:0})
matrix_equal('p zero acoustic kernel vector',M_p0*s.Matrix([1,0,0,1]),s.zeros(4,1))
equal('p zero acoustic principal rank three minor',M_p0.extract([0,1,2],[0,1,2]).det(),
      27*r*r/(16*(r+2)**2))
ar=s.Matrix([0,(2*r+1)/3,1,0])
matrix_equal('q zero acoustic kernel vector',M_q0*ar,s.zeros(4,1))
matrix_equal('q zero bc acoustic block outer product',M_q0.extract([1,2],[1,2]),
      r*s.Matrix([3,-2*r-1])*s.Matrix([[3,-2*r-1]])/(12*(r+2)))
equal('q zero ad acoustic block determinant',M_q0.extract([0,3],[0,3]).det(),
      r*(2*r+1)**2/(4*(r+2)))
for expr,name in [(r/(r+2),'ratio'),(r*(r+2),'product'),(r*(5*r+4),'third SOS coefficient')]:
    s0=s.symbols('positive_s',positive=True)
    # Substitution r=-2-s or r=s makes the signs transparent without a numeric grid.
    assert s.factor(expr.subs(r,s0)).is_positive
    assert s.factor(expr.subs(r,-2-s0)).is_positive
    checks.append('positive on both allowed branches: '+name)

HJ=s.hessian(J,x)
Hd=s.hessian(j,x)
forced=(e12.T*(HJ-lam*Hd).subs(I)*e21)[0]
equal('unique determinant support multiplier from zero e12 curvature',forced,lam-r-2)
K=s.Matrix([1,0,0,-r-1])
support_hessian=(HJ-(r+2)*Hd).subs(I)
matrix_equal('polyconvex support Hessian has claimed additional null vector',support_hessian*K,s.zeros(4,1))
DJ=s.Matrix([s.diff(J,z).subs(I) for z in x])
gap=J-J.subs(I)-(DJ.T*(x-s.Matrix([1,0,0,1])))[0]-(r+2)*(j-1-(a+d-2))
expected_gap=J-(r+2)*j-s.Rational(2,3)*r*(r+2)*a+(r+2)*(r+1)/2
equal('explicit forced polyconvex support gap',gap,expected_gap)
path_gap=gap.subs({a:1+t,b:0,c:0,d:1-(r+1)*t})
equal('nonzero cubic support gap exact identity',path_gap,
      -r*(r+2)*t**3/3+(r+2)*(9*r**3+36*r*r+40*r+12)*t**4/24)
equal('cubic support obstruction independent of alpha',
      s.expand((F-(r+2)*j-s.Rational(2,3)*r*(r+2)*a+(r+2)*(r+1)/2)
               .subs({be:r*(r-1)/6,ga:1,de:r,a:1+t,b:0,c:0,d:1-(r+1)*t})).coeff(t,3),
      -r*(r+2)/3)

ell_r=2*acoustic.subs({a:0,b:(2*r+1)/3,c:1,d:0,p:1,q:0})
z=s.Matrix([r+2,-3])
equal('additional contact is second block kernel functional',ell_r,s.Rational(2,9)*(z.T*M2*z)[0])
minimal_map={al:3*de/(8*(r+2)),be:(r-1)*de/6}
matrix_equal('minimal exposed face coefficient equations',
             (M2*z).subs(minimal_map),s.zeros(2,1))
S,T=s.symbols('extra_j2 nonnegative_scale', nonnegative=True)
minimal_full={**minimal_map,de:T*r,ga:T+S}
equal('minimal exposed face polynomial decomposition',
      F.subs(minimal_map).subs({de:T*r,ga:T+S}),T*J+S*j*j)
equal('minimal exposed face first block determinant',
      M1.subs(minimal_map).subs({de:T*r,ga:T+S}).det(),S*T*r*r)
ac_j2=acoustic.subs({al:0,be:0,ga:1,de:0})
equal('j squared acoustic form',2*ac_j2,2*(d*p-c*q)**2)
equal('j squared vanishes on first sharp acoustic kernel',ac_j2.subs({a:1,b:0,c:0,d:1,p:0,q:1}))
equal('j squared vanishes on second sharp acoustic kernel',ac_j2.subs({a:0,b:(2*r+1)/3,c:1,d:0,p:1,q:0}))

n1,n2,x1,x2=s.symbols('n1 n2 x1 x2', real=True)
rank_one={a:x1*n1,b:x1*n2,c:x2*n1,d:x2*n2}
equal('rank one restriction of every sharp ray',J.subs(rank_one),
      (x1*x1+x2*x2)**2*(sharp[al]*(n1*n1+n2*n2)**2+sharp[be]*n1**4))
equal('r one retains anisotropic determinant term',J.subs(r,1),
      (u+v)**2/8+(u-v)*j/2+3*j*j/2)

receipt={'status':'EXACT_PASS','check_count':len(checks),'checks':checks,
 'claims_not_proved_by_symbolic_checker':['historical priority','quasiconvexity of sharp rays',
    'infinite-dimensional integrand extremality'],
 'proof_sha256':hashlib.sha256((ROOT/'STRUCTURAL_PROOF.txt').read_bytes()).hexdigest(),
 'verifier_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
(ROOT/'STRUCTURAL_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
