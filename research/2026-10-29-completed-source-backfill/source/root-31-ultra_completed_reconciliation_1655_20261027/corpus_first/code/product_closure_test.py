"""Try the consequential tensor/product-state interface; finite diagnostics only."""
import sys
sys.dont_write_bytecode=True
import json,time
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
from exact_instrument import D
from direct_polytope import library
BASE=Path(__file__).resolve().parents[1]

def hc(A):
 n=len(A); ans=[A[i,i].real for i in range(n)]
 for i in range(n):
  for j in range(i+1,n):ans += [np.sqrt(2)*A[i,j].real,np.sqrt(2)*A[i,j].imag]
 return np.array(ans)

def local_phi(rho,c=2.):
 # First and second local partial traces, then full transpose of residual.
 t=rho.reshape(D,D,D,D)
 ra=np.einsum('ijkj->ik',t); rb=np.einsum('ijil->jl',t)
 return (c*c*np.trace(rho)*np.eye(D*D)-c*np.kron(ra.T,np.eye(D))-c*np.kron(np.eye(D),rb.T)+rho.T)/(c*D-1)**2

def run():
 start=time.monotonic(); rng=np.random.default_rng(472716)
 local=[np.array(x,dtype=complex) for x in library()[0]]
 prods=[np.kron(a,b) for a in local for b in local]
 mat=np.array([hc(a) for a in prods]).T
 tests=[]; failures=[]
 for k in range(240):
  if k<3:
   v=np.zeros(D*D,complex)
   for j in range(k+1):v[D*j+j]=1/np.sqrt(k+1)
  else:
   v=rng.normal(size=D*D)+1j*rng.normal(size=D*D);v/=np.linalg.norm(v)
  rho=np.outer(v,v.conj()); output=local_phi(rho)
  lp=linprog(np.zeros(len(prods)),A_eq=mat,b_eq=hc(output),bounds=(0,None),method='highs')
  record=dict(test=k,status=int(lp.status),success=bool(lp.success))
  if lp.success:record['residual']=float(np.max(abs(mat@lp.x-hc(output))))
  else:
   failures.append(dict(test=k,state_real=v.real.tolist(),state_imag=v.imag.tolist()))
   # Bounded normalized Farkas witness: w dot each product >=0, w dot output<0.
   dual=linprog(hc(output),A_ub=-mat.T,b_ub=np.zeros(len(prods)),bounds=[(-1,1)]*len(mat),method='highs')
   if dual.success:
    record['separating_witness_value']=float(dual.fun)
    record['min_product_value']=float(np.min(mat.T@dual.x))
    failures[-1]['witness']=dual.x.tolist()
   tests.append(record);break
  tests.append(record)
 result=dict(local_vertices=len(local),product_vertices=len(prods),hermitian_dimension=len(mat),
  tested=len(tests),failures=len(failures),tests=tests,
  meaning='A failure rejects this fixed product polytope, not separability or classical simulability.',
  elapsed_seconds=time.monotonic()-start)
 (BASE/'results'/'PRODUCT_CLOSURE_DIAGNOSTIC.json').write_text(json.dumps(result,indent=2)+'\n')
 if failures:(BASE/'results'/'PRODUCT_FAILURE.json').write_text(json.dumps(failures,indent=2)+'\n')
 print(json.dumps({k:v for k,v in result.items() if k!='tests'},indent=2))
 if failures:print(json.dumps(tests[-1],indent=2))

if __name__=='__main__':run()
