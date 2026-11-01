from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parent
binding=json.loads((ROOT/'INPUT_BINDING.json').read_text());source=Path(binding['source'])
for name,meta in binding['verified_files'].items():
 b=(source/name).read_bytes();assert len(b)==meta['bytes']and hashlib.sha256(b).hexdigest()==meta['sha256'],name
stage=json.loads((ROOT/'STAGED_REPLAY.json').read_text());assert stage['status']=='PASS_RELOCATED_INDEPENDENT_REPLAY'
for name in ('INDEPENDENT_RESULTS.json','GRAPH_DOMAIN_RESULTS.json','NESTED_FRACTIONAL_RESULTS.json','COMPARATOR_RESULTS.json','RETAINED_PRIMITIVE_BINDING.json'):
 assert json.loads((ROOT/name).read_text())['status'].startswith('PASS'),name
for p in ROOT.rglob('*stderr*'):assert not p.read_bytes(),p
assert (ROOT/'supplement.stdout').read_bytes()==(source/'cutoff_supplement_results.json').read_bytes()
# Check the final staged code copies match the final current implementations.
sdir=Path(stage['staging_directory'])/'audit'
for name in ('independent_aggregate_receiver.py','exercise_independent.py','graph_domain_controls.py','nested_fractional_controls.py'):
 assert (sdir/name).read_bytes()==(ROOT/name).read_bytes(),name
for p in (ROOT/'retained_independent').rglob('*.py'):
 assert (sdir/p.relative_to(ROOT)).read_bytes()==p.read_bytes()
main=json.loads((ROOT/'INDEPENDENT_RESULTS.json').read_text())
summary=dict(status='SCOPED_MATHEMATICAL_CONSTRUCTOR_AND_INDEPENDENT_RECEIVER_PASS',source_manifest_sha256='68843ec51a0e141c3fda3f40ed0287d29ac98806b58fde9fd43701a5e3db3909',review_input_binding_sha256='fae16d2bd6a1e43479b5f860c9b7f03649cf20c554361a80032d0049e5f9c1fa',supplemental_input_binding_sha256='1bf75dee96240b0bd69cd0fecb769fc305519258eee601b417c8dd48b543c427',frozen_author_entries=82,bound_file_union=89,frozen_source_unchanged=True,substantive_defects_found=0,source_repairs=0,main_canonical_bytes=main['main_canonical_bytes'],main_canonical_sha256=main['main_canonical_sha256'],main_mass_head_K=29729394962313506647,actual_mass_head_expanded=False,actual_global_head_expanded=False,actual_stationary_bound_expanded=False,no_external_source_retrieval=True,no_one_hub_acceptance_inheritance=True,scope='All acquired isolated hub-graph satellites; arbitrary nonempty target sets, overlap, positive rates; actual residual raw core passes dominating-cover guard. Not general WR, complete grouping finder, practical tail, historical novelty or source-process-clearance verdict.')
(ROOT/'AUDIT_SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n')
files={}
for p in sorted(ROOT.rglob('*')):
 if p.is_file()and p.name!='FINAL_AUDIT_MANIFEST.json'and '__pycache__'not in p.parts:
  b=p.read_bytes();files[str(p.relative_to(ROOT))]={'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
manifest=dict(**summary,files=files)
(ROOT/'FINAL_AUDIT_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('PASS_FINAL_ARTIFACT_BINDING',len(files),'files')
print('MANIFEST_SHA256',hashlib.sha256((ROOT/'FINAL_AUDIT_MANIFEST.json').read_bytes()).hexdigest())
