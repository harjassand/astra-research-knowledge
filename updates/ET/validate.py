#!/usr/bin/env python3
"""Preservation/navigation checks only; never executes campaign scientific code."""
import ast, hashlib, html, json, subprocess, sys, stat
from zipfile import ZipFile
from pathlib import PurePosixPath
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from evaluation.workflow_trace import validate as validate_trace
from state.publish_checkpoint import validate_record, views
BASE='c4de4cb557588aa729fbda1529b912dec3056a33'
ROUTES=['N760']
PINS = {'updates/ET/package/cray_nonlocal_transport/ORIGINAL_PASTED_SOURCE.txt': '877468ba99014c1174be3c733b23165ab4dee22627c4279e510bc44b1f523fe0', 'updates/ET/package/cray_nonlocal_transport/cray_nonlocal_transport_bundle.zip': '8bf6fcb03978d7e60d8fd87c139eb1c04068b075e4ddb402a7f8f85b3ce3e80c', 'updates/ET/package/cray_nonlocal_transport/recovered/cray_nonlocal_transport/README.md': 'd08619a60ce8c5db9a2d797d37ac7369cbd8ee1d4c343ad53832af32698253bf', 'updates/ET/package/cray_nonlocal_transport/recovered/cray_nonlocal_transport/REPORT.md': 'd502f80ffb3d397a7ea63a1ffcb65b397685955c64ca6d1f6058eb90c9762fc1', 'updates/ET/package/cray_nonlocal_transport/recovered/cray_nonlocal_transport/SHA256.json': '3f1b54c927e4fa3a0321e2b3e2847540ff683152ae43fce88d0d6f5941017571', 'updates/ET/package/cray_nonlocal_transport/recovered/cray_nonlocal_transport/build_flow.py': '17364f6d443b16025cfcccd6b7ac8a0570220104cd98036231cbe423391f4a13', 'updates/ET/package/cray_nonlocal_transport/recovered/cray_nonlocal_transport/build_flow_reproduction_log.txt': '3da5f120075905d837a37d568f477ec96948fc8a85814901b583f3d37e59fe9b', 'updates/ET/package/cray_nonlocal_transport/recovered/cray_nonlocal_transport/certificate_bounds.py': '378942c138a6001c3d81f032207cf17e8cafc69a9e7cd13efd927b1a548c796c', 'updates/ET/package/cray_nonlocal_transport/recovered/cray_nonlocal_transport/certificate_bounds_reproduction_log.txt': 'aee5caf4335ca8d84a0bafa299eb7a0607ec8cb7a45944aca5bbf303e0187fb2', 'updates/ET/package/cray_nonlocal_transport/recovered/cray_nonlocal_transport/certified_bounds.json': 'ab5e798801987ccc3145f196a5e0502b7298d58133d73236da34034fbacb8845', 'updates/ET/package/cray_nonlocal_transport/recovered/cray_nonlocal_transport/coarse_flow.py': '9df0d7b879c5579ccbdd77f280efaa596f59950db39d137d06e8401ab2f3512a', 'updates/ET/package/cray_nonlocal_transport/recovered/cray_nonlocal_transport/completed_current.py': 'abbbaad111adc9446c957ceaeda7fe93f5e485fb42bed3855dba43d668fab30b', 'updates/ET/package/cray_nonlocal_transport/recovered/cray_nonlocal_transport/exploration/README.md': '92f08f8b95f0b0d13b40ae600845f23b1f54c78661abd6e91ec83fe1009241fb', 'updates/ET/package/cray_nonlocal_transport/recovered/cray_nonlocal_transport/exploration/demand_gate_search.py': 'aa92b772e221fb004f34742abbbb13fb49453dcefcf745032391f7fa09ca78e1', 'updates/ET/package/cray_nonlocal_transport/recovered/cray_nonlocal_transport/exploration/demand_gate_search_results.json': '44ffdcbb32f1cd42c25e97f5c9ba0815298fb92fd1c4ae413dbe97670197b9ef', 'updates/ET/package/cray_nonlocal_transport/recovered/cray_nonlocal_transport/exploration/first_tail_bounds.json': '41eab282867be67b34cb8c6c3f24d3c76c3e8041b94224eebf93511e17624ed9', 'updates/ET/package/cray_nonlocal_transport/recovered/cray_nonlocal_transport/exploration/gadget_explore.py': '3baf6d1bfc0a88c52468debf58822bff4328abb2a7ba6d9353aba3ac7c11ca0c', 'updates/ET/package/cray_nonlocal_transport/recovered/cray_nonlocal_transport/exploration/gate_search.py': '03d74c1bcd478f245c33d9b1c169321d5d64987c144c7e4957320f4f44e97875', 'updates/ET/package/cray_nonlocal_transport/recovered/cray_nonlocal_transport/exploration/gate_search_results.json': '38c81a97af4c505ed47672ea2a39332ca00bdc2cdec024c78c6621232def516e', 'updates/ET/package/cray_nonlocal_transport/recovered/cray_nonlocal_transport/exploration/graph_6x3.npz': 'd4536c8e09493f25fc2d1d4e707c7e0ed1b281c152758d16ebada31df0ee6ccf', 'updates/ET/package/cray_nonlocal_transport/recovered/cray_nonlocal_transport/module_flow.npz': 'c2110dd84ac4744e79568fdfe153516304ee8a49610fcc85b3b4a7dd66904255', 'updates/ET/package/cray_nonlocal_transport/recovered/cray_nonlocal_transport/module_metadata.json': '33383d252703c9d6362ec1ce3478981cb7d185652341c64e3d7ba2006cfb53da', 'updates/ET/package/cray_nonlocal_transport/recovered/cray_nonlocal_transport/reproduce.py': '955437c98fbc25ee7f61456815324b702acce680cd35fad4267d37074574b982', 'updates/ET/package/cray_nonlocal_transport/recovered/cray_nonlocal_transport/reproduction_log.txt': '88cb1ff55f308c766b1f1bd65ac1e2d5dde4a9866b7f0766fece1f000f6e4867', 'updates/ET/package/cray_nonlocal_transport/recovered/cray_nonlocal_transport/reproduction_resources.txt': '7f8c6084fa60fd4b2eb595c316a5c8871c859bf6a215bd11b2754641a094e82f', 'updates/ET/package/cray_nonlocal_transport/recovered/cray_nonlocal_transport/reproduction_results.json': '88cb1ff55f308c766b1f1bd65ac1e2d5dde4a9866b7f0766fece1f000f6e4867', 'updates/ET/package/cray_nonlocal_transport/recovered/cray_nonlocal_transport/selftest.py': '4422f675d8cf63ce2437fbb29ece7b390bcc8f35d913d485d6fa7954ca3767c4', 'updates/ET/package/cray_nonlocal_transport/recovered/cray_nonlocal_transport/selftest_reproduction_log.txt': '46ff1b5d15721e16d2159f93fe7f30ca71fc2cb7ed8758bc1faff9b3254b50f1', 'updates/ET/package/cray_nonlocal_transport/recovered/cray_nonlocal_transport/selftest_results.json': '46ff1b5d15721e16d2159f93fe7f30ca71fc2cb7ed8758bc1faff9b3254b50f1', 'updates/ET/package/cray_nonlocal_transport/recovered/cray_nonlocal_transport/verification_results.json': '8573cf37102e56018c87249bbbb1f3a138e4eb885bd2bb91b86613a2e3cfd426', 'updates/ET/package/cray_nonlocal_transport/recovered/cray_nonlocal_transport/verify_module.py': '6f988b5e0c12f984d9cbfeab3c476b921263e3895ac8856ce01275810cfcbf5b', 'updates/ET/package/cray_nonlocal_transport/recovered/cray_nonlocal_transport/verify_module_reproduction_log.txt': '8573cf37102e56018c87249bbbb1f3a138e4eb885bd2bb91b86613a2e3cfd426'}
NOTICE = {'notice_id': 'SN-ET-N751-N760-SCOPED-CONTINUATION', 'card_ids': ['N751-translation-orbit-certificates-and-local-current-transport-obstruction', 'N760-frozen-reservoir-lifting-and-nonlocal-hard-ka-certificate'], 'issue': 'Scoped nonlocal completion of earlier open interface; exact-local obstruction retained.', 'status': 'source_derived_unreviewed_continuation_only', 'clarification': 'N760 continues N751 with a source-reported explicit hard-KA nonlocal completion: finite port-independent source-defect modules, reservoir-frozen lifting, cluster-quotient stream and acquired ensemble L2 tail. The instantiated L=3 certificate covers0<p<=0.40; it leaves dense regimes, polynomial accuracy/representation cost and matched strongest-method advantage open. N751 exact-local box-closure no-go remains intact. Earlier sources, statuses and gates remain historical and unchanged; neither candidate has independent correctness or priority clearance.', 'material_updates': [{'target': 'N760-frozen-reservoir-lifting-and-nonlocal-hard-ka-certificate', 'scope': 'N760 continues N751 with a source-reported explicit hard-KA nonlocal completion: finite port-independent source-defect modules, reservoir-frozen lifting, cluster-quotient stream and acquired ensemble L2 tail. The instantiated L=3 certificate covers0<p<=0.40; it leaves dense regimes, polynomial accuracy/representation cost and matched strongest-method advantage open. N751 exact-local box-closure no-go remains intact. Earlier sources, statuses and gates remain historical and unchanged; neither candidate has independent correctness or priority clearance.', 'relation_status': 'new source-reported scoped candidate'}, {'target': 'N751-translation-orbit-certificates-and-local-current-transport-obstruction', 'scope': 'N760 continues N751 with a source-reported explicit hard-KA nonlocal completion: finite port-independent source-defect modules, reservoir-frozen lifting, cluster-quotient stream and acquired ensemble L2 tail. The instantiated L=3 certificate covers0<p<=0.40; it leaves dense regimes, polynomial accuracy/representation cost and matched strongest-method advantage open. N751 exact-local box-closure no-go remains intact. Earlier sources, statuses and gates remain historical and unchanged; neither candidate has independent correctness or priority clearance.', 'relation_status': 'historical result/status/gate retained'}], 'source_refs': [{'path': 'updates/ET/package/cray_nonlocal_transport/recovered/cray_nonlocal_transport/REPORT.md', 'source_id': 'src-ET-n760-6c97351260e6', 'sha256': 'd502f80ffb3d397a7ea63a1ffcb65b397685955c64ca6d1f6058eb90c9762fc1', 'lines': [1, 43], 'range_scope': 'Result scope, prior positivity and three distinct nonlocal alternatives.', 'read_path': 'updates/ET/package/cray_nonlocal_transport/recovered/cray_nonlocal_transport/REPORT.md', 'hash_kind': 'original_utf8_bytes'}, {'path': 'updates/ET/package/cray_nonlocal_transport/recovered/cray_nonlocal_transport/REPORT.md', 'source_id': 'src-ET-n760-6c97351260e6', 'sha256': 'd502f80ffb3d397a7ea63a1ffcb65b397685955c64ca6d1f6058eb90c9762fc1', 'lines': [44, 85], 'range_scope': 'Hard-rate collective variational target and Thomson normalization; no extra hydrodynamic theorem.', 'read_path': 'updates/ET/package/cray_nonlocal_transport/recovered/cray_nonlocal_transport/REPORT.md', 'hash_kind': 'original_utf8_bytes'}, {'path': 'updates/ET/package/cray_nonlocal_transport/recovered/cray_nonlocal_transport/REPORT.md', 'source_id': 'src-ET-n760-6c97351260e6', 'sha256': 'd502f80ffb3d397a7ea63a1ffcb65b397685955c64ca6d1f6058eb90c9762fc1', 'lines': [86, 168], 'range_scope': 'Port-independent gate, exact source module, forest repair and weighted energy cost.', 'read_path': 'updates/ET/package/cray_nonlocal_transport/recovered/cray_nonlocal_transport/REPORT.md', 'hash_kind': 'original_utf8_bytes'}, {'path': 'updates/ET/package/cray_nonlocal_transport/recovered/cray_nonlocal_transport/REPORT.md', 'source_id': 'src-ET-n760-6c97351260e6', 'sha256': 'd502f80ffb3d397a7ea63a1ffcb65b397685955c64ca6d1f6058eb90c9762fc1', 'lines': [169, 259], 'range_scope': 'Cluster-quotient stream, chordless distinct-site path automaton and explicit nonlocal tail.', 'read_path': 'updates/ET/package/cray_nonlocal_transport/recovered/cray_nonlocal_transport/REPORT.md', 'hash_kind': 'original_utf8_bytes'}, {'path': 'updates/ET/package/cray_nonlocal_transport/recovered/cray_nonlocal_transport/REPORT.md', 'source_id': 'src-ET-n760-6c97351260e6', 'sha256': 'd502f80ffb3d397a7ea63a1ffcb65b397685955c64ca6d1f6058eb90c9762fc1', 'lines': [260, 330], 'range_scope': 'Reservoir forcing, legal antisymmetry and conditional proof of global admissibility.', 'read_path': 'updates/ET/package/cray_nonlocal_transport/recovered/cray_nonlocal_transport/REPORT.md', 'hash_kind': 'original_utf8_bytes'}, {'path': 'updates/ET/package/cray_nonlocal_transport/recovered/cray_nonlocal_transport/REPORT.md', 'source_id': 'src-ET-n760-6c97351260e6', 'sha256': 'd502f80ffb3d397a7ea63a1ffcb65b397685955c64ca6d1f6058eb90c9762fc1', 'lines': [331, 362], 'range_scope': 'Response normalization, covering congestion, energy and diffusion lower formula.', 'read_path': 'updates/ET/package/cray_nonlocal_transport/recovered/cray_nonlocal_transport/REPORT.md', 'hash_kind': 'original_utf8_bytes'}, {'path': 'updates/ET/package/cray_nonlocal_transport/recovered/cray_nonlocal_transport/REPORT.md', 'source_id': 'src-ET-n760-6c97351260e6', 'sha256': 'd502f80ffb3d397a7ea63a1ffcb65b397685955c64ca6d1f6058eb90c9762fc1', 'lines': [363, 432], 'range_scope': 'Legal nonconserved truncations, explicit L2 completion error and conditional tighter energy.', 'read_path': 'updates/ET/package/cray_nonlocal_transport/recovered/cray_nonlocal_transport/REPORT.md', 'hash_kind': 'original_utf8_bytes'}, {'path': 'updates/ET/package/cray_nonlocal_transport/recovered/cray_nonlocal_transport/REPORT.md', 'source_id': 'src-ET-n760-6c97351260e6', 'sha256': 'd502f80ffb3d397a7ea63a1ffcb65b397685955c64ca6d1f6058eb90c9762fc1', 'lines': [433, 450], 'range_scope': 'Bounded stationary stream modifications, limited completion interface and no density theorem.', 'read_path': 'updates/ET/package/cray_nonlocal_transport/recovered/cray_nonlocal_transport/REPORT.md', 'hash_kind': 'original_utf8_bytes'}, {'path': 'updates/ET/package/cray_nonlocal_transport/recovered/cray_nonlocal_transport/REPORT.md', 'source_id': 'src-ET-n760-6c97351260e6', 'sha256': 'd502f80ffb3d397a7ea63a1ffcb65b397685955c64ca6d1f6058eb90c9762fc1', 'lines': [451, 500], 'range_scope': 'Density interval, producer diagnostics/timings, exponential accuracy costs and compatibility with local no-go.', 'read_path': 'updates/ET/package/cray_nonlocal_transport/recovered/cray_nonlocal_transport/REPORT.md', 'hash_kind': 'original_utf8_bytes'}, {'path': 'updates/ET/package/cray_nonlocal_transport/recovered/cray_nonlocal_transport/REPORT.md', 'source_id': 'src-ET-n760-6c97351260e6', 'sha256': 'd502f80ffb3d397a7ea63a1ffcb65b397685955c64ca6d1f6058eb90c9762fc1', 'lines': [501, 538], 'range_scope': 'Dense compressed-module obligation, established baselines and unknown historical novelty.', 'read_path': 'updates/ET/package/cray_nonlocal_transport/recovered/cray_nonlocal_transport/REPORT.md', 'hash_kind': 'original_utf8_bytes'}], 'source_revision': 'c4de4cb557588aa729fbda1529b912dec3056a33'}
def need(ok,message):
    if not ok:raise ValueError(message)
