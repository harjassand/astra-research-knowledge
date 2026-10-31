"""Finite check of non-Markov bin fibres using explicit Weibull primitives."""

import itertools
import json
import math
from pathlib import Path
import sys
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'new_rare_event'))
from event_time_compiler import LocalRate, local_hazard_before
from check_cascade_lifting import independent_held_bins


def main():
    rates = [LocalRate((2,), np.array([0.4, 4.0])),
             LocalRate((0,), np.array([0.0, 3.0])),
             LocalRate((1,), np.array([0.05, 5.0]))]
    shapes = np.array([1.4, 2.0, 3.0])
    bins, deadline = 3, 0.7
    dt = deadline / bins
    rng = np.random.default_rng(4312)
    mass, assignments, draws = 0.0, 0, 0
    for values in itertools.product(range(bins+1), repeat=len(rates)):
        kv = np.array(values)
        local = []
        log_p = 0.0
        for i, rate in enumerate(rates):
            low, exposure = local_hazard_before(i, rate, kv, bins, deadline)
            lower_exp = low ** shapes[i]
            upper_exp = math.inf if values[i] == bins else (low+exposure*dt) ** shapes[i]
            if upper_exp == lower_exp:
                log_p = -math.inf
                break
            log_p += -lower_exp if math.isinf(upper_exp) else -lower_exp + math.log(-math.expm1(-(upper_exp-lower_exp)))
            local.append((lower_exp, upper_exp))
        if not math.isfinite(log_p):
            continue
        mass += math.exp(log_p)
        assignments += 1
        for _ in range(20):
            threshold = np.empty(len(rates))
            for i, (low, high) in enumerate(local):
                transformed = low + (rng.exponential() if math.isinf(high) else
                                      -math.log1p(-rng.random()*(-math.expm1(-(high-low)))))
                threshold[i] = transformed ** (1/shapes[i])
            returned = independent_held_bins(rates, threshold, bins, deadline)
            assert np.array_equal(returned, kv)
            draws += 1
    assert abs(mass-1) < 1e-13
    result = {'threshold_laws': 'independent unit-scale Weibull',
              'shapes': shapes.tolist(), 'rescaling_exponent_D': float(shapes.sum()),
              'normalization_error': abs(mass-1), 'positive_assignments_checked': assignments,
              'conditional_threshold_draws_checked': draws,
              'all_reconstructed_drivers_return_original_bin_assignment': True,
              'scope': 'Finite mechanism check, not a complexity or total-variation certification.'}
    Path(__file__).with_name('weibull_fibre_results.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
