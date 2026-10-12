#!/usr/bin/env python3
"""Deterministic ER archive/navigation guards. Never executes scientific scripts."""
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

BASE = 'b07610a28f61ce9020b485033d5628baf7a47dc5'
EXPECTED = {'N752':(2530,'targeted_warm_continuation','same'),'N753':(None,'UNKNOWN','UNKNOWN'),'N754':(None,'UNKNOWN','UNKNOWN'),'N755':(None,'UNKNOWN','UNKNOWN'),'N756':(None,'UNKNOWN','UNKNOWN')}
PINS = {'updates/ER/package/constructive_short_edge/ORIGINAL_PASTED_SOURCE.txt': '63bf72e5adc98c165eadfbe52f604cc21d9570acfe8de26ac62b1695b98ad23b', 'updates/ER/package/constructive_short_edge/astra_constructive_short_edge_20261013.zip': '15a23e607362f2ef65ae172bec4138857cee91b152faff8d0035d9ee5b697312', 'updates/ER/package/constructive_short_edge/recovered/spectral_audit_results.json': '015d6d77f7f0559237f49cae529af08786bdfa1c4a2096de5003bbdbf2cb3d44', 'updates/ER/package/constructive_short_edge/recovered/exact_audit.py': '97ca17f807279a30c76d15a06d5f338fbef9b455f753c3308e67333ee36c1d25', 'updates/ER/package/constructive_short_edge/recovered/exact_audit_results.json': '8ac252986b988637965516d82617324e7b430b94b815366af33b9e9405fbeaf0', 'updates/ER/package/constructive_short_edge/recovered/audit_history.md': '066462d3104ead3fd6b3d42db1eb1ef60af51668722a6eb10a32e79b91f56e7b', 'updates/ER/package/constructive_short_edge/recovered/SHA256SUMS.json': 'b5beb026bbf50dffdb0bb6ea7f945ebf589717ccab572309e6e97de63822aba1', 'updates/ER/package/constructive_short_edge/recovered/cell_repair.py': '5828cb1ec5727cce17f5aef15f59ce3d06db793f184afe22a79b5da619c840cc', 'updates/ER/package/constructive_short_edge/recovered/README.md': '17c699a3870083ada0dcada6f5927ef872f1ef35beb090a29cef801f17d68d8c', 'updates/ER/package/constructive_short_edge/recovered/constructive_short_edge_geometry.md': 'c5264be212b4310249d6fa483938ab12053f6e14adac282d3e2ec26752c2d64f', 'updates/ER/package/constructive_short_edge/recovered/result_card.json': 'cebe41e98dd610c0a634582bf1a87e808a424e6f861eb3b4e39bd86cc63ccb79', 'updates/ER/package/constructive_short_edge/recovered/spectral_audit.py': '950142412e2e6f98bb3607d5ace6d8a6e1ffe949826a0ba8e5c071cb607f14b1', 'updates/ER/package/constructive_short_edge/recovered/sources/Pasted text(20261006-162929).txt': 'ef9ec86043f7f6c0dd10df67028f8a1bb0f353b85d608f90d5dc6385db78fced', 'updates/ER/package/research_results_bundle/README.md': '87b074b8e5a0a7cbbaceb76685730e3846560d28807e1a49d3502c0080662c9b', 'updates/ER/package/research_results_bundle/SHA256SUMS.txt': '56b0323b51b0a7d87c0f106aafd503aae925935089c5d8f3384a63eafc5cce4d', 'updates/ER/package/research_results_bundle/check_outputs/boolean_polynomial_xor_checks.txt': '63906e20110b5da2a5190000b25e9720140c9d1b90856501a6119ca200a3ad4e', 'updates/ER/package/research_results_bundle/check_outputs/calculate.txt': 'e2824d5220f3d463c04a77626f1666d2b01ad3e7188ece1148b27f976f4903fc', 'updates/ER/package/research_results_bundle/check_outputs/check_excursion_reset.txt': 'acc73162e75e87a2e1863ccbbb50bd7d8ba786c48e1dd39a5a36804d75d6b150', 'updates/ER/package/research_results_bundle/check_outputs/check_infinite_degree_coupling.txt': 'ec7c14590dd8b7ee7905fc4b85d0c6831040aa195ab2b0fb864907ba8fcacb74', 'updates/ER/package/research_results_bundle/check_outputs/check_paid_bounds.txt': '22f06f3a46a0b316e02e9926d00b327d22d71f86c43876995088c572d2073b24', 'updates/ER/package/research_results_bundle/check_outputs/check_projection_obstruction.txt': 'b77e1f21daf74c852312e85f3484c415e795b1c356f2dbc72959358dabf28111', 'updates/ER/package/research_results_bundle/check_outputs/check_restart_response.txt': '067bc37c80fdd2953fdaff5d1a436a83e0681a23edb78ea06489f96495242a6a', 'updates/ER/package/research_results_bundle/check_outputs/packaging_check_run.txt': 'b4581b93daaa777bee8e8c9271bb2fc01effe1c7953ed60430542e22ba7e8e18', 'updates/ER/package/research_results_bundle/check_outputs/repeated_control_checks.txt': 'b8853d240e673debb8650ac5e95b2037f1fca7b32eb36b76424f6073d830bcf6', 'updates/ER/package/research_results_bundle/check_outputs/test_degree_ladder.txt': 'a701af86715f0231917780091856f97da36c0bec37b82bfc6aa68a350a0fa142', 'updates/ER/package/research_results_bundle/check_outputs/weighted_basis_peeling_check.txt': 'ea0d722b9f826c754de4cedbe056263b2954de3bd72a4309de8e097b34a18cb7', 'updates/ER/package/research_results_bundle/controlled_noise/boolean_polynomial_xor_checks.py': '0c4eb93e9e41b9c7cb2df1f3023c3844d7bdfabf909b9d8620c64286139922c9', 'updates/ER/package/research_results_bundle/controlled_noise/boolean_polynomial_xor_sampler.md': '03551edad4f6e519329c2cc1ad3054b61059e2ed5d94c867492dd731c7a1ab8b', 'updates/ER/package/research_results_bundle/controlled_noise/categorical_rank_budget_lemmas.md': '561b7b1df819c13bffc48226d9ba0aaf3220273b6f31309dc40c4f47dae050ab', 'updates/ER/package/research_results_bundle/controlled_noise/compressed_discrete_noise_affine_span_sampler.md': '70730d2e07145941b7967c968c559894d01bbb77e48ea29767670491ab4b654b', 'updates/ER/package/research_results_bundle/controlled_noise/compressed_linear_control_poisson_noise_compiler.md': 'c4be4d72d6af1a4ed2a787346a11fb3d3e9bd290002b2515b319d9a15052971e', 'updates/ER/package/research_results_bundle/controlled_noise/repeated_control_checks.py': 'bcf39e5bb6223335d5c1c22400a15d8b94aed2d6b0ea8974b629769c0e223277', 'updates/ER/package/research_results_bundle/controlled_noise/repeated_linear_control_sampler.md': '7629a3f005646509a9dd4e2e938a1b37a72a3b61b59eca32375dc2358daa308b', 'updates/ER/package/research_results_bundle/controlled_noise/sparse_polynomial_leaf_importance.md': '931b82d2897bdd6671d96234feac928cc1440626046e7527d7d8eb74c3f7efe4', 'updates/ER/package/research_results_bundle/controlled_noise/weighted_basis_peeling_check.py': '7ba7a4560890fa9cf8ca594807ed7b90d401765294cd6f1ee1144d8449440282', 'updates/ER/package/research_results_bundle/front_scaling/admission.md': '7b1038fbbe7ae8b3664cfede9e743f6ec1a09c0a1a0b9ab5efb14ac8f009a20d', 'updates/ER/package/research_results_bundle/front_scaling/calculate.py': 'de9747ab26c736a094ce3f9cf9c6c60b9a0916af80ba74c01472b0b72a73742b', 'updates/ER/package/research_results_bundle/front_scaling/results.json': '2365602e696fc06c9a45244af3f22ed8e2e284dd4ef152d85aee4b0570ec2c3e', 'updates/ER/package/research_results_bundle/nonlocal_transport_compression/NONLOCAL_COMPRESSION_FEASIBILITY.md': '4a76191350227f15a62b88df7544040b0162f443bbcfac436ae1b7e8c814c563', 'updates/ER/package/research_results_bundle/nonlocal_transport_compression/check_infinite_degree_coupling.py': 'f912b5afd99e89a0e6b51e83f14e3ddc73b4edfcb963466b77f0b874031f3f1c', 'updates/ER/package/research_results_bundle/nonlocal_transport_compression/test_degree_ladder.py': '37cbfbb8f01370641d76e81f25cdd588504da73ca357da2404edf9a45b77f223', 'updates/ER/package/research_results_bundle/replica_recombination/REPORT.md': 'f5b0c45604d451eb78acf32bc48815cf5cd71810beaa5c5c71d88f85019381fc', 'updates/ER/package/research_results_bundle/replica_recombination/check_recombination.py': '9ba8c3fff33e150e6a192e1695df5c50e06dc3ab49395449a7f1cd1ea5708039', 'updates/ER/package/research_results_bundle/replica_recombination/results.json': '18a1f923b0f71a17ba15dd1862ab9b684ded11b161f06cac5badeaf00be88730', 'updates/ER/package/research_results_bundle/requirements_snapshot.txt': '127e3ec289ee63cd4f8725ab74456aab032506d28550799650b2c5b1894fc70c', 'updates/ER/package/research_results_bundle/run_checks.py': 'c20b8e47ba226c16143d5f4451c89190da6d044667fd3ed6d5d6d19a3f6cfeb7', 'updates/ER/package/research_results_bundle/transport_continuation_cost/PAID_CONTINUATION_CERTIFICATE.md': 'bf0c5337530bb0dbf112139cd4b8d92b2f2bedb58f9c02c362ad36b0cb29a12f', 'updates/ER/package/research_results_bundle/transport_continuation_cost/check_paid_bounds.py': '4027c031aa0fdd0075b9472e15f2571d7dd88d34fa4db5acc00a81914a764ca8', 'updates/ER/package/research_results_bundle/transport_continuation_cost/check_restart_response.py': 'c0b11db92be0e10d988378de1139a91e8819a88d61bc525ac2b804b99347dd04', 'updates/ER/package/research_results_bundle/transport_excursion_resummation/EXCURSION_RESUMMATION_ADMISSION.md': '536d0ee8340834fb8d5da3298729d5778613edaf756d551bb380d72b9c774c09', 'updates/ER/package/research_results_bundle/transport_excursion_resummation/check_excursion_reset.py': 'f496d23ca85d592bca7bf56079dfb24d3cbaf221e28e0de6b9e28c39f993ce66', 'updates/ER/package/research_results_bundle/transport_projection_locality/PROJECTION_LOCALITY_OBSTRUCTION.md': 'db7e2ff0da8b1431dd215e1b5496c24a0d77a67d592c06401250676a73e0d2ca', 'updates/ER/package/research_results_bundle/transport_projection_locality/check_projection_obstruction.py': '97601f55cfa0d26ee04cdc32b445f7bea585f5ecee01b6074f3a4f44ce498815'}

