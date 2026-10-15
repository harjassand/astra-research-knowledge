#!/usr/bin/env python3
"""FS additive integrity and individually validated handoffs; no scientific certification."""
from __future__ import annotations
import argparse
import ast
import copy
import hashlib
import html
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys

sys.dont_write_bytecode = True
BASE = '846f185763ed3a27310fad4ce9471ba324d1e5f4'
PREFIX = 'updates/FS-phase-closure-20261015/'
IMMUTABLE = ('cards/', 'frontier/cards/', 'frontier/review_cards/', 'updates/', 'state/checkpoints/',
             'state/branches/', 'technology/records/', 'web/pages/', 'evaluation/workflows/records/')

def need(value, message):
    if not value: raise ValueError(message)
def digest(data): return hashlib.sha256(data).hexdigest()
def encoded(value): return (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode()
def local(root, name):
    need(isinstance(name, str) and name and not Path(name).is_absolute() and '..' not in Path(name).parts, 'unsafe path: ' + str(name))
    p = (root / name).resolve(); need(p.is_relative_to(root.resolve()), 'outside root: ' + name); return p
def sha(root, name): return digest(local(root, name).read_bytes())
def load(root, name): return json.loads(local(root, name).read_text())
def rows(root, name): return [json.loads(x) for x in local(root, name).read_text().splitlines() if x.strip()]
def git(root, *args): return subprocess.check_output(['git', '-C', str(root), *args])
def unique(items, key):
    result = {x[key]: x for x in items}; need(len(result) == len(items), 'duplicate identifiers: ' + key); return result
def module(path, name):
    spec = importlib.util.spec_from_file_location(name, path); obj = importlib.util.module_from_spec(spec); spec.loader.exec_module(obj); return obj
def refs(value):
    if isinstance(value, dict):
        if {'path', 'sha256'} <= value.keys(): yield value
        for x in value.values(): yield from refs(x)
    elif isinstance(value, list):
        for x in value: yield from refs(x)

def check(root, ref):
    need(re.fullmatch(r'[0-9a-f]{64}', ref['sha256']), 'invalid full evidence hash')
    found = None
    for name in dict.fromkeys([ref['path'], ref.get('read_path', ref['path'])]):
        p = local(root, name)
        if not p.is_file(): continue
        raw = p.read_bytes()
        if digest(raw) == ref['sha256']: found = raw; break
        if p.suffix == '.html':
            for b in re.findall(r'<pre(?:\s[^>]*)?>(.*?)</pre>', raw.decode(), re.S):
                text = html.unescape(b).encode()
                if digest(text) == ref['sha256']: found = text; break
    need(found is not None, 'source hash unavailable: ' + ref['path'])
    if 'bytes' in ref: need(len(found) == ref['bytes'], 'size mismatch: ' + ref['path'])
    if ref.get('lines'):
        a, b = ref['lines']; need(type(a) is int and type(b) is int and 1 <= a <= b <= len(found.decode().splitlines()), 'invalid inclusive range: ' + ref['path'])
    if ref.get('source_revision'):
        old = git(root, 'show', ref['source_revision'] + ':' + ref['path'])
        need(digest(old) == ref['sha256'], 'source revision mismatch: ' + ref['path'])

def check_history(root):
    for path in ['indexes/claims.jsonl', 'indexes/source_metadata.jsonl', 'frontier/CURRENT_CLAIM_STATUS.jsonl',
                 'frontier/OPEN_PROOF_GATES.jsonl', 'agent/SEMANTIC_NOTICES.jsonl', 'web/documents.jsonl', 'state/branches.tsv']:
        need(local(root, path).read_bytes().startswith(git(root, 'show', BASE + ':' + path)), 'historical byte prefix changed: ' + path)
    grouped = {'indexes/agent_catalog.json': ['claims'], 'indexes/agent_graph.json': ['nodes', 'edges'],
               'mechanisms/bridge_candidates.json': ['bridges', 'rejected_transfers'], 'web/catalog.json': [None]}
    for path, fields in grouped.items():
        old_bytes = git(root, 'show', BASE + ':' + path); old = json.loads(old_bytes); new = load(root, path); projection = copy.deepcopy(new)
        for field in fields:
            before = old[field] if field else old; after = new[field] if field else new
            need(after[:len(before)] == before, 'historical array value/order changed: ' + path)
            if field: projection[field] = after[:len(before)]
            else: projection = after[:len(before)]
        need(encoded(projection) == old_bytes, 'historical JSON keys/metadata/format changed: ' + path)
    aliases = json.loads(git(root, 'show', BASE + ':indexes/query_aliases.json'))
    need(all(load(root, 'indexes/query_aliases.json').get(k) == v for k, v in aliases.items()), 'historical aliases changed')
    history = set(git(root, 'ls-tree', '-r', '--name-only', BASE).decode().splitlines())
    for path in git(root, 'diff', '--name-only', BASE).decode().splitlines():
        need(not (path in history and path.startswith(IMMUTABLE)), 'historical immutable artifact changed: ' + path)
    return history

def check_replay(root, replay_dir, specs):
    receipt = json.loads((replay_dir / 'RECEIPT.json').read_text())
    expected = [(x[0], x[1]) for x in specs]
    need(receipt['status'] == 'PASS' and receipt['published_inputs_hash_unchanged'] and not receipt['changed_published_paths'], 'replay failed or published input changed')
    need(receipt['base_revision'] == BASE and receipt['total_steps'] == len(expected) == len(receipt['checks']), 'replay count/pin mismatch')
    need(receipt['generator_sha256'] == sha(root, PREFIX + 'replay.py'), 'replay runner hash drift')
    need([(x['name'], x['script']) for x in receipt['checks']] == expected, 'bounded replay selection changed')
    need(receipt['all_positivity_certified'] is False, 'inconclusive replay promoted to all-positivity')
    for item in receipt['checks']:
        need(item['exit_code'] == 0 and item['execution_check'] == 'PASS', 'replay execution failure: ' + item['name'])
        need(digest(local(replay_dir, item['log']).read_bytes()) == item['log_sha256'], 'replay log hash drift')
        need(item['original_script_sha256'] == sha(root, PREFIX + item['script']), 'replay original script drift')
        output = item['fresh_output']; need(output and digest(local(replay_dir, output['path']).read_bytes()) == output['sha256'], 'fresh replay output hash drift')
    for name in ['published_input_manifest', 'packet_input_manifest']:
        ref = receipt[name]; need(digest(local(replay_dir, ref['path']).read_bytes()) == ref['sha256'], 'replay input manifest drift')
    integral = next(x for x in receipt['checks'] if x['name'] == 'phase_integral512')
    data = json.loads(local(replay_dir, integral['fresh_output']['path']).read_text())
    need(data['N'] == 512 and data['status'] == 'inconclusive interval bound' and integral['result_classification'] == 'expected_inconclusive_interval_bound', 'integral512 scope lost')
    need(len(receipt['inconclusive_results']) == 1 and receipt['inconclusive_results'][0]['name'] == 'phase_integral512', 'expected inconclusive result not retained separately')
    for ref in receipt['pinned_dependencies']:
        check(root, ref); need(local(root, ref['path']).read_bytes() == git(root, 'show', BASE + ':' + ref['path']), 'pinned older dependency changed')
    for adapter in receipt['runtime_adapters']:
        if adapter.get('file'):
            need(adapter['original_sha256'] == sha(root, PREFIX + adapter['file']), 'runtime adapter original hash drift')
            need(re.fullmatch(r'[0-9a-f]{64}', adapter['adapted_sha256']), 'runtime adapter adapted hash absent')
            executed = [x for x in receipt['checks'] if x['script'] == adapter['file']]
            need(len(executed) == 1 and executed[0]['executed_script_sha256'] == adapter['adapted_sha256'], 'recorded adaptation differs from executed script')
    return receipt

def validate(root, replay_dir=None, pre_publication=False):
    source = load(root, PREFIX + 'SOURCE_MANIFEST.json'); derived = load(root, PREFIX + 'DERIVED_MANIFEST.json')
    need(source['main_revision'] == BASE and source['total_files'] == len(source['files']) == 67, 'supplied source count/pin mismatch')
    need(source['total_bytes'] == sum(x['bytes'] for x in source['files']) == 460919, 'supplied source bytes mismatch')
    need(len(derived['files']) == derived['total_files'] and sum(x['bytes'] for x in derived['files']) == derived['total_bytes'], 'derived manifest count/bytes mismatch')
    originals = 0
    for ref in source['files'] + derived['files']: check(root, ref)
    for ref in source['files']:
        p = Path(ref['source_absolute_path']); need(p.is_absolute(), 'original provenance must be absolute')
        if p.is_file(): need(digest(p.read_bytes()) == ref['sha256'], 'available original changed: ' + str(p)); originals += 1
    curation = load(root, PREFIX + 'CURATION_INPUT.json'); receipt = load(root, PREFIX + 'INTEGRATION_GENERATOR_RECEIPT.json')
    need(curation['schema'] == 'astra.fs-curation-input.v1' and curation['intake_id'] == 'FS' and curation['base_revision'] == BASE, 'curation schema/pin mismatch')
    need(receipt['curation_input_sha256'] == sha(root, PREFIX + 'CURATION_INPUT.json') and receipt['generator_sha256'] == sha(root, PREFIX + 'build_integration.py'), 'generator/input receipt hash mismatch')
    for path, wanted in receipt['owned_artifacts'].items(): need(sha(root, path) == wanted, 'generated owned artifact drift: ' + path)
    for ref in curation['evidence'].values(): check(root, ref)
    ids = {x['id'] for x in curation['cards']}; need({x.split('-')[0] for x in ids} == {'N840', 'N841', 'N842'} and len(ids) == len(curation['cards']), 'reserved claim routes changed')
    claims = unique(rows(root, 'indexes/claims.jsonl'), 'id'); current = unique(rows(root, 'frontier/CURRENT_CLAIM_STATUS.jsonl'), 'card_id')
    catalog = unique(load(root, 'indexes/agent_catalog.json')['claims'], 'id')
    for cid in ids:
        status = current[cid]; need(claims[cid]['status'] == status['claim_status'] == catalog[cid]['status'] == 'source_derived_unreviewed', 'scientific status promotion')
        need(load(root, 'frontier/cards/' + cid + '.json') == status, 'current status sidecar disagreement')
        need(sha(root, status['card_path']) == status['card_sha256'] == catalog[cid]['card_sha256'], 'raw card hash disagreement')
        need(local(root, 'frontier/review_cards/' + cid + '.txt').read_bytes().endswith(local(root, status['card_path']).read_bytes()), 'review wrapper changed raw card bytes')
        need(local(root, 'frontier/dossiers/' + cid.split('-')[0] + '.txt').is_file(), 'generated dossier absent')
        for ref in refs(status): check(root, ref)
    metadata = rows(root, 'indexes/source_metadata.jsonl')
    for item in curation['sources']:
        sid = item.get('source_id', 'src-FS-' + digest(item['path'].encode())[:16])
        matches = [x for x in metadata if x.get('source_id') == sid]
        need(len(matches) == 1 and matches[0].get('path') == item['path'] and matches[0].get('sha256') == item['sha256'], 'new source metadata disagreement')
        check(root, matches[0]); need(local(root, 'web/pages/' + sid + '.html').is_file(), 'new source page absent')
    gates = {x['gate_id']: x for x in rows(root, 'frontier/OPEN_PROOF_GATES.jsonl') if x['gate_id'].startswith('G-FS-')}
    need(set(gates) == set(receipt['gate_ids']) and len(gates) == 2 * len(ids) + len(curation.get('gates', [])), 'open gate count/identity mismatch')
    need(all(x['status'] == 'open' and x['completion_evidence'] == [] for x in gates.values()), 'scientific gate promoted')
    bridges = load(root, PREFIX + 'BRIDGES.json')['bridges']; notices = load(root, PREFIX + 'SCOPED_NOTICES.json')
    need({x['id'] for x in bridges} == {x['id'] for x in curation.get('bridges', [])}, 'bridge selection mismatch')
    need({x['notice_id'] for x in notices} == {x['notice_id'] for x in curation.get('notices', [])}, 'notice selection mismatch')
    for ref in refs([bridges, notices, list(gates.values())]): check(root, ref)
    history = check_history(root)
    replay_module = module(local(root, PREFIX + 'replay.py'), 'fs_replay_scoped_validation')
    replay = check_replay(root, replay_dir or local(root, PREFIX + 'replay_validation'), replay_module.STEP_SPECS)
    subprocess.run([sys.executable, '-B', str(root / 'frontier/build_access.py'), 'check', '--base-revision', BASE], cwd=root, check=True, capture_output=True)
    new_tech = [str(p.relative_to(root)) for p in (root / 'technology/records').rglob('*.json') if str(p.relative_to(root)) not in history]
    sys.path.insert(0, str(root)); tech_module = module(root / 'technology/validate.py', 'fs_technology_validation')
    for path in new_tech:
        record = load(root, path); tech_module.validate(record, root)
        need(record['stage'] in ('opportunity', 'mechanism', 'model'), 'technology stage promoted beyond scoped model')
        need(all(g['decision'] == 'open' for g in record.get('gates', []) if g['stage'] in ('simulation', 'experiment', 'prototype', 'scaling')), 'physical capability gate promoted')
    checkpoint_checked = False; global_status = 'NOT CHECKED (explicit pre-publication mode)'
    if not pre_publication:
        pub = load(root, PREFIX + 'PUBLICATION_STATUS.json')
        need(pub['standard_publisher_exit_code'] != 0 and 'unsupported checkpoint schema' in pub['standard_publisher_stderr'], 'inherited standard-publisher failure not retained')
        need(pub['global_validation_exit_code'] != 0 and 'unsupported checkpoint schema' in pub['global_validation_stderr'], 'inherited global validation failure not retained')
        inherited = json.loads(git(root, 'show', BASE + ':updates/FR-capital-mining-20261015/PUBLICATION_STATUS.json'))['inherited_records_preserved']
        need({x['path'] for x in pub['inherited_records_preserved']} == {x['path'] for x in inherited}, 'known inherited failed record set changed')
        for ref in pub['inherited_records_preserved']: check(root, ref); need(local(root, ref['path']).read_bytes() == git(root, 'show', BASE + ':' + ref['path']), 'inherited checkpoint bytes changed')
        path = pub['individually_validated_checkpoint']; need(path == curation['checkpoint_path'] and path not in history, 'new checkpoint identity mismatch')
        checkpoint = load(root, path); publisher = module(root / 'state/publish_checkpoint.py', 'fs_checkpoint_validation'); publisher.validate_record(checkpoint, root)
        need(checkpoint['base_revision'] == BASE, 'new checkpoint base mismatch'); checkpoint_checked = True
        global_status = 'FAIL: inherited unsupported schemas preserved; new checkpoint individually valid only.'
    parsed = 0
    for p in local(root, PREFIX).rglob('*.py'):
        if '__pycache__' not in p.parts: ast.parse(p.read_text(), filename=str(p)); parsed += 1
    return {'status': 'PASS', 'scope': 'FS additive integrity only; no mathematical truth, interval implementation, novelty or physical acquisition certification.',
        'base_revision': BASE, 'original_files': len(source['files']), 'original_bytes': source['total_bytes'],
        'available_originals_observed_unchanged': originals, 'derived_files': derived['total_files'], 'derived_bytes': derived['total_bytes'],
        'new_cards': len(ids), 'typed_bridges': len(bridges), 'scoped_notices': len(notices), 'open_gates': len(gates),
        'fresh_bounded_replay_steps': replay['total_steps'], 'inconclusive_results_retained': len(replay['inconclusive_results']),
        'all_positivity_certified': False, 'parsed_python_files': parsed, 'new_technology_records_validated': len(new_tech),
        'new_checkpoint_individually_validated': checkpoint_checked, 'global_checkpoint_validation': global_status,
        'scientific_truth_checked': False, 'mode': 'pre-publication' if pre_publication else 'complete_scoped_validation'}

def main():
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--replay-dir', type=Path); parser.add_argument('--pre-publication', action='store_true')
    args = parser.parse_args(); print(json.dumps(validate(args.repo.resolve(), args.replay_dir.resolve() if args.replay_dir else None, args.pre_publication), indent=2))
if __name__ == '__main__': main()
