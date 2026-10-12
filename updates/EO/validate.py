#!/usr/bin/env python3
"""Deterministic EO archive/navigation guards. Never executes scientific scripts."""
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

BASE = 'a33fc7e1db8f42873025fa29882f85f2d4503695'
EXPECTED = {'N745':(2761,'independent_selective_capital','UNKNOWN'), 'N746':(3108,'fresh_direction_retained_context','same'), 'N747':(3644,'targeted_warm_continuation','same')}
PINS = {'updates/EO/package/genesis_boolean_cancellation/ORIGINAL_PASTED_SOURCE.txt': '2106793a213f8a201681e5b6facdecb4c652b583771da9260ae8f50510032741', 'updates/EO/package/cray_analytic_anchor/ORIGINAL_PASTED_SOURCE.txt': 'ee92f8d479531b7b87ed912203359321cbde658cb0575384a5db6caee024ca45', 'updates/EO/package/frontier_balanced_transport/ORIGINAL_PASTED_SOURCE.txt': '68cfef4a8b074e461efb52a918fee3cbb6481dfb478193d59e7e3ea2653b1360', 'updates/EO/package/genesis_boolean_cancellation/astra_boolean_cancellation_research.zip': '0ffade6c9c8b845e24130edff75900e801acf81980ede2902b4d968c7f440a4d', 'updates/EO/package/genesis_boolean_cancellation/recovered/astra_boolean_cancellation/RESEARCH_RECORD.md': '469489415c211533b71c6ebfe7dc95cbbff2ba0b48852e89de5d0708cb7f43b3', 'updates/EO/package/genesis_boolean_cancellation/recovered/astra_boolean_cancellation/verify.py': 'fde378719ea6b634b1b51cfcd4e7def3671934e9727b7cb94a9eea7b72aadcfd', 'updates/EO/package/genesis_boolean_cancellation/recovered/astra_boolean_cancellation/VERIFICATION.json': '1addfa608f18d3b5e6c232bfe2d74306022e7a0537ddb434150950297beb6580', 'updates/EO/package/genesis_boolean_cancellation/recovered/astra_boolean_cancellation/MANIFEST.json': 'bda0cbe1734f60d0f25c0f2970a635dcade1395f06b452357a2ccc82cce6edde', 'updates/EO/package/cray_analytic_anchor/cray_anchored_complex_transport_2026-10-12.zip': 'f8c8cb340a4ac3fcc8bdf6ed59b3d972663cbeb668910a00315c7db033e3128d', 'updates/EO/package/cray_analytic_anchor/recovered/cray_anchored_complex_transport_2026-10-12/CLAIMS.json': '2c1590129ee0751c2ac3219a3bdc0c38685930e2483b0d6f4569a34a90c19278', 'updates/EO/package/cray_analytic_anchor/recovered/cray_anchored_complex_transport_2026-10-12/IMPLEMENTATION_LOG.md': '5eb7e164437642deeecb4a087d9474ff2b0aadaf66ce92e49855518ce7c3f7a1', 'updates/EO/package/cray_analytic_anchor/recovered/cray_anchored_complex_transport_2026-10-12/MANIFEST.json': '5e10e5d68824fe3ccae36f3b102168676db4b14953e46b1f084b1c3641b3b6fe', 'updates/EO/package/cray_analytic_anchor/recovered/cray_anchored_complex_transport_2026-10-12/README.md': '924e73229f75528cf687d445e67ffa86cb4f05bfb5e9a9cb02872862c1092daa', 'updates/EO/package/cray_analytic_anchor/recovered/cray_anchored_complex_transport_2026-10-12/RESEARCH_NOTE.md': '767c34891eb855346e1bce800d65076f39db0de73b6cc4756dd3edeebb7468cb', 'updates/EO/package/cray_analytic_anchor/recovered/cray_anchored_complex_transport_2026-10-12/RESTART.md': 'f0aa835d430568f4fc0052336ba938e166a62f6dcd7d61d5093cfef13234e26d', 'updates/EO/package/cray_analytic_anchor/recovered/cray_anchored_complex_transport_2026-10-12/SOURCES.md': '54e06ca4909f424f7746cb0eb23685349e8d503e145b498a4c4bfd6c847434fd', 'updates/EO/package/cray_analytic_anchor/recovered/cray_anchored_complex_transport_2026-10-12/audit.py': 'e8f91ff433fda50740e0552c5d8b18934b9ee367d4a43814a3bceb20a9fb704a', 'updates/EO/package/cray_analytic_anchor/recovered/cray_anchored_complex_transport_2026-10-12/audit_results.json': 'bcfa43fc8f014ba0055921901b3f8216283533447d281f5b6b4f7e2290ff62aa', 'updates/EO/package/cray_analytic_anchor/recovered/cray_anchored_complex_transport_2026-10-12/audit_stdout.txt': 'bcfa43fc8f014ba0055921901b3f8216283533447d281f5b6b4f7e2290ff62aa', 'updates/EO/package/cray_analytic_anchor/recovered/cray_anchored_complex_transport_2026-10-12/connected_results.json': '633d35ab962f3c96a6728606ec889c9610bce49a1e7432e7de12edd17aeee5ee', 'updates/EO/package/cray_analytic_anchor/recovered/cray_anchored_complex_transport_2026-10-12/connected_test.py': 'c1290fd664a2c98b2bee1109563170ddde1eed057e4d27c7adbf4a990c31cb84', 'updates/EO/package/cray_analytic_anchor/recovered/cray_anchored_complex_transport_2026-10-12/environment.json': '0f1e68af43c9b7bcf61673541ab49a2b3f841dbf6326dea18dd21044be37f5fd', 'updates/EO/package/cray_analytic_anchor/recovered/cray_anchored_complex_transport_2026-10-12/experiment.py': 'a1a54bb5bafc022484b11459b2dc494c5cd113284371de32ea454d7ec94a4788', 'updates/EO/package/cray_analytic_anchor/recovered/cray_anchored_complex_transport_2026-10-12/results_h_0.005.json': '5aa20536d3694d1742fa658360b183e676ede235b5c01dbcb6d1d2a38056b3ea', 'updates/EO/package/cray_analytic_anchor/recovered/cray_anchored_complex_transport_2026-10-12/results_h_0.01.json': 'b792e8beb3ca05a6c12dc9316a3af78ac9183dd5e6e319a8e3d9fadb7204702c', 'updates/EO/package/cray_analytic_anchor/recovered/cray_anchored_complex_transport_2026-10-12/results_h_0.02.json': '2a2ce211d6cda93c76d90427c7e1e8302c33158099aad8327a6957b0687a4850', 'updates/EO/package/frontier_balanced_transport/astra_frontier_balanced_transport.zip': '8773a9c77f539b6af8931eb2372116320f8ca7dc4bc1ce744810d660f83ac08e', 'updates/EO/package/frontier_balanced_transport/recovered/astra_frontier_balanced_transport/README.md': 'c11d1130b82fa661a938ef6d3978a0cda149ec74782d35246031efefb04063e0', 'updates/EO/package/frontier_balanced_transport/recovered/astra_frontier_balanced_transport/block_checks.json': 'ab4d56029304e70e8b243c2217eaf900cdbb8b6a28758cba5c7c1ad06c2fa4df', 'updates/EO/package/frontier_balanced_transport/recovered/astra_frontier_balanced_transport/block_checks.py': '5c018fe96cec3a8016ea803832a41680a7389bd1321a3de3df9e88bfc96d1a67', 'updates/EO/package/frontier_balanced_transport/recovered/astra_frontier_balanced_transport/checkpoint.md': '5e5e035a328847f3b29b60e404b6ba7478fb1d489fb6d12e13ba360008e727db', 'updates/EO/package/frontier_balanced_transport/recovered/astra_frontier_balanced_transport/checks.json': '7ac5f47893d58e77c19af483d36cd77cd15e4482e0a47b1761a221456167618b', 'updates/EO/package/frontier_balanced_transport/recovered/astra_frontier_balanced_transport/environment.json': '192e9230560eadfe2c34a41fad27d31a04194fbac3a747e043bf2ae323cc01ba', 'updates/EO/package/frontier_balanced_transport/recovered/astra_frontier_balanced_transport/experiments.py': '744c8fc90542d0085034838a9f42fd02c88584db5987ac3c1f74882bc8e27ebc', 'updates/EO/package/frontier_balanced_transport/recovered/astra_frontier_balanced_transport/larger_checks.json': '0ee244c60b8ac7ad3ba685633b78858019b1fb3d590e0375ad8195788a2ffe9a', 'updates/EO/package/frontier_balanced_transport/recovered/astra_frontier_balanced_transport/larger_checks.py': 'a32513a58fa85bf372c839377df942cd50cb9cee01bff3f5427b782c71adfb78', 'updates/EO/package/frontier_balanced_transport/recovered/astra_frontier_balanced_transport/noise_response.py': 'b4d8dc85ab4eda992b467ece188621089489cdc80ed0c16563c06b06d6872ae8', 'updates/EO/package/frontier_balanced_transport/recovered/astra_frontier_balanced_transport/noise_response_checks.json': '0d4dfb600aa5d257eb93ac09dee3f0287f5c0ae27fb2e064cf47a6766afd24b8', 'updates/EO/package/frontier_balanced_transport/recovered/astra_frontier_balanced_transport/pauli_core.py': '880e55619b4b14ca2cf8a478dc4675ed9744fd7b9de20bc23c2dc3c537bbd0af', 'updates/EO/package/frontier_balanced_transport/recovered/astra_frontier_balanced_transport/ramsey_certificate.py': '63a36fd972e39c3b54db18aac0f9c9444e79f80c5d841826b96eda0a575d5efa', 'updates/EO/package/frontier_balanced_transport/recovered/astra_frontier_balanced_transport/ramsey_checks.json': '0661b7c521bea664da033f95bdaa6b8201c3f90d07054913af1af803d1deb2b8', 'updates/EO/package/frontier_balanced_transport/recovered/astra_frontier_balanced_transport/research_note.md': '9f7201106cd1c38964ef8be73a33b284ec096f4c1ef9c17aa72e3e69b634f11c', 'updates/EO/package/frontier_balanced_transport/recovered/astra_frontier_balanced_transport/run_blocks.log': 'd062df003eb5f300fe31ae0dc9c4261971b6f2fa7ceac8c09d936d66e99a133d', 'updates/EO/package/frontier_balanced_transport/recovered/astra_frontier_balanced_transport/run_larger.log': '5cd61f3fa4f1bb118c2eee70a807bdd9a10ecd1ec9e7277cb93b5301895194d1', 'updates/EO/package/frontier_balanced_transport/recovered/astra_frontier_balanced_transport/run_main.log': 'ea30226598cb7e5a135ad3079cdda93fe794b06031c850735dc9a892641c8bef', 'updates/EO/package/frontier_balanced_transport/recovered/astra_frontier_balanced_transport/run_noise.log': '36fbcfecf997807ef010b3d8d3ef5bcf886fbe16894732878277511ee9c0642e', 'updates/EO/package/frontier_balanced_transport/recovered/astra_frontier_balanced_transport/run_ramsey.log': 'f5f99f5c59b9ac4c6cddcef54f5033d66343b31e2b42b1fda874d2cea3376a81', 'updates/EO/package/frontier_balanced_transport/recovered/astra_frontier_balanced_transport/sources.json': '5a48831fe28d5aff7c996e4747b6b8b4a9da2d8bf7b89940dbf270823b71ea8a', 'updates/EO/package/frontier_balanced_transport/recovered/astra_frontier_balanced_transport/manifest.json': '11a2fc80f535d2f46844f329d29502fcc7675ea93aed9e19b6ec6770950f7dd6'}


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
    need(len(manifest['originals']) == 3 and sum(x['bytes'] for x in manifest['originals']) == 68581,
         'pasted source coverage/extent changed')
    packages = manifest['recovered_packages']
    need(len(packages) == 3 and manifest['recovered_files'] == manifest['source_link_receipts'] == [], 'archive coverage changed')
    source_rows = manifest['originals'] + sum(([p]+p['members'] for p in packages), [])
    indexed = {x['path']:x for x in source_rows}
    need(len(indexed) == len(source_rows) == 49 and set(indexed) == set(PINS), 'original source identities changed')
    scripts = 0
    for path,item in indexed.items():
        data = (ROOT/path).read_bytes()
        need(sha(data) == item['sha256'] == PINS[path] and len(data) == item['bytes'], 'original bytes/hash changed')
        if 'lines' in item:
            need(len(data.decode().splitlines()) == item['lines'], 'source extent changed')
        if path.endswith('.py'):
            ast.parse(data,filename=path)
            scripts += 1
    need(scripts == 10 and sum(x['bytes'] for x in indexed.values()) == 399569, 'original byte/script coverage changed')
    for pkg,count,hash_count in zip(packages,[4,17,22],[3,16,21]):
        with ZipFile(ROOT/pkg['archive_path']) as z:
            need(z.testzip() is None, 'ZIP CRC failure')
            names = z.namelist()
            need(len(names) == len(set(names)) and len(pkg['members']) == count and
                 set(names) == {m['archive_member'] for m in pkg['members']} | set(pkg['directory_entries']),
                 'ZIP member coverage changed')
            for info in z.infolist():
                p = PurePosixPath(info.filename)
                need(not p.is_absolute() and '..' not in p.parts and chr(92) not in info.filename and
                     not stat.S_ISLNK(info.external_attr>>16), 'unsafe ZIP path')
                if info.is_dir():
                    need(info.filename in pkg['directory_entries'], 'directory receipt mismatch')
                    continue
                item = next(m for m in pkg['members'] if m['archive_member'] == info.filename)
                need(z.read(info) == (ROOT/item['path']).read_bytes(), 'extracted member bytes changed')
            need(pkg['producer_hashes_checked'] == hash_count, 'producer manifest coverage changed')
            producer = load(pkg['producer_manifest_path'])
            producer = producer.get('files',producer.get('payloads',producer.get('sha256',producer)))
            if isinstance(producer,dict):
                producer = [dict(path=k,**v) if isinstance(v,dict) else dict(path=k,sha256=v) for k,v in producer.items()]
            mname = next(m['archive_member'] for m in pkg['members'] if m['path'] == pkg['producer_manifest_path'])
            prefix = mname.rsplit('/',1)[0]+'/' if '/' in mname else ''
            need(len(producer) == hash_count and
                 {x['path'] for x in producer} ==
                 {m['archive_member'][len(prefix):] for m in pkg['members'] if m['path'] != pkg['producer_manifest_path']},
                 'producer manifest names changed')
            for item in producer:
                data = z.read(prefix+item['path'])
                need(sha(data) == item['sha256'] and ('bytes' not in item or len(data) == item['bytes']), 'producer member digest changed')
            need(pkg['verification']['scientific_code_execution'] == pkg['verification']['independent_proof_review'] == 'not performed',
                 'integrity promoted to scientific replay')
    need({p.relative_to(ROOT).as_posix() for p in (ROOT/'updates/EO/package').rglob('*') if p.is_file()} == set(indexed),
         'extra/missing archived disclosure')
    return indexed


