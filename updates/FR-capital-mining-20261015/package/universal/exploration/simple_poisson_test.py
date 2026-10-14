import sympy as s
from scipy.optimize import minimize
import numpy as np
z=s.symbols('z');a,b,c=s.symbols('a b c',real=True)
s1=(z-z**-1)/(2*s.I);s3=(z**3-z**-3)/(2*s.I);s5=(z**5-z**-5)/(2*s.I)
h=a*s1+b*s3+c*s5
k=4/s.sqrt(3)
L=s.expand((h*h+s1*s1)**2-k*h*s1*(h*h+s1*s1))
mean=lambda p:s.expand(p).coeff(z,0)
r=mean(L)+k*a/8
print('residual',s.expand(r),flush=True)
fun=s.lambdify((a,b,c),r,'numpy');jac=s.lambdify((a,b,c),[s.diff(r,t) for t in (a,b,c)],'numpy')
res=minimize(lambda v:fun(*v),[1.1,-.1,0],jac=lambda v:np.array(jac(*v)),method='BFGS',tol=1e-13)
print(res.fun,res.x,flush=True)
for den in [10,20,100]:
 v=[s.Rational(round(float(x)*den),den) for x in res.x]
 print(v,s.simplify(r.subs(dict(zip((a,b,c),v)))),float(r.subs(dict(zip((a,b,c),v)))))
