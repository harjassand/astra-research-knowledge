#!/usr/bin/env python3
"""Validate EC source integrity and exact scoped continuation routes, not science."""
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

BASE = '142e27d7eb0a0590a8fc649c63a95a818dca95aa'
EXPECTED = [
    ('N712', 'f366b1fe4464bfe42a0a36801b6ce66553b2d39f650fc5dc19e62ac08edb0bd0', 20114, 214, 20, 2413),
    ('N713', 'd6ebe2c66dfab6af079e66ed518c86cbcf88f39a37c9903c00f85b6eb3e9ba97', 24771, 243, 20, 2552),
    ('N714', 'a3af80b71096790927a6e8b9d87e28d4b3b1a50898e033d7e86c61df9b0a84c3', 25624, 548, 53, 3312),
]
ARCHIVES = [
    ('d2c1dacbf1d24483e235904d8bb89ff58d13a279a97f5bc794d97d05deff267f', 453206, 7, 'astra_local_readout/SHA256SUMS.json'),
    ('153e0d2f943457648e89d720efb90d6c7f19bcac01d4468235e92af22b424b59', 23325, 8, 'astra_active_closure/MANIFEST.json'),
]
NOTICES = {
    'SN-EC-N711-N712-INDEPENDENT-READOUT-CONDITIONAL-COROLLARY': ('N711', 'N712'),
    'SN-EC-N709-N713-CLOSURE-AND-ROBUSTNESS-SCOPE': ('N709', 'N713'),
}


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
    manifest = load('updates/EC/SOURCE_MANIFEST.json')
    claims_map = load('updates/EC/CLAIMS.json')
    need(manifest['intake_base_revision'] == claims_map['base_revision'] == BASE, 'base changed')
    need(len(manifest['originals']) == len(claims_map['claims']) == 3, 'attempt coverage changed')
    sources = list(manifest['originals'])
    for original, (route, digest, size, count, report, duration) in zip(manifest['originals'], EXPECTED):
        data = (ROOT / original['path']).read_bytes()
        need(sha(data) == original['sha256'] == digest and len(data) == original['bytes'] == size and
             len(data.decode().splitlines()) == original['lines'] == count, 'original bytes/extent changed')
        need(original['initiating_prompt_lines'] == [1, 11 if route == 'N714' else 10] and
             original['final_report_lines'] == [report, count] and
             original['reported_duration']['seconds'] == duration and
             original['reported_duration']['lines'] == ([26, 26] if route == 'N714' else [11, 11]),
             'prompt/report/duration classification changed')
    need(len(manifest['recovered_packages']) == 2, 'archive coverage changed')
    for package, (digest, size, count, producer_path) in zip(manifest['recovered_packages'], ARCHIVES):
        data = (ROOT / package['archive_path']).read_bytes()
        need(sha(data) == package['sha256'] == digest and len(data) == package['bytes'] == size, 'ZIP bytes changed')
        with ZipFile(ROOT / package['archive_path']) as archive:
            need(archive.testzip() is None and len(archive.namelist()) == len(set(archive.namelist())) == count,
                 'archive integrity/duplicates')
            need(set(archive.namelist()) == {m['archive_member'] for m in package['members']}, 'member coverage')
            for info in archive.infolist():
                p = PurePosixPath(info.filename)
                need(not p.is_absolute() and '..' not in p.parts and '\\' not in info.filename and
                     not info.is_dir() and not stat.S_ISLNK(info.external_attr >> 16), 'unsafe archive member')
            for member in package['members']:
                data = (ROOT / member['path']).read_bytes()
                need(data == archive.read(member['archive_member']) and sha(data) == member['sha256'] and
                     len(data) == member['bytes'], 'extracted member changed')
            producer = json.loads(archive.read(producer_path))
            prefix = producer_path.rsplit('/', 1)[0] + '/'
            need({prefix + name for name in producer} == set(archive.namelist()) - {producer_path}, 'producer coverage')
            need(all(sha(archive.read(prefix + name)) == digest for name, digest in producer.items()), 'producer hash mismatch')
            need(package['producer_hashes_checked'] == count - 1, 'producer count invented')
        sources += package['members'] + [dict(path=package['archive_path'], **{k:package[k] for k in ['source_id','sha256','bytes']})]
    need(len(manifest['recovered_files']) == 2, 'standalone file coverage')
    need([(f['sha256'], f['bytes'], f['lines']) for f in manifest['recovered_files']] == [
        ('5fca1ca522bf1c48e3af7a9acd1d2ee6d957b42b257633e61958d6886482a40b', 9283, 251),
        ('fc86e1425466b2079701f798730e9783c23c245b1af936d8c310e2001ebf377f', 2650, 92)], 'standalone source identity changed')
    sources += manifest['recovered_files']
    package_files = {p.relative_to(ROOT).as_posix() for p in (ROOT / 'updates/EC/package').rglob('*') if p.is_file()}
    need(package_files == {r['path'] for r in sources}, 'missing/extra archived disclosure')
    need(len(manifest['source_link_receipts']) == 1, 'citation metadata coverage')
    sources += manifest['source_link_receipts']
    ledgers = {p:rows(p) for p in ['indexes/claims.jsonl','frontier/CURRENT_CLAIM_STATUS.jsonl','indexes/source_metadata.jsonl','web/documents.jsonl']}
    for item in sources:
        data = (ROOT / item['path']).read_bytes()
        need(sha(data) == item['sha256'] and len(data) == item['bytes'], 'source/receipt hash mismatch')
        if 'lines' in item:
            need(len(data.decode().splitlines()) == item['lines'], 'source line extent changed')
        metadata = [r for r in ledgers['indexes/source_metadata.jsonl'] if r.get('source_id') == item['source_id']]
        docs = [r for r in ledgers['web/documents.jsonl'] if r['id'] == item['source_id']]
        need(len(metadata) == len(docs) == 1 and metadata[0]['sha256'] == item['sha256'] and
             metadata[0]['path'] == docs[0]['path'] == item['path'], 'source routing disagreement')
        if docs[0]['extraction'] == 'original_binary':
            need(docs[0]['url'] == '../' + item['path'], 'binary source misrendered')
        else:
            need('<pre>' + html.escape(data.decode()) + '</pre>' in (ROOT / ('web/' + docs[0]['url'])).read_text(), 'text page changed source')
    graph = load('indexes/agent_graph.json')
    node_ids = {n['id'] for n in graph['nodes']}
    need(len(node_ids) == len(graph['nodes']) and all(e['from'] in node_ids and e['to'] in node_ids for e in graph['edges']), 'graph integrity')
    entry_by_route = {e['id'].split('-',1)[0]:e for e in claims_map['claims']}
    proof_count = 0
    for route, entry in entry_by_route.items():
        cid = entry['id']
        status = [r for r in ledgers['frontier/CURRENT_CLAIM_STATUS.jsonl'] if r['card_id'] == cid]
        claims = [r for r in ledgers['indexes/claims.jsonl'] if r['id'] == cid]
        catalog = [r for r in load('indexes/agent_catalog.json')['claims'] if r['id'] == cid]
        need(len(status) == len(claims) == len(catalog) == 1, 'claim coverage')
        status = status[0]
        need(status == load('frontier/cards/' + cid + '.json'), 'sidecar mismatch')
        need(status['claim_status'] == claims[0]['status'] == entry['status'] == 'source_derived_unreviewed', 'status promotion')
        need(status['depends_on'] == claims[0]['depends_on'] == [], 'whole-claim proof dependency invented')
        data = (ROOT / status['card_path']).read_bytes()
        need(sha(data) == status['card_sha256'] == catalog[0]['card_sha256'] and
             (ROOT / ('frontier/review_cards/' + cid + '.txt')).read_bytes().endswith(data), 'card/wrapper hash mismatch')
        refs = status['proof_availability']['located_proof_sources'] + status['proof_availability']['available_evidence_sources']
        for ref in refs:
            data = (ROOT / ref['path']).read_bytes()
            need(sha(data) == ref['sha256'] and 1 <= ref['lines'][0] <= ref['lines'][1] <= len(data.decode().splitlines()), 'proof/evidence route invalid')
        proof_count += len(status['proof_availability']['located_proof_sources'])
        need(set(claims[0]['source_ids']) <= {e['to'] for e in graph['edges'] if e['from'] == cid and e['kind'] == 'provenance'}, 'source provenance incomplete')
        need(cid + '\t' in (ROOT / 'agent/routes.tsv').read_text(), 'legacy route missing')
        for topic in status['topics']:
            need(cid + '\t' in (ROOT / ('agent/topics/' + topic + '.tsv')).read_text(), 'topic route missing')
        need(any(cid in g['card_ids'] and g['status'] == 'open' for g in rows('frontier/OPEN_PROOF_GATES.jsonl')), 'review gate missing')
        trace = load(entry['workflow_trace'])
        validate_trace(trace, ROOT)
        need(trace['mode'] == ('fresh_direction_retained_context' if route == 'N714' else 'targeted_warm_continuation') and
             trace['context']['conversation_relation'] == 'same' and trace['prompt_availability'] == 'exact', 'workflow context misclassified')
        need(all(v is None for v in trace['model'].values()) and all(v is None for v in trace['resources']['usage'].values()) and
             trace['resources']['worker_invocations'] is None and trace['matched_run_id'] is None and
             trace['advance']['verification'] == 'producer_reported', 'usage/model/independent validation invented')
        cp = load(entry['checkpoint'])
        validate_record(cp, ROOT)
        need(cp['base_revision'] == BASE and cp['parent_checkpoint_ids'] == [], 'intake ancestry invented')
        generated = views(ROOT, {cp['branch_id']:{cp['checkpoint_id']:cp}})
        view = 'state/branches/' + cp['branch_id'] + '.txt'
        need((ROOT / view).read_text() == generated[view], 'new checkpoint view stale')
        row = next(r for r in generated['state/branches.tsv'].splitlines() if r.startswith(cp['branch_id'] + '\t'))
        need((ROOT / 'state/branches.tsv').read_text().splitlines().count(row) == 1, 'new checkpoint registry mismatch')
    notices = rows('agent/SEMANTIC_NOTICES.jsonl')
    need(set(manifest['reciprocal_continuation_notices']) == set(NOTICES), 'notice coverage changed')
    for nid, (earlier, newer) in NOTICES.items():
        notice = [n for n in notices if n['notice_id'] == nid]
        need(len(notice) == 1 and {c.split('-',1)[0] for c in notice[0]['card_ids']} == {earlier,newer} and
             notice[0]['status'] == 'source_derived_unreviewed_continuation_only', 'notice lost/promoted')
        notice = notice[0]
        for route in [earlier,newer]:
            need(nid in (ROOT / ('frontier/dossiers/' + route + '.txt')).read_text(), 'reciprocal notice not exposed')
        # Strip only this exact new notice and global snapshot line. Every
        # historical mathematical statement and prior notice must survive.
        old = git('show',BASE + ':frontier/dossiers/' + earlier + '.txt').decode().splitlines()
        now = (ROOT / ('frontier/dossiers/' + earlier + '.txt')).read_text().splitlines()
        pos = now.index('SEMANTIC NOTICE ' + nid)
        need(now[pos+1] == notice['status'] + ': ' + notice['clarification'], 'notice projection mismatch')
        del now[pos-1:pos+2]
        old[1] = now[1] = '<global snapshot>'
        need(old == now, 'earlier dossier mathematics rewritten: ' + earlier)
        path = 'frontier/connections/' + earlier + '.json'
        old, now = json.loads(git('show',BASE + ':' + path)), load(path)
        for key in old:
            if key in ['snapshot','nodes','edges']:
                continue
            need(old[key] == now[key], 'earlier connection scope changed')
        need(all(n in now['nodes'] for n in old['nodes']) and len(now['nodes']) == len(old['nodes']) + 1 and
             all(e in now['edges'] for e in old['edges']) and len(now['edges']) == len(old['edges']) + 1, 'earlier connections rewritten')
        edge = next(e for e in now['edges'] if e not in old['edges'])
        need(edge['kind'] == 'material_update' and edge['from'] == entry_by_route[newer]['id'] and
             edge['to'].startswith(earlier + '-') and edge['composition'] == notice['clarification'], 'wrong scoped edge')
    for path in list(ledgers) + ['agent/SEMANTIC_NOTICES.jsonl','frontier/OPEN_PROOF_GATES.jsonl','state/branches.tsv','agent/routes.tsv']:
        need((ROOT / path).read_bytes().startswith(git('show',BASE + ':' + path)), 'historical ledger rows rewritten: ' + path)
    for path, fields in [('indexes/agent_catalog.json',['claims']),('indexes/agent_graph.json',['nodes','edges'])]:
        old, now = json.loads(git('show',BASE + ':' + path)), load(path)
        for field in fields:
            need(now[field][:len(old[field])] == old[field], 'historical catalog/graph rewritten')
    old, now = json.loads(git('show',BASE + ':indexes/query_aliases.json')), load('indexes/query_aliases.json')
    need(all(now.get(k) == v for k,v in old.items()), 'historical aliases changed')
    old_paths = set(git('ls-tree','-r','--name-only',BASE).decode().splitlines())
    changed = set(git('diff','--name-only',BASE,'--','updates','cards','frontier/cards','state/checkpoints','state/branches','evaluation','technology/records').decode().splitlines())
    need(not (changed & old_paths), 'historical source/card/status/checkpoint/evaluation/technology record changed')
    outputs = json.loads(git('show',BASE + ':agent/access_manifest.json'))['outputs']
    scientific = {p:d for p,d in outputs.items() if p.startswith(('frontier/dossiers/','frontier/connections/','frontier/proof_ranges/'))}
    actual = {p for p,d in scientific.items() if not (ROOT / p).is_file() or sha((ROOT / p).read_bytes()) != d}
    need(actual == set(manifest['permitted_historical_navigation_changes']) == {
        'frontier/dossiers/N709.txt','frontier/connections/N709.json','frontier/dossiers/N711.txt','frontier/connections/N711.json'}, 'unscoped earlier navigation change')
    print(json.dumps(dict(intake='EC',status='PASS',original_pastes=3,archive_members=15,producer_hashes_checked=13,
                          standalone_files=2,source_routes=len(sources),research_attempts=3,proof_ranges=proof_count,
                          record_level_checkpoints=3,unchanged_earlier_scientific_routes=len(scientific)-4,
                          scoped_continuation_views=sorted(actual),historical_scientific_objects_changed=0,
                          scientific_scripts_executed=0,independent_scientific_verification='not performed'),sort_keys=True))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, KeyError, subprocess.CalledProcessError) as error:
        raise SystemExit(str(error))
