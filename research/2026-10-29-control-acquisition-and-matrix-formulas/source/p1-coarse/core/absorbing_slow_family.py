"""Exact algebra for a norm-one reachable family; no statistical trials."""
from fractions import Fraction as F
from pathlib import Path
import json


def encoded(x):
    if isinstance(x, F):
        return {'fraction': str(x), 'diagnostic': float(x)}
    if isinstance(x, dict):
        return {k: encoded(v) for k, v in x.items()}
    if isinstance(x, list):
        return [encoded(v) for v in x]
    return x


def run():
    cases = []
    for denominator in [4, 8, 16, 32, 64, 128, 1024]:
        g = F(1, denominator)
        p, coupling, stay, slow = 1-g, g/2, F(1, 4), g**3/16
        horizon = 2
        while stay**(horizon-1) > g/8:
            horizon += 1
        # Sum w_n^2/eta_n = slow/8; sum w_n^2 = slow^2/3.
        return_infinite = coupling**2/(1-stay)+slow/8
        pending_fast = coupling*stay**(horizon-1)
        unresolved_upper = pending_fast+slow
        return_or_pending_upper = return_infinite+unresolved_upper
        assert return_or_pending_upper <= g*g/2
        absorption_lower = g-return_or_pending_upper
        assert absorption_lower >= 7*g/8
        minus_lower = 2*p+absorption_lower
        local_inverse = (1/absorption_lower+1/minus_lower)/2
        q_bound = return_or_pending_upper+local_inverse*return_or_pending_upper**2
        weighted_bound = 2*q_bound/(1-p*p)
        norm_defect = coupling**2+slow**2/3
        unweighted_bound = norm_defect/(1-p)**2
        assert unweighted_bound >= F(1, 4)
        assert weighted_bound <= g
        expected_steps_upper = 1+coupling/(1-stay)+slow*(horizon-1)
        assert expected_steps_upper < 2
        cases.append(dict(g=g, horizon=horizon, boundary_model=p,
            slow_total_coupling=slow, eventual_return_probability=return_infinite,
            pending_probability_upper=unresolved_upper,
            return_or_pending_probability_upper=return_or_pending_upper,
            absorption_probability_lower=absorption_lower,
            local_inverse_dissipation_upper=local_inverse, true_residual_form_upper=q_bound,
            uniform_weighted_dynamic_bound=weighted_bound,
            weighted_bound_divided_by_g=weighted_bound/g,
            uniform_unweighted_dynamic_bound=unweighted_bound,
            expected_steps_per_trial_upper=expected_steps_upper,
            all_exact_inequalities_passed=True))
    result = dict(source_norm='Exactly one at every scale; infinitely many reachable slow states.',
        source_definition='Boundary p=1-g; fast coupling g/2 and stay1/4; slow total S=g^3/16, w_n=S*2^(-n-1), eta_n=4S*2^(-n).',
        scope='Exact source and certificate algebra only. No new sampled trajectories; no budgets represented as execution.',
        cases=cases)
    path = Path(__file__).resolve().parents[1]/'results'/'ABSORBING_SLOW_FAMILY.json'
    path.write_text(json.dumps(encoded(result), indent=2)+'\n')
    for x in cases:
        print(x['g'], x['horizon'], float(x['uniform_weighted_dynamic_bound']),
              float(x['uniform_unweighted_dynamic_bound']), float(x['expected_steps_per_trial_upper']))


if __name__ == '__main__':
    run()
