#!/usr/bin/env python3
"""Exact population and prospective power, before any fresh pulse record."""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'outputs/pulse_entropy'
sys.path.insert(0, str(ROOT/'work'))
from pulse_entropy import enclose, dual_witness, logs
from ctmc_reflection_control import exp_negative_bounds

N = 32768
ALPHA = F(1, 80)
T = F(1, 40)
GATE = F(16)
B = GATE*T
CAP = F(176)  # SOURCE SIMULATION ONLY; never supplied to the receiver.


def generator(p=F(10), q=F(1), gate=GATE):
    Q = [[F(0) for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for j, rate in [((i+1)%3, p), ((i-1)%3, q)]:
            Q[i][j] = rate*(gate if (i == 0) != (j == 0) else 1)
        Q[i][i] = -sum(Q[i])
    return Q


def population(p=F(10), q=F(1), gate=GATE, cap=CAP, duration=T, order=90):
    """Directed positive uniformization; tail explicitly retained."""
    Q = generator(p, q, gate)
    assert all(-Q[i][i] <= cap for i in range(3))
    P = [[F(i == j)+Q[i][j]/cap for j in range(3)] for i in range(3)]
    assert all(min(row) >= 0 and sum(row) == 1 for row in P)
    mu = cap*duration
    elo, ehi = exp_negative_bounds(mu, 180)
    assert 0 < elo <= ehi
    current = [[F(i == j) for j in range(3)] for i in range(3)]
    total = [[F(0) for j in range(3)] for i in range(3)]
    weight = F(1)
    mass = F(0)
    for k in range(order+1):
        for i in range(3):
            for j in range(3):
                total[i][j] += weight*current[i][j]
        mass += weight
        current = [[sum((current[i][h]*P[h][j] for h in range(3)), F(0))
            for j in range(3)] for i in range(3)]
        weight *= mu/(k+1)
    tail = 1-elo*mass
    assert 0 <= tail < F(1, 2**100)
    pairs = [F(0)]*4
    for i in range(3):
        for j in range(3):
            pairs[2*int(i == 0)+int(j == 0)] += total[i][j]/3
    box = [enclose(elo*x, min(F(1), ehi*x+tail)) for x in pairs]
    return box, enclose(F(0), tail)[1]


def prepare():
    start = time.perf_counter()
    if (OUT/'PROTOCOL.json').exists():
        raise RuntimeError('frozen protocol already exists; do not overwrite or redraw')
    driven, tail = population()
    null, nulltail = population(F(11, 2), F(11, 2))
    passive, passivetail = population(gate=F(1), cap=F(11))
    assert passive[3][0] > F(1, 9) and passive[3][1] < F(1, 3)
    assert null[1][0]+null[3][0] <= F(1, 3) <= null[1][1]+null[3][1]
    # CP tails of risk 1/640 lie within empirical +/-1/100 by Hoeffding.
    # The empirical four-cell law is also within true law +/-1/100,
    # except with probability at most 8 exp(-2*n/10000) <= 1/80.
    e = F(1, 100)
    exponent = 2*N*e*e
    assert exponent > logs(8/ALPHA)[1]
    widened = [(max(F(0), lo-2*e), min(F(1), hi+2*e)) for lo, hi in driven]
    KL, witness = dual_witness(widened)
    floor = 4*KL/B
    assert floor >= F(1, 2), ('prospective power target failed', float(floor))
    filelist = [ROOT/'work'/name for name in ['pulse_entropy.py', 'pulse_entropy_source.py',
        'pulse_entropy_acquire.py', 'pulse_entropy_controls.py', 'kinetic_incumbent_control.py',
        'ctmc_reflection_control.py']]
    filelist += [ROOT/'outputs/reversible_currents/currents.py']
    assert all(path.is_file() for path in filelist)
    code = {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest() for path in filelist}
    protocol = {'status': 'FROZEN_BEFORE_FRESH_DRAWS', 'date_local': '2026-10-31',
        'purpose': 'finite stationary-mean entropy lower inference from independent two-bit pulses',
        'scope': 'synthetic exact CTMC control, not a physical acquisition',
        'N_per_source': N, 'alpha_per_record': str(ALPHA), 'paired_coverage_risk': str(2*ALPHA),
        'pulse_duration_T': str(T), 'symmetric_cut_multiplier': str(GATE),
        'amplitude_envelope_M': str(GATE), 'B': str(B),
        'decision_target_nats_per_time': '1/2',
        'two_sources': [
            {'name': 'driven', 'p': '10', 'q': '1', 'seed': 2026110116,
             'true_sigma': '9 log(10)', 'stationary_start': 'uniform 3-state'},
            {'name': 'equilibrium', 'p': '11/2', 'q': '11/2', 'seed': 2026110117,
             'true_sigma': '0', 'stationary_start': 'uniform 3-state'}],
        'source_only_uniformization_cap': str(CAP), 'source_only_Poisson_mean': str(CAP*T),
        'inference_inputs': ['endpoint cells', 'B', 'alpha', 'constant symmetric pulse contract'],
        'prospective_power': {'confidence_tail_risk': str(ALPHA/8), 'empirical_cell_tolerance': str(e),
            'CP_cell_radius_upper': str(e), 'source_population_to_box_radius': str(2*e),
            'Hoeffding_exponent': str(exponent), 'log_640_upper': str(logs(8/ALPHA)[1]),
            'source_rate_lower_on_power_event': str(floor),
            'source_rate_lower_on_power_event_preview': float(floor),
            'miss_target_risk_upper': str(ALPHA),
            'proof': '8 exp(-2*n*(1/100)^2) <= 1/80; every resulting CP box is inside population +/-1/50',
            'fixed_witness': witness},
        'code_SHA256': code, 'new_draws_at_freeze': 0,
        'no_redraw_rule': 'one record each at these seeds and budgets; retain any failure',
        'resources_supplied_not_acquired': ['independent stationary preparation', 'symmetric microscopic cut gate',
            'dimensionless gate envelope', 'physical duration clock', 'binary sensor'],
        'expected_pulse_time_per_source': str(N*T), 'readouts_per_source': 2*N,
        'independent_preparations_per_source': N,
        'all_in_physical_cost': 'UNKNOWN; preparation/reset/control/sensor cost is not acquired'}
    pop = {'status': 'EXACT_POPULATION_AND_PRE_DRAW_POWER_CERTIFIED',
        'cell_order': ['00', '01', '10', '11'],
        'driven_pair_enclosure': [[str(a), str(b)] for a, b in driven],
        'equilibrium_pair_enclosure': [[str(a), str(b)] for a, b in null],
        'passive_pair_enclosure': [[str(a), str(b)] for a, b in passive],
        'driven_previews': [float((a+b)/2) for a, b in driven],
        'equilibrium_previews': [float((a+b)/2) for a, b in null],
        'passive_covariance_positive_exact': True,
        'uniformization_tail_upper': [str(tail), str(nulltail), str(passivetail)],
        'true_source_sigma_enclosure': [str(9*x) for x in logs(F(10))],
        'true_source_sigma_preview': float(9*logs(F(10))[0]),
        'source_state_count_cap_and_rates_are_not_receiver_inputs': True,
        'exploratory_numerical_population_scan_no_draws': [
            {'m': 8, 'T': '1/40', 'marginal_rate_preview': .7213372831667083},
            {'m': 16, 'T': '1/40', 'marginal_rate_preview': 1.125631039660835},
            {'m': 20, 'T': '1/50', 'marginal_rate_preview': 1.2193719821961868}],
        'selection': 'm16 gives simple common integer cap, finite response and certified fixed witness at n32768',
        'CPU_wall_seconds': time.perf_counter()-start}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT/'population_and_power.json').write_text(json.dumps(pop, indent=2)+'\n')
    (OUT/'PROTOCOL.json').write_text(json.dumps(protocol, indent=2)+'\n')
    print(json.dumps({'status': pop['status'], 'power_event_floor': float(floor),
        'target': .5, 'N_per_source': N, 'driven_pair': pop['driven_previews'],
        'miss_target_risk_upper': str(ALPHA), 'seconds': pop['CPU_wall_seconds']}, indent=2))


if __name__ == '__main__':
    prepare()
