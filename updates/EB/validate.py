#!/usr/bin/env python3
"""Validate EB preservation and the exact N705 continuation exception, not science."""
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
    manifest = load('updates/EB/SOURCE_MANIFEST.json')
    claim_map = load('updates/EB/CLAIMS.json')
    base = manifest['intake_base_revision']
    need(base == claim_map['base_revision'] == 'e71f628e474a77a6950e50b64855237561344ad3', 'base revision changed')
    need(len(manifest['originals']) == len(claim_map['claims']) == 2, 'research-attempt coverage changed')
    expected = [('4278fdd55cde99ee0c84619515511226f8a35367fa54be10686f86351204dfd4',30735,578,[1,16],[62,578],3170),
                ('9d914423ff19123ca9f59f0fec5645230d0cf68b13c910ada658a9ce53476d73',22652,582,[1,17],[59,582],2250)]
    for original, (digest, size, lines, prompt, report, duration) in zip(manifest['originals'], expected):
        data = (ROOT / original['path']).read_bytes()
        need(sha(data) == original['sha256'] == digest and len(data) == original['bytes'] == size and
             len(data.decode().splitlines()) == original['lines'] == lines, 'source bytes/extent changed')
        need(original['initiating_prompt_lines'] == prompt and original['final_report_lines'] == report and
             original['reported_duration']['seconds'] == duration, 'prompt/output/duration misclassified')
    need(len(manifest['recovered_packages']) == 1, 'archive coverage changed')
    package = manifest['recovered_packages'][0]
    data = (ROOT / package['archive_path']).read_bytes()
    need(sha(data) == package['sha256'] == 'b4701ebff8b09ff92e5e1c61d279a4afca09f97f94ac3c9bd4bd902a55fe619f' and
         len(data) == package['bytes'] == 400630, 'ZIP bytes changed')
    need(package['verification']['producer_member_manifest'] == 'not supplied', 'producer manifest invented')
    with ZipFile(ROOT / package['archive_path']) as z:
        need(z.testzip() is None and len(z.namelist()) == len(set(z.namelist())) == len(package['members']) == 5, 'ZIP integrity/coverage')
        need(set(z.namelist()) == {m['archive_member'] for m in package['members']}, 'archive member disagreement')
        for info in z.infolist():
            name = PurePosixPath(info.filename)
            need(not name.is_absolute() and '..' not in name.parts and '\\' not in info.filename and
                 not info.is_dir() and not stat.S_ISLNK(info.external_attr >> 16), 'unsafe archive member')
        for member in package['members']:
            data = (ROOT / member['path']).read_bytes()
            need(data == z.read(member['archive_member']) and sha(data) == member['sha256'] and len(data) == member['bytes'], 'extracted original changed')
    originals = manifest['originals'] + package['members'] + [dict(path=package['archive_path'], **{k:package[k] for k in ['source_id','sha256','bytes']})]
    files = {p.relative_to(ROOT).as_posix() for p in (ROOT / 'updates/EB/package').rglob('*') if p.is_file()}
    need(files == {r['path'] for r in originals}, 'missing/extra archived disclosure')
    all_sources = originals + manifest['source_link_receipts']
    ledgers = {p:rows(p) for p in ['indexes/claims.jsonl','frontier/CURRENT_CLAIM_STATUS.jsonl','indexes/source_metadata.jsonl','web/documents.jsonl']}
    for item in all_sources:
        data = (ROOT / item['path']).read_bytes()
        need(sha(data) == item['sha256'] and len(data) == item['bytes'], 'source/receipt changed')
        metadata = [r for r in ledgers['indexes/source_metadata.jsonl'] if r.get('source_id') == item['source_id']]
        docs = [r for r in ledgers['web/documents.jsonl'] if r['id'] == item['source_id']]
        need(len(metadata) == len(docs) == 1 and metadata[0]['sha256'] == item['sha256'] and
             metadata[0]['path'] == docs[0]['path'] == item['path'], 'source route disagreement')
        if docs[0]['extraction'] == 'original_binary':
            need(docs[0]['url'] == '../' + item['path'], 'binary source misrendered')
        else:
            need('<pre>' + html.escape(data.decode()) + '</pre>' in (ROOT / ('web/' + docs[0]['url'])).read_text(), 'static source changed')
    graph = load('indexes/agent_graph.json')
    nodes = {n['id'] for n in graph['nodes']}
    need(len(nodes) == len(graph['nodes']) and all(e['from'] in nodes and e['to'] in nodes for e in graph['edges']), 'graph integrity failure')
    proof_count = 0
    for entry in claim_map['claims']:
        cid = entry['id']
        statuses = [r for r in ledgers['frontier/CURRENT_CLAIM_STATUS.jsonl'] if r['card_id'] == cid]
        claims = [r for r in ledgers['indexes/claims.jsonl'] if r['id'] == cid]
        catalog = [r for r in load('indexes/agent_catalog.json')['claims'] if r['id'] == cid]
        need(len(statuses) == len(claims) == len(catalog) == 1, 'family coverage changed')
        status = statuses[0]
        need(status == load('frontier/cards/' + cid + '.json'), 'sidecar disagreement')
        need(status['claim_status'] == claims[0]['status'] == entry['status'] == 'source_derived_unreviewed', 'status promotion')
        need(status['depends_on'] == claims[0]['depends_on'] == [], 'repository proof premise invented')
        data = (ROOT / status['card_path']).read_bytes()
        need(sha(data) == status['card_sha256'] == catalog[0]['card_sha256'] and
             (ROOT / ('frontier/review_cards/' + cid + '.txt')).read_bytes().endswith(data), 'card hash/wrapper disagreement')
        for ref in status['proof_availability']['located_proof_sources'] + status['proof_availability']['available_evidence_sources']:
            data = (ROOT / ref['path']).read_bytes()
            need(sha(data) == ref['sha256'] and 1 <= ref['lines'][0] <= ref['lines'][1] <= len(data.decode().splitlines()), 'invalid proof/evidence reference')
        proof_count += len(status['proof_availability']['located_proof_sources'])
        need(set(claims[0]['source_ids']) <= {e['to'] for e in graph['edges'] if e['from'] == cid and e['kind'] == 'provenance'}, 'provenance incomplete')
        need(cid + '\t' in (ROOT / 'agent/routes.tsv').read_text(), 'legacy route missing')
        for topic in status['topics']:
            need(cid + '\t' in (ROOT / ('agent/topics/' + topic + '.tsv')).read_text(), 'topic route missing')
        need(any(cid in g['card_ids'] and g['status'] == 'open' for g in rows('frontier/OPEN_PROOF_GATES.jsonl')), 'review gate missing')
        trace = load(entry['workflow_trace'])
        validate_trace(trace, ROOT)
        need(trace['mode'] == ('fresh_direction_retained_context' if cid.startswith('N710-') else 'targeted_warm_continuation') and
             trace['context']['conversation_relation'] == 'same' and trace['prompt_availability'] == 'exact', 'research mode invented/lost')
        need(all(v is None for v in trace['model'].values()) and all(v is None for v in trace['resources']['usage'].values()) and
             trace['resources']['worker_invocations'] is None and trace['matched_run_id'] is None and trace['advance']['verification'] == 'producer_reported', 'model/usage/verification invented')
        cp = load(entry['checkpoint'])
        validate_record(cp, ROOT)
        need(cp['base_revision'] == base and cp['parent_checkpoint_ids'] == [], 'intake ancestry invented')
        generated = views(ROOT, {cp['branch_id']:{cp['checkpoint_id']:cp}})
        view = 'state/branches/' + cp['branch_id'] + '.txt'
        need((ROOT / view).read_text() == generated[view], 'new checkpoint view stale')
        registry_row = next(r for r in generated['state/branches.tsv'].splitlines() if r.startswith(cp['branch_id'] + '\t'))
        need((ROOT / 'state/branches.tsv').read_text().splitlines().count(registry_row) == 1, 'new checkpoint registry disagreement')
    earlier = 'N705-bounded-coupling-local-thermal-faithfulness-and-finite-band'
    newer = next(c['id'] for c in claim_map['claims'] if c['id'].startswith('N711-'))
    notices = [n for n in rows('agent/SEMANTIC_NOTICES.jsonl') if n['notice_id'] == manifest['reciprocal_continuation_notice']]
    need(len(notices) == 1 and set(notices[0]['card_ids']) == {earlier,newer} and
         notices[0]['status'] == 'source_derived_unreviewed_continuation_only', 'reciprocal notice lost/promoted')
    for route in ['N705','N711']:
        need(notices[0]['notice_id'] in (ROOT / ('frontier/dossiers/' + route + '.txt')).read_text(), 'notice not exposed reciprocally')
    for path in list(ledgers) + ['agent/SEMANTIC_NOTICES.jsonl','frontier/OPEN_PROOF_GATES.jsonl','state/branches.tsv','agent/routes.tsv']:
        need((ROOT / path).read_bytes().startswith(git('show',base + ':' + path)), 'historical ledger rows changed: ' + path)
    for path, fields in [('indexes/agent_catalog.json',['claims']),('indexes/agent_graph.json',['nodes','edges'])]:
        old, now = json.loads(git('show',base + ':' + path)), load(path)
        for field in fields:
            need(now[field][:len(old[field])] == old[field], 'historical catalog/graph changed')
    old_paths = set(git('ls-tree','-r','--name-only',base).decode().splitlines())
    changed = set(git('diff','--name-only',base,'--','updates','cards','frontier/cards','state/checkpoints','state/branches','evaluation','technology/records').decode().splitlines())
    need(not (changed & old_paths), 'historical source/card/status/checkpoint/record changed')
    outputs = json.loads(git('show',base + ':agent/access_manifest.json'))['outputs']
    scientific = {p:d for p,d in outputs.items() if p.startswith(('frontier/dossiers/','frontier/connections/','frontier/proof_ranges/'))}
    actual = {p for p,d in scientific.items() if not (ROOT / p).is_file() or sha((ROOT / p).read_bytes()) != d}
    need(actual == set(manifest['permitted_historical_navigation_changes']) ==
         {'frontier/dossiers/N705.txt','frontier/connections/N705.json'}, 'unscoped earlier scientific navigation change')
    # The old dossier content is retained verbatim modulo its global snapshot line
    # and the one appended notice, which must not repair or replace mathematics.
    old = git('show',base + ':frontier/dossiers/N705.txt').decode().splitlines()
    now = (ROOT / 'frontier/dossiers/N705.txt').read_text().splitlines()
    pos = now.index('SEMANTIC NOTICE ' + notices[0]['notice_id'])
    need(now[pos+1] == notices[0]['status'] + ': ' + notices[0]['clarification'], 'notice content changed')
    del now[pos-1:pos+2]
    old[1] = now[1] = '<global snapshot>'
    need(old == now, 'N705 historical dossier mathematics rewritten')
    print(json.dumps(dict(intake='EB',status='PASS',original_pastes=2,archive_members=5,source_routes=len(all_sources),
                          research_attempts=2,proof_ranges=proof_count,record_level_checkpoints=2,
                          unchanged_earlier_scientific_routes=len(scientific)-2,scoped_reciprocal_navigation_extensions=sorted(actual),
                          historical_scientific_objects_changed=0,scientific_scripts_executed=0,
                          independent_scientific_verification='not performed'),sort_keys=True))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, KeyError, subprocess.CalledProcessError) as error:
        raise SystemExit(str(error))
