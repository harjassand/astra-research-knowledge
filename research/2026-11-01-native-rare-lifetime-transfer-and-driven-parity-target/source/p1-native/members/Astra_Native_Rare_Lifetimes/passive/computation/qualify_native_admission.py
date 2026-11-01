"""Invert native count/exposure confidence intervals and check all-cell admission."""
from pathlib import Path
import json
import math
import numpy as np

HERE = Path(__file__).resolve().parent
raw = json.loads((HERE / 'native_rate_counts.json').read_text())
alpha, proposed_eta = 0.001, 0.04
cells = raw['cells']
z = math.log(2 * len(cells) / alpha)


def deviance(mu, count):
    if count == 0:
        return mu
    if mu == 0:
        return math.inf
    return count * math.log(count / mu) - count + mu


def interval(count, exposure):
    # Conservative outward numerical pad; this is a floating-point prototype.
    if count == 0:
        return 0.0, (z / exposure) * (1 + 1e-11)
    lo, hi = 0.0, float(count)
    for _ in range(80):
        mid = (lo + hi) / 2
        if deviance(mid, count) > z:
            lo = mid
        else:
            hi = mid
    lower = lo / exposure
    lo, hi = float(count), 2.0 * (count + z)
    while deviance(hi, count) < z:
        hi *= 2
    for _ in range(80):
        mid = (lo + hi) / 2
        if deviance(mid, count) < z:
            lo = mid
        else:
            hi = mid
    return lower * (1 - 1e-11), (hi / exposure) * (1 + 1e-11)


eta_needed = 0.0
covered = True
q0 = np.zeros((16, 16))
q = np.zeros((16, 16))
for cell in cells:
    lower, upper = interval(cell['count'], cell['exposure'])
    ref = cell['reference_rate']
    cell['confidence_lower'] = lower
    cell['confidence_upper'] = upper
    cell['admitted'] = lower >= (1 - proposed_eta) * ref and upper <= (1 + proposed_eta) * ref
    eta_needed = max(eta_needed, 1 - lower / ref, upper / ref - 1)
    i = (cell['mask'] & -cell['mask']).bit_length() - 1
    sign = 1 if (cell['context_value'].bit_count() + i) % 2 == 0 else -1
    actual_rate = ref * (1 + raw['actual_relative_rate_error'] * sign)
    covered = covered and lower <= actual_rate <= upper
    for x in range(16):
        if x & cell['context_mask'] == cell['context_value']:
            y = x ^ cell['mask']
            q0[x, y] = ref
            q[x, y] = actual_rate
q0 -= np.diag(q0.sum(axis=1))
q -= np.diag(q.sum(axis=1))
a = q.T.copy()
a[-1] = 1
rhs = np.zeros(16)
rhs[-1] = 1
pi = np.linalg.solve(a, rhs)
assert pi.min() > 0
assert all(c['admitted'] for c in cells)
assert covered
assert np.max(np.abs(np.ones(16) @ q)) > 1e-6

# Is the actual law a nearest-neighbor path law? Check the 0--1--2 marginal.
triple = np.zeros((2, 2, 2))
for x in range(16):
    triple[(x & 1), ((x >> 1) & 1), ((x >> 2) & 1)] += pi[x]
p01 = triple.sum(axis=2)
p12 = triple.sum(axis=0)
p1 = triple.sum(axis=(0, 2))
path_residual = max(abs(triple[i, j, k] * p1[j] - p01[i, j] * p12[j, k])
                    for i in range(2) for j in range(2) for k in range(2))

cap, c, g = float((-np.diag(q0)).max()), 0.5, 1.0
a0 = proposed_eta * cap / (c * (1 - proposed_eta))
beta = a0 / (1 + a0)
r = math.log(4 * (4 - 1) / beta) / (2 * c)
u = 2 * proposed_eta * cap * r / (1 - proposed_eta) - math.log(1 - beta)
v = u - math.log(1 - proposed_eta)
log_f = 2 * math.asinh(math.sqrt(2 * cap / g) * math.sinh(v / 2))
result = {
    'n': 4, 'all_aggregate_local_cells': len(cells),
    'initial_state': 0, 'burn_in': 0, 'resets': 0,
    'observed_interface': 'Only actual full-state jumps and calibrated holding times.',
    'quota_per_cell': raw['quota'],
    'native_jumps': raw['native_jumps'],
    'native_elapsed_time': raw['native_elapsed_time'],
    'theoretical_simultaneous_confidence': 1 - alpha,
    'proposed_relative_admission_box': proposed_eta,
    'smallest_box_containing_computed_intervals': eta_needed,
    'all_cells_admitted': all(c['admitted'] for c in cells),
    'simulation_truth_covered': covered,
    'actual_rate_box': raw['actual_relative_rate_error'],
    'actual_stationary_max_relative_deviation_from_uniform': float(np.max(np.abs(16 * pi - 1))),
    'actual_path_markov_conditional_independence_residual': float(path_residual),
    'general_mean_log_factor_from_certified_box': 3 * u + log_f,
    'warning': 'Admission-interface demonstration only. This deliberately modest run gives a broad lifetime factor; it is not an efficient rare-lifetime experiment. Floating-point simulation and confidence inversion are prototypes, not interval-arithmetic certification.',
    'cells': cells,
}
(HERE / 'native_admission_results.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({k: value for k, value in result.items() if k != 'cells'}))
