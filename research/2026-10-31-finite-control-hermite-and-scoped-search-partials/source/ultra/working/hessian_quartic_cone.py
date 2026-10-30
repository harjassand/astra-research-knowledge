"""Lossless ROC cone for ALL homogeneous quartics on Sym(2).

Matrix Fejer--Riesz: H''(x^2,xy,y^2)>=0 iff it has a 9x9 PSD
quadratic Gram. An optimizer proposes coefficients; exact rational
reception and an actual compatible strict negative remain separate.
"""
from pathlib import Path
from fractions import Fraction as R
from itertools import product,permutations
import sys,json,time
import numpy as np,cvxpy as cp
root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root/'outputs/hopf_structure'));import receive as b
sp=sys.modules.get('hessian_graded_core')
if sp is None:
 import importlib.util
 ss=importlib.util.spec_from_file_location('hessian_graded_core',root/'outputs/graded_stabilization/receive.py');sp=importlib.util.module_from_spec(ss);ss.loader.exec_module(sp)
powers=sorted([pw for pw in product(range(5),repeat=3) if sum(pw)==4]);monomials=[{pw:R(1)} for pw in powers];x,y=b.var(2,0),b.var(2,1);ray=[b.mul(x,x),b.mul(x,y),b.mul(y,y)];HH=[[[sp.substitute(b.diff(b.diff(P,i),j),ray) for j in range(3)] for i in range(3)] for P in monomials];Hcoef=np.array([[[[float(P.get((4-j,j),0)) for P in row] for row in H] for H in HH] for j in range(5)])
class Model:
 def __init__(self):
  self.h=cp.Variable(15);self.gram=cp.Variable((9,9),symmetric=True);self.mom=cp.Parameter(15);constraints=[self.gram>>0,cp.trace(self.gram)==1]
  for k in range(5):
   target=cp.reshape(Hcoef[k].reshape(15,9).T@self.h,(3,3),order='C');coeff=sum(self.gram[3*i:3*i+3,3*j:3*j+3] for i in range(3) for j in range(3) if i+j==k);constraints.append(coeff==target)
  self.problem=cp.Problem(cp.Minimize(self.mom@self.h),constraints)
 def solve(self,mom):
  self.mom.value=np.array(mom,float);self.problem.solve(solver='CLARABEL',tol_gap_abs=1e-10,tol_gap_rel=1e-10,tol_feas=1e-11,max_iter=300)
  if self.h.value is None:return None
  return {'status':self.problem.status,'objective':float(self.problem.value),'coefficients':np.array(self.h.value).tolist(),'Gram':np.array(self.gram.value).tolist(),'Gram_minimum_eigenvalue':float(np.linalg.eigvalsh(self.gram.value)[0])}
if __name__=='__main__':
 model=Model();out=model.solve([0.]*15);print(json.dumps({'powers':powers,'initial':out,'scope':__doc__},indent=2))
