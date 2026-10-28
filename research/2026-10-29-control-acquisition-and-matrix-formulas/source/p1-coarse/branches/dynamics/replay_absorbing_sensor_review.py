"""Representative exact replay of saved sensor sensitivity; no trajectories."""
from fractions import Fraction as F
from math import isqrt
from pathlib import Path
import hashlib
import json
from replay_multiboundary_review import decode, eye, scale, sub, psd3, vec, check_endpoint

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT/'results/ABSORBING_BOUNDARY_RESULTS.json'
SENSITIVITY = ROOT/'results/ABSORBING_SENSOR_ROBUSTNESS.json'


def square_root_upper(x):
    scale = 10**14
    floor = isqrt(x.numerator*scale*scale//x.denominator)
    if F(floor*floor, scale*scale) < x:
        floor += 1
    result = F(floor, scale)
    assert result*result >= x
    return result


def propagate(modes, word, dynamic):
    low = high = [F(1), F(0), F(0)]
    for i in word:
        low = vec(modes[i]['kernel_lower'], low)
        high = vec(modes[i]['kernel_upper'], high)
    return max(F(0), low[2]), min(F(1), high[2]+dynamic)


def main():
    original = decode(json.loads(BASE.read_text()))
    saved = decode(json.loads(SENSITIVITY.read_text()))
    modes = original['certificate']['modes']
    record = original['receipts'][0]
    m = modes[0]
    for countkey, boundkey, side in (
        ('returned_or_pending', 'excursion_return_row_upper', 'upper'),
        ('even_returned_or_pending', 'even_excursion_return_row_upper', 'upper'),
        ('absorbed_before_boundary_return', 'observed_absorption_row_lower', 'lower')):
        check_endpoint(record[countkey], record['trials'], m[boundkey][0],
                       original['confidence_exponent'], side)
    selected = []
    for eta in (F(0), F(1, 10**6), F(1, 10**4)):
        case = next(x for x in saved['cases'] if x['per_report_error_warranty'] == eta)
        contamination = min(F(1), original['censor_horizon']*eta)
        assert contamination == case['per_trial_contamination_upper']
        theta_max = (case['uniform_point_model_error']-
                     original['certificate']['uniform_structured_correction_noise_bound'])/2
        gal_thetas = []
        for m in modes:
            ru = [min(F(1), x+contamination) for x in m['excursion_return_row_upper']]
            eu = [min(F(1), x+contamination) for x in m['even_excursion_return_row_upper']]
            al = [max(F(0), x-contamination) for x in m['observed_absorption_row_lower']]
            kp = max(min(al), min(1-m['row_mass_intervals'][j][1]-ru[j] for j in range(3)))
            km = min(2*m['kernel_lower'][j][j]+al[j] for j in range(3))
            assert kp > 0 and km > 0
            local = (1/kp+1/km)/2
            q = max(eu)+max(ru)**2*local
            proposed = (square_root_upper(q)+m['operator_error_upper']*square_root_upper(local))**2
            assert psd3(sub(scale(m['budget'], theta_max), scale(eye(3), proposed)))
            gal_thetas.append(q/(1-m['true_kernel_norm_upper']**2))
        dynamic = 2*max(gal_thetas)
        assert dynamic == case['true_galerkin_dynamic_remainder']
        a = propagate(modes, (0,)*10+(1,)*10, dynamic)
        b = propagate(modes, (1,)*10+(0,)*10, dynamic)
        interval = [a[0]-b[1], a[1]-b[0]]
        assert interval == case['transport_difference_interval']
        assert case['order_resolved'] == (interval[0] > 0 or interval[1] < 0)
        selected.append({'eta': str(eta), 'uniform_point_model_error': str(case['uniform_point_model_error']),
                         'order_resolved': case['order_resolved'], 'all_exact_checks_passed': True})
    assert saved['additional_source_queries'] == 0 and saved['confidence_budget_unchanged'] is True
    output = dict(base_result_sha256=hashlib.sha256(BASE.read_bytes()).hexdigest(),
        sensor_result_sha256=hashlib.sha256(SENSITIVITY.read_bytes()).hexdigest(),
        representative_base_confidence_endpoints_checked=3, cases=selected,
        new_trajectories_generated=0, all_reviewed_checks_passed=True)
    path = Path(__file__).with_name('ABSORBING_SENSOR_REVIEW_RESULTS.json')
    path.write_text(json.dumps(output, indent=2)+'\n')
    print(json.dumps(output, indent=2))


if __name__ == '__main__':
    main()
