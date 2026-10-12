#!/usr/bin/env python3
"""Deterministic EH archive/navigation guards. Never executes scientific scripts."""
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

BASE = '01eda4be0686e9fe4dc650af7137efc3c88ba0fb'
EXPECTED = {'N724':(2240,'fresh_direction_retained_context','same'),
            'N725':(2612,'independent_selective_capital','UNKNOWN'),
            'N726':(3239,'fresh_direction_retained_context','same')}
PINS = {'updates/EH/package/genesis_scalar_horizon/ORIGINAL_PASTED_SOURCE.txt': '712b239d261bbf1576e8115a167394ea1c59c9d2db739032fef356de7400b23d', 'updates/EH/package/theoretical_quantum_snapshot/ORIGINAL_PASTED_SOURCE.txt': '21c9dce45c4a489ce60266906217da19233bd5108bb61009a971f2f9c0471cad', 'updates/EH/package/computational_gaussian_crossings/ORIGINAL_PASTED_SOURCE.txt': '15a6f9d2ab6d8695eccbc42edbde5d2e349f92f32bfdd43cd1ab0a7904eab44a', 'updates/EH/package/computational_gaussian_crossings/recovered/verify_crossing.py': '3da4982db2f9d7da316f15a25634e532296ba17a9cf6e89ffd57bc973ee4ea13', 'updates/EH/package/computational_gaussian_crossings/recovered/verification_results.json': 'c243761988dc452042f2f512391cef217bc25539f09ac794813576839f655e2a', 'updates/EH/package/genesis_scalar_horizon/astra_spectral_horizon.zip': 'd44435105d3ea3f4ca58ab646c0c58ede25ee6bb9ad268d330e6afed9e713438', 'updates/EH/package/genesis_scalar_horizon/recovered/astra_spectral_horizon/MANIFEST.json': '7c0a4d9bb936f10a534e1c772ebfceb548a87207aef355558ca44bb9abef84c1', 'updates/EH/package/genesis_scalar_horizon/recovered/astra_spectral_horizon/RESULT.md': 'f0d1669c7d2a17888254bc24c4bba4ba9b318584f3972728dc2daf5abcbddf72', 'updates/EH/package/genesis_scalar_horizon/recovered/astra_spectral_horizon/exact_models.json': '2839bdf2525216034e8347c481bd8e9989b28675d0249b9ef6c656d21430d381', 'updates/EH/package/genesis_scalar_horizon/recovered/astra_spectral_horizon/results.json': '4d55a9afd804495b75ea4924b54e088e013684b954a1eec0da4ab47248c50e14', 'updates/EH/package/genesis_scalar_horizon/recovered/astra_spectral_horizon/verify.py': 'b0cf3164e44b54bd17089d8ded5bf7680acda9d2a4c2d3d7b3abba4acc994fed', 'updates/EH/package/theoretical_quantum_snapshot/astra_imaginary_time_prediction_2026-10-12.zip': 'dbb07ceeb779f809a8f3e5cb7bffc4002b3a29df8f73a8d42a881a068342c91c', 'updates/EH/package/theoretical_quantum_snapshot/recovered/astra_euclidean/README.md': '7268a1448323693171a4fc3cc8f3436c910cb454f2e9c1e6a8eae598f1c68f7e', 'updates/EH/package/theoretical_quantum_snapshot/recovered/astra_euclidean/check_construction.py': 'c582f9b58bf10a39fdc2e004ca53d2a7068929b9ef86c02c428f95a8d87c99cf', 'updates/EH/package/theoretical_quantum_snapshot/recovered/astra_euclidean/check_results.json': '503078d90964e32950d2ba76046464cbf384573613afa1d8971481e16d0653fd', 'updates/EH/package/theoretical_quantum_snapshot/recovered/astra_euclidean/manifest.json': '38cb1d58227f2a9a0c11d4653565b358b2d6000dcf69696a73e9a301c541de8f', 'updates/EH/package/theoretical_quantum_snapshot/recovered/astra_euclidean/requirements.txt': '68a798d14ab7ceac5f914897b07fd7053ddfd40acabcd6c79e6ba7677e874b13', 'updates/EH/package/theoretical_quantum_snapshot/recovered/astra_euclidean/research_note.md': 'ed86c28e5179b9987ea6e5a68741e20076699be93897dc3a06d57741eb147af1'}


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
    need(len(manifest['originals']) == 3 and sum(x['bytes'] for x in manifest['originals']) == 72562,
         'pasted source coverage/extent changed')
    packages = manifest['recovered_packages']
    need(len(packages) == 2 and len(manifest['recovered_files']) == 2,
         'archive/standalone coverage changed')
    source_rows = manifest['originals']+manifest['recovered_files']
    for pkg in packages:
        source_rows += [pkg]+pkg['members']
    indexed = {x['path']:x for x in source_rows}
    need(len(indexed) == len(source_rows) == 18 and set(indexed) == set(PINS),
         'original source identities changed')
    scripts = 0
    for path,item in indexed.items():
        data = (ROOT/path).read_bytes()
        need(sha(data) == item['sha256'] == PINS[path] and len(data) == item['bytes'],
             'original bytes/hash changed')
        if 'lines' in item:
            need(len(data.decode().splitlines()) == item['lines'], 'source extent changed')
        if path.endswith('.py'):
            ast.parse(data,filename=path)
            scripts += 1
    need(scripts == 3 and sum(x['bytes'] for x in indexed.values()) == 200324,
         'original byte/script coverage changed')
    for pkg in packages:
        with ZipFile(ROOT/pkg['archive_path']) as z:
            need(z.testzip() is None, 'ZIP CRC failure')
            names = z.namelist()
            need(len(names) == len(set(names)) == len(pkg['members']) and
                 set(names) == {m['archive_member'] for m in pkg['members']}, 'ZIP member coverage changed')
            for info in z.infolist():
                p = PurePosixPath(info.filename)
                need(not p.is_absolute() and '..' not in p.parts and '\\' not in info.filename and
                     not info.is_dir() and not stat.S_ISLNK(info.external_attr>>16), 'unsafe ZIP path')
                item = next(m for m in pkg['members'] if m['archive_member'] == info.filename)
                need(z.read(info) == (ROOT/item['path']).read_bytes(), 'extracted member bytes changed')
            producer = load(pkg['producer_manifest_path'])
            if 'files' in producer:
                producer = producer['files']
            need(len(producer) == pkg['producer_hashes_checked'] == len(names)-1,
                 'producer manifest coverage changed')
            prefix = names[0].split('/',1)[0]+'/'
            need(set(producer) == {m['archive_member'].split('/',1)[1] for m in pkg['members']
                                  if m['path'] != pkg['producer_manifest_path']},
                 'producer manifest names changed')
            for name,digest in producer.items():
                need(sha(z.read(prefix+name)) == digest, 'producer member digest changed')
    need({p.relative_to(ROOT).as_posix() for p in (ROOT/'updates/EH/package').rglob('*') if p.is_file()} ==
         set(indexed), 'extra/missing archived disclosure')
    need(len(manifest['source_link_receipts']) == 3, 'citation receipt coverage changed')
    for item in manifest['source_link_receipts']:
        data = (ROOT/item['path']).read_bytes()
        need(sha(data) == item['sha256'] and len(data) == item['bytes'], 'derived citation receipt changed')
        receipt = json.loads(data)
        need(receipt['classification'].startswith('derived source-page metadata') and
             receipt['source_url'].startswith('https://chatgpt.com/c/') and len(receipt['links']) == 5,
             'citation metadata promoted to original proof')
        indexed[item['path']] = item
    return indexed


