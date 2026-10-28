"""Actual combined SOS-support/closed-heat construction attempt.
These are ordinary sufficient methods. Floating failure proves no obstruction;
floating success must be reconstructed before a QC claim is made.
"""
from pathlib import Path
import sys,time,json
import numpy as np
import cvxpy as cp
from itertools import combinations_with_replacement
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent/'quartic_alternative'))
from poly_support import build
SRC=Path('producer-workspace/principal')
data=np.load(SRC/'interfaces.npz')
tau=float(sys.argv[1]) if len(sys.argv)>1 else 11.3
K=np.zeros((9,4));K[0,0]=K[1,0]=1;K[2,1]=K[3,2]=1;K[6,3]=1;K[7,3]=-1
p=np.array([1,1,tau,3-tau,0,0,4,-4,0.])
M,b,terms,monoms,*_=build([str(t) for t in p],multiplier='candidate')
# All support maps use the same monomial rows and candidate multiplier basis.
bs=[]
for col in K.T:
    mk,bk,tk,mn,*_=build([str(t) for t in col],multiplier='candidate')
    assert np.array_equal(M,mk) and mn==monoms
    bs.append(bk)
B=np.array(bs).T
Q=cp.Variable((26,26),symmetric=True)
R=cp.Variable((24,24),symmetric=True)
theta=cp.Variable(2);h=cp.Variable(4);omega=cp.Variable(data['ON'].shape[1])
margin=cp.Variable()
qvec=cp.hstack([Q[i,j]*(1 if i==j else np.sqrt(2)) for i,j,_ in terms]+[theta])
xp=list(combinations_with_replacement(range(4),2));zp=list(combinations_with_replacement(range(6),2))
gmap=np.zeros((210,576))
for i in range(24):
    for j in range(24):
        k=21*xp.index(tuple(sorted((i//6,j//6))))+zp.index(tuple(sorted((i%6,j%6))))
        gmap[k,24*i+j]+=1
constraints=[M@qvec+B@h==b,
 data['E']@K@h+data['ON']@omega==gmap@cp.reshape(R,(576,),order='C'),
 Q >> margin*np.eye(26),R >> 0,margin<=1]
start=time.monotonic();problem=cp.Problem(cp.Maximize(margin),constraints)
problem.solve(solver='CLARABEL',max_iter=100,tol_gap_abs=1e-8,tol_feas=1e-8,tol_gap_rel=1e-8)
out={'status':'NUMERICAL_COMBINED_SUFFICIENT_METHOD_ATTEMPT','tau':tau,
 'solver_status':problem.status,'support_margin':None if margin.value is None else float(margin.value),
 'seconds':time.monotonic()-start,
 'scope':'No exact QC or infeasibility claim from solver status. Combined operation is established machinery; target is extension beyond both separate certificate classes.'}
if h.value is not None:
    np.savez(ROOT/f'combined_{tau:g}.npz',Q=Q.value,R=R.value,theta=theta.value,h=h.value,omega=omega.value)
    out['heat_component_coefficients']=h.value.tolist()
    out['minimum_eigenvalues']=[float(np.linalg.eigvalsh(q.value).min()) for q in (Q,R)]
    out['maximum_equality_residual']=max(float(np.max(np.abs(c.violation()))) for c in constraints[:2])
(ROOT/f'combined_{tau:g}.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
