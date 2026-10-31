#!/usr/bin/env python3
"""Adversarial hypothesis, scale and conventional-comparator controls."""
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path
import hashlib
import json
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'outputs/pulse_entropy'
sys.path.insert(0, str(ROOT/'work'))
from pulse_entropy import linear_min, logs, cp_box, dual_witness
from pulse_entropy_source import population, generator, B, T
from kinetic_incumbent_control import finite_tail_controls
from ctmc_reflection_control import exp_negative_bounds


def mvrow(pi, Q):
    return [sum((pi[i]*Q[i][j] for i in range(len(pi))), F(0)) for j in range(len(pi))]


def repair(Q):
    for i in range(len(Q)):
        Q[i][i] = -sum(Q[i][j] for j in range(len(Q)) if j != i)
    return Q


def reference_checks():
    rows = []
    for pi in ([F(1, 2), F(1, 3), F(1, 6)], [F(1, 10), F(2, 10), F(3, 10), F(4, 10)]):
        n = len(pi)
        Q = [[F(0) for _ in pi] for _ in pi]
        R = [[F(0) for _ in pi] for _ in pi]
        for i in range(n):
            j = (i+1) % n
            Q[i][j] = 9/pi[i]
            Q[j][i] = 4/pi[j]
            R[i][j] = 6/pi[i]
            R[j][i] = 6/pi[j]
        repair(Q); repair(R)
        assert mvrow(pi, Q) == [0]*n and mvrow(pi, R) == [0]*n
        gates = [[F(1+(i+j) % 4) for j in range(n)] for i in range(n)]
        Qm = repair([[gates[i][j]*Q[i][j] if i != j else F(0) for j in range(n)] for i in range(n)])
        Rm = repair([[gates[i][j]*R[i][j] if i != j else F(0) for j in range(n)] for i in range(n)])
        assert mvrow(pi, Rm) == [0]*n
        H = F(n)
        sigma_lower = 5*n*logs(F(9, 4))[0]
        assert 4*H <= sigma_lower
        pair_KL_rate = F(0)
        for i in range(n):
            j = (i+1) % n
            a, b, c = pi[i]*Q[i][j], pi[j]*Q[j][i], pi[i]*R[i][j]
            assert c*c == a*b and (c/a)*(c/b) == 1
            pair_KL_rate += gates[i][j]*(a+b-2*c)
        assert pair_KL_rate <= 4*H
        rows.append({'pi': list(map(str, pi)), 'Q_stationary_exact': True, 'R_stationary_exact': True,
            'symmetric_R_pulse_stationary_exact': True,
            'actual_Q_pulse_changes_pi': mvrow(pi, Qm) != [0]*n,
            'H': str(H), 'sigma_lower': str(sigma_lower),
            'reverse_path_KL_rate_exact': str(pair_KL_rate),
            'jump_log_cancellation_exact': True})
    return rows


def vertex_min(coeff, box):
    """Independent exhaustive four-variable vertex receiver for LP control."""
    best = None
    for free in range(4):
        fixed = [j for j in range(4) if j != free]
        for sides in product((0, 1), repeat=3):
            p = [F(0)]*4
            for j, side in zip(fixed, sides):
                p[j] = box[j][side]
            p[free] = 1-sum(p)
            if box[free][0] <= p[free] <= box[free][1]:
                value = sum((c*x for c, x in zip(coeff, p)), F(0))
                best = value if best is None else min(best, value)
    return best


