"""Aggregate measured results; no new source calls."""
import json,math,hashlib,statistics
from pathlib import Path
root=Path(__file__).resolve().parent
old=json.loads((root/'runs/aggregate_summary.json').read_text())
new=json.loads((root/'runs_independent_comparator/aggregate_summary.json').read_text())
primary=[r for r in old if r['run'].startswith('bandit')]+new
aggregates=[]
for algorithm in ('bandit','ordinary'):
    for n in (128,512):
        runs=[r for r in primary if r['run'].startswith(f'{algorithm}_N{n}_')]
        aggregate={'algorithm':algorithm,'N':n,'seed_count':len(runs),'runs':[r['run'] for r in runs]}
        keys=set.intersection(*(set(r.keys()) for r in runs))
        for key in sorted(keys):
            values=[r[key] for r in runs]
            if isinstance(values[0],(int,float)):
                outputkey='prequential_decoder_conditional_bell_loss' if key=='played_policy_mean_bell_loss' else key
                aggregate[outputkey]={'mean':statistics.mean(values),'min':min(values),'max':max(values)}
        aggregate['scored_decoder_semantics']='Actually applied sampled probe decoder, also the private-terminal candidate' if algorithm=='bandit' else 'Pre-call available hypothetical private-terminal decoder; NOT applied to calibration output'
        aggregates.append(aggregate)
delta=.25/(64*64*12*12)
precision=[]
for n in (128,512,8388608):
    m=n+4
    precision.append({'N':n,'mu_power_of_two_exponent':-m,
        'fixed_coordinate_grid_min_binary_fraction_bits':math.ceil(-math.log2(delta)+2*m+math.log2(128*4*12)),
        'weak_solve_objective_tolerance_min_binary_fraction_bits':math.ceil(-2*math.log2(delta)+4*m+math.log2(4096*4))})
ledger={'original_paired_seed_runs':sum(r['actual_source_calls'] for r in old),
        'additional_independently_seeded_comparator_runs':sum(r['actual_source_calls'] for r in new),
        'total_actual_simulated_source_calls':sum(r['actual_source_calls'] for r in old+new),
        'total_trajectories':len(old+new),
        'primary_independently_seeded_longest_trajectories':8,
        'primary_independent_seed_families_per_algorithm':4,
        'primary_short_prefix_reruns':8,'additional_exploratory_shared_seed_runs':8,
        'acquisition_failure_count':sum(r['failure_count'] for r in old+new),
        'new_source_calls_in_replay_scoring_tests':0,
        'all_probe_process_only':True,'terminal_payload_calls':0,
        'note':'Within an algorithm, N128 and N512 reuse the same four seeds, so their 128-call prefixes coincide. They are not eight independent seed families. Original algorithms also shared RNG seeds; primary comparator instead uses fresh offset seeds.'}
sources={}
for f in ('ordinary_prequential_small_loss_decoder_bandit_20261028.md','ordinary_prequential_terminal_memory_recovery_20261028.md'):
    sources[f]=hashlib.sha256((root.parent/f).read_bytes()).hexdigest()
output={'primary_aggregate':aggregates,'source_call_ledger':ledger,'theorem_worst_case_precision':precision,
        'source_hashes':sources,'comparison_scope':'Empirical average conditional Bell risks on each run\'s own actual visited conditional memory states; no counterfactual-policy or expected-occupation theorem estimate claimed.'}
(root/'ANALYSIS.json').write_text(json.dumps(output,indent=2)+'\n')
for a in aggregates:
    print(a['algorithm'],a['N'])
    for k in ('prequential_decoder_conditional_bell_loss','center_policy_mean_bell_loss','known_U_oracle_mean_bell_loss','identity_no_learning_mean_bell_loss','final_decoder_retrospective_past_occupation_loss','acquisition_wall_seconds','source_simulation_seconds','whitening_seconds','prox_seconds','decoder_matrix_compilation_seconds','decoder_svd_seconds','update_seconds','mean_conditioning_trace_distance'):
        if k in a:print(' ',k,a[k]['mean'])
print(json.dumps(ledger,indent=2));print(json.dumps(precision,indent=2))
