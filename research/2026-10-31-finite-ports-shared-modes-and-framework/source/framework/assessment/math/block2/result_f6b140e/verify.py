"""Independent exact receiver for the new compatible QC construction.
Requires only already-installed SymPy. No exploratory-script imports.
"""
import sympy as s
from itertools import combinations

a,b,c,d=s.symbols('a b c d',real=True)
A=s.Matrix([a,b,c,d]);T=A.dot(A);D=a*d-b*c
F=3*T*T-4*T*D-4*D*D
theta=s.Matrix([-c,-d,a,b]);zeta=s.Matrix([-b,a,-d,c])
k,nu,lam=s.symbols('k nu lam',real=True)
alphaF=((3+9*k)*T+(14-14*k)*D)*theta+((9-9*k)*T+(-6+14*k)*D)*zeta
O=lambda alpha:s.Matrix(4,4,lambda i,j:s.diff(alpha[j],A[i])-s.diff(alpha[i],A[j]))
OF=O(alphaF)
OC=s.zeros(4);OQ=s.zeros(4)
pairs=list(combinations(range(4),2))
for (i,j),val in zip(pairs,[0,-8*(a-d),8*(b+c),8*(b+c),8*(a-d),0]):
    OC[i,j]=val;OC[j,i]=-val
for (i,j),val in zip(pairs,[-8,-16,0,0,-16,-8]):
    OQ[i,j]=val;OQ[j,i]=-val
for Om in [OF,OC,OQ]:
    for i,j,l in combinations(range(4),3):
        assert s.expand(s.diff(Om[j,l],A[i])-s.diff(Om[i,l],A[j])+s.diff(Om[i,j],A[l]))==0
print('PASS: new quartic, retained cubic, and quadratic two-forms are globally closed.')
alphaC=OC.T*A/3
alphaQ=OQ.T*A/2
assert O(alphaC)==OC and O(alphaQ)==OQ
print('PASS: explicit polynomial primitives for all three correcting forms.')

x1,x2,y1,y2=s.symbols('x1 x2 y1 y2',real=True)
P1,P2,Q1,Q2,R1,R2=s.symbols('P1 P2 Q1 Q2 R1 R2',real=True)
X=x1+s.I*x2;Y=y1+s.I*y2
P=P1+s.I*P2;Q=Q1+s.I*Q2;R=R1+s.I*R2
ab2=lambda z:s.expand(z*s.conjugate(z))
re=lambda z:s.expand((z+s.conjugate(z))/2)
subsA={a:(x1+y1)/2,b:(y2-x2)/2,c:(x2+y2)/2,d:(x1-y1)/2}
assert s.expand(F.subs(subsA,simultaneous=True)-2*ab2(X)*ab2(Y)-ab2(Y)**2)==0
C=(a+d)*((a-d)**2-(b+c)**2)+2*(c-b)*(a-d)*(b+c)
assert s.expand(C.subs(subsA,simultaneous=True)-re(s.conjugate(X)*Y**2))==0
h=s.symbols('h:6',real=True)
B1=s.Matrix([h[0],h[1],h[3],h[4]])
B2=s.Matrix([h[1],h[2],h[4],h[5]])
subsH={h[0]:P1+2*Q1+R1,h[1]:-P2+R2,h[2]:-P1+2*Q1-R1,h[3]:P2+2*Q2+R2,h[4]:P1-R1,h[5]:-P2+2*Q2-R2}
def heat(poly,Om):
    HH=s.hessian(poly,A)
    val=(B1.T*HH*B1)[0]+(B2.T*HH*B2)[0]+(B1.T*Om*B2)[0]
    return s.expand(val.subs(subsA|subsH,simultaneous=True)/16)
K=s.Matrix([[1+k,2,0],[2,10-4*k,4-2*k],[0,4-2*k,3-2*k]])
W=s.Matrix([s.conjugate(X)*P+2*Y*s.conjugate(R),s.conjugate(Y)*Q-Y*s.conjugate(R),X*s.conjugate(Q)+2*Y*s.conjugate(R)])
N=X*Q+2*Y*P
V=s.Matrix([0,2,1])
lead=(s.conjugate(W).T*K*W)[0]+k*ab2(N)
assert s.expand(heat(F,OF)-lead)==0
assert s.expand(heat(C,OC)-2*re((s.conjugate(W).T*V)[0]*R))==0
assert s.expand(heat(2*T,OQ)-4*ab2(R))==0
print('PASS: new quartic identity in all four base and six compatible jet coordinates, symbolic k.')
print('PASS: cubic and quadratic identities match the same joint Gram block.')
dk=1+4*k-2*k*k
shift=s.Matrix([-2,1+k,-1])/dk
assert (K*shift-V).applyfunc(s.simplify)==s.zeros(3,1)
gamma=(2*k+1)/dk
assert s.simplify((V.T*shift)[0]-gamma)==0
WW=W+lam*R*shift
square=(s.conjugate(WW).T*K*WW)[0]+k*ab2(N)+(4*nu-lam*lam*gamma)*ab2(R)
assert s.expand(heat(F+lam*C+2*nu*T,OF+lam*OC+nu*OQ)-(lead+2*lam*re((s.conjugate(W).T*V)[0]*R)+4*nu*ab2(R)))==0
assert s.cancel(s.expand(square-(lead+2*lam*re((s.conjugate(W).T*V)[0]*R)+4*nu*ab2(R))))==0
print('PASS: exact completed joint heat square for arbitrary real cubic amplitude and nu.')
assert s.expand(K[:2,:2].det()-(-4*k*k+6*k+6))==0
assert s.expand(K.det()-2*(1-k)*dk)==0
print('PASS: Sylvester minors prove K positive definite for 0 <= k < 1.')
rate=gamma/4
assert s.simplify(s.diff(rate,k)-(2*k*k+2*k-1)/(2*(2*k*k-4*k-1)**2))==0
opt=(s.sqrt(3)-1)/2
threshold=(3+s.sqrt(3))/24
assert s.simplify(rate.subs(k,opt)-threshold)==0
assert threshold>s.Rational(3,16) and threshold<s.Rational(1,5)
print('PASS: optimal sufficient coefficient in this one-parameter completion is (3+sqrt(3))/24.')
assert s.factor(rate.subs(k,s.Rational(1,3)))==s.Rational(15,76)
print('PASS: rational alternative k=1/3 certifies nu=15/76.')

eps=s.symbols('eps',positive=True)
curve={x1:-(1+eps)/(eps*(1-eps)),x2:0,y1:1/(1-eps),y2:0,P1:2*eps**2/(1+eps),P2:0,Q1:eps,Q2:0,R1:1,R2:0}
assert s.limit(s.simplify(lead.subs(curve)),eps,0)==1+3*k
print('PASS: inherited obstructing jets acquire leading dissipation 1+3k, rather than 1.')
print('QC ESTABLISHED: F0 + Re[conjugate(X)Y^2] + nu(|X|^2+|Y|^2), nu >= (3+sqrt(3))/24.')
print('OPEN: all-ROC-implies-QC, including 3/16 <= nu < (3+sqrt(3))/24 and the other exceptional modes.')
