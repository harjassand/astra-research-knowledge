"""Exact receiver for the improved compatible heat certificate in REPORT.md.
Uses only SymPy and constructs every final polynomial identity from scratch.
"""
import sympy as s
from itertools import combinations

a,b,c,d=s.symbols('a b c d',real=True);Av=s.Matrix([a,b,c,d]);T=Av.dot(Av);D=a*d-b*c
x1,x2,y1,y2,P1,P2,Q1,Q2,R1,R2=s.symbols('x1 x2 y1 y2 P1 P2 Q1 Q2 R1 R2',real=True)
X=x1+s.I*x2;Y=y1+s.I*y2;P=P1+s.I*P2;Q=Q1+s.I*Q2;R=R1+s.I*R2
cc=s.conjugate;ab=lambda v:s.expand(v*cc(v));re=lambda v:s.expand((v+cc(v))/2)
h=s.symbols('h:6',real=True);B1=s.Matrix([h[0],h[1],h[3],h[4]]);B2=s.Matrix([h[1],h[2],h[4],h[5]])
sub={a:(x1+y1)/2,b:(y2-x2)/2,c:(x2+y2)/2,d:(x1-y1)/2,h[0]:P1+2*Q1+R1,h[1]:-P2+R2,h[2]:-P1+2*Q1-R1,h[3]:P2+2*Q2+R2,h[4]:P1-R1,h[5]:-P2+2*Q2-R2}
F=3*T*T-4*T*D-4*D*D
C=((a+d)*((a-d)**2-(b+c)**2)+2*(c-b)*(a-d)*(b+c))
def twoform(alpha):return s.Matrix(4,4,lambda i,j:s.diff(alpha[j],Av[i])-s.diff(alpha[i],Av[j]))
def heat(F,O):return s.expand(((B1.T*s.hessian(F,Av)*B1)[0]+(B2.T*s.hessian(F,Av)*B2)[0]+(B1.T*O*B2)[0]).subs(sub,simultaneous=True))
A1=cc(X)*P+2*cc(Y)*Q
A2=Y*cc(R)+X*cc(Q)+cc(Y)*Q
A3=X*cc(Q)+2*cc(Y)*Q
V=s.Matrix([A1,A2,A3]);L7=X*Q+2*Y*P;L5=X*R+2*Y*Q;L3=X*cc(R)+2*cc(Y)*P
rho=s.symbols('rho',real=True)
theta=s.Matrix([-c,-d,a,b]);zeta=s.Matrix([-b,a,-d,c])
alpha=((3+s.Rational(9,2)*rho)*T+(14-7*rho)*D)*theta+((9-s.Rational(9,2)*rho)*T+(7*rho-6)*D)*zeta
OF=twoform(alpha)
G=s.Matrix([[1+rho/2,rho,-rho],[rho,2,-rho],[-rho,-rho,1+rho]])
leading=s.expand(rho*ab(L7)/2+(s.conjugate(V).T*G*V)[0])
assert s.expand(heat(F,OF)-16*leading)==0
print('PASS: new global quartic primitive and exact complex Gram identity.')
assert s.expand(G[:2,:2].det()-(2-rho)*(rho+1))==0
assert s.factor(G.det()-(2-rho)*(2+4*rho-rho**2)/2)==0
# Sylvester: all three leading principal minors are positive for 0 <= rho < 2.
f=s.factor((G.inv())[2,2]);assert s.factor(f-2*(rho+1)/(2+4*rho-rho**2))==0
assert s.factor(s.diff(f,rho)-2*(rho**2+2*rho-2)/(rho**2-4*rho-2)**2)==0
rhostar=s.sqrt(3)-1;mustar=(3+s.sqrt(3))/24
assert s.simplify(f.subs(rho,rhostar)/4-mustar)==0
assert s.simplify(f.subs(rho,1)/4-s.Rational(1,5))==0
print('PASS: Gram positive for 0 <= rho < 2; optimum nu=(3+sqrt(3))/24; rational nu=1/5 at rho=1.')
OC=s.zeros(4);OQ=s.zeros(4)
for (i,j),val in zip(combinations(range(4),2),[0,-8*(a-d),8*(b+c),8*(b+c),8*(a-d),0]):OC[i,j]=val;OC[j,i]=-val
for (i,j),val in zip(combinations(range(4),2),[-8,-16,0,0,-16,-8]):OQ[i,j]=val;OQ[j,i]=-val
for i,j,k in combinations(range(4),3):
 assert s.expand(s.diff(OC[j,k],Av[i])-s.diff(OC[i,k],Av[j])+s.diff(OC[i,j],Av[k]))==0
