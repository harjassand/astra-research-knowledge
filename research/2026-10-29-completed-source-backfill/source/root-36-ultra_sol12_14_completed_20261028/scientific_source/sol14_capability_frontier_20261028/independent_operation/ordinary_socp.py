"""Strong ordinary comparator: the same secant bound as one SOCP.

The numerical solution only proposes nu. Its upper bound is then rebuilt
with exact rational arithmetic using the same input and verifier.
"""
from pathlib import Path
from fractions import Fraction as F
import json,time
START=time.monotonic()
import numpy as np
import cvxpy as cp
from box_compiler import compile_box,verify_certificate,dual_bound
OUT=Path(__file__).resolve().parent
IMPORT_SECONDS=time.monotonic()-START
rows=[]
for name in ['16_narrow','16_heterogeneous_width','4096_heterogeneous_width']:
    start=time.monotonic();raw=json.loads((OUT/f'INPUT_{name}.json').read_text())
    lo,hi,r=([F(z) for z in raw[k]] for k in ['lo','hi','r']);load_seconds=time.monotonic()-start
    start=time.monotonic();exact=compile_box(lo,hi,r);verify_certificate(lo,hi,r,exact);exact_seconds=time.monotonic()-start
    start=time.monotonic();k=len(lo)
    lf=np.asarray([float(z) for z in lo]);hf=np.asarray([float(z) for z in hi])
    density=np.asarray([float(c*(a+b)) for a,b,c in zip(lo,hi,r)])
    baseC=float(sum((c*a*b for a,b,c in zip(lo,hi,r)),F(0)))
    z=cp.Variable(k);nu=cp.Variable(nonneg=True);upper=cp.Variable(nonneg=True)
    positive=baseC-cp.sum(z)
    problem=cp.Problem(cp.Minimize(upper),[
        z>=cp.multiply(density-nu,lf),z>=cp.multiply(density-nu,hf),positive>=0,
        cp.SOC(upper+positive,cp.hstack([nu,upper-positive]))])
    problem.solve(solver='CLARABEL',tol_gap_abs=1e-10,tol_feas=1e-10,tol_gap_rel=1e-10,max_iter=300)
    proposal_seconds=time.monotonic()-start
    assert problem.status in ['optimal','optimal_inaccurate'] and nu.value is not None
    start=time.monotonic();nu_rational=F(round(float(nu.value)*2**40),2**40)
    certified,eta=dual_bound(lo,hi,r,nu_rational)
    assert certified>=exact['upper']
    certificate=dict(exact);certificate.update({'upper':certified,'nu':nu_rational,'eta':eta,
                                               'factor':certified/exact['lower']})
    verify_certificate(lo,hi,r,certificate)
    certification_seconds=time.monotonic()-start
    row={'name':name,'k':k,'status':problem.status,'numeric_solver_objective':problem.value,
         'certified_upper':str(certified),'exact_secant_upper':str(exact['upper']),
         'relative_excess':float(certified/exact['upper']-1),
         'nu_rational':str(nu_rational),'eta_rational':str(eta),
         'times':{'shared_input_loading':load_seconds,'exact_compiler_plus_verifier':exact_seconds,
                  'socp_conversion_build_and_solve':proposal_seconds,'rational_recovery_and_verification':certification_seconds}}
    rows.append(row);print(json.dumps(row),flush=True)
result={'status':'ORDINARY_SOCP_EXACT_CERTIFICATES_PASSED','cvxpy':cp.__version__,
        'import_seconds':IMPORT_SECONDS,'cases':rows,'module_seconds':time.monotonic()-START,
        'scope':'The SOCP is mathematically equivalent to the secant envelope. No advantage over all optimized ordinary implementations is claimed.'}
(OUT/'ORDINARY_SOCP.json').write_text(json.dumps(result,indent=2)+'\n')
