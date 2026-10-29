"""C1 algebraic weight chosen for an analytic second-derivative receiver.

No optimization of weight coefficients. A single scalar maximization and
one fixed-location resolution check remain diagnostics, never admission.
"""
from pathlib import Path
import json,time
from scipy.optimize import minimize_scalar
from suspect_resolution import fixed
from smooth_weight import phi


def main():
    start=time.perf_counter();records=[]
    def obj(v):
        r=fixed(float(v),160,128,weight=phi)
        records.append(r);return -r['row']
    anchors=[obj(v) for v in (0.,2.,5.,8.)]
    fit=minimize_scalar(obj,bounds=(2.,5.),method='bounded',options={'xatol':.003,'maxiter':30})
    control=fixed(float(fit.x),320,256,weight=phi)
    out={'status':'FLOAT_ONLY','weight':'smooth_weight.py exact rational formula',
         'anchors_negative':anchors,'records':records,
         'maximum':{'v':float(fit.x),'row':float(-fit.fun)},
         'fixed_resolution':control,'seconds':time.perf_counter()-start,
         'continuum_admission':False}
    Path(__file__).with_name('SMOOTH_WEIGHT_PREVIEW.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='records'},indent=2))


if __name__=='__main__': main()