def sha(d):return hashlib.sha256(d).hexdigest()
def load(p):return json.loads((ROOT/p).read_text())
def rows(p):return [json.loads(l) for l in (ROOT/p).read_text().splitlines() if l.strip()]
def git(*args):return subprocess.check_output(['git','-C',str(ROOT),*args])
def route(c):return c.split('-',1)[0]


def check_sources(m):
    need(m['intake_base_revision']==BASE and m['source_handling']=='source=DATA','source authority changed')
    need(len(m['originals'])==len(m['recovered_packages'])==1,'source identities changed')
    pkg=m['recovered_packages'][0];items=m['originals']+[pkg]+pkg['members'];indexed={x['path']:x for x in items}
    need(len(items)==len(indexed)==32 and set(indexed)==set(PINS),'source identities changed')
    need(sum(x['bytes'] for x in items)==12320208 and m['originals'][0]['lines']==416,'source extent changed')
    for path,x in indexed.items():
        p=PurePosixPath(path);need(not p.is_absolute() and '..' not in p.parts and not (ROOT/path).is_symlink(),'unsafe original path')
        d=(ROOT/path).read_bytes();need(sha(d)==x['sha256']==PINS[path] and len(d)==x['bytes'],'original bytes/hash changed')
        if 'lines' in x:need(len(d.decode().splitlines())==x['lines'],'source lines changed')
        if path.endswith('.py'):ast.parse(d,filename=path)
    actual={p.relative_to(ROOT).as_posix() for p in (ROOT/'updates/ET/package').rglob('*') if p.is_file()};need(actual==set(PINS),'extra/missing disclosure')
    with ZipFile(ROOT/pkg['archive_path']) as z:
        need(z.testzip() is None,'ZIP CRC failure');names=z.namelist();need(len(names)==len(set(names))==30 and set(names)=={x['archive_member'] for x in pkg['members']},'ZIP member coverage changed')
        for info in z.infolist():
            p=PurePosixPath(info.filename);need(not p.is_absolute() and '..' not in p.parts and chr(92) not in info.filename and not stat.S_ISLNK(info.external_attr>>16) and not info.is_dir(),'unsafe ZIP path')
            member=next(x for x in pkg['members'] if x['archive_member']==info.filename);need(z.read(info)==(ROOT/member['path']).read_bytes(),'extracted member changed')
        producer=json.loads(z.read('cray_nonlocal_transport/SHA256.json'))
        need(len(producer)==pkg['producer_hashes_checked']==29 and set(producer)=={x.removeprefix('cray_nonlocal_transport/') for x in names if not x.endswith('/SHA256.json')},'producer digest coverage changed')
        for name,h in producer.items():need(sha(z.read('cray_nonlocal_transport/'+name))==h,'producer hash changed')
    need(sum(p.endswith('.py') for p in indexed)==10 and sum(p.endswith('.npz') for p in indexed)==2,'script/binary coverage changed')
    need(pkg['verification']['scientific_code_execution']==pkg['verification']['independent_proof_review']==pkg['verification']['binary_array_loading']=='not performed','integrity promoted to scientific replay')
    return indexed

