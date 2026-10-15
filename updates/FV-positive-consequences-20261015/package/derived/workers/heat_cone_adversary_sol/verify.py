"""Exact verifier: no numerical search, numerical eigenvalues, or solver imports."""
from pathlib import Path
from itertools import combinations,combinations_with_replacement
import hashlib,json
import sympy as S

OUT=Path(__file__).resolve().parent
a,b,c,d=X=S.symbols('a b c d',real=True)
z=S.symbols('z0:6',real=True)
B1=S.Matrix([z[0],z[1],z[3],z[4]])
B2=S.Matrix([z[1],z[2],z[4],z[5]])
Z=S.Matrix([x*zz for x in X for zz in z])
u=a*a+c*c;v=b*b+d*d;w=a*b+c*d;j=a*d-b*c;ss=u+v
p=S.symbols('p0:9',real=True)
fb=[u*u,v*v,u*v,w*w,u*w,v*w,j*u,j*v,j*w]
F=sum(x*y for x,y in zip(p,fb))
M11=S.Matrix([[12*p[0],3*p[4],0,3*p[6]],[3*p[4],2*p[2]+2*p[3],-p[6],p[8]],[0,-p[6],4*p[0],p[4]],[3*p[6],p[8],p[4],2*p[2]]])
M12=S.Matrix([[3*p[4],2*p[2]+2*p[3],-p[6],p[8]],[2*p[2]+2*p[3],3*p[5],-p[8],p[7]],[-p[6],-p[8],p[4],p[3]],[p[8],p[7],p[3],p[5]]])
M22=S.Matrix([[2*p[2]+2*p[3],3*p[5],-p[8],p[7]],[3*p[5],12*p[1],-3*p[7],0],[-p[8],-3*p[7],2*p[2],p[5]],[p[7],0,p[5],4*p[1]]])
assert M11==S.hessian(S.diff(F,a,2),X)/2
assert M12==S.hessian(S.diff(F,a,b),X)/2
assert M22==S.hessian(S.diff(F,b,2),X)/2
eta,t=S.symbols('eta t')
R=S.Matrix([eta,t,0,0]);HF=S.hessian(F,X)
assert S.expand((R.T*HF*R)[0]-(S.Matrix(X).T*(eta**2*M11+2*eta*t*M12+t**2*M22)*S.Matrix(X))[0])==0
groups=['all-nine-coefficient acoustic identity']

exps=[q for q in __import__('itertools').product(range(5),repeat=4) if sum(q)==4]
mons=[S.prod(x**n for x,n in zip(X,q)) for q in exps]
VL=S.Matrix([-c,-d,a,b])
Lie=S.Matrix([[S.Poly(S.expand(sum(VL[i]*S.diff(m,X[i]) for i in range(4))),*X).coeff_monomial(n) for m in mons] for n in mons])
assert len(mons)-Lie.rank()==9
assert S.Matrix([[S.Poly(f,*X).coeff_monomial(m) for f in fb] for m in mons]).rank()==9
assert all(S.expand(sum(VL[i]*S.diff(f,X[i]) for i in range(4)))==0 for f in fb)
groups.append('complete invariant dimension nine')

zero_face={p[0]:0,p[1]:0,p[3]:-p[2],p[4]:0,p[5]:0}
assert M11.subs(zero_face)==S.Matrix([[0,0,0,3*p[6]],[0,0,-p[6],p[8]],[0,-p[6],0,0],[3*p[6],p[8],0,2*p[2]]])
assert M22.subs(zero_face)==S.Matrix([[0,0,-p[8],p[7]],[0,0,-3*p[7],0],[-p[8],-3*p[7],2*p[2],0],[p[7],0,0,0]])
groups.append('zero rank-one-average face identities')

alpha,beta,k,l=S.symbols('alpha beta k l',real=True)
Fn=alpha*ss**2+beta*j*j
theta=S.Matrix([-c,-d,a,b]);zeta=S.Matrix([-b,a,-d,c])
primitive=k*ss*zeta+l*j*theta
omega=S.Matrix(4,4,lambda i,h:S.diff(primitive[h],X[i])-S.diff(primitive[i],X[h]))
for i,h,n in combinations(range(4),3):
    assert S.expand(S.diff(omega[h,n],X[i])-S.diff(omega[i,n],X[h])+S.diff(omega[i,h],X[n]))==0
H=S.hessian(Fn,X)
density=S.expand((B1.T*H*B1)[0]+(B2.T*H*B2)[0]+(B1.T*omega*B2)[0])
h=S.sqrt(3);star=12+8*h
ell=S.Matrix([
 (h-1)*a*z[3]/2+(h+1)*a*z[5]/2-b*z[4]+(1-h)*c*z[0]/2-(1+h)*c*z[2]/2+d*z[1],
 (1+h)*a*z[4]-(2+h)*b*z[3]-b*z[5]-(1+h)*c*z[1]+(2+h)*d*z[0]+d*z[2],
 (3-h)*a*z[0]/2+(1-h)*a*z[2]/2+b*z[1]+(3-h)*c*z[3]/2+(1-h)*c*z[5]/2+d*z[4],
 (3+h)*a*z[1]/3-h*b*z[0]/3+b*z[2]+(3+h)*c*z[4]/3-h*d*z[3]/3+d*z[5]])
G=S.diag(16+8*h,4,16+8*h,12)
assert all(G[i,i]>0 for i in range(4))
assert S.expand((ell.T*G*ell)[0]-density.subs({alpha:1,beta:star,k:-2*h,l:-16-12*h}))==0
assert 16-8*h>0
groups.append('closed endpoint primitive and four-square identity')

