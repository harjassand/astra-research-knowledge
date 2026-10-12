#!/usr/bin/env python3
"""Deterministic EM archive/navigation guards. Never executes scientific scripts."""
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

BASE = '0ec7c861e1d687a84a6509c6520f0ad44135f724'
EXPECTED = {'N739':(2979,'targeted_warm_continuation','same'), 'N740':(2921,'fresh_direction_retained_context','same'), 'N741':(3336,'fresh_direction_retained_context','same')}
PINS = {'updates/EM/package/theoretical_local_tolerance/ORIGINAL_PASTED_SOURCE.txt': '60252688fa18a8f6209c6818a3b9a44ae26b055a83454586c7148d442ec77f6f', 'updates/EM/package/genesis_compatibility/ORIGINAL_PASTED_SOURCE.txt': 'b6b247c2ca2710913d24d623c96e7e5e4db7d99afe24bac1f0c1d07f1059b91c', 'updates/EM/package/computational_bounded_field/ORIGINAL_PASTED_SOURCE.txt': '06101d9834ed7466b0f4c3969afc37dcbc750f33c738d891a5b527be15ddfd22', 'updates/EM/package/theoretical_local_tolerance/astra_local_tolerance_2026-10-12.zip': 'c9364e415b2c4829a3613459b6a7f566daaaad6a775680635b537d1dee357f76', 'updates/EM/package/theoretical_local_tolerance/recovered/astra_local_tolerance/research_note.md': '210157597a0ba1a14ee6b9a829f4f06a624ccf2e2dd5a71ceb8d3b62411dd5dd', 'updates/EM/package/theoretical_local_tolerance/recovered/astra_local_tolerance/README.md': 'a61c0f3357f3e4dec29fdbf3c5a0528135e89e1264981bfd785241763e822fc4', 'updates/EM/package/theoretical_local_tolerance/recovered/astra_local_tolerance/check_core.py': '0ac52bdc1f40ff5ff349b25e0e20ffd72f1ca894bd1945153fb660f04527b876', 'updates/EM/package/theoretical_local_tolerance/recovered/astra_local_tolerance/check_interfaces.py': 'b3f0e6f1b8102fb55ce0339c654a9658995f7bfaa7b974f8cd1cee1d1db76833', 'updates/EM/package/theoretical_local_tolerance/recovered/astra_local_tolerance/diagnostics.json': '25247d38e8dd8909eb9356619dc676b9719217ca004d0a3d6e0412b3b2972bb6', 'updates/EM/package/theoretical_local_tolerance/recovered/astra_local_tolerance/interface_diagnostics.json': '6acd574542fd97b653e9bb45c484a07181901029534a4a855fbdde7ddcd8c7c5', 'updates/EM/package/theoretical_local_tolerance/recovered/astra_local_tolerance/example_d4.json': '1926e733efd742e4c758bda96c8767e62ed888118d7a632abf2a715070949cd9', 'updates/EM/package/theoretical_local_tolerance/recovered/astra_local_tolerance/sources.json': 'c8d85da7af0b0a071ea2c8c6eb55e97a5182fc1036a4a3991fba2f254a03f56f', 'updates/EM/package/theoretical_local_tolerance/recovered/astra_local_tolerance/MANIFEST.json': 'c39c08c46e58cdfc4fa01b7637e4c495ed2484a835bed2489e571b62941c43b9', 'updates/EM/package/genesis_compatibility/astra_genesis_compatibility_checkpoint.zip': '3dc22ba2c22eb9f4d2c5252b06cbc01142f600ecec5161bd0388298645eff78a', 'updates/EM/package/genesis_compatibility/recovered/astra_genesis_compatibility/README.txt': 'e666d2e9106ee4d17049b3b6650b68eaa3317c51591d9850d6b0fabbdc7f829e', 'updates/EM/package/genesis_compatibility/recovered/astra_genesis_compatibility/RESEARCH_NOTE.md': 'eecde3e64dc7605fab566d872397a8bea00124add86e352034ab6669a73c4525', 'updates/EM/package/genesis_compatibility/recovered/astra_genesis_compatibility/Q4_GATE.json': 'd6692fecf9e4263ce928b13e1604f209637d4514f5238fb15a0057cce2649efa', 'updates/EM/package/genesis_compatibility/recovered/astra_genesis_compatibility/verify_exact.py': '0f0e99182eb0562e998bb3790927687fbc9e5e7663c3d648cd445bf8af83e12f', 'updates/EM/package/genesis_compatibility/recovered/astra_genesis_compatibility/verification.json': 'b44c58ad0ff0dfaaba04f070625b911c9cdae24db3e0a8c3c0822eae620f2050', 'updates/EM/package/genesis_compatibility/recovered/astra_genesis_compatibility/check_numeric.py': '8370e65c4cd98fa09fa0b632f70c2f83d75027c7d01a52afbf869e04bb4ab407', 'updates/EM/package/genesis_compatibility/recovered/astra_genesis_compatibility/heat_threewave_search.json': '1b9391c4f84313345e77d45688d66343e760be023245cee38be2ef4969db728a', 'updates/EM/package/genesis_compatibility/recovered/astra_genesis_compatibility/numerical_recheck.json': '8dc5b2ff2471f5d8ed47da9a35a9c0e6d7bef7fee8942047f6bf6e0f968c49df', 'updates/EM/package/genesis_compatibility/recovered/astra_genesis_compatibility/MANIFEST.json': '7cad3655e161a629718abd428663108d6c4cc0fe8dd028efa505e6a710b27fa1', 'updates/EM/package/computational_bounded_field/cray_bounded_field_compiler_2026-10-12.zip': '9f4b861d3941592f6c47c8b520db939195895955dc779b4b4b0ffadad9bc7588', 'updates/EM/package/computational_bounded_field/recovered/cray_bounded_field_compiler/CLAIMS.json': '5de77c1e32bfaebd80ed608d5c79b5f694d172ea07ffce0dfc4549ecb7fc1902', 'updates/EM/package/computational_bounded_field/recovered/cray_bounded_field_compiler/IMPLEMENTATION_LOG.md': '3ee94410ccfe2a55487f0d432163df3312586fde6ab1c8c82a470c8f782b3555', 'updates/EM/package/computational_bounded_field/recovered/cray_bounded_field_compiler/MANIFEST.json': '1dcd07ad7fa4d0c414a7d120e19d33499467c12f03107e9b8f455ce840954239', 'updates/EM/package/computational_bounded_field/recovered/cray_bounded_field_compiler/README.md': '879b2f73dd6a233e4b3668e9e1c59167018c5cc62b6343e7fde99c6857725688', 'updates/EM/package/computational_bounded_field/recovered/cray_bounded_field_compiler/RESEARCH_NOTE.md': 'ee80b5ae25bc9171a992c38db996862cb852fcd53e0ef3bd608f55885966bea5', 'updates/EM/package/computational_bounded_field/recovered/cray_bounded_field_compiler/integral_results.json': 'bec7952481676f3b2b7cb04161c6c0d599689cc1a2eafad314060f32fbd85ca0', 'updates/EM/package/computational_bounded_field/recovered/cray_bounded_field_compiler/mixture_results.json': '23587e1871426b7a288bc008df083527102133c5b9a4298bbbe965bc2060e97f', 'updates/EM/package/computational_bounded_field/recovered/cray_bounded_field_compiler/product_prototype_results.json': '5e04fd310e5fe237d4313ab09cb3bbf282f790dbe5cf4c91870a8b692d95702c', 'updates/EM/package/computational_bounded_field/recovered/cray_bounded_field_compiler/prototype_run.log': '5e04fd310e5fe237d4313ab09cb3bbf282f790dbe5cf4c91870a8b692d95702c', 'updates/EM/package/computational_bounded_field/recovered/cray_bounded_field_compiler/rank_one_product_compiler.py': '0e281ca1e524236e256d9a95d354ff88b31e7a282514e8ba7d4b9f8055031a59', 'updates/EM/package/computational_bounded_field/recovered/cray_bounded_field_compiler/results.json': '7ce6700f995958fd639470e47051b35b3f99451bb782f30c3b92b3bffdbddaff', 'updates/EM/package/computational_bounded_field/recovered/cray_bounded_field_compiler/verify_compiler.py': '1a56d0738e0a805e742e091ba3601ceae09018cd93b3d3d07f67b05dd7fe1a9c', 'updates/EM/package/computational_bounded_field/recovered/cray_bounded_field_compiler/verify_discrete_mixture.py': '4d9b1e91ba7854c5908b2da73f7163eebc4dbf4938836b36bf11df2763ade28b', 'updates/EM/package/computational_bounded_field/recovered/cray_bounded_field_compiler/verify_integral_layers.py': '6721ef31ce2d4d139e3d289a0fc3f38ca1732de4e318d01ccd5b2e7b75f604bf'}


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
    need(len(manifest['originals']) == 3 and sum(x['bytes'] for x in manifest['originals']) == 65914,
         'pasted source coverage/extent changed')
    packages = manifest['recovered_packages']
    need(len(packages) == 3 and manifest['recovered_files'] == manifest['source_link_receipts'] == [], 'archive coverage changed')
    source_rows = manifest['originals'] + sum(([p]+p['members'] for p in packages), [])
    indexed = {x['path']:x for x in source_rows}
    need(len(indexed) == len(source_rows) == 38 and set(indexed) == set(PINS), 'original source identities changed')
    scripts = 0
    for path,item in indexed.items():
        data = (ROOT/path).read_bytes()
        need(sha(data) == item['sha256'] == PINS[path] and len(data) == item['bytes'], 'original bytes/hash changed')
        if 'lines' in item:
            need(len(data.decode().splitlines()) == item['lines'], 'source extent changed')
        if path.endswith('.py'):
            ast.parse(data,filename=path)
            scripts += 1
    need(scripts == 8 and sum(x['bytes'] for x in indexed.values()) == 342304, 'original byte/script coverage changed')
    for pkg,count,hash_count in zip(packages,[9,9,14],[8,8,13]):
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
            producer = producer.get('files',producer.get('payloads'))
            if isinstance(producer,dict):
                producer = [dict(path=k,sha256=v) for k,v in producer.items()]
            prefix = names[0].split('/',1)[0]+'/'
            need(len(producer) == hash_count and
                 {x['path'] for x in producer} ==
                 {m['archive_member'][len(prefix):] for m in pkg['members'] if m['path'] != pkg['producer_manifest_path']},
                 'producer manifest names changed')
            for item in producer:
                data = z.read(prefix+item['path'])
                need(sha(data) == item['sha256'] and ('bytes' not in item or len(data) == item['bytes']), 'producer member digest changed')
            need(pkg['verification']['scientific_code_execution'] == pkg['verification']['independent_proof_review'] == 'not performed',
                 'integrity promoted to scientific replay')
    need({p.relative_to(ROOT).as_posix() for p in (ROOT/'updates/EM/package').rglob('*') if p.is_file()} == set(indexed),
         'extra/missing archived disclosure')
    return indexed


