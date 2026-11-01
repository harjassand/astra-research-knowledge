#!/usr/bin/env python3
"""Read-only exact-byte, complete dependency, terminal audit and safety checks."""
import hashlib,json,re
from pathlib import Path,PurePosixPath
ROOT=Path(__file__).resolve().parent;S=ROOT/'sources'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def safe(name):
 p=PurePosixPath(name)
 return not p.is_absolute()and'..'not in p.parts and'\\'not in name and not set(p.parts)&{'.git','.ssh','.aws','.codex','__pycache__'}
def check(p,item):
 assert p.is_file()and not p.is_symlink(),str(p)
 if isinstance(item,str):item={'sha256':item}
 assert sha(p)==item['sha256'],str(p)
 if 'bytes'in item:assert p.stat().st_size==item['bytes'],str(p)
def payloads(p,rows):
 rows=rows.items()if isinstance(rows,dict)else((r['path'],r)for r in rows)
 count=0
 for name,row in rows:
  assert safe(name),name;check(p/name,row);count+=1
 return count
allow=json.loads((ROOT/'SOURCE_ALLOWLIST.json').read_text());names=set()
for row in allow['files']:
 name=row['archive_path'];assert safe(name);check(ROOT/name,row);names.add(name)
assert names=={p.relative_to(ROOT).as_posix()for p in S.rglob('*')if p.is_file()}
manifest_counts={}
for p in S.rglob('*.json'):
 name=p.name;j=json.loads(p.read_text())
 if name in {'FINAL_AUDIT_MANIFEST.json','ARTIFACT_ALLOWLIST.json','FINAL_MANIFEST.json'}:
  manifest_counts[p.relative_to(S).as_posix()]=payloads(p.parent,j['files'])
  if name=='FINAL_AUDIT_MANIFEST.json':assert set(x.name for x in p.parent.iterdir()if x.is_file())=={r['path']for r in j['files']}|{name}
 elif name=='AUDIT_SHA256.json':
  if p.parent.name=='dependencies':
   # Historical manifest snapshot: its full gate lives at the canonical sibling.
   candidates=[q for q in S.rglob('AUDIT_SHA256.json')if q!=p and q.parent.name!='dependencies'and sha(q)==sha(p)]
   assert candidates;continue
  key='audit_payloads'if'audit_payloads'in j else'files';manifest_counts[p.relative_to(S).as_posix()]=payloads(p.parent,j[key])
  for n,row in j.get('original_source_bindings',{}).items():check(p.parent.parent/n,row)
  for n,row in j.get('dependency_bindings',{}).items():
   target=(p.parent.parent/n).resolve();assert target.is_relative_to(S.resolve());check(target,row)
 elif name in {'AUTHOR_FREEZE.json','FREEZE.json'} and 'files'in j:payloads(p.parent,j['files'])
 elif name=='REVIEW_RECEIPT.json':
  if'payloads'in j:payloads(p.parent,j['payloads'])
  if'sha256'in j:payloads(p.parent,j['sha256'])
  if'dependencies'in j:
   for row in j['dependencies'].values():check(S/row['path'],row)
  if'target'in j:check((p.parent/j['target']).resolve(),j['target_sha256'])
 elif name=='AUTHOR_COMPONENT_FREEZE.json'and'sha256'in j:payloads(p.parent,j['sha256'])
 elif name=='MATHEMATICAL_ACCEPTANCE_BINDING.json':payloads(p.parent,j['files'])
 elif name=='FINAL_RECEIPT_BINDING.json':
  for row in j['bindings'].values():check(S/row['path'],row)
# Terminal whole-audit execution gate; historical RUNNING field is not reinterpreted.
g=S/'quadratic_debt_global_audit_20261101_dp9w20ix';f=json.loads((g/'FINAL_BINDINGS.json').read_text())
assert f['status']=='WHOLE_MATHEMATICAL_PASS_FIXED_RATE2_GLOBAL_FOSTER_AND_ONE_STATIONARY_MOMENT'
assert f['global_replay']=='PASS_BYTE_IDENTICAL_FRESH_REPLAY'and f['structural_replay']=='PASS_BYTE_IDENTICAL_STRUCTURAL_REPLAY'
payloads(g,f['sources_and_receipts']);check(g/'GLOBAL_FOSTER_FINITE_HEAD_AUTHOR.md',f['source_sha256'])
r=json.loads((g/'REPLAY_RECEIPT.json').read_text());assert r['status']=='PASS_BYTE_IDENTICAL_FRESH_REPLAY';check(g/'INDEPENDENT_GLOBAL_CHECKS.json',r['result_sha256'])
assert json.loads((g/'STRUCTURAL_REPLAY_RECEIPT.json').read_text())['status'].startswith('PASS')
# All-start consumer is now received at the new exact composition receipt.
c=S/'return_path_construction_20261101/rate2_uniform_removal_composition';cr=json.loads((c/'independent_review_20261101_0454/REVIEW_RECEIPT.json').read_text())
assert not cr['open_blockers'];check(c/'UNIFORM_ACTUAL_REMOVAL_BLOCK.md',cr['target_sha256'])
# New navigation aliases are explicitly derivative indexes, not old reviewer bytes.
for row in json.loads((ROOT/'HASH_ALIASES.json').read_text())['aliases'].values():check(ROOT/row['path'],row)
for row in json.loads((ROOT/'PACKAGE_RECEIPTS.json').read_text())['components']:
 check(ROOT/row['source'],row['source_sha256']);check(ROOT/row['receipt'],row['receipt_sha256'])
forbidden=[b'/home/'+b'agent/.codex/sessions',b'BEGIN '+b'PRIVATE KEY',b'BEGIN '+b'RSA PRIVATE KEY',b'"room_'+b'id"',b'"room'+b'Id"',b'"thread_'+b'id"',b'"thread'+b'Id"']
hits=[];scientific=[]
for p in ROOT.rglob('*'):
 if not p.is_file():continue
 rel=p.relative_to(ROOT).as_posix();assert safe(rel),rel;data=p.read_bytes()
 if any(t in data for t in forbidden):hits.append(rel)
 if re.search(rb'/(?:workspace|tmp)/[A-Za-z0-9_./-]+',data):scientific.append(rel)
assert not hits,hits
if(ROOT/'MANIFEST.json').exists():
 p=ROOT/'MANIFEST.json';j=json.loads(p.read_text());payloads(ROOT,j['files'])
 assert {r['path']for r in j['files']}=={x.relative_to(ROOT).as_posix()for x in ROOT.rglob('*')if x.is_file()and x!=p}
print(json.dumps({'status':'PASS_COMPLETE_RESTRICTED_RATE2_STABILITY_BINDINGS','source_files':len(names),'historical_manifest_payload_counts':manifest_counts,'terminal_whole_audit_and_replays_observed':True,'all_start_composition_and_dependencies_received':True,'private_restricted_pattern_hits':hits,'scientific_provenance_path_files':scientific,'complete_package_manifest_verified':(ROOT/'MANIFEST.json').exists()},indent=2))
