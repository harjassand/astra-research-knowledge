#!/usr/bin/env python3
"""Deterministic EP archive/navigation guards. Never executes scientific scripts."""
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

BASE = 'ac6ce52c80d55173ca38f9cb99cd3ba7f50fb132'
EXPECTED = {'N748':(3610,'targeted_warm_continuation','same'), 'N749':(3100,'independent_selective_capital','UNKNOWN'), 'N750':(2927,'targeted_warm_continuation','same')}
PINS = {'updates/EP/package/frontier_restart_reconstruction/ORIGINAL_PASTED_SOURCE.txt': 'b88c4a8d80a130eb1af8237870922fb557386702ca220c3d809bc36df7706e22', 'updates/EP/package/genesis_short_edge_rounding/ORIGINAL_PASTED_SOURCE.txt': 'a17d1712acac4c5daedd63e47e72b626f74b3bf2da987589bdcb8b0ba2f80df7', 'updates/EP/package/cray_resonance_excision/ORIGINAL_PASTED_SOURCE.txt': '785763dcd90494531a7d6c4c50ca0a6f18f93ba88d29edc49a40f77fdd14fc7c', 'updates/EP/package/frontier_restart_reconstruction/astra_frontier_restart_reconstruction.zip': '623df2808f14006ee2a7447f661c919d873e1fb67eddaed1529e6532c1e0cff8', 'updates/EP/package/frontier_restart_reconstruction/recovered/astra_frontier_restart_reconstruction/README.md': 'e826f23e6172079d98cd6f7ef04e3ee96eec777bf055391863084a6db8f9be9d', 'updates/EP/package/frontier_restart_reconstruction/recovered/astra_frontier_restart_reconstruction/checkpoint.md': 'ee4e83180cb166e7374ba4d38b507d63d9afba3513a23d866a6176d6d1d3390a', 'updates/EP/package/frontier_restart_reconstruction/recovered/astra_frontier_restart_reconstruction/checks.json': '71871a5562401b84cf9a5095a607c70eae66a7d9be9e459c0cbd064223494aa5', 'updates/EP/package/frontier_restart_reconstruction/recovered/astra_frontier_restart_reconstruction/checks.py': '8aa4d51d4b44c773ad8895fff000881e4927a1935f9810616f5095a102b508dd', 'updates/EP/package/frontier_restart_reconstruction/recovered/astra_frontier_restart_reconstruction/manifest.json': 'a70ae4efa57bf7dc6b64da683e309dc3caa77f5d88d33c6c35aa931ee3451ebf', 'updates/EP/package/frontier_restart_reconstruction/recovered/astra_frontier_restart_reconstruction/research_note.md': '41514e7af53184efb966d2fb367d8c8e417a3259b981db5cdb602935aa836046', 'updates/EP/package/frontier_restart_reconstruction/recovered/astra_frontier_restart_reconstruction/schur_check.py': 'ba9cca7fc4a8b1a9119494a50d9ac9800a7860ef98b36a0a0b79296fdf32ab57', 'updates/EP/package/frontier_restart_reconstruction/recovered/astra_frontier_restart_reconstruction/schur_exact.json': 'f0212f73a3dc8e2049e927caea6d8261778b754513da00b3a0e9b7bf2b643e44', 'updates/EP/package/frontier_restart_reconstruction/recovered/astra_frontier_restart_reconstruction/sources.json': '6c075fcb716dbd23a39b127b3c685792c3f9f863394d67def13315693ad2f2ed', 'updates/EP/package/genesis_short_edge_rounding/astra_genesis_short_edge_rounding_20261012.zip': 'f7ab10daf21aa2ccf00619a73e3e659e222d71c3aea87411290e5d19d7c4a660', 'updates/EP/package/genesis_short_edge_rounding/recovered/astra_genesis_20261012/audit.py': 'e895561ced0e92e264c4d7a90a8f985db92539107baa520175c2907dbd527fff', 'updates/EP/package/genesis_short_edge_rounding/recovered/astra_genesis_20261012/audit_results.json': '159636f5471494cefffe082da40f77c69e7d472f27c0e6a2e940c427183d21b0', 'updates/EP/package/genesis_short_edge_rounding/recovered/astra_genesis_20261012/manifest.sha256.json': '348ea6de9f8a8906846678ae71576bfe6a9442c4575ee85e23a5212365cccd49', 'updates/EP/package/genesis_short_edge_rounding/recovered/astra_genesis_20261012/result_card.json': 'ab88e2554f972224df30ed2006c9733a45b0843068407c22d389e0ed7ba380fd', 'updates/EP/package/genesis_short_edge_rounding/recovered/astra_genesis_20261012/short_edge_rounding.md': '7a04430f301a3746ad631f58930409bf3ed8d71ca7bb45d27aabc7fbc5d42731', 'updates/EP/package/cray_resonance_excision/cray_resonance_excision_2026-10-12.zip': '36821ebad2b46d775e17d64e2500ebea6f67059fa6a437c318f42bca0125e41c', 'updates/EP/package/cray_resonance_excision/recovered/cray_resonance_excision_2026-10-12/CLAIMS.json': 'f6e07f81172f27c6cee58fa423384be1799faf2a9b8eab3fd49cf8162ca0f958', 'updates/EP/package/cray_resonance_excision/recovered/cray_resonance_excision_2026-10-12/IMPLEMENTATION_LOG.md': '01b0bdec24f74c4ee9519389cd19d6d3ad9f3d5504b2b75a04e6fb08fd225dee', 'updates/EP/package/cray_resonance_excision/recovered/cray_resonance_excision_2026-10-12/MANIFEST.json': 'f884f5dbc39fc0244dc2fa2fd5233f51bb1194fc25a8b457816c96be8aadbe46', 'updates/EP/package/cray_resonance_excision/recovered/cray_resonance_excision_2026-10-12/README.md': '8495b86f1fb84ed807e82fcc8c0a0b798af617880fcfb1cafd8c69f32b4107d3', 'updates/EP/package/cray_resonance_excision/recovered/cray_resonance_excision_2026-10-12/RESEARCH_NOTE.md': '78e4507d6bad98883961f88c4b618f5811119de01b7b40d37b6b8c41cf8779ea', 'updates/EP/package/cray_resonance_excision/recovered/cray_resonance_excision_2026-10-12/RESTART.md': 'f1623530be95fcd4ae55b105f1d258da8e8f924cc73a1f71c17f46ef885e8ea9', 'updates/EP/package/cray_resonance_excision/recovered/cray_resonance_excision_2026-10-12/SOURCES.json': '9ab77060b796a03c5476334e2f1d6d6adc6342f13c64f0d9ca145c9428b6b61d', 'updates/EP/package/cray_resonance_excision/recovered/cray_resonance_excision_2026-10-12/benchmark_results.json': '9e422fbf3fa336b2d0b6864baa71291d8ff08afa00009ca45e750da845ba6677', 'updates/EP/package/cray_resonance_excision/recovered/cray_resonance_excision_2026-10-12/environment.json': '20411f87dfc980f4aae689b62bee81c4fe9f5303871b8c45d6bfc7889f99e666', 'updates/EP/package/cray_resonance_excision/recovered/cray_resonance_excision_2026-10-12/exact_algebra_checks.py': '7eb851bb9a49814645e5427c54beb5b4a3be0fe5d900ef7f2f432a67b39a640c', 'updates/EP/package/cray_resonance_excision/recovered/cray_resonance_excision_2026-10-12/exact_algebra_results.json': '3de1721145ea197ba7ad9f2cf6c59b4ab03b13ffd48dea0cee09456c895cdf78', 'updates/EP/package/cray_resonance_excision/recovered/cray_resonance_excision_2026-10-12/grid_16_70.npz': 'fb5e5ad4ef621de7e07d5b816de829ffe30167aa4d4f408ffdd8daaba55b8c05', 'updates/EP/package/cray_resonance_excision/recovered/cray_resonance_excision_2026-10-12/grid_4_35.npz': '5d4e4c4488a2b81a640123fe6f0ec58de202d038e78245da775d00b3c417327f', 'updates/EP/package/cray_resonance_excision/recovered/cray_resonance_excision_2026-10-12/grid_8_50.npz': '74d4efeb5671a12995552c8dc0cb697695c2fdd7a94b91dbf1b7daaa762693d2', 'updates/EP/package/cray_resonance_excision/recovered/cray_resonance_excision_2026-10-12/resonance_compiler.py': '3b46e0b0594906642bdb8fe422ce88bd87287f8d37d6c071f2c8c6cef16dad10', 'updates/EP/package/cray_resonance_excision/recovered/cray_resonance_excision_2026-10-12/run_benchmarks.py': '4380785bdf0f0d0a7be63594b5a9d302af156fd8ab2bd07073bdd52bf7cacc00', 'updates/EP/package/cray_resonance_excision/recovered/cray_resonance_excision_2026-10-12/spectral_heat_continuation.py': '24b626593cb96f0803c95b96c7122f3386dbf2e8cab27c64bb65b77fc7d92fa2', 'updates/EP/package/cray_resonance_excision/recovered/cray_resonance_excision_2026-10-12/spectral_heat_results.json': 'eae3ad04572fa42dc3f976108d4938bd21cfb58bc2470842eb675fd55a61179c', 'updates/EP/package/cray_resonance_excision/recovered/cray_resonance_excision_2026-10-12/true_resonance_check.py': 'c6647ea48c0351ca8b3408beab3bf84b05ed4f0355cba9dce1a919c6d79de464', 'updates/EP/package/cray_resonance_excision/recovered/cray_resonance_excision_2026-10-12/true_resonance_results.json': 'a465054c7e97a558883e1909b440e9ee083a5cb5a2d1737269cdc3a6c9da6891'}


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
    need(len(manifest['originals']) == 3 and sum(x['bytes'] for x in manifest['originals']) == 77854,
         'pasted source coverage/extent changed')
    packages = manifest['recovered_packages']
    need(len(packages) == 3 and manifest['recovered_files'] == manifest['source_link_receipts'] == [], 'archive coverage changed')
    source_rows = manifest['originals'] + sum(([p]+p['members'] for p in packages), [])
    indexed = {x['path']:x for x in source_rows}
    need(len(indexed) == len(source_rows) == 40 and set(indexed) == set(PINS), 'original source identities changed')
    scripts = 0
    for path,item in indexed.items():
        data = (ROOT/path).read_bytes()
        need(sha(data) == item['sha256'] == PINS[path] and len(data) == item['bytes'], 'original bytes/hash changed')
        if 'lines' in item:
            need(len(data.decode().splitlines()) == item['lines'], 'source extent changed')
        if path.endswith('.py'):
            ast.parse(data,filename=path)
            scripts += 1
    need(scripts == 8 and sum(x['bytes'] for x in indexed.values()) == 1506550, 'original byte/script coverage changed')
    for pkg,count,hash_count in zip(packages,[9,5,20],[8,4,19]):
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
    need({p.relative_to(ROOT).as_posix() for p in (ROOT/'updates/EP/package').rglob('*') if p.is_file()} == set(indexed),
         'extra/missing archived disclosure')
    return indexed


