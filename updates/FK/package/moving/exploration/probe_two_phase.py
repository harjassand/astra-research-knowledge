import sympy as s
x=s.symbols('a b c d',real=True);a,b,c,d=x
u=a*a+c*c;v=b*b+d*d;q=a*d-b*c
F=3*(u+v-2*q)**2+s.Rational(35,24)*u*u+q*q-s.Rational(5,2)*q*u
H=s.hessian(F,x); DF=s.Matrix([s.diff(F,t) for t in x])
z=s.symbols('z',positive=True)
Rp=s.Matrix([z,1,s.Rational(3,2)*z*z,s.Rational(3,2)*z]);Rm=s.Matrix([-z,1,s.Rational(3,2)*z*z,-s.Rational(3,2)*z])
def ev(p,R): return p.subs(dict(zip(x,R)),simultaneous=True)
HH=s.simplify(ev(H,Rp)+ev(H,Rm))
I=s.Matrix([1,0,0,1]); V=s.Matrix.hstack(s.Matrix([1,0,0,-1]),s.Matrix([0,1,0,0]),s.Matrix([0,0,1,0]))
h=(I.T*HH*I)[0];k=V.T*HH*I;D=V.T*HH*V
sig=s.factor(h-(k.T*D.inv()*k)[0])
print('h',s.factor(h),'sigma',sig, 'ratio',s.factor(sig/h))
print('effective',s.simplify(I-V*D.inv()*k))
# independent profiles with different cubic moments
for m,n in [(1,0),(1,1),(1,-1)]:
 bb=m*ev(DF,Rp)+n*ev(DF,Rm)
 be=s.factor((I.T*bb)[0]-(k.T*D.inv()*V.T*bb)[0])
 print('skew',m,n,'beta',be,'loss',s.factor(be**2/(2*sig)))
M11=s.hessian(s.diff(F,a,2),x)/2;M12=s.hessian(s.diff(F,a,b),x)/2;M22=s.hessian(s.diff(F,b,2),x)/2
Q=z*z*M11+2*z*M12+M22
h1=(I.T*Q*I)[0]; k1=V.T*Q*I; D1=V.T*Q*V
s1=s.factor(h1-(k1.T*D1.inv()*k1)[0]); print('acoustic det',s.factor(Q.det()),'single-sigma',s1)