def check_status(s,text):
    need(route(s['card_id'])=='N760' and s['claim_status']=='source_derived_unreviewed','scientific promotion')
    need(s['validation']['external_correctness']==s['validation']['historical_priority']=='UNKNOWN','validation/priority invented')
    need(s['proof_availability']['classification']=='original_proof_accounts_and_recovered_producer_artifacts_not_independently_audited','availability promoted to audit')
    need(all(s[k]==[] for k in ['depends_on','supersedes','invalidates','contrasting_blockers']),'topical dependency or supersession invented')
    need([route(x['target']) for x in s['material_updates']]==['N751'] and s['material_updates'][0]['scope']==NOTICE['clarification'],'scoped continuation changed')
    required=['collective/bulk','not tagged','0<p<=0.40','no polynomial accuracy','not conserved','ensemble L2','both endpoint block gates good','2^(2L^2)','2^O(R^2)','already established','priority UNKNOWN','N751','Shapira','no head-to-head']
    need(all(x.lower() in text.lower() for x in required),'essential scientific boundary erased')

def check_trace(t):
    need(t['mode']=='targeted_warm_continuation' and t['context']['conversation_relation']=='same','workflow configuration changed')
    need(t['prompt_availability']=='exact' and t['prompt_ref_ids']==['prompt'],'prompt provenance changed')
    res=t['resources'];need(res['reported_inference_seconds']==2971 and res['reported_duration_ref_ids']==['duration'],'reported duration changed')
    need(all(v is None for v in t['model'].values()) and all(v is None for v in res['usage'].values()) and res['worker_invocations'] is None,'unmeasured telemetry invented')
    need(res['worker_receipt_ref_ids']==res['usage_receipt_ref_ids']==[] and t['matched_run_id'] is None,'unsupported comparison')
    need(t['advance']['verification']=='producer_reported' and t['advance']['verification_receipt'] is None,'producer evidence promoted')
    refs={x['id']:x for x in t['refs']};need(refs['duration']['lines']==[43,43] and refs['prompt']['lines']==[1,28] and refs['result']['lines']==[68,416],'prompt/duration/result scope changed')

