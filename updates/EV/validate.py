#!/usr/bin/env python3
"""Intake preservation and evidence-boundary checks; scientific code remains data."""
import ast,hashlib,html,json,stat,subprocess,sys
from pathlib import Path,PurePosixPath
from zipfile import ZipFile
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from evaluation.workflow_trace import validate as validate_trace
from state.publish_checkpoint import validate_record,views
BASE='d47777a817e273668b6af3f0548cd02af92c6bc5'
ROUTES=['N762','N763']
PINS = {'updates/EV/package/genesis_contact/ORIGINAL_PASTED_SOURCE.txt': '569e389416e0893f7487df58ff8319c8d5341ee9618b7d731005f9bf3b481843', 'updates/EV/package/cray_compressed/ORIGINAL_PASTED_SOURCE.txt': '8e7defab3ca3389bf8a2988e0a5e2935bf3c16bdd67f9df1c3a73d243d8539a9', 'updates/EV/package/genesis_contact/astra_genesis_contact_completion.zip': '946e12e61075f97dbe31303a30d5291bd8f258939b85210f552772c78e948cd9', 'updates/EV/package/genesis_contact/recovered/astra_hadwiger/RESEARCH_NOTE.md': '8f9459b55b36f6f506337b82c142525b9a56ce4deb91b13790db70f69426c6f2', 'updates/EV/package/genesis_contact/recovered/astra_hadwiger/SHA256.json': 'd8be471a237250f7c58e8a5d93d799b7f3480f5dea5e4f0a887be52c9d66e06a', 'updates/EV/package/genesis_contact/recovered/astra_hadwiger/critical_palette_atlas.json': '885876a3a375a3d96fd174d198ec125aa173f68f285c9e8a1800eb48d102b1a9', 'updates/EV/package/genesis_contact/recovered/astra_hadwiger/critical_palette_checks.json': '4cae110c5c7eb67475a73a15c1a8636c9a9ff42ec98952d833dd775713f14141', 'updates/EV/package/genesis_contact/recovered/astra_hadwiger/critical_palette_checks.py': '9b97ed5aab065d0a4de3f970d05d28a3128e50036c4fffe284330130097d889a', 'updates/EV/package/genesis_contact/recovered/astra_hadwiger/finite_checks.json': '2166d72bb62da29507bd4eefec277607c503c985c04670355a71bd904a29f3bd', 'updates/EV/package/genesis_contact/recovered/astra_hadwiger/finite_checks.py': 'be32649a444398a3588ea80b04ecf283411eb0058dc6b291e3bd454c221eaa8f', 'updates/EV/package/genesis_contact/recovered/astra_hadwiger/pin_release.py': '085de71e5382041c75897bb96997ccf8c0b46ea387061055dbcaf2ab5c7fbd9a', 'updates/EV/package/genesis_contact/recovered/astra_hadwiger/pin_release_checks.json': '1f9f7250c179997c752286006950c328aef481bb8d8370d2c2afd9ce82d32825', 'updates/EV/package/genesis_contact/recovered/astra_hadwiger/requirements.txt': '10cab7ad30fe7e3954d086586ea6e1709df2c4e58ed2b85646f855441408e222', 'updates/EV/package/cray_compressed/cray_compressed_transport_bundle.zip': '74fdbd1612f0620e3ea72f98c08e6a7f7ab3f1e84ed316d273c0128ae325e598', 'updates/EV/package/cray_compressed/recovered/cray_compressed_transport/README.md': '5e82cca0e68bfd49af7f4a936b1d29010842b029ba3d8b17cba095091d5249bf', 'updates/EV/package/cray_compressed/recovered/cray_compressed_transport/balanced_certificate.json': 'e7c8e9ee90b566398e48370006eb3fce38105c8b87ad49cb8e2fcf50ad65b50f', 'updates/EV/package/cray_compressed/recovered/cray_compressed_transport/balanced_certificate.py': '5c4a456075e9c6d6be0155d42420ea00ccb0049a4daa5440df90ae275491c30e', 'updates/EV/package/cray_compressed/recovered/cray_compressed_transport/balanced_grammar.py': '017514b2b2c09d885b7e23148560b8aa70d671c98c1dbe0949825d2c150099ad', 'updates/EV/package/cray_compressed/recovered/cray_compressed_transport/balanced_tests.json': '025a28e957c9c89e0498e3a7001c01c038c16f1219b5c00954cf408257fa98b5', 'updates/EV/package/cray_compressed/recovered/cray_compressed_transport/cray_compressed_transport_report.md': '32055affdd7488f16da5ad1eb35af1dbca495d745fa4fa5020bbd53f3aa04a4f', 'updates/EV/package/cray_compressed/recovered/cray_compressed_transport/cylinder_flow.py': '7bccd6384d8d74d992dc5a38abbacbaba8d4829f5ea13f8e3ed6fae382ee5df9', 'updates/EV/package/cray_compressed/recovered/cray_compressed_transport/frame_grammar.py': 'a6bb3d310b48964b0ff2e44df02797c64ac62847cb3a2fc4519f3336ea556b41', 'updates/EV/package/cray_compressed/recovered/cray_compressed_transport/invariant_pivot.py': '314fe894d321bd07796fa23088a0055907467f90480df292236f9dc7e4c93fba', 'updates/EV/package/cray_compressed/recovered/cray_compressed_transport/primitive_benchmarks.json': '71c5fe85a205727f079acc80f48aab021ad7b3968890fa6558e3829b7683ec12', 'updates/EV/package/cray_compressed/recovered/cray_compressed_transport/prior_nonlocal_transport_report.md': 'd502f80ffb3d397a7ea63a1ffcb65b397685955c64ca6d1f6058eb90c9762fc1', 'updates/EV/package/cray_compressed/recovered/cray_compressed_transport/probability_certificate.json': 'e1f155e75ce4e1041faf06b2dfe1ae43a7efecb34bbad313a0c8f0cdddd0244b', 'updates/EV/package/cray_compressed/recovered/cray_compressed_transport/probability_certificate.py': '8b5619e6b5ad2d2f9c78b2d761e2460df79c7977f372c087cd3b408c2a382b01', 'updates/EV/package/cray_compressed/recovered/cray_compressed_transport/reproduce.py': 'e2ac651971f904ba31737e137cb933837c52308c502d334c1a6d2e8d11b5bb8d', 'updates/EV/package/cray_compressed/recovered/cray_compressed_transport/reproduction_log.txt': 'fee00bfa74eef2368e4abd14e61bf44dd217f1190b509e1b2f96aa2ea8860d66', 'updates/EV/package/cray_compressed/recovered/cray_compressed_transport/reproduction_resources.txt': '1c6cc9236ba49106e7f2562a8c9ba0426dae0bfab4941c5a4f40c453d474421e', 'updates/EV/package/cray_compressed/recovered/cray_compressed_transport/reproduction_summary.json': 'fee00bfa74eef2368e4abd14e61bf44dd217f1190b509e1b2f96aa2ea8860d66', 'updates/EV/package/cray_compressed/recovered/cray_compressed_transport/test_balanced.py': 'c12b703bcf58595f16e1707b94a51cd249532b7358168bd3034d65021023058a', 'updates/EV/package/cray_compressed/recovered/cray_compressed_transport/test_research.py': 'ed9f5dceada34ae62557af4667b8ffcd89142929ca6a619f9feb510ca45eb976', 'updates/EV/package/cray_compressed/recovered/cray_compressed_transport/test_results.json': '9c1a50ad3a7971bea20d3c8a46c4e8eeb9c33fe564b332a5599c0778c8b8451d', 'updates/EV/package/cray_compressed/recovered/cray_compressed_transport/manifest.sha256': '564afbce5eaeef775a23ac80686f0d3af1ee38039504712995ac70a075cb034b'}
NOTICE = {'notice_id': 'SN-EV-N760-N763-SCOPED-CONTINUATION', 'card_ids': ['N760-frozen-reservoir-lifting-and-nonlocal-hard-ka-certificate', 'N763-balanced-path-law-compression-and-rare-frame-concentration-in-hard-ka'], 'issue': 'Compressed source-module continuation with practical dense-capability gap retained.', 'status': 'source_derived_unreviewed_continuation_only', 'clarification': 'N763 continues N760 with balanced strip pushforward/moment laws, a conserved-division cylinder current and a port-independent compressed hard-KA source module. The p=.80,L4096 certificate10^-11593 is uninformative; useful dense transport and whole signed-current low-concentration bounds remain open. N760 nonlocal lifting is retained as a source-reported dependency, and N751 exact-local obstruction remains intact. No historical theorem, source, status or gate is replaced or closed.', 'material_updates': [{'target': 'N763-balanced-path-law-compression-and-rare-frame-concentration-in-hard-ka', 'scope': 'N763 continues N760 with balanced strip pushforward/moment laws, a conserved-division cylinder current and a port-independent compressed hard-KA source module. The p=.80,L4096 certificate10^-11593 is uninformative; useful dense transport and whole signed-current low-concentration bounds remain open. N760 nonlocal lifting is retained as a source-reported dependency, and N751 exact-local obstruction remains intact. No historical theorem, source, status or gate is replaced or closed.', 'relation_status': 'new source-reported scoped candidate'}, {'target': 'N760-frozen-reservoir-lifting-and-nonlocal-hard-ka-certificate', 'scope': 'N763 continues N760 with balanced strip pushforward/moment laws, a conserved-division cylinder current and a port-independent compressed hard-KA source module. The p=.80,L4096 certificate10^-11593 is uninformative; useful dense transport and whole signed-current low-concentration bounds remain open. N760 nonlocal lifting is retained as a source-reported dependency, and N751 exact-local obstruction remains intact. No historical theorem, source, status or gate is replaced or closed.', 'relation_status': 'historical result/status/gate retained'}], 'source_refs': [{'path': 'updates/EV/package/cray_compressed/recovered/cray_compressed_transport/cray_compressed_transport_report.md', 'source_id': 'src-EV-n763-46250d0310bb', 'sha256': '32055affdd7488f16da5ad1eb35af1dbca495d745fa4fa5020bbd53f3aa04a4f', 'lines': [1, 90], 'range_scope': 'Original hard bulk coefficient, prior frozen-reservoir lift and rejected representations.', 'read_path': 'updates/EV/package/cray_compressed/recovered/cray_compressed_transport/cray_compressed_transport_report.md', 'hash_kind': 'original_utf8_bytes'}, {'path': 'updates/EV/package/cray_compressed/recovered/cray_compressed_transport/cray_compressed_transport_report.md', 'source_id': 'src-EV-n763-46250d0310bb', 'sha256': '32055affdd7488f16da5ad1eb35af1dbca495d745fa4fa5020bbd53f3aa04a4f', 'lines': [91, 229], 'range_scope': 'Cylinder intersection moments, conserved-division lemma, exact8m-10-term empty-column current and energy.', 'read_path': 'updates/EV/package/cray_compressed/recovered/cray_compressed_transport/cray_compressed_transport_report.md', 'hash_kind': 'original_utf8_bytes'}, {'path': 'updates/EV/package/cray_compressed/recovered/cray_compressed_transport/cray_compressed_transport_report.md', 'source_id': 'src-EV-n763-46250d0310bb', 'sha256': '32055affdd7488f16da5ad1eb35af1dbca495d745fa4fa5020bbd53f3aa04a4f', 'lines': [230, 304], 'range_scope': 'Balanced strip pushforward, endpoint optimality, exact recurrence and composition.', 'read_path': 'updates/EV/package/cray_compressed/recovered/cray_compressed_transport/cray_compressed_transport_report.md', 'hash_kind': 'original_utf8_bytes'}, {'path': 'updates/EV/package/cray_compressed/recovered/cray_compressed_transport/cray_compressed_transport_report.md', 'source_id': 'src-EV-n763-46250d0310bb', 'sha256': '32055affdd7488f16da5ad1eb35af1dbca495d745fa4fa5020bbd53f3aa04a4f', 'lines': [305, 393], 'range_scope': 'Port-independent recursive gates, hard legal frame expansion and overlapping-growth probability proof.', 'read_path': 'updates/EV/package/cray_compressed/recovered/cray_compressed_transport/cray_compressed_transport_report.md', 'hash_kind': 'original_utf8_bytes'}, {'path': 'updates/EV/package/cray_compressed/recovered/cray_compressed_transport/cray_compressed_transport_report.md', 'source_id': 'src-EV-n763-46250d0310bb', 'sha256': '32055affdd7488f16da5ad1eb35af1dbca495d745fa4fa5020bbd53f3aa04a4f', 'lines': [394, 414], 'range_scope': 'Exact ensemble source-defect identity and reservoir-restoring port word.', 'read_path': 'updates/EV/package/cray_compressed/recovered/cray_compressed_transport/cray_compressed_transport_report.md', 'hash_kind': 'original_utf8_bytes'}, {'path': 'updates/EV/package/cray_compressed/recovered/cray_compressed_transport/cray_compressed_transport_report.md', 'source_id': 'src-EV-n763-46250d0310bb', 'sha256': '32055affdd7488f16da5ad1eb35af1dbca495d745fa4fa5020bbd53f3aa04a4f', 'lines': [415, 533], 'range_scope': 'Whole path-density and weighted energy bound; marked ports, selection, return and instruction costs.', 'read_path': 'updates/EV/package/cray_compressed/recovered/cray_compressed_transport/cray_compressed_transport_report.md', 'hash_kind': 'original_utf8_bytes'}, {'path': 'updates/EV/package/cray_compressed/recovered/cray_compressed_transport/cray_compressed_transport_report.md', 'source_id': 'src-EV-n763-46250d0310bb', 'sha256': '32055affdd7488f16da5ad1eb35af1dbca495d745fa4fa5020bbd53f3aa04a4f', 'lines': [534, 606], 'range_scope': 'Producer rational certificates, finite tests, regeneration resources and unexecuted large instance.', 'read_path': 'updates/EV/package/cray_compressed/recovered/cray_compressed_transport/cray_compressed_transport_report.md', 'hash_kind': 'original_utf8_bytes'}, {'path': 'updates/EV/package/cray_compressed/recovered/cray_compressed_transport/cray_compressed_transport_report.md', 'source_id': 'src-EV-n763-46250d0310bb', 'sha256': '32055affdd7488f16da5ad1eb35af1dbca495d745fa4fa5020bbd53f3aa04a4f', 'lines': [607, 671], 'range_scope': 'Positive preparation concentration theorem, signed-current scope limitation and missing active-interface theorem.', 'read_path': 'updates/EV/package/cray_compressed/recovered/cray_compressed_transport/cray_compressed_transport_report.md', 'hash_kind': 'original_utf8_bytes'}, {'path': 'updates/EV/package/cray_compressed/recovered/cray_compressed_transport/cray_compressed_transport_report.md', 'source_id': 'src-EV-n763-46250d0310bb', 'sha256': '32055affdd7488f16da5ad1eb35af1dbca495d745fa4fa5020bbd53f3aa04a4f', 'lines': [672, 703], 'range_scope': 'Established stronger asymptotics, priority limits, references and imported internal theorem.', 'read_path': 'updates/EV/package/cray_compressed/recovered/cray_compressed_transport/cray_compressed_transport_report.md', 'hash_kind': 'original_utf8_bytes'}], 'source_revision': 'd47777a817e273668b6af3f0548cd02af92c6bc5'}
def need(ok,message):
    if not ok:raise ValueError(message)
