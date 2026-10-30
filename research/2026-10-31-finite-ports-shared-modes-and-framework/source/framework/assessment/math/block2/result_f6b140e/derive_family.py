"""Recover a short primitive for the new leading correction."""
from leading_rigidity import *
k=s.symbols('k',real=True)
par={coef[49]:12+36*k,coef[55]:24-24*k,coef[56]:0,coef[57]:36-36*k,coef[58]:0,coef[59]:36-36*k}
Ok=O.subs(dict(zip(coef,sol))).subs(par).applyfunc(s.expand)
delta=((Ok-primary)/k).applyfunc(s.simplify)
us=s.symbols('u:4')
alphas=[T*theta,D*theta,T*zeta,D*zeta]
al=sum((us[i]*alphas[i] for i in range(4)),s.zeros(4,1))
om=s.Matrix(4,4,lambda i,j:s.diff(al[j],A[i])-s.diff(al[i],A[j]))
eq=[]
for i,j in pairs:eq.extend(s.Poly(s.expand(om[i,j]-delta[i,j]),*A).coeffs())
ans=list(s.linsolve(eq,us));print('primitive delta coefficients',ans,flush=True)
print('delta Omega',delta,flush=True)
