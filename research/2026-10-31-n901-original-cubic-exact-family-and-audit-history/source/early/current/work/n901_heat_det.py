"""Original N901 gate: heat monotonicity modulo a convex minor square.

Subtract lam*(p*w-q*q)^2, lam>=0, from the original quartic. The
subtracted term is Hessian-polyconvex; no cubic null identity is used.
Numerical proposals only. An exact receipt is required for any theorem.
"""
from pathlib import Path
from fractions import Fraction as R
import sys,json,time
import numpy as np,cvxpy as cp
root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root/'work'));import n901_heat as m
p,q,w=m.val;det=m.add(m.mul(p,w),m.sc(m.mul(q,q),-1));d2=m.mul(det,det)
def solve(rr):
 lead,cub,quad=m.source(rr);D=m.density(m.add(lead,cub,quad));dm=m.density(d2)
 G=cp.Variable((14,14),symmetric=True);om=cp.Variable(30);lam=cp.Variable(nonneg=True);margin=cp.Variable()
 cons=[G-margin*np.eye(14)>>0,m.gc.reshape(len(m.rowkeys),196)@cp.reshape(G,(196,),order='C')==D-lam*dm+m.oc@om,m.closure@om==0]
 prob=cp.Problem(cp.Maximize(margin),cons)
 try:prob.solve(solver='CLARABEL',tol_gap_abs=1e-10,tol_gap_rel=1e-10,tol_feas=1e-11,max_iter=500)
 except cp.error.SolverError as err:return {'r':str(rr),'status':'SOLVER_FAILED','error':str(err)}
 return {'r':str(rr),'status':prob.status,'margin':None if margin.value is None else float(margin.value),'det_square':None if lam.value is None else float(lam.value),'Gram':None if G.value is None else G.value.tolist(),'closed_two_form':None if om.value is None else om.value.tolist()}
if __name__=='__main__':
 start=time.perf_counter();rows=[]
 for rr in (R(1,100),R(1,10),R(1,2),R(1),R(2),R(10),R(100)):
  rec=solve(rr);rows.append(rec);print(json.dumps({k:v for k,v in rec.items() if k not in ('Gram','closed_two_form')}),flush=True)
  (root/'work/n901_heat_det.json').write_text(json.dumps({'records':rows,'seconds':time.perf_counter()-start,'scope':__doc__},indent=2)+'\n')