def sha(d):return hashlib.sha256(d).hexdigest()
def load(p):return json.loads((ROOT/p).read_text())
def rows(p):return [json.loads(l) for l in (ROOT/p).read_text().splitlines() if l.strip()]
def git(*args):return subprocess.check_output(['git','-C',str(ROOT),*args])
def route(c):return c.split('-',1)[0]



def check_sources(m):
    need(m['intake_base_revision']==BASE and m['source_handling']=='source=DATA','source authority changed')
    need(len(m['originals'])==len(m['recovered_packages'])==2,'source coverage changed')
    items=m['originals']+[x for p in m['recovered_packages'] for x in [p]+p['members']];indexed={x['path']:x for x in items}
    need(len(items)==len(indexed)==35 and set(indexed)==set(PINS),'source coverage changed')
    need(sum(x['bytes'] for x in items)==363234 and [x['lines'] for x in m['originals']]==[169,174],'source extent changed')
    need(m['scientific_scripts_executed']==0,'integrity promoted to scientific replay')
    for path,x in indexed.items():
        p=PurePosixPath(path);need(not p.is_absolute() and '..' not in p.parts and not(ROOT/path).is_symlink(),'unsafe original path')
        d=(ROOT/path).read_bytes();need(sha(d)==x['sha256']==PINS[path] and len(d)==x['bytes'],'original bytes/hash changed')
        if 'lines' in x:need(len(d.decode().splitlines())==x['lines'],'source line extent changed')
        if path.endswith('.py'):ast.parse(d,filename=path)
    actual={p.relative_to(ROOT).as_posix() for p in (ROOT/'updates/EV/package').rglob('*') if p.is_file()};need(actual==set(PINS),'extra/missing public disclosure')
    for pkg,prefix,manifest,count in zip(m['recovered_packages'],['astra_hadwiger/','cray_compressed_transport/'],['SHA256.json','manifest.sha256'],[10,21]):
        need(pkg['verification']['scientific_code_execution']==pkg['verification']['independent_proof_review']=='not performed','integrity promoted to proof review')
        with ZipFile(ROOT/pkg['archive_path']) as z:
            need(z.testzip() is None,'ZIP CRC failure');names=z.namelist();need(len(names)==len(set(names))==count and set(names)=={x['archive_member'] for x in pkg['members']},'ZIP member coverage changed')
            for info in z.infolist():
                p=PurePosixPath(info.filename);need(not p.is_absolute() and '..' not in p.parts and chr(92) not in info.filename and not stat.S_ISLNK(info.external_attr>>16) and not info.is_dir(),'unsafe ZIP member')
                x=next(x for x in pkg['members'] if x['archive_member']==info.filename);need(z.read(info)==(ROOT/x['path']).read_bytes(),'extracted member changed')
            raw=z.read(prefix+manifest).decode();producer=json.loads(raw) if manifest.endswith('.json') else {l.split('  ',1)[1]:l.split('  ',1)[0] for l in raw.splitlines()}
            need(len(producer)==pkg['producer_hashes_checked']==count-1 and set(producer)=={n.removeprefix(prefix) for n in names if n!=prefix+manifest},'producer manifest coverage changed')
            for n,h in producer.items():need(sha(z.read(prefix+n))==h,'producer digest mismatch')
    prior=m['recovered_packages'][1]['prior_report_identity'];need(prior['byte_identical'] is True and sha((ROOT/prior['path']).read_bytes())==prior['sha256'] and (ROOT/prior['path']).read_bytes()==(ROOT/prior['historical_path']).read_bytes(),'prior theorem report changed')
    need(sum(p.endswith('.py') for p in indexed)==12,'script coverage changed')
    return indexed

