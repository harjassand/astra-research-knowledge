"""Locate exact endpoint degeneracies in the r>=1 family proposal.

Numerical diagnostic only. The endpoint t=0 is r=infinity after the
explicit Gram rescaling; no finite-r conclusion is inferred from it.
"""
from pathlib import Path
from math import comb
import pickle,json
import numpy as np,cvxpy as cp
root=Path(__file__).resolve().parents[1];K=pickle.loads((root/'work/n901_family_kernel.pickle').read_bytes());T=pickle.loads((root/'work/n901_parameter_template.pickle').read_bytes());gp=T['Gram_pairs'];degree=3;data=K['data'];lo=K['minpower'];u=cp.Variable((len(K['active']),degree+1));margin=cp.Variable();mats=[]
for power in range(lo,1):
 mat=[[0 for _ in range(12)] for _ in range(12)]
 for k,(i,j) in enumerate(gp):
  co=float(data[k][0].nth(power-lo))
  for a in range(len(K['active'])):
   for l in range(degree+1):
    v=data[k][a+1].nth(power-lo-l) if power-lo-l>=0 else 0
    if v:co=co+float(v)*u[a,l]
  mat[i][j]=mat[j][i]=co
 mats.append(cp.bmat(mat))
con=[M==0 for M in mats[:-1]]+[mats[-1]-margin*np.eye(12)>>0];prob=cp.Problem(cp.Maximize(margin),con);prob.solve(solver='CLARABEL',tol_gap_abs=1e-11,tol_gap_rel=1e-11,tol_feas=1e-12,max_iter=300)
M=mats[-1].value;va,U=np.linalg.eigh(M);out={'status':prob.status,'margin':float(margin.value),'Gram_limit':M.tolist(),'eigenvalues':va.tolist(),'u_coefficients':u.value.tolist(),'small_eigenvectors':U[:,:4].tolist()};(root/'work/n901_endpoint.json').write_text(json.dumps(out,indent=2)+'\n');print('status',prob.status,'margin',margin.value,'eigenvalues',va)
for k in range(4):print('eig',k,va[k],[(i,round(v,6)) for i,v in enumerate(U[:,k]) if abs(v)>1e-4])
