"""Exact EIS feasibility and interval arithmetic for a waveform-hard RC pair.

Run after explore_joint_pair.py, or use the retained candidates JSON.
Requires mpmath only. Does not import the grid optimizer or modify source files.
The theorem (including every waveform and adaptive experiment) is analytic;
these calculations verify its hypotheses for the supplied EIS input.
"""
from pathlib import Path
from fractions import Fraction as F
import csv, hashlib, json, math
from mpmath import iv

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parents[1] / 'sources' / 'astra_pulse_observable'
iv.dps = 55
A = F(125)
D = F(1, 40)
CINF = F(9999, 10000)
EPS_EIS = F(1, 10)

def I(x):
    if isinstance(x, F):
        return iv.mpf(x.numerator) / x.denominator
    return iv.mpf(x)

def enclosure(x):
    # mpmath interval endpoint -> float may truncate by more than one ulp.
    # Extract each exact binary endpoint and direct-round its Fraction instead.
    def fraction_of_binary(t):
        sign, mantissa, exponent, bit_count = t
        return F((-1 if sign else 1)*mantissa) * F(2)**exponent
    lower, upper = [fraction_of_binary(t) for t in x._mpi_]
    scale = 10**30
    lower_int = lower.numerator*scale // lower.denominator
    upper_int = -((-upper.numerator*scale) // upper.denominator)
    def decimal(integer):
        sign = '-' if integer < 0 else ''
        integer = abs(integer)
        return f'{sign}{integer//scale}.{integer%scale:030d}'
    result = [decimal(lower_int), decimal(upper_int)]
    assert F(result[0]) <= lower <= upper <= F(result[1])
    return result

def weight(x):
    return (1+x)/(1+x*x) - x/(1+10000*x*x)

def feature(s, f):
    q = 1-s
    r = 100*f
    d1 = q*q+s*s
    dr = q*q+10000*s*s
    b = q**3+s*s*(10000-s)
    factor = d1*dr/((q*q+r*r*s*s)*b)
    return factor*q, -factor*r*s

def target(s, time):
    alpha = 2*iv.pi*I(F(time)/100)
    if s == 0:
        return I(1)
    if s == 1:
        return alpha/I(CINF)
    q = 1-s
    factor = (q*q+s*s)*(q*q+10000*s*s)/(q*(q**3+s*s*(10000-s)))
    return (1-iv.exp(-alpha*I(q/s)))*I(factor)

delta = 2*iv.pi*I(D/100)

def difference(time):
    return I(A)*(1-iv.exp(-delta*I(F(time))))**2

def primitive(time):
    t = I(F(time))
    return I(A)*(t - 2*(1-iv.exp(-delta*t))/delta
                 + (1-iv.exp(-2*delta*t))/(2*delta))

def ramp_separation(horizon, ramp_time):
    h, rho = F(horizon), F(ramp_time)
    if rho == 0:
        return difference(h)
    return (primitive(h)-primitive(max(F(0), h-rho)))/I(rho)

def ramp_critical_bracket(eta, ramp_time):
    """Strict rational bracket for max separation = 2 eta."""
    threshold = I(2*eta)
    left, right = F(0), F(10000)
    assert ramp_separation(right, ramp_time).a > threshold
    while right-left > F(1, 10**8):
        mid = (left+right)/2
        z = ramp_separation(mid, ramp_time)
        if z.b < threshold:
            left = mid
        elif z.a > threshold:
            right = mid
        else:
            raise ArithmeticError('Interval precision did not decide a bracket step')
    assert ramp_separation(left, ramp_time).b < threshold
    assert ramp_separation(right, ramp_time).a > threshold
    return {'lower_exact': str(left), 'upper_exact': str(right),
            'seconds_outward': [enclosure(I(left))[0], enclosure(I(right))[1]]}

candidates = json.loads((HERE/'joint_pair_candidates.json').read_text())
rec = next(z for z in candidates if z['amp_mohm'] == 125. and z['d'] == '1/40')
nodes = [F(str(s)) for s in rec['nodes']]
coefs = [max(F(str(c)), F(0)) for c in rec['baseline_coefficients'][:-1]]
ell = F(str(rec['baseline_coefficients'][-1]))
assert ell > 0
baseline = [(s,c) for s,c in zip(nodes, coefs) if c]
plus_s, minus_s = 1/(1+D), 1/(1+2*D)
plus_hidden = (plus_s, 2*A*weight(1/D))
minus_hidden = (minus_s, A*weight(1/(2*D)))
models = {'minus': baseline+[minus_hidden], 'plus': baseline+[plus_hidden]}

with (SOURCE/'data/cell_001_eis.csv').open() as file:
    rows = list(csv.DictReader(file))
rows = [r for r in rows if F(r['frequency_hz']) <= 1000]
freqs = [F(r['frequency_hz']) for r in rows]
assert len(freqs) == 58
max_frequency = max(freqs)

out = {
    'status': 'PASS: conditional mathematical construction; no physical validation',
    'data_sha256': hashlib.sha256((SOURCE/'data/cell_001_eis.csv').read_bytes()).hexdigest(),
    'n_eis_frequencies': len(freqs),
    'eps_eis_mohm_exact': str(EPS_EIS),
    'eis_scope': '58 points, 0.01 through 904.7 Hz; exploratory model/error premises only',
    'target_time_seconds': 1000,
    'A_mohm_exact': str(A), 'd_exact': str(D),
    'delta_definition': 'delta=(2*pi*0.01 Hz)/40',
    'delta_per_second_interval': enclosure(delta),
    'common_inductance_coefficient_mohm_exact': str(ell),
    'common_inductance_H_interval': enclosure(I(ell)/(1000*2*iv.pi*I(max_frequency))),
    'common_baseline_components': [{'s_exact':str(s), 'mass_mohm_exact':str(c)}
                                  for s,c in baseline],
    'models': {},
    'voltage_interface': 'eta in mOhm = deterministic voltage error bound in mV / maximum current in A; not an instrument calibration',
    'interval_output': 'Authoritative 30-digit directed decimal strings, extracted from exact binary interval endpoint tuples. Never round these through float.',
    'initial_state_interface': 'Both experiments begin from zero incremental state; identical common baseline and L. Strong methods may be told the entire two-model segment.',
    'scope_limit': 'All causal scalar current waveforms within the given duration and peak/slew constraints. Further independent measurements or stronger noise assumptions change the interface.'
}
for name, components in models.items():
    errors = []
    for f, row in zip(freqs, rows):
        real, imag = F(0), ell*f/max_frequency
        for s,c in components:
            re, im = feature(s,f)
            real += c*re
            imag += c*im
        errors.extend([abs(real-1000*F(row['Z_real_ohm'])),
                       abs(imag-1000*F(row['Z_imag_ohm']))])
    error = max(errors)
    assert error < EPS_EIS
    mass = sum((c for s,c in components), F(0))
    q10 = sum((I(c)*target(s,10) for s,c in components), I(0))
    q1000 = sum((I(c)*target(s,1000) for s,c in components), I(0))
    if name == 'minus':
        assert q1000.b < 200
    else:
        assert q1000.a > 200
    out['models'][name] = {
        'max_component_error_mohm_exact': str(error),
        'max_component_error_mohm_outward': enclosure(I(error)),
        'positive_normalized_mass_mohm_exact': str(mass),
        'positive_normalized_mass_mohm_outward': enclosure(I(mass)),
        'Q10_mohm_interval': enclosure(q10),
        'Q1000_mohm_interval': enclosure(q1000),
        'hidden_component': {'s_exact': str(components[-1][0]),
                             'mass_mohm_exact': str(components[-1][1])},
        'all_components_positive': all(c > 0 for s,c in components)
    }

gap = difference(1000)
out['Q1000_separation_mohm_interval'] = enclosure(gap)
out['absolute_error_lower_bound_if_indistinguishable_mohm_interval'] = enclosure(gap/2)
out['experiments'] = []
for horizon in [1, 10, 20, 30, 100]:
    for rho in [0, 1]:
        sep = ramp_separation(horizon, rho)
        out['experiments'].append({
            'horizon_seconds':horizon, 'ramp_seconds':rho,
            'optimal_full_path_separation_per_max_current_mohm_interval':enclosure(sep),
            'minimum_eta_to_hide_pair_mohm_interval':enclosure(sep/2)})
out['critical_duration'] = []
for eta in [F(1,100), F(1,50), F(1,10), F(1)]:
    for rho in [0, 1]:
        out['critical_duration'].append({
            'eta_mohm_exact':str(eta), 'ramp_seconds':rho,
            'duration_for_possible_certain_pair_discrimination':ramp_critical_bracket(eta, rho)})

# Verify the exact rational transfer identity at nonzero rational Laplace s/a.
for z in [F(1, 100), F(1), F(7,3), F(100)]:
    direct = 2*A*D/(z+D)-A*(2*D)/(z+2*D)
    factored = 2*A*D*D/((z+D)*(z+2*D))
    assert direct == factored

(HERE/'verified_hard_pair.json').write_text(json.dumps(out, indent=2))
summary = {k:v for k,v in out.items() if k not in
           ['common_baseline_components','critical_duration','experiments']}
for m in summary['models'].values():
    # Long exact rationals are retained in the artifact, not printed.
    m.pop('max_component_error_mohm_exact')
    m.pop('positive_normalized_mass_mohm_exact')
print(json.dumps(summary, indent=2))
print('All exact feasibility checks, strict threshold tests, and critical-duration brackets passed.')
