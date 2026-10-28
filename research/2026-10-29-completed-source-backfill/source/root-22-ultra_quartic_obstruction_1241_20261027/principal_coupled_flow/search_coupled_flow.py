"""Exploratory affine/PSD feasibility for a skew output-coupled heat flow.
Numerics are not a mathematical certificate, and failed convergence is not
an infeasibility theorem. Uses read-only cleared source coefficient maps.
"""
from pathlib import Path
import numpy as np,json,time,sys
ROOT=Path(__file__).resolve().parent
SRC=Path('producer-workspace/principal')
d=np.load(SRC/'interfaces.npz')
pair=json.loads((ROOT/'PAIRINGS.json').read_text())
mixed=[np.array([float(__import__('fractions').Fraction(x)) for x in row['mixed_coefficient_vector']]) for row in pair['rows']]
p=np.array([1,1,16,-13,0,0,4,-4,0.])
ij=np.triu_indices(24);weights=np.where(ij[0]==ij[1],1.,np.sqrt(2.))

def matrix(v):
    M=np.zeros((24,24));M[ij]=v/weights;M[(ij[1],ij[0])]=v/weights
    return M

start=time.monotonic();results=[]
gammas=[float(sys.argv[1])] if len(sys.argv)>1 else [0,1,2,4,8]
for gamma in gammas:
    tick=time.monotonic()
    rhs=d['D']@(d['E']@p-gamma*d['Ed'])
    ej=mixed[0]-gamma*mixed[1]
    T=np.column_stack([d['D']@d['P'],-d['D']@ej])
    inverse=np.linalg.pinv(T,rcond=1e-11)
    anchor=inverse@rhs;projection=np.eye(301)-inverse@T
    y=anchor.copy();dual=np.zeros(301)
    for iteration in range(30000):
        x=anchor+projection@(y-dual)
        vals,V=np.linalg.eigh(matrix(x[:-1]+dual[:-1]))
        positive=(V*np.maximum(vals,0))@V.T
        new=np.r_[positive[ij]*weights,x[-1]+dual[-1]]
        dual+=x-new
        primal=float(np.linalg.norm(x-new));change=float(np.linalg.norm(new-y));y=new
        if primal<1e-9 and change<1e-9:break
    record={'gamma_fixed':gamma,'coupled_flow_b':float(x[-1]),
      'iterations':iteration+1,'primal_residual':primal,'change':change,
      'affine_residual':float(np.linalg.norm(T@x-rhs)),
      'minimum_gram_eigenvalue':float(np.linalg.eigvalsh(matrix(x[:-1]))[0]),
      'seconds':time.monotonic()-tick,'status':'NUMERICAL_EXPLORATION_ONLY'}
    np.savez(ROOT/f'coupled_gamma_{gamma:g}.npz',x=x,dual=dual,T=T,rhs=rhs)
    results.append(record);print(json.dumps(record),flush=True)
    (ROOT/'NUMERICAL_SEARCH.json').write_text(json.dumps({'results':results,'seconds':time.monotonic()-start,
      'scope':'PSD affine numerical feasibility only; no exact QC/positivity/infeasibility conclusion'},indent=2)+'\n')
