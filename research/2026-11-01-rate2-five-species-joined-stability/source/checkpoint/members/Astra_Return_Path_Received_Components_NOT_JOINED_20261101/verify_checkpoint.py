#!/usr/bin/env python3
"""Read-only integrity, dependency and safety checks for this checkpoint."""
import hashlib,json,re
from pathlib import Path,PurePosixPath
ROOT=Path(__file__).resolve().parent
S=ROOT/'sources'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def safe_path(name):
 p=PurePosixPath(name)
 return not p.is_absolute() and '..' not in p.parts and '\\' not in name and all(t not in {'.git','.ssh','.aws','.codex','__pycache__'} for t in p.parts)
def verify_manifest(path,key='files'):
 data=json.loads(path.read_text());rows=data[key]
 if isinstance(rows,dict):rows=[{'path':k,**(v if isinstance(v,dict)else {'sha256':v})}for k,v in rows.items()]
 for row in rows:
  name=row['path'];assert safe_path(name),name
  p=path.parent/name;assert p.is_file() and not p.is_symlink(),name
  assert sha(p)==row['sha256'],name
  if 'bytes'in row:assert p.stat().st_size==row['bytes'],name
 return len(rows)
allow=json.loads((ROOT/'SOURCE_ALLOWLIST.json').read_text())['files']
expected=set()
for row in allow:
 name=row['archive_path'];assert safe_path(name),name
 p=ROOT/name;assert p.is_file() and not p.is_symlink(),name
 assert sha(p)==row['sha256'] and p.stat().st_size==row['bytes'],name
 expected.add(name)
actual={p.relative_to(ROOT).as_posix()for p in S.rglob('*')if p.is_file()}
assert actual==expected,{'extra':sorted(actual-expected),'missing':sorted(expected-actual)}
manifest_counts={}
for name in [
 'activation_debt_stopped_audit_20261101_sc57xnn6/FINAL_AUDIT_MANIFEST.json',
 'activation_debt_stopped_audit_20261101_sc57xnn6/ARTIFACT_ALLOWLIST.json',
 'return_path_construction_20261101/rate2_dyadic_continuation/audit_stage_20261101_0422/AUDIT_SHA256.json',
 'return_path_construction_20261101/rate2_dyadic_continuation/AUTHOR_STAGE_FREEZE.json',
 'return_path_construction_20261101/rate2_dyadic_continuation/receiving_conventions_20261101/FREEZE.json',
 'sampled_return_consumer_audit_20261101_ta90776j/FINAL_MANIFEST.json',
]:manifest_counts[name]=verify_manifest(S/name)
growth=S/'return_path_construction_20261101/rate2_uniform_initial_growth'
ga=growth/'audit_uniform_growth_20261101_0435/AUDIT_SHA256.json'
manifest_counts[str(ga.relative_to(S))]=verify_manifest(ga,'audit_payloads')
for name,row in json.loads(ga.read_text())['original_source_bindings'].items():
 assert sha(growth/name)==row['sha256'] and (growth/name).stat().st_size==row['bytes']
interior=S/'return_path_construction_20261101/rate2_paid_interior_removal'
ir=S/'return_path_construction_20261101/rate2_paid_interior_removal_independent_review_20261101/REVIEW_RECEIPT.json'
j=json.loads(ir.read_text());assert j['target_sha256']==sha(interior/'PAID_INTERIOR_REMOVAL.md')
for name,h in j['sha256'].items():assert sha(ir.parent/name)==h
for name,h in json.loads((interior/'AUTHOR_COMPONENT_FREEZE.json').read_text())['sha256'].items():assert sha(interior/name)==h
r2=S/'return_path_construction_20261101/rate2_fixed_horizon_obstruction'
r2r=S/'return_path_construction_20261101/rate2_fixed_horizon_obstruction_independent_review_20261101/REVIEW_RECEIPT.json'
j=json.loads(r2r.read_text());assert j['target_sha256']==sha(r2/'RATE2_FIXED_HORIZON_ADDENDUM.md')
for name,h in j['sha256'].items():assert sha(r2r.parent/name)==h
consumer=S/'sampled_return_consumer_root_20261101/PAID_ACTIVATION_TO_STATIONARY_MOMENT.md'
for name in ['FINAL_BINDINGS.json','PORTABLE_FINAL_BINDINGS.json']:
 j=json.loads((S/'sampled_return_consumer_audit_20261101_ta90776j'/name).read_text());assert j['source_sha256']==sha(consumer) and not j['rate2_uniform_block_hypothesis_verified']
assert sha(S/'neutral_return_obstruction_root_20261101/STABLE_PATH_NETWORK_BOUNDED_PROFILE_OBSTRUCTION.md')=='0f6a4405e9566b070100322606f004ea1f58dda08fd7ea46d03cec1da8d3e478'
# Restricted/private material patterns; scientific source-path provenance is allowed.
forbidden=[b'/home/'+b'agent/.codex/sessions',b'BEGIN '+b'PRIVATE KEY',b'BEGIN '+b'RSA PRIVATE KEY',b'"room_'+b'id"',b'"room'+b'Id"',b'"thread_'+b'id"',b'"thread'+b'Id"']
private_hits=[];scientific_path_files=[]
for p in ROOT.rglob('*'):
 if not p.is_file():continue
 name=p.relative_to(ROOT).as_posix();assert safe_path(name),name
 data=p.read_bytes()
 if any(t in data for t in forbidden):private_hits.append(name)
 if re.search(rb'/(?:workspace|tmp)/[A-Za-z0-9_./-]+',data):scientific_path_files.append(name)
assert not private_hits,private_hits
full=ROOT/'MANIFEST.json'
if full.exists():
 rows=json.loads(full.read_text())['files'];listed={r['path']for r in rows}
 actual_all={p.relative_to(ROOT).as_posix()for p in ROOT.rglob('*')if p.is_file()and p!=full}
 assert actual_all==listed,{'unlisted':sorted(actual_all-listed),'missing':sorted(listed-actual_all)}
 verify_manifest(full)
report={'status':'PASS_SOURCE_BINDINGS_MANIFESTS_AND_SAFETY','source_file_count':len(allow),'historical_manifest_payload_counts':manifest_counts,'cross_component_source_bindings_verified':True,'private_restricted_pattern_hits':private_hits,'scientific_source_path_provenance_files':scientific_path_files,'no_joined_network_theorem':True,'complete_package_manifest_verified':full.exists()}
print(json.dumps(report,indent=2))