def need(condition,message):
    if not condition: raise ValueError(message)
def sha(data): return hashlib.sha256(data).hexdigest()
def load(path): return json.loads((ROOT/path).read_text())
def rows(path): return [json.loads(l) for l in (ROOT/path).read_text().splitlines() if l.strip()]
def git(*args): return subprocess.check_output(['git','-C',str(ROOT),*args])
def route(identity): return identity.split('-',1)[0] if identity.startswith('N') else identity

def check_sources(manifest):
    need(len(manifest['originals'])==1 and manifest['originals'][0]['bytes']==22610,'paste extent changed')
    packages=manifest['recovered_packages'];directories=manifest['supplied_directories']
    need(len(packages)==len(directories)==1,'package coverage changed')
    items=manifest['originals']+packages+sum((p['members'] for p in packages+directories),[])
    indexed={x['path']:x for x in items}
    need(len(items)==len(indexed)==53 and set(indexed)==set(PINS),'source identities changed')
    scripts=0
    for path,item in indexed.items():
        data=(ROOT/path).read_bytes()
        need(sha(data)==item['sha256']==PINS[path] and len(data)==item['bytes'],'original bytes/hash changed')
        if 'lines' in item: need(len(data.decode().splitlines())==item['lines'],'source extent changed')
        if path.endswith('.py'): ast.parse(data,filename=path);scripts+=1
    need(scripts==15 and sum(x['bytes'] for x in items)==418570,'source coverage changed')
    need({p.relative_to(ROOT).as_posix() for p in (ROOT/'updates/ER/package').rglob('*') if p.is_file()}==set(indexed),'extra/missing disclosure')
    for p in (ROOT/'updates/ER/package').rglob('*'):need(not p.is_symlink(),'unsafe archived path')
    pkg=packages[0]
    with ZipFile(ROOT/pkg['archive_path']) as z:
        need(z.testzip() is None,'ZIP CRC failure')
        names=z.namelist();need(len(names)==len(set(names))==11 and set(names)=={m['archive_member'] for m in pkg['members']},'ZIP member coverage changed')
        for info in z.infolist():
            p=PurePosixPath(info.filename)
            need(not p.is_absolute() and '..' not in p.parts and chr(92) not in info.filename and not stat.S_ISLNK(info.external_attr>>16),'unsafe ZIP path')
            member=next(m for m in pkg['members'] if m['archive_member']==info.filename)
            need(z.read(info)==(ROOT/member['path']).read_bytes(),'extracted member changed')
        producer=json.loads(z.read('SHA256SUMS.json'))
        need(len(producer)==pkg['producer_hashes_checked']==10 and set(producer)==set(names)-{'SHA256SUMS.json'},'producer ZIP manifest coverage')
        for name,digest in producer.items():need(sha(z.read(name))==digest,'producer ZIP hash changed')
    directory=directories[0];producer={name:digest for digest,name in (l.split('  ',1) for l in (ROOT/directory['producer_manifest_path']).read_text().splitlines())}
    need(len(directory['members'])==40 and len(producer)==directory['producer_hashes_checked']==39 and set(producer)=={m['directory_member'] for m in directory['members'] if m['directory_member']!='SHA256SUMS.txt'},'producer directory manifest coverage')
    for name,digest in producer.items():
        p=PurePosixPath(name);need(not p.is_absolute() and '..' not in p.parts and chr(92) not in name,'unsafe directory path')
        need(sha((ROOT/directory['root']/name).read_bytes())==digest,'producer directory hash changed')
    for p in packages+directories:need(p['verification']['scientific_code_execution']==p['verification']['independent_proof_review']=='not performed','integrity promoted to scientific replay')
    return indexed