def check_status(status):
    route = status['card_id'].split('-',1)[0]
    need(status['claim_status'] == 'source_derived_unreviewed' and
         status['validation']['external_correctness'] == status['validation']['historical_priority'] == 'UNKNOWN',
         'scientific promotion')
    expected = {'N739':[], 'N740':['external:EM_MATRIX_POLYNOMIAL_SOS_AND_HEAT_EXACT_FORMS'],
                'N741':['external:EM_ISING_SPECTRAL_GAP_AND_CONVEX_VOLUME']}[route]
    need([x['target'] for x in status['depends_on']] == expected and
         all(status[k] == [] for k in ['supersedes','invalidates','contrasting_blockers']),
         'unsupported earlier-claim dependency or correction')
    need([x['target'].split('-',1)[0] for x in status['material_updates']] == (['N728'] if route == 'N739' else []),
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
         [{'N728','N725','N724','N736'},{'N729'},{'N726','N730'}], 'family comparison scope changed')
    known = {x['id'] for x in rows('indexes/claims.jsonl')}
    need(all(d['card_id'] in known and all(x['card_id'] in known and x['scope'] for x in d['comparisons'])
             for d in decisions), 'unknown family comparison target')


def check_notices(manifest):
    expected = {'SN-EM-N728-N739-LOCAL-TOLERANT-ACCESS':('N728','N739')}
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