def check_families(f):
    need(f['base_revision']==BASE and f['relation_semantics'].startswith('One scoped reciprocal continuation;'),'family authority changed')
    need(len(f['decisions'])==1 and route(f['decisions'][0]['card_id'])=='N760','family coverage changed')
    need([route(x['card_id']) for x in f['decisions'][0]['comparisons']]==['N751','N754'] and all(x['scope'] for x in f['decisions'][0]['comparisons']),'family comparison scope changed')
    need(f['decisions'][0]['comparisons'][0]['scope']==NOTICE['clarification'],'continuation mismatch')

def check_gate(g,cid):need(g['status']=='open' and g['completion_evidence']==[] and g['card_ids']==[cid],'unresolved gate promoted')
def check_capability(g,cid):
    check_gate(g,cid)
    need(all(x in g['question'].lower() for x in ['dense p','port-independent','weighted energy','2^(2l^2)','baseline']),'capability obligation erased')

def check_projection(old_text,new_text,old_connection,new_connection,notice):
    block='SEMANTIC NOTICE '+notice['notice_id']+'\n'+notice['status']+': '+notice['clarification']+'\n\n'
    need(new_text.count(block)==1,'notice projection missing/duplicated')
    normalize=lambda t:'\n'.join(l for l in t.splitlines() if not l.startswith('snapshot_input_sha256='))
    need(normalize(new_text.replace(block,''))==normalize(old_text),'historical dossier altered beyond notice')
    earlier,later=notice['card_ids'];added=[e for e in new_connection['edges'] if e['from']==later and e['to']==earlier and e['kind']=='material_update']
    need(len(added)==1 and added[0]['composition']==notice['clarification'],'connection notice mismatch')
    p=dict(new_connection);p['edges']=[e for e in p['edges'] if e!=added[0]];p['nodes']=[n for n in p['nodes'] if n['id']!=later];p['snapshot']=old_connection['snapshot'];need(p==old_connection,'historical connection altered beyond notice')