def check_status(status):
    r=route(status['card_id']);expected={'N752':['external:ER_RATIONAL_ORACLES_SFM','external:ER_SPECTRAL_SIGNING_BASEPOLYHEDRON'],'N753':['external:ER_KARPINSKI_LUBY'],'N754':['external:ER_POSITIVE_REAL_AND_EXCLUSION_BASELINES'],'N755':[],'N756':[]}
    need(status['claim_status']=='source_derived_unreviewed' and status['validation']['external_correctness']==status['validation']['historical_priority']=='UNKNOWN','scientific promotion')
    need([d['target'] for d in status['depends_on']]==expected[r] and all(status[k]==[] for k in ['supersedes','invalidates','contrasting_blockers']),'unsupported dependency or correction')
    targets={'N752':{'N749','P-round'},'N753':{'N738'},'N754':{'N747','N748'},'N755':set(),'N756':set()}
    need({route(u['target']) for u in status['material_updates']}==targets[r],'continuation scope changed')
    need(status['proof_availability']['classification']=='original_proof_accounts_and_recovered_producer_artifacts_not_independently_audited','recovery promoted to audit')
    required={'N752':['54k','2209','enclosing-cell','1161k','not implemented'],'N753':['Karpinski','offset','endpoint','not the whole compiler'],'N754':['UPPER','1.76e28','Stieltjes','not every'],'N755':['UNKNOWN','not a prototype','1.07e-14'],'N756':['three-color','not generally ergodic','not a novel']}
    text=(ROOT/status['card_path']).read_text()
    need(all(t.lower() in text.lower() for t in required[r]),'essential scientific boundary erased')

