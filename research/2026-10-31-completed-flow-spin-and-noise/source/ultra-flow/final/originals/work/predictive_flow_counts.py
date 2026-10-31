"""End-to-end synthetic inference from finite iid word counts.

The compiler receives empirical word probabilities only. Its statistic is
selected from those counts, so rejection uses a simultaneous confidence box,
not an invalid fixed-statistic test on the same selected data. Stationary
preparation and independence are explicit properties of this simulator.
No physical data or advantage over the reflection comparator is claimed.
"""
from pathlib import Path
from fractions import Fraction as Q
from math import isqrt, log, sqrt, atanh
import json
import sys
import time
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'outputs/predictive_flow'
sys.path.insert(0, str(OUT))
from compile_lp import compile_certificate


def sqrt_upper(value, denominator=10 ** 6):
    top = value.numerator * denominator ** 2
    bottom = value.denominator
    r = isqrt(top // bottom)
    if r * r * bottom < top:
        r += 1
    result = Q(r, denominator)
    assert result * result >= value
    return result


def experiment(name, P, labels, seed, n=20_000):
    start = time.perf_counter()
    rng = np.random.default_rng(seed)
    # Both supplied synthetic chains are doubly stochastic. Each window
    # starts from an independent exact-uniform stationary state.
    state = rng.integers(len(P), size=n)
    labels = np.asarray(labels, dtype=int)
    word = labels[state].copy()
    for _ in range(2):
        u = rng.random(n)
        state = (u[:, None] >= np.cumsum(P[state], axis=1)).sum(axis=1)
        word = 2 * word + labels[state]
    counts = np.bincount(word, minlength=8).tolist()
    data = {'alphabet_size': 2, 'depth': 1, 'probabilities': [str(Q(c, n)) for c in counts], 'window_count': n, 'word_counts': counts, 'data_source': 'synthetic iid stationary three-letter windows', 'source_seed': seed}
    (OUT / f'{name}_counts.json').write_text(json.dumps(data, indent=2) + '\n')
    certificate = compile_certificate(data, 8)
    (OUT / f'{name}_certificate.json').write_text(json.dumps(certificate, indent=2) + '\n')
    alpha = Q(1, 40)
    m = len(counts)
    # e>2, so this integer C exceeds log(2*m/alpha).
    C = (int(2 * m / alpha) - 1).bit_length()
    radius_squared = Q(C, 2 * n)
    delta = Q(0)
    norm = Q(0)
    if certificate['certificate_status'] == 'RATIONAL_DUAL_PROPOSED':
        delta = Q(certificate['exact_source_gap'])
        y = list(map(Q, certificate['data_duals']))
        norm = sum(abs(y[2 * i] - y[2 * i + 1]) for i in range(m))
    reject = delta > 0 and delta ** 2 > norm ** 2 * radius_squared
    # Matched ordinary reflection comparator: fixed statistic f(Y0)f(Y2).
    # It uses the very same windows and assumes no hidden-state count.
    reflection = sum((Q(counts[w], n) * (1 - 2 * (w // 4)) * (1 - 2 * (w % 2)) for w in range(8)), Q(0))
    scalar_C = (int(1 / alpha) - 1).bit_length()
    scalar_radius_squared = Q(2 * scalar_C, n)
    scalar_reject = reflection < 0 and reflection ** 2 > scalar_radius_squared
    c2_upper = reflection + sqrt_upper(scalar_radius_squared)
    b_squared_lower = max(Q(0), -c2_upper)
    cost_display = 2 * sqrt(float(b_squared_lower)) * atanh(sqrt(float(b_squared_lower))) if b_squared_lower else 0.
    out = {'data_source': data['data_source'], 'stationary_preparations': n, 'independent_windows': n, 'observed_letters': 3 * n, 'simulated_transitions': 2 * n, 'compiler_received_hidden_transition_matrix': False, 'pointwise_error_alpha_each_method': str(alpha), 'selection_safe_uniform_radius_squared': str(radius_squared), 'certified_dual_gap_on_empirical_data': str(delta), 'data_dual_L1_norm': str(norm), 'selection_safe_LP_rejects': bool(reject), 'ordinary_reflection_rejects': bool(scalar_reject), 'ordinary_reflection_empirical_mean': str(reflection), 'ordinary_scalar_radius_squared': str(scalar_radius_squared), 'architecture_free_cost_lower_bound_formula': f'2*sqrt({b_squared_lower})*artanh(sqrt({b_squared_lower}))', 'architecture_free_cost_lower_bound_numeric_display': cost_display, 'exact_certificate_independent_receiver': 'PENDING', 'seconds': time.perf_counter() - start}
    print(json.dumps({'case': name, **out}), flush=True)
    return out


def main():
    P = np.array([[0, .75, .25, 0], [.25, 0, 0, .75], [.75, 0, 0, .25], [0, .25, .75, 0]])
    null = np.array([[.5, .25, .25], [.25, .75, 0], [.25, 0, .75]])
    assert np.allclose(P.sum(axis=0), 1) and np.allclose(null.sum(axis=0), 1)
    rows = {'sampled_source': experiment('sampled_source', P, [0, 0, 1, 1], 7301621), 'sampled_null': experiment('sampled_null', null, [0, 0, 1], 7301622)}
    assert rows['sampled_source']['selection_safe_LP_rejects']
    assert not rows['sampled_null']['selection_safe_LP_rejects']
    (OUT / 'finite_counts.json').write_text(json.dumps({'scope': __doc__, 'cases': rows}, indent=2) + '\n')


if __name__ == '__main__':
    main()