def check_status(status):
    route = status['card_id'].split('-',1)[0]
    need(status['claim_status'] == 'source_derived_unreviewed' and
         status['validation']['external_correctness'] == status['validation']['historical_priority'] == 'UNKNOWN',
         'scientific promotion')
    expected = {'N748':['external:EP_CONSTRUCTIVE_1D_SHORT_TIME_SIMULATION'],
                'N749':['external:EP_SHORT_EDGE_SPECTRAL_DISCREPANCY_BASELINES'],
                'N750':['external:EP_INTERMEDIATE_FIELD_HEAT_AND_IMPORTANCE_BASELINES']}[route]
    need([x['target'] for x in status['depends_on']] == expected and
         all(status[k] == [] for k in ['supersedes','invalidates','contrasting_blockers']),
         'unsupported earlier-claim dependency or correction')
    need([x['target'].split('-',1)[0] for x in status['material_updates']] ==
         {'N748':['N747'],'N749':['N689','N692'],'N750':['N746']}[route],
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
         [{'N747'},{'N689','N692','N24'},{'N746'}], 'family comparison scope changed')
    known = {x['id'] for x in rows('indexes/claims.jsonl')}
    need(all(d['card_id'] in known and all(x['card_id'] in known and x['scope'] for x in d['comparisons'])
             for d in decisions), 'unknown family comparison target')


