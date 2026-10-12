#!/usr/bin/env python3
"""Deterministic EQ archive/navigation guards. Never executes scientific scripts."""
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

BASE = '32392b30ecb2fbe3e94ce4fc04ebc3acb4dd5b2f'
EXPECTED = {'N751':(2063,'independent_selective_capital','UNKNOWN')}
PINS = {'updates/EQ/package/cray_genesis_transport/ORIGINAL_PASTED_SOURCE.txt': 'c5134e347b7bf7163d43175f47151cc0abb165596d4d5215f5f3eb81ba9810c0', 'updates/EQ/package/cray_genesis_transport/cray_genesis_research_bundle.zip': 'c4722b720f209f216fd129ef1a44128d0d2c59454a1c5278f4e4641291dc9921', 'updates/EQ/package/cray_genesis_transport/recovered/cray_genesis/README.md': '67d7302af4f517aa5c6931319455a5ea63bd00b2738472445b7627d4a07480ab', 'updates/EQ/package/cray_genesis_transport/recovered/cray_genesis/verify.py': '0c143ed1dba0aa48dc162bb3506aafa99f4c19240902fba70375dd4cc1bd9074', 'updates/EQ/package/cray_genesis_transport/recovered/cray_genesis/selftest.py': '83813eea63841e9c6246880a004bafb5a1a22ee4bdd6acc51a7cd6898cc67d4a', 'updates/EQ/package/cray_genesis_transport/recovered/cray_genesis/generate_certificates.py': '19aedc268d18ffacf7b528a217796766e78dd9fa548d24d7d5ecd7549b99e265', 'updates/EQ/package/cray_genesis_transport/recovered/cray_genesis/explore.py': 'fc3450b600235e361bd3f211153f085279064186f85a342889f3a3c7d72238fb', 'updates/EQ/package/cray_genesis_transport/recovered/cray_genesis/fast.py': '850383b3d6029d50394c3c4fdd5d1e94a91b575f560ba2cef293f6f84d0d2eda', 'updates/EQ/package/cray_genesis_transport/recovered/cray_genesis/symbolic_bounds.py': '69f77a783e1fbe3ce60916b3503b15ebb5f55985d66fc115459817f1c974a01e', 'updates/EQ/package/cray_genesis_transport/recovered/cray_genesis/symbolic_certificate.txt': '03cc62bab0a8cf7098b1c6ce4b759a78fc66861f091e79bc1bb96869647a94e2', 'updates/EQ/package/cray_genesis_transport/recovered/cray_genesis/certified_results.json': '1bd892556285f6b845db754c0ab5f10f1932eb947dbaede0cf976b612dacdcf7', 'updates/EQ/package/cray_genesis_transport/recovered/cray_genesis/certificate_1_2.json': '42951196341fb241378d0a793679c8018cbb3561e2c5c706bca7eb786a421083', 'updates/EQ/package/cray_genesis_transport/recovered/cray_genesis/certificate_4_5.json': 'eaef5576bd3035ae12668376ce469b807f0da4a02863915242b23233129631a9', 'updates/EQ/package/cray_genesis_transport/recovered/cray_genesis/certificate_19_20.json': 'b2e3880ccb9eb86b254bf8ff4a9d498d9129705460b76f88fa29357815da24a8', 'updates/EQ/package/cray_genesis_transport/recovered/cray_genesis/requirements.txt': 'b511486154ee3fbc3e2476ca1a03ed4abc5678bc5067a4448033b23b661dc9ab', 'updates/EQ/package/cray_genesis_transport/recovered/cray_genesis/resource_usage.txt': 'a049ee648043cff1de6e8e11f94608b8834b9cc393ef845617c8cefeffe534f8', 'updates/EQ/package/cray_genesis_transport/recovered/cray_genesis/regeneration_log.txt': '936575f6bdb4c7fc69ee3de3ed3f0864a74b618815644ee69cdcd80adc1bc51b', 'updates/EQ/package/cray_genesis_transport/recovered/cray_genesis/SHA256SUMS.txt': 'dff5f5614099c6ee21b2291883d714809a74ee9db6c8fa5f0e51c8ebbccae871'}


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
    need(len(manifest['originals']) == 1 and sum(x['bytes'] for x in manifest['originals']) == 23763,
         'pasted source coverage/extent changed')
    packages = manifest['recovered_packages']
    need(len(packages) == 1 and manifest['recovered_files'] == manifest['source_link_receipts'] == [], 'archive coverage changed')
    source_rows = manifest['originals'] + sum(([p]+p['members'] for p in packages), [])
    indexed = {x['path']:x for x in source_rows}
    need(len(indexed) == len(source_rows) == 18 and set(indexed) == set(PINS), 'original source identities changed')
    scripts = 0
    for path,item in indexed.items():
        data = (ROOT/path).read_bytes()
        need(sha(data) == item['sha256'] == PINS[path] and len(data) == item['bytes'], 'original bytes/hash changed')
        if 'lines' in item:
            need(len(data.decode().splitlines()) == item['lines'], 'source extent changed')
        if path.endswith('.py'):
            ast.parse(data,filename=path)
            scripts += 1
    need(scripts == 6 and sum(x['bytes'] for x in indexed.values()) == 634096, 'original byte/script coverage changed')
    for pkg,count,hash_count in zip(packages,[16],[15]):
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
            producer=[]
            for line in (ROOT/pkg['producer_manifest_path']).read_text().splitlines():
                digest,name=line.split('  ',1)
                producer.append(dict(path=name,sha256=digest))
            mname=next(m['archive_member'] for m in pkg['members'] if m['path']==pkg['producer_manifest_path'])
            prefix=mname.rsplit('/',1)[0]+'/'
            need(len(producer) == hash_count and
                 {x['path'] for x in producer} ==
                 {m['archive_member'][len(prefix):] for m in pkg['members'] if m['path'] != pkg['producer_manifest_path']},
                 'producer manifest names changed')
            for item in producer:
                data = z.read(prefix+item['path'])
                need(sha(data) == item['sha256'] and ('bytes' not in item or len(data) == item['bytes']), 'producer member digest changed')
            need(pkg['verification']['scientific_code_execution'] == pkg['verification']['independent_proof_review'] == 'not performed',
                 'integrity promoted to scientific replay')
    need({p.relative_to(ROOT).as_posix() for p in (ROOT/'updates/EQ/package').rglob('*') if p.is_file()} == set(indexed),
         'extra/missing archived disclosure')
    return indexed


