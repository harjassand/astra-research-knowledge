"""Saved-count and exact-confidence replay of the standard survival baseline."""
from fractions import Fraction as F
from math import factorial
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]
RESULT = ROOT/'results/SURVIVAL_DISTRIBUTION_BASELINE.json'
RAW = ROOT/'results/SURVIVAL_DISTRIBUTION_RAW_RECEIPT.json'
CODE = ROOT/'core/survival_distribution_baseline.py'


def main():
    data = json.loads(RESULT.read_text())
    r, c = data['receipt'], data['certificate']
    assert r == json.loads(RAW.read_text())
    n, cap = r['trials'], r['censor_cap']
    lifetimes = r['lifetimes_or_cap_plus_one']
    assert n > 0 and cap >= 1 and len(lifetimes) == n
    assert all(isinstance(t, int) and 1 <= t <= cap+1 for t in lifetimes)
    censored = sum(t == cap+1 for t in lifetimes)
    assert r['censored_count'] == censored
    steps = sum(min(t, cap) for t in lifetimes)
    assert r['primitive_applications'] == r['coarse_observations'] == steps
    assert r['physical_preparations'] == n
    assert r['last_observation_clock'] == min(max(lifetimes), cap)
    epsilon = F(c['dkw_radius'])
    exponent = 2*n*epsilon**2
    assert exponent == F(c['exact_dkw_exponent'])
    exp_lower = sum((exponent**k/F(factorial(k)) for k in range(60)), F(0))
    assert 2/exp_lower < F(c['failure_probability_upper']) == F(1, 1000)
    assert F(c['all_time_absolute_error_bound']) == epsilon+F(censored, n)
    out = dict(result_sha256=hashlib.sha256(RESULT.read_bytes()).hexdigest(),
        code_sha256=hashlib.sha256(CODE.read_bytes()).hexdigest(),
        lifetimes_replayed=n, censor_cap=cap, censored_count=censored,
        primitive_applications=steps, coarse_observations=steps,
        physical_preparations=n, exact_dkw_exponent=str(exponent),
        all_time_absolute_error_bound=c['all_time_absolute_error_bound'],
        confidence_claim_verified_with_exact_rational_exp_lower_bound=True,
        new_trajectories_generated=0, all_reviewed_checks_passed=True)
    path = Path(__file__).with_name('SURVIVAL_DISTRIBUTION_REVIEW_RESULTS.json')
    path.write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps(out, indent=2))


if __name__ == '__main__':
    main()