def check_status(status):
    route = status['card_id'].split('-',1)[0]
    need(status['claim_status'] == 'source_derived_unreviewed' and
         status['validation']['external_correctness'] == status['validation']['historical_priority'] == 'UNKNOWN',
         'scientific promotion')
    expected = {'N745':['external:EO_BOOLEAN_RECTANGLE_BASELINES'],
                'N746':['external:EO_COMPLEX_LANGEVIN_ANALYTIC_BASELINES'],
                'N747':['external:EO_DISSIPATIVE_TRANSPORT_BASELINES']}[route]
    need([x['target'] for x in status['depends_on']] == expected and
         all(status[k] == [] for k in ['supersedes','invalidates','contrasting_blockers']),
         'unsupported earlier-claim dependency or correction')
    need([x['target'].split('-',1)[0] for x in status['material_updates']] == (['N742'] if route == 'N747' else []),
         'scoped continuation coverage changed')
    need(status['proof_availability']['classification'] ==
         'original_proof_accounts_and_recovered_producer_artifacts_not_independently_audited',
         'artifact recovery promoted to independent audit')


def check_trace(trace,route):
    duration,mode,relation = EXPECTED[route]
    resources = trace['resources']
    need(trace['mode'] == mode and trace['context']['conversation_relation'] == relation and
         trace['prompt_availability'] == 'exact' and trace['prompt_ref_ids'] == ['prompt'] and
         trace['status'] == 'completed', 'source workflow configuration changed')
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
         [{'N642'},{'N741','N744'},{'N742','N744'}], 'family comparison scope changed')
    known = {x['id'] for x in rows('indexes/claims.jsonl')}
    need(all(d['card_id'] in known and all(x['card_id'] in known and x['scope'] for x in d['comparisons'])
             for d in decisions), 'unknown family comparison target')