def check_trace(trace,r):
    duration,mode,relation=EXPECTED[r];resources=trace['resources']
    need(trace['mode']==mode and trace['context']['conversation_relation']==relation and trace['status']=='completed','workflow configuration changed')
    need(resources['reported_inference_seconds']==duration and resources['reported_duration_ref_ids']==(['duration'] if r=='N752' else []),'duration provenance invented')
    need(trace['prompt_availability']==('exact' if r=='N752' else 'UNKNOWN') and trace['prompt_ref_ids']==(['prompt'] if r=='N752' else []),'initiating prompt invented')
    if r!='N752':need('one source bundle' in trace['context']['retained_context'].lower() and 'not be counted' in trace['context']['retained_context'],'bundle subaccounts treated as independent runs')
    need(all(v is None for v in trace['model'].values()) and all(v is None for v in resources['usage'].values()) and resources['worker_invocations'] is None and resources['worker_receipt_ref_ids']==resources['usage_receipt_ref_ids']==[],'unmeasured telemetry invented')
    need(trace['matched_run_id'] is None and trace['advance']['verification']=='producer_reported' and trace['advance']['verification_receipt'] is None,'producer evidence promoted')

def check_families(fit):
    need(fit['base_revision']==BASE and fit['relation_semantics'].startswith('Comparisons are navigation only;'),'comparison promoted to proof')
    need([route(d['card_id']) for d in fit['decisions']]==list(EXPECTED),'family coverage changed')
    expected=[{'N749','P-round','N689','N692'},{'N738'},{'N747','N748','N751'},set(),set()]
    need([{route(c['card_id']) for c in d['comparisons']} for d in fit['decisions']]==expected,'family comparison scope changed')
    known={r['id'] for r in rows('indexes/claims.jsonl')}
    need(all(d['card_id'] in known and all(c['card_id'] in known and c['scope'] for c in d['comparisons']) for d in fit['decisions']),'unknown family target')

