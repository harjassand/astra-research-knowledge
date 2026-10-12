#!/usr/bin/env python3
"""Deterministic EN archive/navigation guards. Never executes scientific scripts."""
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

BASE = '5ab60ff49af6da752fe8452031996410a50f00b4'
EXPECTED = {'N742':(2522,'independent_selective_capital','UNKNOWN'), 'N743':(3418,'independent_selective_capital','UNKNOWN'), 'N744':(3432,'fresh_direction_retained_context','same')}
PINS = {'updates/EN/package/frontier_thermal_transport/ORIGINAL_PASTED_SOURCE.txt': '98b0f2ef0bd9fe5e08c4b474ef0efc0d23ed4a6df9a0ae192fc73cfd77e6a336', 'updates/EN/package/genesis_clock_lift/ORIGINAL_PASTED_SOURCE.txt': '6dedb10feba371c0134f45225c1ece8325807864cb66ec9fffd94bc8a515bdbd', 'updates/EN/package/cray_flux_design/ORIGINAL_PASTED_SOURCE.txt': '2570c1f40c169a50150f3063c8d3f556ad14c3d8cde61fc773cbad4cb04ab066', 'updates/EN/package/frontier_thermal_transport/astra_frontier_thermal_transport.zip': '7b0e9ce7dca9c667dfc79081c43b8fb02a17707ad724f581fcd715f9bb9080c9', 'updates/EN/package/frontier_thermal_transport/recovered/astra_frontier_thermal_transport/README.md': '27dcedb1a82bd9ae91d84bc694da14dacf9e8b0338b8a46d94daed69e449ecb6', 'updates/EN/package/frontier_thermal_transport/recovered/astra_frontier_thermal_transport/checks.json': '5a1d5e630f534cf3ca847922410a72d9cf98d6570f0f98181a81b2d42ae593b9', 'updates/EN/package/frontier_thermal_transport/recovered/astra_frontier_thermal_transport/checks.py': 'dc5078e5cc1b95eef81e636eb8e8bda4b8a59cd220e4b794d8602759f07adece', 'updates/EN/package/frontier_thermal_transport/recovered/astra_frontier_thermal_transport/checks_stdout.txt': '5a1d5e630f534cf3ca847922410a72d9cf98d6570f0f98181a81b2d42ae593b9', 'updates/EN/package/frontier_thermal_transport/recovered/astra_frontier_thermal_transport/manifest.json': 'c3c76f662afcf1cea31a7ef890f79ec880700fcb228acb3128cedfa8f93a5d27', 'updates/EN/package/frontier_thermal_transport/recovered/astra_frontier_thermal_transport/research_note.md': 'f62f75edf590c260ccaf6565dcdd474f878009cd6025c9396eca979bf3c37e9b', 'updates/EN/package/frontier_thermal_transport/recovered/astra_frontier_thermal_transport/research_state.json': '1376377017e373fe6ca05ba9d1bc1fe8b32442a796cf1196d6450b25a3f67592', 'updates/EN/package/genesis_clock_lift/astra_clock_lift_research_packet.zip': 'e38747f38745fe36d419934ec5252a52a4801092e20f3605c5efd5f3f5c2b452', 'updates/EN/package/genesis_clock_lift/recovered/astra_clock_lift_research.md': '022f2d7ce54f5d86c82cd92c82e46d584a4f6c333f982b9c10e352614d467594', 'updates/EN/package/genesis_clock_lift/recovered/astra_clock_lift_verify.py': 'afead9aad1bc57f87f99336c1af34ad6ed8c4a382747ad61ecb43a972ba5a695', 'updates/EN/package/genesis_clock_lift/recovered/astra_clock_lift_results.json': 'ab295922b5a29ac94540574ccdacb9b9555f14c310824aa6ec7dbf52792e8b2d', 'updates/EN/package/genesis_clock_lift/recovered/astra_clock_lift_manifest.json': '53af396c05a3a0ca73f26affb055e65dda846237972a59ef16d30f6c46410d1c', 'updates/EN/package/cray_flux_design/cray_flux_design_2026-10-12.zip': '2836cced4a9a904c8c6670b71c78e3a0ee2df94ef78274388d3ef712e7b87dd8', 'updates/EN/package/cray_flux_design/recovered/cray_flux_design/CLAIM_LEDGER.json': '0d1e6952eb9efd548d957229134fa986e1b162b4b8645a0769e81a8252be2659', 'updates/EN/package/cray_flux_design/recovered/cray_flux_design/ENVIRONMENT.json': 'ad4010c90b160ab81c5827f4a7cd55ae96f05d486e4a39f8d2986aa35fa8f157', 'updates/EN/package/cray_flux_design/recovered/cray_flux_design/MANIFEST.json': 'fd195dcb6664adff87491bf0c1522de89bbec557a82b805d565b9dfb3ed090dd', 'updates/EN/package/cray_flux_design/recovered/cray_flux_design/README.md': 'c70bfb98cbf7fd47d75da26062c1ff8662033b9e738bb8b4b4e579c918c1120f', 'updates/EN/package/cray_flux_design/recovered/cray_flux_design/RESEARCH_NOTE.md': '4ce59bec1e9b685ce3b6dff2383d3e78df3d680f3962ec1a4c2ade85c8bc6229', 'updates/EN/package/cray_flux_design/recovered/cray_flux_design/RESTART.md': '81608d014c484b1210f0833bb82364ff7da64d2d710474beb44c073e3db45de0', 'updates/EN/package/cray_flux_design/recovered/cray_flux_design/benchmark.py': 'e34d8684f8bc920c3da459621300853eff82c80d6a1346c2b55672af98d30972', 'updates/EN/package/cray_flux_design/recovered/cray_flux_design/benchmark_stdout.txt': 'f07f12af0eea567aa8d7d635d95ceef4931c23fcdd6d46391bc644933ff7fe8e', 'updates/EN/package/cray_flux_design/recovered/cray_flux_design/exact_algebra_audit.py': '919382e21948c9f9f62e04315b85239ab7b32a0bee6819f51e41b14000e6e03f', 'updates/EN/package/cray_flux_design/recovered/cray_flux_design/exact_algebra_results.json': 'db3e922e3dac6c7f338d95fb7f5747062235d6caada94e776bf9469d6ae44a04', 'updates/EN/package/cray_flux_design/recovered/cray_flux_design/exact_integer_assay.py': '150a814bd1577810565077e36e6939b8078ad7d2b1b42e6456cf53ae10f6efaf', 'updates/EN/package/cray_flux_design/recovered/cray_flux_design/falsification.py': '16159198ebdf2674d359116ca0f97041ce2c6c4bf885042044d54fbe2f90030e', 'updates/EN/package/cray_flux_design/recovered/cray_flux_design/falsification_results.json': '7eeae4bf1f550254ec0003a3ba99f36535fb1e34f1ea8d7a61b194ca238e7d2c', 'updates/EN/package/cray_flux_design/recovered/cray_flux_design/falsification_stdout.txt': '42177ad1a7e6646b09c5295f784583668968f39a9604ca85ab612336ce75f1cb', 'updates/EN/package/cray_flux_design/recovered/cray_flux_design/flux_design.py': '7240f995501cbfee95e2c99dba0c7b0e63083fe0f86eea9de7e1a4bfa5f4d8cd', 'updates/EN/package/cray_flux_design/recovered/cray_flux_design/integer_results.json': '20dbbef4f6363949f8da0ec81e0b823f219ceeadc22a3f034d1f99c963eff525', 'updates/EN/package/cray_flux_design/recovered/cray_flux_design/integer_results_float_radii_historical.json': 'd488d99ae060a2b0138c33b5a861ab4d5b50ecfbe319145904c239c9f9acdcf4', 'updates/EN/package/cray_flux_design/recovered/cray_flux_design/integer_stdout.txt': '21cdbd831b3318ca317eb410bff8c9798b1fb75c8adef3f2cf3ad6e8c00589ea', 'updates/EN/package/cray_flux_design/recovered/cray_flux_design/mixed_design.py': '4d5010dba4aef877468dfaa5c7553473bc5c98a24794670c43590ea7251448a9', 'updates/EN/package/cray_flux_design/recovered/cray_flux_design/mixed_results.json': '073490913d0d201461672e8b2baad57962f8d8606ed7f92477153961dc27ff1c', 'updates/EN/package/cray_flux_design/recovered/cray_flux_design/mixed_stdout.txt': '9786669ef8a4cf4f62b6f3ed4dcd4f58c1a93909ad648d76d7bd5fddbf85f153', 'updates/EN/package/cray_flux_design/recovered/cray_flux_design/opaque_assay.py': '25112e8941902003ba5f4e86e18c0a782024e17587382fd3e59b6c0240587ce6', 'updates/EN/package/cray_flux_design/recovered/cray_flux_design/rational_confidence.py': '34fcd536799dff9d731d6dd7572c832d167ba309a784c28c950b063a07f2772f', 'updates/EN/package/cray_flux_design/recovered/cray_flux_design/requirements.txt': '22f812aed10cd6ee35e1a18c84118cb641a0463b6f6800545ed838ffac17fbad', 'updates/EN/package/cray_flux_design/recovered/cray_flux_design/results.json': '62ef5ee315ebd6ab8acc0771672632c0a25b080d4f5290a89939ca59a68dea68'}


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
    need(len(manifest['originals']) == 3 and sum(x['bytes'] for x in manifest['originals']) == 75067,
         'pasted source coverage/extent changed')
    packages = manifest['recovered_packages']
    need(len(packages) == 3 and manifest['recovered_files'] == manifest['source_link_receipts'] == [], 'archive coverage changed')
    source_rows = manifest['originals'] + sum(([p]+p['members'] for p in packages), [])
    indexed = {x['path']:x for x in source_rows}
    need(len(indexed) == len(source_rows) == 42 and set(indexed) == set(PINS), 'original source identities changed')
    scripts = 0
    for path,item in indexed.items():
        data = (ROOT/path).read_bytes()
        need(sha(data) == item['sha256'] == PINS[path] and len(data) == item['bytes'], 'original bytes/hash changed')
        if 'lines' in item:
            need(len(data.decode().splitlines()) == item['lines'], 'source extent changed')
        if path.endswith('.py'):
            ast.parse(data,filename=path)
            scripts += 1
    need(scripts == 10 and sum(x['bytes'] for x in indexed.values()) == 1646260, 'original byte/script coverage changed')
    for pkg,count,hash_count in zip(packages,[7,4,25],[6,3,24]):
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
            producer = producer.get('files',producer.get('payloads',producer))
            if isinstance(producer,dict):
                producer = [dict(path=k,sha256=v) for k,v in producer.items()]
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
    need({p.relative_to(ROOT).as_posix() for p in (ROOT/'updates/EN/package').rglob('*') if p.is_file()} == set(indexed),
         'extra/missing archived disclosure')
    return indexed


