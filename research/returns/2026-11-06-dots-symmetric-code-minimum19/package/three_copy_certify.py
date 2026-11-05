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
 blocks=[];variables=[];offset=0;psd=[];psd_meta=[];seed_data={}
 for J2 in range(n%2,3*n+1,2):
  J=s.Rational(J2,2);ls=[l for l in range(D) if abs(l-j)<=J<=l+j];h=len(ls)
  U=np.array([[float((-1)**(n+l+lp)*s.sqrt((2*l+1)*(2*lp+1))*wigner_6j(j,j,l,j,J,lp)) for lp in ls]for l in ls]);V=np.diag([(-1)**(n-l) for l in ls]);I=np.eye(h)
  Ps=(I+V+U+V@U@V+V@U+U@V)/6;Pa=(I-V-U-V@U@V+V@U+U@V)/6;Pt=I-Ps-Pa
  Zs=image(Ps);Zp=image(Pt@(I+V)/2);Qs=Ps@Zs;Qp=Pt@(I+V)/2@Zp;Qm=2/np.sqrt(3)*(I-V)/2@U@Qp;R=np.zeros((h,h))
  seed_data[str(J2)]={'ls':ls,'symmetric_seed':Zs.tolist(),'standard_seed':Zp.tolist()}
  for lab,Q in [('sym',Qs),('std',Qp)]:
   if Q.shape[1]:
    X=cp.Variable((Q.shape[1],Q.shape[1]),symmetric=True);psd.append(X);psd_meta.append({"type":"base","J2":J2,"label":lab});R=R+Q@X@Q.T
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
   T=np.array([[float((-1)**n*(J2p+1)*wigner_6j(l,j,s.Rational(J2,2),lp,j,s.Rational(J2p,2)))for J2p,lsp,offp in allowed]for J2,ls,off in allowed])
   if (l,lp) in [(0,0),(2,5),(9,9),(7,15),(18,18)]:
    C=np.array([[float((-1)**(lp+j+s.Rational(J2,2)+rank)*wigner_6j(l,j,s.Rational(J2,2),j,lp,rank))for rank in ranks]for J2,ls,off in allowed]);wj=np.array([J2+1 for J2,ls,off in allowed]);Tcheck=(C*np.array([(-1)**rank*(2*rank+1)for rank in ranks])[None,:])@C.T@np.diag(wj);assert np.max(np.abs(T-Tcheck))<1e-11
   for z,(J2,ls,off)in enumerate(allowed):
    dst=off+ls.index(l)*len(ls)+ls.index(lp)
    for zp,(J2p,lsp,offp)in enumerate(allowed):
     if abs(T[z,zp])>1e-15:F[dst,offp+lsp.index(l)*len(lsp)+lsp.index(lp)]=T[z,zp]
 F=csr_matrix(F);ppt=F@fullR
 for J2,ls,R,U,V,off in blocks:
  h=len(ls);Rp=cp.reshape(ppt[off:off+h*h],(h,h),order='C');psd.append(Rp);psd_meta.append({'type':'ppt','J2':J2})
  if complement:
   B=cp.diag(cp.hstack([w[l]/(2*l+1)for l in ls]));psd.extend([B-R,B-Rp]);psd_meta.extend([{'type':'BminusR','J2':J2},{'type':'BminusPpt','J2':J2}])
 for X in psd:const.append(X+eps*np.eye(X.shape[0])>>0)
 print('built',n,'complement',complement,'constraints',len(const),'variables',sum(X.size for _,X in variables),'entries',offset,'Fnnz',F.nnz,flush=True)
 prob=cp.Problem(cp.Minimize(eps),const);tt=time.time()
 if solver=='CLARABEL':prob.solve(solver=solver,tol_gap_abs=1e-9,tol_feas=1e-9,tol_gap_rel=1e-9,max_iter=300)
 else:prob.solve(solver=solver,eps=1e-7,max_iters=100000,acceleration_lookback=10)
 rec={'n':n,'d':d,'complement':complement,'solver':solver,'status':prob.status,'solve_secs':time.time()-tt,'epsilon':prob.value,'a':a.value.tolist()if a.value is not None else None,'min_psd_eigenvalue':min(np.linalg.eigvalsh(X.value).min()for X in psd)if a.value is not None else None,'max_constraint_violation':max(np.max(np.abs(c.violation()))for c in const)if a.value is not None else None}
 print(json.dumps(rec),flush=True)
 name=f'certificate_n{n}'
 (r/f'{name}.json').write_text(json.dumps(rec,indent=2))
 if a.value is not None:np.savez(r/f'{name}_blocks.npz',a=a.value,fullR=fullR.value,**{name:X.value for name,X in variables})
 from fractions import Fraction
 if a.value is not None:
  dual=[];L=0
  for i,cst in enumerate(const[:8]):
   y=np.array(cst.dual_value,float)
   if isinstance(cst,cp.constraints.nonpos.Inequality):y=np.maximum(y,0)
   dual.append(y.tolist());L=L+cp.sum(cp.multiply(y,cst.expr))
  matrices=[];shifts=[]
  for X,cst,meta in zip(psd,const[8:],psd_meta):
   Z=np.array(cst.dual_value,float);Z=(Z+Z.T)/2;shift=max(1e-12,-float(np.linalg.eigvalsh(Z).min())+1e-12);Z=Z+shift*np.eye(len(Z));matrices.append(Z.tolist());shifts.append(shift);L=L-cp.sum(cp.multiply(Z,X))
  (r/f'{name}_raw_duals.json').write_text(json.dumps({'linear_duals':dual,'psd_meta':psd_meta,'psd_duals':matrices,'basis_seed_data':seed_data},indent=2))
  all_gradients=L.grad
  ga=np.array(all_gradients[a].toarray()).ravel();grads={};scaled=[]
  for vname,X in variables:
   gg=all_gradients[X];grad=np.array(gg.toarray()if hasattr(gg,'toarray')else gg).ravel().reshape(X.shape,order='F');grad=(grad+grad.T)/2;grads[vname]=grad.tolist();J2=int(vname.split('_')[0]);fac=2 if vname.endswith('std') else 1;scaled.append(np.max(np.sum(np.abs(grad),axis=1))/((J2+1)*fac*.999))
  bound=(D/2)*max(abs(ga))+8*max(scaled)
  cexact=-Fraction(float(dual[1]))-Fraction(D,2)*Fraction(float(dual[2]));cn=float(cexact)
  cert={'n':n,'d':d,'solver_status':prob.status,'epsilon':prob.value,'linear_duals':dual,'psd_meta':psd_meta,'psd_duals':matrices,'diagonal_shifts':shifts,'constant_exact':str(cexact),'constant_float':cn,'a_gradient':ga.tolist(),'matrix_gradients':grads,'floating_residual_bound_assuming_min_gram_0999':bound,'floating_margin':cn-bound,'basis_seed_data':seed_data,'psd_dual_min_float':min(np.linalg.eigvalsh(np.array(Z)).min()for Z in matrices)}
  (r/f'{name}_candidate.json').write_text(json.dumps(cert,indent=2));print('DUAL_CANDIDATE',cn,bound,cn-bound,flush=True)

if __name__=='__main__':run(int(sys.argv[1]),int(sys.argv[2]),bool(int(sys.argv[3]))if len(sys.argv)>3 else False,sys.argv[4]if len(sys.argv)>4 else 'CLARABEL')
