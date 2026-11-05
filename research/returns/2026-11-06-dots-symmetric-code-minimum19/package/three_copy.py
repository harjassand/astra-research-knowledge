import numpy as np,sympy as s,json,time,cvxpy as cp
from sympy.physics.wigner import wigner_6j
from pathlib import Path
r=Path(__file__).resolve().parent

def run(n,d):
 D=n+1;j=s.Rational(n,2);K=2;M=np.array([[float(s.Rational(x)) for x in row] for row in json.loads((r/f'transform_n{n}.json').read_text())]);G=K*M-np.eye(D);par=np.array([(-1)**l for l in range(D)])
 a=cp.Variable(D);w=(K*K/D)*M@cp.multiply(par,a)
 const=[a>=0,a[0]==1,cp.sum(a)==D/K,G@a>=0,G[1:d]@a==0,w>=0]
 marg=[0 for l in range(D)];mult=[0 for l in range(D)];blocks=[]
 for J2 in range(n%2,3*n+1,2):
  J=s.Rational(J2,2);ls=[l for l in range(D) if abs(l-j)<=J<=l+j];h=len(ls)
  U=np.array([[float((-1)**(n+l+lp)*s.sqrt((2*l+1)*(2*lp+1))*wigner_6j(j,j,l,j,J,lp)) for lp in ls]for l in ls]);V=np.diag([(-1)**(n-l) for l in ls]);assert np.max(np.abs(U@U-np.eye(h)))<1e-10
  assert np.max(np.abs(U@V@U-V@U@V))<1e-10
  R=cp.Variable((h,h),symmetric=True);const.extend([R>>0,R@U==U@R,R@V==V@R]);blocks.append((J2,ls,R,U,V))
  for ix,l in enumerate(ls):
   marg[l]=marg[l]+(J2+1)*R[ix,ix]
   mult[l]=mult[l]+(J2+1)*(R@U)[ix,ix]
 for l in range(D):const.extend([marg[l]==K*w[l],mult[l]==w[l]])
 prob=cp.Problem(cp.Minimize(0),const);tt=time.time();prob.solve(solver='CLARABEL',tol_gap_abs=1e-9,tol_feas=1e-9,tol_gap_rel=1e-9,max_iter=200)
 rec={'n':n,'d':d,'status':prob.status,'solve_secs':time.time()-tt,'value':prob.value,'a':a.value.tolist() if a.value is not None else None}
 print(json.dumps(rec),flush=True)
 (r/f'three_copy_n{n}.json').write_text(json.dumps(rec,indent=2))
 if a.value is not None:
  np.savez(r/f'three_copy_n{n}_blocks.npz',**{f'J{J2}':R.value for J2,ls,R,U,V in blocks})
for n,d in [(7,3),(18,5),(19,5)]:run(n,d)
