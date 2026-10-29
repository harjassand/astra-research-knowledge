"""Independent direct physical ODE step-refinement reference, float64 not certificate."""
import json,time
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp

def rhs(t,z):
 a=z[:3];b=z[3:]
 return [a[i]*(b[(i+1)%3]-b[i]) for i in range(3)]+[2*(a[i]**2-a[i-1]**2) for i in range(3)]
if __name__=='__main__':
 records=[];start=time.perf_counter()
 for denominator in [256,512]:
  sol=solve_ivp(rhs,(0,32),[1,2,3,0,1,-1],method='DOP853',rtol=2.3e-14,atol=2.3e-15,max_step=1/denominator,t_eval=[16,32]);assert sol.success
  record=dict(max_step=1/denominator,nfev=sol.nfev,states={str(t):list(map(float,sol.y[:,j])) for j,t in enumerate([16,32])})
  records.append(record);Path(__file__).with_suffix('.json').write_text(json.dumps(dict(warning='Float64 direct ODE step-refinement diagnostic; no rigorous error enclosure',records=records,seconds=time.perf_counter()-start),indent=2));print(json.dumps(record),flush=True)
