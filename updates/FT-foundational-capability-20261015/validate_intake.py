#!/usr/bin/env python3
"""Scoped structural/hash validator for the FT intake; no scientific inference."""
from __future__ import annotations
import hashlib, json, pathlib, sys
ROOT=pathlib.Path(__file__).resolve().parents[2]
UPDATE=ROOT/'updates/FT-foundational-capability-20261015'
PACKAGE=UPDATE/'package'
EXPECTED_SOURCE_MANIFEST='1b953dbf369b7daec492037ab07086a52b881f3d27fd4caca75e28624fb4262b'
CARD_IDS=[
'N843-finite-horizon-irrational-phase-state-complexity',
'N844-finite-abelian-subgroup-sampler-and-implementation-boundaries',
'N845-event-conditioned-isotope-renewal-with-unclosed-physical-gates',
'N846-optical-loss-attribution-and-saturable-bucket-boundary',
'N847-dual-rail-erasure-monitor-prior-art-boundary']
def fail(msg): raise SystemExit('FAIL: '+msg)
def sha(b): return hashlib.sha256(b).hexdigest()
def load(p): return json.loads(p.read_text(encoding='utf-8'))
def rows(p): return [json.loads(x) for x in p.read_text(encoding='utf-8').splitlines() if x.strip()]

manifest_bytes=(PACKAGE/'SOURCE_MANIFEST.json').read_bytes()
if sha(manifest_bytes)!=EXPECTED_SOURCE_MANIFEST: fail('exact copied campaign manifest hash')
source_manifest=json.loads(manifest_bytes)
if len(source_manifest.get('files',[]))!=78: fail('campaign manifest entry count')
if sum(int(x['bytes']) for x in source_manifest['files'])!=391572: fail('campaign manifest listed byte total')
expected={'SOURCE_MANIFEST.json'}|{x['path'] for x in source_manifest['files']}
actual={p.relative_to(PACKAGE).as_posix() for p in PACKAGE.rglob('*') if p.is_file()}
if actual!=expected: fail(f'package file set mismatch extra={sorted(actual-expected)[:5]} missing={sorted(expected-actual)[:5]}')
for rel in expected:
 p=PACKAGE/rel
 if p.is_symlink(): fail('symlink in package: '+rel)
 if p.suffix.lower() in {'.pdf','.png','.jpg','.jpeg','.webp','.zip','.npy','.npz'}: fail('raw/binary third-party payload included: '+rel)
for item in source_manifest['files']:
 b=(PACKAGE/item['path']).read_bytes()
 if len(b)!=item['bytes'] or sha(b)!=item['sha256']: fail('source package hash/bytes: '+item['path'])
copy_manifest=load(UPDATE/'SOURCE_MANIFEST.json')
if copy_manifest.get('campaign_manifest_sha256')!=EXPECTED_SOURCE_MANIFEST or copy_manifest.get('copied_item_count')!=79: fail('integration source manifest pin/count')
entries={x['source_path']:x for x in copy_manifest['files']}
if len(entries)!=79 or set(entries)!={'SOURCE_MANIFEST.json'}|{x['path'] for x in source_manifest['files']}: fail('integration source provenance path set')
for item in source_manifest['files']:
 e=entries[item['path']]
 if e['preserved_path']!='updates/FT-foundational-capability-20261015/package/'+item['path'] or e['sha256']!=item['sha256'] or e['bytes']!=item['bytes']: fail('integration source provenance mismatch: '+item['path'])

claims=load(UPDATE/'CLAIMS.json')
if claims.get('mission_status')!='NOT_ACHIEVED' or {x['id'] for x in claims['claims']}!=set(CARD_IDS): fail('claim ledger ID/status set')
status_rows={x['card_id']:x for x in rows(ROOT/'frontier/CURRENT_CLAIM_STATUS.jsonl')}
claim_rows={x['id']:x for x in rows(ROOT/'indexes/claims.jsonl')}
catalog={x['id']:x for x in load(ROOT/'indexes/agent_catalog.json')['claims']}
gate_rows={x['gate_id']:x for x in rows(ROOT/'frontier/OPEN_PROOF_GATES.jsonl')}
expected_gates={f'G-FT-N{n}-{kind}' for n in range(843,848) for kind in ('REVIEW','CAPABILITY')}
if not expected_gates.issubset(gate_rows): fail('new gate registry coverage')
for gid in expected_gates:
 if gate_rows[gid]['status']!='open' or gate_rows[gid]['completion_evidence']: fail('gate not open or has completion evidence: '+gid)
notices={x['notice_id']:x for x in rows(ROOT/'agent/SEMANTIC_NOTICES.jsonl')}
new_notices=[x for x in notices.values() if x['notice_id'].startswith('SN-FT-')]
if len(new_notices)!=5: fail('expected five source-backed FT scope notices')
# Verify every new evidence locator against exact local bytes and source line range.
def walk_refs(v):
 if isinstance(v,dict):
  if {'path','sha256','lines'}<=v.keys(): yield v
  for child in v.values(): yield from walk_refs(child)
 elif isinstance(v,list):
  for child in v: yield from walk_refs(child)
