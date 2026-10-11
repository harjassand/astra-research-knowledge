#!/usr/bin/env python3
"""Check EA archival provenance and routing; never execute archived research code."""
import hashlib
import html
import json
from pathlib import Path, PurePosixPath
import stat
import subprocess
import sys
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from evaluation.workflow_trace import validate as validate_trace
from state.publish_checkpoint import validate_record, views


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


def main():
    manifest = load('updates/EA/SOURCE_MANIFEST.json')
    claim_map = load('updates/EA/CLAIMS.json')
    base = manifest['intake_base_revision']
    need(base == claim_map['base_revision'] == 'c470169c2bffd6f5353ee5d3b0207c56d9f4c288', 'base revision changed')
    need(manifest['source_handling'] == 'source=DATA', 'archived instructions promoted')
    need(len(manifest['originals']) == len(manifest['recovered_packages']) == len(claim_map['claims']) == 1, 'research-attempt coverage changed')
    original = manifest['originals'][0]
    data = (ROOT / original['path']).read_bytes()
    need(sha(data) == original['sha256'] == 'd8d5fee0c27f020c3bd55922c6a17d006909ae5d0c5d4a0c1cf116621e3cce1c', 'pasted original changed')
    need(len(data) == original['bytes'] == 24125 and len(data.decode().splitlines()) == original['lines'] == 241, 'paste extent changed')
    need(original['initiating_prompt_lines'] == [1,14] and original['final_report_lines'] == [45,241], 'prompt/output boundary changed')
    need(original['reported_duration']['seconds'] == 2773 and original['reported_duration']['lines'] == [15,15], 'reported duration changed')
    package = manifest['recovered_packages'][0]
    archive = (ROOT / package['archive_path']).read_bytes()
    need(sha(archive) == package['sha256'] == 'c081712dfa0337953a23bf53a2b1e8d84eaae40a1d0ab7f5186f5ce8fc38220d', 'original ZIP changed')
    need(len(archive) == package['bytes'] == 23571 and len(package['members']) == 12, 'ZIP extent changed')
    with ZipFile(ROOT / package['archive_path']) as z:
        need(z.testzip() is None, 'ZIP CRC failure')
        need(len(z.namelist()) == len(set(z.namelist())) == 12, 'duplicate/extra archive member')
        need(set(z.namelist()) == {m['archive_member'] for m in package['members']}, 'member coverage disagreement')
        for info in z.infolist():
            path = PurePosixPath(info.filename)
            need(not path.is_absolute() and '..' not in path.parts and '\\' not in info.filename and
                 not info.is_dir() and not stat.S_ISLNK(info.external_attr >> 16), 'unsafe archive path')
        for member in package['members']:
            data = (ROOT / member['path']).read_bytes()
            need(data == z.read(member['archive_member']), 'extracted original changed')
            need(sha(data) == member['sha256'] and len(data) == member['bytes'] and
                 len(data.decode().splitlines()) == member['lines'], 'member identity disagreement')
        producer = json.loads(z.read('astra_hidden_memory/MANIFEST.json'))
        need(len(producer) == 11, 'producer manifest coverage changed')
        for name, expected in producer.items():
            data = z.read('astra_hidden_memory/' + name)
            need(sha(data) == expected['sha256'] and len(data) == expected['bytes'], 'producer manifest disagreement')
    files = {p.relative_to(ROOT).as_posix() for p in (ROOT / 'updates/EA/package').rglob('*') if p.is_file()}
    need(files == {original['path'], package['archive_path']} | {m['path'] for m in package['members']}, 'untracked package disclosure/missing original')
    ledgers = {p: rows(p) for p in ['indexes/claims.jsonl', 'frontier/CURRENT_CLAIM_STATUS.jsonl',
                                  'indexes/source_metadata.jsonl', 'web/documents.jsonl']}
    all_sources = [original] + package['members'] + [dict(path=package['archive_path'], **{k:package[k] for k in ['source_id','sha256','bytes']})]
    for item in all_sources:
        sid = item['source_id']
        metadata = [r for r in ledgers['indexes/source_metadata.jsonl'] if r.get('source_id') == sid]
        documents = [r for r in ledgers['web/documents.jsonl'] if r['id'] == sid]
        need(len(metadata) == len(documents) == 1 and metadata[0]['sha256'] == item['sha256'], 'source route disagreement')
        need(metadata[0]['path'] == documents[0]['path'] == item['path'], 'source path disagreement')
        if item['path'] == package['archive_path']:
            need(documents[0]['extraction'] == 'original_binary' and documents[0]['url'] == '../' + item['path'], 'binary source misrendered')
        else:
            text = (ROOT / item['path']).read_text()
            need('<pre>' + html.escape(text) + '</pre>' in (ROOT / ('web/' + documents[0]['url'])).read_text(), 'static original changed')
    entry = claim_map['claims'][0]
    cid = entry['id']
    need(cid == 'N709-hidden-observation-ladder-passive-active-separation', 'stable ID changed')
    current = [r for r in ledgers['frontier/CURRENT_CLAIM_STATUS.jsonl'] if r['card_id'] == cid]
    claims = [r for r in ledgers['indexes/claims.jsonl'] if r['id'] == cid]
    catalog = [r for r in load('indexes/agent_catalog.json')['claims'] if r['id'] == cid]
    need(len(current) == len(claims) == len(catalog) == 1, 'claim coverage disagreement')
    status = current[0]
    need(status == load('frontier/cards/' + cid + '.json'), 'sidecar disagreement')
    need(status['claim_status'] == claims[0]['status'] == entry['status'] == 'source_derived_unreviewed', 'scientific status promoted')
    need(status['depends_on'] == claims[0]['depends_on'] == [], 'topical/imported dependency invented')
    card = (ROOT / status['card_path']).read_bytes()
    need(sha(card) == status['card_sha256'] == catalog[0]['card_sha256'], 'card identity disagreement')
    need((ROOT / ('frontier/review_cards/' + cid + '.txt')).read_bytes().endswith(card), 'review wrapper changed original card')
    need(set(claims[0]['source_ids']) == {r['source_id'] for r in all_sources}, 'claim sources incomplete')
    for ref in status['proof_availability']['located_proof_sources'] + status['proof_availability']['available_evidence_sources']:
        data = (ROOT / ref['path']).read_bytes()
        need(sha(data) == ref['sha256'] and 1 <= ref['lines'][0] <= ref['lines'][1] <= len(data.decode().splitlines()), 'invalid proof/evidence range')
    need(len(status['proof_availability']['located_proof_sources']) == 11, 'proof-route coverage changed')
    need(cid + '\t' in (ROOT / 'agent/routes.tsv').read_text(), 'legacy route missing')
    for topic in status['topics']:
        need(cid + '\t' in (ROOT / ('agent/topics/' + topic + '.tsv')).read_text(), 'topic route missing')
    need(any(cid in g['card_ids'] and g['status'] == 'open' for g in rows('frontier/OPEN_PROOF_GATES.jsonl')), 'independent-review gate missing')
    graph = load('indexes/agent_graph.json')
    nodes = {n['id'] for n in graph['nodes']}
    need(len(nodes) == len(graph['nodes']) and all(e['from'] in nodes and e['to'] in nodes for e in graph['edges']), 'graph integrity failure')
    need({r['source_id'] for r in all_sources} <= {e['to'] for e in graph['edges'] if e['from'] == cid and e['kind'] == 'provenance'}, 'provenance graph incomplete')
    trace = load(entry['workflow_trace'])
    validate_trace(trace, ROOT)
    need(trace['mode'] == 'fresh_direction_retained_context' and trace['context']['conversation_relation'] == 'same' and trace['prompt_availability'] == 'exact', 'research mode invented/lost')
    need(all(v is None for v in trace['model'].values()) and all(v is None for v in trace['resources']['usage'].values()) and
         trace['resources']['worker_invocations'] is None, 'model/usage telemetry invented')
    need(trace['resources']['reported_inference_seconds'] == 2773 and trace['advance']['verification'] == 'producer_reported' and trace['matched_run_id'] is None, 'duration or verification promoted')
    cp = load(entry['checkpoint'])
    validate_record(cp, ROOT)
    need(cp['base_revision'] == base and cp['parent_checkpoint_ids'] == [], 'intake ancestry invented')
    generated = views(ROOT, {cp['branch_id']:{cp['checkpoint_id']:cp}})
    view_path = 'state/branches/' + cp['branch_id'] + '.txt'
    need((ROOT / view_path).read_text() == generated[view_path], 'new checkpoint view stale')
    row = next(r for r in generated['state/branches.tsv'].splitlines() if r.startswith(cp['branch_id'] + '\t'))
    need((ROOT / 'state/branches.tsv').read_text().splitlines().count(row) == 1, 'checkpoint registry disagreement')
    for path in list(ledgers) + ['frontier/OPEN_PROOF_GATES.jsonl', 'state/branches.tsv', 'agent/routes.tsv']:
        need((ROOT / path).read_bytes().startswith(git('show', base + ':' + path)), 'historical ledger rows rewritten: ' + path)
    for path, fields in [('indexes/agent_catalog.json',['claims']), ('indexes/agent_graph.json',['nodes','edges'])]:
        old, now = json.loads(git('show', base + ':' + path)), load(path)
        for field in fields:
            need(now[field][:len(old[field])] == old[field], 'historical graph/catalog changed')
    old_paths = set(git('ls-tree', '-r', '--name-only', base).decode().splitlines())
    changed = set(git('diff', '--name-only', base, '--', 'updates', 'cards', 'state/checkpoints', 'state/branches', 'evaluation', 'technology/records').decode().splitlines())
    need(not (changed & old_paths), 'historical scientific source/card/checkpoint/record changed')
    old_outputs = json.loads(git('show', base + ':agent/access_manifest.json'))['outputs']
    scientific = {p:d for p,d in old_outputs.items() if p.startswith(('frontier/dossiers/','frontier/connections/','frontier/proof_ranges/'))}
    need(all((ROOT / p).is_file() and sha((ROOT / p).read_bytes()) == d for p,d in scientific.items()), 'old scientific route changed')
    print(json.dumps(dict(intake='EA', status='PASS', original_pastes=1, original_archive_members=12,
                          source_routes=len(all_sources), proof_ranges=11, research_attempts=1,
                          old_scientific_routes_unchanged=len(scientific), record_level_checkpoints=1,
                          producer_manifest='PASS', scientific_code_executed=False,
                          independent_scientific_verification='not performed', baseline_revision=base), sort_keys=True))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, KeyError, subprocess.CalledProcessError) as error:
        raise SystemExit(str(error))