def check_status(s,text):
    r=route(s['card_id']);need(r in ROUTES and s['claim_status']=='source_derived_unreviewed','scientific promotion')
    need(s['validation']['external_correctness']==s['validation']['historical_priority']=='UNKNOWN','correctness/priority invented')
    need(s['proof_availability']['classification']=='original_proof_accounts_and_recovered_producer_artifacts_not_independently_audited','availability promoted to proof audit')
    expected={'N762':['external:EV_MATCHING_NEGATIVE_DEPENDENCY','external:EV_SUZUKI_TITS_DOMINATING_OBSTRUCTION','external:EV_RECURSIVE_PERFECT_PARTITION_FAMILY'],'N763':['external:EV_N760_FROZEN_RESERVOIR_LIFT','external:EV_KA_FRAME_GEOMETRY']}
    need([x['target'] for x in s['depends_on']]==expected[r],'imported premise coverage changed')
    need(all(s[k]==[] for k in ['supersedes','invalidates','contrasting_blockers']),'historical theorem superseded')
    if r=='N762':
        need(s['material_updates']==[],'unrelated family promoted')
        required=['UNRESOLVED','induced-four-cycle','1/(4e)','not an optimal graph threshold','Delta(F)','no repeated-repair convergence','h>=chi, not equality','critical','unproved proposal','entire-graph counterexample remains intact','repeated isomorphism','equivalent to exact Hadwiger','unreconciled','Process-only Kakeya','no corresponding theorem or proof']
    else:
        need([route(x['target']) for x in s['material_updates']]==['N760'] and s['material_updates'][0]['scope']==NOTICE['clarification'],'scoped continuation changed')
        required=['collective/bulk','not tagged','10^(-11593)','not an informative prediction','UNNORMALIZED','not the full current energy','not independent','changing active-front counts is invalid','N751 exact-local no-go remains intact','33,554,432','not an executed word','bit','pointwise summation is not proved','not every signed port-exchange','no polynomial accuracy','Shapira','UNKNOWN']
    need(all(x.lower() in text.lower() for x in required),'essential scientific boundary erased')

