"""Facial reduction for the original N901 heat certificate.

The rank-one acoustic zero at S=(0,2,0), xi=(1,0), and its first
directional derivative force two exact Gram kernels. Numerical only.
"""
from fractions import Fraction as R
from pathlib import Path
import sys,json,time
import numpy as np,cvxpy as cp
root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root/'work'));import n901_heat as m
def face(rr):
 rr=R(rr);N=3*rr*rr+8*rr+4;pp=-3*N/((rr+1)**2*(2*rr+1));ww=N/(rr+1)
 L=np.zeros((12,14));rows=[[(2,0,R(1)),(0,0,R(-2))],[(1,0,R(1)),(0,1,-pp)],[(2,1,R(1)),(0,1,R(-2))],[(3,0,R(1)),(0,1,-ww)]]
 rows += [[(a,h,R(1))] for a,h in ((1,1),(1,2),(1,3),(2,2),(2,3),(3,1),(3,2),(3,3))]
 for i,row in enumerate(rows):
  for a,h,c in row:L[i,m.features.index((a,h))]=float(c)
 return L,rows
def solve(rr):
 lead,cub,quad=m.source(rr);raw=m.density(m.add(lead,cub,quad));L,rows=face(rr);gc=np.einsum('ia,kab,jb->kij',L,m.gc,L);G=cp.Variable((12,12),symmetric=True);om=cp.Variable(30);margin=cp.Variable()
 cons=[G-margin*np.eye(12)>>0,gc.reshape(len(m.rowkeys),144)@cp.reshape(G,(144,),order='C')==raw+m.oc@om,m.closure@om==0]
 prob=cp.Problem(cp.Maximize(margin),cons)
 try:prob.solve(solver='CLARABEL',tol_gap_abs=1e-11,tol_gap_rel=1e-11,tol_feas=1e-12,max_iter=500)
 except cp.error.SolverError as err:return {'r':str(rr),'status':'SOLVER_FAILED','error':str(err)}
 return {'r':str(rr),'status':prob.status,'margin':None if margin.value is None else float(margin.value),'Gram':None if G.value is None else G.value.tolist(),'closed_two_form':None if om.value is None else om.value.tolist(),'face':[[[a,h,str(c)] for a,h,c in row] for row in rows]}
if __name__=='__main__':
 start=time.perf_counter();rows=[]
 for rr in (R(1),R(2),R(10),R(1,2)):
  rec=solve(rr);rows.append(rec);print(json.dumps({k:v for k,v in rec.items() if k not in ('Gram','closed_two_form','face')}),flush=True)
  (root/'work/n901_facial.json').write_text(json.dumps({'records':rows,'seconds':time.perf_counter()-start,'scope':__doc__},indent=2)+'\n')
