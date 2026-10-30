import sympy as S
x,y,u,v=S.symbols('x y u v',real=True)
Z=S.Matrix([x,y,u,v]); r=x*x+y*y; t=u*u+v*v
F=t*t+2*r*t
# rank-one direction conformal vectors have equal norm; chart both unit circles rationally
h,k=S.symbols('h k',real=True)
R=S.Matrix([(1-h*h)*(1+k*k),2*h*(1+k*k),(1-k*k)*(1+h*h),2*k*(1+h*h)])
# acoustic H is F''(R); its null vector solved from formula at base first; scaled cubic score
monos=[x**i*y**j*u**l*v**(3-i-j-l) for i in range(4) for j in range(4-i) for l in range(4-i-j)]
H=S.hessian(F,Z)
# at R=(z,w) with unit norms, kernel=(z,-w/2)? H zblock=4|w|²I; H cross=8 z w^T; H wblock=(4|w|²+4|z|²)I+8ww^T, so H*(z,-w/2)=0 when |z|=|w|.
K=S.Matrix([R[0],R[1],-R[2]/2,-R[3]/2])
cols=[]
for m in monos:
    sc=S.expand((S.Matrix([S.diff(m,z) for z in Z]).subs(dict(zip(Z,R)),simultaneous=True).T*K)[0])
    cols.append(S.Poly(sc,h,k))
powers=sorted(set(p for c in cols for p,co in c.terms()))
M=S.Matrix([[c.coeff_monomial(p) for c in cols] for p in powers]); ns=M.nullspace()
print('rank',M.rank(),'kernel',len(ns))
for vec in ns:print(S.factor(sum(m*c for m,c in zip(monos,vec))))
print('translations',[S.factor(S.diff(F,z)) for z in Z])
