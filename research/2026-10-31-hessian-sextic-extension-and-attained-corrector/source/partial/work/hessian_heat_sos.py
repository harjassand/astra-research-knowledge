"""Polynomial heat-SOS diagnostic for the entire scalar-Hessian quartic cone.

Closed quadratic two-forms on Sym(2) correct the compatible four-jet
heat density. A PSD 12 Gram would be sufficient for Hessian QC. Numerical
failures or infeasibility apply only to this polynomial/SOS ansatz.
"""
from pathlib import Path
from fractions import Fraction as R
from itertools import product,combinations
import sys,json,time
import numpy as np,cvxpy as cp
root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root/'work'));import hessian_quartic_cone as m
b=m.b;start=time.perf_counter();qa=sorted(pw for pw in product(range(3),repeat=3) if sum(pw)==2);pi1=(0,1,2);pi2=(1,2,3);pairs=list(combinations(range(3),2));rowkeys=[(pw,i,j) for pw in qa for i in range(4) for j in range(i,4)];index={key:i for i,key in enumerate(rowkeys)};features=[(a,h) for a in range(3) for h in range(4)];gc=np.zeros((60,12,12));oc=np.zeros((60,18));raw=np.zeros((60,15));closure=np.zeros((3,18))
for i,(a,h) in enumerate(features):
 for j,(c,k) in enumerate(features):
  pw=tuple(int(z==a)+int(z==c) for z in range(3));gc[index[pw,min(h,k),max(h,k)],i,j]=1
for ip,(i,j) in enumerate(pairs):
 W=np.zeros((4,4))
 for a,c,sign in ((pi1[i],pi2[j],1),(pi2[j],pi1[i],1),(pi1[j],pi2[i],-1),(pi2[i],pi1[j],-1)):W[a,c]+=sign/2
 for k,pw in enumerate(qa):
  for a in range(4):
   for c in range(a,4):oc[index[pw,a,c],ip*6+k]=W[a,c]*(1 if a==c else 2)
  P={pw:R(1)};dx=0 if (i,j)==(1,2) else 1 if (i,j)==(0,2) else 2;sign=-1 if (i,j)==(0,2) else 1
  for ee,v in b.diff(P,dx).items():closure[ee.index(1),ip*6+k]=float(v)*sign
for l,P in enumerate(m.monomials):
 HH=[[b.diff(b.diff(P,i),j) for j in range(3)] for i in range(3)];B=[[{} for _ in range(4)] for _ in range(4)]
 for ids in (pi1,pi2):
  for i in range(3):
   for j in range(3):B[ids[i]][ids[j]]=b.add(B[ids[i]][ids[j]],HH[i][j])
 for pw in qa:
  for i in range(4):
   for j in range(i,4):raw[index[pw,i,j],l]=float(B[i][j].get(pw,0))*(1 if i==j else 2)
class HeatModel:
 def __init__(self):
  self.h=cp.Parameter(15);self.G=cp.Variable((12,12),symmetric=True);self.o=cp.Variable(18);self.margin=cp.Variable();constraints=[cp.reshape(gc.reshape(60,144)@cp.reshape(self.G,(144,),order='C'),(60,),order='C')==raw@self.h+oc@self.o,closure@self.o==0,self.G-self.margin*np.eye(12)>>0];self.problem=cp.Problem(cp.Maximize(self.margin),constraints)
 def solve(self,h):
  self.h.value=h
  try:self.problem.solve(solver='CLARABEL',tol_gap_abs=1e-9,tol_gap_rel=1e-9,tol_feas=1e-10,max_iter=300)
  except cp.error.SolverError as err:return {'status':'SOLVER_FAILED','error':str(err)}
  return {'status':self.problem.status,'maximum_Gram_margin':None if self.margin.value is None else float(self.margin.value),'Gram':None if self.G.value is None else self.G.value.tolist(),'closed_two_form':None if self.o.value is None else self.o.value.tolist()}
def polynomial_coeff(P):return np.array([float(P.get(pw,0)) for pw in m.powers])
v=[b.var(3,i) for i in range(3)];norm=b.add(b.mul(v[0],v[0]),b.scale(b.mul(v[1],v[1]),2),b.mul(v[2],v[2]));det=b.add(b.mul(v[0],v[2]),b.scale(b.mul(v[1],v[1]),-1));norm4=b.mul(norm,norm);cases=[('norm4',polynomial_coeff(norm4)),('det2',polynomial_coeff(b.mul(det,det))),('DM_11_10',polynomial_coeff(b.add(norm4,b.scale(b.mul(norm,det),-R(11,5)))))]
if '--allow-det2' in sys.argv:
 class HeatModel:
  def __init__(self):
   self.h=cp.Parameter(15);self.G=cp.Variable((12,12),symmetric=True);self.o=cp.Variable(18);self.lam=cp.Variable(nonneg=True);self.margin=cp.Variable();constraints=[cp.reshape(gc.reshape(60,144)@cp.reshape(self.G,(144,),order='C'),(60,),order='C')==raw@(self.h-self.lam*polynomial_coeff(b.mul(det,det)))+oc@self.o,closure@self.o==0,self.G-self.margin*np.eye(12)>>0];self.problem=cp.Problem(cp.Maximize(self.margin-1e-10*self.lam),constraints)
  def solve(self,h):
   self.h.value=h
   try:self.problem.solve(solver='CLARABEL',tol_gap_abs=1e-9,tol_gap_rel=1e-9,tol_feas=1e-10,max_iter=500)
   except cp.error.SolverError as err:return {'status':'SOLVER_FAILED','error':str(err)}
   return {'status':self.problem.status,'maximum_Gram_margin':None if self.margin.value is None else float(self.margin.value),'determinant_square_weight':None if self.lam.value is None else float(self.lam.value),'Gram':None if self.G.value is None else self.G.value.tolist(),'closed_two_form':None if self.o.value is None else self.o.value.tolist()}
roc=m.Model();rng=np.random.default_rng(1379)
for i in range(20):
 fit=roc.solve(rng.normal(size=15));hh=np.array(fit['coefficients'])+1e-5*polynomial_coeff(norm4);cases.append((f'ROC_sample_{i}',hh))
model=HeatModel();records=[]
for name,hh in cases:
 out=model.solve(hh);record={'name':name,'quartic_coefficients':hh.tolist(),**out};records.append(record);print(json.dumps({k:v for k,v in record.items() if k not in ('Gram','closed_two_form','quartic_coefficients')}),flush=True)
 (root/('work/hessian_heat_plus_det2_sos.json' if '--allow-det2' in sys.argv else 'work/hessian_heat_sos.json')).write_text(json.dumps({'powers':m.powers,'records':records,'seconds':time.perf_counter()-start,'scope':__doc__},indent=2)+'\n')
