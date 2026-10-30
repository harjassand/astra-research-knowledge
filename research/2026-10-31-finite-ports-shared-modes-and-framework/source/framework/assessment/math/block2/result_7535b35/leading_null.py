"""Derive all polynomial quadratic heat corrections allowed by acoustic nulls."""
import sympy as s
from itertools import combinations
from pathlib import Path
BASE=Path(__file__).resolve().parent
a,b,c,d=s.symbols('a b c d',real=True);A=s.Matrix([a,b,c,d]);T=A.dot(A);D=a*d-b*c
F=3*T*T-4*T*D-4*D*D
h=s.symbols('h:6',real=True);hvec=s.Matrix(h)
B1=s.Matrix([h[0],h[1],h[3],h[4]]);B2=s.Matrix([h[1],h[2],h[4],h[5]])
mons=[A[i]*A[j] for i in range(4) for j in range(i,4)]
ww=s.symbols('w:60',real=True);O=s.zeros(4);offset=0
for i,j in combinations(range(4),2):
 O[i,j]=sum(ww[offset+k]*m for k,m in enumerate(mons));O[j,i]=-O[i,j];offset+=10
E=(B1.T*s.hessian(F,A)*B1)[0]+(B2.T*s.hessian(F,A)*B2)[0]+(B1.T*O*B2)[0]
H=s.hessian(E,h)/2
r,t,n,m=s.symbols('r t n m',real=True)
K=s.Matrix([r*n+3*t*m,r*m-3*t*n,t*n-3*r*m,t*m+3*r*n])
rank_h=s.Matrix([r*n*n,r*n*m,r*m*m,t*n*n,t*n*m,t*m*m])
eqs=[]
for e in H.subs(dict(zip(A,K)),simultaneous=True)*rank_h:
 eqs.extend(s.Poly(s.expand(e),r,t,n,m).coeffs())
print('Acoustic coefficient equations:',len(eqs),flush=True)
LIN,rhs=s.linear_eq_to_matrix(eqs,ww)
print('Acoustic rank:',LIN.rank(),'unknowns:',len(ww),flush=True)
sol=s.linsolve((LIN,rhs),ww)
print('Acoustic family:',sol,flush=True)
closure=[]
for i,j,k in combinations(range(4),3):
 closure.extend(s.Poly(s.diff(O[j,k],A[i])-s.diff(O[i,k],A[j])+s.diff(O[i,j],A[k]),*A).coeffs())
LIN2,rhs2=s.linear_eq_to_matrix(eqs+closure,ww)
print('Closed acoustic rank:',LIN2.rank(),flush=True)
sol2=s.linsolve((LIN2,rhs2),ww)
print('Closed acoustic family:',sol2,flush=True)
solution=list(sol2)[0]
( BASE/'leading_solution.txt').write_text(str(solution)+'\n')
Osol=s.simplify(O.subs(dict(zip(ww,solution)),simultaneous=True))
print('Two-form:',Osol,flush=True)
params=sorted(set().union(*(z.free_symbols for z in solution)),key=str)
print('Parameters:',params,flush=True)
(BASE/'leading_null_data.py').write_text('solution='+repr(solution)+'\n')
