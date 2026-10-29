from certified_projection_v1 import *
from scipy.optimize import minimize
import json
from pathlib import Path

def propose_large(Y,mult):
 # The unseen objective is negligible but NOT omitted from certificate.
 # Optimize the limiting seen-only dual over Lambda>=0; this is merely
 # a candidate factory, never the proof of acceptance.
 assert mult[-1]>1 and all(k==1 for k in mult[:-1])
 seen=np.array([matrix(y) for y in Y[:-1]])
 def fg(v):
  L=matrix(v);ev,U=np.linalg.eigh(seen-L/2)
  E=(U*np.maximum(ev,0)[...,None,:])@U.conj().swapaxes(-1,-2)
  val=2*v[0]+np.sum(np.maximum(ev,0)**2)
  grad=2*(np.array([1,0,0,0])-coeff(E.sum(0)))
  return val,grad
 opt=minimize(lambda v:fg(v),[.1,0,0,0],jac=True,method='SLSQP',constraints=[{'type':'ineq','fun':lambda v:v[0]-np.linalg.norm(v[1:])}],options={'ftol':1e-14,'maxiter':2000})
 L=matrix(opt.x);ev,U=np.linalg.eigh(seen-L/2)
 E=(U*np.maximum(ev,0)[...,None,:])@U.conj().swapaxes(-1,-2)
 return np.concatenate([E,(I-E.sum(0))[None,:,:]]),opt.x,opt.nit

results=[]
for power in [60,120,512,2048]:
 K=1<<power
 # Overloaded centers, complex off-diagonals, and a finite unseen aggregate.
 Y=[[F(4,5),F(1,5),F(1,4),F(0)],[F(7,10),F(-1,6),F(1,5),F(1,7)],[F(1,5),F(0),F(0),F(0)]]
 mult=[1,1,K];w=[F(1,k) for k in mult]
 cand,ld,it=propose_large(Y,mult);E=repair(cand)
 L=[dyadic(x) for x in ld];_,u=sqrt_interval(dot(L[1:],L[1:]),128);L[0]+=max(F(0),u-L[0])
 primal=objective(E,Y,w);dual=dual_lower(L,Y,w,power+160);gap=primal-dual
 assert 0<=gap<=F(1,10**7),(power,float(gap))
 results.append({'K_power':power,'iterations':it,'input_Y':[[str(x) for x in y] for y in Y],'multiplicities':[str(k) for k in mult],'output_E':[[str(x) for x in e] for e in E],'dual_L':[str(x) for x in L],'primal':str(primal),'dual_lower':str(dual),'gap':str(gap),'gap_float':float(gap),'interval_bits':power+160})
Path(__file__).with_suffix('.json').write_text(json.dumps({'status':'PASS_EXACT_GAPS_INCLUDING_HUGE_UNSEEN_WEIGHT','cases':results},indent=2)+'\n')
print([(x['K_power'],x['gap_float']) for x in results])
