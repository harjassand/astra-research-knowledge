#!/usr/bin/env python3
"""Validate selective intake integrity and gates; never execute archived research."""
import hashlib
import html
import json
from pathlib import Path, PurePosixPath
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from evaluation.workflow_trace import validate as validate_trace
from state.publish_checkpoint import validate_record, views
from technology.validate import validate as validate_technology


def need(condition, message):
    if not condition:
        raise ValueError(message)


def load(path):
    return json.loads((ROOT / path).read_text())


def rows(path):
    return [json.loads(line) for line in (ROOT / path).read_text().splitlines() if line.strip()]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def git(*args):
    return subprocess.check_output(['git', '-C', str(ROOT), *args])


def baseline(base, path):
    return git('show', base + ':' + path)


def main():
    manifest = load('updates/DW/SOURCE_MANIFEST.json')
    claim_map = load('updates/DW/CLAIMS.json')
    base = manifest['intake_base_revision']
    need(base == claim_map['base_revision'], 'intake revision disagreement')
    originals, aliases, excluded = [manifest[k] for k in
                                   ('preserved_files', 'reused_exact_sources', 'exclusions')]
    need((len(originals), len(aliases), len(excluded)) == (36, 107, 1), 'selection changed')
    source_map = {}
    for item in originals + aliases + excluded:
        path = PurePosixPath(item['source_relative_path'])
        need(not path.is_absolute() and '..' not in path.parts, 'unsafe source-relative path')
        need(str(path) not in source_map, 'duplicate source-relative identity')
        source_map[str(path)] = item
    need(len(source_map) == manifest['selection']['source_snapshot_files'] == 144, 'snapshot coverage')
    need(not manifest['selection']['complete_original_output_snapshot_published'], 'exclusion concealed')
    need(excluded[0]['source_relative_path'] == 'diagnostics/technology_latex_compile.json', 'unexpected exclusion')
    for item in originals + aliases:
        data = (ROOT / item['repository_path']).read_bytes()
        need(sha(data) == item['sha256'], 'changed source: ' + item['source_relative_path'])
        need(len(data) == item['bytes'] and len(data.decode('utf-8').splitlines()) == item['lines'],
             'source extent changed: ' + item['source_relative_path'])
    prefix = 'updates/DW/package/frontier_technology_genesis/outputs/'
    actual = {p.relative_to(ROOT).as_posix() for p in (ROOT / prefix).rglob('*') if p.is_file()}
    need(actual == {r['repository_path'] for r in originals}, 'unexpected/missing archived file')
    checksums = (ROOT / (prefix + 'SHA256SUMS.txt')).read_text().splitlines()
    need(len(checksums) == manifest['source_checksum_entries_checked'] == 143, 'checksum count changed')
    for line in checksums:
        digest, path = line.split('  ', 1)
        need(source_map[path]['sha256'] == digest, 'source checksum disagreement: ' + path)
    index = load(prefix + 'proof_index.json')
    for item in index['files']:
        need(item['path'] in source_map and 'repository_path' in source_map[item['path']], 'unrecoverable proof file')
        need(item['sha256'] == source_map[item['path']]['sha256'], 'proof-index hash changed')

    checks = manifest['preservation_checks']
    anchor = b'\\section{Pinned capital and the distinction between sources and deductions}'
    new_report = (ROOT / (prefix + 'research_account.tex')).read_bytes()
    old_report = (ROOT / checks['previous_account_path']).read_bytes()
    need(new_report.count(anchor) == old_report.count(anchor) == 1, 'ambiguous mathematical body anchor')
    new_body, old_body = new_report[new_report.index(anchor):], old_report[old_report.index(anchor):]
    need(new_body == old_body and sha(new_body) == checks['previous_theorem_body_sha256'], 'mathematical body changed')
    old_claims = load(checks['previous_claim_ledger_path'])['claims']
    new_claims = load(prefix + 'claim_ledger.json')['claims']
    need(len(old_claims) == 27 and len(new_claims) == 33 and new_claims[:27] == old_claims, 'prior claim objects changed')

    claim = claim_map['claims'][0]
    cid = claim['id']
    ledgers = {p: rows(p) for p in ('indexes/claims.jsonl', 'frontier/CURRENT_CLAIM_STATUS.jsonl',
                                   'indexes/source_metadata.jsonl', 'web/documents.jsonl')}
    statuses = [r for r in ledgers['frontier/CURRENT_CLAIM_STATUS.jsonl'] if r['card_id'] == cid]
    claims = [r for r in ledgers['indexes/claims.jsonl'] if r['id'] == cid]
    catalog = [r for r in load('indexes/agent_catalog.json')['claims'] if r['id'] == cid]
    need(len(statuses) == len(claims) == len(catalog) == 1, 'claim coverage disagreement')
    status = statuses[0]
    need(status == load('frontier/cards/' + cid + '.json'), 'status sidecar disagreement')
    need(status['claim_status'] == claim['status'] == claims[0]['status'] == 'source_derived_unreviewed', 'status promotion')
    card = (ROOT / status['card_path']).read_bytes()
    need(sha(card) == status['card_sha256'] == catalog[0]['card_sha256'], 'card hash disagreement')
    need((ROOT / ('frontier/review_cards/' + cid + '.txt')).read_bytes().endswith(card), 'wrapper changed card')
    for ref in status['proof_availability']['located_proof_sources'] + status['proof_availability']['available_evidence_sources']:
        data = (ROOT / ref['path']).read_bytes()
        need(sha(data) == ref['sha256'], 'proof reference hash changed')
        need(1 <= ref['lines'][0] <= ref['lines'][1] <= len(data.decode().splitlines()), 'invalid proof/evidence extent')
    need(cid + '\t' in (ROOT / 'agent/routes.tsv').read_text(), 'missing legacy route')
    for topic in status['topics']:
        need(cid + '\t' in (ROOT / ('agent/topics/' + topic + '.tsv')).read_text(), 'missing legacy topic route')
    for item in originals:
        sid = item['source_id']
        metadata = [r for r in ledgers['indexes/source_metadata.jsonl'] if r.get('source_id') == sid]
        docs = [r for r in ledgers['web/documents.jsonl'] if r['id'] == sid]
        need(len(metadata) == len(docs) == 1 and metadata[0]['sha256'] == item['sha256'], 'source route disagreement')
        text = (ROOT / item['repository_path']).read_text()
        need('<pre>' + html.escape(text) + '</pre>' in (ROOT / ('web/' + docs[0]['url'])).read_text(), 'static source text changed')
    gate = [r for r in rows('frontier/OPEN_PROOF_GATES.jsonl') if r['gate_id'] == 'G-DW-POWDER-ACQUISITION']
    need(len(gate) == 1 and gate[0]['status'] == 'open' and cid in gate[0]['card_ids'], 'acquisition gate lost')
    technology = load(claim['technology_record'])
    validate_technology(technology, ROOT)
    need(technology['stage'] == 'model' and not technology['fixture'], 'unjustified readiness')
    need(all(e['kind'] == 'theoretical_derivation' and not e['independence']['attested'] for e in technology['evidence']),
         'invented physical or independent evidence')
    gates = {g['stage']: g for g in technology['gates']}
    need(gates['simulation']['decision'] == gates['experiment']['decision'] == 'open', 'unjustified execution gate')
    trace = load(claim['workflow_trace'])
    validate_trace(trace, ROOT)
    need(trace['prompt_availability'] == 'UNKNOWN' and trace['mode'] == 'UNKNOWN', 'invented prompt/mode')
    need(trace['model']['immutable_version'] is None and all(v is None for v in trace['resources']['usage'].values()),
         'invented model version or measured usage')
    need(trace['resources']['reported_inference_seconds'] is None and trace['resources']['worker_invocations'] is None,
         'invented duration or invocation count')
    need(trace['advance']['verification'] == 'producer_reported' and trace['matched_run_id'] is None, 'unjustified verification/trial')
    cp = load(claim['checkpoint'])
    validate_record(cp, ROOT)
    need(cp['base_revision'] == base and cp['branch_id'] == 'worker-dw-powder-certificate', 'wrong intake checkpoint')
    generated = views(ROOT, {cp['branch_id']: {cp['checkpoint_id']: cp}})
    branch_path = 'state/branches/' + cp['branch_id'] + '.txt'
    need((ROOT / branch_path).read_text() == generated[branch_path], 'stale checkpoint view')
    expected = [r for r in generated['state/branches.tsv'].splitlines() if r.startswith(cp['branch_id'] + '\t')]
    need(len(expected) == 1 and (ROOT / 'state/branches.tsv').read_text().splitlines().count(expected[0]) == 1, 'registry disagreement')

    # Compare actual historical bytes and graph/ledger prefixes against the pinned intake base.
    for path in list(ledgers) + ['frontier/OPEN_PROOF_GATES.jsonl', 'state/branches.tsv', 'agent/routes.tsv']:
        need((ROOT / path).read_bytes().startswith(baseline(base, path)), 'historical rows rewritten: ' + path)
    for path, fields in [('indexes/agent_catalog.json', ['claims']), ('indexes/agent_graph.json', ['nodes', 'edges'])]:
        old, now = json.loads(baseline(base, path)), load(path)
        for field in fields:
            need(now[field][:len(old[field])] == old[field], 'historical graph/catalog rewritten')
    graph = load('indexes/agent_graph.json')
    nodes = {n['id'] for n in graph['nodes']}
    need(len(nodes) == len(graph['nodes']) and all(e['from'] in nodes and e['to'] in nodes for e in graph['edges']), 'invalid graph')
    old_paths = set(git('ls-tree', '-r', '--name-only', base).decode().splitlines())
    changed = set(git('diff', '--name-only', base, '--', 'updates', 'cards', 'state/checkpoints', 'state/branches',
                      'evaluation', 'technology/records').decode().splitlines())
    need(not (changed & old_paths), 'historical source/card/checkpoint/evaluation/technology record changed')
    old_outputs = json.loads(baseline(base, 'agent/access_manifest.json'))['outputs']
    need(all((ROOT / path).is_file() for path in old_outputs), 'historical route disappeared')
    scientific = {p: digest for p, digest in old_outputs.items() if p.startswith(
        ('frontier/dossiers/', 'frontier/connections/', 'frontier/proof_ranges/'))}
    need(all(sha((ROOT / p).read_bytes()) == digest for p, digest in scientific.items()), 'old scientific route changed')
    print(json.dumps({'intake': 'DW', 'status': 'PASS', 'new_originals': len(originals),
                      'new_original_bytes': sum(r['bytes'] for r in originals), 'exact_aliases': len(aliases),
                      'excluded': len(excluded), 'proof_index_files': len(index['files']),
                      'prior_claims_preserved': 27, 'mathematical_body_byte_equal': True,
                      'historical_scientific_routes_unchanged': len(scientific), 'technology_stage': 'model',
                      'record_level_checkpoints': 1, 'baseline_revision': base,
                      'scientific_verification': 'not performed', 'experiments_executed': 0}, sort_keys=True))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, KeyError, subprocess.CalledProcessError) as error:
        raise SystemExit(str(error))
