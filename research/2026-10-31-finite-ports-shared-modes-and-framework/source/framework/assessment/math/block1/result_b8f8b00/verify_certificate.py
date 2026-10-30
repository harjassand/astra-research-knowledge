"""Exact compatible heat certificates for the exceptional cubic modes.

No numerical sample is used to justify the theorem.  All identities below
are coefficient identities over Q or Q(sqrt(3)).
"""
import sympy as S
x,y,u,v=S.symbols('x y u v',real=True);A=S.Matrix([x,y,u,v]);r=x*x+y*y;t=u*u+v*v
h=S.Matrix(S.symbols('h0:6',real=True));X=S.Matrix([h[0]+h[4],h[3]-h[1],h[0]-h[4],h[3]+h[1]]);Y=S.Matrix([h[1]+h[5],h[4]-h[2],h[1]-h[5],h[4]+h[2]])
az=S.Matrix([-y,x,0,0]);aw=S.Matrix([0,0,-v,u]);
Cp=x*(u*u-v*v)+2*y*u*v;Cm=x*(u*u-v*v)-2*y*u*v;F=t*t+2*r*t
PiP=S.Matrix([0,0,x*v-y*u,x*u+y*v]);PiM=S.Matrix([0,0,x*v+y*u,x*u-y*v])
z=x+S.I*y;w=u+S.I*v
al=h[0]-h[2]+2*h[4]+S.I*(h[3]-h[5]-2*h[1])
be=h[0]+h[2]+S.I*(h[3]+h[5])
ga=h[0]-h[2]-2*h[4]+S.I*(h[3]-h[5]+2*h[1])
Ss=z*be+2*w*al
T=S.Matrix([S.conjugate(z)*al+2*S.conjugate(w)*be,z*S.conjugate(be)+2*w*S.conjugate(ga),z*S.conjugate(be)+2*S.conjugate(w)*be])
U=S.conjugate(z)*al+S.conjugate(w)*be+w*S.conjugate(ga)
def norm(e):return S.expand(e*S.conjugate(e))
def density(P,eta):
 H=S.hessian(P,A);W=eta.jacobian(A).T-eta.jacobian(A)
 return S.expand((X.T*H*X)[0]+(Y.T*H*Y)[0]+(X.T*W*Y)[0])
def zero(e):
 assert S.cancel(S.expand(e))==0

a,b=S.symbols('a b',real=True);lam=(a*a+b*b)/4
eta=(2*r+4*t-2*lam)*az+(4*r+2*t-6*lam)*aw-4*a*PiP-4*b*PiM
P=F+a*Cp+b*Cm+lam*(r+t)
rhs=norm(Ss+b*S.conjugate(ga))+2*norm(U)+norm(T[2]+a*ga)
zero(density(P,eta)-rhs)
print('PASS: universal certificate, arbitrary real conformal and anticonformal cubic coefficients.')
# Rank-one M=diag(m,0): a=b=m/2 and sharp lambda=m^2/8.
m=S.symbols('m',real=True)
zero(P.subs({a:m/2,b:m/2})-(F+m*x*(u*u-v*v)+m*m*(r+t)/8))
print('PASS: rank-one M isotropic threshold lambda=m^2/8, equal to exact ROC threshold.')
# Full one-parameter improvement for Cplus with Cminus retained.
p=S.symbols('p',positive=True)
G=S.Matrix([[1+p,p,-p],[p,S.Rational(1,2),S.Rational(1,2)-p],[-p,S.Rational(1,2)-p,S.Rational(3,2)]])
q1=8*p-4
etaF=(1+p)*r*az+q1*t*az+(4*r+2*t)*aw
BF=density(F,etaF)
zero(BF-p*norm(Ss)-(S.conjugate(T).T*G*T)[0])
zero(G[:2,:2].det()-(1-p)*(2*p+1)/2)
zero(G.det()-(1-p)*(1+4*p-2*p*p)/2)
cost=S.factor(G.inv()[2,2]);zero(cost-(2*p+1)/(1+4*p-2*p*p))
etaC=-4*a*PiP-4*b*PiM
zero(density(a*Cp+b*Cm,etaC)-2*S.re(a*T[2]*S.conjugate(ga)+b*Ss*ga))
print('PASS: one-parameter leading-square identity and both cubic cross identities.')
# Specialized conformal improvement, in Q(sqrt(3)).
s=S.sqrt(3);ps=(s-1)/2;lh=(3+s)/24;Gs=G.subs(p,ps)
vv=S.Matrix([S.Rational(1,3),-(1+s)/6,(3+s)/6])
zero((Gs*vv-S.Matrix([0,0,1]))[0]);zero((Gs*vv-S.Matrix([0,0,1]))[1]);zero((Gs*vv-S.Matrix([0,0,1]))[2])
zero(vv[2]-4*lh)
eta=((1+ps)*r+(8*ps-4)*t-2*lh)*az+(4*r+2*t-6*lh)*aw-4*PiP
rhs=ps*norm(Ss)+(S.conjugate(T+vv*ga).T*Gs*(T+vv*ga))[0]
zero(density(F+Cp+lh*(r+t),eta)-rhs)
assert S.simplify(Gs[0,0])>0
assert S.simplify(Gs[:2,:2].det())>0
assert S.simplify(Gs.det())>0
print('PASS: conformal threshold lambda_H=(3+sqrt(3))/24, exact positive-definite Gram matrix.')
print('Central boundary lambda=3/16 for M=I is NOT proved QC by this receiver.')
