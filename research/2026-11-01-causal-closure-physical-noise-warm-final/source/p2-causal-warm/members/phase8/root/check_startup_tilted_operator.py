"""Independent number-sector beamsplitter check of the startup tilted effect.

Each fixed-total-number block is exact, not a truncated oscillator boundary.
Only the initial thermal sum is truncated, with an analytic remainder bound.
This checks the key normal-order formula by an independent state propagation.
"""
from pathlib import Path
import json, math
import numpy as np
from scipy.linalg import expm
from scipy.special import gammainc

HERE=Path(__file__).resolve().parent

def check(r,eta,nb=.1,theta=.8,bath_terms=40):
    t=math.expm1(theta);w=(1-r)*t-eta*r
    coeff=1/(1-nb*w)
    base=1+(r*t-eta*(1-r)+nb*t*eta)/(1-nb*w)
    ns=[0,1,4,12]
    unitaries={}
    for N in range(max(ns)+bath_terms+1):
        G=np.zeros((N+1,N+1))
        for k in range(N):
            G[k+1,k]=math.sqrt((k+1)*(N-k));G[k,k+1]=-G[k+1,k]
        unitaries[N]=expm(math.acos(math.sqrt(r))*G)
    q=nb/(1+nb);rows=[]
    for n in ns:
        actual=0.
        for m in range(bath_terms+1):
            N=n+m;k=np.arange(N+1)
            weights=np.exp(theta*k)*(1-eta)**(N-k)
            actual+=(1-q)*q**m*np.dot(unitaries[N][:,n]**2,weights)
        analytic=coeff*base**n
        remainder=math.exp(theta*n)*(1-q)*(q*math.exp(theta))**(bath_terms+1)/(1-q*math.exp(theta))
        err=abs(actual-analytic)
        assert err<2e-10*max(1,analytic)+remainder,(n,actual,analytic)
        rows.append(dict(initial_number=n,direct_block_sum=float(actual),analytic=float(analytic),
            absolute_error=float(err),thermal_tail_upper=float(remainder)))
    return dict(r=r,eta=eta,nb=nb,theta=theta,old_number_base=base,
       state_uniform_tilted_contraction=base<=1,checks=rows)

if __name__=='__main__':
    out={'good_admission':check(.060976178955714784,.12312259871939688),
         'insufficient_output_observation_counterexample':check(.45,.2)}
    n=np.arange(70);R=1.;c=1.
    effect=gammainc(n+1,R*R)
    majorant=np.exp(c*R*R)/(1+c)**(n+1.)
    ratio=effect/majorant
    assert np.max(ratio)<=1+1e-13
    out['disk_effect_check']={'R':R,'c':c,'number_sectors':70,
        'largest_effect_to_majorant_ratio':float(np.max(ratio))}
    (HERE/'startup_tilted_operator_checks.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
