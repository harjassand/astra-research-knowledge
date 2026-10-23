"""Does passive internal axial conduction relax a temperature-limited regenerator?
Thermal-only mechanism test, not finished NOx or hardware prediction.
"""
import time,json,resource
from pathlib import Path
from scipy.optimize import brentq
from periodic_gate import run
root=Path(__file__).resolve().parent;start=time.monotonic();rows=[]
for N in [40,100]:
 for lam in [0.,.001,.01,.03,.1,.3,1.]:
  for b in [.001,.03]:
   def f(ntu):return run(N,ntu,b,axial=lam)['maximum_solid_theta_sampled']-(2500-300)/2800
   if f(40)<0:nt=40.
   else:nt=brentq(f,.1,40,xtol=1e-6)
   r=run(N,nt,b,trace=True,axial=lam);r['cap_root_or_NTU40_limit']=True;rows.append(r);print(N,lam,b,nt,r['effectiveness'],flush=True)
(root/'axial_challenge.json').write_text(json.dumps({'rows':rows,'wall_s':time.monotonic()-start,'max_rss_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'scope':'thermal submodel only; finite-time peaks sampled not continuous certified; no chemistry/material benefit claimed'},indent=2)+'\n')
