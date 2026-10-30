"""Direct exact energy reconstruction for a positive Hessian quadrature of P0."""
import sys
sys.dont_write_bytecode=True
import sympy as s
from collections import defaultdict
x,y,u,v=s.symbols('x y u v',real=True);V=s.Matrix([x,y,u,v]);r=x*x+y*y;t=u*u+v*v
F=t*t+2*r*t;C=x*(u*u-v*v)+2*y*u*v;P=F+C+s.Rational(3,16)*(r+t)
HP=s.hessian(P,V)
R=[s.Matrix([1,0,1,0]),s.Matrix([1,0,-1,0]),s.Matrix([2,0,0,2])]
X=[s.Matrix([0,0,-s.Rational(1,4),0]),s.Matrix([0,0,s.Rational(1,4),0]),s.zeros(4,1)]
a,b,d=s.Rational(2,3),-s.Rational(3,4),s.Rational(5,7)
amp=[a,b,d];weights=[z*z/2 for z in amp];kap=s.Rational(3,5);phase=(3-4*s.I)/5
k=[(1,0),(0,1),(1,1)];phases=[s.S.One,s.S.One,phase]
G=[{} for j in range(4)]
for j in range(3):
 for sign in [1,-1]:
  kk=tuple(sign*z for z in k[j]);ph=phases[j] if sign==1 else s.conjugate(phases[j])
  for z in range(4):G[z][kk]=amp[j]*R[j][z]*ph/2
zero=(0,0)
def add(a,b):
 out=dict(a)
 for k,v in b.items():out[k]=s.expand(out.get(k,0)+v)
 return {k:v for k,v in out.items() if v!=0}
def mul(a,b):
 out=defaultdict(lambda:s.S.Zero)
 for k,v in a.items():
  for l,w in b.items():out[(k[0]+l[0],k[1]+l[1])]+=v*w
 return {k:s.expand(v) for k,v in out.items() if v!=0}
def mean(poly,arrays):
 out=0
 for powers,coeff in s.Poly(poly,*V).terms():
  pr={zero:coeff}
  for j,powr in enumerate(powers):
   for h in range(powr):pr=mul(pr,arrays[j])
  out+=pr.get(zero,0)
 return s.simplify(out)
M=s.Matrix([s.Rational(1,7),-s.Rational(2,5),s.Rational(1,3),-s.Rational(1,4)])
meanG=[add({zero:M[j]},G[j]) for j in range(4)]
actual=s.simplify(mean(P,meanG)-P.subs(dict(zip(V,M))))
backgrounds=[(a*b*d*kap*Xi/wi) for Xi,wi in zip(X,weights)]
hess=[]
for Ri,wi,Ai in zip(R,weights,backgrounds):
 hs=s.factor((Ri.T*HP.subs(dict(zip(V,M+Ai)))*Ri)[0]);hess.append(hs)
 assert hs>=0
f=mean(F,G);E=kap*kap*d*d*(a*a+b*b)
quad=sum(wi*hi/2 for wi,hi in zip(weights,hess))
assert s.simplify(actual-(f-E+quad))==0
assert f-E>=2*mean((r+t)**2/4,G)
print('mean=',M.T)
for j,(wi,Ai,hs) in enumerate(zip(weights,backgrounds,hess)):
 print('ray',j,'weight',wi,'background',Ai.T,'rank-one Hessian score',hs)
print('actual energy gap=',actual)
print('quartic budget=',s.factor(f-E),'positive Hessian sum=',s.factor(quad))
print('PASS: actual rational-phase periodic gradient energy equals budget plus positive Hessian evaluations')
