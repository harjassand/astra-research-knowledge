#!/usr/bin/env python3
"""Exact rational compiler for finite-horizon passive DC-gain estimation.

Model: x'=-A x+b u, y=b^T x, mu I <= A <= Lambda I, A symmetric,
||b||=1, x(0)=0. Observation: dY=y dt+sigma dW. Apply a monotone
ramp during T/2, then hold U. Average y over m+1 equal bins in [T/2,T].
Certificates use exact rational arithmetic, without exponential evaluation.
The Gaussian observation model is a premise, not a laboratory measurement.
"""
from fractions import Fraction as Q
from math import log10
import argparse
import json
from pathlib import Path

def rational(x):
    return x if isinstance(x, Q) else Q(str(x))

def ceiling(x):
    x = rational(x)
    return -(-x.numerator // x.denominator)

def ceil_log2(x):
    x = rational(x)
    if x <= 1:
        return 0
    k = max(0, x.numerator.bit_length()-x.denominator.bit_length())
    while Q(1 << k) < x:
        k += 1
    return k

def cheb_value(m, x):
    if m == 0:
        return Q(1)
    p, q = Q(1), x
    for _ in range(1, m):
        p, q = q, 2*x*q-p
    return q

def cheb_affine(m, slope, offset):
    """Ascending coefficients of T_m(slope*z+offset)."""
    if m == 0:
        return [Q(1)]
    p, q = [Q(1)], [offset, slope]
    for _ in range(1, m):
        nxt = [Q(0)]*(len(q)+1)
        for j, c in enumerate(q):
            nxt[j] += 2*offset*c
            nxt[j+1] += 2*slope*c
        for j, c in enumerate(p):
            nxt[j] -= c
        p, q = q, nxt
    return q

def endpoints(mu, upper, horizon, degree):
    h = horizon/(2*(degree+1))
    a = max(Q(0), 1-upper*h)
    b = 1/(1+mu*h)
    assert 0 <= a < b < 1
    return h, a, b

def compile_experiment(mu='1', upper='16', horizon='1/10', epsilon='1/16',
                       alpha='1/20', amplitude='1', sigma='1', max_degree=4096):
    mu, upper, horizon, epsilon, alpha, amplitude, sigma = map(
        rational, (mu, upper, horizon, epsilon, alpha, amplitude, sigma))
    if not (0 < mu <= upper and horizon > 0 and 0 < epsilon < 1 and
            0 < alpha < 1 and amplitude > 0 and sigma > 0):
        raise ValueError('Invalid model/accuracy parameters.')
    budget = epsilon/4
    degree = 1
    while True:
        h, a, b = endpoints(mu, upper, horizon, degree)
        denom = cheb_value(degree, (2-a-b)/(b-a))
        if 1/denom <= budget:
            break
        degree *= 2
        if degree > max_degree:
            raise ValueError('Degree exceeds cap; increase --max-degree.')
    # Refine within the final doubling bracket; least degree is not claimed.
    for candidate in range(max(1, degree//2+1), degree):
        hc, ac, bc = endpoints(mu, upper, horizon, candidate)
        dc = cheb_value(candidate, (2-ac-bc)/(bc-ac))
        if 1/dc <= budget:
            degree, h, a, b, denom = candidate, hc, ac, bc, dc
            break
    weights = [v/denom for v in cheb_affine(degree, 2/(b-a), -(a+b)/(b-a))]
    assert sum(weights) == 1
    amplification = sum(map(abs, weights))
    assert amplification == cheb_value(degree, (2+a+b)/(b-a))/denom
    squared_norm = sum(w*w for w in weights)
    variance_one = (mu*sigma/amplitude)**2*squared_norm/h
    # Tail <= alpha/2: ln(4/alpha) <= ceil(log2(4/alpha)).
    qtail = ceil_log2(4/alpha)
    repetitions = max(1, ceiling(2*qtail*variance_one/budget**2))
    adc_error = amplitude*budget/(mu*amplification)
    forcing_effort_one = Q(2, 3)*amplitude**2*horizon
    dimensionless_effort = repetitions*forcing_effort_one/(sigma**2*mu**2)
    return {
        'mu': mu, 'Lambda': upper, 'T': horizon, 'epsilon': epsilon,
        'alpha': alpha, 'U': amplitude, 'sigma': sigma,
        'ramp_duration': horizon/2, 'ramp_slew': 2*amplitude/horizon,
        'degree': degree, 'bin_count': degree+1, 'bin_width': h,
        'spectral_z_lower': a, 'spectral_z_upper': b,
        'weights': weights, 'weights_sum': sum(weights),
        'bias_bound': 1/denom, 'l1_amplification': amplification,
        'weights_squared_norm': squared_norm,
        'single_trial_variance': variance_one,
        'statistical_error_budget': budget,
        'gaussian_tail_log_upper': qtail,
        'repetitions_sufficient': repetitions,
        'per_bin_absolute_ADC_error_budget': adc_error,
        'squared_drive_effort_per_trial_linear_ramp': forcing_effort_one,
        'dimensionless_total_effort_sufficient': dimensionless_effort,
        'status': 'Exact rational mathematical certificate; no physical trials performed.',
        'preparation': 'Known zero state per trial; actual preparation, copies and resets are additional resources.',
        'scope': 'Symmetric passive relaxation, supplied spectral interval and coupling normalization, additive Gaussian read noise.'
    }

def encode(obj):
    if isinstance(obj, Q):
        return f'{obj.numerator}/{obj.denominator}'
    if isinstance(obj, dict):
        return {k: encode(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [encode(v) for v in obj]
    return obj

def log10_fraction(x):
    x = rational(x)
    return log10(x.numerator)-log10(x.denominator) if x > 0 else float('-inf')

def summary(c):
    return {
        'mu': str(c['mu']), 'Lambda': str(c['Lambda']), 'T': str(c['T']),
        'epsilon': str(c['epsilon']), 'degree': c['degree'],
        'bin_count': c['bin_count'], 'bias_bound': float(c['bias_bound']),
        'log10_l1_amplification': log10_fraction(c['l1_amplification']),
        'log10_repetitions_sufficient': log10(c['repetitions_sufficient']),
        'log10_dimensionless_effort': log10_fraction(c['dimensionless_total_effort_sufficient']),
        'log10_ADC_error_budget': log10_fraction(c['per_bin_absolute_ADC_error_budget']),
        'exact_weights_sum_one': c['weights_sum'] == 1
    }

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for key, default in [('mu','1'),('upper','16'),('horizon','1/10'),
                         ('epsilon','1/16'),('alpha','1/20'),
                         ('amplitude','1'),('sigma','1')]:
        parser.add_argument('--'+key, default=default)
    parser.add_argument('--max-degree', type=int, default=4096)
    parser.add_argument('--output', default='response_certificate.json')
    args = vars(parser.parse_args())
    output = Path(args.pop('output'))
    c = compile_experiment(**args)
    output.write_text(json.dumps(encode(c), indent=2)+'\n')
    print(json.dumps(summary(c), indent=2))

if __name__ == '__main__':
    main()
