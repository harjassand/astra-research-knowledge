#!/usr/bin/env python3
"""Check original-value cosine acquisition and residual preimage quadrature."""
import json
import math
from pathlib import Path
import numpy as np
from residual_action import correction


def run():
    kappa, eta, k, m = .5, .01, 2., 1.234
    a=math.sqrt(1-kappa*kappa)
    calls=0
    def g(x):
        nonlocal calls
        calls+=1
        return m+kappa*x+eta*np.sin(k*x)/k
    def cos_by_value(omega,x):
        v=omega*x/(a*k)
        return k*(g(v+math.pi/(2*k))-g(v-math.pi/(2*k))-kappa*math.pi/k)/(2*eta)
    def C(omega,x):
        return np.exp(kappa*kappa*omega*omega/(2*a*a))*cos_by_value(omega,x)
    rng=np.random.default_rng(87126)
    count=200000
    T=rng.uniform(size=count)
    points=np.array([-.7,.2,.9])
    residual_mean_errors=[]
    residual_query_counts=[]
    xx,ww=np.polynomial.legendre.leggauss(150)
    ts,ws=(xx+1)/2,ww/2
    for x in points:
        old=calls
        w=np.exp(-k*k*(1-T*T)/2)
        estimate=kappa*eta*C(k,x)+w*(kappa*eta*C(k*T,x)+eta*eta*(C(k*(1+T),x)+C(k*(1-T),x))/2)
        residual_query_counts.append(calls-old)
        def exactC(omega):
            return np.exp(kappa*kappa*omega*omega/(2*a*a))*np.cos(omega*x/a)
        target=kappa*eta*exactC(k)+np.sum(ws*np.exp(-k*k*(1-ts*ts)/2)*(kappa*eta*exactC(k*ts)+eta*eta*(exactC(k*(1+ts))+exactC(k*(1-ts)))/2))
        residual_mean_errors.append(float(abs(np.mean(estimate)-target)))
    # Full positive update executes one source query and eight residual queries.
    G,Z=rng.normal(size=(count,1)),rng.normal(size=(count,1))
    old=calls
    base=g(G)+a*Z
    def action(yg,yz,v):
        t=rng.uniform(size=yg.shape)
        w=np.exp(-k*k*(1-t*t)/2)
        rh=kappa*eta*C(k,yg)+w*(kappa*eta*C(k*t,yg)+eta*eta*(C(k*(1+t),yg)+C(k*(1-t),yg))/2)
        return rh*v
    U,_=correction(G,Z,kappa,action,rng)
    tau=.5
    output=base+U+tau*rng.normal(size=G.shape)
    fullcalls=calls-old
    b=2*kappa*eta*math.exp(kappa*kappa*k*k/(2*a*a))+eta*eta*math.exp(kappa*kappa*(2*k)**2/(2*a*a))
    out={
        'sample_count':count,'family_Lip_bound':kappa+eta,
        'residual_action_queries_per_execution':residual_query_counts,
        'full_update_g_queries_per_execution':fullcalls,
        'residual_action_mean_abs_errors':residual_mean_errors,
        'residual_action_proved_bound_b':b,
        'output_mean_empirical':float(np.mean(output)),
        'target_mean':m,'output_variance_empirical':float(np.var(output)),
        'target_variance':1+tau*tau,
        'ordinary_comparator_exact_query_count':1,
        'Monte_Carlo_does_not_certify_TV':True,
    }
    C0=4+2*math.sqrt(2)/3
    dG=C0/(a*kappa); dZ=1/a+C0/a**2; j0=1/(2*a)
    j=j0+(1+math.sqrt(2))*(1+kappa*dG+a*dZ+a*j0)/a
    A=dG+dZ+j; B=j*dZ
    H=math.log(1+tau**-2)/math.sqrt(2)
    c=math.pi/(2*math.sqrt(2)*a)
    phi=math.exp(-.5)/math.sqrt(2*math.pi)
    bounds=[]
    for ee in [.01,.001,.0001]:
        bb=2*kappa*ee*math.exp(kappa*kappa*k*k/(2*a*a))+ee*ee*math.exp(kappa*kappa*(2*k)**2/(2*a*a))
        bound=H*(A*ee*bb+B*bb*bb)+phi*c*c*bb*bb/tau**2
        bounds.append({'eta':ee,'proved_TV_upper_bound':bound,'target_variance':1+tau*tau})
    out['full_law_bound_values']=bounds
    assert all(n==8 for n in residual_query_counts)
    assert fullcalls==9
    assert max(residual_mean_errors)<.0001
    return out


if __name__=='__main__':
    result=run()
    (Path(__file__).resolve().parent/'value_only_family_checks.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
