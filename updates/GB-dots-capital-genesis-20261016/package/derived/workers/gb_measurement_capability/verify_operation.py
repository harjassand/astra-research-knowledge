#!/usr/bin/env python3
"""Arithmetic tests of the proposed prospective operation; never empirical data.

Only reads the frozen packets. Does not invoke any STM code or read its labels.
The exact physical POVM used below is an existence witness, not an apparatus fit.
"""
from fractions import Fraction as Q
from pathlib import Path
import hashlib
import json
import math
import sys

import sympy as S

HERE = Path(__file__).resolve().parent
PACKET = Path('/Users/harjas/Downloads/Dots/Astra_measured_POVM_research_packet_2026-10-15')
DESIGN = json.loads((PACKET / 'certificates/frozen_design.json').read_text())
SCORES = [Q(n, DESIGN['score_denominator']) for n in DESIGN['score_numerators']] + [Q(0)]
GAINS = {l: [2*l*s-s*s for s in SCORES] for l in [-1, 1]}
RANGES = {l: max(v)-min(v) for l, v in GAINS.items()}
CHECKS = []


def check(name, condition):
    if not condition:
        raise AssertionError(name)
    CHECKS.append(name)


def analyze_counts(counts, attempts, q, eta=None, alpha=0.05):
    """Fixed-design, fixed-horizon, stratified Hoeffding arithmetic.

    Assumes complete prospective attempt counts, fixed stratum sizes, and a
    common stationary receiver across both hidden-label strata. Arbitrary
    label-correlated drift needs the pooled randomized-label alternative.
    eta is separately justified trace-distance uncertainty
    for each label. Numerical output is conditional on those external premises.
    This function cannot validate physical state calibration or provenance.
    """
    if set(counts) != {-1, 1} or set(attempts) != {-1, 1}:
        raise ValueError('Both label strata are required')
    if not 0 < alpha < 1 or not 0 <= q <= 1:
        raise ValueError('Invalid alpha or erasure probability')
    for l in [-1, 1]:
        if len(counts[l]) != 5:
            raise ValueError('Four frozen outcomes plus failure are required')
        if any(type(n) is not int or n < 0 for n in counts[l]):
            raise ValueError('Counts must be nonnegative integers')
        if type(attempts[l]) is not int or attempts[l] <= 0:
            raise ValueError('Positive attempt denominators are required')
        if sum(counts[l]) != attempts[l]:
            raise ValueError('Outcome counts must cover all declared attempts')
    mean = sum((sum(n*z for n, z in zip(counts[l], GAINS[l])) / attempts[l]
                for l in [-1, 1]), Q(0)) / 2
    v = sum((RANGES[l]**2 / attempts[l] for l in [-1, 1]), Q(0)) / 4
    halfwidth = math.sqrt(float(v) * math.log(1/alpha) / 2)
    lower = float(mean)-halfwidth
    out = {'mean_gain': float(mean), 'statistical_lower_gain': lower,
           'halfwidth': halfwidth, 'source_gain': float(q*Q(36, 121)),
           'external_contract_validated_by_this_function': False}
    if eta is None:
        out['decision'] = 'PREPARATION_UNCALIBRATED'
        return out
    if set(eta) != {-1, 1} or any(not 0 <= x <= 1 for x in eta.values()):
        raise ValueError('Trace distances must lie in [0,1] for both labels')
    allowance = sum((RANGES[l]*eta[l] for l in [-1, 1]), Q(0))/2
    ideal_lower = lower-float(allowance)
    out.update({'preparation_allowance': float(allowance),
                'ideal_lower_gain': ideal_lower,
                'conditional_decision': 'REJECT_SOURCE_MMSE_DOMINANCE'
                if ideal_lower > out['source_gain'] else 'INCONCLUSIVE',
                'decision': 'CONDITIONAL_ARITHMETIC_ONLY'})
    return out


def rounded_counts(probabilities, n):
    """Deterministic count fixture; not random or held-out observations."""
    reals = [float(S.N(p, 35))*n for p in probabilities]
    values = [math.floor(p) for p in reals]
    residual = n-sum(values)
    check('fixture residual is small', 0 <= residual <= len(values))
    order = sorted(range(len(values)), key=lambda k: reals[k]-values[k], reverse=True)
    for k in order[:residual]:
        values[k] += 1
    return values


