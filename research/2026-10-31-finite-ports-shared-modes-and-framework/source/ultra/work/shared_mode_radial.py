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
aux1=[[1.,t,t,t*t] for t in (-1.,.5,2.)];aux2=[[(1+t)**2,t*(1+t),t*(1+t),t*t] for t in (-1.,.5,2.)]
rays=[original[:3]+aux1,[original[i] for i in (0,2,3)]+aux2]
target=b.N.T@np.array([[float(R(x)) for x in row] for row in oc['cubic_targets']]);target[:,1]*=4
GG=[[b.derivatives(np.array(r),b.cpows)@b.N for r in rs] for rs in rays];WW=[]
for rs in rays:
 ws=[]
 for r in rs:
  vals,vecs=la.eigh(b.Hvalue(np.array(r)));ws.append(np.sqrt(np.maximum(vals,0))[:,None]*vecs.T)
 WW.append(ws)
def radial_hessian(r):
 r=np.array(r);return 8*np.outer(r,r)+4*np.dot(r,r)*np.eye(4)
Tm=np.diag([3/8*np.dot(r,r)**2 for r in original])
for i in range(4):
 for j in range(i+1,4):Tm[i,j]=Tm[j,i]=np.array(original[j])@radial_hessian(original[i])@np.array(original[j])/16
for i,co in ((0,.5),(2,11.)):
 for j in (1,3):Tm[i,j]+=co/4;Tm[j,i]+=co/4
sols=[]
for order in permutations(range(4)):
 tau=1.;eps=.25
 if order==(1,3,2,0):tau=.25;eps=.3125
 if order in ((3,2,0,1),(3,2,1,0)):tau=.25
 base_e=0 if order.index(1)>order.index(3) else 1
 indices=[(0,1,2),(0,2,3)][base_e];leaf=3 if base_e==0 else 1
 minimum=next(i for i in order if i in indices)
 variables=[];constraints=[];D=cp.Constant(Fm);young=[]
 for gi,co in ((0,abs(u)),(2,abs(v))):
  lam=cp.Variable(nonneg=True);beta=cp.Variable(nonneg=True);young.append((lam,beta))
  constraints+=[cp.bmat([[lam,1.],[1.,beta]])>>0]
  for gj,vv in ((1,lam),(3,beta)):
   MM=np.zeros((4,4));MM[gi,gj]=MM[gj,gi]=1;D=D-co*vv*MM/4
 rs=rays[base_e]+[original[leaf]]
 XX=cp.Variable((7,4));YY=cp.Variable((7,4));variables=[XX,YY]
 GGbase=[b.derivatives(np.array(r),b.cpows)@b.N for r in rs]
 for e,X in enumerate(variables):
  en=cp.Variable(7,nonneg=True)
  constraints+=[sum(g.T@X[i] for i,g in enumerate(GGbase))==target[:,e]]
  if e==base_e:constraints+=[X[6]==0]
  for i,r in enumerate(rs):
   vals,vecs=la.eigh(b.Hvalue(np.array(r)));W=np.sqrt(np.maximum(vals,0))[:,None]*vecs.T
   constraints+=[cp.sum_squares(W@X[i])<=en[i]]
  new=9*en[3]+9/16*en[4]+9*en[5]
  target_ids=[(0,1,2),(0,2,3)][e]
  for i,global_i in enumerate(indices):
   pair=[z for z in target_ids if z!=global_i] if global_i in target_ids else [0,2]
   M=np.zeros((4,4));M[pair[0],pair[1]]=M[pair[1],pair[0]]=1
   gamma=(1+tau) if e==base_e else (1+1/tau);D=D-gamma*en[i]*M/(4*(.5-eps))
  pair=[z for z in target_ids if z!=minimum] if minimum in target_ids else [0,2]
  M=np.zeros((4,4));M[pair[0],pair[1]]=M[pair[1],pair[0]]=1;gamma=(1+tau) if e==base_e else (1+1/tau);D=D-gamma*new*M/(4*eps)
  M=np.zeros((4,4));M[0,2]=M[2,0]=1;D=D-en[6]*M/2
 chart=np.zeros((4,4))
 for i in range(4):
  for j in range(i+1):chart[order[i],j]=1
 P=cp.Variable((4,4),symmetric=True);N=cp.Variable((4,4),symmetric=True);gap=cp.Variable()
 constraints += [chart.T@D@chart-gap*(chart.T@Tm@chart)==P+N,P>>0,N>=0]
 problem=cp.Problem(cp.Maximize(gap),constraints);problem.solve(solver='CLARABEL',tol_feas=1e-9,tol_gap_abs=1e-9,tol_gap_rel=1e-9,max_iter=300)
 print(order,base_e,minimum,problem.status,problem.value,flush=True)
 sols.append({'order':list(order),'tau':tau,'epsilon':eps,'base':base_e,'minimum':minimum,'status':problem.status,'gap':None if problem.value is None else float(problem.value),'young':[[float(a.value),float(c.value)] for a,c in young],'X':[None if x.value is None else x.value.tolist() for x in variables]})
result={'charts':sols,'seconds':time.perf_counter()-start,'scope':'Numerical proposal only, half covariance per local triad and Young bound for quartets.'};(root/'work/shared_mode_radial_proposal.json').write_text(json.dumps(result,indent=2)+'\n');print('seconds',result['seconds'],flush=True)
