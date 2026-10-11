#!/usr/bin/env python3
"""Check DX preservation and routing only; never execute the archived research."""
import hashlib
import html
import json
from pathlib import Path
import subprocess
import sys
import stat
from zipfile import ZipFile
from pathlib import PurePosixPath

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from evaluation.workflow_trace import validate as validate_trace
from state.publish_checkpoint import validate_record, views


def need(condition, message):
    if not condition:
        raise ValueError(message)


def load(path):
    return json.loads((ROOT / path).read_text())


def sha(data):
    return hashlib.sha256(data).hexdigest()


def rows(path):
    return [json.loads(line) for line in (ROOT / path).read_text().splitlines() if line.strip()]


def base_bytes(base, path):
    return subprocess.check_output(['git', '-C', str(ROOT), 'show', base + ':' + path])


def main(intake='DX', expected_count=1, expected_bytes=21404):
    manifest = load(f'updates/{intake}/SOURCE_MANIFEST.json')
    claim_map = load(f'updates/{intake}/CLAIMS.json')
    base = manifest['intake_base_revision']
    need(base == claim_map['base_revision'], 'intake revision disagreement')
    need(len(manifest['originals']) == len(claim_map['claims']) == expected_count, 'missing source family')
    indexes = {path: rows(path) for path in ['indexes/claims.jsonl', 'frontier/CURRENT_CLAIM_STATUS.jsonl',
                                            'indexes/source_metadata.jsonl', 'web/documents.jsonl']}
    catalog = load('indexes/agent_catalog.json')['claims']
    graph = load('indexes/agent_graph.json')
    nodes = {node['id'] for node in graph['nodes']}
    need(len(nodes) == len(graph['nodes']), 'duplicate graph node')
    need(all(e['from'] in nodes and e['to'] in nodes for e in graph['edges']), 'missing graph endpoint')
    gates = rows('frontier/OPEN_PROOF_GATES.jsonl')
    totals = 0
    cp_records = {}
    for source, claim in zip(manifest['originals'], claim_map['claims']):
        path = source['path']
        data = (ROOT / path).read_bytes()
        text = data.decode('utf-8')
        lines = text.splitlines()
        need(sha(data) == source['sha256'] == claim['source_sha256'], 'changed source: ' + path)
        need(len(data) == source['bytes'] and len(lines) == source['lines'], 'source extent changed')
        totals += len(data)
        for bounds in [source['initiating_prompt_lines'], source['reported_duration']['lines'], source['final_report_lines']]:
            need(1 <= bounds[0] <= bounds[1] <= len(lines), 'invalid source range')
        a, b = source['reported_duration']['lines']
        display = '\n'.join(lines[a-1:b])
        seconds = source['reported_duration']['seconds']
        need(display == f'Worked for {seconds // 60}m {seconds % 60}s', 'duration not linked to exact display')
        cid = claim['id']
        matching = [r for r in indexes['indexes/claims.jsonl'] if r['id'] == cid]
        statuses = [r for r in indexes['frontier/CURRENT_CLAIM_STATUS.jsonl'] if r['card_id'] == cid]
        entries = [r for r in catalog if r['id'] == cid]
        need(len(matching) == len(statuses) == len(entries) == 1, 'coverage disagreement: ' + cid)
        status = statuses[0]
        need(load('frontier/cards/' + cid + '.json') == status, 'status sidecar disagrees')
        card = (ROOT / status['card_path']).read_bytes()
        need(sha(card) == status['card_sha256'] == entries[0]['card_sha256'], 'card hash disagreement')
        need(status['claim_status'] == matching[0]['status'] == claim['status'] == 'source_derived_unreviewed',
             'unjustified scientific-status promotion')
        need((ROOT / ('frontier/review_cards/' + cid + '.txt')).read_bytes().endswith(card), 'wrapper changed card')
        need(any(cid in gate['card_ids'] and gate['status'] == 'open' for gate in gates), 'missing open review gate')
        need(cid + '\t' in (ROOT / 'agent/routes.tsv').read_text(), 'missing legacy route')
        for topic in status['topics']:
            need(cid + '\t' in (ROOT / ('agent/topics/' + topic + '.tsv')).read_text(), 'missing legacy topic route')
        for ref in status['proof_availability']['located_proof_sources']:
            refdata = (ROOT / ref['path']).read_bytes()
            allowed = {path} | {m['path'] for p in manifest.get('recovered_packages', []) for m in p['members']}
            need(ref['path'] in allowed and ref['sha256'] == sha(refdata), 'wrong proof source')
            need(1 <= ref['lines'][0] <= ref['lines'][1] <= len(refdata.decode().splitlines()), 'invalid proof range')
        sid = source['source_id']
        need(matching[0]['source_ids'] == [sid], 'source identity changed')
        metadata = [r for r in indexes['indexes/source_metadata.jsonl'] if r.get('source_id') == sid]
        docs = [r for r in indexes['web/documents.jsonl'] if r['id'] == sid]
        need(len(metadata) == len(docs) == 1, 'missing static source route')
        need(metadata[0]['sha256'] == sha(data), 'source metadata hash mismatch')
        page = (ROOT / ('web/' + docs[0]['url'])).read_text()
        need('<pre>' + html.escape(text) + '</pre>' in page, 'static source text changed')
        trace = load(claim['workflow_trace'])
        validate_trace(trace, ROOT)
        need(trace['resources']['reported_inference_seconds'] == seconds, 'trace duration disagreement')
        need(all(v is None for v in trace['model'].values()), 'unobserved model data')
        need(all(v is None for v in trace['resources']['usage'].values()), 'unobserved usage data')
        need(trace['resources']['worker_invocations'] is None and trace['matched_run_id'] is None,
             'invented worker usage or matched trial')
        need(trace['advance']['verification'] == 'producer_reported' and trace['advance']['verification_receipt'] is None,
             'unjustified independent verification')
        cp = load(claim['checkpoint'])
        validate_record(cp, ROOT)
        need(cp['base_revision'] == base and cp['parent_checkpoint_ids'] == [], 'intake ancestry changed')
        need(cp['branch_id'].startswith('worker-' + intake.lower() + '-'), 'active research branch changed')
        cp_records[cp['branch_id']] = {cp['checkpoint_id']: cp}
        need(any(e['from'] == cid and e['to'] == sid and e['kind'] == 'provenance' for e in graph['edges']),
             'missing provenance graph edge')
    need(totals == expected_bytes, 'attachment size changed')
    need(all(not (ROOT / x['path']).read_bytes().endswith(b'\n') for x in manifest['originals']),
         'original final byte changed')
    packages = manifest.get('recovered_packages', [])
    need(len(packages) == 1, 'recovered package inventory changed')
    for package in packages:
        archive = (ROOT / package['archive_path']).read_bytes()
        need(sha(archive) == package['sha256'] and len(archive) == package['bytes'], 'archive bytes changed')
        with ZipFile(ROOT / package['archive_path']) as z:
            names = [x.filename for x in z.infolist()]
            need(len(names) == len(set(names)) == len(package['members']), 'duplicate or omitted archive member')
            need(names == [m['archive_member'] for m in package['members']], 'archive inventory mismatch')
            need(z.testzip() is None, 'archive CRC failure')
            for info, member in zip(z.infolist(), package['members']):
                name = PurePosixPath(info.filename)
                need(not name.is_absolute() and '..' not in name.parts and '\\' not in info.filename
                     and not stat.S_ISLNK(info.external_attr >> 16), 'unsafe archive member')
                original = z.read(info)
                need((ROOT / member['path']).read_bytes() == original, 'extracted original changed')
                need(sha(original) == member['sha256'] and len(original) == member['bytes'], 'member hash changed')
                if 'lines' in member:
                    need(len(original.decode().splitlines()) == member['lines'], 'member line count changed')
                metadata = [r for r in indexes['indexes/source_metadata.jsonl'] if r.get('source_id') == member['source_id']]
                need(len(metadata) == 1 and metadata[0]['sha256'] == member['sha256'], 'missing member source metadata')
                doc = [r for r in indexes['web/documents.jsonl'] if r['id'] == member['source_id']]
                need(len(doc) == 1, 'missing recovered-member web route')
                if 'lines' in member:
                    page = (ROOT / ('web/' + doc[0]['url'])).read_text()
                    need('<pre>' + html.escape(original.decode()) + '</pre>' in page, 'recovered static source changed')
            if intake == 'DY':
                declared = json.loads(z.read('astra_thermal_response/manifest.json'))['files']
                for name, value in declared.items():
                    data = z.read('astra_thermal_response/' + name)
                    need(sha(data) == value['sha256'] and len(data) == value['bytes'], 'producer manifest mismatch')
    if intake == 'DX':
        source = manifest['originals'][0]
        need(source['lines'] == 190 and source['reported_duration']['seconds'] == 2672, 'source display changed')
        need(len(source['referenced_but_not_supplied']) == 2, 'remaining review/backend gates changed')
        trace = load(claim_map['claims'][0]['workflow_trace'])
        need(trace['mode'] == 'fresh_direction_retained_context' and trace['context']['conversation_relation'] == 'same',
             'initiating intervention changed')
        need(claim_map['claims'][0]['id'].startswith('N703-'), 'stable claim identity changed')
    else:
        need([s['reported_duration']['seconds'] for s in manifest['originals']] == [2964, 2949], 'reported duration changed')
        need([load(c['workflow_trace'])['mode'] for c in claim_map['claims']] ==
             ['targeted_warm_continuation', 'independent_selective_capital'], 'workflow intervention changed')
        n704 = next(c for c in claim_map['claims'] if c['id'].startswith('N704-'))
        dependency = 'N701-activity-sensitive-loss-complete-lindblad-simulation'
        need(any(e['from'] == n704['id'] and e['to'] == dependency and e['kind'] == 'dependency'
                 for e in graph['edges']), 'missing inherited first-event proof gate')
    generated = views(ROOT, cp_records)
    registry = (ROOT / 'state/branches.tsv').read_text().splitlines()
    for branch in cp_records:
        path = 'state/branches/' + branch + '.txt'
        need((ROOT / path).read_text() == generated[path], 'stale new checkpoint view')
        expected = [r for r in generated['state/branches.tsv'].splitlines() if r.startswith(branch + '\t')]
        need(len(expected) == 1 and registry.count(expected[0]) == 1, 'missing new registry row')

    # Full baseline comparisons preserve all historical scientific claims, source
    # records, graph entries, registered outcomes and checkpoint bytes. Generated
    # concept/recent indexes may extend; no old branch objective is rewritten.
    for path in list(indexes) + ['frontier/OPEN_PROOF_GATES.jsonl', 'state/branches.tsv', 'agent/routes.tsv']:
        old = base_bytes(base, path)
        need((ROOT / path).read_bytes().startswith(old), 'historical rows rewritten: ' + path)
    for path in ['indexes/agent_catalog.json', 'indexes/agent_graph.json', 'web/catalog.json',
                 'indexes/external_dependencies.json']:
        old = json.loads(base_bytes(base, path))
        now = load(path)
        if path.endswith('agent_catalog.json'):
            need(now['claims'][:len(old['claims'])] == old['claims'], 'old catalog claims changed')
        elif path.endswith('agent_graph.json'):
            for field in ['nodes', 'edges']:
                need(now[field][:len(old[field])] == old[field], 'old graph records changed')
        else:
            need(now[:len(old)] == old, 'old public records changed: ' + path)
    changed = subprocess.check_output(['git', '-C', str(ROOT), 'diff', '--name-only', base, '--',
                                      'cards', 'state/checkpoints', 'state/branches', 'evaluation/FROZEN_TASKS.jsonl',
                                      'evaluation/MODEL_COMPARISONS.jsonl', 'evaluation/VERIFIED_OUTCOMES.jsonl', 'updates'], text=True).splitlines()
    old_paths = set(subprocess.check_output(['git', '-C', str(ROOT), 'ls-tree', '-r', '--name-only', base], text=True).splitlines())
    need(not (set(changed) & old_paths), 'historical card/checkpoint/view/evaluation bytes changed')
    old_routes = json.loads(base_bytes(base, 'agent/access_manifest.json'))['outputs']
    need(all((ROOT / path).is_file() for path in old_routes), 'an existing navigation route disappeared')
    scientific = {p: digest for p, digest in old_routes.items() if p.startswith(
        ('frontier/dossiers/', 'frontier/connections/', 'frontier/proof_ranges/'))}
    changed_routes = {p for p, digest in scientific.items() if sha((ROOT / p).read_bytes()) != digest}
    need(changed_routes == {'frontier/connections/N701.json'}, 'unexpected historical scientific route change')
    # The sole allowed extension is the explicit N704 -> N701 inherited proof
    # dependency. Every old edge/node and all claim/status/proof data remain exact.
    old = json.loads(base_bytes(base, 'frontier/connections/N701.json'))
    current = load('frontier/connections/N701.json')
    for field in set(old) - {'snapshot', 'edges', 'nodes'}:
        need(current[field] == old[field], 'N701 scientific claim/status changed')
    need(all(x in current['edges'] for x in old['edges']) and all(x in current['nodes'] for x in old['nodes']),
         'N701 historical connection removed')
    added_edges = [x for x in current['edges'] if x not in old['edges']]
    added_nodes = [x for x in current['nodes'] if x not in old['nodes']]
    n704 = 'N704-excitation-budget-coherent-collective-emission-simulation'
    n701 = 'N701-activity-sensitive-loss-complete-lindblad-simulation'
    need(len(added_edges) == 1 and added_edges[0]['from'] == n704 and added_edges[0]['to'] == n701
         and added_edges[0]['kind'] == 'dependency' and 'unreviewed' in added_edges[0]['composition'],
         'unscoped N701 connection extension')
    need(added_nodes == [{'id': n704, 'node_kind': 'claim'}], 'unexpected N701 connection node')
    print(json.dumps({'intake':intake,'status':'PASS','originals':expected_count,'original_bytes':totals,'cards':expected_count,
                      'workflow_traces':expected_count,'record_level_checkpoints':expected_count,'recovered_archives':len(packages),'baseline_revision':base,
                      'historical_records_preserved':True,'historical_route_extension':'N704 -> N701 scoped dependency only','scientific_verification':'not performed',
                      'global_checkpoint_validation':'separate; known pre-existing malformed records remain'}, sort_keys=True))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, KeyError, subprocess.CalledProcessError) as error:
        raise SystemExit(str(error))