def check_status(status):
    route = status['card_id'].split('-',1)[0]
    need(status['claim_status'] == 'source_derived_unreviewed' and
         status['validation']['external_correctness'] == status['validation']['historical_priority'] == 'UNKNOWN',
         'scientific promotion')
    imports = [] if route != 'N726' else ['external:EH_RICE_PALM_CROSSING_DISINTEGRATION',
                                         'external:EH_CONVEX_BODY_BIT_INTEGRATION_SAMPLING']
    need([x['target'] for x in status['depends_on']] == imports and
         all(status[k] == [] for k in ['supersedes','invalidates','material_updates','contrasting_blockers']),
         'unsupported earlier-claim dependency or correction')
    need(status['proof_availability']['classification'] ==
         'original_proof_accounts_and_recovered_producer_artifacts_not_independently_audited',
         'artifact recovery promoted to independent audit')


def check_trace(trace,route):
    duration,mode,relation = EXPECTED[route]
    resources = trace['resources']
    need(trace['mode'] == mode and trace['context']['conversation_relation'] == relation and
         trace['prompt_availability'] == 'exact' and trace['prompt_ref_ids'] == ['prompt'] and
         trace['status'] == 'completed', 'source workflow configuration changed')
    if route == 'N725':
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
    need(fit['base_revision'] == BASE and fit['relation_semantics'].startswith('Navigation comparison only;'),
         'family comparison promoted to proof relation')
    decisions = fit['decisions']
    need([x['card_id'].split('-',1)[0] for x in decisions] == list(EXPECTED), 'family coverage changed')
    need([{x['card_id'].split('-',1)[0] for x in d['comparisons']} for d in decisions] ==
         [{'N725','N95','N99','N711','N712'}, {'N724','N716','N711','N712'},
          {'N492','N493','N715','N719','N708','N721'}], 'family comparison scope changed')
    known = {x['id'] for x in rows('indexes/claims.jsonl')}
    need(all(d['card_id'] in known and all(x['card_id'] in known and x['scope'] for x in d['comparisons'])
             for d in decisions), 'unknown family comparison target')


