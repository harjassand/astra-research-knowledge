#!/usr/bin/env python3
"""Fail-closed FJ integrity, history, routing and scope checks; not scientific certification."""
from pathlib import Path
from fractions import Fraction
import ast
import hashlib
import importlib.util
import json
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[2]
BASE = 'cb62d881a071c617b11d7dbc82a98921969389a7'
MAIN = 'ace0cfc4437fe91c20ccd24d69e0ee4bb335e871'


def need(ok, message):
    if not ok:
        raise ValueError(message)


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
    need(not Path(p).is_absolute() and (ROOT / p).resolve().is_relative_to(ROOT), 'unsafe reference: '+p)
    need((ROOT / p).is_file() and sha(p) == r['sha256'], 'hash mismatch: '+p)
    if 'bytes' in r:
        need((ROOT / p).stat().st_size == r['bytes'], 'size mismatch: '+p)
    if r.get('lines'):
        a,b = r['lines']
        need(1 <= a <= b <= len((ROOT / p).read_text().splitlines()), 'bad lines: '+p)


def main():
    source = load('updates/FJ/SOURCE_MANIFEST.json')
    need(source['main_revision'] == MAIN and source['previous_pr_head'] == BASE, 'source pins')
    need(len(source['files']) == 26 and sum(x['bytes'] for x in source['files']) == 259242, 'source inventory')
    need(sum(x['kind'] == 'original_archive' for x in source['files']) == 3, 'archive count')
    need(sum(x['kind'] == 'archive_member' for x in source['files']) == 20, 'member count')
    need(sum(x['kind'] == 'pasted_source' for x in source['files']) == 3, 'pasted count')
    for r in source['files']:
        check(r)
        need(Path(r['source_absolute_path']).is_absolute(), 'original provenance')
    for archive in [x for x in source['files'] if x['kind'] == 'original_archive']:
        with zipfile.ZipFile(ROOT / archive['path']) as z:
            need(z.testzip() is None, 'zip CRC')
            members = [x for x in source['files'] if x['kind'] == 'archive_member' and x['group'] == archive['group']]
            need(set(x['archive_member'] for x in members) == set(x.filename for x in z.infolist() if not x.is_dir()), 'zip member inventory')
            for x in members:
                need(hashlib.sha256(z.read(x['archive_member'])).hexdigest() == x['sha256'], 'member byte identity')
    initial = load('updates/FJ/INTAKE_MANIFEST.json')
    supplement = load('updates/FJ/SUPPLEMENTAL_INTAKE_MANIFEST.json')
    need(len(initial['files']) == 21 and len(supplement['files']) == 5, 'intake chronology')
    need(supplement['initial_manifest_sha256'] == sha('updates/FJ/INTAKE_MANIFEST.json'), 'supplement parent pin')
    derived = load('updates/FJ/DERIVED_MANIFEST.json')['files']
    need(len(derived) == 174 and sum(x['bytes'] for x in derived) == 1083449, 'derived inventory')
    for r in derived:
        check(r)
        need(Path(r['owned_original_absolute_path']).is_absolute(), 'owned provenance')
    need(not any(x['path'].endswith(('.pdf','.xml','.png')) or 'site-packages' in x['path'] or '__pycache__' in x['path'] for x in derived), 'full primary/environment/cache publication')

    for p in ['indexes/claims.jsonl','indexes/source_metadata.jsonl','frontier/CURRENT_CLAIM_STATUS.jsonl',
              'frontier/OPEN_PROOF_GATES.jsonl','web/documents.jsonl','agent/SEMANTIC_NOTICES.jsonl','state/branches.tsv']:
        need((ROOT / p).read_bytes().startswith(git('show', BASE+':'+p)), 'not append-only: '+p)
    for p,key in [('indexes/agent_catalog.json','claims'),('indexes/agent_graph.json','nodes'),('indexes/agent_graph.json','edges'),
                  ('mechanisms/bridge_candidates.json','bridges'),('mechanisms/bridge_candidates.json','rejected_transfers')]:
        old = json.loads(git('show', BASE+':'+p))[key]
        need(load(p)[key][:len(old)] == old, 'old sequence changed: '+p+':'+key)
    old = json.loads(git('show', BASE+':web/catalog.json'))
    need(load('web/catalog.json')[:len(old)] == old, 'old web catalog changed')
    old = json.loads(git('show', BASE+':indexes/query_aliases.json'))
    need(all(load('indexes/query_aliases.json').get(k) == v for k,v in old.items()), 'old aliases changed')
    historical = set(git('ls-tree','-r','--name-only',BASE).decode().splitlines())
    immutable = ('state/branches/','frontier/review_cards/','cards/','frontier/cards/','state/checkpoints/',
                 'technology/records/','evaluation/workflows/records/','updates/','web/pages/')
    for p in git('diff','--name-only',BASE).decode().splitlines():
        need(not (p in historical and p.startswith(immutable)), 'immutable old file changed: '+p)

    own = load('updates/FJ/CLAIMS.json')['claims']
    need(len(own) == 3 and {x['id'].split('-')[0] for x in own} == {'N806','N807','N808'}, 'claim set')
    checked = 0
    for c in own:
        st = load('frontier/cards/'+c['id']+'.json')
        need(st['claim_status'] == 'source_derived_unreviewed', 'status promotion')
        need(sha(st['card_path']) == st['card_sha256'], 'card hash')
        need((ROOT / 'frontier/dossiers' / (c['id'].split('-')[0]+'.txt')).is_file(), 'missing dossier')
        need((ROOT / 'web/pages' / (c['id']+'.html')).is_file(), 'missing card page')
        for r in refs(st):
            check(r)
            checked += 1
    notices = load('updates/FJ/SCOPED_NOTICES.json')
    need(len(notices) == 3 and all(x['whole_claim_invalidated'] is False for x in notices), 'notice scope')
    bridges = load('updates/FJ/BRIDGES.json')['bridges']
    states = {'PROVEN LOGICAL DEPENDENCY','ESTABLISHED COMPATIBLE INTERFACE','CANDIDATE CONNECTION','INCOMPATIBLE ASSUMPTIONS','REFUTED TRANSFER'}
    need(len(bridges) == 9, 'bridge count')
    for b in bridges:
        need(b['state'] == b['status'] and b['state'] in states, 'bridge state')
        for side in ['source_interface','destination_interface']:
            need(all(b[side].get(k) for k in ['objects','regime_and_quantifiers','supplied_information','acquired_information',
                                            'legal_access','guarantee','units_norm_and_precision','costs']), 'incomplete paired interface')
    for r in refs(notices+bridges):
        check(r)
        checked += 1
    metadata = [x for x in rows('indexes/source_metadata.jsonl') if x.get('source_id','').startswith('src-FJ-')]
    need(len(metadata) == 200 and {x['path'] for x in metadata} == {x['path'] for x in source['files']+derived}, 'indexed evidence set')
    for r in metadata:
        check(r)
        need((ROOT / 'web/pages' / (r['source_id']+'.html')).is_file(), 'missing source page')
    gates = [x for x in rows('frontier/OPEN_PROOF_GATES.jsonl') if x['gate_id'].startswith('G-FJ-')]
    need(len(gates) == 6 and all(x['status'] == 'open' and not x['completion_evidence'] for x in gates), 'proof gate promotion')
    parsed = 0
    for p in (ROOT / 'updates/FJ').rglob('*.py'):
        ast.parse(p.read_text(), filename=str(p))
        parsed += 1

    pub = load('updates/FJ/PUBLICATION_STATUS.json')
    need(pub['standard_publisher_exit_code'] != 0 and len(pub['individually_validated_new_checkpoints']) == 1, 'publisher boundary')
    for r in pub['inherited_records_preserved']:
        check(r)
        need(sha(r['path']) == hashlib.sha256(git('show', BASE+':'+r['path'])).hexdigest(), 'inherited unsupported schema changed')
    spec = importlib.util.spec_from_file_location('fj_publisher', ROOT / 'state/publish_checkpoint.py')
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    for p in pub['individually_validated_new_checkpoints']:
        x = load(p)
        m.validate_record(x, ROOT)
        need(x['base_revision'] == BASE and x['parent_checkpoint_ids'] == [], 'checkpoint lineage')

    replay = load('updates/FJ/PORTABLE_REPLAY_RECEIPT.json')
    need(replay['status'] == 'PASS' and replay['total_steps'] == 27, 'replay result')
    counts = {}
    for r in replay['groups']:
        check(r)
        receipt = load(r['path'])
        need(receipt['status'] == 'PASS' and len(receipt['checks']) == receipt['expected_steps'] and
             all(x['exit_code'] == 0 for x in receipt['checks']), 'replay group failure')
        need(receipt['published_inputs_hash_unchanged'] and receipt['hashed_original_and_derived_files'] == 200, 'replay source drift')
        counts[receipt['group']] = len(receipt['checks'])
        for log in receipt['checks']:
            need(sha(str(Path(r['path']).parent / log['log'])) == log['log_sha256'], 'replay log drift')
    need(counts == dict(quartic=6,nonlinear=13,physical=6,supporting=2), 'replay scope')

    result = load('updates/FJ/synthesis/root/results/OBSERVATION_CHANNEL_RESULTS.json')
    cert = result['exact_certificate']
    need(result['outputs'] == 8000 and result['every_execution_PDE_node_cap'] == 18572400 and len(result['checks']) == 5, 'root diagnostic scope')
    need([cert[k] for k in ['m','K','Jcap','B','ncap']] == [60,67,22,176880,105], 'exact cap parameters')
    need(Fraction(cert['epsilon_g'])+Fraction(cert['delta']) == Fraction(1,20), 'TV budget')
    need(result['observed']['nodes'] == 8947919 and result['observed']['aborts'] == 0 and 'diagnostic' in result['scope'], 'diagnostic promotion')
    near = load('updates/FJ/synthesis/contact_global/near_contact_checks.json')
    need(near['rotated_line_plus_small_independent_mode']['h_star_over_h_limit'] == '0' and
         near['exact_tangent_resonance']['optimized_gap_limit'] == '111/8', 'compatible control scope')
    hydro = load('updates/FJ/synthesis/hydro_archive_audit/REPLAY_RECEIPT.json')
    need(hydro['execution']['exit_code'] == 0 and hydro['comparison']['grid_points'] == 40804 and
         hydro['comparison']['all_four_floating_diagnostics_differ_only_at_rounding_scale'], 'archive replay scope')
    need('five' in (ROOT / 'updates/FJ/synthesis/root/SCOPE_CLARIFICATIONS.md').read_text(), 'six-label qualification omitted')
    need('already' in (ROOT / 'updates/FJ/synthesis/intervention_schur/DELTA_001_ENERGY_ACCOUNTING.md').read_text(), 'energy correction omitted')
    need((ROOT / 'updates/FJ/synthesis/nonlinear_benchmark/DELTA-001.md').is_file(), 'interval notation correction omitted')
    deployment = load('updates/FJ/synthesis/root/WORKER_DEPLOYMENT.json')
    workers = deployment['initial_workers']
    need(len(workers) == 15 and len({x['agent'] for x in workers}) == 15 and all(
        x['configured_model'] == 'gpt-6-luna' and x['reasoning_effort'] == 'max' and x['fork_turns'] == 'none' for x in workers), 'worker configuration')
    need(deployment['initial_concurrent_running_observation']['all15_observed_running'], 'simultaneous launch evidence')
    for tid in ['T-bounded-correction-observation-channel','T-shunt-qualified-neutral-liquid-isolation']:
        t = load('technology/records/'+tid+'/v0001.json')
        need(t['version'] == 1 and t['stage'] == 'simulation' and any(x['stage'] == 'experiment' and x['decision'] == 'open' for x in t['gates']), 'technology promotion')
    print(json.dumps(dict(status='PASS', base_revision=BASE, main_revision=MAIN,
        original_files=26, original_bytes=259242, derived_files=174, derived_bytes=1083449, indexed_sources=200,
        new_cards=3, scoped_notices=3, paired_bridges=9, new_checkpoints=1, configured_concurrent_luna_max_workers=15,
        portable_replay_steps=27, python_syntax_checks=parsed, scoped_evidence_refs=checked,
        global_checkpoint_validation='Inherited unsupported-schema failure preserved; new checkpoint individually validated.', scientific_truth_checked=False), indent=2))


if __name__ == '__main__':
    main()
