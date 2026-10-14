import sympy as S
z,t=S.symbols('z t');I=S.I
cs=lambda n:(z**n+z**(-n))/2
sn=lambda n:(z**n-z**(-n))/(2*I)
dy=lambda f:S.expand(I*z*S.diff(f,z))
dx=lambda f:S.expand(t*S.diff(f,t))
mean=lambda f:S.expand(f).coeff(z,0)
def halfint(f):
 f=S.Poly(mean(f),t);return S.simplify(sum(co/S.Integer(p[0]) for p,co in f.terms()))
f=t*cs(1)-S.Rational(1,5)*t*t*sn(2)-S.Rational(1,6)*t**3*cs(3)
h=-S.Rational(3,8)+S.Rational(7,6)*t*sn(1)+S.Rational(1,10)*t*t*cs(2)-S.Rational(1,2)*t**3*sn(3)
fx,fy,hx,hy=dx(f),dy(f),dx(h),dy(h)
dI=halfint((fx*hy-hx*fy)*(fx*fx+fy*fy))
p=fy.subs(t,1);v=h.subs(t,1)
k=4/S.sqrt(3)
L=mean((v*v+p*p)**2+k*v*p*(v*v+p*p))
DP=-k*dI/2
R=S.simplify(L-DP);n4=mean((v*v+p*p)**2)
print('dI',dI,'L',S.simplify(L),'DP',S.simplify(DP),'residual',R,'N4',n4,'ratio',S.N(R/n4,16))
