import sympy as S
x,y,u,v=S.symbols('x y u v',real=True); z=S.Matrix([x,y,u,v]);a,b,c,d=S.symbols('a b c d',real=True);A=S.Matrix([a,b,c,d]);aa=S.Matrix([(x+u)/2,(v-y)/2,(y+v)/2,(x-u)/2]);sub=dict(zip(A,aa))
T=(A.T*A)[0];D=a*d-b*c;s=S.Rational(1,3);F0=T*T-4*s*T*D+(6*s*s-2)*D*D
th=S.Matrix([-c,-d,a,b]);ze=S.Matrix([-b,a,-d,c]);P=(3*s*T+6*(1-2*s*s)*D)*th+(3*T-6*s*D)*ze
PF=S.simplify(3*aa.jacobian(z).T*P.subs(sub,simultaneous=True))
r=x*x+y*y;t=u*u+v*v;F=t*t+2*r*t;C=x*(u*u-v*v)+2*y*u*v;Q=S.Rational(3,16)*(r+t)
h=S.Matrix(S.symbols('h0:6',real=True));Jx=S.Matrix([h[0]+h[4],h[3]-h[1],h[0]-h[4],h[3]+h[1]]).jacobian(h);Jy=S.Matrix([h[1]+h[5],h[4]-h[2],h[1]-h[5],h[4]+h[2]]).jacobian(h)
def correction(P):
 W=P.jacobian(z).T-P.jacobian(z)
 temp=Jx.T*W*Jy
 return S.expand((temp+temp.T)/2)
def heat(f):
 H=S.hessian(f,z);return S.expand(Jx.T*H*Jx+Jy.T*H*Jy)
BF=S.simplify(heat(F)+correction(PF));print('PF',list(PF));print('BFcomputed')
f,g,j,k=S.symbols('f g j k',real=True)
PC=S.Matrix([0,0,x*u+y*v,y*u-x*v]);PCi=S.Matrix([0,0,x*v-y*u,x*u+y*v]);PQ=S.Matrix([-j*y/2,j*x/2,-k*v/2,k*u/2]);BC=heat(C)+f*correction(PC)+g*correction(PCi);BQ=heat(Q)+correction(PQ);B=BF+BC+BQ
# boundary candidate acoustic R in conformal coords (0,1,1,0); original R=(1/2,-1/2;1/2,-1/2): output(1,1) domain(1,-1)
# compatible Hess h=(1,-1,1,1,-1,1), normalization irrelevant
hh=S.Matrix([1,-1,1,1,-1,1]);tau=S.symbols('tau',real=True);Ac={x:-S.Rational(1,4),y:tau,u:-tau/2,v:-S.Rational(1,4)}
eq=[]
for e in B.subs(Ac)*hh:
 eq.extend(S.Poly(S.expand(e),tau).all_coeffs())
sol=S.solve(eq,[f,g,j,k],dict=True);print('sol',sol)
if sol:
 B0=S.simplify(B.subs(sol[0]).subs({x:0,y:0,u:0,v:0}))
 print('B0',B0)
 print('negative vector', (S.Matrix([1,0,-1,0,0,0]).T*B0*S.Matrix([1,0,-1,0,0,0]))[0])
