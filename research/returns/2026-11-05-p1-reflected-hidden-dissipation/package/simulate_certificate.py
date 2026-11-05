"""One-apparatus synthetic experiment; no hidden-state resets.
Run from this directory: python3 simulate_certificate.py
Requires numpy, scipy, and dynamics_reflection_check.py.
"""
import itertools
import json
import math
from pathlib import Path
import numpy as np
from scipy.linalg import expm
from dynamics_reflection_check import generator, entropy_rate, check_instance, F


def advance(state, u, cdf):
    row = cdf[state]
    if u < row[0]: return 0
    if u < row[1]: return 1
    if u < row[2]: return 2
    return 3


def run(n=750000, training=20000, seed=20261105):
    a, eps, t, delta = 1., .4, 1., .05
    q = generator(a, eps)
    # Q contains an independent uniform refresh generator of rate a-2eps.
    # This proves alpha(s) <= exp(-(a-2eps)s), including arbitrary initial states.
    refresh = a-2*eps
    gap = math.log(8*(n+training)/delta)/refresh
    cg = np.cumsum(expm(q*gap), axis=1)
    ct = np.cumsum(expm(q*t), axis=1)
    rng = np.random.default_rng(seed)
    state, corr = 0, 0.
    for us in rng.random((training, 2)):
        state = advance(state, us[0], cg); first = F[state]
        state = advance(state, us[1], ct); corr += first*F[state]
    center = float(np.clip(corr/training, 0, 1))
    total, nminus = 0., 0
    for offset in range(0, n, 10000):
        for us in rng.random((min(n-offset, 10000), 3)):
            state = advance(state, us[0], cg); left = F[state]
            state = advance(state, us[1], ct); mid = F[state]
            state = advance(state, us[2], ct); right = F[state]
            total += float(mid == -1)*(left+center)*(right+center)
            nminus += int(mid == -1)
    values = [float(y == -1)*(x+center)*(z+center)
              for x,y,z in itertools.product([-1,1], repeat=3)]
    width = max(values)-min(values)
    mean = total/n
    radius = width*math.sqrt(math.log(4/delta)/(2*n))
    neg = max(0., -mean-radius)
    p_upper = min(1., nminus/n+math.sqrt(math.log(4/delta)/(2*n)))
    eta = neg/p_upper
    nonlinear = (2*p_upper/t)*math.sqrt(eta)*math.atanh(math.sqrt(eta)) if eta else 0.
    r = math.exp(-a*t)
    result = dict(
        synthetic_only=True, no_hidden_state_resets=True, initial_hidden_state=0,
        a=a, epsilon=eps, lag=t, seed=seed, training_blocks=training,
        validation_blocks=n, learned_center=center, exact_pair_correlation=r,
        empirical_score=mean, exact_score=.5*((center-r)**2-(eps*t*r)**2),
        confidence_radius=radius, certified_negative_score=neg,
        linear_EPR_lower_bound=2*neg/t, nonlinear_EPR_lower_bound=nonlinear,
        true_EPR=entropy_rate(q), confidence_at_least=1-delta,
        gap_per_block=gap, mixing_envelope_rate=refresh,
        coupling_failure_bound=(n+training)*math.exp(-refresh*gap),
        observation_count=2*training+3*n,
        physical_duration_model_units=training*(gap+t)+n*(gap+2*t),
        sample_accumulators_constant_memory=True)
    assert neg > 0
    # Independently verify known readout-noise correction, using exact table.
    noise, rho = .1, .8
    expected = 0.; scores = []
    for zz in itertools.product([-1,1], repeat=3):
        probability = 0.
        for yy in itertools.product([-1,1], repeat=3):
            x,y,z = yy
            pp = (1+r*(x*y+y*z)+r*r*x*z+(eps*t*r)**2*x*y*z)/8
            probability += pp*np.prod([1-noise if b==c else noise for b,c in zip(yy,zz)])
        score = (1-zz[1]/rho)/2*(zz[0]/rho+center)*(zz[2]/rho+center)
        expected += probability*score; scores.append(score)
    assert abs(expected-result['exact_score']) < 1e-12
    result['noise_correction_check'] = dict(flip_probability=noise,
        unbiasedness_error=abs(expected-result['exact_score']),
        score_range=max(scores)-min(scores))
    return result


def run_stationary_null_test(n=750000, seed=20261106):
    """One stationary record, consecutive blocks, no thinning or mixing input."""
    a, eps, t, center = 1., .4, 1., .37
    q = generator(a, eps)
    cdf = np.cumsum(expm(q*t), axis=1)
    rng = np.random.default_rng(seed)
    # Exactly uniform stationary preparation for this synthetic four-state model.
    state = int(rng.integers(0,4)); left = F[state]
    total = 0.
    for start in range(0,n,10000):
        for us in rng.random((min(10000,n-start),2)):
            state=advance(state,us[0],cdf); mid=F[state]
            state=advance(state,us[1],cdf); right=F[state]
            total += float(mid==-1)*(left+center)*(right+center)
            left=right
    mean=total/n; negative=max(0.,-mean); B=(1+abs(center))**2
    z=negative/B
    I=.5*(1+z)*math.log1p(z)+.5*(1-z)*math.log1p(-z)
    logq=-n*I; qbound=math.exp(logq); delta=.05
    kl=(delta*math.log(delta/qbound)+(1-delta)*math.log((1-delta)/(1-qbound))) if qbound<delta else 0.
    return dict(synthetic_only=True, stationary_uniform_preparation=True,
        no_thinning=True, no_mixing_bound_used_by_test=True, seed=seed,
        fixed_witness_center=center, blocks=n, empirical_score=mean,
        null_p_value_upper_bound=qbound, log_null_p_bound=logq,
        conservative_stationary_rate_lower_bound=4*kl/(n*2*t),
        rate_confidence=1-delta, observation_count=2*n+1,
        physical_duration_model_units=2*n*t)


if __name__ == '__main__':
    result = {'exact_family_check': check_instance(), 'simulation': run(),
              'stationary_null_test':run_stationary_null_test()}
    Path('simulation_results.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({'simulation':result['simulation'], 'stationary_null_test':result['stationary_null_test']}, indent=2))
