"""Change the heat metric for the original N901 Hessian inequality.

This retains its exact cubic and quartic, with nu=1. Numerical output
is only a proposal until closure, PSD and all parameter ranges are received.
"""
from pathlib import Path
from fractions import Fraction as R
from itertools import product
import sys,json,time
import numpy as np,cvxpy as cp
root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root/'work'));import n901_heat as m
b=m.b;start=time.perf_counter()
def diffusion_density(P,mode):
 H=[[b.diff(b.diff(P,i),j) for j in range(3)] for i in range(3)];B=[[{} for _ in range(4)] for _ in range(4)]
 maps=((m.p1,m.p1),) if mode==0 else ((m.p2,m.p2),) if mode==2 else ((m.p1,m.p2),(m.p2,m.p1))
 for p1,p2 in maps:
  for i,j in product(range(3),repeat=2):B[p1[i]][p2[j]]=b.add(B[p1[i]][p2[j]],H[i][j])
 return np.array([float(B[i][j].get(pw,0))*(1 if i==j else 2) for pw,i,j in m.rowkeys])
records=[]
for rr in (R(1,10),R(1,2),R(1,100),R(1),R(2),R(10)):
 lead,cub,quad=m.source(rr);P=b.add(lead,cub,quad);dd=[diffusion_density(P,i) for i in range(3)];D=cp.Variable((2,2),symmetric=True);G=cp.Variable((14,14),symmetric=True);om=cp.Variable(30);margin=cp.Variable();constraints=[D-R(1,100000)*np.eye(2)>>0,cp.trace(D)==1,G-margin*np.eye(14)>>0,cp.reshape(m.gc.reshape(len(m.rowkeys),196)@cp.reshape(G,(196,),order='C'),(len(m.rowkeys),),order='C')==D[0,0]*dd[0]+D[0,1]*dd[1]+D[1,1]*dd[2]+m.oc@om,m.closure@om==0];prob=cp.Problem(cp.Maximize(margin),constraints)
 try:prob.solve(solver='CLARABEL',tol_gap_abs=1e-10,tol_gap_rel=1e-10,tol_feas=1e-11,max_iter=500);rec={'r':str(rr),'status':prob.status,'margin':None if margin.value is None else float(margin.value),'diffusion':None if D.value is None else D.value.tolist(),'Gram':None if G.value is None else G.value.tolist(),'two_form':None if om.value is None else om.value.tolist()}
 except cp.error.SolverError as err:rec={'r':str(rr),'status':'SOLVER_FAILED','error':str(err)}
 records.append(rec);print(json.dumps({k:v for k,v in rec.items() if k not in ('Gram','two_form')}),flush=True)
 (root/'work/n901_anisotropic_heat.json').write_text(json.dumps({'records':records,'seconds':time.perf_counter()-start,'scope':__doc__},indent=2)+'\n')
