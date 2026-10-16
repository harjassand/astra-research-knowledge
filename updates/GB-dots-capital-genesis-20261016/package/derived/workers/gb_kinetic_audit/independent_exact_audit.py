#!/usr/bin/env python3
"""Independent exact audit of the supplied total-count obstruction.

No producer functions are imported. The physical graph is reconstructed from
coordinates, rows from elementary channels, and the two boundary problems are
solved by forward affine shooting rather than producer Thomas elimination.
All writes are confined to this audit directory.
"""
from collections import defaultdict
from decimal import Decimal, localcontext
from fractions import Fraction as R
from math import factorial
from pathlib import Path
import hashlib
import json
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
FROZEN = HERE / 'candidate_frozen'
FIRST, LAST, START, ALPHA = 16, 499, 400, 100
SITES = [(i // 4, i % 4) for i in range(8)]
ARCS = [(i, j) for i in range(8) for j in range(8)
        if sum(abs(a-b) for a, b in zip(SITES[i], SITES[j])) == 1]
assert len(ARCS) == 20
assert [sum(i == u for u, v in ARCS) for i in range(8)] == [2,3,3,2,2,3,3,2]


def b(n):
    return R(2676*n*(n-1) + 108102, 1000)


def d(n):
    return R(40*n*(n-1)*(n-2) + 37881*n, 1000)


def configuration(s):
    if s < 122:
        return (16,) + tuple(min(15, max(0, s-16-15*j)) for j in range(7))
    return tuple(min(100, max(0, s-100*j)) for j in range(8))


def physical_channels(x):
    for i in range(8):
        yp = tuple(n + (j == i) for j, n in enumerate(x))
        yield yp, b(x[i]), 'birth'
        if x[i] > 0:
            ym = tuple(n - (j == i) for j, n in enumerate(x))
            yield ym, d(x[i]), 'death'
    for i, j in ARCS:
        if x[i] > 0:
            y = tuple(n - (k == i) + (k == j) for k, n in enumerate(x))
            yield y, R(82207*x[i], 10000), 'diffusion'


def row(s):
    x = configuration(s)
    assert len(x) == 8 and all(0 <= n <= 100 for n in x)
    assert sum(x) == s and max(x) > 15
    # Directly form Q acting on symbolic values U_S, target=1, overflow=0.
    coeff = defaultdict(R)
    event_counts = defaultdict(int)
    target_channels = defaultdict(int)
    overflow = 0
    max_successor = 0
    for y, rate, kind in physical_channels(x):
        assert rate > 0
        event_counts[kind] += 1
        max_successor = max(max_successor, max(y))
        coeff[('U', s)] -= rate
        if max(y) > 162:
            overflow += 1
        elif max(y) <= 15:
            coeff[('target', 1)] += rate
            target_channels[kind] += 1
        else:
            coeff[('U', sum(y))] += rate
    assert overflow == 0 and max_successor <= 101
    up = sum((b(n) for n in x), R(0))
    all_death = sum((d(n) for n in x), R(0))
    if s < 122:
        # Physical site 0 has precisely neighbours 1 and 4.
        success = d(16) + R(82207*16, 10000)*((x[1] < 15)+(x[4] < 15))
        down = all_death - d(16)
    else:
        down, success = all_death, R(0)
    expected = {('U', s): -(up+down+success), ('U', s+1): up}
    if down:
        expected[('U', s-1)] = down
    if success:
        expected[('target', 1)] = success
    assert {k: v for k, v in coeff.items() if v} == expected
    assert up > 0 and down >= 0 and success >= 0
    assert (down == 0) == (s == FIRST)
    assert (success > 0) == (s <= 121)
    return (up, down, success), {
        'total': s, 'configuration': list(x), 'up': str(up),
        'down': str(down), 'success': str(success),
        'elementary_channels': dict(event_counts),
        'target_channels': dict(target_channels), 'overflow_channels': overflow,
        'largest_successor_coordinate': max_successor,
    }


def shoot(rows, alpha, success_value, failure_value):
    # Write v_s=A_s*z+C_s, with z=v_16. The left down rate is zero.
    a_prev, c_prev = R(0), R(0)
    a_cur, c_cur = R(1), R(0)
    aa, cc = [a_cur], [c_cur]
    for up, down, success in rows:
        diagonal = up + down + success - alpha
        a_next = (diagonal*a_cur - down*a_prev)/up
        c_next = (diagonal*c_cur - down*c_prev - success*success_value)/up
        aa.append(a_next); cc.append(c_next)
        a_prev, a_cur = a_cur, a_next
        c_prev, c_cur = c_cur, c_next
    assert aa[-1] != 0
    z = (failure_value - cc[-1])/aa[-1]
    values = [a*z+c for a, c in zip(aa[:-1], cc[:-1])]
    assert aa[-1]*z+cc[-1] == failure_value
    pivots = [rows[i][0]*aa[i+1]/aa[i] for i in range(len(rows))]
    assert all(p > 0 for p in pivots)
    # Independent full residual replay, with both absorbing values explicit.
    residuals = []
    for i, (up, down, success) in enumerate(rows):
        lhs = (up+down+success-alpha)*values[i]
        if i:
            lhs -= down*values[i-1]
        if i+1 < len(rows):
            lhs -= up*values[i+1]
        rhs = success*success_value + (up*failure_value if i == len(rows)-1 else 0)
        residuals.append(lhs-rhs)
    assert all(r == 0 for r in residuals)
    return values, pivots


def dec(q):
    with localcontext() as ctx:
        ctx.prec = 45
        return str(Decimal(q.numerator)/Decimal(q.denominator))


def digest(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def main():
    begin = time.perf_counter()
    built = [row(s) for s in range(FIRST, LAST+1)]
    rows = [x[0] for x in built]
    detailed_rows = [x[1] for x in built]
    failure, pivots0 = shoot(rows, R(0), R(0), R(1))
    clock, pivots100 = shoot(rows, R(ALPHA), R(1), R(1))
    idx = START-FIRST
    assert all(0 < x < 1 for x in failure)
    assert all(x > 1 for x in clock)
    assert failure[idx] < R(1, 10**18)
    assert clock[idx] < 100
    term = R(100**100, factorial(100))
    assert term > 10**42
    bound = R(1, 10**18) + R(1, 10**40)
    assert failure[idx] + clock[idx]/term < bound

    # Distinguish the artificial quotient from the physical total process.
    initial = (50,)*8
    initial_rates = [sum((b(n) for n in initial), R(0)),
                     sum((d(n) for n in initial), R(0))]
    chosen_rates = list(rows[idx][:2])
    assert initial_rates != chosen_rates
    same_total_target = (15, 1, 0, 0, 0, 0, 0, 0)
    same_total_cont = configuration(16)
    assert sum(same_total_target) == sum(same_total_cont) == 16
    assert max(same_total_target) <= 15 < max(same_total_cont)

    # Replay producer only in a separate owned directory; frozen inputs survive.
    replay = HERE/'producer_replay'
    replay.mkdir(exist_ok=True)
    producer_bytes = (FROZEN/'check_total_count_obstruction.py').read_bytes()
    (replay/'check_total_count_obstruction.py').write_bytes(producer_bytes)
    run = subprocess.run([sys.executable, str(replay/'check_total_count_obstruction.py')],
                         capture_output=True, text=True, check=True)
    (replay/'stdout.txt').write_text(run.stdout)
    (replay/'stderr.txt').write_text(run.stderr)
    producer = json.loads((FROZEN/'total_count_obstruction_result.json').read_bytes())
    replayed = json.loads((replay/'total_count_obstruction_result.json').read_bytes())
    for key in producer:
        if key != 'wall_seconds_descriptive':
            assert producer[key] == replayed[key], key
    assert producer['script_sha256'] == hashlib.sha256(producer_bytes).hexdigest()
    assert producer['initial_failure_probability_descriptive'] == dec(failure[idx])
    assert producer['initial_exponential_clock_certificate_descriptive'] == dec(clock[idx])

    # These full exact vectors permit direct residual replay without trusting a solver.
    witness = {
        'domain': [FIRST, LAST], 'alpha': ALPHA,
        'failure_absorbing_values': {'success': '0', 'failure': '1'},
        'clock_absorbing_values': {'success': '1', 'failure': '1'},
        'rows': detailed_rows,
        'failure_values_exact': list(map(str, failure)),
        'clock_values_exact': list(map(str, clock)),
    }
    witness_bytes = (json.dumps(witness, indent=2)+'\n').encode()
    (HERE/'EXACT_WITNESS.json').write_bytes(witness_bytes)
    initial_exact = {
        'failure_numerator': str(failure[idx].numerator),
        'failure_denominator': str(failure[idx].denominator),
        'clock_numerator': str(clock[idx].numerator),
        'clock_denominator': str(clock[idx].denominator),
    }
    (HERE/'INITIAL_EXACT_VALUES.json').write_text(json.dumps(initial_exact, indent=2)+'\n')
    out = {
        'status': 'FROZEN_INDEPENDENT_EXACT_AUDIT_PASS',
        'audited_candidate_script_sha256': hashlib.sha256(producer_bytes).hexdigest(),
        'independent_audit_script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'physical_probability_acquired': False, 'solver_advantage_established': False,
        'historical_novelty_established': False,
        'physical_directed_graph_arcs': len(ARCS),
        'physical_graph_degree_sequence': [sum(i == u for u, v in ARCS) for i in range(8)],
        'actual_generator_rows_reconstructed': len(rows),
        'actual_elementary_channels_reconstructed': sum(sum(x['elementary_channels'].values()) for x in detailed_rows),
        'actual_target_entry_rows': sum(x[2] > 0 for x in rows),
        'actual_target_diffusion_channels': sum(x['target_channels'].get('diffusion', 0) for x in detailed_rows),
        'actual_overflow_channels_in_selected_rows': 0,
        'largest_successor_coordinate': max(x['largest_successor_coordinate'] for x in detailed_rows),
        'exact_full_linear_equations_replayed': 2*len(rows),
        'independent_solver': 'forward affine shooting with separate exact residual replay',
        'all_failure_values_in_open_unit_interval': True,
        'all_clock_values_strictly_above_one': True,
        'all_independently_reconstructed_elimination_pivots_positive': True,
        'failure_initial_descriptive': dec(failure[idx]),
        'clock_initial_descriptive': dec(clock[idx]),
        'exact_failure_initial_strict_upper': '1/10^18',
        'exact_clock_initial_strict_upper': '100',
        'exact_exp100_single_term_strict_lower': '10^42',
        'finite_deadline_failure_strict_upper': '1/10^18 + 1/10^40',
        'certified_envelope_floor': '1 - 1/10^18 - 1/10^40 (strict)',
        'full_exact_witness_sha256': hashlib.sha256(witness_bytes).hexdigest(),
        'full_exact_witness_bytes': len(witness_bytes),
        'initial_exact_values_sha256': digest(initial_exact),
        'producer_replay_matches_all_nontiming_supplied_fields': True,
        'row_400_selected_configuration': list(configuration(400)),
        'physical_all_50_initial_birth_death_rates': list(map(str, initial_rates)),
        'adversarial_row_400_birth_death_rates': list(map(str, chosen_rates)),
        'target_overwrite_same_total_witness': {'target': list(same_total_target), 'continuation': list(same_total_cont)},
        'time_boundary_requirement': 'Finite, nonnegative, locally absolutely continuous on t<1; actual supercaloric inequality a.e.; target 1 and overflow 0 throughout. Signed envelopes also work with nonnegative terminal liminf by global comparison.',
        'scope': 'Every all-state total-count-only supercaloric continuation envelope for the exact capped model. Adversarial chain probability is not the physical probability.',
        'wall_seconds_descriptive': time.perf_counter()-begin,
    }
    (HERE/'INDEPENDENT_EXACT_AUDIT.json').write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps(out, indent=2))


if __name__ == '__main__':
    if hasattr(sys, 'set_int_max_str_digits'):
        sys.set_int_max_str_digits(0)
    main()