def check_q4(gate):
    need(gate['gate_id'] == 'G-EM-N740-Q4' and gate['status'] == 'open' and gate['completion_evidence'] == [] and
         gate['card_ids'][0].startswith('N740-'), 'Q4 unproved gate promoted or removed')
    need('every allowed gamma, M and omega' in gate['pass_condition'] and
         'failed finite SOS' in gate['validation_boundary'], 'Q4 quantifiers/falsification scope erased')


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
    manifest = load('updates/EM/SOURCE_MANIFEST.json'); mapping = load('updates/EM/CLAIMS.json')
    need(manifest['intake_base_revision'] == mapping['base_revision'] == BASE and
         manifest['source_handling'] == 'source=DATA', 'base/source boundary changed')
    indexed = check_sources(manifest); check_families(load('updates/EM/FAMILY_FIT.json')); check_notices(manifest)
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
        gates = [g for g in rows('frontier/OPEN_PROOF_GATES.jsonl') if g['gate_id'] == 'G-EM-'+route+'-INDEPENDENT-REVIEW']
        need(len(gates) == 1 and gates[0]['card_ids'] == [cid] and gates[0]['status'] == 'open' and
             gates[0]['completion_evidence'] == [], 'independent review gate closed/missing')
        trace = load(entry['workflow_trace']); validate_trace(trace,ROOT); check_trace(trace,route)
        cp = load(entry['checkpoint']); validate_record(cp,ROOT)
        need(cp['base_revision'] == BASE and cp['parent_checkpoint_ids'] == [] and
             cp['branch_id'].startswith('worker-em-'), 'intake ancestry invented')
        generated = views(ROOT,{cp['branch_id']:{cp['checkpoint_id']:cp}})
        view = 'state/branches/'+cp['branch_id']+'.txt'
        need((ROOT/view).read_text() == generated[view], 'checkpoint view stale')
        row = next(r for r in generated['state/branches.tsv'].splitlines() if r.startswith(cp['branch_id']+'\t'))
        need((ROOT/'state/branches.tsv').read_text().splitlines().count(row) == 1, 'checkpoint registry mismatch')
        trace_paths.add(entry['workflow_trace']); cp_paths.add(entry['checkpoint'])
    need(proof_count == 49 and len(trace_paths) == len(cp_paths) == 3, 'source-range/attempt coverage changed')
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
    allowed = {p for n in ['N728'] for p in ['frontier/dossiers/'+n+'.txt','frontier/connections/'+n+'.json']}
    need(set(manifest['permitted_historical_navigation_changes']) == changed_routes == allowed,
         'earlier scientific navigation changed beyond exact scoped notices')
    q4 = next(g for g in rows('frontier/OPEN_PROOF_GATES.jsonl') if g['gate_id'] == 'G-EM-N740-Q4')
    check_q4(q4)
    notice = next(n for n in rows('agent/SEMANTIC_NOTICES.jsonl') if n['notice_id'] == manifest['reciprocal_continuation_notices'][0])
    check_projection(git('show',BASE+':frontier/dossiers/N728.txt').decode(), (ROOT/'frontier/dossiers/N728.txt').read_text(),
                     json.loads(git('show',BASE+':frontier/connections/N728.json')),load('frontier/connections/N728.json'),notice)
    print(json.dumps(dict(intake='EM',status='PASS',original_files=38,original_bytes=342304,
          exact_pastes=3,pasted_bytes=65914,zip_archives=3,archive_members=32,
          producer_member_hashes_checked=29,mechanism_cards=3,proof_ranges=49,
          observational_traces=3,record_level_checkpoints=3,open_review_gates=3,open_positive_quartic_gate=1,
          unchanged_earlier_scientific_routes=len(scientific)-len(allowed),scoped_notice_navigation_updates=len(allowed),
          scientific_scripts_syntax_parsed_only=8,scientific_scripts_executed=0,
          scientific_verification='not performed'),sort_keys=True))


if __name__ == '__main__':
    try:
        main()
    except (ValueError,OSError,KeyError,subprocess.CalledProcessError) as error:
        raise SystemExit(str(error))
