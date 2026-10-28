"""Standard DKW survival baseline; native costs, no hidden-rank promise."""
from fractions import Fraction as F
from pathlib import Path
from math import factorial
import json,sys
import numpy as np
ROOT=Path(__file__).resolve().parents[1]

def acquire(n=4000,cap=1000000):
    rng=np.random.default_rng(2026102903)
    threshold=np.where(rng.integers(0,2,size=n)==0,1,1024)
    active=np.arange(n)
    lifetimes=np.full(n,cap+1,dtype=np.int64)
    steps=last=0
    for t in range(1,cap+1):
        if not len(active):break
        steps+=len(active)
        death=rng.integers(0,32768,size=len(active))<threshold[active]
        lifetimes[active[death]]=t
        active=active[~death]
        last=t
        if t%100000==0:print('clock',t,'remaining',len(active),flush=True)
    assert steps==sum(min(int(t),cap) for t in lifetimes)
    return dict(trials=n,censor_cap=cap,lifetimes_or_cap_plus_one=lifetimes.tolist(),
                censored_count=len(active),last_observation_clock=last,
                primitive_applications=steps,coarse_observations=steps,physical_preparations=n)

def infer(r):
    eps=F(1,32);x=2*r['trials']*eps**2
    assert 2/sum((x**k/F(factorial(k)) for k in range(60)),F(0))<F(1,1000)
    bound=eps+F(r['censored_count'],r['trials'])
    return dict(all_time_absolute_error_bound=str(bound),failure_probability_upper='1/1000',
                dkw_radius=str(eps),exact_dkw_exponent=str(x),hidden_dimension_upper_bound=None,
                estimator='Through the censor cap use the fraction of recorded lifetimes greater than h; afterwards predict zero. Censored mass is added to the uniform error.',
                future_scope='All repetition lengths of this one operation and total-survival readout; no unexecuted switching-program guarantee.',
                prior_art='Standard Dvoretzky-Kiefer-Wolfowitz-Massart empirical-distribution band.',
                source='https://doi.org/10.1214/aop/1176990746')

def run(replay=False):
    p=ROOT/'results'/'SURVIVAL_DISTRIBUTION_RAW_RECEIPT.json'
    r=json.loads(p.read_text()) if replay else acquire()
    if not replay:p.write_text(json.dumps(r,indent=2)+'\n')
    c=infer(r)
    times=np.array(sorted(r['lifetimes_or_cap_plus_one']))
    points=sorted({0,r['censor_cap']}|{int(t) for t in times if t<=r['censor_cap']}|{int(t)-1 for t in times if t<=r['censor_cap']})
    # Floating private diagnostic is not used to establish the certificate.
    h=np.array(points,dtype=float)
    truth=((1-1/32768)**h+(1-1/32)**h)/2
    empirical=(r['trials']-np.searchsorted(times,h,side='right'))/r['trials']
    diagnostic=float(np.max(np.abs(truth-empirical)))
    out=dict(receipt=r,certificate=c,private_max_error_float_diagnostic=diagnostic,
             exact_cost_sum_check=True,
             scope='Integer-RNG software trajectories. Every primitive and report until absorption or the fixed cap is charged; fresh preparations are paid.')
    (ROOT/'results'/'SURVIVAL_DISTRIBUTION_BASELINE.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(dict(certificate=c,diagnostic=diagnostic,
                         costs={k:v for k,v in r.items() if k!='lifetimes_or_cap_plus_one'}),indent=2))

if __name__=='__main__':run('--replay' in sys.argv)