def physical_fixture():
    I = S.eye(2)
    X = S.Matrix([[0, 1], [1, 0]])
    Y = S.Matrix([[0, -S.I], [S.I, 0]])
    Z = S.diag(1, -1)
    rot = []
    for ns in DESIGN['stereographic_numerators']:
        t = [S.Rational(n, DESIGN['stereographic_denominator']) for n in ns]
        t2 = sum(x*x for x in t)
        u = ((1-t2)*I-2*S.I*(t[0]*X+t[1]*Y+t[2]*Z))/(1+t2)
        check('exact local unitarity', S.simplify(u.conjugate().T*u) == I)
        rot.append(u)
    U = S.kronecker_product(*rot)
    b, r, z = 9*S.sqrt(2)/20, S.Rational(6, 11), S.Rational(9, 11)
    states = {}
    for l in [-1, 1]:
        rho = S.zeros(4)
        for i in [-1, 1]:
            sigma = (I+b*Z+i*b*X)/2
            ref = (I+l*i*r*X+z*Z)/2
            rho += S.kronecker_product(sigma, ref)/2
        states[l] = (U*rho*U.conjugate().T).applyfunc(S.expand)
        check('normalized prepared state', S.simplify(S.trace(states[l])) == 1)
    data = json.loads((PACKET / 'certificates/physical_half_box_candidate.json').read_text())
    F = [(S.Matrix(e['real_numerators'])+S.I*S.Matrix(e['imag_numerators']))/
         data['denominator'] for e in data['effects']]
    check('existence POVM completeness', sum(F, S.zeros(4)) == S.eye(4))
    for f in F:
        check('existence POVM Hermitian', f == f.conjugate().T)
        check('existence POVM positive definite', all(f[:k, :k].det() > 0 for k in range(1, 5)))
    probs = {l: [S.simplify(S.trace(f*states[l])) for f in F] + [S.Integer(0)]
             for l in [-1, 1]}
    for l in probs:
        check('exact probability normalization', S.simplify(sum(probs[l])) == 1)
        check('positive success probabilities', all(p > 0 for p in probs[l][:-1]))
    gain = S.simplify(sum(sum(S.Rational(z.numerator, z.denominator)*p
                              for z, p in zip(GAINS[l], probs[l]))
                          for l in [-1, 1])/2)
    return probs, gain


