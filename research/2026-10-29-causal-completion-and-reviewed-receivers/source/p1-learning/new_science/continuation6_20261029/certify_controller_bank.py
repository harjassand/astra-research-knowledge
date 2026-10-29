"""Exact arithmetic audit of the saved learner bank, without new trials.

All importance estimates share an integer denominator on the dyadic grid.
The log ceiling is certified by a positive exponential Taylor partial sum;
square-root ceilings are checked with integer arithmetic. Floating point
only nominates constants subsequently verified by rational inequalities.
"""
from pathlib import Path
from fractions import Fraction as F
from math import factorial, lcm, ceil, log, isqrt
import hashlib
import json
import numpy as np

ROOT = Path(__file__).resolve().parent
T, N, L = 64, 131072, 4096
BETA = F(1, 100)


def ceil_fraction(x):
    return (x.numerator+x.denominator-1)//x.denominator


def main():
    bank_path = ROOT/'controller_learning_records/kt_bank.npz'
    bank = np.load(bank_path)
    counts, reads = bank['counts'], bank['reads']
    assert len(counts) == N and set(np.unique(reads)) <= {0, 1}
    rewards = [int(np.count_nonzero((counts == k) & (reads == 1)))
               for k in range(T+1)]
    coefficients = []
    for k in range(T+1):
        qword = F(factorial(2*k)*factorial(2*(T-k)),
                  4**T*factorial(k)*factorial(T-k)*factorial(T))
        coefficients.append(rewards[k]/qword)
    D = lcm(*(x.denominator for x in coefficients))
    integer_coefficients = [x.numerator*(D//x.denominator)
                            for x in coefficients]
    denominator = N*D*L**T
    numerators = []
    for m in range(L+1):
        xp, yp = [1], [1]
        for _ in range(T):
            xp.append(xp[-1]*m)
            yp.append(yp[-1]*(L-m))
        numerators.append(sum(integer_coefficients[k]*xp[k]*yp[T-k]
                              for k in range(T+1)))
    selected = max(range(L+1), key=numerators.__getitem__)
    assert selected == 3086

    # C >= 2 sqrt(T+1), certified by its square.
    C = F(16124515497, 10**9)
    assert C*C >= 4*(T+1)
    log_argument = F(2*(L+1), 1)/BETA
    x = F(ceil(log(float(log_argument))*10**9), 10**9)
    term = F(1)
    exp_lower = term
    for k in range(1, 81):
        term *= x/k
        exp_lower += term
    assert exp_lower >= log_argument  # Positivity proves x >= log(argument).
    variance_term = 2*C*x/N
    linear_term = 2*C*x/(3*N)
    root_scale = 10**12
    root_num = isqrt((variance_term.numerator*root_scale**2)
                     //variance_term.denominator)+1
    root_upper = F(root_num, root_scale)
    assert root_upper*root_upper >= variance_term
    radius = F(ceil_fraction((root_upper+linear_term)*10**9), 10**9)
    assert radius > linear_term
    assert (radius-linear_term)**2 >= variance_term

    exact_selected = F(numerators[selected], denominator)
    exact_half = F(numerators[L//2], denominator)
    regret = 2*radius+F(T, L)
    improvement = exact_selected-exact_half-2*radius
    # These are the outward-rounded bounds stated in the saved report.
    assert regret <= F(133619738, 10**9)
    assert improvement >= F(191929786, 10**9)
    result = {
        'status': 'exact rational selection and finite-grid confidence arithmetic PASS',
        'bank_sha256': hashlib.sha256(bank_path.read_bytes()).hexdigest(),
        'episodes': N, 'horizon': T, 'grid_denominator': L,
        'selected_numerator': selected, 'selected_probability': str(F(selected,L)),
        'all_grid_estimates_exactly_compared': L+1,
        'common_estimate_denominator_bits': denominator.bit_length(),
        'C_upper': str(C), 'log_argument': str(log_argument),
        'log_upper': str(x), 'exponential_partial_sum_terms': 81,
        'radius_upper': str(radius),
        'regret_upper': str(regret), 'regret_upper_decimal': float(regret),
        'improvement_lower_exact': str(improvement),
        'reported_improvement_lower': '0.191929786',
        'reported_global_regret_upper': '0.133619738',
        'confidence_failure_probability': str(BETA),
        'additional_physical_trials': 0,
        'scope': 'arithmetic only; sampling/start, sensor and timing premises remain unchanged'
    }
    (ROOT/'EXACT_CONTROLLER_CERTIFICATE.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k: result[k] for k in ['status','selected_probability',
                     'radius_upper','reported_improvement_lower',
                     'reported_global_regret_upper','additional_physical_trials']},indent=2))


if __name__ == '__main__':
    main()
