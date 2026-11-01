#!/usr/bin/env python3
"""Read-only frozen-source verification. Does not execute a scalar constructor."""
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
counts={}
for name in ['PACKAGE_MANIFEST.json','SOURCE_ALLOWLIST.json']:
 obj=json.loads((ROOT/name).read_text())
 for row in obj['files']:
  p=ROOT/row['path'];assert p.is_file(),row['path'];assert sha(p)==row['sha256'],row['path']
  assert p.stat().st_size==row['bytes'],row['path']
 counts[name]=len(obj['files'])
base=ROOT/'boundary_clearance_kernel_root_20261101'
src=base/'coarse_cold_algorithm_20261101';audit=base/'audit_coarse_cold_20261101'
assert sha(audit/'REVIEW_RECEIPT.json')=='46fc3785bb137f81af5b8574a5fbaef14934573e65e8f627228ee83e33469b15'
assert json.loads((audit/'REVIEW_RECEIPT.json').read_text())['status']=='PASS_SOURCE_BOUND_PROSPECTIVE_COARSE_COLD_ALGORITHM_AND_TWO_FIXTURE_JOIN'
assert sha(src/'AUTHOR_FREEZE.json')=='a6e1638f31b6d8055c2e158e4bdbabc0256b2a6c43cf49ea564ce4c1c69b4114'
f=json.loads((src/'AUTHOR_FREEZE.json').read_text())
for rel,row in f['files'].items():assert sha(src/rel)==row['sha256']
for rel,row in f['old_files_preserved'].items():assert sha(ROOT/rel)==row['sha256']
m=json.loads((src/'COLD_SOURCE_BINDINGS.json').read_text())
for row in m['files']:assert sha(ROOT/row['path'])==row['sha256']
assert len(m['files'])==36
print(json.dumps({'status':'PASS_FROZEN_COARSE_COLD_PACKAGE','counts':counts,'runtime_source_files':36,'fresh_scalar_solves':0,'note':'Run run_cold.py for the complete fresh prospective construction.'},indent=2))
