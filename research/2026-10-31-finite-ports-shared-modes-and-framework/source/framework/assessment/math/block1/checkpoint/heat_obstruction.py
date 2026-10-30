"""Exact impossibility of a polynomial closed-form heat correction for P0.

The symmetry-reduced primitive classes are exhaustive modulo exact 1-forms.
This is an obstruction to this certificate method, NOT to quasiconvexity.
"""
import sympy as S
from itertools import combinations
x,y,u,v=S.symbols('x y u v',real=True);z=S.Matrix([x,y,u,v]);r=x*x+y*y;t=u*u+v*v
F=t*t+2*r*t;C=x*(u*u-v*v)+2*y*u*v;Q=S.Rational(3,16)*(r+t)
h=S.Matrix(S.symbols('h0:6',real=True))
Jx=S.Matrix([h[0]+h[4],h[3]-h[1],h[0]-h[4],h[3]+h[1]]).jacobian(h)
Jy=S.Matrix([h[1]+h[5],h[4]-h[2],h[1]-h[5],h[4]+h[2]]).jacobian(h)
def correction(P):
    W=P.jacobian(z).T-P.jacobian(z);temp=Jx.T*W*Jy
    return S.expand((temp+temp.T)/2)
def heat(f):
    H=S.hessian(f,z);return S.expand(Jx.T*H*Jx+Jy.T*H*Jy)
q0,q1,q2,q3,q4,f,g,j,k=S.symbols('q0 q1 q2 q3 q4 f g j k',real=True)
az=S.Matrix([-y,x,0,0]);aw=S.Matrix([0,0,-v,u]);rw=S.Matrix([0,0,u,v])
PF=q0*r*az+q1*t*az+q2*r*aw+q3*t*aw+q4*r*rw
PC=f*S.Matrix([0,0,x*u+y*v,y*u-x*v])+g*S.Matrix([0,0,x*v-y*u,x*u+y*v])
PQ=S.Matrix([-j*y/2,j*x/2,-k*v/2,k*u/2])
BF=heat(F)+correction(PF);eq=[]
# PSD at all leading acoustic zeros requires annihilation, not merely zero score.
for ox,oy in [(1,0),(0,1),(1,1),(1,-1)]:
    for nx,ny in [(1,0),(0,1),(1,1),(1,-1)]:
        U=S.Matrix([[ox,-oy],[oy,ox]]);V=S.Matrix([[nx,-ny],[ny,nx]]);K=U*S.diag(S.Rational(1,3),1)*V.T
        ac={x:K[0,0]+K[1,1],y:K[1,0]-K[0,1],u:K[0,0]-K[1,1],v:K[1,0]+K[0,1]}
        hh=S.Matrix([ox*nx*nx,ox*nx*ny,ox*ny*ny,oy*nx*nx,oy*nx*ny,oy*ny*ny])
        eq.extend(BF.subs(ac)*hh)
leading=S.solve(eq,[q0,q1,q2,q3,q4],dict=True)[0]
assert leading=={q0:q1/8+S.Rational(3,2),q2:6-q3,q4:0}
B=BF.subs(leading)+heat(C)+correction(PC)+heat(Q)+correction(PQ)
tau=S.symbols('tau',real=True);Astar={x:-S.Rational(1,4),y:tau,u:-tau/2,v:-S.Rational(1,4)}
hstar=S.Matrix([1,-1,1,1,-1,1]);eq=[]
for item in B.subs(Astar)*hstar:eq.extend(S.Poly(S.expand(item),tau).all_coeffs())
necessary=S.solve(eq,[q1,q3,f,g,j,k],dict=True)[0]
assert necessary=={f:0,g:16*j/3+8*k/3+8,q1:-32*j/9+32*k/9+4,q3:64*j/9+8*k/9+12}
B=S.expand(B.subs(necessary))
# Two exact PSD requirements already contradict one another.
B0=B.subs({x:0,y:0,u:0,v:0})
h0=S.Matrix([0,-1,0,1,0,-1]);val0=S.factor((h0.T*B0*h0)[0])
BL=BF.subs(leading).subs(necessary).subs({x:0,y:0,u:1,v:0})
hL=S.Matrix([-5,0,7,0,1,0]);valL=S.factor((hL.T*BL*hL)[0])
assert val0==4*j+3
assert S.expand(valL+1536*j+1216)==0
print('At A=0, h=(0,-1,0,1,0,-1):',val0,'>=0 requires j>=-3/4')
print('Leading density at (z,w)=(0,1), h=(-5,0,7,0,1,0):',valL,'>=0 requires j<=-19/24')
assert -S.Rational(19,24)<-S.Rational(3,4)
print('Contradiction: no polynomial differential-form heat certificate exists for P0.')
print('This does not prove any failure of the compatible QC inequality.')
