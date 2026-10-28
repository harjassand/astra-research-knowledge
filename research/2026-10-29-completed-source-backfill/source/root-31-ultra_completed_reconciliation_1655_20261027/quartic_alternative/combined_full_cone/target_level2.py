"""One justified higher-support attempt after exact level1+heat exclusion."""
from pathlib import Path
from fractions import Fraction as F
import json,sys,time
import numpy as np
import scipy.sparse as sp
import cvxpy as cp
from maps import ROOT,SOL8
from models import symmetric


def main():
    sys.path.insert(0,str(SOL8/'principal_combined_quartic'))
    from compile_hierarchy import compile_level
    from verify_dual import plus,times,var,invariants,scale
    p=list(map(F,json.loads((ROOT/'heat_normal_extreme_ROC.json').read_text())['coefficients']))
    u,v,w,q=invariants([var(i) for i in range(4)])
    basis=[times(u,u),times(v,v),times(u,v),times(w,w),times(u,w),times(v,w),times(q,u),times(q,v),times(q,w)]
    energy=plus(*(scale(f,c) for f,c in zip(basis,p)))
    data=compile_level({e[:4]:c for e,c in energy.items()},2)
    (ROOT/'LEVEL2_INTERFACE.json').write_text(json.dumps(data,separators=(',',':'))+'\n')
    rr=[];cc=[];dd=[]
    for i,row in enumerate(data['rows']):
        for j,c in row['entries']:rr.append(i);cc.append(j);dd.append(float(F(c)))
    n=data['features'];size=len(data['gram_upper_pairs']);v=cp.Variable(size+10);rho=cp.Variable()
    A=sp.coo_matrix((dd,(rr,cc)),shape=(len(data['rows']),size+10)).tocsr()
    b=np.array([float(F(row['rhs'])) for row in data['rows']]);weights=np.sqrt(np.asarray(A.multiply(A).sum(axis=1)).ravel())
    Q=symmetric(v[:size],n);problem=cp.Problem(cp.Maximize(rho),[sp.diags(1/weights)@A@v==b/weights,Q-rho*np.eye(n)>>0])
    start=time.monotonic();problem.solve(solver='CLARABEL',max_iter=160,tol_gap_abs=1e-9,tol_gap_rel=1e-9,tol_feas=1e-9)
    out={'status':'ONE_NUMERICAL_LEVEL2_ATTEMPT_ONLY','features':n,'equations':len(data['rows']),
         'solver_status':problem.status,'margin':None if rho.value is None else float(rho.value),
         'seconds':time.monotonic()-start,'scope':'No PC/QC or infeasibility inference before exact reconstruction.'}
    if v.value is not None:
        np.savez(ROOT/'LEVEL2_NUMERIC.npz',values=v.value,gram=Q.value,rho=rho.value)
        out['max_affine_residual']=float(np.max(np.abs(A@v.value-b)))
    (ROOT/'LEVEL2_ATTEMPT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))


if __name__=='__main__':main()
