"""Combine already measured stages; this script launches no computations."""
import hashlib
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
FROZEN=HERE.parent
BASE=FROZEN.parent
acq13_path=BASE/'qec_score_resolvent_20261105/fresh_setup_benchmark.json'
acq21_path=BASE/'qec_score_d21_20261105/acquisition_replay_resource.json'
a13=json.loads(acq13_path.read_text())
a21=json.loads(acq21_path.read_text())
acq13=next(s['wall_seconds'] for s in a13['stages'] if s['name']=='circuit_acquisition')
records=[]
for d,n,acq,source in [(13,20000,acq13,acq13_path),(21,10000,a21['wall_seconds'],acq21_path)]:
    fresh=json.loads((HERE/f'd{d}_preprocessing_summary.json').read_text())
    prod_path=FROZEN/f'production_d{d}_{n}_process_resources.json'
    prod=json.loads(prod_path.read_text())
    equivalent=json.loads((HERE/f'd{d}_equivalence.json').read_text())
    assert equivalent['all_equivalent'] and prod['exit_code']==0 and prod['kill_reason'] is None
    record={
        'distance':d,
        'scope':'Sum of separately measured full subprocess stages from different runs, NOT one uninterrupted acquisition-to-production benchmark. No additional statistical sampling.',
        'full_acquisition_seconds':acq,
        'full_floating_preprocessing_seconds':fresh['stages'][0]['full_subprocess_wall_seconds'],
        'full_exact_producer_seconds':fresh['stages'][1]['full_subprocess_wall_seconds'],
        'full_fresh_preprocessing_stage_sum_seconds':fresh['sum_complete_stage_wall_seconds'],
        'joint_fresh_preprocessing_wall_seconds':fresh['fresh_preprocessing_joint_wall_seconds'],
        'prior_full_production_process_seconds':prod['full_subprocess_wall_seconds'],
        'sum_separately_measured_complete_stage_seconds':acq+fresh['sum_complete_stage_wall_seconds']+prod['full_subprocess_wall_seconds'],
        'sum_using_joint_preprocessing_wall_seconds':acq+fresh['fresh_preprocessing_joint_wall_seconds']+prod['full_subprocess_wall_seconds'],
        'fresh_largest_wait4_process_peak_rss_kib':fresh['largest_wait4_process_peak_rss_kib'],
        'fresh_largest_sampled_process_group_peak_rss_kib':fresh['largest_observed_process_group_rss_kib'],
        'prior_production_wait4_peak_rss_kib':prod['full_subprocess_peak_rss_kib'],
        'all_six_arrays_byte_identical':True,
        'exact_Z_TV_and_certificate_equal':True,
        'acquisition_source':str(source.relative_to(BASE)),
        'acquisition_source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
        'production_resource_source':str(prod_path.relative_to(BASE)),
        'preprocessing_summary_source':str((HERE/f'd{d}_preprocessing_summary.json').relative_to(BASE)),
        'excluded_work':'File-copy setup, pre/post hash checks, equivalence comparisons, independent scientific review and test-development work are outside these operational stage times. Compiler time and stage input/output are included.',
    }
    if d==13:
        record['acquisition_memory_caveat']='Earlier137492KiB peak_child_rss is across the complete earlier fresh path-cover setup pipeline, not acquisition alone. No acquisition-only peak is claimed.'
        record['earlier_setup_pipeline_peak_child_rss_kib']=a13['peak_child_rss_kib']
    else:
        record['acquisition_wait4_peak_child_rss_kib']=a21['peak_child_rss_kib']
        record['acquisition_sampled_tree_rss_kib']=a21['observed_peak_tree_rss_kib']
    records.append(record)
(HERE/'COMPLETE_COST_ACCOUNTING.json').write_text(json.dumps(records,indent=2)+'\n')
print(json.dumps(records,indent=2))
