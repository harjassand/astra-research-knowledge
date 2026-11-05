import numpy as np,sympy as s,json,time,cvxpy as cp,sys
from sympy.physics.wigner import wigner_6j
from pathlib import Path
from scipy.linalg import eigh
from scipy.sparse import lil_matrix,csr_matrix
r=Path(__file__).resolve().parent

def image(P):
 vals,vecs=eigh((P+P.T)/2);return vecs[:,vals>0.5]
def run(n,d,complement=False,solver='CLARABEL'):
 D=n+1;j=s.Rational(n,2);K=2;M=np.array([[float(s.Rational(x)) for x in row] for row in json.loads((r/f'transform_n{n}.json').read_text())]);G=K*M-np.eye(D);par=np.array([(-1)**l for l in range(D)])
 a=cp.Variable(D);w=(K*K/D)*M@cp.multiply(par,a);eps=cp.Variable(nonneg=True)
 const=[a>=0,a[0]==1,cp.sum(a)==D/K,G@a>=0,G[1:d]@a==0,w>=0]
 blocks=[];variables=[];offset=0;psd=[]
 for J2 in range(n%2,3*n+1,2):
  J=s.Rational(J2,2);ls=[l for l in range(D) if abs(l-j)<=J<=l+j];h=len(ls)
  U=np.array([[float((-1)**(n+l+lp)*s.sqrt((2*l+1)*(2*lp+1))*wigner_6j(j,j,l,j,J,lp)) for lp in ls]for l in ls]);V=np.diag([(-1)**(n-l) for l in ls]);I=np.eye(h)
  Ps=(I+V+U+V@U@V+V@U+U@V)/6;Pa=(I-V-U-V@U@V+V@U+U@V)/6;Pt=I-Ps-Pa
  Qs=image(Ps);Qp=image(Pt@(I+V)/2);Qm=2/np.sqrt(3)*(I-V)/2@U@Qp;R=np.zeros((h,h))
  for lab,Q in [('sym',Qs),('std',Qp)]:
   if Q.shape[1]:
    X=cp.Variable((Q.shape[1],Q.shape[1]),symmetric=True);psd.append(X);R=R+Q@X@Q.T
    if lab=='std':R=R+Qm@X@Qm.T
    variables.append((f'{J2}_{lab}',X))
  blocks.append((J2,ls,R,U,V,offset));offset+=h*h
 fullR=cp.hstack([cp.vec(R,order='C')for J2,ls,R,U,V,off in blocks]);Marg=lil_matrix((D,offset))
 for J2,ls,R,U,V,off in blocks:
  h=len(ls)
  for ix,l in enumerate(ls):Marg[l,off+ix*h+ix]=J2+1
 const.append(csr_matrix(Marg)@fullR==K*w)
 equations=[]
 for rank in range(d):
  for l in range(D):
   for lp in range(l,min(D,l+rank+1)):
    if l+lp<rank:continue
    row={}
    for J2,ls,R,U,V,off in blocks:
     if l not in ls or lp not in ls:continue
     h=len(ls);J=s.Rational(J2,2);coef=float((-1)**(lp+j+J+rank)*wigner_6j(l,j,J,j,lp,rank));ix=ls.index(lp);col=ls.index(l)
     for z in range(h):
      v=(J2+1)*coef*(U[z,col]-(z==col)/K)
      if abs(v)>1e-15:row[off+ix*h+z]=v
    equations.append(row)
 KL=lil_matrix((len(equations),offset))
 for i,row in enumerate(equations):
  for k,v in row.items():KL[i,k]=v
 const.append(csr_matrix(KL)@fullR==0)
 F=lil_matrix((offset,offset))
 for l in range(D):
  for lp in range(D):
   allowed=[(J2,ls,off)for J2,ls,R,U,V,off in blocks if l in ls and lp in ls];ranks=list(range(abs(l-lp),min(l+lp,n)+1))
   C=np.array([[float((-1)**(lp+j+s.Rational(J2,2)+rank)*wigner_6j(l,j,s.Rational(J2,2),j,lp,rank))for rank in ranks]for J2,ls,off in allowed]);wj=np.array([J2+1 for J2,ls,off in allowed]);wr=np.array([2*rank+1 for rank in ranks]);assert np.max(np.abs(C.T@np.diag(wj)@C-np.diag(1/wr)))<1e-10
   T=(C*np.array([(-1)**rank*(2*rank+1)for rank in ranks])[None,:])@C.T@np.diag(wj)
   for z,(J2,ls,off)in enumerate(allowed):
    dst=off+ls.index(l)*len(ls)+ls.index(lp)
    for zp,(J2p,lsp,offp)in enumerate(allowed):
     if abs(T[z,zp])>1e-15:F[dst,offp+lsp.index(l)*len(lsp)+lsp.index(lp)]=T[z,zp]
 F=csr_matrix(F);ppt=F@fullR
 for J2,ls,R,U,V,off in blocks:
  h=len(ls);Rp=cp.reshape(ppt[off:off+h*h],(h,h),order='C');psd.append(Rp)
  if complement:
   B=cp.diag(cp.hstack([w[l]/(2*l+1)for l in ls]));psd.extend([B-R,B-Rp])
 for X in psd:const.append(X+eps*np.eye(X.shape[0])>>0)
 print('built',n,'complement',complement,'constraints',len(const),'variables',sum(X.size for _,X in variables),'entries',offset,'Fnnz',F.nnz,flush=True)
 prob=cp.Problem(cp.Minimize(eps),const);tt=time.time()
 if solver=='CLARABEL':prob.solve(solver=solver,tol_gap_abs=1e-9,tol_feas=1e-9,tol_gap_rel=1e-9,max_iter=300)
 else:prob.solve(solver=solver,eps=1e-7,max_iters=100000,acceleration_lookback=10)
 rec={'n':n,'d':d,'complement':complement,'solver':solver,'status':prob.status,'solve_secs':time.time()-tt,'epsilon':prob.value,'a':a.value.tolist()if a.value is not None else None,'min_psd_eigenvalue':min(np.linalg.eigvalsh(X.value).min()for X in psd)if a.value is not None else None,'max_constraint_violation':max(np.max(np.abs(c.violation()))for c in const)if a.value is not None else None}
 print(json.dumps(rec),flush=True)
 name=f'sparse_ppt_n{n}_c{int(complement)}_{solver}'
 (r/f'{name}.json').write_text(json.dumps(rec,indent=2))
 if a.value is not None:np.savez(r/f'{name}_blocks.npz',a=a.value,fullR=fullR.value,**{name:X.value for name,X in variables})
if __name__=='__main__':run(int(sys.argv[1]),int(sys.argv[2]),bool(int(sys.argv[3]))if len(sys.argv)>3 else False,sys.argv[4]if len(sys.argv)>4 else 'CLARABEL')