def check_notices(manifest):
    expected = {
        'SN-EP-N747-N748-SCOPED-CONTINUATION':('N747','N748'),
        'SN-EP-N689-N749-SCOPED-CONTINUATION':('N689','N749'),
        'SN-EP-N692-N749-SCOPED-CONTINUATION':('N692','N749'),
        'SN-EP-N746-N750-SCOPED-CONTINUATION':('N746','N750')}
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
    need(gate['gate_id'] == 'G-EP-'+route+'-CAPABILITY' and gate['status'] == 'open' and
         gate['completion_evidence'] == [] and gate['card_ids'][0].startswith(route+'-'),
         'unproved capability gate promoted or removed')
    required = {
        'N748':['quantitative_thermodynamic_transfer','constructive_limit_constants','production_locality_simulator','matched_practical_and_calibration_cost'],
        'N749':['polynomial_bit_face_and_barrier_access','quantitative_progress','sharper_bound_construction','N689_N692_scope_and_proof_comparison'],
        'N750':['coefficient_acquired_resonant_blocks','selection_event_retention','weighted_large_block_control','residual_global_phase','finite_bit_and_matched_comparison']}
    need(gate['required_obligations'] == required[route], 'capability obligations erased')
    boundaries = {
        'N748':['literal G1 remains open','unexecuted sufficient budget','not a necessary lower bound','synthetic'],
        'N749':['N689 already records','not an efficient sampler','N692 does not prove construction at108'],
        'N750':['one-sided continuation','not a global sign-problem solution','strong-gap estimator loses']}
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
    need(new_connection['snapshot'] == load('agent/access_manifest.json')['snapshot'], 'unexpected generated snapshot metadata')
    projected['snapshot'] = old_connection['snapshot']
    need(projected == old_connection, 'historical connection content altered beyond notice')


