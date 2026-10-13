"""Exact rational verification of final kinetic intervals.
Floating-point solves provide candidate fields only. Every residual is recomputed
using Fraction arithmetic for the exact rational soft-East model. M-matrix
comparison then produces rigorous endpoints without a spectral-gap assumption.
"""
from pathlib import Path
ROOT = Path(__file__).resolve().parent
import sys,time,json
from fractions import Fraction as F
from decimal import Decimal,localcontext,ROUND_FLOOR,ROUND_CEILING
import numpy as np
from scipy.sparse.linalg import spsolve
from probe import soft_east,matrix


def outward(x,lower,places=14):
    with localcontext() as ctx:
        ctx.prec=places
        ctx.rounding=ROUND_FLOOR if lower else ROUND_CEILING
        return str(Decimal(x.numerator)/Decimal(x.denominator))

def certify_field(model,fac,vec):
    q=F(str(model['q']));eps=F(str(model['softness']));n=model['L']-1;N=1<<n
    v=[F(float(x)) for x in vec] # exact IEEE-754 rational values
    if min(v)<=0:raise ArithmeticError('candidate is not positive')
    residual=[F(-1) for _ in range(N)]
    for e,(i,j) in enumerate(zip(model['a'],model['b'])):
        i=int(i);j=int(j)
        if fac[e]==1:ff=F(1)
        elif fac[e]==model['softness']:ff=eps
        else:raise ValueError('This verifier expects binary endpoint facilitation factors.')
        if j<0:
            residual[i]+=q*ff*v[i]
        else:
            dv=v[i]-v[j]
            residual[i]+=q*ff*dv
            residual[j]-=(1-q)*ff*dv
    delta=max(abs(x) for x in residual)
    if delta>=1:raise ArithmeticError('residual too large to certify')
    masses=[q**x.bit_count()*(1-q)**(n-x.bit_count()) for x in range(N)]
    assert sum(masses)==1
    value=sum((p*x for p,x in zip(masses,v)),F(0))
    low=value/(1+delta);high=value/(1-delta)
    return low,high,delta,value

def certify_run(model,result):
    st=time.perf_counter();E=len(model['a'])
    flo=np.full(E,model['softness']);fhi=np.ones(E)
    picked=result['selected_edges']
    observed=result['observed_facilitations'] if 'observed_facilitations' in result else model['fac'][picked]
    flo[picked]=fhi[picked]=observed
    vl=spsolve(matrix(model,model['base']*fhi),model['m'])
    vu=spsolve(matrix(model,model['base']*flo),model['m'])
    low,_,dl,_=certify_field(model,fhi,vl)
    _,upper,du,_=certify_field(model,flo,vu)
    return {'certified_lower':outward(low,True),'certified_upper':outward(upper,False),
            'certified_upper_lower_ratio':outward(upper/low,False),
            'delta_lower_field_upper':outward(dl,False),'delta_upper_field_upper':outward(du,False),
            'seconds':time.perf_counter()-st,
            'proof':'Exact rational pointwise residual and inverse-positive killed-generator comparison.',
            'exact_lower_numerator':str(low.numerator),'exact_lower_denominator':str(low.denominator),
            'exact_upper_numerator':str(upper.numerator),'exact_upper_denominator':str(upper.denominator)}

if __name__=='__main__':
    data=json.load(open(str(ROOT / 'probe_results.json')))
    rel=json.load(open(str(ROOT / 'relative_results.json')))
    out=[]
    for k,d in enumerate(data):
        m=soft_east(d['L'],d['q'],d['softness'])
        tests=d['runs']+[rel[k]]
        v=spsolve(matrix(m,m['base']*m['fac']),m['m'])
        st=time.perf_counter();tl,tu,dt,_=certify_field(m,m['fac'],v)
        record={'L':d['L'],'q':d['q'],'softness':d['softness'],
                'reference_lower':outward(tl,True),'reference_upper':outward(tu,False),
                'reference_delta_upper':outward(dt,False),'reference_certification_seconds':time.perf_counter()-st,'runs':[]}
        for r in tests:
            c=certify_run(m,r);c['policy']=r['policy'];c['queries']=r['queries']
            assert F(int(c['exact_lower_numerator']),int(c['exact_lower_denominator']))<=tl
            assert tu<=F(int(c['exact_upper_numerator']),int(c['exact_upper_denominator']))
            record['runs'].append(c)
            print(d['L'],r['policy'],c['certified_lower'],c['certified_upper'],c['certified_upper_lower_ratio'],c['seconds'],flush=True)
        out.append(record)
    json.dump(out,open(str(ROOT / 'certified_results.json'),'w'),indent=2)