def check_status(status):
    route = status['card_id'].split('-',1)[0]
    need(status['claim_status'] == 'source_derived_unreviewed' and
         status['validation']['external_correctness'] == status['validation']['historical_priority'] == 'UNKNOWN',
         'scientific promotion')
    expected = {'N742':['external:EN_QUANTUM_BELIEF_PROPAGATION'],
                'N743':['external:EN_HYPERPLANE_COVER_BASELINES'],
                'N744':['external:EN_MARKOV_FINITE_PERTURBATION_AND_RESET_RESOLVENT']}[route]
    need([x['target'] for x in status['depends_on']] == expected and
         all(status[k] == [] for k in ['supersedes','invalidates','contrasting_blockers']),
         'unsupported earlier-claim dependency or correction')
    need([x['target'].split('-',1)[0] for x in status['material_updates']] == (['N735'] if route == 'N743' else []),
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
         [{'N711','N739'},{'N735'},{'N718','N736','N547','N620'}], 'family comparison scope changed')
    known = {x['id'] for x in rows('indexes/claims.jsonl')}
    need(all(d['card_id'] in known and all(x['card_id'] in known and x['scope'] for x in d['comparisons'])
             for d in decisions), 'unknown family comparison target')


def check_notices(manifest):
    expected = {'SN-EN-N735-N743-GENERATOR-INTERFACE-TRANSFER':('N735','N743')}
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
    need(gate['gate_id'] == 'G-EN-'+route+'-CAPABILITY' and gate['status'] == 'open' and
         gate['completion_evidence'] == [] and gate['card_ids'][0].startswith(route+'-'),
         'unproved capability gate promoted or removed')
    if route == 'N743':
        need(gate['falsifier_required_fields'] == ['prime','normal_matrix','affine_offsets','full_coverage',
             'private_point_per_hyperplane','nonzero_scaling','exact_support_separator'],
             'cover-specific falsifier contract erased')
        need('every irredundant affine cover' in gate['question'] and
             'not cover counterexamples' in gate['validation_boundary'], 'cover quantifiers erased')
    elif route == 'N744':
        need(gate['required_acquisitions'] == ['useful_measured_probe_basis','output_relevant_actuator_residual',
             'nonvacuous_global_regret','physical_resource_ledger'], 'flux acquisition obligations erased')
        need('upper bound 1' in gate['validation_boundary'] and
             'isolated' in gate['validation_boundary'], 'failed certificate promoted')
    else:
        need(gate['required_acquisitions'] == ['reference_equilibration_and_independence',
             'certified_filter_or_observable_operation','observable_specific_overlap_or_update_condition',
             'total_acquisition_and_computation'], 'thermal acquisition obligations erased')
        need('zero boundary leakage' in gate['validation_boundary'], 'overlap obstruction erased')


