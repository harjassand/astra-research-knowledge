#!/usr/bin/env python3
"""One frozen, exact synthetic pulse record per source; never redraw."""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'outputs/pulse_entropy'
sys.path.insert(0, str(ROOT/'work'))
from pulse_entropy import evaluate
from pulse_entropy_source import generator
from ctmc_reflection_control import CountedBits, ExactPoisson


def sample(n, p, q, gate, duration, cap, seed):
    start = time.perf_counter()
    Q = generator(p, q, gate)
    P = [[F(i == j)+Q[i][j]/cap for j in range(3)] for i in range(3)]
    denominator = 352
    weights = [[int(x*denominator) for x in row] for row in P]
    assert all(F(w, denominator) == x for row, prow in zip(weights, P) for w, x in zip(row, prow))
    assert all(sum(row) == denominator and min(row) >= 0 for row in weights)
    bits = CountedBits(seed)
    poisson = ExactPoisson(cap*duration)
    record = []
    updates = jumps = 0
    for _ in range(n):
        x = bits.below(3)  # Independent uniform STATIONARY start, every trial.
        initial = int(x == 0)
        K = poisson.draw(bits)
        updates += K
        for j in range(K):
            u = bits.below(denominator)
            cumulative = 0
            for y, weight in enumerate(weights[x]):
                cumulative += weight
                if u < cumulative:
                    break
            jumps += int(y != x)
            x = y
        record.append(2*initial+int(x == 0))
    return record, {'independent_stationary_preparations': n, 'bit_readouts': 2*n,
        'model_pulse_duration_per_trial': str(duration), 'total_model_pulse_duration': str(n*duration),
        'expected_uniformization_updates': str(n*cap*duration), 'simulated_updates': updates,
        'simulated_microscopic_jumps': jumps, 'simulated_virtual_holds': updates-jumps,
        'PRNG_bits_generated': bits.bits, 'exact_Poisson_draws': poisson.draws,
        'Poisson_interval_refinements': poisson.refinements,
        'source_only_uniformization_cap': str(cap),
        'event_times': 'marginalized exactly at fixed T; not an observed jump-time record',
        'CPU_wall_seconds': time.perf_counter()-start,
        'sampler': 'rational Poisson inverse CDF, exact categorical rejection, seeded synthetic PRNG',
        'physical_preparation_reset_gate_timing_detector_cost': 'UNKNOWN; resources supplied, not acquired'}


def main():
    start = time.perf_counter()
    protocol_path = OUT/'PROTOCOL.json'
    protocol = json.loads(protocol_path.read_text())
    assert protocol['status'] == 'FROZEN_BEFORE_FRESH_DRAWS' and protocol['new_draws_at_freeze'] == 0
    for path, digest in protocol['code_SHA256'].items():
        assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest() == digest, f'frozen code changed: {path}'
    started = OUT/'ACQUISITION_STARTED.json'
    if started.exists() or any((OUT/(row['name']+'_record.json')).exists() for row in protocol['two_sources']):
        raise RuntimeError('acquisition already started; replay existing data, never redraw')
    protocol_hash = hashlib.sha256(protocol_path.read_bytes()).hexdigest()
    started.write_text(json.dumps({'status': 'STARTED_ONCE', 'protocol_SHA256': protocol_hash,
        'seeds': [row['seed'] for row in protocol['two_sources']], 'N': protocol['N_per_source'],
        'redraw_authorized': False}, indent=2)+'\n')
    acquisitions = []
    for row in protocol['two_sources']:
        record, cost = sample(protocol['N_per_source'], F(row['p']), F(row['q']),
            F(protocol['symmetric_cut_multiplier']), F(protocol['pulse_duration_T']),
            F(protocol['source_only_uniformization_cap']), row['seed'])
        path = OUT/(row['name']+'_record.json')
        path.write_text(json.dumps(record)+'\n')
        acquisitions.append({'name': row['name'], 'seed': row['seed'], 'cost': cost,
            'record': str(path.relative_to(ROOT)), 'record_SHA256': hashlib.sha256(path.read_bytes()).hexdigest()})
        print(json.dumps({'acquired': row['name'], 'trials': len(record), 'cost': cost}), flush=True)
    # Both records are persisted before any inference. No adaptation to outcomes.
    for row in acquisitions:
        path = ROOT/row['record']
        result = evaluate(json.loads(path.read_text()), F(protocol['B']), F(protocol['alpha_per_record']))
        result_path = OUT/(row['name']+'_inference.json')
        result_path.write_text(json.dumps(result, indent=2)+'\n')
        row.update(inference=str(result_path.relative_to(ROOT)), rate_lower=result['rate_lower'],
            rate_lower_preview=result['rate_lower_preview'], comparators=result['ordinary_shared_method_comparators'],
            inference_CPU_wall_seconds=result['CPU_wall_seconds'])
    source, null = acquisitions
    passed = F(source['rate_lower']) >= F(protocol['decision_target_nats_per_time']) and F(null['rate_lower']) == 0
    receipt = {'status': 'FRESH_FINITE_PULSE_CONTROLS_PASSED' if passed else 'FRESH_FINITE_PULSE_TARGET_NOT_PASSED',
        'protocol_SHA256': protocol_hash, 'records': acquisitions,
        'source_target_met': F(source['rate_lower']) >= F(protocol['decision_target_nats_per_time']),
        'equilibrium_returned_zero': F(null['rate_lower']) == 0,
        'familywise_fixed_n_coverage_risk': protocol['paired_coverage_risk'],
        'prospective_source_miss_target_risk': protocol['prospective_power']['miss_target_risk_upper'],
        'total_independent_preparations': 2*protocol['N_per_source'],
        'total_bit_readouts': 4*protocol['N_per_source'],
        'total_model_pulse_duration': str(2*protocol['N_per_source']*F(protocol['pulse_duration_T'])),
        'total_simulated_updates': sum(x['cost']['simulated_updates'] for x in acquisitions),
        'total_simulated_microscopic_jumps': sum(x['cost']['simulated_microscopic_jumps'] for x in acquisitions),
        'total_PRNG_bits': sum(x['cost']['PRNG_bits_generated'] for x in acquisitions),
        'physical_experiments': 0, 'redraws': 0,
        'novelty_physical_validation_practical_advantage_and_mission': 'NOT_ESTABLISHED',
        'CPU_wall_seconds': time.perf_counter()-start}
    (OUT/'receipt.json').write_text(json.dumps(receipt, indent=2)+'\n')
    print(json.dumps({k: v for k, v in receipt.items() if k != 'records'} |
        {'bounds': [{'name': row['name'], 'lower': row['rate_lower_preview'],
            'ordinary_marginal_KL': float(F(row['comparators']['ordinary_marginal_KL_rate_lower'])),
            'ordinary_paired_Pinsker': float(F(row['comparators']['ordinary_paired_Pinsker_rate_lower']))}
            for row in acquisitions]}, indent=2))


if __name__ == '__main__':
    main()
