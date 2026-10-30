"""All-amplitude proposal, with covariance allocated once and order cones."""
from pathlib import Path
from fractions import Fraction as R
from itertools import permutations
import sys,json,time
import numpy as np,scipy.linalg as la,cvxpy as cp
root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root/'outputs/quadratic_boundary'));import check_shape as m
sys.path.insert(0,str(root/'work'));import boundary_variation as b
start=time.perf_counter();oc=json.loads((root/'outputs/resonant_gluing/overlap_certificate.json').read_text())
original=[[1.,0,0,0],[0,0,0,1.],[1.]*4,[4.,2.,2.,1.]];H=[b.Hvalue(np.array(r)) for r in original]
Fm=np.diag([3/8*b.Fvalue(r) for r in original])
for i in range(4):
 for j in range(i+1,4):Fm[i,j]=Fm[j,i]=np.array(original[j])@H[i]@np.array(original[j])/16
fc=list(map(float,map(R,oc['quartic_phase_coefficients'])));u=2*(fc[1]-fc[2]);v=2*(fc[1]+fc[2])
for i,co in ((0,abs(u)),(2,abs(v))):
 for j in (1,3):Fm[i,j]-=co/4;Fm[j,i]-=co/4
aux1=[[1.,t,t,t*t] for t in (-1.,.5,2.)];aux2=[[(1+t)**2,t*(1+t),t*(1+t),t*t] for t in (-1.,.5,2.)]
rays=[original[:3]+aux1,[original[i] for i in (0,2,3)]+aux2]
target=b.N.T@np.array([[float(R(x)) for x in row] for row in oc['cubic_targets']]);target[:,1]*=4
GG=[[b.derivatives(np.array(r),b.cpows)@b.N for r in rs] for rs in rays];WW=[]
for rs in rays:
 ws=[]
 for r in rs:
  vals,vecs=la.eigh(b.Hvalue(np.array(r)));ws.append(np.sqrt(np.maximum(vals,0))[:,None]*vecs.T)
 WW.append(ws)
sols=[]
for order in permutations(range(4)):
 minimums=[next(i for i in order if i in ids) for ids in ((0,1,2),(0,2,3))]
 variables=[];constraints=[];D=cp.Constant(Fm)
 for e,(rs,indices) in enumerate(zip(rays,[(0,1,2),(0,2,3)])):
  X=cp.Variable((6,4));en=cp.Variable(6,nonneg=True)
  constraints+=[sum(g.T@X[i] for i,g in enumerate(GG[e]))==target[:,e]]
  for i,W in enumerate(WW[e]):constraints+=[cp.sum_squares(W@X[i])<=en[i]]
  new=9*en[3]+9/16*en[4]+9*en[5]
  for i in range(3):
   j,k=[a for a in range(3) if a!=i];M=np.zeros((4,4));M[indices[j],indices[k]]=M[indices[k],indices[j]]=1
   D=D-2*(en[i]+(new if indices[i]==minimums[e] else 0))*M
  variables.append(X)
 chart=np.zeros((4,4))
 for i in range(4):
  for j in range(i+1):chart[order[i],j]=1
 P=cp.Variable((4,4),symmetric=True);N=cp.Variable((4,4),symmetric=True);gap=cp.Variable()
 constraints += [chart.T@D@chart-gap*np.eye(4)==P+N,P>>0,N>=0]
 problem=cp.Problem(cp.Maximize(gap),constraints);problem.solve(solver='CLARABEL',tol_feas=1e-9,tol_gap_abs=1e-9,tol_gap_rel=1e-9,max_iter=300)
 print(order,minimums,problem.status,problem.value,flush=True)
 sols.append({'order':list(order),'minimums':minimums,'status':problem.status,'gap':None if problem.value is None else float(problem.value),'X':[None if x.value is None else x.value.tolist() for x in variables]})
result={'charts':sols,'seconds':time.perf_counter()-start,'scope':'Numerical proposal only, half covariance per local triad and Young bound for quartets.'};(root/'work/shared_mode_charts_proposal.json').write_text(json.dumps(result,indent=2)+'\n');print('seconds',result['seconds'],flush=True)
