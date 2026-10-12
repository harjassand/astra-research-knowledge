#!/usr/bin/env python3
"""Validate EE source integrity and exact scoped continuation routes, not science."""
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

BASE = '787ab8b8ec23d17d4ab44a5cf2af602e5050355b'
EXPECTED = [
    ('N716', '709206071bedebed9a37c55b46a4da68ee82c9a560bdb12dcdd18d5b7da1778d', 26249, 3276, 46, 2762, 24, 27),
    ('N717', 'd6da86725e0cc91ab401ae0d5dc8f14407568bffb7c4239762ad0abe3a15855c', 27282, 553, 54, 2191, 12, 27),
    ('N718', 'a0a15327c135629530870eba5fe36b075557322f146d32428be7c7989bb38500', 30377, 2961, 78, 2243, 25, 28),
]
NOTICES = {
    'SN-EE-N714-N717-FEASIBLE-ENERGY-EXTENSION': ('N714', 'N717'),
    'SN-EE-N713-N718-PRODUCT-ACCESS-COMPLETION': ('N713', 'N718'),
}
ARTIFACT_PINS = {'2ae13f8c0bb63c9fc12f41795e4a3739fdbfde6c82cb0cd8ab6dfeb68ae74dbb': (30554, 648), 'ecdb8c4fa716c22033b31600f82365e12c80568f046372ab9f24b38d7ec1fbd8': (4060, 84), '57659253c162b49536e82ebf685d945a6dd9818d1dd85e207afd4cf84fc60907': (1075, 33), '18af8267ebe7841dbb23abbd637b2a2a5d97cf42ba387ba8007d84733dfb8b35': (1417, 13), 'b04cb202953d13451a960ae93afbe0cde3fc59760077ea7d315a16d40a9f86cb': (539, 8), '0eed3af3b847667f3569fe470cf229c6014bf4b464ed52a65bc89085dae24f8a': (32795, 428), '763951c16c9515ded2cb00144703225884ac693ad228b54b088237c9988297ea': (2226, 13), '20febd28a24e60917f0974215103613a3c57597d7d173138b09cbf0539047f87': (12321, 511), '3a6b2aee62516e8524f07e5738d777b87f9c6953d1ca1af1ed6a69c1beacdeb6': (1884, 139), '9bca2d0cb1fa74108bcd26270ca14b4166ddb4682854bc0cc07956f194a8a231': (11240, 256), '3fe912b96c46e7a3a2175fd103d0ad2201efd9dd221f08f41b467fa56c931fbc': (9813, 233), 'ff210b780c7e3d896268fe996d29d024baf50fdf1f2928d7383b3fd8e26dcfab': (1815, 53)}


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


def check_navigation_hashes(scientific, permitted):
    """Check the frozen route set separately from other intake projections."""
    actual = {p for p,d in scientific.items() if not (ROOT / p).is_file() or sha((ROOT / p).read_bytes()) != d}
    need(actual == set(permitted), 'unscoped earlier navigation change')
    return actual


def main():
    manifest = load('updates/EE/SOURCE_MANIFEST.json')
    claims_map = load('updates/EE/CLAIMS.json')
    need(manifest['intake_base_revision'] == claims_map['base_revision'] == BASE, 'base changed')
    need(len(manifest['originals']) == len(claims_map['claims']) == 3, 'attempt coverage changed')
    sources = list(manifest['originals'])
    for original, (route, digest, size, count, report, duration, prompt, duration_line) in zip(manifest['originals'], EXPECTED):
        data = (ROOT / original['path']).read_bytes()
        need(sha(data) == original['sha256'] == digest and len(data) == original['bytes'] == size and
             len(data.decode().splitlines()) == original['lines'] == count, 'original bytes/extent changed')
        need(original['initiating_prompt_lines'] == [1,prompt] and
             original['final_report_lines'] == [report,count] and
             original['reported_duration']['seconds'] == duration and
             original['reported_duration']['lines'] == [duration_line,duration_line],
             'prompt/report/duration classification changed')
    directories = manifest['supplied_directories']
    need([(d['route'],d['original_directory_name'],len(d['members'])) for d in directories] == [
        ('N716','Astra_Resonant_Convex_Lifting',3),('N718','astra_intervention_products',7)], 'directory coverage changed')
    for directory in directories:
        sources += directory['members']
        if directory['route'] == 'N718':
            producer = load(directory['producer_manifest_path'])
            members = {Path(i['path']).name:i for i in directory['members']}
            need(set(producer) == set(members)-{'manifest.json'} and len(producer) ==
                 directory['producer_hashes_checked'] == 6, 'producer manifest coverage')
            for name,digest in producer.items():
                need(sha((ROOT/members[name]['path']).read_bytes()) == digest == members[name]['sha256'], 'producer hash mismatch')
        else:
            need(directory['producer_hashes_checked'] == 0, 'missing producer manifest invented')
    need(len(manifest['supplied_files']) == 2, 'standalone coverage')
    sources += manifest['supplied_files']
    artifacts = sources[3:]
    need(len(artifacts) == len(ARTIFACT_PINS) == 12 and {i['sha256'] for i in artifacts} == set(ARTIFACT_PINS), 'supporting artifact identity changed')
    for item in artifacts:
        data = (ROOT/item['path']).read_bytes()
        need(sha(data) == item['sha256'] and (len(data),len(data.decode().splitlines())) ==
             ARTIFACT_PINS[item['sha256']] == (item['bytes'],item['lines']), 'supporting artifact bytes/extent changed')
        if item['path'].endswith('.py'):
            import ast
            ast.parse(data,filename=item['path'])
    need({p.relative_to(ROOT).as_posix() for p in (ROOT/'updates/EE/package').rglob('*') if p.is_file()} ==
         {i['path'] for i in sources}, 'missing/extra archived disclosure')
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
        expected_imports = ['external:EE_CMP21_THEOREM31_POLYNOMIAL_ODE_SIMULATION'] if route == 'N716' else []
        need([d['target'] for d in status['depends_on']] == claims[0]['depends_on'] == expected_imports,
             'whole-claim proof dependency invented or import lost')
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
        need(trace['mode'] == ('UNKNOWN' if route == 'N716' else 'targeted_warm_continuation') and
             trace['context']['conversation_relation'] == ('UNKNOWN' if route == 'N716' else 'same') and trace['prompt_availability'] == 'exact', 'workflow context misclassified')
        need(all(v is None for v in trace['model'].values()) and all(v is None for v in trace['resources']['usage'].values()) and
             trace['resources']['worker_invocations'] is None and trace['matched_run_id'] is None and
             trace['advance']['verification'] == 'producer_reported' and trace['advance']['verification_receipt'] is None, 'usage/model/independent validation invented')
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
    permitted = manifest['permitted_historical_navigation_changes']
    need(set(permitted) == {'frontier/dossiers/N713.txt','frontier/connections/N713.json',
                            'frontier/dossiers/N714.txt','frontier/connections/N714.json'}, 'unscoped earlier navigation change')
    actual = check_navigation_hashes(scientific, permitted)
    print(json.dumps(dict(intake='EE',status='PASS',original_pastes=3,supplied_supporting_files=12,producer_hashes_checked=6,
                          source_routes=len(sources),research_attempt_observations=3,proof_ranges=proof_count,
                          record_level_checkpoints=3,unchanged_earlier_scientific_routes=len(scientific)-4,
                          scoped_continuation_views=sorted(actual),historical_scientific_objects_changed=0,
                          scientific_scripts_executed=0,independent_scientific_verification='not performed'),sort_keys=True))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, KeyError, subprocess.CalledProcessError) as error:
        raise SystemExit(str(error))
