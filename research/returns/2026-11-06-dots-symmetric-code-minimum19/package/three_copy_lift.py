import numpy as np,sympy as s,json,time,cvxpy as cp,sys
from sympy.physics.wigner import wigner_6j
from pathlib import Path
from scipy.linalg import eigh
r=Path(__file__).resolve().parent

def image(P):
 vals,vecs=eigh((P+P.T)/2);return vecs[:,vals>0.5]
def run(n,d):
 D=n+1;j=s.Rational(n,2);K=2;M=np.array([[float(s.Rational(x)) for x in row] for row in json.loads((r/f'transform_n{n}.json').read_text())]);G=K*M-np.eye(D);par=np.array([(-1)**l for l in range(D)])
 a=cp.Variable(D);w=(K*K/D)*M@cp.multiply(par,a)
 const=[a>=0,a[0]==1,cp.sum(a)==D/K,G@a>=0,G[1:d]@a==0,w>=0]
 marg=[0 for l in range(D)];blocks=[];variables=[]
 for J2 in range(n%2,3*n+1,2):
  J=s.Rational(J2,2);ls=[l for l in range(D) if abs(l-j)<=J<=l+j];h=len(ls)
  U=np.array([[float((-1)**(n+l+lp)*s.sqrt((2*l+1)*(2*lp+1))*wigner_6j(j,j,l,j,J,lp)) for lp in ls]for l in ls]);V=np.diag([(-1)**(n-l) for l in ls]);I=np.eye(h)
  Ps=(I+V+U+V@U@V+V@U+U@V)/6;Pa=(I-V-U-V@U@V+V@U+U@V)/6;Pt=I-Ps-Pa
  Qs=image(Ps);Qp=image(Pt@(I+V)/2);Qm=2/np.sqrt(3)*(I-V)/2@U@Qp
  assert np.max(np.abs(Qm.T@Qm-np.eye(Qm.shape[1])))<1e-10 if Qm.shape[1] else True
  R=np.zeros((h,h))
  for lab,Q in [('sym',Qs),('std',Qp)]:
   if Q.shape[1]:
    X=cp.Variable((Q.shape[1],Q.shape[1]),symmetric=True);const.append(X>>0);R=R+Q@X@Q.T
    if lab=='std':R=R+Qm@X@Qm.T
    variables.append((f'{J2}_{lab}',X))
  blocks.append((J2,ls,R,U,V))
  for ix,l in enumerate(ls):marg[l]=marg[l]+(J2+1)*R[ix,ix]
 for l in range(D):const.append(marg[l]==K*w[l])
 for rank in range(d):
  for l in range(D):
   for lp in range(l,min(D,l+rank+1)):
    if l+lp<rank:continue
    expression=0
    for J2,ls,R,U,V in blocks:
     if l not in ls or lp not in ls:continue
     J=s.Rational(J2,2);coef=float((-1)**(lp+j+J+rank)*wigner_6j(l,j,J,j,lp,rank))
     expression=expression+(J2+1)*coef*(R@(U-np.eye(len(ls))/K))[ls.index(lp),ls.index(l)]
    const.append(expression==0)
 print('built',n,len(const),sum(X.size for _,X in variables),flush=True)
 prob=cp.Problem(cp.Minimize(0),const);tt=time.time();prob.solve(solver='CLARABEL',tol_gap_abs=1e-8,tol_feas=1e-8,tol_gap_rel=1e-8,max_iter=200)
 rec={'n':n,'d':d,'status':prob.status,'solve_secs':time.time()-tt,'value':prob.value,'a':a.value.tolist() if a.value is not None else None}
 print(json.dumps(rec),flush=True)
 (r/f'three_lift_n{n}.json').write_text(json.dumps(rec,indent=2))
 if a.value is not None:np.savez(r/f'three_lift_n{n}_blocks.npz',**{name:X.value for name,X in variables})
if __name__=='__main__':
 for n,d in [(int(sys.argv[1]),int(sys.argv[2]))] if len(sys.argv)>1 else [(7,3),(18,5),(19,5)]:run(n,d)