def val(A,zz):
    return S.expand(density.subs(dict(zip(X,A))).subs(dict(zip(z,zz))))
q0=val([1,0,0,0],[1,0,h,0,0,0])
q1=val([1,0,0,0],[0,0,0,-2-h,0,1])
q2=val([1,0,0,1],[1,0,-1,0,-1,0])
assert S.simplify((1+2*h/3)*q0+q1+(2+h)/4*q2-2*(1+h)*(star*alpha-beta))==0
assert star-26<0 and star-25>0
groups.append('three-evaluation exact dual and rational F26 exclusion')

cert_path=OUT/'F25_EXACT_HEAT_CERTIFICATE.json'
data=json.loads(cert_path.read_text())
C=S.Matrix(data['basis']).applyfunc(S.Rational)
T=S.Matrix(data['reduced_gram']).applyfunc(S.Rational)
Q=S.Matrix(data['gram']).applyfunc(S.Rational)
assert T.is_diagonal() and all(T[i,i]>0 for i in range(T.rows))
assert C.rank()==data['rank']==8
assert C*T*C.T==Q
assert list(T.diagonal())==list(map(S.Rational,data['ldl_diagonal']))
assert S.Poly(S.expand((Z.T*Q*Z)[0]-density.subs({alpha:1,beta:25,k:-S.Rational(13,4),l:-S.Rational(71,2)})),*X,*z).is_zero
assert S.expand(sum(S.Rational(ci)*fi for ci,fi in zip(data['coefficients'],fb))-ss**2-25*j*j)==0
groups.append('portable rational F25 rank-eight LDL and full identity')

# Complete correction-space calculation, independent of any candidate search.
pairs=list(combinations(range(4),2));qmons=list(combinations_with_replacement(range(4),2))
q=S.symbols('q0:60');W=S.zeros(4,4)
for n,(i,t0) in enumerate(pairs):
    W[i,t0]=sum(q[10*n+m]*X[r]*X[s] for m,(r,s) in enumerate(qmons));W[t0,i]=-W[i,t0]
eq=[]
for i,t0,r in combinations(range(4),3):
    eq+=S.Poly(S.diff(W[t0,r],X[i])-S.diff(W[i,r],X[t0])+S.diff(W[i,t0],X[r]),*X).coeffs()
for V in [VL,S.Matrix([-b,a,-d,c])]:
    DV=V.jacobian(X)
    LW=W.applyfunc(lambda f:sum(V[i]*S.diff(f,X[i]) for i in range(4)))+DV.T*W+W*DV
    for i,t0 in pairs:eq+=S.Poly(S.expand(LW[i,t0]),*X).coeffs()
for signs,parity in [([1,1,-1,-1],1),([1,-1,1,-1],-1)]:
    for n,(i,t0) in enumerate(pairs):
        for m,(r,s) in enumerate(qmons):
            fact=signs[i]*signs[t0]*signs[r]*signs[s]-parity
            if fact:eq.append(fact*q[10*n+m])
E,_=S.linear_eq_to_matrix(eq,q)
assert E.rank()==58
for WW in [omega.diff(k),omega.diff(l)]:
    cv=S.Matrix([S.Poly(S.expand(WW[i,t0]),*X).coeff_monomial(X[r]*X[s]) for i,t0 in pairs for r,s in qmons])
    assert E*cv==S.zeros(E.rows,1)
groups.append('complete averaged closed quadratic correction dimension two')

# Convex lower endpoint Hessian: an identity in arbitrary A,H.
hh=S.symbols('h0:4',real=True);HH=S.Matrix(2,2,hh);AA=S.Matrix([[a,b],[c,d]])
lower=ss**2-2*j*j
hv=S.Matrix(hh)
rhs=2*S.trace((HH.T*AA+AA.T*HH)**2)+4*S.trace(AA.T*AA*HH.T*HH)
assert S.expand((hv.T*S.hessian(lower,X)*hv)[0]-rhs)==0
groups.append('convex lower endpoint Hessian identity')

coef_alpha=(3*(p[0]+p[1])+p[2]+p[3])/8
coef_beta=(-p[0]-p[1]+p[2]-p[3])/2
Lf=(5+3*h)*(p[0]+p[1])+(1+h)*p[2]+(2+h)*p[3]
assert S.expand(star*coef_alpha-coef_beta-Lf)==0
groups.append('full isotropic-heat coefficient separator')

tt=S.symbols('t',real=True)
Gsource=3*(ss-2*j)**2+S.Rational(35,24)*u*u+j*j-S.Rational(5,2)*j*u
At={a:1,b:S.Rational(3,2)*tt,c:-S.Rational(3,2)*tt,d:1}
Rt=S.Matrix([tt,1,0,0])
assert S.expand((Rt.T*S.hessian(Gsource,X)*Rt)[0].subs(At)-S.Rational(15,8)*tt**4)==0
assert S.expand((Rt.T*S.hessian(j*j,X)*Rt)[0].subs(At)-S.Rational(25,2)*tt**2)==0
groups.append('G zero determinant-extraction rank-one family')

receipt={'status':'EXACT_ALGEBRA_PASS','groups':groups,'count':len(groups),
 'F25_certificate_sha256':hashlib.sha256(cert_path.read_bytes()).hexdigest(),
 'scope':'Exact algebra only. Symmetry averaging, established Calderon theorem, heat analytic implication and polyconvex support equivalence are proved or cited separately. No full-cone QC or heat-plus-PC inclusion follows.',
 'external_review':'UNKNOWN','historical_novelty':'UNKNOWN'}
(OUT/'VERIFICATION.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