def check_notices(manifest):
    expected = {'SN-EO-N742-N747-CHANGED-ACCESS-AND-OUTPUT':('N742','N747')}
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


def check_capability_gate(gate,route):
    need(gate['gate_id'] == 'G-EO-'+route+'-CAPABILITY' and gate['status'] == 'open' and
         gate['completion_evidence'] == [] and gate['card_ids'][0].startswith(route+'-'),
         'unproved capability gate promoted or removed')
    required = {
        'N745':['global_predicate_synthesis','amortized_partition_bound','explicit_representation_cost'],
        'N746':['correct_integral_anchor','finite_bit_error_budget','matched_nonfactorizing_comparator','target_preserving_geometry'],
        'N747':['balanced_witness_representation_bound','pressure_and_bit_cost','quantitative_finite_size_transfer','physical_model_and_assay_errors']}
    need(gate['required_obligations'] == required[route], 'capability obligations erased')
    boundaries = {
        'N745':['equal sharing','2^{Omega(sqrt(n))}','not a general partition lower bound'],
        'N746':['unexecuted sufficient upper recipe','not a necessary lower bound','comparator wins'],
        'N747':['synthetic','not Gaussian hydrodynamics','N742 lower bound remains valid']}
    need(all(s in gate['validation_boundary'] for s in boundaries[route]), 'scientific boundary erased')