def check_status(status):
    route = status['card_id'].split('-',1)[0]
    need(status['claim_status'] == 'source_derived_unreviewed' and
         status['validation']['external_correctness'] == status['validation']['historical_priority'] == 'UNKNOWN',
         'scientific promotion')
    expected = ['external:EQ_PRODUCT_EQUILIBRIUM_DIFFUSION_BASELINES','external:EQ_COOPERATIVE_POSITIVITY_ZERO_SOFTENING']
    need([x['target'] for x in status['depends_on']] == expected and
         all(status[k] == [] for k in ['supersedes','invalidates','contrasting_blockers','material_updates']),
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
    need([{x['card_id'].split('-',1)[0] for x in d['comparisons']} for d in decisions] == [{'N747','N748','N721'}], 'family comparison scope changed')
    known = {x['id'] for x in rows('indexes/claims.jsonl')}
    need(all(d['card_id'] in known and all(x['card_id'] in known and x['scope'] for x in d['comparisons'])
             for d in decisions), 'unknown family comparison target')


def check_notices(manifest):
    need(manifest['reciprocal_continuation_notices'] == manifest['permitted_historical_navigation_changes'] == [], 'topical comparison promoted to historical update')
    need(not any(n['notice_id'].startswith('SN-EQ-') for n in rows('agent/SEMANTIC_NOTICES.jsonl')), 'unscoped historical notice')


def check_capability_gate(gate,route):
    need(route=='N751' and gate['gate_id']=='G-EQ-N751-CAPABILITY' and gate['status']=='open' and gate['completion_evidence']==[], 'unproved capability gate promoted or removed')
    need(gate['required_obligations']==['independent_orbit_and_no_go_review','legal_nonlocal_completion','acquired_energy_error','routing_congestion_and_tails','accuracy_bit_cost_and_matched_baseline'], 'capability obligations erased')
    need(all(x in gate['validation_boundary'] for x in ['nonpositive dual value under box closure','no affordable nonlocal completion','not acquired energy control','not independent review','Exponential patch cost','does not close N747/N748']), 'scientific boundary erased')


def check_validator_compatibility(old,new):
    before = "    need(new_connection['snapshot'] == load('agent/access_manifest.json')['snapshot'], 'unexpected generated snapshot metadata')"
    after = "    manifest = load('agent/access_manifest.json')\n    path = 'frontier/connections/'+earlier.split('-',1)[0]+'.json'\n    need(sha((ROOT/path).read_bytes()) == manifest['outputs'].get(path) and\n         new_connection['snapshot'] == load(path)['snapshot'], 'unexpected generated snapshot metadata')"
    need(old.count(before)==1 and new==old.replace(before,after), 'historical validator changed beyond cached-output guard')


def main():
    manifest = load('updates/EQ/SOURCE_MANIFEST.json'); mapping = load('updates/EQ/CLAIMS.json')
    need(manifest['intake_base_revision'] == mapping['base_revision'] == BASE and
         manifest['source_handling'] == 'source=DATA', 'base/source boundary changed')
    indexed = check_sources(manifest); check_families(load('updates/EQ/FAMILY_FIT.json')); check_notices(manifest)
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
    need(len(mapping['claims']) == 1, 'card coverage changed')
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
        gates = [g for g in rows('frontier/OPEN_PROOF_GATES.jsonl') if g['gate_id'] == 'G-EQ-'+route+'-INDEPENDENT-REVIEW']
        need(len(gates) == 1 and gates[0]['card_ids'] == [cid] and gates[0]['status'] == 'open' and
             gates[0]['completion_evidence'] == [], 'independent review gate closed/missing')
        trace = load(entry['workflow_trace']); validate_trace(trace,ROOT); check_trace(trace,route)
        cp = load(entry['checkpoint']); validate_record(cp,ROOT)
        need(cp['base_revision'] == BASE and cp['parent_checkpoint_ids'] == [] and
             cp['branch_id'].startswith('worker-eq-'), 'intake ancestry invented')
        generated = views(ROOT,{cp['branch_id']:{cp['checkpoint_id']:cp}})
        view = 'state/branches/'+cp['branch_id']+'.txt'
        need((ROOT/view).read_text() == generated[view], 'checkpoint view stale')
        row = next(r for r in generated['state/branches.tsv'].splitlines() if r.startswith(cp['branch_id']+'\t'))
        need((ROOT/'state/branches.tsv').read_text().splitlines().count(row) == 1, 'checkpoint registry mismatch')
        trace_paths.add(entry['workflow_trace']); cp_paths.add(entry['checkpoint'])
    need(proof_count == 12 and len(trace_paths) == len(cp_paths) == 1, 'source-range/attempt coverage changed')
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
    permitted={'updates/EP/validate.py'}
    need(changed & old_paths == permitted, 'earlier scientific/source/checkpoint/evaluation object changed')
    check_validator_compatibility(git('show',BASE+':updates/EP/validate.py').decode(),(ROOT/'updates/EP/validate.py').read_text())
    outputs = json.loads(git('show',BASE+':agent/access_manifest.json'))['outputs']
    scientific = {p:d for p,d in outputs.items() if p.startswith(('frontier/dossiers/','frontier/connections/','frontier/proof_ranges/'))}
    changed_routes = {p for p,d in scientific.items() if not (ROOT/p).is_file() or sha((ROOT/p).read_bytes()) != d}
    allowed=set()
    need(set(manifest['permitted_historical_navigation_changes']) == changed_routes == allowed, 'earlier scientific navigation changed')
    for route in EXPECTED:
        gate = next(g for g in rows('frontier/OPEN_PROOF_GATES.jsonl') if g['gate_id'] == 'G-EQ-'+route+'-CAPABILITY')
        check_capability_gate(gate,route)
    print(json.dumps(dict(intake='EQ',status='PASS',original_files=18,original_bytes=634096,
          exact_pastes=1,pasted_bytes=23763,zip_archives=1,archive_members=16,
          producer_member_hashes_checked=15,mechanism_cards=1,proof_ranges=12,
          observational_traces=1,record_level_checkpoints=1,open_review_gates=1,open_capability_gates=1,
          unchanged_earlier_scientific_routes=len(scientific),scoped_notice_navigation_updates=0,
          scientific_scripts_syntax_parsed_only=6,scientific_scripts_executed=0,
          scientific_verification='not performed'),sort_keys=True))



if __name__ == '__main__':
    try:
        main()
    except (ValueError,OSError,KeyError,subprocess.CalledProcessError) as error:
        raise SystemExit(str(error))
