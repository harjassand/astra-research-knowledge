"""A changed norm, not an extra Gaussian exponent grid.

The analytic scalar weight is 1+(s-2)(5-s)/9 on[2,5], 1 elsewhere.
It is between1 and5/4. Its boundedness pays nonlinear weight ratios
without a new source/invariant/control oracle. This file is diagnostic.
"""
from pathlib import Path
import json, time
import numpy as np
from scipy.optimize import minimize_scalar
from suspect_resolution import fixed


def phi(v):
    return 1+np.where((v>=2)&(v<=5),(v-2)*(5-v)/9,0)


def main():
    begin=time.perf_counter();records=[];maxima=[]
    def f(v):
        r=fixed(float(v),128,96,weight=phi)
        records.append(r);return -r['row']
    for bracket in ((0.,2.),(2.,5.),(5.,8.)):
        fit=minimize_scalar(f,bounds=bracket,method='bounded',
                            options={'xatol':.003,'maxiter':30})
        maxima.append({'bracket':bracket,'success':bool(fit.success),
                       'v':float(fit.x),'row':float(-fit.fun)})
    for v in (0.,2.,5.,8.):
        f(v)
    worst=max(records,key=lambda r:r['row'])
    finer=fixed(worst['v'],256,192,weight=phi)
    result={'status':'CHANGED_NORM_FLOAT_PREVIEW_NOT_A_CERTIFICATE',
            'beta':'3/4','phi':'1+(v-2)(5-v)/9 on[2,5], else1',
            'phi_min':'1','phi_max':'5/4','maxima':maxima,
            'records':records,'fixed_worst_resolution':finer,
            'seconds':time.perf_counter()-begin,'continuum_admission':False}
    Path(__file__).with_name('PERRON_WEIGHT_PREVIEW.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='records'},indent=2))


if __name__=='__main__':
    main()
