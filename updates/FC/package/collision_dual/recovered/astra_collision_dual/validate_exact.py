from __future__ import annotations
import json,time
from pathlib import Path
from math import exp,sqrt,pi
import numpy as np
from collision_dual import DiscreteVariance
from exact_extension import linear_bernoulli_factory,exact_velocity_ideal_prototype,parameters

rng=np.random.default_rng(2026101302)
result={'seed':2026101302,'status':'Floating-point tests of ideal-exact construction; no exact-real certification.'}
rows=[]
for p,margin in [(.1,.7),(.3,.35),(.45,.08),(.49,.015)]:
    count=[0]
    def coin():
        count[0]+=1
        return bool(rng.random()<p)
    n=12000
    samples=np.array([linear_bernoulli_factory(coin,2.,margin,rng) for _ in range(n)])
    rows.append({'p':p,'margin':margin,'samples':n,'empirical_probability':float(samples.mean()),
                 'target':2*p,'standard_error':sqrt(2*p*(1-2*p)/n),'mean_input_flips':count[0]/n,
                 'proven_input_flip_bound':19/margin})
result['factory_checks']=rows
A,B,RHO=1.,1.1,.2
initial=DiscreteVariance((A,B),(.5,.5))
r,g,c,integral=parameters(A,B,RHO)
result['parameters']={'a':A,'b':B,'rho':RHO,'r':r,'proposal_variance':g,'envelope_C':c,
    'integrated_inverse_lower_bound':integral,'input_coin_expectation_bound':19*c*c*integral,
    'degree_expectation_per_input_coin':r/(RHO-r)}
rows=[]
for t in [0.,3.,100.,1e6]:
    n=4500; samples=[];proposals=[];coins=[];degrees=[];splits=[]
    start=time.perf_counter()
    for _ in range(n):
        v,w=exact_velocity_ideal_prototype(t,A,B,RHO,initial,rng)
        samples.append(v);proposals.append(w.proposals);coins.append(w.input_coins)
        degrees.append(w.total_degree);splits.append(w.effective_splits)
    samples=np.array(samples);sq=np.sum(samples*samples,axis=1)
    covariance=(A+B)/2
    fourth=15*(covariance**2+((B-A)/2)**2*exp(-t/3))
    rows.append({'time':t,'samples':n,'mean_squared_speed':float(sq.mean()),
        'target_mean_squared_speed':3*covariance,'mean_fourth_speed':float((sq*sq).mean()),
        'target_mean_fourth_speed':fourth,'fourth_speed_standard_error':float((sq*sq).std(ddof=1)/sqrt(n)),
        'mean_proposals':float(np.mean(proposals)),'expected_proposals':c,
        'mean_input_coins':float(np.mean(coins)),'mean_total_degree':float(np.mean(degrees)),
        'mean_effective_splits':float(np.mean(splits)),'runtime_seconds':time.perf_counter()-start})
result['sampler_checks']=rows
Path('exact_results.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
