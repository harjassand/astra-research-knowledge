#!/usr/bin/env python3
"""Deterministic integration safeguards on a temporary fixture; no scientific tests."""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = Path('/Users/harjas/Documents/ChatGPT/ultra/work/astra-capital-compensation-exchange')


def module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj


g = module(HERE / 'build_fp_integration.py', 'fp_generator_fixture')
access = module(REPO / 'frontier/build_access.py', 'fp_access_fixture')
checks = []


def put(root, path, value):
    p = root / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(value if isinstance(value, bytes) else g.encoded(value))


def fail(label, action):
    try:
        action()
    except ValueError:
        checks.append(label)
    else:
        raise AssertionError('Expected fail-closed result: ' + label)


with tempfile.TemporaryDirectory(prefix='astra-fp-fixture-') as temp:
    root = Path(temp)
    for path in access.INPUTS:
        put(root, path, b'fixture text\n')
    for path in ['indexes/claims.jsonl', 'indexes/source_metadata.jsonl',
                 'frontier/CURRENT_CLAIM_STATUS.jsonl', 'frontier/OPEN_PROOF_GATES.jsonl',
                 'agent/SEMANTIC_NOTICES.jsonl', 'literature/LEMMA_ATLAS.jsonl', 'web/documents.jsonl']:
        put(root, path, b'')
    put(root, 'indexes/agent_catalog.json', {'claims': []})
    put(root, 'indexes/agent_graph.json', {'nodes': [], 'edges': []})
    put(root, 'indexes/query_aliases.json', {})
    put(root, 'indexes/blockers.json', {'blockers': []})
    put(root, 'mechanisms/bridge_candidates.json', {'status': 'MODEL_HYPOTHESIS / NOT_THEOREM',
                                                 'bridges': [], 'rejected_transfers': []})
    put(root, 'web/catalog.json', [])
    put(root, 'agent/manifest.json', {'hashes': {}, 'claims': 0})
    path = 'updates/FP/fixture-source.txt'
    source = b'Fixture-only first line.\nFixture-only second line.\n'
    put(root, path, source)
    digest = hashlib.sha256(source).hexdigest()
    interface = {k: 'Fixture-only interface value for ' + k + '.' for k in g.INTERFACE}
    curation = {'schema': g.SCHEMA, 'intake_id': 'FP', 'base_revision': '0' * 40,
        'date_version': 'disposable software fixture',
        'checkpoint_path': 'state/checkpoints/worker-fp-fixture/fixture.json',
        'sources': [{'path': path, 'sha256': digest, 'title': 'Disposable fixture source',
                     'read_depth': 'Two fixture lines only; no scientific claim.'}],
        'evidence': {'fixture': {'path': path, 'sha256': digest, 'lines': [1, 2],
                                 'range_scope': 'Fixture-only two-line range.'}},
        'cards': [{'id': 'N822-disposable-fixture', 'title': 'Disposable fixture card',
            'topics': ['software fixture'], 'scientific_scope': 'Disposable fixture only.',
            'statement': 'No scientific statement is asserted by this fixture.',
            'assumptions': ['Disposable temporary directory.'], 'proof_spine': ['Verify fixture publication structure.'],
            'costs': 'Unmeasured fixture runtime.', 'information_acquisition': 'Two supplied fixture lines.',
            'obstruction': 'No scientific inference is allowed from fixture success.',
            'comparator': 'Not applicable to a scientific comparison.', 'missing_lemma': 'No scientific lemma is supplied.',
            'next_decisive_step': 'Review actual supplied research separately.',
            'read_review_depth': 'Fixture only.', 'proof_refs': ['fixture']}],
        'notices': [{'notice_id': 'SN-FP-fixture', 'card_ids': ['N822-disposable-fixture'],
                     'issue': 'Fixture only.', 'clarification': 'Fixture notice does not change scientific status.',
                     'ref_ids': ['fixture']}],
        'bridges': [{'id': 'FP_fixture', 'state': 'CANDIDATE CONNECTION',
                     'cards': ['N822-disposable-fixture'], 'source_interface': interface,
                     'destination_interface': interface, 'alignment': 'Disposable fixture pairing.',
                     'missing_lemma': 'No scientific bridge is asserted.', 'falsifier': 'Reject mismatched fixture bytes.',
                     'ref_ids': ['fixture']}]}
    input_hash = g.sha(g.encoded(curation))
    plan = g.build_plan(root, curation, input_hash)
    assert not (root / 'cards/N822-disposable-fixture.txt').exists()
    checks.append('read-only planning writes no fixture artifact')
    count = g.apply_plan(plan)
    assert count > 0
    checks.append('initial fixture apply succeeds')
    replay = g.build_plan(root, curation, input_hash)
    assert replay.summary()['changed_file_count'] == 0
    assert g.apply_plan(replay) == 0
    checks.append('identical rerun changes zero files')
    outputs, manifest = access.build(root=root, base_revision=curation['base_revision'])
    assert 'frontier/dossiers/N822.txt' in outputs
    assert manifest['counts']['cards'] == 1 and manifest['counts']['source_access_issues'] == 0
    assert manifest['counts']['gates'] == 2
    checks.append('actual public-access builder accepts generated authoritative records')
    for gate in g.Plan(root).rows('frontier/OPEN_PROOF_GATES.jsonl'):
        assert gate['status'] == 'open' and gate['completion_evidence'] == []
    checks.append('scientific gates remain open')
    claim_map = json.loads((root / 'updates/FP/CLAIMS.json').read_text())
    assert claim_map['claims'][0]['checkpoint'] == curation['checkpoint_path']
    checks.append('checkpoint pointer propagated without publication')
    changed = copy.deepcopy(curation)
    changed['cards'][0]['statement'] = 'Changed fixture bytes.'
    fail('immutable card overwrite rejected', lambda: g.build_plan(root, changed, input_hash))
    changed = copy.deepcopy(curation)
    changed['sources'][0]['sha256'] = 'f' * 64
    fail('source hash mismatch rejected', lambda: g.build_plan(root, changed, input_hash))
    changed = copy.deepcopy(curation)
    changed['evidence']['fixture']['lines'] = [1, 3]
    fail('invalid inclusive source range rejected', lambda: g.build_plan(root, changed, input_hash))
    changed = copy.deepcopy(curation)
    changed['cards'][0]['id'] = 'N822-colliding-fixture'
    fail('numeric route collision rejected', lambda: g.build_plan(root, changed, input_hash))
    pending = g.build_plan(root, curation, input_hash)
    (root / path).write_bytes(source + b'Concurrent fixture change.\n')
    fail('source changed after planning rejected before mutation', lambda: g.apply_plan(pending))
    (root / path).write_bytes(source)
    original = (root / 'indexes/claims.jsonl').read_bytes()
    duplicate = json.loads(original)
    duplicate['title'] = 'Conflicting fixture title.'
    (root / 'indexes/claims.jsonl').write_bytes(original + (json.dumps(duplicate) + '\n').encode())
    fail('conflicting claim duplicate rejected', lambda: g.build_plan(root, curation, input_hash))

result = {'status': 'PASS', 'scope': 'Disposable integration software safeguards only; no scientific verification.',
          'checks': checks, 'check_count': len(checks), 'real_repository_mutated': False,
          'generator_sha256': hashlib.sha256((HERE / 'build_fp_integration.py').read_bytes()).hexdigest()}
(HERE / 'FIXTURE_TEST_RECEIPT.json').write_bytes(g.encoded(result, sort=True))
print(json.dumps(result, indent=2))
