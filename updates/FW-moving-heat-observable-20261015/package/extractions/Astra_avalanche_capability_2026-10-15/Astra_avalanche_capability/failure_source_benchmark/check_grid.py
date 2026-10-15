import json
import numpy as np
from pathlib import Path
from verify_avalanche_clock import clock,independent_Q
from scipy.linalg import expm
rng=np.random.default_rng(2026101502)
rows=[]
for n in [5,10,100]:
 for f0 in [.125,.15,.175]:
  for T in [.05,.1,.15]:
   delta=[];rat=[];av=[];no=[];initial=0
   for j in range(2000):
    h=rng.uniform(size=n);E=rng.exponential(size=n)*np.exp(h/T)
    a,e=clock(h,f0,T,E=E);b,_=clock(h,f0,T,E=E,avalanche=False)
    assert a<=b+1e-9*max(1,b)
    av.append(a);no.append(b);delta.append(b-a);initial+=a==0
   rows.append({'n':n,'f0':f0,'T':T,'N':2000,'initial_collapse_fraction':initial/2000,'avalanche_mean':float(np.mean(av)),'no_avalanche_mean':float(np.mean(no)),'mean_time_added_without_closure':float(np.mean(delta)),'paired_difference_SE':float(np.std(delta,ddof=1)/np.sqrt(2000))})
Path(__file__).with_name('grid_results.json').write_text(json.dumps(rows,indent=2))
print(rows[-1])
