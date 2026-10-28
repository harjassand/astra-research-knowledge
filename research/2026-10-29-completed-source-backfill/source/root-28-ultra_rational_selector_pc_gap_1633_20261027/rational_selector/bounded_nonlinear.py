"""Bounded acquisition of the first genuine nonlinear support selector.

The earlier unstructured numerical control was terminated without a result;
the control is now exact algebra. This completes the same target attempt.
"""
from pathlib import Path
from itertools import combinations_with_replacement as cw
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
os.environ.setdefault('OMP_NUM_THREADS','1')
import json
import time
import numpy as np
import sympy as s
import scipy.sparse as sp
import cvxpy as cp

ROOT=Path(__file__).resolve().parent


def main():
    started=time.monotonic()
    d=np.load(ROOT/'NONLINEAR_LITERAL_MAPS.npz')
    gram=sp.coo_matrix((d['gram_values'],(d['gram_rows'],d['gram_cols'])),shape=(3185,16290)).tocsr()
    sr,sc,sv=[],[],[]
    for col,(i,j) in enumerate(cw(range(180),2)):
        sr.append(i*180+j);sc.append(col);sv.append(1)
        if i!=j:sr.append(j*180+i);sc.append(col);sv.append(1)
    sym=sp.coo_matrix((sv,(sr,sc)),shape=(32400,16290)).tocsr()
    q=cp.Variable(16290);selector=cp.Variable(6);rho=cp.Variable()
    point=json.loads((ROOT.parent/'common_cone_review/EXACT_SYMMETRIC_TARGET.json').read_text())
    coeff=np.array([float(s.Rational(v)) for v in point['coefficients']])
    matrix=cp.reshape(sym@q,(180,180),order='C')
    eq=gram@q+d['C']@selector==d['E']@coeff
    problem=cp.Problem(cp.Maximize(rho),[eq,matrix-rho*np.eye(180)>>0,rho<=1])
    problem.solve(solver='SCS',use_indirect=True,max_iters=12000,
                  eps_abs=1e-7,eps_rel=1e-7,time_limit_secs=60)
    out={'status':'BOUNDED_NONLINEAR_SELECTOR_ACQUISITION_ONLY',
         'solver_status':problem.status,
         'margin':None if rho.value is None else float(rho.value),
         'max_affine_residual':None if q.value is None else float(np.max(abs(eq.violation()))),
         'seconds':time.monotonic()-started,
         'solver_stats':{'iterations':problem.solver_stats.num_iters,
                         'solve_seconds':problem.solver_stats.solve_time},
         'previous_control_run':'UNSTRUCTURED_CLARABEL_CONTROL_TERMINATED_WITHOUT_RESULT; replaced by exact analytic R>=I/4 control',
         'scope':'Numerical suggestion only. No PC or class-infeasibility claim without exact reconstruction.'}
    if q.value is not None:
        np.savez(ROOT/'BOUNDED_NONLINEAR_NUMERIC.npz',q=q.value,selector=selector.value,
                 equality_dual=eq.dual_value,rho=rho.value)
    (ROOT/'BOUNDED_NONLINEAR_ACQUISITION.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))


if __name__=='__main__':main()
