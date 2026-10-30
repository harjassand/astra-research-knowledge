"""Exact local receiver for REPORT.md. Requires the already installed SymPy.
No source files are modified and no network or external services are used.
"""
import sympy as s
from itertools import combinations

x1,x2,y1,y2=s.symbols('x1 x2 y1 y2',real=True)
Z=[x1,x2,y1,y2]; x=s.Matrix(Z[:2]);y=s.Matrix(Z[2:]); N=x.dot(x)-y.dot(y)
eta=lambda z:s.Matrix([z[0]**2-z[1]**2,2*z[0]*z[1]])
J=s.Matrix([[0,-1],[1,0]])
F0=2*x.dot(x)*y.dot(y)+y.dot(y)**2
mons=[x1**i*x2**j*y1**k*y2**(3-i-j-k) for i in range(4) for j in range(4-i) for k in range(4-i-j)]
def acoustic(C):
    op=2*x1*s.diff(C,x1)+2*x2*s.diff(C,x2)-y1*s.diff(C,y1)-y2*s.diff(C,y2)
    return s.rem(op,N,*Z)
images=[s.Poly(acoustic(C),*Z) for C in mons]
keys=sorted(set().union(*(p.monoms() for p in images)))
CM=s.Matrix([[p.coeff_monomial(k) for p in images] for k in keys])
assert CM.rank()==12
basis=[x[i]*y.dot(y) for i in range(2)]+[y[i]*(x.dot(x)+y.dot(y)) for i in range(2)]+[x[i]*eta(y)[j] for i in range(2) for j in range(2)]
assert all(acoustic(C)==0 for C in basis)
BM=s.Matrix([[s.Poly(C,*Z).coeff_monomial(k) for C in basis] for k in [s.Poly(m,*Z).monoms()[0] for m in mons]])
assert BM.rank()==8
print('PASS: full cubic acoustic map rank 12; explicit kernel basis rank 8.')

u1,u2,v1,v2=s.symbols('u1 u2 v1 v2',real=True)
u=s.Matrix([u1,u2]);v=s.Matrix([v1,v2]);rr=u.col_join(v)
m11,m12,m21,m22=s.symbols('m11 m12 m21 m22',real=True)
M=s.Matrix([[m11,m12],[m21,m22]]);C=(x.T*M*eta(y))[0]
H=s.hessian(F0,Z);HC=s.hessian(C,Z)
xi1,xi2,t,z=s.symbols('xi1 xi2 t z',real=True);xi=s.Matrix([xi1,xi2])
base=list(xi-2*t*u)+list(t*v+z*J*v)
sub=dict(zip(Z,base))
G=s.groebner([u1*u1+u2*u2-1,v1*v1+v2*v2-1],u1,u2,v1,v2,xi1,xi2,t,z,m11,m12,m21,m22)
red=lambda e:G.reduce(s.expand(e))[1]
assert red((rr.T*H*rr)[0].subs(sub,simultaneous=True)-4*xi.dot(xi)-8*z*z)==0
assert red((rr.T*HC*rr)[0].subs(sub,simultaneous=True)-2*(xi.T*M*eta(v))[0]-4*z*(u.T*M*J*eta(v))[0])==0
print('PASS: exact normalized rank-one Hessian and completed-square coefficients.')

slope=s.symbols('slope',real=True)
def nonnegative(poly):
    p=s.Poly(s.expand(poly),slope)
    if p.is_zero:return True
    if p.degree()==0:return p.LC()>=0
    if p.degree()%2 or p.LC()<0:return False
    _, factors=s.sqf_list(p)
    return all(exponent%2==0 or factor.count_roots(-s.oo,s.oo)==0 for factor,exponent in factors)
def block_membership(M,A,D):
    vv=s.Matrix([1,slope]);w=eta(vv);norm=vv.dot(vv)
    K=((vv.T*D*vv)[0]*norm-(w.T*M.T*M*w)[0]/8)*s.eye(2)+norm**2*A-(M*J*w)*(M*J*w).T/4
    return all(nonnegative(g) for g in [K[0,0],K[1,1],K.det()])
MM=s.diag(2,1);threshold=s.Rational(9,16)
assert block_membership(MM,threshold*s.eye(2),threshold*s.eye(2))
assert not block_membership(MM,(threshold-s.Rational(1,100))*s.eye(2),(threshold-s.Rational(1,100))*s.eye(2))
assert block_membership(s.Matrix([[1,2],[-3,1]]),2*s.eye(2),2*s.eye(2))
assert not block_membership(s.eye(2),s.zeros(2),s.zeros(2))
print('PASS: exact finite block-diagonal quadratic membership, including sharp isotropic boundary and failure below it.')

