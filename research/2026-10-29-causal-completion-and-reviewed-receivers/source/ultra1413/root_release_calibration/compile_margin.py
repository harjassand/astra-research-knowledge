"""Exact reference-calibration margin; no producer import or source samples."""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import math
import time


def inverse(matrix):
    n = len(matrix)
    rows = [row[:] + [F(i == j) for j in range(n)]
            for i, row in enumerate(matrix)]
    for j in range(n):
        pivot = next(k for k in range(j, n) if rows[k][j])
        rows[j], rows[pivot] = rows[pivot], rows[j]
        scale = rows[j][j]
        rows[j] = [entry / scale for entry in rows[j]]
        for k in range(n):
            if k != j:
                factor = rows[k][j]
                rows[k] = [x - factor*y for x, y in zip(rows[k], rows[j])]
    return [row[n:] for row in rows]


def main():
    start = time.perf_counter()
    root = Path(__file__).resolve().parent
    source_path = root.parent / 'c_independent_opening' / 'SOURCE.json'
    source_bytes = source_path.read_bytes()
    source = json.loads(source_bytes)
    channel = [[F(x) for x in row] for row in source['reference_L']]
    n = len(channel)
    assert n >= 2 and all(len(row) == n for row in channel)
    assert all(x > 0 for row in channel for x in row)
    assert all(sum(channel[y][i] for y in range(n)) == 1 for i in range(n))
    linv = inverse(channel)
    assert all(sum(channel[y][i]*linv[i][z] for i in range(n)) == int(y == z)
               for y in range(n) for z in range(n))
    lower = [min(row) for row in channel]
    upper = [max(row) for row in channel]
    bound = [[sum(channel[y][i]*abs(linv[i][z]) for i in range(n))
              for z in range(n)] for y in range(n)]
    squared = sum(bound[y][z]**2*upper[z]/lower[y]
                  for y in range(n) for z in range(n))
    ceiling = math.isqrt(squared.numerator // squared.denominator)
    if ceiling**2 < squared:
        ceiling += 1
    ceiling = max(1, ceiling)
    assert F(ceiling**2) >= squared
    delta = F(1, 32*ceiling)
    a_bound = delta*ceiling
    nominal = F(source['budget'])
    assert nominal == F(1, 2)
    factor = (1+delta)/(1-a_bound)**2
    robust = nominal*factor
    assert robust <= F(528, 961) < F(3, 5)
    result = {
        'status': 'EXACT_CALIBRATION_MARGIN_CONDITIONAL_ON_NOMINAL_DESIGN',
        'source_path': str(source_path),
        'source_sha256': hashlib.sha256(source_bytes).hexdigest(),
        'reference_alphabet': n,
        'weighted_error_squared_bound_S': str(squared),
        'integer_sqrt_majorant': ceiling,
        'relative_entry_error_delta': str(delta),
        'relative_entry_error_delta_display': float(delta),
        'weighted_relative_error_a_upper': str(a_bound),
        'nominal_information_budget': str(nominal),
        'robust_information_budget_upper': str(robust),
        'robust_information_budget_display': float(robust),
        'additional_physical_or_statistical_premise':
            'actual stochastic Lprime satisfies |Lprime_yi-L_yi| <= delta L_yi',
        'quantum_reference_dimension_factor': False,
        'nominal_release_certificate_rechecked': False,
        'new_channel_samples_or_SDP_runs': 0,
        'seconds_after_stdlib_imports': time.perf_counter()-start,
    }
    (root/'MARGIN.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({key: value for key, value in result.items()
                      if key != 'weighted_error_squared_bound_S'}, indent=2))


if __name__ == '__main__':
    main()