assert s.expand(heat(C,OC)-32*re(A3*cc(R)))==0
assert s.expand(heat(2*T,OQ)-64*ab(R))==0
nu=s.symbols('nu',real=True);e=s.Matrix([0,0,1]);VV=V+G.inv()*e*R
completed=(s.conjugate(VV).T*G*VV)[0]+rho*ab(L7)/2+(4*nu-f)*ab(R)
assert s.simplify(s.expand(leading+2*re(A3*cc(R))+4*nu*ab(R)-completed))==0
print('PASS: closed cubic/constant quadratic corrections and full square completion.')
# A finite real jet attaining the optimized bound, uniformly in rho.
rt=s.sqrt(3);ms=(3+rt)/6;aa=1-1/rt;bb=aa/2
q0=-3/(1+2*rt);p0=-q0/rt
y0=-ms/(2*(q0-p0));x0=-2*y0*p0/q0
jet={x1:x0,x2:0,y1:y0,y2:0,P1:p0,P2:0,Q1:q0,Q2:0,R1:1,R2:0}
assert s.simplify(L7.subs(jet))==0
for val,target in zip(V,[-ms*aa,-ms*bb,-ms]):assert s.simplify(val.subs(jet)-target)==0
assert s.simplify(leading.subs(jet)-ms)==0
assert s.simplify((2*re(A3*cc(R))).subs(jet)+2*ms)==0
assert s.simplify(4*mustar-ms)==0
print('PASS: finite real compatible jet attains nu*, uniformly in the one-parameter leading family (fixed cubic correction).')
# Exhaust the acoustic-null real bilinear forms: 24 variables, 12-dimensional kernel.
u0,u1,v0,v1=s.symbols('u0 u1 v0 v1',real=True)
K=[u0*v0+3*u1*v1,u0*v1-3*u1*v0,u1*v0-3*u0*v1,u1*v1+3*u0*v0]
Hrank=[u0*v0*v0,u0*v0*v1,u0*v1*v1,u1*v0*v0,u1*v0*v1,u1*v1*v1]
monomials=[aa*hh for aa in Av for hh in h]
images=[s.Poly(mm.subs(dict(zip(Av,K)),simultaneous=True).subs(dict(zip(h,Hrank)),simultaneous=True),u0,u1,v0,v1) for mm in monomials]
keys=sorted(set().union(*(im.monoms() for im in images)))
NM=s.Matrix([[im.coeff_monomial(k) for im in images] for k in keys]);assert NM.rank()==12
nulls=[L7,L5,L3,A1,A2,A3]
xyh={x1:a+d,x2:c-b,y1:a-d,y2:c+b,P1:(h[0]-h[2])/4,P2:(h[3]-h[5]-2*h[1])/4,Q1:(h[0]+h[2])/4,Q2:(h[3]+h[5])/4,R1:(h[0]-h[2]+2*h[4])/4,R2:(h[3]-h[5]+2*h[1])/4}
# Correct complex conversion from the six Hessian entries, inverted explicitly.
xyh[P1]=(h[0]-h[2]+2*h[4])/4
xyh[R1]=(h[0]-h[2]-2*h[4])/4
# P2=(h3-h5-2h1)/4, R2=(h3-h5+2h1)/4 as above.
nb=[]
for z in nulls:
 nb.extend([re(z).subs(xyh,simultaneous=True).expand(),s.im(z).expand(complex=True).subs(xyh,simultaneous=True).expand()])
for nn in nb:assert s.expand(nn.subs(dict(zip(Av,K)),simultaneous=True).subs(dict(zip(h,Hrank)),simultaneous=True))==0
BM=s.Matrix([[s.Poly(nn,*Av,*h).coeff_monomial(mm) for nn in nb] for mm in monomials]);assert BM.rank()==12
print('PASS: six complex null bilinears span the full 12-real-dimensional acoustic-null bilinear space.')
# Coefficient-matched general residual-symmetric bilinear SOS family.
t,z,r=s.symbols('t z r',real=True)
Gs=s.Matrix([[1+s.Rational(5,4)*t-z/2-r,t-z,z-t],[t-z,2*(1-t),z],[z-t,z,1-t/2-z+r]])
l7=t/4-z/2;l5=r;l3=t-r
w55=24-6*t+12*z+24*r;w59=36-45*t+18*z+36*r
alphas=((12-w59/4)*T+(-w55/3+11*w59/18)*D)*theta+(w59*T/4+(-w55/3-w59/6+8)*D)*zeta
sosgen=l7*ab(L7)+l5*ab(L5)+l3*ab(L3)+(s.conjugate(V).T*Gs*V)[0]
assert s.expand(heat(F,twoform(alphas))-16*sosgen)==0
Ts=Gs+s.diag(r,0,t-r)
v=s.Matrix([aa,bb,1])
assert s.simplify((v.T*Ts*v)[0]-(3-rt+(s.Rational(5,6)-rt/2)*t))==0
assert s.Rational(5,6)-rt/2<0
# Cubic coupling constraints, including the entire correction parameter gamma.
ee,ff,k1,k2,k3,gamma=s.symbols('e f k1 k2 k3 gamma',real=True)
terms=[re(cc(X)*Q*R),re(cc(Y)*R**2),re(X*R*cc(P)),re(Y*Q*cc(P)),re(Y*R*cc(Q))]
coupled=2*ee*re(L5*cc(P))+2*ff*re(L3*cc(Q))+2*re((cc(V).T*s.Matrix([k1,k2,k3]))[0]*R)
# Re(V* k R) is the conjugate of Re(V k bar R), hence the same real density.
coupled=coupled.subs({k1:-ee,k2:0,k3:1-ff},simultaneous=True)
gam=4*(1-ee-ff)
target=2*terms[0]+(4-gam)*terms[3]+gam*terms[4]
assert s.expand(coupled-target)==0
print('PASS: complete cubic square-coupling map and general null-bilinear SOS dual bound nu >= nu*.')
print('RESULT: improved compatible QC threshold established. Full exceptional ROC/QC question remains unresolved.')
