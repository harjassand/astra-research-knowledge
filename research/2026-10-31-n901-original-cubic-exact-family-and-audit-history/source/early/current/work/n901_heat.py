"""Direct original N901 Hessian gate, without the false cubic identity.

Attempt a global compatible-Hessian heat SOS for
J_r(q,w;-sigma p,-sigma q)/(kappa*sigma^2)
 -p^2 q-q^3/sigma^2+nu*p^2.
nu<=1 would prove the exact original gate for that r. Numerical
proposal status alone proves neither admission nor the inequality.
"""
from pathlib import Path
from fractions import Fraction as R
from itertools import product,combinations
import importlib.util,json,time
import numpy as np,cvxpy as cp
root=Path(__file__).resolve().parents[1];sp=importlib.util.spec_from_file_location('n901_poly',root/'outputs/hopf_structure/receive.py');b=importlib.util.module_from_spec(sp);sp.loader.exec_module(b);add,mul,sc,diff=b.add,b.mul,b.scale,b.diff
pwval=sorted([pw for pw in product(range(3),repeat=3) if sum(pw)<=2],key=lambda p:(sum(p),p));qa=[p for p in pwval if sum(p)==2];val=[b.var(3,i) for i in range(3)];one={(0,0,0):R(1)};p1=(0,1,2);p2=(1,2,3);pairs=list(combinations(range(3),2));features=[(0,j) for j in (0,1)]+[(a,j) for a in range(1,4) for j in range(4)];rowkeys=[(pw,i,j) for pw in pwval for i in range(4) for j in range(i,4)];where={v:i for i,v in enumerate(rowkeys)};gc=np.zeros((len(rowkeys),14,14));oc=np.zeros((len(rowkeys),30));closure=np.zeros((4,30));linpowers=[(0,0,0),(1,0,0),(0,1,0),(0,0,1)]
for i,(a,h) in enumerate(features):
 for j,(c,k) in enumerate(features):
  pp=[0]*3
  if a:pp[a-1]+=1
  if c:pp[c-1]+=1
  gc[where[tuple(pp),min(h,k),max(h,k)],i,j]=1
for ip,(i,j) in enumerate(pairs):
 W=np.zeros((4,4))
 for a,c,sign in ((p1[i],p2[j],1),(p2[j],p1[i],1),(p1[j],p2[i],-1),(p2[i],p1[j],-1)):W[a,c]+=sign/2
 for k,pw in enumerate(pwval):
  for a in range(4):
   for c in range(a,4):oc[where[pw,a,c],ip*10+k]=W[a,c]*(1 if a==c else 2)
  dx=0 if (i,j)==(1,2) else 1 if (i,j)==(0,2) else 2;sign=-1 if (i,j)==(0,2) else 1
  for ee,v in diff({pw:R(1)},dx).items():closure[linpowers.index(ee),ip*10+k]=float(v)*sign
def source(r):
 r=R(r);sigma=r+1;kappa=r*(r+2)/3;alpha=3*r/(8*(r+2));beta=r*(r-1)/6;p,q,w=val;a,bb,c,d=q,w,sc(p,-sigma),sc(q,-sigma);u=add(mul(a,a),mul(c,c));vv=add(mul(bb,bb),mul(d,d));det=add(mul(a,d),sc(mul(bb,c),-1));conf=add(u,vv,sc(det,-2));J=add(sc(mul(conf,conf),alpha),sc(mul(u,u),beta),mul(det,det),sc(mul(u,det),r));lead=sc(J,1/(kappa*sigma*sigma));cub=add(sc(mul(mul(p,p),q),-1),sc(mul(mul(q,q),q),-1/(sigma*sigma)));quad=mul(p,p);return lead,cub,quad
def density(P):
 H=[[diff(diff(P,i),j) for j in range(3)] for i in range(3)];B=[[{} for _ in range(4)] for _ in range(4)]
 for ids in (p1,p2):
  for i,j in product(range(3),repeat=2):B[ids[i]][ids[j]]=add(B[ids[i]][ids[j]],H[i][j])
 return np.array([float(B[i][j].get(pw,0))*(1 if i==j else 2) for pw,i,j in rowkeys])
def solve(r,nu_fixed=None):
 lead,cub,quad=source(r);raw0=density(add(lead,cub));rawQ=density(quad);G=cp.Variable((14,14),symmetric=True);om=cp.Variable(30);nu=cp.Variable(nonneg=True);margin=cp.Variable();target=raw0+nu*rawQ+oc@om;constraints=[cp.reshape(gc.reshape(len(rowkeys),196)@cp.reshape(G,(196,),order='C'),(len(rowkeys),),order='C')==target,closure@om==0]
 if nu_fixed is None:constraints.append(G>>0);objective=cp.Minimize(nu)
 else:constraints += [G-margin*np.eye(14)>>0,nu==float(nu_fixed)];objective=cp.Maximize(margin)
 prob=cp.Problem(objective,constraints)
 try:prob.solve(solver='CLARABEL',tol_gap_abs=1e-9,tol_gap_rel=1e-9,tol_feas=1e-10,max_iter=500)
 except cp.error.SolverError as err:return {'r':str(r),'status':'SOLVER_FAILED','error':str(err)}
 return {'r':str(r),'status':prob.status,'nu':None if nu.value is None else float(nu.value),'margin':None if margin.value is None else float(margin.value),'Gram':None if G.value is None else G.value.tolist(),'closed_two_form':None if om.value is None else om.value.tolist()}
if __name__=='__main__':
 start=time.perf_counter();rows=[]
 for r in (R(1,10),R(1),R(10),R(1,100),R(100),R(1,2),R(2)):
  out=solve(r);rows.append(out);print(json.dumps({k:v for k,v in out.items() if k not in ('Gram','closed_two_form')}),flush=True)
  (root/'work/n901_heat.json').write_text(json.dumps({'records':rows,'seconds':time.perf_counter()-start,'scope':__doc__},indent=2)+'\n')