def main():
    manifest = load('updates/EH/SOURCE_MANIFEST.json'); mapping = load('updates/EH/CLAIMS.json')
    need(manifest['intake_base_revision'] == mapping['base_revision'] == BASE and
         manifest['source_handling'] == 'source=DATA', 'base/source boundary changed')
    indexed = check_sources(manifest); check_families(load('updates/EH/FAMILY_FIT.json'))
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
        gates = [g for g in rows('frontier/OPEN_PROOF_GATES.jsonl') if g['gate_id'] == 'G-EH-'+route+'-INDEPENDENT-REVIEW']
        need(len(gates) == 1 and gates[0]['card_ids'] == [cid] and gates[0]['status'] == 'open' and
             gates[0]['completion_evidence'] == [], 'independent review gate closed/missing')
        trace = load(entry['workflow_trace']); validate_trace(trace,ROOT); check_trace(trace,route)
        cp = load(entry['checkpoint']); validate_record(cp,ROOT)
        need(cp['base_revision'] == BASE and cp['parent_checkpoint_ids'] == [] and
             cp['branch_id'].startswith('worker-eh-'), 'intake ancestry invented')
        generated = views(ROOT,{cp['branch_id']:{cp['checkpoint_id']:cp}})
        view = 'state/branches/'+cp['branch_id']+'.txt'
        need((ROOT/view).read_text() == generated[view], 'checkpoint view stale')
        row = next(r for r in generated['state/branches.tsv'].splitlines() if r.startswith(cp['branch_id']+'\t'))
        need((ROOT/'state/branches.tsv').read_text().splitlines().count(row) == 1, 'checkpoint registry mismatch')
        trace_paths.add(entry['workflow_trace']); cp_paths.add(entry['checkpoint'])
    need(proof_count == 31 and len(trace_paths) == len(cp_paths) == 3, 'source-range/attempt coverage changed')
    for path in list(ledgers)+['frontier/OPEN_PROOF_GATES.jsonl','state/branches.tsv','agent/routes.tsv']:
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
    need(manifest['permitted_historical_navigation_changes'] == [] and
         all((ROOT/p).is_file() and sha((ROOT/p).read_bytes()) == d for p,d in scientific.items()),
         'earlier scientific navigation changed')
    print(json.dumps(dict(intake='EH',status='PASS',original_files=18,original_bytes=200324,
          exact_pastes=3,pasted_bytes=72562,zip_archives=2,archive_members=11,standalone_files=2,
          producer_member_hashes_checked=9,derived_citation_receipts=3,mechanism_cards=3,proof_ranges=31,
          observational_traces=3,record_level_checkpoints=3,unchanged_earlier_scientific_routes=len(scientific),
          scientific_scripts_syntax_parsed_only=3,scientific_scripts_executed=0,
          scientific_verification='not performed'),sort_keys=True))


if __name__ == '__main__':
    try:
        main()
    except (ValueError,OSError,KeyError,subprocess.CalledProcessError) as error:
        raise SystemExit(str(error))
