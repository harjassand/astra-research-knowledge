"""Adversarial alternating search for failure of the fixed product cone."""
import sys
sys.dont_write_bytecode=True
import numpy as np,json,time
from scipy.optimize import linprog
from pathlib import Path
from direct_polytope import library
from product_closure_test import hc,local_phi,D,BASE

def unhc(v,n=D*D):
 A=np.diag(v[:n].astype(complex));k=n
 for i in range(n):
  for j in range(i+1,n):
   A[i,j]=(v[k]+1j*v[k+1])/np.sqrt(2);A[j,i]=A[i,j].conjugate();k+=2
 return A

def run():
 t=time.monotonic();rng=np.random.default_rng(591077)
 loc=[np.array(x,dtype=complex) for x in library()[0]]
 mat=np.array([hc(np.kron(a,b)) for a in loc for b in loc]).T
 norm=np.r_[np.ones(D*D),np.zeros(len(mat)-D*D)]
 best=1e10;records=[];witness=None
 for restart in range(120):
  v=rng.normal(size=D*D)+1j*rng.normal(size=D*D);v/=np.linalg.norm(v)
  last=1e10
  for iteration in range(35):
   rho=np.outer(v,v.conj()); out=local_phi(rho)
   lp=linprog(hc(out),A_ub=-mat.T,b_ub=np.zeros(mat.shape[1]),A_eq=norm[None,:],b_eq=[1.],bounds=[(None,None)]*len(mat),method='highs')
   assert lp.success,lp.message
   W=unhc(lp.x);eigs,vecs=np.linalg.eigh(local_phi(W));val=float(eigs[0]);v=vecs[:,0]
   if val<best:
    best=val;witness=dict(witness=lp.x.tolist(),state_real=v.real.tolist(),state_imag=v.imag.tolist(),restart=restart,iteration=iteration)
   if abs(last-val)<1e-12:break
   last=val
  records.append(dict(restart=restart,value=val,iterations=iteration+1))
 result=dict(restarts=len(records),minimum_found=best,universal_certificate=False,
  records=records,elapsed_seconds=time.monotonic()-t)
 (BASE/'results'/'PRODUCT_WITNESS_SEARCH.json').write_text(json.dumps(result,indent=2)+'\n')
 (BASE/'results'/'PRODUCT_WORST_FOUND.json').write_text(json.dumps(witness,indent=2)+'\n')
 print(json.dumps({k:v for k,v in result.items() if k!='records'},indent=2))

if __name__=='__main__':run()