def check_notices(m):
    need(m['reciprocal_continuation_notices']==[NOTICE['notice_id']] and set(m['permitted_historical_navigation_changes'])=={'frontier/dossiers/N751.txt','frontier/connections/N751.json'},'unscoped historical navigation')
    ns=[n for n in rows('agent/SEMANTIC_NOTICES.jsonl') if n['notice_id']==NOTICE['notice_id']];need(ns==[NOTICE],'notice content changed')
    need({x['target'] for x in NOTICE['material_updates']}==set(NOTICE['card_ids']),'notice not reciprocal')
    for ref in NOTICE['source_refs']:need(sha((ROOT/ref['path']).read_bytes())==ref['sha256'],'notice source changed')
    for r in ['N751','N760']:
        need(NOTICE['notice_id'] in (ROOT/('frontier/dossiers/'+r+'.txt')).read_text(),'notice not reciprocal')
        need(any(e['kind']=='material_update' and e['composition']==NOTICE['clarification'] for e in load('frontier/connections/'+r+'.json')['edges']),'connection not reciprocal')
    dp,cp='frontier/dossiers/N751.txt','frontier/connections/N751.json'
    check_projection(git('show',BASE+':'+dp).decode(),(ROOT/dp).read_text(),json.loads(git('show',BASE+':'+cp)),load(cp),NOTICE)
