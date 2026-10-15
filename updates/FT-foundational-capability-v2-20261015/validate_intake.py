"""Scoped FT2 preservation validation; no scientific certification."""
from pathlib import Path
import hashlib, importlib.util, json, subprocess

UPDATE=Path(__file__).resolve().parent
ROOT=UPDATE.parents[1]
PACKAGE=UPDATE/'package'
BASE='0c789ca775808e23e57138b56a393ad1e58cb15c'
FREEZE='c291512b7c7491a9b93e7048188dc6b4407518cc168f9949e081926fa9a1734a'
def sha(b): return hashlib.sha256(b).hexdigest()
def git(*args): return subprocess.check_output(['git','-C',str(ROOT),*args])
manifest_bytes=(PACKAGE/'SOURCE_MANIFEST.json').read_bytes()
assert sha(manifest_bytes)==FREEZE
manifest=json.loads(manifest_bytes)
expected={f['path'] for f in manifest['files']}|{'SOURCE_MANIFEST.json'}
actual={str(p.relative_to(PACKAGE)) for p in PACKAGE.rglob('*') if p.is_file()}
assert expected==actual
for f in manifest['files']:
    p=PACKAGE/f['path']; assert not p.is_symlink()
    b=p.read_bytes(); assert len(b)==f['bytes'] and sha(b)==f['sha256'],f['path']

ref_count=0
def walk(obj):
    global ref_count
    if isinstance(obj,dict):
        if isinstance(obj.get('path'),str) and 'sha256' in obj:
            rel=Path(obj['path']); p=(ROOT/rel).resolve()
            assert not rel.is_absolute() and p.is_relative_to(ROOT.resolve()) and p.is_file(),rel
            assert sha(p.read_bytes())==obj['sha256'],rel
            if obj.get('lines') is not None:
                a,b=obj['lines']; assert 1<=a<=b<=len(p.read_text().splitlines()),rel
            ref_count+=1
        for x in obj.values(): walk(x)
    elif isinstance(obj,list):
        for x in obj: walk(x)

cards=[]; gates=[]
for n in range(853,857):
    found=list((ROOT/'frontier/cards').glob(f'N{n}-*.json')); assert len(found)==1
    side=json.loads(found[0].read_text()); cards.append(side['card_id'])
    assert side['claim_status']=='source_derived_unreviewed'
    assert sha((ROOT/side['card_path']).read_bytes())==side['card_sha256']
    walk(side)
    for kind in ['REVIEW','CAPABILITY']:
        path=ROOT/f'frontier/gates/G-FT-N{n}-{kind}.json'
        g=json.loads(path.read_text()); assert g['status']=='open'
        assert side['card_id'] in g['card_ids']; walk(g); gates.append(g['gate_id'])

append_checks=[]
for rel in ['indexes/claims.jsonl','frontier/CURRENT_CLAIM_STATUS.jsonl',
            'frontier/OPEN_PROOF_GATES.jsonl','agent/SEMANTIC_NOTICES.jsonl',
            'indexes/source_metadata.jsonl']:
    before=git('show',f'{BASE}:{rel}'); now=(ROOT/rel).read_bytes()
    assert now.startswith(before),rel
    added=now[len(before):].decode().splitlines()
    rows=[json.loads(line) for line in added]
    if rel=='indexes/claims.jsonl':
        assert len(rows)==4 and {x['id'] for x in rows}==set(cards)
    elif rel=='frontier/CURRENT_CLAIM_STATUS.jsonl':
        assert len(rows)==4 and {x['card_id'] for x in rows}==set(cards)
    elif rel=='frontier/OPEN_PROOF_GATES.jsonl':
        assert len(rows)==8 and {x['gate_id'] for x in rows}==set(gates)
    elif rel=='agent/SEMANTIC_NOTICES.jsonl':
        assert len(rows)==4 and len({x['notice_id'] for x in rows})==4
    elif rel=='indexes/source_metadata.jsonl':
        assert len(rows)==len({x['source_id'] for x in rows})==22
    for line in added:
        row=json.loads(line)
        if rel.endswith('CURRENT_CLAIM_STATUS.jsonl'):
            assert row['card_id'] in cards
        if rel.endswith('OPEN_PROOF_GATES.jsonl'):
            assert row['gate_id'] in gates and row['status']=='open'
    append_checks.append({'path':rel,'old_bytes_unchanged':True,'new_rows':len(added)})

protected=git('ls-tree','-r','--name-only',BASE,'--',
              'updates/FT-foundational-capability-20261015',
              'cards/N843*','cards/N844*','cards/N845*','cards/N846*','cards/N847*',
              'frontier/cards/N843*','frontier/cards/N844*','frontier/cards/N845*',
              'frontier/cards/N846*','frontier/cards/N847*').decode().splitlines()
for rel in protected: assert (ROOT/rel).read_bytes()==git('show',f'{BASE}:{rel}'),rel
assert not git('diff','--name-only','--diff-filter=MDRT',BASE,'--','cards','frontier/cards').strip()
assert not git('status','--porcelain','--untracked-files=all','--','state/checkpoints').strip()

checkpoint=json.loads((UPDATE/'CHECKPOINT_RECORD.json').read_text())
assert checkpoint['base_revision']==BASE
spec=importlib.util.spec_from_file_location('checkpoint',ROOT/'state/publish_checkpoint.py')
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
mod.validate_record(checkpoint,ROOT)
walk(checkpoint)
for name in ['BRIDGES.json','OPEN_GATES.json','CLAIMS.json','SCOPED_NOTICES.json']:
    p=UPDATE/name
    if p.exists(): walk(json.loads(p.read_text()))
print(json.dumps({'status':'PASS','source_items':len(expected),'source_bytes':manifest['bytes'],
                  'cards':len(cards),'open_gates':len(gates),'evidence_ref_occurrences':ref_count,
                  'individual_checkpoint':'PASS','checkpoint_ref_count':len(checkpoint['evidence_refs']),
                  'canonical_checkpoint_publication':'NOT_ATTEMPTED; known inherited unsupported schemas',
                  'append_only_checks':append_checks,'protected_earlier_intake_files':len(protected),
                  'scope':'source/integration integrity and record access only; no proof, priority, physical or practical certification'},indent=2))
