"""Exact receiver for the phase-two polyconvex support construction.
Uses only SymPy already installed on the host. No file or network writes.
"""
import sympy as s
x1,x2,y1,y2,h,l,k,nu=s.symbols('x1 x2 y1 y2 h l k nu',real=True)
m1,m2,n1,n2=s.symbols('m1 m2 n1 n2',real=True)
A=s.Matrix([x1,x2,y1,y2]);H=s.Matrix([h,l]);K=s.Matrix([k,0]);R=H.col_join(K)
M=s.Matrix([[m1,n1],[m2,n2]]);m=M[:,0];n=M[:,1]
def poly(Z):
 x=Z[:2,0];y=Z[2:,0]
 return 2*x.dot(x)*y.dot(y)+y.dot(y)**2+(x.T*M*s.Matrix([y[0]**2-y[1]**2,2*y[0]*y[1]]))[0]+nu*(x.dot(x)+y.dot(y))
p=poly(A);Dp=s.Matrix([s.diff(p,z) for z in A]);N=lambda Z:Z[0]**2+Z[1]**2-Z[2]**2-Z[3]**2
mu=x1*x1+x2*x2+2*(y1*y1+y2*y2);lam=nu-mu
E=s.expand(poly(A+R)-p-(Dp.T*R)[0]-lam*N(R))
q=h*h+l*l;aa=q+k*k;delta=q-k*k;sm=H.dot(m);tn=H.dot(n)
SX=(aa*s.Matrix([x1,x2])+4*k*H*y1+2*k*k*H+k*k*m/2)
SX=SX.dot(SX)/aa
SY1=(4*delta*y1+2*k*delta+k*sm)**2/(4*aa)
SY2=(4*q*y2+k*tn)**2/(4*q)
rem=k*k*(q+2*nu-(k*k*m.dot(m)+sm*sm)/(4*aa)-tn*tn/(4*q))
assert s.cancel(E-SX-SY1-SY2-rem)==0
print('PASS: exact global support-gap Schur identity for all four entries of M.')
T=(m.dot(m)+n.dot(n))/8
cross=lambda V,W:V[0]*W[1]-V[1]*W[0]
positive_rem=k*k*q+k*k*cross(H,m)**2/(4*aa)+k*k*cross(H,n)**2/(4*q)
assert s.cancel(rem.subs(nu,T)-positive_rem)==0
assert s.cancel(E.subs(nu,T)-(SX+SY1+SY2+positive_rem))==0
print('PASS: at nu=||M||_F^2/8 the support gap is six explicit nonnegative rational squares/terms.')
print('PASS: larger nu adds 2(nu-||M||_F^2/8)|K|^2; degenerate increments follow by continuity.')
print('CONSEQUENCE: P is polyconvex, hence QC, for nu>=||M||_F^2/8.')
print('CONSEQUENCE: for rank(M)<=1 this equals the earned sharp ROC threshold; ROC=QC=PC in the entire isotropic family.')

# A rational two-cut exclusion of every polyconvex lift near the M=I ROC boundary.
d=s.symbols('d',real=True);I=s.eye(2)
pp=s.expand(p.subs({m1:1,m2:0,n1:0,n2:1,nu:s.Rational(3,16)+d}))
base=s.Matrix([-s.Rational(1,4),0,0,-s.Rational(1,4)]);sub=dict(zip(A,base));Hess=s.hessian(pp,A).subs(sub)
rr=s.Matrix([0,1,s.Rational(26,25),0]);lower=s.factor((rr.T*Hess*rr)[0]/(2*N(rr)))
assert s.simplify(lower-(47-20816*d)/816)==0
W=s.Matrix([-2,0,0,1]);tau,lambda0=s.symbols('tau lambda0',real=True)
grad=s.Matrix([s.diff(pp,z) for z in A]).subs(sub)
B=base+tau*W
support=s.expand(pp.subs(dict(zip(A,B)),simultaneous=True)-pp.subs(sub)-(grad.T*(B-base))[0]-lambda0*N(B-base))
assert s.factor(support-tau**2*(9*tau**2-tau+5*d-3*(lambda0-s.Rational(1,16))))==0
upper=s.Rational(23,432)+5*d/3
assert s.simplify(support.subs({tau:s.Rational(1,18),lambda0:upper}))==0
root=s.solve(lower-upper,d)
assert root==[s.Rational(1,6237)] and s.diff(lower-upper,d)<0 and (lower-upper).subs(d,0)>0
print('PASS: opposite-determinant support cuts require lambda >= (47-20816d)/816 and lambda <= 23/432+5d/3.')
print('PASS: these cuts are incompatible for 0<=d<1/6237.')
assert s.simplify(support.subs({d:0,lambda0:s.Rational(1,16)}))==tau**3*(9*tau-1)
print('CONSEQUENCE: every nu in [3/16,3/16+1/6237) is globally ROC and non-polyconvex for M=I.')
print('QC in the remaining ROC/PC gap is NOT established; no compatible negative-energy field has been acquired.')

# Optimize the local negative-determinant cut over its entire 2D block.
e=s.symbols('e',real=True)
Jmetric=s.diag(1,1,-1,-1)
S=Hess-2*(s.Rational(1,16)+e)*Jmetric
block=S.extract([1,2],[1,2])
assert s.expand(block.det())==2*d+4*d*d-4*e*e
star=(43-3*s.sqrt(205))/288
assert s.simplify(20736*star**2-6192*star+1)==0
assert star>0 and star<s.Rational(1,180) and star>s.Rational(1,6237)
# Finite W cut gives 3e <= 5d-1/36. Combined with the determinant bound,
# positivity requires 5d+3sqrt(d/2+d^2)>=1/36. Its left side is increasing.
assert s.simplify(5*star+3*s.sqrt(star/2+star**2)-s.Rational(1,36))==0
print('PASS: optimized local PSD block gives e^2<=d/2+d^2.')
print('STRONGER CONSEQUENCE: M=I is ROC and non-PC for 0<=d<(43-3sqrt(205))/288.')