def check_projection(old_text,new_text,old_connection,new_connection,notice):
    block = 'SEMANTIC NOTICE '+notice['notice_id']+'\n'+notice['status']+': '+notice['clarification']+'\n\n'
    need(new_text.count(block) == 1, 'scoped notice projection missing/duplicated')
    normalize = lambda text: '\n'.join(line for line in text.splitlines() if not line.startswith('snapshot_input_sha256='))
    need(normalize(new_text.replace(block,'')) == normalize(old_text), 'historical dossier content altered beyond notice')
    earlier,later = notice['card_ids']
    wanted = [e for e in new_connection['edges'] if e['from'] == later and e['to'] == earlier and e['kind'] == 'material_update']
    need(len(wanted) == 1 and wanted[0]['composition'] == notice['clarification'], 'scoped connection projection missing/duplicated')
    projected = dict(new_connection)
    projected['edges'] = [e for e in new_connection['edges'] if e != wanted[0]]
    projected['nodes'] = [n for n in new_connection['nodes'] if n['id'] != later]
    projected['snapshot'] = dict(new_connection['snapshot'],input_sha256=old_connection['snapshot']['input_sha256'])
    need(projected == old_connection, 'historical connection content altered beyond notice')


def main():
    manifest = load('updates/EO/SOURCE_MANIFEST.json'); mapping = load('updates/EO/CLAIMS.json')
    need(manifest['intake_base_revision'] == mapping['base_revision'] == BASE and
         manifest['source_handling'] == 'source=DATA', 'base/source boundary changed')
    indexed = check_sources(manifest); check_families(load('updates/EO/FAMILY_FIT.json')); check_notices(manifest)
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
        gates = [g for g in rows('frontier/OPEN_PROOF_GATES.jsonl') if g['gate_id'] == 'G-EO-'+route+'-INDEPENDENT-REVIEW']
        need(len(gates) == 1 and gates[0]['card_ids'] == [cid] and gates[0]['status'] == 'open' and
             gates[0]['completion_evidence'] == [], 'independent review gate closed/missing')
        trace = load(entry['workflow_trace']); validate_trace(trace,ROOT); check_trace(trace,route)
        cp = load(entry['checkpoint']); validate_record(cp,ROOT)
        need(cp['base_revision'] == BASE and cp['parent_checkpoint_ids'] == [] and
             cp['branch_id'].startswith('worker-eo-'), 'intake ancestry invented')
        generated = views(ROOT,{cp['branch_id']:{cp['checkpoint_id']:cp}})
        view = 'state/branches/'+cp['branch_id']+'.txt'
        need((ROOT/view).read_text() == generated[view], 'checkpoint view stale')
        row = next(r for r in generated['state/branches.tsv'].splitlines() if r.startswith(cp['branch_id']+'\t'))
        need((ROOT/'state/branches.tsv').read_text().splitlines().count(row) == 1, 'checkpoint registry mismatch')
        trace_paths.add(entry['workflow_trace']); cp_paths.add(entry['checkpoint'])
    need(proof_count == 29 and len(trace_paths) == len(cp_paths) == 3, 'source-range/attempt coverage changed')
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
    allowed = {p for n in ['N742'] for p in ['frontier/dossiers/'+n+'.txt','frontier/connections/'+n+'.json']}
    need(set(manifest['permitted_historical_navigation_changes']) == changed_routes == allowed,
         'earlier scientific navigation changed beyond exact scoped notices')
    for route in EXPECTED:
        gate = next(g for g in rows('frontier/OPEN_PROOF_GATES.jsonl') if g['gate_id'] == 'G-EO-'+route+'-CAPABILITY')
        check_capability_gate(gate,route)
    notice = next(n for n in rows('agent/SEMANTIC_NOTICES.jsonl') if n['notice_id'] == manifest['reciprocal_continuation_notices'][0])
    check_projection(git('show',BASE+':frontier/dossiers/N742.txt').decode(), (ROOT/'frontier/dossiers/N742.txt').read_text(),
                     json.loads(git('show',BASE+':frontier/connections/N742.json')),load('frontier/connections/N742.json'),notice)
    print(json.dumps(dict(intake='EO',status='PASS',original_files=49,original_bytes=399569,
          exact_pastes=3,pasted_bytes=68581,zip_archives=3,archive_members=43,
          producer_member_hashes_checked=40,mechanism_cards=3,proof_ranges=29,
          observational_traces=3,record_level_checkpoints=3,open_review_gates=3,open_capability_gates=3,
          unchanged_earlier_scientific_routes=len(scientific)-len(allowed),scoped_notice_navigation_updates=len(allowed),
          scientific_scripts_syntax_parsed_only=10,scientific_scripts_executed=0,
          scientific_verification='not performed'),sort_keys=True))


if __name__ == '__main__':
    try:
        main()
    except (ValueError,OSError,KeyError,subprocess.CalledProcessError) as error:
        raise SystemExit(str(error))
