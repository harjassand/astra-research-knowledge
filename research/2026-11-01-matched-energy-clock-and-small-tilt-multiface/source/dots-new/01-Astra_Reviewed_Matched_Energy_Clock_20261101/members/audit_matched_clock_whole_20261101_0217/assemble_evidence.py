from pathlib import Path
from fractions import Fraction as F
import json,hashlib,shutil
A=Path(__file__).resolve().parent;W=A.parent;S=W/'matched_energy_clock_constructor_20261101';R=A/'replay'/S.name
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def out(name,x):
 p=A/name
 if p.exists():raise RuntimeError('no overwrite '+str(p))
 p.write_text(json.dumps(x,indent=2)+'\n')
bindings=read(A/'INITIAL_SOURCE_BINDINGS.json');assert len(bindings)==100
for z in bindings:
 p=W/z['path'];assert p.stat().st_size==z['bytes'] and h(p)==z['sha256'],str(p)
 q=A/'frozen_snapshot'/z['path'];q.parent.mkdir(parents=True,exist_ok=True);assert not q.exists();shutil.copyfile(p,q)
manifest=S/'FROZEN_SHA256.json';assert len(manifest.read_bytes())==18256 and h(manifest)=='b8179929c53e2eaa0f22809137efdd02da0fc7372f8efab9ae3527122349fed3'
shutil.copyfile(manifest,A/'frozen_snapshot'/S.name/manifest.name)
out('FINAL_SOURCE_BINDINGS.json',bindings)
P=W/'audit_matched_positive_primitive_20261101_0201';pm=read(P/'AUDIT_SHA256.json');assert h(P/'AUDIT_SHA256.json')=='c70f3d9cee39e19571f9c061ad06f008c9a60b40ad314d75ecc3d29759669280'
for name,z in pm['files'].items():
 p=P/name;assert len(p.read_bytes())==z['bytes'] and h(p)==z['sha256'];q=A/'primitive_gate'/name;q.parent.mkdir(parents=True,exist_ok=True);assert not q.exists();shutil.copyfile(p,q)
shutil.copyfile(P/'AUDIT_SHA256.json',A/'primitive_gate/AUDIT_SHA256.json')
original=read(S/'author_checks.json');fresh=read(R/'author_checks.json')
for x in [original,fresh]:
 for k in ['production_replay_seconds','total_seconds']:x.pop(k)
assert original==fresh
original_b=read(S/'boundary_checks.json');fresh_b=read(R/'boundary_checks.json')
for col in [original_b,fresh_b]:
 for z in col:z.pop('seconds')
assert original_b==fresh_b
assert (S/'same_task_comparison.json').read_bytes()==(R/'same_task_comparison.json').read_bytes()
out('REPLAY_COMPARISON.json',{'status':'PASS','all_frozen_bindings':len(bindings),'author_semantic_report_equal_excluding':['production_replay_seconds','total_seconds'],'actual_boundary_reports_equal_excluding':['seconds'],'comparator_replay_byte_identical':True,'primitive_gate_files_read_back':len(pm['files']),'primitive_audit_manifest_sha256':h(P/'AUDIT_SHA256.json'),'copied_replay_is_execution_area_not_immutable_original':True,'separate_frozen_snapshot':True})
c=read(A/'actual_full_recapture.json')
fields=['global_moment_error_upper','record_TV_error_upper','continuous_jitter_failure_unclipped_upper','continuous_jitter_failure_upper','reference_dimensionless_step','full_trial_energy_upper','reference_flip_rate','reference_mean_time','actual_physical_spacing','actual_physical_horizon','normalized_odd_basin_source_inverse_upper','normalized_odd_slab_residual_inverse_upper']
out('RESULT_AND_COST_SUMMARY.json',{'status':'PASS','rounding_notice':'Every float here is a non-certifying display; exact certificate endpoints retained unchanged in actual_full_recapture.json.','display':{k:float(F(c[k]))for k in fields},'event_display':{k:float(F(v))for k,v in c['event']['actual_probability'].items()if k in ['lower','upper']},'work':c['work'],'primal_work':c['primal_scalar_price']['work'],'inherited_work':c['inherited_source_certificate']['work'],'whole_new_independent_assertions':sum(read(A/name)['checks']for name in ['independent_whole_results.json','shifted_comparator_results.json','scaling_odd_results.json']),'primitive_independent_assertions_separate':pm['independent_exact_checks'],'author_assertions_replayed':fresh['assertions'],'author_UNKNOWN_replayed':fresh['UNKNOWN_refusals'],'whole_independent_UNKNOWN':read(A/'independent_whole_results.json')['UNKNOWN_refusals'],'additional_exploratory_UNKNOWN':read(A/'nonunit_odd_alpha_case.json')['status']=='UNKNOWN','single_full_successful_producer_calls':read(A/'actual_full_capture_count.json')['full_actual_successful_producer_calls']})
print('PASS 100 frozen sources, 66 primitive payload bindings, author/boundary semantics and byte-identical comparator; immutable snapshots assembled.')
