"""Finite-record identifiability diagnostic for the declared exponential model.
No physical trajectory extension and no statistical error bars.
"""
from pathlib import Path
import csv,json,time,resource
import numpy as np
from scipy.optimize import minimize_scalar
p=Path(__file__).parent;src=p.parent/'nitrite_finishing/dataset';start=time.perf_counter()
rows=list(csv.reader((src/'Figure_6A.csv').open(encoding='utf-8-sig')))[1:]
x=[];y=[]
for row in rows:
 try:x.append(float(row[8]));y.append(float(row[9]))
 except (ValueError,IndexError):pass
x=np.array(x);y=np.array(y);out=[]
for A in [145.,250.,500.,1000.,10000.]:
 fun=lambda logk:np.mean((y-A*(-np.expm1(-np.exp(logk)*x)))**2)
 fit=minimize_scalar(fun,bounds=(-20,0),method='bounded',options={'xatol':1e-12})
 out.append({'fixed_A_mM':A,'k_s-1':float(np.exp(fit.x)),'RMS_mM':float(np.sqrt(fit.fun)),'violates_500mM_closed_inventory_ceiling':A>500})
r=json.load((p/'dataset_result.json').open());cal=r['calibration'];equiv=max(abs(v) for v in cal['residuals'])/cal['ratio_vs_Ceff_slope']
res={'source':'Figure_6A.csv column0.5M','profile':out,'largest_calibration_fit_residual_equivalent_mM':equiv,'bias_mM_that_removes_air2700_gt_750':r['controls'][0]['value_at_2700s_linear_interpolation']-750,'scope':'Profiles challenge asymptote identification, not statistical confidence. Values above500mM are deliberately rejected physical extrapolations if tracer-inventory contract holds. Calibration residual is not a guaranteed uncertainty bound or cross-matrix calibration.','elapsed_s':time.perf_counter()-start,'peak_RSS_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
(p/'profile_result.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps(res,indent=2))
