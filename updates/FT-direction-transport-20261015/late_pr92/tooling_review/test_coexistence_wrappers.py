#!/usr/bin/env python3
"""Software fixtures for additive exact-owned-ID coexistence adapters."""
from pathlib import Path
import ast,copy,hashlib,importlib.util,json,sys
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parent
A=Path('/Users/harjas/Documents/ChatGPT/ultra/work/astra-pr92-audit-20261015')
B=Path('/Users/harjas/Documents/ChatGPT/ultra/work/astra-capital-direction-transport-20261015')
def loadmodule(name):
 s=importlib.util.spec_from_file_location(name,H/(name+'.py'));m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m92=loadmodule('validate_pr92_coexist_v0002');m93=loadmodule('validate_pr93_coexist_v0002')
checks=[];versions={}
for role,m,r in [('92',m92,A),('93',m93,B)]:
 raw=(r/m.ORIGINAL).read_bytes();adapted=m.adapt(raw);ast.parse(adapted)
 versions[role]={'original_path':m.ORIGINAL,'original_sha256':hashlib.sha256(raw).hexdigest(),'adapted_in_memory_sha256':hashlib.sha256(adapted.encode()).hexdigest(),'wrapper_sha256':hashlib.sha256((H/(m.__name__+'.py')).read_bytes()).hexdigest()}
 assert m.BEFORE not in adapted and m.AFTER in adapted
 checks.append('PR'+role+' exact original hash and narrowly scoped adaptation compile')
 try:m.adapt(raw+b'\n')
 except ValueError:checks.append('PR'+role+' altered original fails closed')
 else:raise AssertionError('unreviewed original accepted')
notices92=json.loads((A/'updates/FT-foundational-capability-20261015/SCOPED_NOTICES.json').read_text())['notices']
notices93=json.loads((B/'updates/FT-direction-transport-20261015/SCOPED_NOTICES.json').read_text())
allnotices={x['notice_id']:copy.deepcopy(x) for x in notices92+notices93};prior=copy.deepcopy(allnotices)
def fail(msg):raise ValueError(msg)
ns={'notices':allnotices,'load':lambda _: {'notices':notices92},'UPDATE':Path('.'),'fail':fail}
exec(m92.AFTER,ns)
assert len(allnotices)==13 and len(ns['new_notices'])==5 and [x['notice_id'] for x in ns['new_notices']]==[x['notice_id'] for x in notices92]
assert allnotices==prior
checks.append('combined13 FT notices select exact5 PR92 records without altering either set')
gates92=json.loads((A/'updates/FT-foundational-capability-20261015/OPEN_GATES.json').read_text())['gates']
ids93=json.loads((B/'updates/FT-direction-transport-20261015/INTEGRATION_GENERATOR_RECEIPT.json').read_text())['gate_ids']
gates93=[json.loads(x) for x in (B/'frontier/OPEN_PROOF_GATES.jsonl').read_text().splitlines() if json.loads(x).get('gate_id') in ids93]
allgates=gates92+gates93;prior=copy.deepcopy(allgates)
ns={'receipt':{'gate_ids':ids93},'rows':lambda _r,_p:allgates,'root':Path('.')}
exec(m93.AFTER.replace('\n    ','\n'),ns)
assert len(allgates)==16 and len(ns['gates'])==6 and set(ns['gates'])==set(ids93) and allgates==prior
checks.append('combined16 FT gates select exact6 PR93 generator-owned records without altering either set')
adapted=m93.adapt((B/m93.ORIGINAL).read_bytes())
assert "BASE = 'b7cada92d2eb304578be5ed974f1e44b10a89928'" in adapted
assert "'check', '--base-revision', COEXIST_PROJECTION_BASE]" in adapted
checks.append('current projection ancestor parameter does not change scientific/source/checkpoint base')
history=m93.check_pr92_history(A);assert history['canonical_registry_prefixes_preserved']
checks.append('canonical PR92 ancestry and complete immutable/registry-history audit passes standalone')
receipt={'schema':'astra.ft-coexistence-wrapper-fixtures.v1','status':'PASS','checks':checks,'check_count':len(checks),'versions':versions,'history':history,'scope':'Software selection/hash/byte-history fixtures only. Does not claim complete merged-tree validation before root reconciliation.','worktrees_modified':False}
(H/'COEXISTENCE_WRAPPER_FIXTURE_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
