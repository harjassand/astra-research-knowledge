#!/usr/bin/env python3
"""Floating evaluation of the proved fixed-temporal-span residual floor."""
import hashlib,json
from pathlib import Path
import numpy as np
from scipy.integrate import quad
OUT=Path(__file__).parent

def compute():
    records=[];v=2.1;T=.6
    for nodes in [[0,T],[0,T/2,T],[0,T/3,2*T/3,T]]:
        nodes=np.array(nodes)
        C=v/(1-1j*(nodes[None,:]-nodes[:,None]))
        def tau(t):
            c=v/(1-1j*(t-nodes))
            return max(0.,float(v-np.vdot(c,np.linalg.solve(C,c)).real))
        tt=np.linspace(0,T,3001);ta=np.array([tau(t) for t in tt])
        val,err=quad(lambda t:12*np.sin(np.pi*t/T)**2*(-np.expm1(-tau(t)))/np.sqrt(2),0,T,epsabs=1e-12)
        records.append({'nodes':nodes.tolist(),'maximum_tau_on_3001_grid':float(ta.max()),
                        'residual_integral_floor_float':val,'quad_error_estimate':err,
                        'kernel_gram_condition':float(np.linalg.cond(C))})
    return {'records':records,'scope':'Analytic floor is proved; these numerical evaluations are not outward interval certificates.',
            'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
if __name__=='__main__':
    r=compute();(OUT/'temporal_span_floor_receipt.json').write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps(r,indent=2))
