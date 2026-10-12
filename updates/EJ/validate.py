#!/usr/bin/env python3
"""Deterministic EJ archive/navigation guards. Never executes scientific scripts."""
import ast
import hashlib
import html
import json
from pathlib import Path, PurePosixPath
import stat
import subprocess
import sys
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from evaluation.workflow_trace import validate as validate_trace
from state.publish_checkpoint import validate_record, views

BASE = 'e5ad789a43006ec9cb6f5f7e304128ddc7f924f7'
EXPECTED = {'N728':(2249,'targeted_warm_continuation','same'),
            'N729':(1909,'independent_selective_capital','UNKNOWN'),
            'N730':(1762,'targeted_warm_continuation','same')}
PINS = {'updates/EJ/package/theoretical_active_prediction/ORIGINAL_PASTED_SOURCE.txt': '22b47cc1ea22f718bbff97ce7135575f72f2bda0334237e97efa804e5240a3b9', 'updates/EJ/package/genesis_strain_geometry/ORIGINAL_PASTED_SOURCE.txt': '997264898342d68fb5ed541c00330905d2bc67614d4f6ceff69364086f912035', 'updates/EJ/package/computational_relative_model_transfer/ORIGINAL_PASTED_SOURCE.txt': '0698572fa8ea9937c6ff81382c5fd10d99e8de903925f965445754c5042185f9', 'updates/EJ/package/theoretical_active_prediction/astra_active_prediction_2026-10-12.zip': '08b4accffddd8aa5ee9d730f344e2dc3f75303cbcbb9c27f3fb1bc5d951e5718', 'updates/EJ/package/theoretical_active_prediction/recovered/astra_active_prediction/MANIFEST.json': '48aa8390c7b2e53c7b641bded53aca89bc975bd352b5dfd4ac6085c1de4915a4', 'updates/EJ/package/theoretical_active_prediction/recovered/astra_active_prediction/README.md': 'ed8e3036a14d64802129df7e552179e23749edcceebebdb0ecd8b2eaa063242d', 'updates/EJ/package/theoretical_active_prediction/recovered/astra_active_prediction/diagnostics.json': 'f0a02f2845e2c34ff28ae9214ae65a55491f24fdc2ec7130fa684b1d6f798fee', 'updates/EJ/package/theoretical_active_prediction/recovered/astra_active_prediction/genesis_bridge_diagnostics.json': 'd2debc9b46ed20f1e069a90763240db4949bcb2bc862dfc866b4a7ecb4519630', 'updates/EJ/package/theoretical_active_prediction/recovered/astra_active_prediction/research_note.md': '936c565153c197c507313b129e337f41f11fe3bdae448a888777f14928e58178', 'updates/EJ/package/theoretical_active_prediction/recovered/astra_active_prediction/verify.py': '3b62bc0727b3143309143f02b010cb8b0af4ba56059c3e054f67a01bcd7bda2b', 'updates/EJ/package/theoretical_active_prediction/recovered/astra_active_prediction/verify_genesis_bridge.py': '36ecfb19384a197ac71d6aeaadedf6d642d9414ae7434ce8f8132b0e119e3801', 'updates/EJ/package/genesis_strain_geometry/astra_strain_geometry_research.zip': 'd974847259370bfa67243de652944ac60cb01df9b0c042c4463f7ee5c4aa2ac7', 'updates/EJ/package/genesis_strain_geometry/recovered/astra_strain_geometry/research_note.md': 'efa53794f0def12eb8f9639445980bd7053cb898ca414df62769d6f1611f925b', 'updates/EJ/package/genesis_strain_geometry/recovered/astra_strain_geometry/verify.py': '7804121d711eacbfd568c22e0cfb055f6ef3b2076609ccefd5b77495e8f76b0d', 'updates/EJ/package/genesis_strain_geometry/recovered/astra_strain_geometry/verification_results.json': 'bf69095851fc98217b39ff866fc427acdbdf581761c381208eec94be265d4e2e', 'updates/EJ/package/genesis_strain_geometry/recovered/astra_strain_geometry/manifest.json': 'df34cf166c560352fa0d3885580fc54424ec6f827b4a553bbfc130ffbeb616da', 'updates/EJ/package/computational_relative_model_transfer/cray_relative_model_transfer.zip': '19c28167942d56562b7a752606f9c3f31dae211488183bedc41b41c772d9c0ea', 'updates/EJ/package/computational_relative_model_transfer/recovered/cray_relative_model_transfer/run_summary.json': '9583c0a44c201d4da3a527873b49827a8c9129f763b652e485aafe392dcad0f6', 'updates/EJ/package/computational_relative_model_transfer/recovered/cray_relative_model_transfer/verify_and_plan.py': 'fa7a9cf87a168e6d06341392c3f8e35c66f40106e0b79e0994a856fa1cf69243', 'updates/EJ/package/computational_relative_model_transfer/recovered/cray_relative_model_transfer/verification_results.json': 'b44af8e1097b666a3c07de6cc1e967413d77dc05fbb0ca16a57b12fdd6a5281d', 'updates/EJ/package/computational_relative_model_transfer/recovered/cray_relative_model_transfer/RESULTS.md': '1cfa26f9066bf76d5d3745d98be9dc3bfbd79aa72e29ed3dd12aeecdaea291b8'}


