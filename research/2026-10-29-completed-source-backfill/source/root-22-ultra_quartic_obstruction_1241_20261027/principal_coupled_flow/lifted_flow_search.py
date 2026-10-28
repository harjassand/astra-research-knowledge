"""Convex relaxation for every real b and nonnegative gamma.
Lift beta=b*gamma to an independent free variable. Infeasibility of this
larger cone, if EXACTLY certified, rules out all original coupled flows.
Floating failure alone is not such a result.
"""
from pathlib import Path
from fractions import Fraction
import numpy as np,json,time
ROOT=Path(__file__).resolve().parent
SRC=Path('producer-workspace/principal')
d=np.load(SRC/'interfaces.npz');data=json.loads((ROOT/'PAIRINGS.json').read_text())
ej=[np.array([float(Fraction(t)) for t in row['mixed_coefficient_vector']]) for row in data['rows']]
p=np.array([1,1,16,-13,0,0,4,-4,0.])
rhs=d['D']@d['E']@p
T=np.column_stack([d['D']@d['P'],d['D']@d['Ed'],-d['D']@ej[0],d['D']@ej[1]])
inv=np.linalg.pinv(T,rcond=1e-11);anchor=inv@rhs;proj=np.eye(303)-inv@T
ij=np.triu_indices(24);wt=np.where(ij[0]==ij[1],1.,np.sqrt(2.))
def matrix(vec):
    M=np.zeros((24,24));M[ij]=vec/wt;M[(ij[1],ij[0])]=vec/wt
    return M
start=time.monotonic();y=anchor.copy();dual=np.zeros(303)
for iteration in range(60000):
    x=anchor+proj@(y-dual)
    vals,V=np.linalg.eigh(matrix(x[:300]+dual[:300]))
    positive=(V*np.maximum(vals,0))@V.T
    new=np.r_[positive[ij]*wt,max(0.,x[300]+dual[300]),x[301:]+dual[301:]]
    dual+=x-new;primal=float(np.linalg.norm(x-new));change=float(np.linalg.norm(new-y));y=new
    if primal<1e-9 and change<1e-9:break
lam=-d['D'].T@inv.T@dual;lam/=np.linalg.norm(lam)
Y=np.array([[lam[21*list(__import__('itertools').combinations_with_replacement(range(4),2)).index(tuple(sorted((i//6,j//6))))+list(__import__('itertools').combinations_with_replacement(range(6),2)).index(tuple(sorted((i%6,j%6))))] for j in range(24)] for i in range(24)])
out={'status':'NUMERICAL_LIFTED_CONE_EXPLORATION_ONLY','iterations':iteration+1,
 'primal':primal,'change':change,'seconds':time.monotonic()-start,
 'dual_pair_F':float(lam@(d['E']@p)),'dual_pair_det':float(lam@d['Ed']),
 'dual_pair_mixed_F':float(lam@ej[0]),'dual_pair_mixed_det':float(lam@ej[1]),
 'dual_min_eigenvalue':float(np.linalg.eigvalsh(Y)[0]),
 'scope':'Numerical relaxation only; exact rational certificate is required before any infeasibility theorem.'}
np.savez(ROOT/'LIFTED_NUMERIC.npz',x=x,dual=dual,lam=lam,T=T,rhs=rhs)
(ROOT/'LIFTED_NUMERIC.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
