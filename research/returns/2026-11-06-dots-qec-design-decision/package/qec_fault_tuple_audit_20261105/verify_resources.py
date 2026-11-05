"""Independently reconcile saved full-process costs and fresh equivalence."""
from pathlib import Path
import json,hashlib
root=Path(__file__).resolve().parents[1];src=root/'qec_fault_tuple_20261105';fresh=src/'fresh_preprocessing'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
manifest=json.loads((fresh/'SOURCE_COPY_MANIFEST.json').read_text())
for x in manifest['copied_sources']:
    assert sha(Path(x['original']))==x['sha256']==sha(fresh/x['copy'])
assert sha(fresh/'measure_fresh.py')==manifest['measurement_script_sha256']
records=json.loads((fresh/'COMPLETE_COST_ACCOUNTING.json').read_text());out=[]
for r in records:
    d=r['distance'];summary=json.loads((root/r['preprocessing_summary_source']).read_text())
    assert len(summary['stages'])==2
    for stage in summary['stages']:
        separate=json.loads((fresh/(stage['stage']+'_resource.json')).read_text())
        assert stage==separate and stage['exit_code']==0 and stage['budget_failure'] is None
    elapsed=sum(stage['full_subprocess_wall_seconds'] for stage in summary['stages'])
    assert elapsed==summary['sum_complete_stage_wall_seconds']==r['full_fresh_preprocessing_stage_sum_seconds']
    assert elapsed<=summary['fresh_preprocessing_joint_wall_seconds']<1200
    assert max(stage['wait4_largest_process_peak_rss_kib'] for stage in summary['stages'])==r['fresh_largest_wait4_process_peak_rss_kib']
    assert max(stage['observed_peak_process_group_rss_kib'] for stage in summary['stages'])==r['fresh_largest_sampled_process_group_peak_rss_kib']
    assert max(r['fresh_largest_wait4_process_peak_rss_kib'],r['fresh_largest_sampled_process_group_peak_rss_kib'])<2*1024*1024
    original=src/f'd{d}';copy=fresh/'qec_fault_tuple_20261105'/f'd{d}'
    a=json.loads((original/'parameters.json').read_text());b=json.loads((copy/'parameters.json').read_text())
    for name in ['U.npy','J_lo.npy','J_hi.npy','distance.npy','W.npy','starts.npy']:
        assert sha(original/name)==sha(copy/name)==a['sha256'][name]
    for field in ['Z_exact','conversion_TV_upper_exact','N','D','Q','qden','q_numerators','dl','dr','dlmax','certificate']:
        assert a[field]==b[field]
    assert sha(original/'input_graph.json')==sha(copy/'input_graph.json')==a['source_sha256']
    acquisition=root/r['acquisition_source'];assert sha(acquisition)==r['acquisition_source_sha256']
    ar=json.loads(acquisition.read_text())
    acq=ar['stages'][0]['wall_seconds'] if d==13 else ar['full_process_seconds'] if 'full_process_seconds' in ar else ar['wall_seconds']
    assert acq==r['full_acquisition_seconds']
    production=json.loads((root/r['production_resource_source']).read_text())
    assert production['full_subprocess_wall_seconds']==r['prior_full_production_process_seconds']
    total=acq+elapsed+production['full_subprocess_wall_seconds']
    assert total==r['sum_separately_measured_complete_stage_seconds']
    out.append({'distance':d,'all_six_fresh_arrays_and_exact_parameters_match':True,
                'acquisition_seconds':acq,'fresh_preprocessing_stage_seconds':elapsed,
                'full_production_process_seconds':production['full_subprocess_wall_seconds'],
                'separately_measured_stage_sum_seconds':total,
                'largest_preprocessing_process_RSS_KiB':r['fresh_largest_wait4_process_peak_rss_kib'],
                'largest_sampled_preprocessing_group_RSS_KiB':r['fresh_largest_sampled_process_group_peak_rss_kib'],
                'not_an_uninterrupted_benchmark':True})
result={'status':'PASS: fresh byte identity and complete separate-stage accounting','records':out,
        'excluded':'Research, source/file-copy preparation, testing, hash/equivalence checks and independent audit are not included in operational timings. Shared-host timings do not establish optimized-competitor speed.'}
Path(__file__).with_name('resource_results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