def need(condition,message):
    if not condition:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def load(path):
    return json.loads((ROOT/path).read_text())


def rows(path):
    return [json.loads(l) for l in (ROOT/path).read_text().splitlines() if l.strip()]


def git(*args):
    return subprocess.check_output(['git','-C',str(ROOT),*args])


def check_sources(manifest):
    need(len(manifest['originals']) == 3 and sum(x['bytes'] for x in manifest['originals']) == 62609,
         'pasted source coverage/extent changed')
    packages = manifest['recovered_packages']
    need(len(packages) == 3 and manifest['recovered_files'] == [], 'archive coverage changed')
    source_rows = manifest['originals'] + sum(([p]+p['members'] for p in packages), [])
    indexed = {x['path']:x for x in source_rows}
    need(len(indexed) == len(source_rows) == 21 and set(indexed) == set(PINS), 'original source identities changed')
    scripts = 0
    for path,item in indexed.items():
        data = (ROOT/path).read_bytes()
        need(sha(data) == item['sha256'] == PINS[path] and len(data) == item['bytes'], 'original bytes/hash changed')
        if 'lines' in item:
            need(len(data.decode().splitlines()) == item['lines'], 'source extent changed')
        if path.endswith('.py'):
            ast.parse(data,filename=path)
            scripts += 1
    need(scripts == 4 and sum(x['bytes'] for x in indexed.values()) == 222865, 'original byte/script coverage changed')
    for pkg,count,hash_count in zip(packages,[7,4,4],[6,3,0]):
        with ZipFile(ROOT/pkg['archive_path']) as z:
            need(z.testzip() is None, 'ZIP CRC failure')
            names = z.namelist()
            need(len(names) == len(set(names)) and len(pkg['members']) == count and
                 set(names) == {m['archive_member'] for m in pkg['members']} | set(pkg['directory_entries']),
                 'ZIP member coverage changed')
            for info in z.infolist():
                p = PurePosixPath(info.filename)
                need(not p.is_absolute() and '..' not in p.parts and '\\' not in info.filename and
                     not stat.S_ISLNK(info.external_attr>>16), 'unsafe ZIP path')
                if info.is_dir():
                    need(info.filename in pkg['directory_entries'], 'directory receipt mismatch')
                    continue
                item = next(m for m in pkg['members'] if m['archive_member'] == info.filename)
                need(z.read(info) == (ROOT/item['path']).read_bytes(), 'extracted member bytes changed')
            need(pkg['producer_hashes_checked'] == hash_count, 'producer manifest coverage changed')
            if hash_count:
                producer = load(pkg['producer_manifest_path'])['files']
                prefix = names[0].split('/',1)[0]+'/'
                need(len(producer) == hash_count and
                     {x.get('path',x.get('name')) for x in producer} ==
                     {m['archive_member'][len(prefix):] for m in pkg['members'] if m['path'] != pkg['producer_manifest_path']},
                     'producer manifest names changed')
                for item in producer:
                    data = z.read(prefix+item.get('path',item.get('name')))
                    need(sha(data) == item['sha256'] and len(data) == item['bytes'], 'producer member digest changed')
            else:
                need(pkg['producer_manifest_path'] is None and pkg['verification']['producer_member_manifest'].startswith('not supplied'),
                     'producer manifest invented')
    need({p.relative_to(ROOT).as_posix() for p in (ROOT/'updates/EJ/package').rglob('*') if p.is_file()} == set(indexed),
         'extra/missing archived disclosure')
    need(len(manifest['source_link_receipts']) == 3, 'citation receipt coverage changed')
    for item,count in zip(manifest['source_link_receipts'],[2,2,4]):
        data = (ROOT/item['path']).read_bytes()
        need(sha(data) == item['sha256'] and len(data) == item['bytes'], 'derived citation receipt changed')
        receipt = json.loads(data)
        need(receipt['classification'].startswith('derived source-page metadata') and
             receipt['source_url'].startswith('https://chatgpt.com/c/') and len(receipt['links']) == count,
             'citation metadata promoted to original proof')
        indexed[item['path']] = item
    return indexed