def check_trace(t):
    r='N762' if t['id']=='RW-ev-genesis-contact' else 'N763';need(t['id'] in ['RW-ev-genesis-contact','RW-ev-cray-compressed'],'workflow identity changed')
    expected={'N762':('independent_selective_capital','UNKNOWN',3746,[1,23],[24,24],[33,169]),'N763':('targeted_warm_continuation','same',3348,[1,17],[18,18],[22,174])}[r]
    mode,conv,dur,prompt,duration,result=expected
    need(t['mode']==mode and t['context']['conversation_relation']==conv,'workflow/context invented')
    need(t['prompt_availability']=='exact' and t['prompt_ref_ids']==['prompt'],'prompt provenance changed')
    res=t['resources'];need(res['reported_inference_seconds']==dur and res['reported_duration_ref_ids']==['duration'],'reported duration changed')
    need(all(v is None for v in t['model'].values()) and all(v is None for v in res['usage'].values()) and res['worker_invocations'] is None,'unmeasured model/usage invented')
    need(res['worker_receipt_ref_ids']==res['usage_receipt_ref_ids']==[] and t['matched_run_id'] is None,'unsupported comparison')
    need(t['advance']['verification']=='producer_reported' and t['advance']['verification_receipt'] is None,'producer diagnostics promoted')
    refs={x['id']:x for x in t['refs']};need(refs['prompt']['lines']==prompt and refs['duration']['lines']==duration and refs['result']['lines']==result,'prompt/duration/result range changed')

