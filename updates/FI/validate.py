#!/usr/bin/env python3
"""Fail-closed FI provenance/history/routing audit; never scientific validation."""
from pathlib import Path
from fractions import Fraction
import ast
import hashlib
import importlib.util
import json
import subprocess

ROOT = Path(__file__).resolve().parents[2]
BASE = 'b7f166a4e0495acc01b6657be44a364432475df4'
MAIN = 'ace0cfc4437fe91c20ccd24d69e0ee4bb335e871'


def need(ok, msg):
    if not ok:
        raise ValueError(msg)


def load(p):
    return json.loads((ROOT / p).read_text())


def rows(p):
    return [json.loads(s) for s in (ROOT / p).read_text().splitlines() if s]


def git(*args):
    return subprocess.check_output(['git', '-C', str(ROOT), *args])


def sha(p):
    return hashlib.sha256((ROOT / p).read_bytes()).hexdigest()


def refs(obj):
    if isinstance(obj, dict):
        if 'path' in obj and 'sha256' in obj:
            yield obj
        for value in obj.values():
            yield from refs(value)
    elif isinstance(obj, list):
        for value in obj:
            yield from refs(value)


def check(r):
    p = r['path']
    need(not Path(p).is_absolute() and (ROOT / p).resolve().is_relative_to(ROOT), 'unsafe reference: ' + p)
    need((ROOT / p).is_file() and sha(p) == r['sha256'], 'hash mismatch: ' + p)
    if 'bytes' in r:
        need((ROOT / p).stat().st_size == r['bytes'], 'size mismatch: ' + p)
    if r.get('lines'):
        a, b = r['lines']
        need(1 <= a <= b <= len((ROOT / p).read_text().splitlines()), 'bad line range: ' + p)


