"""Ordinary comparator: pointwise minor supports for the tangent quartic.

An 18x18 SOS Gram is a sufficient constrained polyconvexity certificate.
Failure is an ansatz failure; numerical feasibility still requires exact
reconstruction. It is not ROC admission or an actual-field separation.
"""
from pathlib import Path
from itertools import combinations_with_replacement,product
from fractions import Fraction as R
import sys,json,time
import numpy as np,cvxpy as cp
root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root/'work'));import heat_model as h
b=h.b;start=time.perf_counter();data=np.load(root/'work/sharp_square_model.npz');ell,fac=data['ell'],data['fac'];var=[b.var(7,i) for i in range(7)];M=var[:4];G=[b.add(b.scale(var[4],-ell[1]),b.scale(var[6],-ell[3])),var[4],var[5],var[6]];detG=b.add(b.mul(G[0],G[3]),b.scale(b.mul(G[1],G[2]),-1));MG=[b.mul(m,g) for m,g in product(M,var[4:])];GG=[b.mul(var[4+i],var[4+j]) for i,j in combinations_with_replacement(range(3),2)];features=MG+GG;gamma=[b.mul(m,n) for m,n in combinations_with_replacement(M,2)]
def subst(poly):
 out={}
 for pw,co in poly.items():
  term={(0,)*7:float(co)}
  for mm,gg,p in zip(M,G,pw):
   for _ in range(p):term=b.mul(term,b.add(mm,gg))
  out=b.add(out,term)
 return {pw:v for pw,v in out.items() if sum(pw[4:])>=2}
Fgap=subst(h.F);pows=sorted({pw for i in range(18) for j in range(i,18) for pw in b.mul(features[i],features[j])}|{pw for pp in gamma for pw in b.mul(pp,detG)}|set(Fgap));Gco=np.zeros((len(pows),18,18));gam=np.zeros((len(pows),10));where={pw:i for i,pw in enumerate(pows)}
for i in range(18):
 for j in range(18):
  for pw,v in b.mul(features[i],features[j]).items():Gco[where[pw],i,j]=float(v)
for j,P in enumerate(gamma):
 for pw,v in b.mul(P,detG).items():gam[where[pw],j]=float(v)
Fvec=np.array([float(Fgap.get(pw,0)) for pw in pows]);records=[]
# Every PSD support Gram has these exact acoustic kernels in its MG block.
# Facial reduction is essential; the unreduced solver reached inaccurate
# matrices with negative eigenvalues and supplied no certificate.
av=list(map(lambda v:float(R(v)),h.base['ray']['A0']));alpha=ell[1]/ell[3];aa,bb,cc,dd=av
Mroots=[np.array([-cc,-dd,aa,bb]),np.array([-bb+alpha,aa-alpha*cc,dd+alpha*bb,-cc-alpha*aa])];groots=[np.array([0.,1.,0.]),np.array([1.,0.,-alpha])];kernels=[np.r_[np.outer(M0,g0).ravel(),np.zeros(6)] for M0,g0 in zip(Mroots,groots)];piv=[int(np.argmax(abs(v))) for v in kernels];free=[i for i in range(18) if i not in piv];E=np.eye(18)[:,free]
for v,pi in zip(kernels,piv):
 for j,k in enumerate(free):E[pi,j]=-v[k]/v[pi]
assert np.max(abs(np.array(kernels)@E))<1e-12
Gco=np.einsum('ia,kij,jb->kab',E,Gco,E,optimize=True)
for angle in [None,0.,np.pi/4,np.pi/2,3*np.pi/4]:
 gram=cp.Variable((16,16),symmetric=True);gg=cp.Variable(10);nu=cp.Variable(nonneg=True)
 if angle is None:
  target=Fvec;objective=cp.Minimize(cp.trace(gram));psi2={}
 else:
  coef=np.array([np.cos(angle),np.sin(angle)])@fac;m=coef[:4];lam=coef[4];lM=b.add(*(b.scale(v,q) for v,q in zip(M,ell)));mG=b.add(*(b.scale(v,q) for v,q in zip(G,m)));cofMG=b.add(b.mul(M[0],G[3]),b.mul(M[3],G[0]),b.scale(b.mul(M[1],G[2]),-1),b.scale(b.mul(M[2],G[1]),-1));psi=b.add(b.scale(b.mul(lM,mG),2),b.scale(b.add(detG,cofMG),lam));psi2=b.mul(psi,psi);target=4*nu*Fvec-np.array([float(psi2.get(pw,0)) for pw in pows]);objective=cp.Minimize(nu)
 constraints=[gram>>0,cp.reshape(Gco.reshape(len(pows),256)@cp.reshape(gram,(256,),order='C'),(len(pows),),order='C')+gam@gg==target];problem=cp.Problem(objective,constraints)
 try:problem.solve(solver='CLARABEL',tol_gap_abs=1e-8,tol_gap_rel=1e-8,tol_feas=1e-10,max_iter=500)
 except cp.error.SolverError as err:
  rec={'cubic_angle':angle,'status':'SOLVER_FAILED','error':str(err)};records.append(rec);print(json.dumps(rec),flush=True);continue
 rec={'cubic_angle':angle,'status':problem.status,'nu_proposal':None if nu.value is None else float(nu.value),'Gram_min_eigenvalue':None if gram.value is None else float(np.linalg.eigvalsh(gram.value)[0]),'Gram':None if gram.value is None else gram.value.tolist(),'minor_support_coefficients':None if gg.value is None else gg.value.tolist()};records.append(rec);print(json.dumps({k:v for k,v in rec.items() if k not in ('Gram','minor_support_coefficients')}),flush=True)
(root/'work/tangent_support_sos.json').write_text(json.dumps({'records':records,'seconds':time.perf_counter()-start,'scope':__doc__},indent=2)+'\n')