def check_bridge(bridge):
    need(bridge['id'] == 'B-EN-N735-N743-GENERATOR-PROJECTION' and
         bridge['status'] == 'read' and bridge['source_handling'] == 'source=DATA' and
         bridge['relation_state'] == 'CANDIDATE CONNECTION', 'bridge review/status promoted')
    need(bridge['forbidden_transfers'] == ['CRN rate-query complexity','Exact random-variate unit cost',
         'Reaction batching or passive slowdown bounds','Finite-bit implementation','Unconditional covering theorem'],
         'unsupported complexity or theorem transfer')
    need(set(bridge['paired_contracts']) == {'source','destination'} and
         'Q_prime' in bridge['paired_contracts']['source']['interface'] and
         'r_i independent of state' in bridge['paired_contracts']['destination']['interface'],
         'paired generator interfaces missing')
    for ref in bridge['evidence_refs']:
        data = (ROOT/ref['path']).read_bytes()
        need(sha(data) == ref['sha256'] and 1<=ref['lines'][0]<=ref['lines'][1]<=len(data.decode().splitlines()),
             'bridge exact proof provenance changed')


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
    manifest = load('updates/EN/SOURCE_MANIFEST.json'); mapping = load('updates/EN/CLAIMS.json')
    need(manifest['intake_base_revision'] == mapping['base_revision'] == BASE and
         manifest['source_handling'] == 'source=DATA', 'base/source boundary changed')
    indexed = check_sources(manifest); check_families(load('updates/EN/FAMILY_FIT.json')); check_notices(manifest)
    check_bridge(load('updates/EN/B-EN-N735-N743-GENERATOR-PROJECTION.json'))
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
        gates = [g for g in rows('frontier/OPEN_PROOF_GATES.jsonl') if g['gate_id'] == 'G-EN-'+route+'-INDEPENDENT-REVIEW']
        need(len(gates) == 1 and gates[0]['card_ids'] == [cid] and gates[0]['status'] == 'open' and
             gates[0]['completion_evidence'] == [], 'independent review gate closed/missing')
        trace = load(entry['workflow_trace']); validate_trace(trace,ROOT); check_trace(trace,route)
        cp = load(entry['checkpoint']); validate_record(cp,ROOT)
        need(cp['base_revision'] == BASE and cp['parent_checkpoint_ids'] == [] and
             cp['branch_id'].startswith('worker-en-'), 'intake ancestry invented')
        generated = views(ROOT,{cp['branch_id']:{cp['checkpoint_id']:cp}})
        view = 'state/branches/'+cp['branch_id']+'.txt'
        need((ROOT/view).read_text() == generated[view], 'checkpoint view stale')
        row = next(r for r in generated['state/branches.tsv'].splitlines() if r.startswith(cp['branch_id']+'\t'))
        need((ROOT/'state/branches.tsv').read_text().splitlines().count(row) == 1, 'checkpoint registry mismatch')
        trace_paths.add(entry['workflow_trace']); cp_paths.add(entry['checkpoint'])
    need(proof_count == 33 and len(trace_paths) == len(cp_paths) == 3, 'source-range/attempt coverage changed')
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
    allowed = {p for n in ['N735'] for p in ['frontier/dossiers/'+n+'.txt','frontier/connections/'+n+'.json']}
    need(set(manifest['permitted_historical_navigation_changes']) == changed_routes == allowed,
         'earlier scientific navigation changed beyond exact scoped notices')
    for route in EXPECTED:
        gate = next(g for g in rows('frontier/OPEN_PROOF_GATES.jsonl') if g['gate_id'] == 'G-EN-'+route+'-CAPABILITY')
        check_capability_gate(gate,route)
    notice = next(n for n in rows('agent/SEMANTIC_NOTICES.jsonl') if n['notice_id'] == manifest['reciprocal_continuation_notices'][0])
    check_projection(git('show',BASE+':frontier/dossiers/N735.txt').decode(), (ROOT/'frontier/dossiers/N735.txt').read_text(),
                     json.loads(git('show',BASE+':frontier/connections/N735.json')),load('frontier/connections/N735.json'),notice)
    print(json.dumps(dict(intake='EN',status='PASS',original_files=42,original_bytes=1646260,
          exact_pastes=3,pasted_bytes=75067,zip_archives=3,archive_members=36,
          producer_member_hashes_checked=33,mechanism_cards=3,proof_ranges=33,
          observational_traces=3,record_level_checkpoints=3,open_review_gates=3,open_capability_gates=3,
          unchanged_earlier_scientific_routes=len(scientific)-len(allowed),scoped_notice_navigation_updates=len(allowed),
          scientific_scripts_syntax_parsed_only=10,scientific_scripts_executed=0,
          scientific_verification='not performed'),sort_keys=True))


if __name__ == '__main__':
    try:
        main()
    except (ValueError,OSError,KeyError,subprocess.CalledProcessError) as error:
        raise SystemExit(str(error))