# Reconstruct the supplied primary primitive at s=1/3, scaled by 3.
a,b,c,d=s.symbols('a b c d',real=True);AA=s.Matrix([a,b,c,d]);T=AA.dot(AA);D=a*d-b*c
F=3*T*T-4*T*D-4*D*D
assert s.expand(F.subs({a:(x1+y1)/2,b:(y2-x2)/2,c:(x2+y2)/2,d:(x1-y1)/2},simultaneous=True)-F0)==0
theta=s.Matrix([-c,-d,a,b]);zeta=s.Matrix([-b,a,-d,c]);alpha=(3*T+14*D)*theta+(9*T-6*D)*zeta
omega=s.Matrix(4,4,lambda i,j:s.diff(alpha[j],AA[i])-s.diff(alpha[i],AA[j]))
h=s.symbols('h:6',real=True);B1=s.Matrix([h[0],h[1],h[3],h[4]]);B2=s.Matrix([h[1],h[2],h[4],h[5]])
P1,P2,Q1,Q2,R1,R2=s.symbols('P1 P2 Q1 Q2 R1 R2',real=True)
P=P1+s.I*P2;QQ=Q1+s.I*Q2;R=R1+s.I*R2;X=x1+s.I*x2;Y=y1+s.I*y2
sub={a:(x1+y1)/2,b:(y2-x2)/2,c:(x2+y2)/2,d:(x1-y1)/2,h[0]:P1+2*Q1+R1,h[1]:-P2+R2,h[2]:-P1+2*Q1-R1,h[3]:P2+2*Q2+R2,h[4]:P1-R1,h[5]:-P2+2*Q2-R2}
S1=s.conjugate(X)*P+2*s.conjugate(Y)*QQ
S2=s.conjugate(Y)*R+s.conjugate(X)*QQ+Y*s.conjugate(QQ)
S3=s.conjugate(X)*QQ+2*Y*s.conjugate(QQ)
abs2=lambda w:s.expand(w*s.conjugate(w))
real=lambda w:s.expand((w+s.conjugate(w))/2)
heat=lambda F,O:s.expand(((B1.T*s.hessian(F,AA)*B1)[0]+(B2.T*s.hessian(F,AA)*B2)[0]+(B1.T*O*B2)[0]).subs(sub,simultaneous=True))
assert s.expand(heat(F,omega)-16*(abs2(S1)+2*abs2(S2)+abs2(S3)))==0
Cplus=(x1*(y1*y1-y2*y2)+2*x2*y1*y2).subs({x1:a+d,x2:c-b,y1:a-d,y2:c+b},simultaneous=True)
OC=s.zeros(4);OQ=s.zeros(4)
for (i,j),val in zip(combinations(range(4),2),[0,-8*(a-d),8*(b+c),8*(b+c),8*(a-d),0]):OC[i,j]=val;OC[j,i]=-val
for i,j,k in combinations(range(4),3):assert s.expand(s.diff(OC[j,k],AA[i])-s.diff(OC[i,k],AA[j])+s.diff(OC[i,j],AA[k]))==0
assert s.expand(heat(Cplus,OC)-32*real(R*S3))==0
for (i,j),val in zip(combinations(range(4),2),[-8,-16,0,0,-16,-8]):OQ[i,j]=val;OQ[j,i]=-val
assert s.expand(heat(2*T,OQ)-64*abs2(R))==0
print('PASS: primary quartic heat density = three explicit complex squares.')
print('PASS: closed cubic correction gives 32 Re(R S3); quadratic correction gives 64 nu |R|^2.')
print('PASS: compatible QC certificate for Cplus coefficient kappa and nu >= |kappa|^2/4 (phase transported by rotations).')

eps=s.symbols('eps',positive=True);xeps=-(1+eps)/(eps*(1-eps));yeps=1/(1-eps);peps=2*eps**2/(1+eps)
curve={x1:xeps,x2:0,y1:yeps,y2:0,P1:peps,P2:0,Q1:eps,Q2:0,R1:1,R2:0}
assert s.simplify(S1.subs(curve))==0 and s.simplify(S2.subs(curve))==0 and s.simplify(S3.subs(curve))==-1
assert s.limit(peps,eps,0)==0
print('PASS: exact degenerating jets prove nu >= 1/4 for this inherited quartic/cubic heat completion with any constant quadratic correction.')
print('Central all-ROC-implies-QC question: NOT RESOLVED. The ROC/QC sufficient thresholds differ: 3/16 versus 1/4 for Cplus.')

# Exhaust all real covariant CLOSED LINEAR cubic two-forms, rather than
# only testing the acquired one. Averaging over the residual circle and
# simultaneous conjugation justifies this invariant subspace; see report.
ww=s.symbols('omega0:24',real=True);OO=s.zeros(4);offset=0
for i,j in combinations(range(4),2):
    OO[i,j]=sum(ww[offset+k]*AA[k] for k in range(4));OO[j,i]=-OO[i,j];offset+=4
cs=s.symbols('coef0:5',real=True)
terms=[s.conjugate(X)*QQ*R,s.conjugate(Y)*R**2,X*R*s.conjugate(P),Y*QQ*s.conjugate(P),Y*R*s.conjugate(QQ)]
EE=s.Poly(s.expand(heat(Cplus,OO)-16*sum(k*real(term) for k,term in zip(cs,terms))),x1,x2,y1,y2,P1,P2,Q1,Q2,R1,R2)
eqs=list(EE.coeffs())
for i,j,k in combinations(range(4),3):eqs.append(s.diff(OO[j,k],AA[i])-s.diff(OO[i,k],AA[j])+s.diff(OO[i,j],AA[k]))
sol=list(s.linsolve(eqs,ww+cs))
assert len(sol)==1 and sol[0][-5:]==(2,0,0,4-cs[4],cs[4])
generic=16*sum(k*real(term) for k,term in zip((2,0,0,4-cs[4],cs[4]),terms))
assert s.limit(s.simplify(generic.subs(curve)),eps,0)==-32
print('PASS: exhaustive covariant cubic-correction family has coefficients (2,0,0,4-gamma,gamma).')
print('PASS: same limiting obstruction holds for EVERY closed linear cubic correction of the fixed primary leading heat density.')