def check_projection(old_text,new_text,old_connection,new_connection,notice):
    block='SEMANTIC NOTICE '+notice['notice_id']+'\n'+notice['status']+': '+notice['clarification']+'\n\n'
    need(new_text.count(block)==1,'notice projection missing/duplicated')
    normalize=lambda t:'\n'.join(l for l in t.splitlines() if not l.startswith('snapshot_input_sha256='))
    need(normalize(new_text.replace(block,''))==normalize(old_text),'historical dossier altered beyond notice')
    earlier,later=notice['card_ids'];wanted=[e for e in new_connection['edges'] if e['from']==later and e['to']==earlier and e['kind']=='material_update']
    need(len(wanted)==1 and wanted[0]['composition']==notice['clarification'],'connection notice mismatch')
    projected=dict(new_connection);projected['edges']=[e for e in new_connection['edges'] if e!=wanted[0]];projected['nodes']=[n for n in new_connection['nodes'] if n['id']!=later];projected['snapshot']=old_connection['snapshot']
    need(projected==old_connection,'historical connection altered beyond notice')

def check_notices(manifest):
    pairs=[('N749','N752'),('P-round','N752'),('N738','N753'),('N747','N754'),('N748','N754')]
    ids=['SN-ER-'+a+'-'+b+'-SCOPED-CONTINUATION' for a,b in pairs]
    need(manifest['reciprocal_continuation_notices']==ids,'notice coverage changed')
    allowed={p for a,b in pairs for p in ['frontier/dossiers/'+a+'.txt','frontier/connections/'+a+'.json']}
    need(set(manifest['permitted_historical_navigation_changes'])==allowed,'unscoped historical navigation')
    notices=rows('agent/SEMANTIC_NOTICES.jsonl')
    for nid,pair in zip(ids,pairs):
        ns=[n for n in notices if n['notice_id']==nid];need(len(ns)==1,'duplicate/missing notice');n=ns[0]
        need(tuple(route(c) for c in n['card_ids'])==pair and n['status']=='source_derived_unreviewed_continuation_only' and n['source_revision']==BASE and {u['target'] for u in n['material_updates']}==set(n['card_ids']),'notice status/scope changed')
        for ref in n['source_refs']:need(sha((ROOT/ref['path']).read_bytes())==ref['sha256'],'notice source changed')
        for a in pair:
            text=(ROOT/('frontier/dossiers/'+a+'.txt')).read_text();connection=load('frontier/connections/'+a+'.json')
            need(nid in text and any(e['kind']=='material_update' and e['composition']==n['clarification'] for e in connection['edges']),'notice not reciprocal')
        a=pair[0];dp,cp='frontier/dossiers/'+a+'.txt','frontier/connections/'+a+'.json'
        check_projection(git('show',BASE+':'+dp).decode(),(ROOT/dp).read_text(),json.loads(git('show',BASE+':'+cp)),load(cp),n)

def check_legacy_test(old,new):
    before='            connection = intake.load(cp)\n            intake.check_projection(old,new,old_connection,connection,notice)'
    after="            connection = intake.load(cp)\n            # ER adds a separately guarded reciprocal continuation to N747.\n            # Remove only that exact navigation projection before checking EP.\n            for later in intake.rows('agent/SEMANTIC_NOTICES.jsonl'):\n                if later['notice_id'] != 'SN-ER-N747-N754-SCOPED-CONTINUATION' or notice['card_ids'][0] != later['card_ids'][0]:\n                    continue\n                block = 'SEMANTIC NOTICE '+later['notice_id']+'\\n'+later['status']+': '+later['clarification']+'\\n\\n'\n                self.assertEqual(new.count(block),1)\n                new = new.replace(block,'')\n                earlier_id,later_id = later['card_ids']\n                added = [e for e in connection['edges'] if e['from']==later_id and e['to']==earlier_id and e['kind']=='material_update']\n                self.assertEqual(len(added),1)\n                self.assertEqual(added[0]['composition'],later['clarification'])\n                connection['edges'] = [e for e in connection['edges'] if e != added[0]]\n                connection['nodes'] = [n for n in connection['nodes'] if n['id'] != later_id]\n            intake.check_projection(old,new,old_connection,connection,notice)"
    need(old.count(before)==1 and new==old.replace(before,after), "legacy test changed beyond exact later-notice projection")

