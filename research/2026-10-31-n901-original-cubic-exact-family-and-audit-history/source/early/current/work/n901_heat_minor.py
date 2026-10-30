"""Original N901 gate modulo a convex function of (det Hessian,p).

This enlarges the heat certificate by a PSD quadratic form in these two
minors. It changes neither the original functional nor the actual field.
Numerical proposals only.
"""
from pathlib import Path
from fractions import Fraction as R
import sys,json,time
import numpy as np,cvxpy as cp
root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root/'work'));import n901_heat as m
p,q,w=m.val;det=m.add(m.mul(p,w),m.sc(m.mul(q,q),-1));polys=[m.mul(det,det),m.sc(m.mul(p,det),2),m.mul(p,p)]
def solve(rr):
 lead,cub,quad=m.source(rr);D=m.density(m.add(lead,cub,quad));ds=[m.density(P) for P in polys]
 G=cp.Variable((14,14),symmetric=True);om=cp.Variable(30);K=cp.Variable((2,2),symmetric=True);margin=cp.Variable()
 cons=[K>>0,G-margin*np.eye(14)>>0,m.gc.reshape(len(m.rowkeys),196)@cp.reshape(G,(196,),order='C')==D-K[0,0]*ds[0]-K[0,1]*ds[1]-K[1,1]*ds[2]+m.oc@om,m.closure@om==0]
 prob=cp.Problem(cp.Maximize(margin),cons)
 try:prob.solve(solver='CLARABEL',tol_gap_abs=1e-10,tol_gap_rel=1e-10,tol_feas=1e-11,max_iter=500)
 except cp.error.SolverError as err:return {'r':str(rr),'status':'SOLVER_FAILED','error':str(err)}
 return {'r':str(rr),'status':prob.status,'margin':None if margin.value is None else float(margin.value),'minor_form':None if K.value is None else K.value.tolist(),'Gram':None if G.value is None else G.value.tolist(),'closed_two_form':None if om.value is None else om.value.tolist()}
if __name__=='__main__':
 start=time.perf_counter();rows=[]
 for rr in (R(1,100),R(1,10),R(1,2),R(1),R(2),R(10)):
  rec=solve(rr);rows.append(rec);print(json.dumps({k:v for k,v in rec.items() if k not in ('Gram','closed_two_form')}),flush=True)
  (root/'work/n901_heat_minor.json').write_text(json.dumps({'records':rows,'seconds':time.perf_counter()-start,'scope':__doc__},indent=2)+'\n')
