import sympy as s,numpy as np,json
from scipy.optimize import linprog
from pathlib import Path
r=Path(__file__).resolve().parent
for n in [17,18,19,20,21]:
 D=n+1;M=s.Matrix([[s.Rational(x) for x in row] for row in json.loads((r/f'transform_n{n}.json').read_text())]);N=np.array(M,float);G=2*N-np.eye(D);S=N*np.array([(-1)**l for l in range(D)])[None,:]
 eq=np.vstack([np.eye(D)[0],np.ones(D),G[1:5]]);rhs=np.r_[1,D/2,np.zeros(4)]
 for typ in ['base','shadow','zero_overlap']:
  ine=-G if typ=='base' else -np.vstack([G,S])
  ee=np.vstack([eq,S[0]]) if typ=='zero_overlap' else eq;rr=np.r_[rhs,0] if typ=='zero_overlap' else rhs
  o=linprog(np.zeros(D),A_ub=ine,b_ub=np.zeros(len(ine)),A_eq=ee,b_eq=rr,bounds=(0,None))
  print(n,typ,o.status,o.x,flush=True)