def main():
    m=load('updates/ET/SOURCE_MANIFEST.json');indexed=check_sources(m);mapping=load('updates/ET/CLAIMS.json');check_families(load('updates/ET/FAMILY_FIT.json'))
    need([route(e['id']) for e in mapping['claims']]==ROUTES,'claim coverage changed')
    check_notices(m)
    ledgers={p:rows(p) for p in ['indexes/claims.jsonl','frontier/CURRENT_CLAIM_STATUS.jsonl','indexes/source_metadata.jsonl','web/documents.jsonl']}
    for path,x in indexed.items():
        md=[a for a in ledgers['indexes/source_metadata.jsonl'] if a.get('source_id')==x['source_id']];doc=[a for a in ledgers['web/documents.jsonl'] if a.get('id')==x['source_id']]
        need(len(md)==len(doc)==1 and md[0]['sha256']==x['sha256'] and md[0]['path']==doc[0]['path']==path,'source metadata mismatch')
        if 'lines' in x:need('<pre>'+html.escape((ROOT/path).read_text())+'</pre>' in (ROOT/('web/'+doc[0]['url'])).read_text(),'source mirror changed')
        else:need(doc[0]['url']=='../'+path,'binary source route changed')
    catalog=load('indexes/agent_catalog.json')['claims'];web=load('web/catalog.json');proof_count=0;trace_ids=set();cp_ids=set()
    for e in mapping['claims']:
        cid=e['id'];r=route(cid);s=load('frontier/cards/'+cid+'.json');card=(ROOT/s['card_path']).read_bytes();check_status(s,card.decode())
        need(e['source_sha256']==indexed[e['source_path']]['sha256'] and e['source_id']==indexed[e['source_path']]['source_id'] and e['missing_artifacts']==[],'primary source mismatch')
        for pool,k in [(ledgers['frontier/CURRENT_CLAIM_STATUS.jsonl'],'card_id'),(ledgers['indexes/claims.jsonl'],'id'),(catalog,'id'),(web,'id')]:need(sum(x[k]==cid for x in pool)==1,'duplicate/missing claim')
        need(next(x for x in ledgers['frontier/CURRENT_CLAIM_STATUS.jsonl'] if x['card_id']==cid)==s,'status ledger mismatch')
        claim=next(x for x in ledgers['indexes/claims.jsonl'] if x['id']==cid);wc=next(x for x in web if x['id']==cid)
        need(claim['status']==e['status']==s['claim_status'] and claim['depends_on']==claim['scoped_dependencies']==[],'claim status/dependency mismatch')
        need(wc['source_paths']==claim['source_paths'] and wc['source_ids']==claim['source_ids'],'web provenance missing')
        need(sha(card)==s['card_sha256']==next(x for x in catalog if x['id']==cid)['card_sha256'] and (ROOT/('frontier/review_cards/'+cid+'.txt')).read_bytes().endswith(card),'card hash/wrapper mismatch')
        proofs=s['proof_availability']['located_proof_sources'];proof_count+=len(proofs)
        for ref in proofs+s['proof_availability']['available_evidence_sources']:
            x=indexed[ref['path']];need(ref['sha256']==x['sha256'],'source hash changed')
            if 'lines' in ref:need('lines' in x and 1<=ref['lines'][0]<=ref['lines'][1]<=x['lines'],'proof range changed')
            else:need(ref['path'].endswith(('.npz','.zip')) and 'lines' not in x,'unclassified binary evidence')
        for path in ['agent/routes.tsv']+['agent/topics/'+t+'.tsv' for t in s['topics']]:need(cid+'\t' in (ROOT/path).read_text(),'navigation route missing')
        gates=[g for g in rows('frontier/OPEN_PROOF_GATES.jsonl') if g['gate_id']=='G-ET-'+r+'-INDEPENDENT-REVIEW'];need(len(gates)==1,'gate missing');check_gate(gates[0],cid)
        t=load(e['workflow_trace']);validate_trace(t,ROOT);check_trace(t);trace_ids.add(t['id'])
        cp=load(e['checkpoint']);validate_record(cp,ROOT);need(cp['base_revision']==BASE and cp['parent_checkpoint_ids']==[] and cp['branch_id'].startswith('worker-et-'),'source ancestry invented');cp_ids.add(cp['branch_id'])
        generated=views(ROOT,{cp['branch_id']:{cp['checkpoint_id']:cp}});view='state/branches/'+cp['branch_id']+'.txt';need((ROOT/view).read_text()==generated[view],'checkpoint view stale')
        row=next(l for l in generated['state/branches.tsv'].splitlines() if l.startswith(cp['branch_id']+'\t'));need((ROOT/'state/branches.tsv').read_text().splitlines().count(row)==1,'checkpoint registry stale')
    need(proof_count==13 and len(trace_ids)==len(cp_ids)==1,'proof/trace/checkpoint coverage changed')
    gate=next(g for g in rows('frontier/OPEN_PROOF_GATES.jsonl') if g['gate_id']=='G-ET-N760-CAPABILITY');check_capability(gate,mapping['claims'][0]['id'])
    for path in list(ledgers)+['frontier/OPEN_PROOF_GATES.jsonl','state/branches.tsv','agent/routes.tsv','agent/SEMANTIC_NOTICES.jsonl']:
        need((ROOT/path).read_bytes().startswith(git('show',BASE+':'+path)),'historical ledger rewritten')
    for path,fields in [('indexes/agent_catalog.json',['claims']),('indexes/agent_graph.json',['nodes','edges'])]:
        old=json.loads(git('show',BASE+':'+path));now=load(path)
        for f in fields:need(now[f][:len(old[f])]==old[f],'historical graph/catalog rewritten')
    graph=load('indexes/agent_graph.json');nodes={x['id'] for x in graph['nodes']}
    need(len(nodes)==len(graph['nodes']) and all(x['from'] in nodes and x['to'] in nodes for x in graph['edges']),'graph integrity')
    for e in mapping['claims']:
        c=next(c for c in ledgers['indexes/claims.jsonl'] if c['id']==e['id']);need(set(c['source_ids'])=={x['to'] for x in graph['edges'] if x['from']==e['id'] and x['kind']=='provenance'},'claim provenance mismatch')
    old_alias=json.loads(git('show',BASE+':indexes/query_aliases.json'));need(all(load('indexes/query_aliases.json').get(k)==v for k,v in old_alias.items()),'earlier alias changed')
    old_paths=set(git('ls-tree','-r','--name-only',BASE).decode().splitlines());changed=set(git('diff','--name-only',BASE,'--','updates','cards','frontier/cards','frontier/review_cards','state/checkpoints','state/branches','evaluation','technology/records','web/pages').decode().splitlines())
    need(not changed & old_paths,'earlier scientific/source/checkpoint/evaluation object changed')
    outputs=json.loads(git('show',BASE+':agent/access_manifest.json'))['outputs'];scientific={p:h for p,h in outputs.items() if p.startswith(('frontier/dossiers/','frontier/connections/','frontier/proof_ranges/'))}
    changed_views={p for p,h in scientific.items() if not (ROOT/p).is_file() or sha((ROOT/p).read_bytes())!=h}
    need(changed_views==set(m['permitted_historical_navigation_changes']),'unscoped scientific navigation change')
    print(json.dumps(dict(intake='ET',status='PASS',original_files=32,original_bytes=12320208,archive_members=30,producer_hashes_checked=29,scientific_scripts_syntax_only=10,proof_ranges=13,cards=1,checkpoints=1,scoped_historical_views=2,earlier_scientific_views_unchanged=len(scientific)-2,scientific_scripts_executed=0)))
if __name__=='__main__':
    try:main()
    except (ValueError,KeyError,OSError) as e:print(str(e),file=sys.stderr);sys.exit(1)