def check_status(status):
    route = status['card_id'].split('-',1)[0]
    need(status['claim_status'] == 'source_derived_unreviewed' and
         status['validation']['external_correctness'] == status['validation']['historical_priority'] == 'UNKNOWN',
         'scientific promotion')
    expected = {'N728':[], 'N729':['external:EJ_FER_TRANSFORM_AND_FLUID_CONTINUATION'],
                'N730':['N726-polyhedral-gaussian-crossing-witness-acquisition']}[route]
    need([x['target'] for x in status['depends_on']] == expected and
         all(status[k] == [] for k in ['supersedes','invalidates','contrasting_blockers']),
         'unsupported earlier-claim dependency or correction')
    updates = {'N728':['N725','N724'], 'N729':[], 'N730':['N726']}[route]
    need([x['target'].split('-',1)[0] for x in status['material_updates']] == updates,
         'scoped continuation coverage changed')
    if route == 'N730':
        need(status['depends_on'][0]['scope'].startswith('ONLY the infinite-spectrum algorithmic corollary') and
             'self-contained' in status['depends_on'][0]['scope'], 'conditional import scope erased')
    need(status['proof_availability']['classification'] ==
         'original_proof_accounts_and_recovered_producer_artifacts_not_independently_audited',
         'artifact recovery promoted to independent audit')


def check_trace(trace,route):
    duration,mode,relation = EXPECTED[route]
    resources = trace['resources']
    need(trace['mode'] == mode and trace['context']['conversation_relation'] == relation and
         trace['prompt_availability'] == 'exact' and trace['prompt_ref_ids'] == ['prompt'] and
         trace['status'] == 'completed', 'source workflow configuration changed')
    if route == 'N729':
        need(trace['context']['retained_context'] is None, 'retained conversation invented')
    need(resources['reported_inference_seconds'] == duration and resources['reported_duration_ref_ids'] == ['duration'],
         'reported duration provenance changed')
    need(all(v is None for v in trace['model'].values()) and
         all(v is None for v in resources['usage'].values()) and resources['worker_invocations'] is None and
         resources['worker_receipt_ref_ids'] == resources['usage_receipt_ref_ids'] == [],
         'unmeasured model/worker/usage telemetry invented')
    need(trace['matched_run_id'] is None and trace['advance']['verification'] == 'producer_reported' and
         trace['advance']['verification_receipt'] is None and
         trace['advance']['scientific_status'].startswith('source_derived_unreviewed;'),
         'producer output promoted to independent or matched evidence')


def check_families(fit):
    need(fit['base_revision'] == BASE and fit['relation_semantics'].startswith('Comparisons are navigation only;'),
         'family comparison promoted to proof relation')
    decisions = fit['decisions']
    need([x['card_id'].split('-',1)[0] for x in decisions] == list(EXPECTED), 'family coverage changed')
    need([{x['card_id'].split('-',1)[0] for x in d['comparisons']} for d in decisions] ==
         [{'N724','N725'},set(),{'N726','N493','N719','N708','N721'}], 'family comparison scope changed')
    known = {x['id'] for x in rows('indexes/claims.jsonl')}
    need(all(d['card_id'] in known and all(x['card_id'] in known and x['scope'] for x in d['comparisons'])
             for d in decisions), 'unknown family comparison target')


def check_notices(manifest):
    expected = {'SN-EJ-N725-N728-ACTIVE-ACCESS':('N725','N728'),
                'SN-EJ-N724-N728-NOMINAL-VECTOR-BRIDGE':('N724','N728'),
                'SN-EJ-N726-N730-CERTIFIED-TAIL-TRANSFER':('N726','N730')}
    need(manifest['reciprocal_continuation_notices'] == list(expected), 'reciprocal notice coverage changed')
    notices = rows('agent/SEMANTIC_NOTICES.jsonl')
    for nid,pair in expected.items():
        matches = [x for x in notices if x['notice_id'] == nid]
        need(len(matches) == 1, 'duplicate/missing reciprocal notice')
        n = matches[0]
        need(tuple(x.split('-',1)[0] for x in n['card_ids']) == pair and
             {x['target'] for x in n['material_updates']} == set(n['card_ids']) and
             n['status'] == 'source_derived_unreviewed_continuation_only' and n['source_revision'] == BASE,
             'reciprocal notice scope/status mismatch')
        for r in n['source_refs']:
            need(sha((ROOT/r['path']).read_bytes()) == r['sha256'], 'notice proof hash changed')
        for short in pair:
            dossier = (ROOT/('frontier/dossiers/'+short+'.txt')).read_text()
            connection = load('frontier/connections/'+short+'.json')
            need(nid in dossier and any(e['kind'] == 'material_update' and
                 e['composition'] == n['clarification'] for e in connection['edges']),
                 'reciprocal notice not retrievable')