refs=[]
for cid in CARD_IDS:
 st=load(ROOT/'frontier/cards'/f'{cid}.json')
 if status_rows.get(cid)!=st: fail('status sidecar/current ledger mismatch: '+cid)
 if st['claim_status']!='source_derived_unreviewed': fail('claim status changed: '+cid)
 if claim_rows.get(cid,{}).get('status')!='source_derived_unreviewed' or catalog.get(cid,{}).get('status')!='source_derived_unreviewed': fail('claim/index/catalog mismatch: '+cid)
 card=(ROOT/'cards'/f'{cid}.txt').read_bytes()
 if sha(card)!=st['card_sha256']: fail('card hash mismatch: '+cid)
 if not (ROOT/'frontier/review_cards'/f'{cid}.txt').read_bytes().endswith(card): fail('review wrapper does not preserve card bytes: '+cid)
 refs.extend(walk_refs(st))
for gid in expected_gates: refs.extend(walk_refs(gate_rows[gid]))
for notice in new_notices: refs.extend(walk_refs(notice))
bridge_doc=load(UPDATE/'BRIDGES.json')
if len(bridge_doc.get('bridges',[]))!=3 or any(x.get('status')!='CANDIDATE CONNECTION' for x in bridge_doc['bridges']): fail('typed bridge count/status')
refs.extend(walk_refs(bridge_doc))
for ref in refs:
 p=ROOT/ref['path']
 if not p.is_file() or sha(p.read_bytes())!=ref['sha256']: fail('evidence path/hash mismatch: '+ref['path'])
 lo,hi=ref['lines']
 if lo<1 or hi<lo or hi>len(p.read_text(encoding='utf-8').splitlines()): fail('evidence line range mismatch: '+ref['path'])
if not any(('joint categories' in x['clarification'] or 'joint category fields' in x['clarification']) and 'prime-power' in x['clarification'] for x in new_notices): fail('N844 prime-power/mixed CRT notice absent')
if 'NOT_ACHIEVED' not in (UPDATE/'SYNTHESIS.md').read_text() or 'rank-collapse' not in (UPDATE/'SYNTHESIS.md').read_text() or 'Hidden transfer-spectrum' not in (UPDATE/'SYNTHESIS.md').read_text(): fail('shared negative results or mission status absent')
raw843=(ROOT/'cards'/f'{CARD_IDS[0]}.txt').read_text()
side843=status_rows[CARD_IDS[0]]
if '0<epsilon<1/4' not in raw843 or 'one fixed computable irrational phase' not in raw843 or 'not additionally handed k or an external lookup table' not in raw843: fail('N843 fixed-phase/readout scope absent from raw card')
context=side843['proof_availability'].get('shared_negative_context_sources',[])
context_paths={x['path'] for x in context}
if not {'updates/FT-foundational-capability-20261015/package/workers/foundational_math/RANK_COLLAPSE.md','updates/FT-foundational-capability-20261015/package/workers/foundational_math/HIDDEN_SPECTRUM_COUNTEREXAMPLE.md','updates/FT-foundational-capability-20261015/package/root/REPLAY_RECEIPTS.json'}<=context_paths: fail('N843 shared negative context refs absent')
if any(x in [y['path'] for y in side843['proof_availability']['located_proof_sources']] for x in context_paths): fail('N843 shared negative context misclassified as theorem proof')
card845=(ROOT/'cards'/f'{CARD_IDS[2]}.txt').read_text()
if not all(x in card845 for x in ('EXPECTED','p=.01109','sigma_L=56.6 mb','sigma_H=2.1 mb','unbounded','finite caps','not a general 90% cost')): fail('N845 expected-cost inputs/tails/caps absent')
card846=(ROOT/'cards'/f'{CARD_IDS[3]}.txt').read_text()
gate846=gate_rows['G-FT-N846-CAPABILITY']['question']
if not all(x in card846 and x in gate846 for x in ('0<a<b','(ab)^(1/3)(a^(1/3)+b^(1/3))<=1')): fail('N846 finite-power theorem premise absent from card/gate')
if 'small-angle phase-error budget' not in (ROOT/'cards'/f'{CARD_IDS[4]}.txt').read_text() or 'quadratic' not in (ROOT/'cards'/f'{CARD_IDS[4]}.txt').read_text(): fail('N847 phase-error budget/infidelity scaling absent')
if 'No physical demonstration of the proposed coupler-inclusive monitor' not in (ROOT/'cards'/f'{CARD_IDS[4]}.txt').read_text() or 'established SWS and transmon experiments remain prior evidence' not in (ROOT/'cards'/f'{CARD_IDS[4]}.txt').read_text(): fail('N847 proposed-monitor physical status ambiguous')
access_ready=all((ROOT/f'frontier/dossiers/N{n}.txt').is_file() and (ROOT/f'frontier/connections/N{n}.json').is_file() for n in range(843,848))
print(json.dumps({'status':'PASS','source_items':79,'listed_files':78,'listed_bytes':391572,'cards':len(CARD_IDS),'open_gates':len(expected_gates),'typed_bridges':len(bridge_doc['bridges']),'new_scope_notices':len(new_notices),'evidence_references_checked':len(refs),'generated_access_views_present':access_ready,'mission_status':'NOT_ACHIEVED','scope':'structure, source hashes, provenance and access only; no scientific certification'},indent=2))