def check_families(f):
    need(f['base_revision']==BASE and f['relation_semantics'].startswith('One scoped reciprocal continuation;'),'family authority changed')
    need([route(x['card_id']) for x in f['decisions']]==ROUTES,'family coverage changed')
    need([[route(x['card_id']) for x in d['comparisons']] for d in f['decisions']]==[['N699'],['N760','N751']] and all(x['scope'] for d in f['decisions'] for x in d['comparisons']),'family comparison missing/unscoped')
    need(f['decisions'][1]['comparisons'][0]['scope']==NOTICE['clarification'],'continuation mismatch')
    known={x['id'] for x in rows('indexes/claims.jsonl')};need(all(x['card_id'] in known for d in f['decisions'] for x in d['comparisons']),'family target unknown')
def check_gate(g,cid):need(g['status']=='open' and g['completion_evidence']==[] and g['card_ids']==[cid],'unresolved gate promoted')
def check_capability(g,cid):
    check_gate(g,cid)
    need(all(x in g['question'].lower() for x in ['whole signed','port-independent','second-moment','bit costs','baseline']),'capability obligation erased')
def check_projection(old_text,new_text,old_connection,new_connection,notice):
    block='SEMANTIC NOTICE '+notice['notice_id']+'\n'+notice['status']+': '+notice['clarification']+'\n\n'
    need(new_text.count(block)==1,'notice projection missing/duplicated')
    normalize=lambda t:'\n'.join(l for l in t.splitlines() if not l.startswith('snapshot_input_sha256='))
    need(normalize(new_text.replace(block,''))==normalize(old_text),'historical dossier altered beyond notice')
    earlier,later=notice['card_ids'];added=[e for e in new_connection['edges'] if e['from']==later and e['to']==earlier and e['kind']=='material_update']
    need(len(added)==1 and added[0]['composition']==notice['clarification'],'connection notice mismatch')
    p=dict(new_connection);p['edges']=[e for e in p['edges'] if e!=added[0]];p['nodes']=[n for n in p['nodes'] if n['id']!=later];p['snapshot']=old_connection['snapshot'];need(p==old_connection,'historical connection altered beyond notice')

