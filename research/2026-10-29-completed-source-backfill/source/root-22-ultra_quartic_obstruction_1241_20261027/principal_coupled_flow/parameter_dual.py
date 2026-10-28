"""Search a continuously valid dual family, not a grid in gamma.

Any candidate coupled-flow certificate has0<=gamma<=10 by the compatible
plane-wave jet A=diag(-1,1), B1=e11,B2=0 (20-2gamma>=0).
An affine lambda(gamma) with PSD moment endpoints, exact mixed annihilation,
and negative Bernstein energy coefficients would exclude allb/allgamma.
Only floating search here; rational reconstruction is a separate obligation.
"""
from pathlib import Path
from fractions import Fraction
from itertools import combinations_with_replacement
import cvxpy as cp
import numpy as np,json,time,sys
ROOT=Path(__file__).resolve().parent
SRC=Path('producer-workspace/principal')
d=np.load(SRC/'interfaces.npz');data=json.loads((ROOT/'PAIRINGS.json').read_text())
ej=[np.array([float(Fraction(t)) for t in row['mixed_coefficient_vector']]) for row in data['rows']]
p=np.array([1,1,16,-13,0,0,4,-4,0.]);ef=d['E']@p;ed=d['Ed']
xp=list(combinations_with_replacement(range(4),2));zp=list(combinations_with_replacement(range(6),2))
indices=np.array([21*xp.index(tuple(sorted((i//6,j//6))))+zp.index(tuple(sorted((i%6,j%6)))) for i in range(24) for j in range(24)])
lo=float(sys.argv[1]) if len(sys.argv)>1 else 0.
hi=float(sys.argv[2]) if len(sys.argv)>2 else 10.
width=hi-lo
v0=ej[0]-lo*ej[1];e0=ef-lo*ed
L0=cp.Variable(210);L1=cp.Variable(210);margin=cp.Variable()
Y0=cp.reshape(L0[indices],(24,24),order='C');Yend=cp.reshape((L0+L1)[indices],(24,24),order='C')
q0=L0@e0;q1=L1@e0-width*(L0@ed);q2=-width*(L1@ed)
constraints=[d['ON'].T@L0==0,d['ON'].T@L1==0,
  L0@v0==0,L1@v0-width*(L0@ej[1])==0,L1@ej[1]==0,
  Y0 >> 1e-7*np.eye(24),Yend >> 1e-7*np.eye(24),
  cp.trace(Y0+Yend)==1,q0<=-margin,q0+q1/2<=-margin,q0+q1+q2<=-margin]
problem=cp.Problem(cp.Maximize(margin),constraints)
start=time.monotonic()
problem.solve(solver='CLARABEL',max_iter=150,tol_gap_abs=1e-9,tol_feas=1e-9,tol_gap_rel=1e-9,verbose=False)
out={'status':'NUMERICAL_PARAMETER_DUAL_SEARCH','solver_status':problem.status,
 'gamma_interval':[lo,hi],'margin':None if margin.value is None else float(margin.value),
 'seconds':time.monotonic()-start,
 'scope':'Floating parameter-dual search only; no exact infeasibility/positivity theorem without reconstruction.'}
if L0.value is not None:
  np.savez(ROOT/f'PARAMETER_DUAL_{lo:g}_{hi:g}.npz',L0=L0.value,L1=L1.value)
  out['moment_min_eigenvalues']=[float(np.linalg.eigvalsh(y.value).min()) for y in (Y0,Yend)]
(ROOT/f'PARAMETER_DUAL_{lo:g}_{hi:g}.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
