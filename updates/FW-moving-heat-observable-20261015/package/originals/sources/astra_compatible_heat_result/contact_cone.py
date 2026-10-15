from reconstruct import *
n,m=s.symbols('n m',real=True)
al,be,ga,de=s.symbols('alpha beta gamma delta',real=True)
Hdist=(u+v-2*j)**2
F=al*Hdist+be*u**2+ga*j**2+de*u*j
H=s.Matrix([n,m,0,0]);h=(H.T*s.hessian(F,x)*H)[0].expand();M=s.hessian(h,x)/2
print('M0',M.subs({n:0,m:1}))
I=s.Matrix([1,0,0,1]);t=s.symbols('t')
M0=M.subs({n:0,m:1});M1=M.diff(n).subs({n:0,m:1});M2=M.diff(n,2).subs({n:0,m:1})/2
P=s.eye(4)[:,:3]
k=s.factor((I.T*M2*I)[0]-(I.T*M1*P*(P.T*M0*P).inv()*P.T*M1*I)[0]);print('schur quadratic coeff=',k)
print('boundary beta=',s.solve(k,be))
# determinant in n,m after boundary replacement
bv=s.solve(k,be)[0]
Mb=M.subs(be,bv)
print('boundary det=',s.factor(Mb.det()))
# choose gamma1 parameter delta=-2-t maybe
print('fixed ratio boundary at supplied beta',s.factor(k.subs({be:R(35,24),ga:1,de:-R(5,2)})))
print('general det coefficients')
poly=s.Poly(M.det(method='domain-ge'),n,m)
for mon,coef in poly.terms():print(mon,s.factor(coef))
