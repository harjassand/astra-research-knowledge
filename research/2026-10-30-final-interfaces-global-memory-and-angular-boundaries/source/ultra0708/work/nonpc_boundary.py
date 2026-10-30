"""Acquire and then exactly check two opposite determinant support cuts."""
from pathlib import Path
import json,sympy as S,numpy as np
from scipy.optimize import differential_evolution
p=Path(__file__).parent
t,s,z,w=S.symbols('t s z w',real=True)
def F(a,b,c,d):
    T=a*a+b*b+c*c+d*d;q=a*d-b*c;X=a*a+c*c-b*b-d*d
    return T*T+S.Rational(60,13)*q*q+S.Rational(44,13)*q*X
def cut(base):
    poly=S.Poly(S.expand(F(base[0]+t*s,base[1],base[2],base[3]+t)),t)
    c0,c1,c2=[poly.nth(i) for i in range(3)]
    return S.factor((c2-c1*c1/(4*c0))/(base[0]*base[3]-base[1]*base[2]))
U=cut([0,z,-1,0]);L=cut([1,0,0,-w]);gap=L-U
print('upper',U,'lower',L,flush=True)
fn=S.lambdify((s,z,w),gap/(s*s+1),'numpy',cse=True)
res=differential_evolution(lambda x:-float(fn(*np.exp(x))),[(-1,1),(-4,6),(-4,4)],seed=207,popsize=12,maxiter=180,tol=1e-11)
nums=np.exp(res.x); print('diagnostic',nums,-res.fun,flush=True)
vals=[S.Rational(float(x)).limit_denominator(1000) for x in nums]
up=S.factor(U.subs(dict(zip((s,z,w),vals))));low=S.factor(L.subs(dict(zip((s,z,w),vals))))
out={'A_diagonal':[str(vals[0]),'1'],'Rplus':[['0',str(vals[1])],['-1','0']],
     'Rminus':[['1','0'],['0',str(-vals[2])]],'upper':str(up),'lower':str(low),'gap':str(low-up),
     'strict_nonpc':bool(low>up),'scope':'Exact support inequalities if strict_nonpc is true; optimizer used only to propose cuts.'}
(p/'nonpc_boundary.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
