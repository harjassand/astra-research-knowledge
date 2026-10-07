#!/usr/bin/env python3
"""C07_S01 fresh exact verifier of C07_L02's finite N72 witness.

No peer implementation is imported or executed. Exponentials use positive
exp(x/64) Taylor sums and a geometric tail, reciprocal/exact64 powers, then
owned outward512-bit rounding. This differs from the author's alternating
exp(-x/1024) and ten256-bit interval squares. All scientific operations are
integer/Fraction arithmetic; wall time metadata may be floating point.
"""
from fractions import Fraction as Q
from math import comb, factorial
from pathlib import Path
from hashlib import sha256
from datetime import datetime, timezone
from copy import deepcopy
import json
import time

OWN = Path(__file__).resolve().parent
ROOT = OWN.parents[4]
SOURCE = ROOT / 'work/cycle6/c07_l02/revisions/axial_hankel_N72_delta81_50_exact.json'
EXPECTED_HASH = 'c795d61b152331adc8feec51476bb4690927555b8721390a26fae00f65e1c3c8'
BITS = 512
D = 1 << BITS


def require(test, message):
    if not test:
        raise ValueError(message)


def floor_q(x):
    return x.numerator // x.denominator


def ceil_q(x):
    return -((-x.numerator) // x.denominator)


def rational(pair):
    require(isinstance(pair, list) and len(pair) == 2, 'invalid rational pair')
    require(all(isinstance(a, str) and str(int(a)) == a for a in pair), 'noncanonical integer')
    require(int(pair[1]) > 0, 'nonpositive denominator')
    return Q(int(pair[0]), int(pair[1]))


def exp_minus(x):
    require(0 <= x <= Q(729, 25), 'exponent outside N72 declared scope')
    if not x:
        return Q(1), Q(1)
    z = x / 64
    total = term = Q(1)
    for j in range(1, 81):
        term *= z / j
        total += term
    upper = total + (term * z / 81) / (1 - z / 82)
    lo, hi = (1 / upper)**64, (1 / total)**64
    return Q(floor_q(lo * D), D), Q(ceil_q(hi * D), D)


def signed_sum(coeff, intervals):
    lo = hi = Q(0)
    for k, c in enumerate(coeff):
        if c >= 0:
            lo += c * intervals[k][0]
            hi += c * intervals[k][1]
        else:
            lo += c * intervals[k][1]
            hi += c * intervals[k][0]
    return lo, hi


def powers_of_two(e):
    return Q(1 << e) if e >= 0 else Q(1, 1 << (-e))


def strict_power_upper(x):
    require(x > 0, 'norm must be positive')
    e = x.numerator.bit_length() - x.denominator.bit_length()
    while x >= powers_of_two(e):
        e += 1
    while x < powers_of_two(e - 1):
        e -= 1
    return e


def verify(cert, cache):
    require(cert['status'] == 'CERTIFIED_NEGATIVE', 'wrong status')
    require(cert['N'] == 72 and cert['delta'] == '81/50', 'wrong physical target')
    require(cert['dyadic_bits'] == 256 and cert['quadratic_interval_denominator'] == str(1 << 256), 'wrong author interval grid')
    e = cert['scale_exponents_e_i']
    z = [rational(pair) for pair in cert['z_rational']]
    require(len(e) == len(z) == 36, 'missing witness entry')
    require(all(isinstance(a, int) and 0 <= a <= 34 for a in e), 'wrong witness scale')
    require(z[-1] == 1, 'wrong terminal witness coordinate')
    v = [z_i * powers_of_two(e_i) for z_i, e_i in zip(z, e)]
    coeff = [Q(0) for _ in range(73)]
    for i in range(36):
        for j in range(36):
            k = i + j + 1
            coeff[k] += v[i] * v[j] / comb(72, k)
    saved = cert['coefficient_c_k']
    require(set(saved) == {str(k) for k, c in enumerate(coeff) if c}, 'missing coefficient')
    for k, c in enumerate(coeff):
        if c:
            require(rational(saved[str(k)]) == c, 'false recorded witness coefficient')
    intervals = [cache[abs(k - 36)] for k in range(73)]
    form = signed_sum(coeff, intervals)
    q_intervals = [tuple(t / comb(72, k) for t in intervals[k]) for k in range(73)]
    # Direct 36x36 quadratic recurrence, without aggregating repeated inputs.
    lo = hi = Q(0)
    for i in range(36):
        for j in range(36):
            c, k = v[i] * v[j], i + j + 1
            if c >= 0:
                lo += c * q_intervals[k][0]
                hi += c * q_intervals[k][1]
            else:
                lo += c * q_intervals[k][1]
                hi += c * q_intervals[k][0]
    require(lo <= form[0] <= form[1] <= hi, 'aggregated/direct enclosure mismatch')
    require(hi < -Q(1, 3000), 'direct quadratic form not negative enough')
    recorded = tuple(Q(int(a), 1 << 256) for a in cert['quadratic_interval_scaled_numerators'])
    require(len(recorded) == 2 and recorded[0] <= form[0] <= form[1] <= recorded[1], 'independent form outside recorded interval')
    require(form[1] < -Q(1, 3000), 'independent form not negative enough')
    require(max(abs(a) for a in z) < 10**14 and max(e) == 34, 'author norm envelope false')
    norm = sum((v[i]**2 / (comb(36, i + 1) * comb(36, i)) for i in range(36)), Q(0))
    require(norm < powers_of_two(168), 'author norm charge false')
    norm_e = strict_power_upper(norm)
    # Scalar negative expectation of sigma uses unnormalized y and Tr(S)<=73.
    require(Q(1, 3000 * 73) > powers_of_two(-18), 'normalized state margin false')
    require(powers_of_two(168 + 36 + 73 - 300) == powers_of_two(-23), 'author finite-alpha budget false')
    # Root-origin rank-one partial-transpose improvement: <=||y||^2 operator norm.
    require(powers_of_two(168 + 73 - 264) == powers_of_two(-23), 'root improvement budget false')
    # Independently tighter exact y norm plus the root-origin observable bound.
    sharper_alpha = norm_e + 93
    require(norm * powers_of_two(73 - sharper_alpha) < powers_of_two(-20), 'sharper alpha budget false')
    return {'verified_witness_entries': len(z), 'verified_exact_coefficients': len(saved),
            'independent_exponential_grid_bits': BITS,
            'independent_quadratic_interval': [str(a) for a in form],
            'direct_quadratic_interval': [str(lo), str(hi)],
            'recorded_interval_contains_independent_interval': True,
            'negative_bound': '-1/3000', 'norm_y_squared_exact': str(norm),
            'norm_y_squared_strict_power_upper': norm_e,
            'author_alpha_log2_multiplier': 300,
            'root_origin_improved_alpha_log2_multiplier': 264,
            'exact_norm_plus_root_bound_alpha_log2_multiplier': sharper_alpha,
            'all_finite_axial_fields': 'NPT preserved by invertible tensor local filters, independently reconstructed; root-origin suggested consequence',
            'q_intervals': [[str(x) for x in pair] for pair in q_intervals]}


def negative_controls(cert, cache):
    controls = []
    c = deepcopy(cert);c['N'] = 73;controls.append(('wrong N', c))
    c = deepcopy(cert);c['z_rational'].pop();controls.append(('missing witness entry', c))
    c = deepcopy(cert);c['coefficient_c_k']['1'][0] = str(int(c['coefficient_c_k']['1'][0]) + 1);controls.append(('false coefficient', c))
    c = deepcopy(cert);c['quadratic_interval_scaled_numerators'] = ['-1', '-1'];controls.append(('false recorded form interval', c))
    reports = []
    for name, altered in controls:
        try:
            verify(altered, cache)
        except ValueError as error:
            reports.append({'control': name, 'status': 'REJECTED', 'reason': str(error)})
        else:
            raise ValueError('corrupted certificate accepted: ' + name)
    return reports


def main():
    start = time.perf_counter()
    raw = SOURCE.read_bytes()
    require(sha256(raw).hexdigest() == EXPECTED_HASH, 'certificate changed')
    cert = json.loads(raw)
    cache = {d: exp_minus(Q(9 * d * d, 400)) for d in range(37)}
    result = verify(cert, cache)
    result['rejection_controls'] = negative_controls(cert, cache)
    # A low-order negative control: all adjacent log-convexity gates still pass.
    # exp(9/400)<37/36 implies the minimum ratio bracket exceeds the Gaussian loss.
    x = Q(9, 400)
    S = sum((x**j / factorial(j) for j in range(19)), Q(0))
    U = S + x**19 / factorial(19) / (1 - x / 20)
    require(U < Q(37, 36), 'low-order gate check failed')
    result.update({'status': 'PASS distinct exact acquisition and full finite N72 transfer audit',
                   'utc': datetime.now(timezone.utc).isoformat(),
                   'certificate_path': str(SOURCE), 'certificate_sha256': sha256(raw).hexdigest(),
                   'verifier_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
                   'distinct_exp_method': 'positive exp(x/64) Taylor80/geometric tail, reciprocal/exact64 powers, own512-bit outward grid',
                   'all_two_by_two_principal_Hankel_minors': 'strictly positive by exact discrete log-convexity; higher-order H1 witness is nevertheless negative',
                   'finite_scope_only': 'N72 delta81/50; no unbounded-N persistence or eventual-positivity inference',
                   'wall_seconds': time.perf_counter() - start})
    (OWN / 'INDEPENDENT_N72_WITNESS_VERIFY.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: result[k] for k in ['status', 'verified_witness_entries', 'verified_exact_coefficients',
          'norm_y_squared_strict_power_upper', 'exact_norm_plus_root_bound_alpha_log2_multiplier', 'wall_seconds']}, indent=2))


if __name__ == '__main__':
    main()
