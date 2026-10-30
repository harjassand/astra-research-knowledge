"""Compact continuation toward r<1 for the original N901 gate.

The additional t^2 denominator factor clears the Laurent terms; no
condition at infinity is imposed on this compact certificate.
Numerical proposal only.
"""
from pathlib import Path
from fractions import Fraction as R
from math import comb
import pickle,json,time,sys
import numpy as np,cvxpy as cp
root=Path(__file__).resolve().parents[1];K=pickle.loads((root/'work/n901_family_kernel.pickle').read_bytes());T=pickle.loads((root/'work/n901_parameter_template.pickle').read_bytes());gp=T['Gram_pairs'];data=K['data'];active=K['active']
def weights(N,low,high):
 return [[sum((R(comb(k,a),comb(N,a))*comb(p,a)*low**(p-a)*(high-low)**a for a in range(min(k,p)+1)),R(0)) for p in range(N+1)] for k in range(N+1)]
def solve(degree=3,elevation=8,low=R(1),high=R(4,3)):
 start=time.perf_counter();N=K['maxdegree']+degree+elevation;u=cp.Variable(len(active)*(degree+1));margin=cp.Variable();constant=np.zeros((N+1,144));linear=np.zeros((N+1,144,len(active)*(degree+1)))
 for power in range(N+1):
  for k,(i,j) in enumerate(gp):
   constant[power,i*12+j]=constant[power,j*12+i]=float(data[k][0].nth(power))
   for a in range(len(active)):
    for l in range(degree+1):
     v=float(data[k][a+1].nth(power-l)) if power>=l else 0;linear[power,i*12+j,a*(degree+1)+l]=linear[power,j*12+i,a*(degree+1)+l]=v
 ww=np.array(weights(N,low,high),dtype=float);cc=ww@constant;ll=np.einsum('kp,pij->kij',ww,linear);constraints=[]
 for k in range(N+1):
  B=cp.reshape(cc[k]+ll[k]@u,(12,12),order='C')
  for block in K['blocks']:constraints.append(B[np.ix_(block,block)]-margin*np.eye(6)>>0)
 prob=cp.Problem(cp.Maximize(margin),constraints)
 try:prob.solve(solver='CLARABEL',tol_gap_abs=1e-10,tol_gap_rel=1e-10,tol_feas=1e-11,max_iter=400)
 except cp.error.SolverError as err:return {'status':'SOLVER_FAILED','error':str(err)}
 return {'degree':degree,'elevation':elevation,'t_lower':str(low),'t_upper':str(high),'extra_t_power':2,'Bernstein_degree':N,'status':prob.status,'margin':None if margin.value is None else float(margin.value),'u_coefficients':None if u.value is None else u.value.reshape(len(active),degree+1).tolist(),'seconds':time.perf_counter()-start,'active_free_positions':active,'free_scaling_exponents':K['fexp'],'Gram_scaling_exponents':K['gexp']}
if __name__=='__main__':
 out=solve();(root/'work/n901_compact_fit.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='u_coefficients'}),flush=True)
