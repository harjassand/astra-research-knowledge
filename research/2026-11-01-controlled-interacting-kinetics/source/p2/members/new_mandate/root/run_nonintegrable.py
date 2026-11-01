"""Reproduce the large nonintegrable one-insertion calculation and refinement."""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
from pathlib import Path
import json,time,numpy as np
from gaussian_kinetics import model,mean_reference,first_correction

n=64
nu=np.full(n,.001);nu[:2]=1
m=model(np.full(n,-.4),nu)
ref=mean_reference(m,1e-10)
start=time.perf_counter()
c=first_correction(m,160,32,1e-10)
mu=c['coefficient']/ref['W'];epsilon=.7
lo=ref['mean']/(1+epsilon*mu)
hi=ref['mean']*(1-epsilon*mu/(1+epsilon))
out={'model':'64-site even wall ring; betaJ=-0.4; nu0=nu1=1, others0.001; a_i=1+0.7 eta_(i+2)',
     'W0':ref['W'],'reference_mean':ref['mean'],'reference_log10_pi':m['logpi']/np.log(10),
     'first_correction':c,'mu':mu,'epsilon':epsilon,'mean_lower_numerical':lo,
     'mean_upper_numerical':hi,'enclosure_width_relative_to_lower':hi/lo-1,
     'seconds':time.perf_counter()-start,
     'qualification':'Operator enclosure proved; numerical quadrature refined, not directed rounding.'}
start=time.perf_counter();c2=first_correction(m,256,64,1e-11)
out['further_refinement']={**c2,'seconds':time.perf_counter()-start,
                         'relative_coefficient_change':abs(c2['coefficient']/c['coefficient']-1)}
mu2=c2['coefficient']/ref['W'];out['refined_mu']=mu2
out['refined_mean_lower_numerical']=ref['mean']/(1+epsilon*mu2)
out['refined_mean_upper_numerical']=ref['mean']*(1-epsilon*mu2/(1+epsilon))
Path(__file__).with_name('nonintegrable_result.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
