"""Counterexample-guided acquisition of a common local product frame.
Numerics propose vertices/kernels; exact rational replay is separate.
"""
import sys
sys.dont_write_bytecode=True
import json,time
from collections import deque
import numpy as np
from scipy.optimize import linprog
import sympy as S
from direct_polytope import library
from product_closure_test import hc,local_phi,BASE,D
from product_witness_search import unhc
from exact_product_counterexample import rational_unit
from exact_instrument import clean,projector

def negative_product(W,rng):
 best=1e10;ans=None
 T=W.reshape(D,D,D,D)
 for repeat in range(24):
  b=rng.normal(size=D)+1j*rng.normal(size=D);b/=np.linalg.norm(b)
  prev=1e10
  for _ in range(50):
   A=np.einsum('j,ijkl,l->ik',b.conj(),T,b);_,vs=np.linalg.eigh(A);a=vs[:,0]
   B=np.einsum('i,ijkl,k->jl',a.conj(),T,a);ev,vs=np.linalg.eigh(B);b=vs[:,0];value=ev[0]
   if abs(value-prev)<1e-12:break
   prev=value
  if value<best:best=float(value);ans=(a,b)
 return best,ans

def run(max_states=55):
 t=time.monotonic();rng=np.random.default_rng(92671)
 example=json.loads((BASE/'results'/'EXACT_PRODUCT_COUNTEREXAMPLE.json').read_text())
 U=np.array([[complex(S.sympify(v)) for v in row] for row in example['gate']])
 exact=library()[0];states=[np.array(r,dtype=complex) for r in exact]
 queue=deque((i,j) for i in range(len(states)) for j in range(len(states)))
 solved={};repairs=[];calls=0
 norm=np.r_[np.ones(D*D),np.zeros(D*D*(D*D-1))]
 def matrix():return np.array([hc(np.kron(a,b)) for a in states for b in states]).T
 mat=matrix();eye=hc(np.eye(D*D)/(D*D))
 while queue:
  i,j=queue.popleft()
  if (i,j) in solved:continue
  rho=U@np.kron(states[i],states[j])@U.conj().T;out=local_phi(rho,1.8)
  lp=linprog(np.r_[np.zeros(mat.shape[1]),-1.],A_eq=np.c_[mat,eye],b_eq=hc(out),bounds=(0,None),method='highs')
  calls+=1
  if lp.success:
   N=len(states); terms=[[k//N,k%N,float(v)] for k,v in enumerate(lp.x[:-1]) if v>1e-12]
   solved[i,j]=dict(terms=terms,reserve=float(lp.x[-1]));continue
  dual=linprog(hc(out),A_ub=-mat.T,b_ub=np.zeros(mat.shape[1]),A_eq=norm[None,:],b_eq=[1.],bounds=[(None,None)]*len(mat),method='highs')
  assert dual.success and dual.fun< -1e-8
  value,pair=negative_product(unhc(dual.x),rng)
  assert value< -1e-8
  if len(states)+2>max_states:
   print('STATE CAP: no closure acquired',len(states),len(queue),flush=True);break
  old=len(states);added=[]
  for v in pair:
   q=rational_unit(v,den=256);rho=projector(q)
   exact.append(rho);states.append(np.array(rho,dtype=complex));added.append(len(states)-1)
  repairs.append(dict(input=[i,j],witness_value=float(dual.fun),new_product_value=value,added=added))
  print('repair',len(repairs),'states',len(states),'solved',len(solved),'queue',len(queue),flush=True)
  for a in range(len(states)):
   for b in range(old,len(states)):
    queue.append((a,b));queue.append((b,a))
  queue.appendleft((i,j));mat=matrix()
 result=dict(states=len(states),exact_closure_acquired=False,numerical_closure_proposed=not queue,
  solved_pairs=len(solved),required_pairs=len(states)**2,lp_calls=calls,
  repairs=repairs,min_identity_reserve=min([v['reserve'] for v in solved.values()],default=0),
  elapsed_seconds=time.monotonic()-t)
 artifact=dict(result=result,local_states=[[[str(v) for v in row] for row in M.tolist()] for M in exact],
  kernels=[dict(input=[i,j],**v) for (i,j),v in sorted(solved.items())],gate=example['gate'])
 (BASE/'results'/'REPAIRED_FRAME_PROPOSAL.json').write_text(json.dumps(artifact,separators=(',',':'))+'\n')
 (BASE/'results'/'REPAIR_RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(result,indent=2))

if __name__=='__main__':run()