def main():
    manifest = load('updates/EJ/SOURCE_MANIFEST.json'); mapping = load('updates/EJ/CLAIMS.json')
    need(manifest['intake_base_revision'] == mapping['base_revision'] == BASE and
         manifest['source_handling'] == 'source=DATA', 'base/source boundary changed')
    indexed = check_sources(manifest); check_families(load('updates/EJ/FAMILY_FIT.json')); check_notices(manifest)
    ledgers = {p:rows(p) for p in ['indexes/claims.jsonl','frontier/CURRENT_CLAIM_STATUS.jsonl',
                                  'indexes/source_metadata.jsonl','web/documents.jsonl']}
    for item in indexed.values():
        metadata = [x for x in ledgers['indexes/source_metadata.jsonl'] if x.get('source_id') == item['source_id']]
        docs = [x for x in ledgers['web/documents.jsonl'] if x['id'] == item['source_id']]
        need(len(metadata) == len(docs) == 1 and metadata[0]['sha256'] == item['sha256'] and
             metadata[0]['path'] == docs[0]['path'] == item['path'], 'source metadata mismatch')
        if 'lines' in item:
            need('<pre>'+html.escape((ROOT/item['path']).read_text())+'</pre>' in
                 (ROOT/('web/'+docs[0]['url'])).read_text(), 'source web mirror changed')
    need(len(mapping['claims']) == 3, 'card coverage changed')
    catalog = load('indexes/agent_catalog.json')['claims']; web = load('web/catalog.json')
    proof_count = 0; trace_paths = set(); cp_paths = set()
    for entry in mapping['claims']:
        cid = entry['id']; route = cid.split('-',1)[0]
        primary = indexed[entry['source_path']]
        need(entry['source_sha256'] == primary['sha256'] and entry['source_id'] == primary['source_id'] and
             entry['missing_artifacts'] == [], 'claim source or artifact coverage mismatch')
        status = load('frontier/cards/'+cid+'.json'); check_status(status)
        for pool,key in [(ledgers['frontier/CURRENT_CLAIM_STATUS.jsonl'],'card_id'),
                         (ledgers['indexes/claims.jsonl'],'id'),(catalog,'id'),(web,'id')]:
            need(sum(x[key] == cid for x in pool) == 1, 'duplicate/missing claim row')
        need(status == next(x for x in ledgers['frontier/CURRENT_CLAIM_STATUS.jsonl'] if x['card_id'] == cid),
             'status ledger disagreement')
        claim = next(x for x in ledgers['indexes/claims.jsonl'] if x['id'] == cid)
        need(entry['status'] == claim['status'] == status['claim_status'] and
             claim['depends_on'] == [d['target'] for d in status['depends_on']] and claim['scoped_dependencies'] == [],
             'claim dependency/status disagreement')
        wc = next(x for x in web if x['id'] == cid)
        need(wc['source_paths'] == claim['source_paths'] and wc['source_ids'] == claim['source_ids'], 'web provenance missing')
        card = (ROOT/status['card_path']).read_bytes()
        need(sha(card) == status['card_sha256'] == next(x for x in catalog if x['id'] == cid)['card_sha256'] and
             (ROOT/('frontier/review_cards/'+cid+'.txt')).read_bytes().endswith(card), 'card/wrapper disagreement')
        proofs = status['proof_availability']['located_proof_sources']; proof_count += len(proofs)
        for r in proofs+status['proof_availability']['available_evidence_sources']:
            item = indexed[r['path']]
            need(r['sha256'] == item['sha256'] and 1<=r['lines'][0]<=r['lines'][1]<=item['lines'],
                 'proof/source range invalid')
        need(cid+'\t' in (ROOT/'agent/routes.tsv').read_text(), 'claim route missing')
        for topic in status['topics']:
            need(cid+'\t' in (ROOT/('agent/topics/'+topic+'.tsv')).read_text(), 'topic route missing')
        gates = [g for g in rows('frontier/OPEN_PROOF_GATES.jsonl') if g['gate_id'] == 'G-EJ-'+route+'-INDEPENDENT-REVIEW']
        need(len(gates) == 1 and gates[0]['card_ids'] == [cid] and gates[0]['status'] == 'open' and
             gates[0]['completion_evidence'] == [], 'independent review gate closed/missing')
        trace = load(entry['workflow_trace']); validate_trace(trace,ROOT); check_trace(trace,route)
        cp = load(entry['checkpoint']); validate_record(cp,ROOT)
        need(cp['base_revision'] == BASE and cp['parent_checkpoint_ids'] == [] and
             cp['branch_id'].startswith('worker-ej-'), 'intake ancestry invented')
        generated = views(ROOT,{cp['branch_id']:{cp['checkpoint_id']:cp}})
        view = 'state/branches/'+cp['branch_id']+'.txt'
        need((ROOT/view).read_text() == generated[view], 'checkpoint view stale')
        row = next(r for r in generated['state/branches.tsv'].splitlines() if r.startswith(cp['branch_id']+'\t'))
        need((ROOT/'state/branches.tsv').read_text().splitlines().count(row) == 1, 'checkpoint registry mismatch')
        trace_paths.add(entry['workflow_trace']); cp_paths.add(entry['checkpoint'])
    need(proof_count == 51 and len(trace_paths) == len(cp_paths) == 3, 'source-range/attempt coverage changed')
    for path in list(ledgers)+['frontier/OPEN_PROOF_GATES.jsonl','state/branches.tsv','agent/routes.tsv','agent/SEMANTIC_NOTICES.jsonl']:
        need((ROOT/path).read_bytes().startswith(git('show',BASE+':'+path)), 'historical ledger rewritten')
    for path,fields in [('indexes/agent_catalog.json',['claims']),('indexes/agent_graph.json',['nodes','edges'])]:
        old,now = json.loads(git('show',BASE+':'+path)),load(path)
        for field in fields:
            need(now[field][:len(old[field])] == old[field], 'historical graph/catalog rewritten')
    graph = load('indexes/agent_graph.json'); node_ids = {n['id'] for n in graph['nodes']}
    need(len(node_ids) == len(graph['nodes']) and
         all(e['from'] in node_ids and e['to'] in node_ids for e in graph['edges']), 'graph integrity')
    for entry in mapping['claims']:
        claim = next(c for c in ledgers['indexes/claims.jsonl'] if c['id'] == entry['id'])
        need(set(claim['source_ids']) == {e['to'] for e in graph['edges']
             if e['from'] == entry['id'] and e['kind'] == 'provenance'}, 'claim provenance missing')
    old_aliases = json.loads(git('show',BASE+':indexes/query_aliases.json'))
    need(all(load('indexes/query_aliases.json').get(k) == v for k,v in old_aliases.items()), 'earlier alias changed')
    old_paths = set(git('ls-tree','-r','--name-only',BASE).decode().splitlines())
    changed = set(git('diff','--name-only',BASE,'--','updates','cards','frontier/cards','state/checkpoints',
                      'state/branches','evaluation','technology/records').decode().splitlines())
    need(not changed & old_paths, 'earlier scientific/source/checkpoint/evaluation object changed')
    outputs = json.loads(git('show',BASE+':agent/access_manifest.json'))['outputs']
    scientific = {p:d for p,d in outputs.items() if p.startswith(('frontier/dossiers/','frontier/connections/','frontier/proof_ranges/'))}
    changed_routes = {p for p,d in scientific.items() if not (ROOT/p).is_file() or sha((ROOT/p).read_bytes()) != d}
    allowed = {p for n in ['N724','N725','N726'] for p in ['frontier/dossiers/'+n+'.txt','frontier/connections/'+n+'.json']}
    need(set(manifest['permitted_historical_navigation_changes']) == changed_routes == allowed,
         'earlier scientific navigation changed beyond exact scoped notices')
    print(json.dumps(dict(intake='EJ',status='PASS',original_files=21,original_bytes=222865,
          exact_pastes=3,pasted_bytes=62609,zip_archives=3,archive_members=15,standalone_files=0,
          producer_member_hashes_checked=9,derived_citation_receipts=3,mechanism_cards=3,proof_ranges=51,
          observational_traces=3,record_level_checkpoints=3,unchanged_earlier_scientific_routes=len(scientific)-len(allowed),scoped_notice_navigation_updates=len(allowed),
          scientific_scripts_syntax_parsed_only=4,scientific_scripts_executed=0,
          scientific_verification='not performed'),sort_keys=True))


if __name__ == '__main__':
    try:
        main()
    except (ValueError,OSError,KeyError,subprocess.CalledProcessError) as error:
        raise SystemExit(str(error))
