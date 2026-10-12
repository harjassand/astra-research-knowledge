#!/usr/bin/env python3
"""Validate DZ source preservation and scoped routes; never execute research code."""
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
    return [json.loads(x) for x in (ROOT / path).read_text().splitlines() if x.strip()]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def git(*args):
    return subprocess.check_output(['git', '-C', str(ROOT), *args])


def main():
    manifest = load('updates/DZ/SOURCE_MANIFEST.json')
    claim_map = load('updates/DZ/CLAIMS.json')
    base = manifest['intake_base_revision']
    need(base == claim_map['base_revision'], 'intake revision disagreement')
    originals, aliases, excluded = [manifest[k] for k in
                                   ('preserved_files', 'reused_exact_sources', 'exclusions')]
    need((len(originals), len(aliases), len(excluded)) == (35, 143, 2), 'selection changed')
    source_map = {}
    for item in originals + aliases + excluded:
        name = PurePosixPath(item['source_relative_path'])
        need(not name.is_absolute() and '..' not in name.parts, 'unsafe relative path')
        need(str(name) not in source_map, 'duplicate relative source identity')
        source_map[str(name)] = item
    need(len(source_map) == manifest['selection']['source_snapshot_files'] == 180, 'snapshot coverage')
    need(not manifest['selection']['complete_original_output_snapshot_published'], 'exclusions concealed')
    need({r['source_relative_path'] for r in excluded} ==
         {'diagnostics/high_leverage_latex_compile.json', 'diagnostics/technology_latex_compile.json'}, 'unexpected exclusion')
    for item in originals + aliases:
        data = (ROOT / item['repository_path']).read_bytes()
        need(sha(data) == item['sha256'], 'changed original/alias: ' + item['source_relative_path'])
        need(len(data) == item['bytes'] and len(data.decode().splitlines()) == item['lines'], 'source extent changed')
    prefix = 'updates/DZ/package/high_leverage_invention/outputs/'
    actual = {p.relative_to(ROOT).as_posix() for p in (ROOT / prefix).rglob('*') if p.is_file()}
    need(actual == {r['repository_path'] for r in originals}, 'unexpected/missing archived file')
    checksums = (ROOT / (prefix + 'SHA256SUMS.txt')).read_text().splitlines()
    need(len(checksums) == manifest['source_checksum_entries_checked'] == 179, 'checksum count changed')
    for line in checksums:
        digest, path = line.split(None, 1)
        need(source_map[path.strip().lstrip('*')]['sha256'] == digest, 'source checksum disagreement')
    index = load(prefix + 'proof_index.json')
    for item in index['files']:
        need(item['path'] in source_map and 'repository_path' in source_map[item['path']], 'unrecoverable proof')
        need(item['sha256'] == source_map[item['path']]['sha256'], 'proof-index hash disagreement')
    prior = load('updates/DW/SOURCE_MANIFEST.json')
    old_by_rel = {r['source_relative_path']: r for r in prior['preserved_files'] + prior['reused_exact_sources']}
    for rel in ['research_account.tex', 'claim_ledger.json', 'research_state.json', 'source_manifest.json',
                'proof_index.json', 'READ_ME.txt', 'SHA256SUMS.txt']:
        need(source_map['history/phase3/' + rel]['sha256'] == old_by_rel[rel]['sha256'], 'phase-three history changed')
    old_claims = load(manifest['preservation_checks']['previous_claim_ledger_path'])['claims']
    new_claims = load(prefix + 'claim_ledger.json')['claims']
    need(len(old_claims) == 33 and len(new_claims) == 39 and new_claims[:33] == old_claims, 'prior claim objects changed')
    need([c['id'] for c in new_claims[33:]] == ['HL1', 'HL2', 'HL3', 'HL4', 'HL5', 'HL6'], 'source claim identities changed')
    need('history/phase3/research_account.tex' in index['prior_report_reference_resolution'], 'old report references misresolved')

    ledgers = {p: rows(p) for p in ['indexes/claims.jsonl', 'frontier/CURRENT_CLAIM_STATUS.jsonl',
                                  'indexes/source_metadata.jsonl', 'web/documents.jsonl']}
    graph = load('indexes/agent_graph.json')
    nodes = {n['id'] for n in graph['nodes']}
    need(len(nodes) == len(graph['nodes']) and all(e['from'] in nodes and e['to'] in nodes for e in graph['edges']), 'graph integrity')
    for item in originals:
        sid = item['source_id']
        metadata = [r for r in ledgers['indexes/source_metadata.jsonl'] if r.get('source_id') == sid]
        docs = [r for r in ledgers['web/documents.jsonl'] if r['id'] == sid]
        need(len(metadata) == len(docs) == 1 and metadata[0]['sha256'] == item['sha256'], 'source route disagreement')
        text = (ROOT / item['repository_path']).read_text()
        need('<pre>' + html.escape(text) + '</pre>' in (ROOT / ('web/' + docs[0]['url'])).read_text(), 'static source changed')
    need(len(claim_map['claims']) == 3, 'claim family coverage')
    catalog = load('indexes/agent_catalog.json')['claims']
    for claim in claim_map['claims']:
        cid = claim['id']
        current = [r for r in ledgers['frontier/CURRENT_CLAIM_STATUS.jsonl'] if r['card_id'] == cid]
        entries = [r for r in ledgers['indexes/claims.jsonl'] if r['id'] == cid]
        cat = [r for r in catalog if r['id'] == cid]
        need(len(current) == len(entries) == len(cat) == 1, 'family coverage disagreement')
        status = current[0]
        need(status == load('frontier/cards/' + cid + '.json'), 'sidecar disagreement')
        need(status['claim_status'] == entries[0]['status'] == claim['status'] == 'source_derived_unreviewed', 'status promotion')
        card = (ROOT / status['card_path']).read_bytes()
        need(sha(card) == status['card_sha256'] == cat[0]['card_sha256'], 'card hash disagreement')
        need((ROOT / ('frontier/review_cards/' + cid + '.txt')).read_bytes().endswith(card), 'wrapper changed card')
        for ref in status['proof_availability']['located_proof_sources'] + status['proof_availability']['available_evidence_sources']:
            data = (ROOT / ref['path']).read_bytes()
            need(sha(data) == ref['sha256'], 'proof/evidence hash disagreement')
            need(1 <= ref['lines'][0] <= ref['lines'][1] <= len(data.decode().splitlines()), 'invalid proof range')
        need(cid + '\t' in (ROOT / 'agent/routes.tsv').read_text(), 'missing legacy route')
        for topic in status['topics']:
            need(cid + '\t' in (ROOT / ('agent/topics/' + topic + '.tsv')).read_text(), 'missing topic route')
        need(any(cid in g['card_ids'] and g['status'] == 'open' for g in rows('frontier/OPEN_PROOF_GATES.jsonl')), 'review gate lost')
        if claim['technology_record']:
            technology = load(claim['technology_record'])
            validate_technology(technology, ROOT)
            need(technology['stage'] == 'model' and not technology['fixture'], 'unjustified readiness')
            need(all(e['kind'] == 'theoretical_derivation' and not e['independence']['attested'] for e in technology['evidence']), 'invented physical/independent evidence')
            gates = {g['stage']: g for g in technology['gates']}
            need(gates['simulation']['decision'] == gates['experiment']['decision'] == 'open', 'unjustified test gate')
    trace = load(claim_map['workflow_trace'])
    validate_trace(trace, ROOT)
    need(trace['prompt_availability'] == trace['mode'] == 'UNKNOWN', 'invented prompt/mode')
    need(all(v is None for v in trace['model'].values()), 'single model configuration inferred from mixed-worker source')
    need(all(v is None for v in trace['resources']['usage'].values()) and
         trace['resources']['reported_inference_seconds'] is None and trace['resources']['worker_invocations'] is None, 'diagnostic time/roles promoted to actual research usage')
    need(trace['advance']['verification'] == 'producer_reported' and trace['matched_run_id'] is None, 'invented verification/trial')
    cp = load(claim_map['checkpoint'])
    validate_record(cp, ROOT)
    need(cp['base_revision'] == base and cp['parent_checkpoint_ids'] == [], 'invented intake ancestry')
    generated = views(ROOT, {cp['branch_id']: {cp['checkpoint_id']: cp}})
    path = 'state/branches/' + cp['branch_id'] + '.txt'
    need((ROOT / path).read_text() == generated[path], 'stale checkpoint view')
    expected = [r for r in generated['state/branches.tsv'].splitlines() if r.startswith(cp['branch_id'] + '\t')]
    need(len(expected) == 1 and (ROOT / 'state/branches.tsv').read_text().splitlines().count(expected[0]) == 1, 'registry disagreement')

    for path in list(ledgers) + ['frontier/OPEN_PROOF_GATES.jsonl', 'state/branches.tsv', 'agent/routes.tsv']:
        need((ROOT / path).read_bytes().startswith(git('show', base + ':' + path)), 'historical rows rewritten: ' + path)
    for path, fields in [('indexes/agent_catalog.json', ['claims']), ('indexes/agent_graph.json', ['nodes', 'edges'])]:
        old, now = json.loads(git('show', base + ':' + path)), load(path)
        for field in fields:
            need(now[field][:len(old[field])] == old[field], 'historical graph/catalog rewritten')
    old_paths = set(git('ls-tree', '-r', '--name-only', base).decode().splitlines())
    changed = set(git('diff', '--name-only', base, '--', 'updates', 'cards', 'state/checkpoints', 'state/branches',
                      'evaluation', 'technology/records').decode().splitlines())
    need(not (changed & old_paths), 'historical source/card/checkpoint/evaluation/technology record changed')
    old_outputs = json.loads(git('show', base + ':agent/access_manifest.json'))['outputs']
    need(all((ROOT / path).is_file() for path in old_outputs), 'historical route disappeared')
    scientific = {p: digest for p, digest in old_outputs.items() if p.startswith(
        ('frontier/dossiers/', 'frontier/connections/', 'frontier/proof_ranges/'))}
    need(all(sha((ROOT / p).read_bytes()) == digest for p, digest in scientific.items()), 'old scientific route changed')
    print(json.dumps({'intake': 'DZ', 'status': 'PASS', 'new_originals': len(originals),
                      'new_original_bytes': sum(r['bytes'] for r in originals), 'exact_aliases': len(aliases),
                      'excluded': len(excluded), 'checksum_entries': len(checksums), 'proof_index_files': len(index['files']),
                      'prior_claim_objects_preserved': 33, 'previous_complete_report_byte_equal': True,
                      'old_scientific_routes_unchanged': len(scientific), 'research_cards': 3,
                      'technology_records_at_model_stage': 2, 'workflow_campaigns': 1,
                      'record_level_checkpoints': 1, 'baseline_revision': base,
                      'scientific_verification': 'not performed', 'experiments_executed': 0}, sort_keys=True))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, KeyError, subprocess.CalledProcessError) as error:
        raise SystemExit(str(error))
