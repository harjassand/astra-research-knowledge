"""Exact acoustic-null constraints for every quadratic closed heat correction.
All computations are local and use the supplied F0 only.
"""
import sympy as s
from itertools import combinations

a,b,c,d=s.symbols('a b c d',real=True)
A=s.Matrix([a,b,c,d]); pairs=list(combinations(range(4),2))
mons=[a*a,a*b,a*c,a*d,b*b,b*c,b*d,c*c,c*d,d*d]
coef=s.symbols('z:60')
O=s.zeros(4)
for k,(i,j) in enumerate(pairs):
    O[i,j]=sum(coef[10*k+l]*m for l,m in enumerate(mons))
    O[j,i]=-O[i,j]
T=A.dot(A);D=a*d-b*c
F=3*T*T-4*T*D-4*D*D
h=s.Matrix(s.symbols('h:6'))
B1=s.Matrix([h[0],h[1],h[3],h[4]])
B2=s.Matrix([h[1],h[2],h[4],h[5]])
L=(B1.T*s.hessian(F,A)*B1)[0]+(B2.T*s.hessian(F,A)*B2)[0]+(B1.T*O*B2)[0]
LH=s.hessian(L,h)/2
eqs=[]
for i,j,k in combinations(range(4),3):
    eqs.extend(s.Poly(s.diff(O[j,k],A[i])-s.diff(O[i,k],A[j])+s.diff(O[i,j],A[k]),*A).coeffs())
# The six components of LH(K(u,v))*h(u,v) have u-degree 3,
# v-degree 4, so these four by five projective samples prove the identity.
us=[(1,0),(0,1),(1,1),(1,-1)]
vs=[(1,0),(0,1),(1,1),(1,-1),(1,2)]
for u1,u2 in us:
    for v1,v2 in vs:
        K=[u1*v1+3*u2*v2,u1*v2-3*u2*v1,u2*v1-3*u1*v2,u2*v2+3*u1*v1]
        hr=s.Matrix([u1*v1*v1,u1*v1*v2,u1*v2*v2,u2*v1*v1,u2*v1*v2,u2*v2*v2])
        eqs.extend(LH.subs(dict(zip(A,K)))*hr)
MM,bb=s.linear_eq_to_matrix(eqs,coef)
print('matrix',MM.shape,'rank',MM.rank(), 'augmented rank',MM.row_join(bb).rank(),flush=True)
sol=list(s.linsolve((MM,bb),coef))[0]
theta=s.Matrix([-c,-d,a,b]);zeta=s.Matrix([-b,a,-d,c])
alpha=(3*T+14*D)*theta+(9*T-6*D)*zeta
primary=s.Matrix(4,4,lambda i,j:s.diff(alpha[j],A[i])-s.diff(alpha[i],A[j]))
OO=s.simplify(O.subs(dict(zip(coef,sol))))
print('free coefficients',sorted(set().union(*(e.free_symbols for e in sol)) & set(coef),key=str),flush=True)
print('six-dimensional family retained; full density tested in optimize_primitive.py',flush=True)
open(__file__.replace('.py','_solution.txt'),'w').write(str(sol)+'\n'+str(OO.applyfunc(s.expand))+'\n')