def main():
    start = time.perf_counter()
    references = reference_checks()
    LP_cases = 0
    for box in [[(F(0), F(1))]*4, [(F(1, 10), F(2, 5))]*4,
                [(F(1, 5), F(3, 10)), (F(1, 10), F(3, 5)), (F(0), F(1, 2)), (F(0), F(3, 4))]]:
        for coeff in [[F(1), F(-2), F(3), F(0)], [F(0)]*4, [F(2), F(1, 3), F(-1, 5), F(-3)]]:
            assert linear_min(coeff, box)[0] == vertex_min(coeff, box)
            LP_cases += 1
    # Stationarity is essential even when the microscopic gate is symmetric.
    elo, ehi = exp_negative_bounds(F(2), 100)
    nonstationary_terminal = ((1+elo)/2, (1+ehi)/2)
    assert nonstationary_terminal[1] < 1
    # A source-clock/asymmetric pulse on a stationary reversible two-state
    # chain changes the mean; it is NOT an allowed symmetric rate pulse.
    alo, ahi = exp_negative_bounds(F(3, 2), 100)
    asymmetric_terminal = (F(1, 3)+alo/6, F(1, 3)+ahi/6)
    assert asymmetric_terminal[1] < F(1, 2)
    # Time-unit covariance: same exact cap*T and uniformized kernel.
    source, _ = population()
    s = F(7, 3)
    scaled, _ = population(p=10*s, q=s, cap=176*s, duration=T/s)
    assert source == scaled
    fixed_base = dual_witness(source)[0]*4/B
    fixed_scaled = dual_witness(scaled)[0]*4/(B/s)
    assert fixed_scaled == s*fixed_base
    # Global clock changes preserve the true stationary pi for driven Q.
    Q = generator(gate=F(1))
    assert mvrow([F(1, 3)]*3, repair([[7*Q[i][j] if i != j else F(0) for j in range(3)] for i in range(3)])) == [0]*3
    passive, _ = population(gate=F(1), cap=F(11))
    ratio = ((passive[3][0]-F(1, 9))/F(2, 9), (passive[3][1]-F(1, 9))/F(2, 9))
    assert 0 < ratio[0] <= ratio[1] < 1
    kappa = (-logs(ratio[1])[1]/T, -logs(ratio[0])[0]/T)
    # Boundary-count CP cases, including all outcomes in one cell. The
    # verifier must return a valid nonempty set instead of inventing a floor.
    boundary = []
    for counts in ([0, 0, 0, 32], [8, 8, 8, 8], [16, 0, 0, 16]):
        box, calls = cp_box(counts, F(1, 40))
        assert sum(a for a, b in box) <= 1 <= sum(b for a, b in box)
        assert dual_witness(box)[0] <= 0
        boundary.append({'counts': counts, 'nonempty_box': True, 'fixed_witness_positive': False})
    small_tails = finite_tail_controls()
    result = {'status': 'PULSE_THEOREM_ADVERSARIAL_AND_ARITHMETIC_CONTROLS_PASSED',
        'nonuniform_stationary_reference_models': references,
        'linear_program_independent_vertex_checks': LP_cases,
        'direct_binomial_tail_checks': small_tails,
        'boundary_count_controls': boundary,
        'nonstationary_preparation_counterexample': {'baseline_sigma': '0',
            'initial_mean': '1', 'symmetric_gate': '2', 'T': '1/2',
            'terminal_mean_preview': [float(x) for x in nonstationary_terminal],
            'positive_response_with_zero_sigma': True, 'excluded_by_contract': 'stationary preparation'},
        'asymmetric_source_clock_counterexample': {'baseline_sigma': '0', 'initial_mean': '1/2',
            'pulsed_out_rates': ['2', '1'], 'T': '1/2',
            'terminal_mean_preview': [float(x) for x in asymmetric_terminal],
            'positive_response_with_zero_sigma': True, 'excluded_by_contract': 'symmetric microscopic multipliers'},
        'global_clock_on_driven_source': 'zero mean response exactly',
        'physical_time_rescaling': {'rate_multiplier': str(s), 'duration_multiplier': str(1/s),
            'same_population_pair_enclosure_exact': True, 'bound_scales_as_rate_exact': True},
        'passive_single_pair_equilibrium_incumbent': {'reversible_two_state_realization_exists': True,
            'visible_stationary_open_probability': '1/3', 'total_escape_sum_enclosure': list(map(str, kappa)),
            'scope': 'matches this one passive horizon pair, not the entire dwell law'},
        'new_random_draws': 0, 'physical_experiments': 0,
        'code_SHA256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'CPU_wall_seconds': time.perf_counter()-start,
        'independent_audit': 'NOT_PERFORMED; solo internal exact controls'}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT/'controls.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({'status': result['status'], 'LP_checks': LP_cases, 'tail_checks': small_tails,
        'seconds': result['CPU_wall_seconds'], 'new_random_draws': 0}, indent=2))


if __name__ == '__main__':
    main()
