import sympy as s,numpy as np,json
from scipy.optimize import linprog
from pathlib import Path
r=Path(__file__).resolve().parent;n=18;D=19
M=s.Matrix([[s.Rational(x)for x in row]for row in json.loads((r/f'transform_n{n}.json').read_text())]);G=2*M-s.eye(D);S=M*s.diag(*[(-1)**l for l in range(D)]);H=s.eye(D).col_join(G).col_join(S)
E=s.eye(D)[0,:].col_join(s.ones(1,D)).col_join(G[1:5,:]);b=s.Matrix([1,s.Rational(D,2),0,0,0,0]);o=linprog(np.zeros(D),A_ub=-np.array(H,float),b_ub=np.zeros(H.rows),A_eq=np.array(E,float),b_eq=np.array(b,float).ravel(),bounds=[(None,None)]*D)
active=[i for i,v in enumerate(np.array(H,float)@o.x)if abs(v)<1e-8];AA=E.col_join(H[active,:]);bb=b.col_join(s.zeros(len(active),1));sol=list(s.linsolve((AA,bb)))[0];assert not set().union(*[x.free_symbols for x in sol]);a=s.Matrix(sol);assert E*a==b;assert all(x>=0 for x in H*a)
(r/'exact_feasible18.json').write_text(json.dumps({'a':[str(x)for x in a],'G_a':[str(x)for x in G*a],'shadow':[str(x)for x in S*a],'exact_verified':True},indent=2));print('exact shadow-feasible n18 witness',a.T)
