"""One constant common dual annihilating the entire mixed energy map."""
from pathlib import Path
import sys,json,time
from fractions import Fraction as F
import numpy as np
import cvxpy as cp
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent))
from maps import load


def main():
    d=load();flow=np.load(ROOT/'FLOW_MAPS.npz');target=json.loads((ROOT/'SYMMETRIC_TARGET.json').read_text())
    p=np.array([float(F(c)) for c in target['coefficients']]);lp=cp.Variable(658);lh=cp.Variable(210)
    Mp=cp.reshape(lp[d['pc_indices']],(60,60),order='C');Mh=cp.reshape(lh[d['heat_indices']],(24,24),order='C')
    g=d['B'].T@lp
    constraints=[Mp>>0,Mh>>0,d['A'][:,1830:].T@lp==0,d['ON'].T@lh==0,
                 g==d['E'].T@lh,flow['EJ'].T@lh==0,cp.trace(Mp)+cp.trace(Mh)==1]
    problem=cp.Problem(cp.Minimize(p@g),constraints);start=time.monotonic()
    problem.solve(solver='CLARABEL',max_iter=160,tol_gap_abs=1e-10,tol_gap_rel=1e-10,tol_feas=1e-10)
    out={'status':'NUMERICAL_UNIFORM_COMMON_DUAL_ONLY','solver_status':problem.status,
         'objective':float(problem.value),'seconds':time.monotonic()-start,
         'scope':'Exactnegative would exclude PC1+all canonical mixedflow heat cones, not arbitrary unknown-component/unknown-operator averages.'}
    np.savez(ROOT/'UNIFORM_COMMON_NUMERIC.npz',lp=lp.value,lh=lh.value)
    (ROOT/'UNIFORM_COMMON_SEARCH.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))


if __name__=='__main__':main()