def check_notices(m):
    need(m['reciprocal_continuation_notices']==[NOTICE['notice_id']] and set(m['permitted_historical_navigation_changes'])=={'frontier/dossiers/N760.txt','frontier/connections/N760.json'},'unscoped historical navigation')
    ns=[n for n in rows('agent/SEMANTIC_NOTICES.jsonl') if n['notice_id']==NOTICE['notice_id']];need(ns==[NOTICE],'notice content changed')
    need({x['target'] for x in NOTICE['material_updates']}==set(NOTICE['card_ids']),'notice not reciprocal')
    for ref in NOTICE['source_refs']:need(sha((ROOT/ref['path']).read_bytes())==ref['sha256'],'notice source changed')
    for r in ['N760','N763']:
        need(NOTICE['notice_id'] in (ROOT/('frontier/dossiers/'+r+'.txt')).read_text(),'notice not reciprocal')
        need(any(e['kind']=='material_update' and e['composition']==NOTICE['clarification'] for e in load('frontier/connections/'+r+'.json')['edges']),'connection not reciprocal')
    dp,cp='frontier/dossiers/N760.txt','frontier/connections/N760.json'
    check_projection(git('show',BASE+':'+dp).decode(),(ROOT/dp).read_text(),json.loads(git('show',BASE+':'+cp)),load(cp),NOTICE)
