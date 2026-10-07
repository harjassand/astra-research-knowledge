"""Source-weight information upper from a supplied exact finite matrix table.

No matrix square-root/eigenvalue oracle. PSD is checked by exact Schur steps.
Log intervals reuse an owned implementation; importing it does not run checks.
"""
from fractions import Fraction as F
from pathlib import Path
import sys
import json
import time

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from log_covariance_certificate import log_interval


def psd_check(matrix):
    a = [[F(x) for x in row] for row in matrix]
    d = len(a)
    if not d or any(len(row) != d for row in a):
        raise ValueError('square nonempty matrix required')
    if any(a[i][j] != a[j][i] for i in range(d) for j in range(d)):
        raise ValueError('matrix must be symmetric')
    operations = 0
    max_bits = 0
    rank = 0
    for k in range(d):
        pivot = a[k][k]
        if pivot < 0:
            raise ValueError('negative Schur pivot')
        if pivot == 0:
            if any(a[k][j] != 0 for j in range(k + 1, d)):
                raise ValueError('nonzero row at zero Schur pivot')
            continue
        rank += 1
        for i in range(k + 1, d):
            for j in range(i, d):
                a[i][j] -= a[i][k] * a[k][j] / pivot
                a[j][i] = a[i][j]
                operations += 4
                max_bits = max(max_bits, a[i][j].numerator.bit_length(), a[i][j].denominator.bit_length())
    return {'rank': rank, 'rational_operations': operations, 'max_fraction_bits': max_bits}


def certificate(weights, matrices, cap, eta=F(1, 2**36)):
    weights = list(map(F, weights))
    cap = F(cap)
    if cap <= 0 or len(weights) != len(matrices) or not weights or min(weights) < 0 or sum(weights) != 1:
        raise ValueError('invalid cap/table law')
    d = len(matrices[0])
    stats = []
    energy = F(0)
    for w, matrix in zip(weights, matrices):
        if len(matrix) != d:
            raise ValueError('dimension mismatch')
        stats.append(psd_check(matrix))
        energy += w * sum(F(matrix[i][i]) for i in range(d))
    q = 1 + cap
    # Cancellation-aware absolute H interval, not merely absolute log error.
    lo, hi, terms = log_interval(q, F(eta) * cap**2 / q**2)
    hlo = q**2 / cap**2 * lo - q / cap - F(1, 2)
    hhi = q**2 / cap**2 * hi - q / cap - F(1, 2)
    assert hhi - hlo <= eta
    hlo = max(F(0), hlo)
    glo = max(F(0), (q/cap*lo-1)/2)
    ghi = (q/cap*hi-1)/2
    assert ghi-glo <= eta
    bound = ghi * energy
    return {'cap': str(cap), 'G_lower': str(glo), 'G_upper': str(ghi),
            'H_lower': str(hlo), 'H_upper': str(hhi),
            'mean_trace_exact': str(energy), 'integrated_MI_dT_over_T_squared_upper': str(bound),
            'H_energy_corollary_upper_for_comparison': str(2*hhi*energy),
            'coarse_linear_cap_trace_upper_for_comparison': str(cap*energy/4),
            'upper_float_display_only': float(bound), 'states_read': len(weights), 'dimension': d,
            'scalar_model_entries_read': len(weights) * (d*d + 1),
            'psd_checks': stats, 'atanh_series_terms': terms,
            'H_absolute_interval_width': str(eta),
            'scope': 'Rigorous exact fixed-reference KL integral upper G_L EtrB for supplied PSD-table law. H_L variance branch separately derived but variance not acquired. No MI computation or unknown-field acquisition.'}


def main():
    start = time.perf_counter()
    mats = [[[1, 1], [1, 1]], [[1, 0], [0, 0]], [[0, 0], [0, 2]]]
    weights = [F(1, 4), F(1, 2), F(1, 4)]
    caps = [F(1, 1000), F(1, 2), F(1), F(16), F(256), F(2**20)]
    certs = [certificate(weights, mats, L) for L in caps]
    # Different nullspaces and a noncommuting rank-one matrix are admitted.
    assert sum(F(c['mean_trace_exact']) != F(3, 2) for c in certs) == 0
    bad = [[[0, 1], [1, 0]], [[1, 2], [2, 1]], [[-1]], [[1, 1], [0, 1]]]
    rejections = 0
    for a in bad:
        try:
            psd_check(a)
        except ValueError:
            rejections += 1
        else:
            raise AssertionError('invalid PSD table accepted')
    exact_derivative = 0
    for L in caps:
        q = 1 + L
        for u in [F(1, 3), F(1), F(7)]:
            for T in [F(1, 8), F(1), F(8)]:
                t = T*u*u/L
                a = 1 + L*T*u*u/(L + T*u*u)
                # Squared u derivative / T^2 times dT/dt, no sqrt needed.
                lhs = u*u*L**4 / ((L+T*u*u)**4 * a) * L/(u*u)
                rhs = L / ((1+t)**3*(1+q*t))
                assert lhs == rhs
                exact_derivative += 1
        lo, hi, _ = log_interval(1+L, F(1, 2**32))
        assert F(certs[caps.index(L)]['H_lower']) <= hi
    out = Path(__file__).with_name('trace_information_checks.json')
    result = {'certificates': certs, 'invalid_matrix_rejections': rejections,
              'exact_derivative_change_of_variable_checks': exact_derivative,
              'elapsed_seconds': time.perf_counter() - start,
              'finite_fixtures_are_not_theorem_validation': True}
    out.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'certificates': len(certs), 'exact_derivative_checks': exact_derivative,
                      'invalid_PSD_rejections': rejections, 'seconds': result['elapsed_seconds'], 'output': str(out)}))

if __name__ == '__main__':
    main()
