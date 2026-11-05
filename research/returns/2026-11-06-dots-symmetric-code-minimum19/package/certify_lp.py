import sympy as s,numpy as np,json
from scipy.optimize import linprog
from pathlib import Path
r=Path(__file__).resolve().parent
out=[]
for n in range(9,19):
 D=n+1;M=s.Matrix([[s.Rational(x)for x in row]for row in json.loads((r/f'transform_n{n}.json').read_text())]);G=2*M-s.eye(D);H=s.eye(D).col_join(G);E=G[1:5,:];A=s.ones(D,1).row_join(-H.T).row_join(-E.T);b=s.eye(D)[:,0]
 c=np.r_[1,np.zeros(H.rows+E.rows)];o=linprog(c,A_eq=np.array(A,float),b_eq=np.array(b,float).ravel(),bounds=[(None,None)]+[(0,None)]*H.rows+[(None,None)]*E.rows)
 support=[0]+[i for i in range(1,1+H.rows)if o.x[i]>1e-7]+list(range(1+H.rows,A.cols));sub=A[:,support];sol=s.linsolve((sub,b));v=list(sol)[0];free=set().union(*[x.free_symbols for x in v]);v=[x.subs({y:0 for y in free})for x in v];x=s.zeros(A.cols,1)
 for i,value in zip(support,v):x[i]=value
 assert A*x==b
 assert all(t>=0 for t in x[1:1+H.rows])
 bound=s.factor(x[0]*s.Rational(D,2));rec={'n':n,'upper_a0':str(bound),'excludes':bool(bound<1),'beta':str(x[0]),'inequality_multipliers':[str(y)for y in x[1:1+H.rows]],'equality_multipliers':[str(y)for y in x[1+H.rows:]],'exact_identity_verified':True};out.append(rec);print(n,str(bound),float(bound),flush=True)
(r/'exact_lp_certificates.json').write_text(json.dumps(out,indent=2))
