"""Oracle initialization and invariance diagnostics; NOT acquisition algorithms."""
import json,time
import numpy as np
from scipy.optimize import least_squares
from benchmark import OUT,setup,response
rows=[]
for path in sorted(OUT.glob('m*_noise0_*.npz')):
 d=np.load(path);m=len(d['a']);masks,ii,jj=setup(m);B,a=d['B'],d['a'];train=d['train'];fitids=train[masks[train].sum(1)>=2];gt=d['truth']-.3
 dual=B.T*a[None,:]/a[:,None]
 _,J=response(B[ii,jj],a,masks[fitids],ii,jj,True);sv=np.linalg.svd(J,compute_uv=False)
 p0=B[ii,jj]+np.random.default_rng(999).normal(0,.005,len(ii))
 t=time.perf_counter()
 opt=least_squares(lambda p:response(p,a,masks[fitids],ii,jj)-gt[fitids],p0,jac=lambda p:response(p,a,masks[fitids],ii,jj,True)[1],bounds=(-.6,.6),max_nfev=1000,ftol=1e-13,xtol=1e-13,gtol=1e-13)
 rows.append(dict(tag=path.stem,jacobian_sigma_min=float(sv[-1]),jacobian_condition=float(sv[0]/sv[-1]),dual_parameter_difference=float(np.linalg.norm(dual-B)),dual_max_response_difference=float(np.max(abs(response(dual[ii,jj],a,masks,ii,jj)-gt))),oracle_near_init_max_response_error=float(np.max(abs(response(opt.x,a,masks,ii,jj)-gt))),oracle_near_init_nfev=int(opt.nfev),oracle_near_init_seconds=time.perf_counter()-t))
(OUT/'diagnostics.json').write_text(json.dumps(rows,indent=2))
print('diagnostic rows',len(rows))
