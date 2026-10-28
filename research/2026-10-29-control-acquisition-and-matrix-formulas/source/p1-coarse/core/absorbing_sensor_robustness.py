"""Same-count sensitivity to bounded live/absorbed report errors; no new trials."""
from pathlib import Path
from fractions import Fraction as F
from copy import deepcopy
import json
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'branches'/'physical'))
from rational_linalg import Mat, diag
from multiboundary_positive_events import sqrt_upper, dominate, dumpable, compare_words


def decode(x):
    if isinstance(x, dict):
        if 'fraction' in x:
            return F(x['fraction'])
        return {k: decode(v) for k, v in x.items()}
    if isinstance(x, list):
        return [decode(v) for v in x]
    return x


def run():
    original = decode(json.loads((ROOT/'results'/'ABSORBING_BOUNDARY_RESULTS.json').read_text()))
    base = original['certificate']
    for mode in base['modes']:
        for key in ['model', 'kernel_lower', 'kernel_upper', 'entry_radius', 'budget', 'structured_uncertainty_form']:
            mode[key] = Mat(mode[key])
    records = []
    for eta in [F(0), F(1, 10**8), F(1, 10**7), F(1, 10**6), F(1, 10**5), F(1, 10**4)]:
        c = deepcopy(base)
        contamination = min(F(1), original['censor_horizon']*eta)
        for m in c['modes']:
            ru = [min(F(1), x+contamination) for x in m['excursion_return_row_upper']]
            eu = [min(F(1), x+contamination) for x in m['even_excursion_return_row_upper']]
            al = [max(F(0), x-contamination) for x in m['observed_absorption_row_lower']]
            kp = max(min(al), min(1-m['row_mass_intervals'][j][1]-ru[j] for j in range(3)))
            km = min(2*m['kernel_lower'][j, j]+al[j] for j in range(3))
            assert kp > 0 and km > 0
            local = (1/kp+1/km)/2
            qt = max(eu)+max(ru)**2*local
            qp = (sqrt_upper(qt)+m['operator_error_upper']*sqrt_upper(local))**2
            m.update(excursion_return_row_upper=ru, even_excursion_return_row_upper=eu,
                     observed_absorption_row_lower=al, boundary_schur_plus_lower=kp,
                     boundary_schur_minus_lower=km, local_boundary_inverse_dissipation_upper=local,
                     true_galerkin_form_operator_upper=qt, proposed_form_operator_upper=qp,
                     theta_squared=dominate(qp*diag(1, 1, 1), m['budget']),
                     robust_galerkin_theta_squared=qt/(1-m['true_kernel_norm_upper']**2))
        remainder = 2*max(m['theta_squared'] for m in c['modes'])
        c['uniform_signed_remainder_bound'] = remainder
        c['uniform_all_word_bound'] = remainder+c['uniform_correction_noise_bound']
        c['uniform_structured_all_word_bound'] = remainder+c['uniform_structured_correction_noise_bound']
        c['robust_galerkin_uniform_dynamical_bound'] = 2*max(m['robust_galerkin_theta_squared'] for m in c['modes'])
        if eta == 0:
            assert c['uniform_structured_all_word_bound'] == base['uniform_structured_all_word_bound']
        comparison = compare_words(c, (0,)*10+(1,)*10, (1,)*10+(0,)*10, 0, 2)
        records.append(dict(per_report_error_warranty=eta, per_trial_contamination_upper=contamination,
            uniform_point_model_error=c['uniform_structured_all_word_bound'],
            true_galerkin_dynamic_remainder=c['robust_galerkin_uniform_dynamical_bound'],
            transport_difference_interval=comparison['robust_galerkin_difference_interval'],
            order_resolved=comparison['robust_galerkin_order_resolved']))
    result = dict(scope='Same counts under a specified live/absorbed sensor error warranty; exact boundary labels retained. Warranty not acquired here.',
                  additional_source_queries=0, confidence_budget_unchanged=True, cases=records)
    (ROOT/'results'/'ABSORBING_SENSOR_ROBUSTNESS.json').write_text(json.dumps(dumpable(result), indent=2)+'\n')
    for x in records:
        print(float(x['per_report_error_warranty']), float(x['uniform_point_model_error']),
              [float(v) for v in x['transport_difference_interval']], x['order_resolved'])


if __name__ == '__main__':
    run()