def main():
    manifest = load('updates/ER/SOURCE_MANIFEST.json'); mapping = load('updates/ER/CLAIMS.json')
    need(manifest['intake_base_revision'] == mapping['base_revision'] == BASE and
         manifest['source_handling'] == 'source=DATA', 'base/source boundary changed')
    indexed = check_sources(manifest); check_families(load('updates/ER/FAMILY_FIT.json')); check_notices(manifest)
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
    need(len(mapping['claims']) == 5, 'card coverage changed')
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
                need(r['path'].endswith('.zip') and 'lines' not in item, 'unclassified binary evidence')
        need(cid+'\t' in (ROOT/'agent/routes.tsv').read_text(), 'claim route missing')
        for topic in status['topics']:
            need(cid+'\t' in (ROOT/('agent/topics/'+topic+'.tsv')).read_text(), 'topic route missing')
        gates = [g for g in rows('frontier/OPEN_PROOF_GATES.jsonl') if g['gate_id'] == 'G-ER-'+route+'-INDEPENDENT-REVIEW']
        need(len(gates) == 1 and gates[0]['card_ids'] == [cid] and gates[0]['status'] == 'open' and
             gates[0]['completion_evidence'] == [], 'independent review gate closed/missing')
        trace = load(entry['workflow_trace']); validate_trace(trace,ROOT); check_trace(trace,route)
        cp = load(entry['checkpoint']); validate_record(cp,ROOT)
        need(cp['base_revision'] == BASE and cp['parent_checkpoint_ids'] == [] and
             cp['branch_id'].startswith('worker-er-'), 'intake ancestry invented')
        generated = views(ROOT,{cp['branch_id']:{cp['checkpoint_id']:cp}})
        view = 'state/branches/'+cp['branch_id']+'.txt'
        need((ROOT/view).read_text() == generated[view], 'checkpoint view stale')
        row = next(r for r in generated['state/branches.tsv'].splitlines() if r.startswith(cp['branch_id']+'\t'))
        need((ROOT/'state/branches.tsv').read_text().splitlines().count(row) == 1, 'checkpoint registry mismatch')
        trace_paths.add(entry['workflow_trace']); cp_paths.add(entry['checkpoint'])
    need(proof_count == 30 and len(trace_paths) == len(cp_paths) == 5, 'source-range/attempt coverage changed')
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
    permitted={'updates/EP/test_validate.py'}
    need(changed & old_paths == permitted, 'earlier scientific/source/checkpoint/evaluation object changed')
    check_legacy_test(git('show',BASE+':updates/EP/test_validate.py').decode(),(ROOT/'updates/EP/test_validate.py').read_text())
    outputs = json.loads(git('show',BASE+':agent/access_manifest.json'))['outputs']
    scientific = {p:d for p,d in outputs.items() if p.startswith(('frontier/dossiers/','frontier/connections/','frontier/proof_ranges/'))}
    changed_routes = {p for p,d in scientific.items() if not (ROOT/p).is_file() or sha((ROOT/p).read_bytes()) != d}
    allowed=set(manifest['permitted_historical_navigation_changes'])
    need(changed_routes == allowed, 'earlier scientific navigation changed beyond exact notices')
    print(json.dumps(dict(intake='ER',status='PASS',original_files=53,original_bytes=418570,exact_pastes=1,zip_members=11,directory_members=40,producer_hashes_checked=49,mechanism_cards=5,proof_ranges=proof_count,observational_subaccounts=5,record_level_checkpoints=5,scoped_historical_views=len(allowed),unchanged_earlier_scientific_views=len(scientific)-len(allowed),scientific_scripts_syntax_parsed_only=15,scientific_scripts_executed=0,scientific_verification='not performed'),sort_keys=True))

if __name__ == '__main__':
    try:
        main()
    except (ValueError,OSError,KeyError,subprocess.CalledProcessError) as error:
        raise SystemExit(str(error))