def main():
    manifest = load('updates/EP/SOURCE_MANIFEST.json'); mapping = load('updates/EP/CLAIMS.json')
    need(manifest['intake_base_revision'] == mapping['base_revision'] == BASE and
         manifest['source_handling'] == 'source=DATA', 'base/source boundary changed')
    indexed = check_sources(manifest); check_families(load('updates/EP/FAMILY_FIT.json')); check_notices(manifest)
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
            need(r['sha256'] == item['sha256'], 'proof/source hash invalid')
            if 'lines' in r:
                need('lines' in item and 1<=r['lines'][0]<=r['lines'][1]<=item['lines'], 'proof/source range invalid')
            else:
                need(r['path'].endswith('.npz') and 'lines' not in item, 'unclassified binary evidence')
        need(cid+'\t' in (ROOT/'agent/routes.tsv').read_text(), 'claim route missing')
        for topic in status['topics']:
            need(cid+'\t' in (ROOT/('agent/topics/'+topic+'.tsv')).read_text(), 'topic route missing')
        gates = [g for g in rows('frontier/OPEN_PROOF_GATES.jsonl') if g['gate_id'] == 'G-EP-'+route+'-INDEPENDENT-REVIEW']
        need(len(gates) == 1 and gates[0]['card_ids'] == [cid] and gates[0]['status'] == 'open' and
             gates[0]['completion_evidence'] == [], 'independent review gate closed/missing')
        trace = load(entry['workflow_trace']); validate_trace(trace,ROOT); check_trace(trace,route)
        cp = load(entry['checkpoint']); validate_record(cp,ROOT)
        need(cp['base_revision'] == BASE and cp['parent_checkpoint_ids'] == [] and
             cp['branch_id'].startswith('worker-ep-'), 'intake ancestry invented')
        generated = views(ROOT,{cp['branch_id']:{cp['checkpoint_id']:cp}})
        view = 'state/branches/'+cp['branch_id']+'.txt'
        need((ROOT/view).read_text() == generated[view], 'checkpoint view stale')
        row = next(r for r in generated['state/branches.tsv'].splitlines() if r.startswith(cp['branch_id']+'\t'))
        need((ROOT/'state/branches.tsv').read_text().splitlines().count(row) == 1, 'checkpoint registry mismatch')
        trace_paths.add(entry['workflow_trace']); cp_paths.add(entry['checkpoint'])
    need(proof_count == 34 and len(trace_paths) == len(cp_paths) == 3, 'source-range/attempt coverage changed')
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
    allowed = {p for n in ['N747','N689','N692','N746'] for p in ['frontier/dossiers/'+n+'.txt','frontier/connections/'+n+'.json']}
    need(set(manifest['permitted_historical_navigation_changes']) == changed_routes == allowed,
         'earlier scientific navigation changed beyond exact scoped notices')
    for route in EXPECTED:
        gate = next(g for g in rows('frontier/OPEN_PROOF_GATES.jsonl') if g['gate_id'] == 'G-EP-'+route+'-CAPABILITY')
        check_capability_gate(gate,route)
    for notice in [n for n in rows('agent/SEMANTIC_NOTICES.jsonl') if n['notice_id'] in manifest['reciprocal_continuation_notices']]:
        route = notice['card_ids'][0].split('-',1)[0]
        dp,cp = 'frontier/dossiers/'+route+'.txt','frontier/connections/'+route+'.json'
        check_projection(git('show',BASE+':'+dp).decode(), (ROOT/dp).read_text(),
                         json.loads(git('show',BASE+':'+cp)),load(cp),notice)
    print(json.dumps(dict(intake='EP',status='PASS',original_files=40,original_bytes=1506550,
          exact_pastes=3,pasted_bytes=77854,zip_archives=3,archive_members=34,
          producer_member_hashes_checked=31,mechanism_cards=3,proof_ranges=34,
          observational_traces=3,record_level_checkpoints=3,open_review_gates=3,open_capability_gates=3,
          unchanged_earlier_scientific_routes=len(scientific)-len(allowed),scoped_notice_navigation_updates=len(allowed),
          scientific_scripts_syntax_parsed_only=8,scientific_scripts_executed=0,
          scientific_verification='not performed'),sort_keys=True))


if __name__ == '__main__':
    try:
        main()
    except (ValueError,OSError,KeyError,subprocess.CalledProcessError) as error:
        raise SystemExit(str(error))