def main():
    m=load('updates/EV/SOURCE_MANIFEST.json');indexed=check_sources(m);mapping=load('updates/EV/CLAIMS.json');check_families(load('updates/EV/FAMILY_FIT.json'))
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
        need(claim['status']==e['status']==s['claim_status'] and claim['depends_on']==[x['target'] for x in s['depends_on']] and claim['scoped_dependencies']==[],'claim status/dependency mismatch')
        need(wc['source_paths']==claim['source_paths'] and wc['source_ids']==claim['source_ids'],'web provenance missing')
        need(sha(card)==s['card_sha256']==next(x for x in catalog if x['id']==cid)['card_sha256'] and (ROOT/('frontier/review_cards/'+cid+'.txt')).read_bytes().endswith(card),'card hash/wrapper mismatch')
        proofs=s['proof_availability']['located_proof_sources'];proof_count+=len(proofs)
        for ref in proofs+s['proof_availability']['available_evidence_sources']:
            x=indexed[ref['path']];need(ref['sha256']==x['sha256'],'source hash changed')
            if 'lines' in ref:need('lines' in x and 1<=ref['lines'][0]<=ref['lines'][1]<=x['lines'],'proof range changed')
            else:need(ref['path'].endswith(('.npz','.zip')) and 'lines' not in x,'unclassified binary evidence')
        for path in ['agent/routes.tsv']+['agent/topics/'+t+'.tsv' for t in s['topics']]:need(cid+'\t' in (ROOT/path).read_text(),'navigation route missing')
        gates=[g for g in rows('frontier/OPEN_PROOF_GATES.jsonl') if g['gate_id']=='G-EV-'+r+'-INDEPENDENT-REVIEW'];need(len(gates)==1,'gate missing');check_gate(gates[0],cid)
        t=load(e['workflow_trace']);validate_trace(t,ROOT);check_trace(t);trace_ids.add(t['id'])
        cp=load(e['checkpoint']);validate_record(cp,ROOT);need(cp['base_revision']==BASE and cp['parent_checkpoint_ids']==[] and cp['branch_id'].startswith('worker-ev-'),'source ancestry invented');cp_ids.add(cp['branch_id'])
        generated=views(ROOT,{cp['branch_id']:{cp['checkpoint_id']:cp}});view='state/branches/'+cp['branch_id']+'.txt';need((ROOT/view).read_text()==generated[view],'checkpoint view stale')
        row=next(l for l in generated['state/branches.tsv'].splitlines() if l.startswith(cp['branch_id']+'\t'));need((ROOT/'state/branches.tsv').read_text().splitlines().count(row)==1,'checkpoint registry stale')
    need(proof_count==24 and len(trace_ids)==len(cp_ids)==2,'proof/trace/checkpoint coverage changed')
    gate=next(g for g in rows('frontier/OPEN_PROOF_GATES.jsonl') if g['gate_id']=='G-EV-N763-CAPABILITY');check_capability(gate,mapping['claims'][1]['id'])
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
    print(json.dumps(dict(intake='EV',status='PASS',original_files=35,original_bytes=363234,archive_members=31,producer_hashes_checked=29,scientific_scripts_syntax_only=12,proof_ranges=24,cards=2,checkpoints=2,scoped_historical_views=2,earlier_scientific_views_unchanged=len(scientific)-2,scientific_scripts_executed=0)))
if __name__=='__main__':
    try:main()
    except (ValueError,KeyError,OSError) as e:print(str(e),file=sys.stderr);sys.exit(1)
