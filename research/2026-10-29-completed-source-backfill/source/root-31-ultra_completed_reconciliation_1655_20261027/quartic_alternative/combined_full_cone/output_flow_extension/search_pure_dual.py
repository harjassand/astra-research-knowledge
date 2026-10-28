"""Uniform all-b/all-gamma pure-flow dual; no parameter sampling."""
from pathlib import Path
import sys,json,time
import numpy as np
import cvxpy as cp
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent))
from maps import load


def main():
    d=load();f=np.load(ROOT/'FLOW_MAPS.npz');old=np.load(ROOT/'PURE_FLOW_NUMERIC.npz')['dual']
    pairs={name:float(old@f[name]) for name in ['ef','ejf','ed','ejd']}
    lam=cp.Variable(210);moment=cp.reshape(lam[d['heat_indices']],(24,24),order='C')
    problem=cp.Problem(cp.Minimize(lam@f['ef']),[moment>>0,cp.trace(moment)==1,
                 d['ON'].T@lam==0,lam@f['ejf']==0,lam@f['ejd']==0,lam@f['ed']>=0])
    start=time.monotonic();problem.solve(solver='CLARABEL',max_iter=160,tol_gap_abs=1e-10,tol_gap_rel=1e-10,tol_feas=1e-10)
    out={'status':'NUMERICAL_PURE_PARAMETER_DUAL_ONLY','solver_status':problem.status,
         'objective':float(problem.value),'seconds':time.monotonic()-start,
         'initial_gamma0_dual_pairings':pairs,'scope':'Exactnegative would exclude every real b and nonnegative gamma for the pure-target canonical flow; no combined arbitrary-component claim.'}
    np.savez(ROOT/'PURE_DUAL_NUMERIC.npz',lam=lam.value)
    (ROOT/'PURE_DUAL_SEARCH.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))


if __name__=='__main__':main()
