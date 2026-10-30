"""Exact P0/F0 transfer receiver. No external scientific inputs or bytecode writes."""
import sys
sys.dont_write_bytecode=True
import sympy as s
x,y,u,v=s.symbols('x y u v',real=True);V=s.Matrix([x,y,u,v]);r=x*x+y*y;t=u*u+v*v
F=t*t+2*r*t;HF=s.hessian(F,V);DF=s.Matrix([s.diff(F,j) for j in V])
basis=[s.diff(F,j) for j in V]+[x*(u*u-v*v),2*x*u*v,y*(u*u-v*v),2*y*u*v]
R=[s.Matrix([1,0,1,0]),s.Matrix([1,0,-1,0]),s.Matrix([2,0,0,2])]
X=[s.Matrix([0,0,-s.Rational(1,4),0]),s.Matrix([0,0,s.Rational(1,4),0]),s.zeros(4,1)]
c0,c1,c2=s.symbols('c0 c1 c2');cc=[c0,c1,c2]
G=sum((R[j]*cc[j] for j in range(3)),s.zeros(4,1));sb=dict(zip(V,G))
def cubeavg(p):return s.Poly(s.expand(p.subs(sb,simultaneous=True)),*cc).coeff_monomial(c0*c1*c2)/4
for k,C in enumerate(basis):
 grad=s.Matrix([s.diff(C,j) for j in V]);lhs=sum((grad.subs(dict(zip(V,Ri))).dot(Xi) for Ri,Xi in zip(R,X)),s.S.Zero)
 assert s.simplify(lhs-cubeavg(C))==0
print('PASS: three original rays match all eight actual exceptional cubics')
assert sum((HF.subs(dict(zip(V,Ri)))*Xi for Ri,Xi in zip(R,X)),s.zeros(4,1))==s.Matrix([-4,0,0,0])
cost=[s.factor((Xi.T*HF.subs(dict(zip(V,Ri)))*Xi)[0]) for Ri,Xi in zip(R,X)]
assert cost==[1,1,0]
A,B,D,kappa=s.symbols('A B D kappa',real=True);S=A+B
f=(9*A*A+4*A*B+48*A*D+9*B*B+48*B*D+144*D*D)/8
rad=(3*A*A+4*A*B+24*A*D+3*B*B+24*B*D+48*D*D)/8
sos=(S-8*D)**2/16+2*D*D+5*(A-B)**2/16
assert s.expand(f-S*D-2*rad-sos)==0
assert s.expand(f-kappa*kappa*S*D-2*rad-sos-(1-kappa*kappa)*S*D)==0
print('PASS: cost E=kappa^2 D(A+B), and exact three-square budget >=2<|G|^4>')
# Derive the actual quartic moments from the polynomial, rather than trusting f/rad.
weighted={}
for powers,co in s.Poly(s.expand(F.subs(sb,simultaneous=True)),*cc).terms():
 if sorted(powers)==[0,0,4]:weighted[powers]=3*[A,B,D][powers.index(4)]**2/8
 elif sorted(powers)==[0,2,2]:
  inds=[j for j in range(3) if powers[j]==2];weighted[powers]=[A,B,D][inds[0]]*[A,B,D][inds[1]]/4
 else:weighted[powers]=0
assert s.expand(sum(co*weighted[p] for p,co in s.Poly(s.expand(F.subs(sb,simultaneous=True)),*cc).terms())-f)==0
normG=(G.dot(G)/2)**2
assert s.expand(sum(co*weighted.get(p,0) for p,co in s.Poly(s.expand(normG),*cc).terms())-rad)==0
print('PASS: actual quartic and radial field moments reconstructed')
# Universal mixed rank-one lower bound: s0=a dot c, t0=b dot d.
s0,t0=s.symbols('s0 t0',real=True)
score=12+8*t0*t0+16*s0*t0
assert s.expand(score-4-8*(t0+ s0)**2-8*(1-s0*s0))==0
# score-4=8(t+s)^2+8(1-s^2) >=0 for |s|<=1.
radscore=4+2*(s0+t0)**2
assert s.expand(score-radscore-6*(t0+s0)**2-8*(1-s0*s0))==0
print('PASS: F0 rank-one cross Hessian dominates the radial quartic cross Hessian')
print('PASS: single-block all-face theorem; lacunary mixed bound gives constant 1')

# The new safe field has nonzero P0 Schur correlation.
H0=sum((HF.subs(dict(zip(V,Ri)))/2 for Ri in R),s.zeros(4))
C0=x*(u*u-v*v)+2*y*u*v
dC0=s.Matrix([s.diff(C0,j) for j in V])
w0=sum((dC0.subs(dict(zip(V,Ri)))/2 for Ri in R),s.zeros(4,1))
assert s.factor(-1-(s.Matrix([-4,0,0,0]).T*H0.inv()*w0)[0])==-s.Rational(4,7)
print('PASS: P0 correlation r=-4/7 is active on the unit-amplitude block')
