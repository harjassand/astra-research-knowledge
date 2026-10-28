"""Affine gamma dual, exact mixed annihilation, no b/gamma grid inference."""
from pathlib import Path
from fractions import Fraction as F
import sys,json,time
import numpy as np
import cvxpy as cp
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent))
from maps import load


def main():
    d=load();flow=np.load(ROOT/'FLOW_MAPS.npz');G=float(F(json.loads((ROOT/'GAMMA_BOUND.json').read_text())['used_rational_upper_bound']))
    L0=cp.Variable(210);L1=cp.Variable(210);margin=cp.Variable()
    Y0=cp.reshape(L0[d['heat_indices']],(24,24),order='C');Yend=cp.reshape((L0+L1)[d['heat_indices']],(24,24),order='C')
    q0=L0@flow['ef'];q1=L1@flow['ef']-G*(L0@flow['ed']);q2=-G*(L1@flow['ed'])
    constraints=[d['ON'].T@L0==0,d['ON'].T@L1==0,
                 L0@flow['ejf']==0,L1@flow['ejf']-G*(L0@flow['ejd'])==0,L1@flow['ejd']==0,
                 Y0>>1e-7*np.eye(24),Yend>>1e-7*np.eye(24),cp.trace(Y0+Yend)==1,
                 q0<=-margin,q0+q1/2<=-margin,q0+q1+q2<=-margin]
    problem=cp.Problem(cp.Maximize(margin),constraints);start=time.monotonic()
    problem.solve(solver='CLARABEL',max_iter=160,tol_gap_abs=1e-10,tol_gap_rel=1e-10,tol_feas=1e-10)
    out={'status':'NUMERICAL_AFFINE_GAMMA_DUAL_ONLY','solver_status':problem.status,
         'gamma_upper':G,'margin':None if margin.value is None else float(margin.value),'seconds':time.monotonic()-start,
         'scope':'No impossibility statement before exact rational reconstruction over the whole interval.'}
    if L0.value is not None:np.savez(ROOT/'PARAMETER_FAMILY_NUMERIC.npz',L0=L0.value,L1=L1.value)
    (ROOT/'PARAMETER_FAMILY_SEARCH.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))


if __name__=='__main__':main()
