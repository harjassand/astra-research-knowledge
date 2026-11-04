"""Executed rare-event estimator on 40 independent parallel edges.

All local failure/repair rates equal 1. Failure-conditioned stationary start is
exactly the all-down state. Count reduction simulates the same uniformized
kernel, without enumerating configurations. Confidence arithmetic is rational;
the stochastic guarantee assumes independent uniform random choices. NumPy's
seeded PRNG is used for reproducible implementation diagnostics.
"""
from fractions import Fraction as F
from pathlib import Path
import json, math, time
import numpy as np

def run():
    started=time.perf_counter(); m=40; n=100000; k=600
    rng=np.random.default_rng(53320261105)
    active=np.full(n,m,dtype=np.int64); updates=0
    for _ in range(k+1):
        updates+=len(active)
        u=rng.integers(0,2*m,size=len(active))
        new=active-(u<active)+((u>=active)&(u<m))
        active=new[new<m]
    successes=len(active)
    # h=.0055: 2 exp(-2 n h^2) = 2 exp(-6.05) < .01.
    h=F(11,2000); zhat=F(successes,n); zL=zhat-h; zU=zhat+h
    p=F(1,2**m); g=F(1,m); Lambda=2*m
    H=sum((F(1,j) for j in range(1,m+1)),F(0))
    a=p/(1-p)
    assert k>=1/g and a*k<1 and a/g<1 and zL>0
    main_lower=(1-a/g)*(1-k*a)
    high_upper=(1-g)**k
    lambdaL=p*zL/(1+high_upper)
    lambdaU=min(a,p*zU/main_lower)
    ML=(1/lambdaU-1/g)/Lambda
    MU=(1/lambdaL+H/g)/Lambda
    exact=sum((F(sum(math.comb(m,j) for j in range(i+1)),
                     (m-i)*math.comb(m,i)) for i in range(m)),F(0))
    result={
      'model':'40 independent parallel edges, all a_i=b_i=1',
      'configurations':2**m,'conditional_sampler':'exact singleton all-down',
      'trials':n,'steps_per_successful_trial':k+1,'actual_kernel_updates':updates,
      'successes':successes,'seed':53320261105,'stationary_failure_probability':float(p),
      'estimated_conditional_success':float(zhat),
      'conditional_success_interval':[float(zL),float(zU)],
      'confidence_at_least':.99,
      'confidence_statement':'Hoeffding under independent uniform random choices; seeded PRNG diagnostic',
      'mean_interval':[float(ML),float(MU)],'interval_ratio':float(MU/ML),
      'exact_birth_death_mean':float(exact),'exact_mean_inside_interval':ML<=exact<=MU,
      'inverse_stationary_frequency':float(F(2**m,m)),
      'point_estimate':float(1/(Lambda*p*zhat)),
      'expected_direct_uniformized_steps':float(Lambda*exact),
      'rational_lower':str(ML),'rational_upper':str(MU),
      'wall_seconds':time.perf_counter()-started,
      'scope':'special static sampler and symmetry reduction; not a general Karger implementation'
    }
    Path(__file__).with_name('parallel_experiment.json').write_text(json.dumps(result,indent=2)+'\n')
    for key in ['rational_lower','rational_upper']: result.pop(key)
    print(json.dumps(result,indent=2))

if __name__=='__main__':run()
