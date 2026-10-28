"""A pure-target canonical mixed-flow certificate, without gamma lifting."""
from pathlib import Path
import sys,json,time
import numpy as np
import cvxpy as cp
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent))
from maps import load
from models import symmetric


def main():
    d=load();flow=np.load(ROOT/'FLOW_MAPS.npz');b=cp.Variable();r=cp.Variable(300);omega=cp.Variable(45);margin=cp.Variable()
    R=symmetric(r,24)
    equality=d['G']@r==flow['ef']+b*flow['ejf']+d['ON']@omega
    problem=cp.Problem(cp.Maximize(margin),[equality,R-margin*np.eye(24)>>0])
    start=time.monotonic();problem.solve(solver='CLARABEL',max_iter=160,tol_gap_abs=1e-10,tol_gap_rel=1e-10,tol_feas=1e-10)
    out={'status':'NUMERICAL_PURE_FLOW_ONLY','solver_status':problem.status,
         'margin':None if margin.value is None else float(margin.value),'b':None if b.value is None else float(b.value),
         'seconds':time.monotonic()-start,'scope':'No QC or impossibility conclusion before exact reconstruction.'}
    if r.value is not None:
        np.savez(ROOT/'PURE_FLOW_NUMERIC.npz',b=b.value,gram=R.value,omega=omega.value,dual=equality.dual_value)
        out['equality_residual']=float(np.max(np.abs(equality.violation())))
    (ROOT/'PURE_FLOW_SEARCH.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))


if __name__=='__main__':main()
