"""One canonical output-coupled flow acquisition, genuinely new target."""
from pathlib import Path
import os,sys,time,json
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
os.environ.setdefault('OMP_NUM_THREADS','1')
import numpy as np
import cvxpy as cp
OUT=Path(__file__).resolve().parent
SRC=OUT.parents[2]/'sol8_opportunity_selection_20261027/quartic_alternative/combined_full_cone'
sys.path.insert(0,str(SRC))
from maps import load
from models import symmetric
d=load();flow=np.load(SRC/'output_flow_extension/FLOW_MAPS.npz')
p=np.array([1,1,12.08,-10.08,0,0,3.96,-3.96,0])
b=cp.Variable();r=cp.Variable(300);omega=cp.Variable(45);margin=cp.Variable()
R=symmetric(r,24);eq=d['G']@r==d['E']@p+b*(flow['EJ']@p)+d['ON']@omega
problem=cp.Problem(cp.Maximize(margin),[eq,R-margin*np.eye(24)>>0,margin<=1])
start=time.monotonic()
problem.solve(solver='CLARABEL',max_iter=160,tol_gap_abs=1e-10,tol_gap_rel=1e-10,tol_feas=1e-10)
out={'status':'NUMERICAL_ACQUISITION_ONLY','solver_status':problem.status,'seconds':time.monotonic()-start,'scope':'No QC or class exclusion theorem without exact reconstruction.'}
if margin.value is not None:
    out.update(margin=float(margin.value),b=float(b.value),equality_error=float(np.max(np.abs(eq.violation()))))
    np.savez(OUT/'coupled.npz',b=b.value,r=r.value,omega=omega.value,dual=eq.dual_value,margin=margin.value)
(OUT/'COUPLED.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out))