def main():
    check('negative-label range', RANGES[-1] == Q(526071, 200000))
    check('positive-label range', RANGES[1] == Q(565929, 200000))
    check('uniform preparation sensitivity', sum(RANGES.values())/2 == Q(273, 100))
    check('pooled gain range', max(sum(GAINS.values(), []))-min(sum(GAINS.values(), [])) == Q(719, 250))
    check('optimal Hoeffding positive-label allocation', RANGES[1]/sum(RANGES.values()) == Q(565929, 1092000))

    # Exact sharp rare-success construction, including biased failure score.
    for s in [Q(0), Q(1, 1000), Q(1, 10), Q(1, 4), Q(1, 2)]:
        fail_mean = -s/(1-s)
        gain = s + (1-s)*fail_mean**2
        check('sharp biased-herald identity', gain == s/(1-s))
        check('valid biased-herald failure score', -1 <= fail_mean <= 0)
        check('balanced label plus conditional probabilities', 0 <= 2*s <= 1)
    # An informative failure output can defeat an unqualified efficiency no-go.
    check('failure-extra-output counterexample', Q(1, 1000)+(1-Q(1, 1000)) == 1)

    certs = json.loads((PACKET / 'certificates/tight_box_certificate.json').read_text())
    planning = []
    for q, cert_index in [(Q(9, 20), 0), (Q(43, 100), 1)]:
        g = q*Q(36, 121)
        upper = S.sympify(certs[cert_index]['risk_upper_exact'], locals={'sqrt': S.sqrt})
        delta = S.simplify(1-S.Rational(g.numerator, g.denominator)-upper)
        check('selected deterministic gap positive', delta > 0)
        d = float(S.N(delta, 30))
        R = float(sum(RANGES.values())/2)
        crossing = math.ceil(R*R*math.log(20)/(2*d*d))
        power80 = math.ceil(R*R*(math.sqrt(math.log(20))+math.sqrt(math.log(5)))**2/(2*d*d))
        pooled_R = float(max(sum(GAINS.values(), []))-min(sum(GAINS.values(), [])))
        pooled_power80 = math.ceil(pooled_R*pooled_R*(math.sqrt(math.log(20))+math.sqrt(math.log(5)))**2/(2*d*d))
        threshold = float(S.N(S.Rational(g.numerator, g.denominator)/(1-upper), 30))
        check('fair-success threshold below one', 0 < threshold < 1)
        planning.append({'q': str(q), 'source_gain': str(g), 'gap': d,
                         'component_tolerance': certs[cert_index]['component_tolerance'],
                         'arbitrary_herald_necessary_success': str(g/(1+g)),
                         'fair_success_sufficient_threshold': threshold,
                         'equal_eta_max_before_statistical_margin': d/R,
                         'asymptotic_optimal_label_allocation': float(RANGES[1]/sum(RANGES.values())),
                         'center_crossing_trial_count': crossing,
                         'fixed_horizon_80pct_power_sufficient_trial_count': power80,
                         'randomized_label_pooled_80pct_power_sufficient_trial_count': pooled_power80,
                         'trial_count_note': 'Stratified numbers assume a common stationary receiver and continuous optimal allocation; round label counts and use exact variance proxy before preregistration. Pooled number supports average predictable gain with fresh hidden balanced labels and arbitrary predictable receiver drift. No failure/preparation allowance or calibration confidence included.'})
    probs, fixture_gain = physical_fixture()
    n = 20_000_000
    counts = {l: rounded_counts(probs[l], n) for l in [-1, 1]}
    zero = {-1: Q(0), 1: Q(0)}
    fixture = analyze_counts(counts, {-1: n, 1: n}, Q(43, 100), zero)
    check('synthetic physical-witness count fixture accepts conditionally', fixture['conditional_decision'] == 'REJECT_SOURCE_MMSE_DOMINANCE')
    uncal = analyze_counts(counts, {-1: n, 1: n}, Q(43, 100))
    check('uncalibrated preparation fails closed', uncal['decision'] == 'PREPARATION_UNCALIBRATED')
    prep = analyze_counts(counts, {-1: n, 1: n}, Q(43, 100), {-1: Q(1, 100), 1: Q(1, 100)})
    check('large preparation allowance blocks acceptance', prep['conditional_decision'] == 'INCONCLUSIVE')
    lossy_probs = {l: [p/S.Integer(1000) for p in probs[l][:-1]] + [S.Rational(999, 1000)]
                   for l in [-1, 1]}
    lossy = {l: rounded_counts(lossy_probs[l], n) for l in [-1, 1]}
    lossy_result = analyze_counts(lossy, {-1: n, 1: n}, Q(43, 100), zero)
    check('all-trial low-efficiency fixture inconclusive', lossy_result['conditional_decision'] == 'INCONCLUSIVE')
    for bad in [({-1: [n, 0, 0, 0, 0], 1: [n-1, 0, 0, 0, 0]}, {-1: n, 1: n}),
                ({-1: [n, 0, 0, 0], 1: [n, 0, 0, 0]}, {-1: n, 1: n}),
                ({-1: [n+1, -1, 0, 0, 0], 1: [n, 0, 0, 0, 0]}, {-1: n, 1: n})]:
        try:
            analyze_counts(*bad, Q(43, 100), zero)
        except ValueError:
            check('invalid denominators/count schema rejected', True)
        else:
            check('invalid denominators/count schema rejected', False)
    lock = json.loads((HERE / 'INPUT_LOCK.json').read_text())
    nfiles = 0
    for root in lock['inputs']:
        for entry in root['files']:
            raw = (Path(root['root']) / entry['path']).read_bytes()
            check('source bytes unchanged', len(raw) == entry['bytes'] and hashlib.sha256(raw).hexdigest() == entry['sha256'])
            nfiles += 1
    result = {'status': 'ARITHMETIC_PASS_NOT_APPARATUS_EVIDENCE',
              'checks_passed': len(CHECKS), 'input_files_unchanged': nfiles,
              'python': sys.version, 'sympy': S.__version__,
              'planning': planning,
              'synthetic_model_fixture': {'meaning': 'Deterministic rounded probabilities of an exact physical existence witness, not acquired or held-out trials',
                                          'exact_model_gain': str(fixture_gain),
                                          'model_gain_decimal': float(fixture_gain),
                                          'no_loss_fixture': fixture,
                                          'one_percent_preparation_uncertainty_fixture': prep,
                                          'fair_one_per_mille_success_fixture': lossy_result},
              'stm': 'FROZEN_NO_GO_BURNED_TEST_UNCHANGED; this program imports no STM code and parses no STM labels; immutable source files are hashed only. No predictions are refit or rescored by this program. A separate authorized portable same-record arithmetic verifier has its own receipt.'}
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
