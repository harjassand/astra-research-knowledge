import sympy as s,numpy as np,json,time
from sympy.physics.wigner import wigner_6j
from scipy.optimize import linprog
from pathlib import Path
root=Path(__file__).resolve().parent
out=[]
for dist,ns in [(3,range(3,9)),(5,range(9,22))]:
 for n in ns:
  tt=time.time();j=s.Rational(n,2);D=n+1;K=2
  M=s.Matrix([[(2*k+1)*(-1)**(n+k+l)*wigner_6j(j,j,k,j,j,l) for l in range(D)] for k in range(D)])
  N=np.array(M,float);G=K*N-np.eye(D)
  eq=np.vstack([np.eye(D)[0],np.ones(D),G[1:dist]]);rhs=np.r_[1,D/K,np.zeros(dist-1)]
  opt=linprog(np.zeros(D),A_ub=-G,b_ub=np.zeros(D),A_eq=eq,b_eq=rhs,bounds=(0,None),method='highs')
  rec={'n':n,'dist':dist,'status':opt.status,'message':opt.message,'solution':opt.x.tolist() if opt.x is not None else None,'seconds':time.time()-tt};out.append(rec);print(rec,flush=True)
  (root/f'transform_n{n}.json').write_text(json.dumps([[str(x) for x in M.row(k)] for k in range(D)]))
(root/'screen.json').write_text(json.dumps(out,indent=2))
