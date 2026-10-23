"""Exact witness and scalar diagnostics for the instrument-arm theorem.

This is not a norm optimizer and does not prove any universal upper bound.
The witness uses Fraction throughout. Decimal constants are non-interval
diagnostics only; the proof defines c_star by its equation.
"""
import time
_wall_start = time.perf_counter()
import json
import os
import resource
from decimal import Decimal, localcontext
from fractions import Fraction as F
from pathlib import Path

BASE = Path(__file__).resolve().parent
resource.setrlimit(resource.RLIMIT_AS, (512 * 1024**2, 512 * 1024**2))


def matrix_string(matrix):
    return [[str(x) for x in row] for row in matrix]


def exact_witness():
    b, delta, r, s = F(63, 100), F(1, 2000), F(1, 2**500), F(1, 32)
    q = [b, b*r, 1-b-b*r]
    pi = [delta*b*r*r, delta*b*r, 1-delta*b*(r+r*r)]
    W = [pi[i]/q[i] for i in range(3)]
    Q = [[F(0), F(1), F(0)], [F(1), F(0), F(0)], [F(0), F(0), F(1)]]
    G = [[F(0) for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for j in range(3):
            if i != j:
                G[i][j] = q[j]*min(F(1), W[j]/W[i])
        G[i][i] = 1-sum(G[i])
    L = [[1-s, s, F(0)], [r*s, 1-r*s, F(0)], [F(0), F(0), F(1)]]
    C = [[(F(i == j)+F(1, 2)*G[i][j]+F(1, 2)*L[i][j])/2
          for j in range(3)] for i in range(3)]
    T = [[C[0][0], 16*C[0][1]], [C[1][0]/16, C[1][1]]]
    checks = {
        'q_positive': all(x > 0 for x in q),
        'pi_positive': all(x > 0 for x in pi),
        'q_sum_one': sum(q) == 1,
        'pi_sum_one': sum(pi) == 1,
        'Q_symmetric_stochastic': all(Q[i][j] == Q[j][i] for i in range(3) for j in range(3)) and all(sum(row) == 1 for row in Q),
        'unsafe_exactly_0_1': W[0] < F(1, 1000) and W[1] < F(1, 1000) and W[2] > F(1, 1000),
        'weight_order': W[0] < W[1] < W[2],
        'local_screen_root_identity': s**100 == r,
        'tilt_root_identity': F(16)**125*r == 1,
        'local_forward_second_factor_ge_one': (pi[1]/pi[0])/s >= 1,
        'local_reverse_second_factor': (pi[0]/pi[1])*s == r*s,
        'C_positive_stochastic': all(x >= 0 for row in C for x in row) and all(sum(row) == 1 for row in C),
        'C_exact_reversibility': all(pi[i]*C[i][j] == pi[j]*C[j][i] for i in range(3) for j in range(3)),
        'killed_mass_retained': all(sum(C[i][:2]) < 1 for i in (0, 1)),
        'KL_aux_r_small': r < F(1, 1000),
        'KL_safe_q_lower': q[2] > F(36937, 100000) > F(24, 65),
        'KL_unsafe_terms_negative': W[0] < 1 and W[1] < 1,
        'T_diagonal_formula': T[0][0] == F(2879, 3200),
        'T_off_diagonal_formula': T[0][1] == F(1, 8)+4*q[1],
        'norm_power_lower_gt_one': F(3279, 3200)-F(2, 124) == 1+F(849, 99200) > 1,
        'probe_2_power_bound': 26**20 > 2*25**20,
        'probe_log1000_bound': 27**7 > 1000*10**7,
        'probe_e_lower_27_10': F(65, 24) > F(27, 10),
        'probe_e_upper_aux': F(8, 3)+F(5, 96) < F(11, 4),
        'probe_entropy_exponent': F(1008, 999) < F(101, 100),
        'probe_rho_rational': (1+F(1, 2)*F(16, 25)*F(26, 25)+F(1, 2)*F(5, 4)*F(26, 25))/2 == F(4957, 5000),
    }
    assert all(checks.values()), checks
    result = {
        'kind': 'exact rational admissible finite counterexample; analytic norm-power lower certificate',
        'K': 1, 'alpha': '1/2', 'h': '1/1000', 'c': '4/5', 'eta': '1/100',
        'theta': '1/125', 'p': '125/124', 'q': list(map(str, q)),
        'pi': list(map(str, pi)), 'Q': matrix_string(Q), 'G': matrix_string(G),
        'L': matrix_string(L), 'C': matrix_string(C), 'T_AA': matrix_string(T),
        'trial_v': ['1', '0'], 'killed_row_sums': [str(sum(C[i][:2])) for i in (0, 1)],
        'norm_ratio_p_power_lower': str(1+F(849, 99200)),
        'KL_proof': 'Unsafe terms <0; safe term <=log(1/q_safe); q_safe>36937/100000>24/65>exp(-1), where exp(1)>65/24 by its series.',
        'norm_proof': 'For 0<x<=1 and p=125/124, x^p>=x-(p-1); use T00=2879/3200 and T01>1/8. Their p-power sum >=1+849/99200.',
        'checks': checks,
    }
    (BASE/'exact_witness_c08.json').write_text(json.dumps(result, indent=2)+'\n')
    return checks


def constants():
    with localcontext() as ctx:
        ctx.prec = 90
        D = Decimal
        r = (-D(1)).exp()
        def f(c):
            return c*((1-c).ln()*(1-c)/c).exp()
        lo, hi = D('.01'), D('.99')
        for _ in range(300):
            mid = (lo+hi)/2
            if f(mid) < r:
                lo = mid
            else:
                hi = mid
        c = (lo+hi)/2
        h, theta = D('.001'), D('.05')
        entropy = -h*h.ln()-(1-h)*(1-h).ln()
        dh = (-(1+entropy)/(1-h)).exp()
        rho = (1+D('.5')*(1-dh)*(theta*D(2).ln()).exp()
               +D('.5')*((1-theta)*D('1.25').ln()+theta*D(2).ln()).exp())/2
        result = {
            'interpretation': 'Non-interval rounded Decimal diagnostics; universal results use defining equations and exact analytic inequalities.',
            'decimal_precision': ctx.prec, 'bisection_iterations': 300,
            'c_star': str(c), 'Lambda_new': str(1/c), 'delta_h_0001': str(dh),
            'rho_c05_eta01_diagnostic': str(rho), 'S_diagnostic': str(1+1/(2*(1-rho))),
            'rho_c05_eta_le01_certified_rational': '4957/5000',
            'S_certified_rational': '2543/43',
        }
        (BASE/'constants.json').write_text(json.dumps(result, indent=2)+'\n')
        return result


if __name__ == '__main__':
    checks = exact_witness()
    vals = constants()
    usage = resource.getrusage(resource.RUSAGE_SELF)
    costs = {
        'wall_s_since_early_module_start': time.perf_counter()-_wall_start,
        'total_process_cpu_s': usage.ru_utime+usage.ru_stime,
        'peak_rss_kib': usage.ru_maxrss,
        'address_space_limit_bytes': 512*1024**2,
        'threads_env': {k: os.environ.get(k) for k in ['OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS']},
        'exact_checks_count': len(checks), 'constants_queries': 300,
    }
    (BASE/'replay_costs.json').write_text(json.dumps(costs, indent=2)+'\n')
    print(json.dumps({'all_exact_checks_passed': all(checks.values()), 'Lambda_new': vals['Lambda_new'], 'costs': costs}))
