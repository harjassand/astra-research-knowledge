"""Integrate the angular kernel BEFORE taking its absolute value.

Actual invariant radial class, beta3/4. No global/continuum certificate.
"""
import json,math,time
from pathlib import Path
import numpy as np
from scipy.special import roots_genlaguerre,erf
from scipy.integrate import quad
from scipy.optimize import linprog
from scipy.sparse import csr_matrix,hstack,vstack,eye


def radial_kernel(v,speed):
    if v==0:
        return 4/speed-speed
    minimum=np.minimum(v,speed)
    gain=2*math.sqrt(2*math.pi)/(v*speed)*np.exp(minimum**2/2)*erf(minimum/math.sqrt(2))
    loss=((v+speed)**3-np.abs(v-speed)**3)/(6*v*speed)
    return gain-loss


def main():
    started=time.perf_counter();beta=.75
    xx,ww=roots_genlaguerre(192,.5);speed=np.sqrt(2*xx/beta)
    design=np.column_stack([np.ones(len(speed)),speed**2]);identity=eye(len(speed),format='csr')
    records=[]
    for v in (0.0,2.0,4.0,8.0):
        kernel=radial_kernel(v,speed)
        weights=ww/math.gamma(1.5)*beta**(-1.5)*math.exp(-(1-beta)*v*v/2)
        nu=2*math.sqrt(2/math.pi) if v==0 else math.sqrt(2/math.pi)*math.exp(-v*v/2)+(v+1/v)*math.erf(v/math.sqrt(2))
        matrix=csr_matrix(design*weights[:,None]);rhs=weights*kernel
        constraints=vstack([hstack([-matrix,-identity]),hstack([matrix,-identity])],format='csr')
        fit=linprog(np.r_[np.zeros(2),np.ones(len(speed))],A_ub=constraints,
                    b_ub=np.r_[-rhs,rhs],bounds=[(None,None)]*2+[(0,None)]*len(speed),method='highs')
        cost=float(weights@np.abs(kernel-design@fit.x[:2]))
        records.append({'v':v,'controls':fit.x[:2].tolist(),'weighted_absolute_row_over_nu':cost/nu,
                        'without_controls':float(weights@np.abs(kernel))/nu,'lp_success':fit.success})
    # A single nondegenerate angular identity control, unrelated to fitting.
    v,speed0=4.,2.
    def integrand(mu):
        r=math.sqrt(v*v+speed0*speed0-2*v*speed0*mu)
        perp=v*v*speed0*speed0*(1-mu*mu)/(r*r)
        return .5*(4*math.exp(perp/2)/r-r)
    integral,error=quad(integrand,-1,1,epsabs=1e-12,epsrel=1e-12)
    closed=float(radial_kernel(v,np.array([speed0]))[0])
    assert abs(integral-closed)<1e-11
    result={'status':'FLOAT_PREVIEW_not_continuum_certificate','beta':'3/4','radial_order':192,
            'angular_integral_control':{'quadrature':integral,'closed':closed,'reported_error':error},
            'records':records,'seconds_total':time.perf_counter()-started,
            'uniform_or_nonlinear_or_normalized_sampler_claim':False}
    (Path(__file__).parent/'RADIAL_WEIGHT_PREVIEW.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
