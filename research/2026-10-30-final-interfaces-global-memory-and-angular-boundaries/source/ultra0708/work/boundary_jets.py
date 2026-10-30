"""Exact acoustic-zero jets for a rational curved-boundary quartic."""
from pathlib import Path
import sympy as S
import json,os

here=Path(os.environ.get('ASTRA_ANGULAR_CASE',Path(__file__).parent))
cfg=json.loads((here/'case_config.json').read_text()) if (here/'case_config.json').exists() else {'beta':'11/13','r':'28/13'}
BV,RV=S.Rational(cfg['beta']),S.Rational(cfg['r'])
a,b,c,d,t=S.symbols('a b c d t',real=True)
A=S.Matrix([a,b,c,d]); T=sum(x*x for x in A); q=a*d-b*c; X=a*a+c*c-b*b-d*d
F=T*T+4*(RV-1)*q*q+4*BV*q*X
H=S.hessian(F,A); HR=H.subs({a:1,b:t,c:0,d:0})
print('det Hessian at rankone:',S.factor(HR.det()),flush=True)
poly=S.factor(HR.det())
factors=S.factor_list(poly,t)[1]
mod=next(f for f,power in factors if S.degree(f,t)==4)
def red(ex): return S.rem(S.expand(ex),mod,t)
K=HR.adjugate()[:,0].applyfunc(red)
fac=S.gcd_list(list(K)); K=K.applyfunc(lambda x:S.cancel(x/fac))
print('polynomial kernel',list(K),flush=True)
assert all(red(x)==0 for x in HR*K)
data=json.loads((here/'angular_family.json').read_text())
v=[S.Symbol(n,real=True) for n in data['variables']]
beta,r=S.symbols('beta r',real=True)
loc={str(x):x for x in (a,b,c,d,beta,r,*v)}
C=S.Matrix([[S.sympify(x,locals=loc) for x in row] for row in data['C']])
C=C.subs({beta:BV,r:RV})
h=S.Matrix([1,t,t*t,0,0,0])
print('substituting exact kernel into completion',flush=True)
eq=[]
sub=dict(zip(A,K))
for x in C*h:
    eq.extend(S.Poly(red(x.subs(sub,simultaneous=True)),t).all_coeffs())
M,rhs=S.linear_eq_to_matrix(eq,v)
solution=next(iter(S.linsolve((M,rhs),v)))
free=sorted(set().union(*(x.free_symbols for x in solution)),key=str)
out={'modulus':str(mod),'kernel':[str(x) for x in K],
     'rank':M.rank(),'variables':list(map(str,v)),
     'solution':list(map(str,solution)),'free':list(map(str,free))}
(here/'boundary_jets.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2),flush=True)