def main():
    sources = load('updates/FI/SOURCE_MANIFEST.json')
    need(sources['main_revision'] == MAIN and sources['previous_pr_head'] == BASE, 'pin mismatch')
    need(len(sources['files']) == 179 and sum(x['bytes'] for x in sources['files']) == 3637863, 'original inventory drift')
    need(sum(x['kind'] == 'directory_payload' for x in sources['files']) == 176, 'directory input count')
    need(sum(x['kind'] == 'pasted_source' for x in sources['files']) == 3, 'pasted input count')
    for r in sources['files']:
        check(r)
        need(Path(r['source_absolute_path']).is_absolute(), 'missing original provenance')
    derived = load('updates/FI/DERIVED_MANIFEST.json')['files']
    need(len(derived) == 114 and sum(x['bytes'] for x in derived) == 859333, 'derived inventory drift')
    for r in derived:
        check(r)
        need(Path(r['owned_original_absolute_path']).is_absolute(), 'missing authored provenance')
    need(not any('site-packages' in x['path'] or '__pycache__' in x['path'] for x in derived), 'environment/cache included')

    for p in ['indexes/claims.jsonl', 'indexes/source_metadata.jsonl', 'frontier/CURRENT_CLAIM_STATUS.jsonl',
              'frontier/OPEN_PROOF_GATES.jsonl', 'web/documents.jsonl', 'agent/SEMANTIC_NOTICES.jsonl', 'state/branches.tsv']:
        need((ROOT / p).read_bytes().startswith(git('show', BASE + ':' + p)), 'not append-only: ' + p)
    for p, k in [('indexes/agent_catalog.json', 'claims'), ('indexes/agent_graph.json', 'nodes'),
                 ('indexes/agent_graph.json', 'edges'), ('mechanisms/bridge_candidates.json', 'bridges'),
                 ('mechanisms/bridge_candidates.json', 'rejected_transfers')]:
        old = json.loads(git('show', BASE + ':' + p))[k]
        need(load(p)[k][:len(old)] == old, 'historical sequence changed: ' + p + ':' + k)
    old = json.loads(git('show', BASE + ':web/catalog.json'))
    need(load('web/catalog.json')[:len(old)] == old, 'historical web catalog changed')
    old = json.loads(git('show', BASE + ':indexes/query_aliases.json'))
    need(all(load('indexes/query_aliases.json').get(k) == v for k, v in old.items()), 'historical aliases changed')
    historical = set(git('ls-tree', '-r', '--name-only', BASE).decode().splitlines())
    immutable = ('state/branches/', 'frontier/review_cards/', 'cards/', 'frontier/cards/', 'state/checkpoints/',
                 'technology/records/', 'evaluation/workflows/records/', 'updates/', 'web/pages/')
    for p in git('diff', '--name-only', BASE).decode().splitlines():
        need(not (p in historical and p.startswith(immutable)), 'old immutable file changed: ' + p)

    own = load('updates/FI/CLAIMS.json')['claims']
    need(len(own) == 3, 'new claim count')
    count = 0
    for c in own:
        st = load('frontier/cards/' + c['id'] + '.json')
        need(st['claim_status'] == 'source_derived_unreviewed', 'unjustified status promotion')
        need(sha(st['card_path']) == st['card_sha256'], 'card hash')
        need((ROOT / 'frontier/dossiers' / (c['id'].split('-')[0] + '.txt')).is_file(), 'missing dossier')
        need((ROOT / 'web/pages' / (c['id'] + '.html')).is_file(), 'missing card page')
        for r in refs(st):
            check(r)
            count += 1
    notices = load('updates/FI/SCOPED_NOTICES.json')
    bridges = load('updates/FI/BRIDGES.json')['bridges']
    need(len(notices) == 2 and all(x['whole_claim_invalidated'] is False for x in notices), 'notice scope')
    need(len(bridges) == 10, 'bridge count')
    states = {'PROVEN LOGICAL DEPENDENCY', 'ESTABLISHED COMPATIBLE INTERFACE', 'CANDIDATE CONNECTION',
              'INCOMPATIBLE ASSUMPTIONS', 'REFUTED TRANSFER'}
    for b in bridges:
        need(b['state'] == b['status'] and b['state'] in states, 'bridge state')
        for side in ['source_interface', 'destination_interface']:
            need(all(b[side].get(k) for k in ['objects', 'regime_and_quantifiers', 'supplied_information',
                'acquired_information', 'legal_access', 'guarantee', 'units_norm_and_precision', 'costs']), 'incomplete paired contract')
    for r in refs(notices + bridges):
        check(r)
        count += 1
    metadata = [x for x in rows('indexes/source_metadata.jsonl') if x.get('source_id', '').startswith('src-FI-')]
    need(len(metadata) == 293, 'indexed evidence count')
    need({x['path'] for x in metadata} == {x['path'] for x in sources['files'] + derived}, 'indexed file set drift')
    for r in metadata:
        check(r)
        need((ROOT / 'web/pages' / (r['source_id'] + '.html')).is_file(), 'missing evidence page')
    need(all(x['status'] == 'open' and not x['completion_evidence'] for x in rows('frontier/OPEN_PROOF_GATES.jsonl')
             if x['gate_id'].startswith('G-FI-')), 'unjustified proof-gate closure')
    parsed = 0
    for p in (ROOT / 'updates/FI').rglob('*.py'):
        ast.parse(p.read_text(), filename=str(p))
        parsed += 1

    pub = load('updates/FI/PUBLICATION_STATUS.json')
    need(pub['standard_publisher_exit_code'] != 0 and len(pub['individually_validated_new_checkpoints']) == 1, 'publisher boundary')
    for r in pub['inherited_records_preserved']:
        check(r)
        need(sha(r['path']) == hashlib.sha256(git('show', BASE + ':' + r['path'])).hexdigest(), 'old malformed checkpoint changed')
    spec = importlib.util.spec_from_file_location('fi_publisher', ROOT / 'state/publish_checkpoint.py')
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    for p in pub['individually_validated_new_checkpoints']:
        x = load(p)
        m.validate_record(x, ROOT)
        need(x['base_revision'] == BASE and x['parent_checkpoint_ids'] == [], 'new lineage')

    portable = load('updates/FI/PORTABLE_REPLAY_RECEIPT.json')
    need(portable['status'] == 'PASS' and portable['total_steps'] == 19, 'portable replay scope')
    need('FAIL' in portable['historical_kinetic_endpoint_equality_audit'], 'historical failure omitted')
    step_counts = {}
    for r in portable['groups']:
        check(r)
        receipt = load(r['path'])
        need(receipt['status'] == 'PASS' and len(receipt['checks']) == receipt['expected_steps']
             and all(x['exit_code'] == 0 for x in receipt['checks']), 'portable replay failure')
        need(receipt['published_inputs_hash_unchanged'] is True, 'input integrity failure')
        step_counts[receipt['group']] = len(receipt['checks'])
        for log in receipt['checks']:
            p = str(Path(r['path']).parent / log['log'])
            need(sha(p) == log['log_sha256'], 'replay log mismatch')
    need(step_counts == dict(quartic=7, kinetics=8, barrier=4), 'replay groups changed')

    for tid, version in [('T-completion-directed-kinetic-acquisition', 4), ('T-recoverable-local-compliance-gating', 1)]:
        t = load('technology/records/' + tid + '/v' + str(version).zfill(4) + '.json')
        if version > 1:
            check(t['previous'])
        need(t['version'] == version and t['stage'] == 'simulation' and any(g['stage'] == 'experiment' and
             g['decision'] == 'open' for g in t['gates']), 'unjustified technology promotion')
    q = load('updates/FI/synthesis/quartic/results/independent_checks.json')
    need(len(q['checks_passed']) == 9 and q['near_contact_pair']['covariance_hessian_over_anisotropy_squared_limit'] == '5/78', 'quartic result scope')
    need('9*eps**14' in q['full_rank_compatible_covariance_extension']['covariance_determinant'], 'full-rank extension missing')
    gate = load('updates/FI/synthesis/root/MIXED_GATE_RESULTS.json')
    need(gate['status'] == 'PASS' and gate['groups'] == 8 and
         Fraction(gate['finite_amplitude_counterexample']['total_energy_difference']) == -Fraction(3969, 5242880), 'spatial countermodel scope')
    historical_failure = load('updates/FI/synthesis/kinetics/analysis/audit_reverse_failure.json')
    need(historical_failure['returncode'] == 1 and 'AssertionError' in historical_failure['stderr'], 'historical FAIL not preserved')
    alpha = load('updates/FI/synthesis/root/WEIGHTED_ALPHA_REPLAY.json')
    need(alpha['status'] == 'PASS' and len(alpha['cases']) == 3 and all(
         x['raw_Euclidean_symmetric'] is False and x['weighted_detailed_balance_exact'] is True and
         x['old_alpha_le_new_alpha'] is True for x in alpha['cases']), 'weighted retained-witness scope')
    fresh = load('updates/FI/synthesis/kinetics/analysis/fresh_replay_results.json')
    need(len(fresh['tensor_replays']) == 3 and all(
         x['exact_high_precision_alpha_recertification']['old_alpha_le_new_exact_alpha'] is True and
         x['exact_high_precision_alpha_recertification']['stored_upper_rebuilt_exactly_from_old_alpha'] is True
         for x in fresh['tensor_replays']), 'separate recertification scope')
    need(fresh['matched_full_state_comparator']['states'] == 262144 and fresh['matched_full_state_comparator']['iterations'] == 6, 'matched comparator scope')
    cubic = load('updates/FI/synthesis/kinetics/analysis/degree3_countermodel_results.json')
    need(cubic['query_vectors_identical_for_every_coordinate'] is True and cubic['both_exact_Ku_eq_one'] is True, 'cubic countermodel scope')
    workers = load('updates/FI/synthesis/root/READ_AND_PRIMARY_LEDGER.json')['worker_configuration']
    need(workers['configured_model'] == 'gpt-6-luna' and workers['reasoning_effort'] == 'max' and
         workers['roles'] == 5 and workers['nested_agents'] == 0, 'worker contract')
    print(json.dumps(dict(status='PASS', base_revision=BASE, main_revision=MAIN,
        original_files=179, original_bytes=3637863, derived_files=114, derived_bytes=859333,
        indexed_sources=len(metadata), new_cards=3, scoped_notices=2, paired_bridges=10, new_checkpoints=1,
        python_syntax_checks=parsed, scoped_evidence_refs=count, portable_replay_steps=19,
        historical_kinetic_endpoint_audit='FAIL preserved; separate retained-vector recertification PASS',
        global_checkpoint_validation='Inherited unsupported-schema failure preserved; not passed',
        scientific_truth_checked=False), indent=2))


if __name__ == '__main__':
    main()
