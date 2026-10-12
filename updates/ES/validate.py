#!/usr/bin/env python3
"""Preservation/navigation checks only; never executes campaign scientific code."""
import ast, hashlib, html, json, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from evaluation.workflow_trace import validate as validate_trace
from state.publish_checkpoint import validate_record, views
BASE='76f1e365648e225f89bff437693e7bd148cc88d9'
ROUTES=['N757','N758','N759']
PINS = {'updates/ES/package/adaptive_invention/CLAIM_LEDGER.json': '06bfd7ed30282173f1b5c50f3c98c6fa127881f6b66182848f7abd7f1c0a6f7d', 'updates/ES/package/adaptive_invention/REPLAY.txt': '5a1a670bed575b9f36cd86a8050fdced321123276efbccf032f21839798979c9', 'updates/ES/package/adaptive_invention/RESEARCH_STATE.txt': 'e6a9512aaf6326d5fac71761452c4c8868c3de096d5760aa68ac84bc72c4d205', 'updates/ES/package/adaptive_invention/algebraic_exchange/RESULTS.txt': 'e0906a8ab9e2455fed0a8f7fd1b61f236d518be312450fc3877d1f95aff1a62c', 'updates/ES/package/adaptive_invention/algebraic_exchange/verified.json': 'a0e27148b404590b598095b870ea29b76ea0094da629f098467aff0b0c86b8ae', 'updates/ES/package/adaptive_invention/algebraic_exchange/verify_exact.py': 'd845ff035036a440b948a544f622d1c839aadb13ae47b77f3fbf71c85818cb11', 'updates/ES/package/adaptive_invention/kinetic_energy_bridge/WORKING_MATHEMATICS.md': '98d9f8aea25d63603d2abb1ed4ce1430e9b5267a4a9cdb5e5dbfdf11a8887e71', 'updates/ES/package/adaptive_invention/kinetic_energy_bridge/checks.json': '7230cb6b2c14941d9f0e6da89c2ab5176b8c31d23346e4e66f6a83e87567636f', 'updates/ES/package/adaptive_invention/kinetic_energy_bridge/verify.py': '6e7d299c1e34be8dd060110f6a50d459c12c0bd64b63f9d82b05953ac194bb9d', 'updates/ES/package/adaptive_invention/kinetic_recombination/dimer_experiment.json': '70695af9beb1f990ec0d95bf887ca4b796f9607bd6aa3b7c683630009c2e0f3e', 'updates/ES/package/adaptive_invention/kinetic_recombination/echo_counterexample.json': 'd9d54323310799da766a1a88a923edaf1f9dac66a66f84b5f55448a3336bb92c', 'updates/ES/package/adaptive_invention/kinetic_recombination/prototypes.py': '39265ee8ae100fe68a0e78bec0d643e0c5afee4a49453d9a5ff204164eca5c8a', 'updates/ES/package/adaptive_invention/kinetic_recombination/radial_screening.json': '5c1191358af680911a9eccc0ac97dafe8000d61e642d27e2a8f61154b0695c43', 'updates/ES/package/adaptive_invention/kinetic_recombination/ring_response.json': '817f7262591fbd4bc8226346a160ef6ab637d18fad432a64d86ec97e7684bb60', 'updates/ES/package/adaptive_invention/projective_geometry/FINITE_TIME_INDEPENDENT_CHECK.md': '46ed9a7401d11d896e99a12add69509344c088b4a435596c3dbc3c5307d7dff1', 'updates/ES/package/adaptive_invention/projective_geometry/FINITE_TIME_TEST_RESULTS.json': '525fac9d47dbfcb7d8f3d6aa3aad78d4078619e4c4529445f3caf3390a94cec7', 'updates/ES/package/adaptive_invention/projective_geometry/TEST_RESULTS.json': '3be426ed52de8bc78f80ded892ab2368a05949182fc02424f4c57f9be18552fe', 'updates/ES/package/adaptive_invention/projective_geometry/WORKING_MATHEMATICS.md': '36a46d5e312f238ce017255dc235f120fdfabaaf2c767441669004f6f40aba02', 'updates/ES/package/adaptive_invention/projective_geometry/decisive_tests.py': 'b355f66eadbac0eddbd74411e3eabe108adb03e268eb4877f3f295d2a9bd8a2f', 'updates/ES/package/adaptive_invention/projective_geometry/finite_time_tests.py': '1f14aeda152f6faa350720ae2aef5a75116b711140c2340f897822bdbce00a7e', 'updates/ES/package/adaptive_invention/quantum_influence/BASELINES.md': '1f4a6668dcb4c31b67c7a8ae4b5dd7e6a355d3255fbb90c3d2916ccd1331e530', 'updates/ES/package/adaptive_invention/quantum_influence/CLAIM_LEDGER.json': 'a8c227806952d76defbd82b3d6c7523b0ac0273ee24973cd11d8944db4a92f28', 'updates/ES/package/adaptive_invention/quantum_influence/GAUGE_MATH.md': '99a14abe96107776942fe493f12052a755808c3575f701482531597b9803564d', 'updates/ES/package/adaptive_invention/quantum_influence/GAUGE_RESULTS.json': '55f033b501d46c18e285b04f318427896e43ce518bc54839c50ed7b53596236e', 'updates/ES/package/adaptive_invention/quantum_influence/RESULTS.json': '81fd954b47a95e23ee58c516b3408b455a02241fc5dda0243dcf2227e6bdf4ef', 'updates/ES/package/adaptive_invention/quantum_influence/WORKING_MATH.md': 'fbf337a9703a9eab9ac7f4413766d7ae7465ef7e85f9125367dee48a0908ebcb', 'updates/ES/package/adaptive_invention/quantum_influence/derive_and_test.py': '98e5c763068c90cfbe8a1c32e3b3e644dfd008ee8f0b850cbfa829227422b8f3', 'updates/ES/package/adaptive_invention/quantum_influence/gauge_quotient.py': 'a6a7c7b7095b5cfec3e910f4fdc2a3f8b26a15ef6d8f2fe0525b4808b8784e5d', 'updates/ES/package/adaptive_invention/root/FINITE_TIME_RESONANCE.txt': '61f66e7f6bf3f34109be445718ed7da8a9229afe8c244c1486b3f3e2dd01d07d', 'updates/ES/package/adaptive_invention/root/resonance_evidence.json': 'cba8962e47ec200c1de163e922df77d5464cc211888605a4d84505ba65e37e5d', 'updates/ES/package/adaptive_invention/root/resonance_experiment.py': '95603e4cde9b6464bfe99d842cb14879c41530a036620510b85df7a83d573ffd', 'updates/ES/package/adaptive_invention/root/resonance_stdout.json': 'ccbc4c1317741f343dd0dbf351a5b5f367fd6e511d114a179e8bdb58c3dc3cad', 'updates/ES/package/adaptive_invention/signed_block_transport/RESULTS.md': '061cbb4b7ab0c2622876efac282ad1f798329185f61f82d538aebd770f99c30e', 'updates/ES/package/adaptive_invention/signed_block_transport/checks.json': '15ddacb985cf70711cdae807348be458f397b901bc8eb73ffe71dfcad6ed4a46', 'updates/ES/package/adaptive_invention/signed_block_transport/verify.py': '3e7caa802f7612f2e9d4e7db2b3a1a01d6b6288f16426b743bc24365a7d9d625', 'updates/ES/package/adaptive_invention/sources/RECEIPTS.json': 'f2742f62ba67e4bcb2ef8a3738c2fa5d13b14fe7b9cffe1936844bdf53bcf4cf', 'updates/ES/package/adaptive_invention/sources/astra_00_START_HERE.txt': '4a91985ece91557af12ba5c216e7fe17cf5dd000596e9a0c73b0b6705498f360', 'updates/ES/package/adaptive_invention/sources/astra_N733_overlap_proof.txt': '29f584b80d00c90db9186af68f963c437168c085b01db3ecc7d0c2594f2946ec', 'updates/ES/package/adaptive_invention/sources/astra_agent_CURRENT.txt': '4387a47897626b45b2b0f0c51d95a9c1b79878e22155f4b44b7800d17599b0c4', 'updates/ES/package/adaptive_invention/sources/astra_agent_concepts.txt': '0a61f87ec70f349d37ce704c474ba8ec5fe9a3619cc9e88d21704858d73d913c', 'updates/ES/package/adaptive_invention/sources/astra_agent_concepts_c.tsv': 'a480827605e886be5572df9f807d76cf66f7305c0ace54b6c191ad40bf2204c1', 'updates/ES/package/adaptive_invention/sources/astra_agent_concepts_l.tsv': '94d0d5e81f70f162588d20c5ab80e148eac710db57449827eda09550963566e7', 'updates/ES/package/adaptive_invention/sources/astra_frontier_dossiers_N393.txt': '86c35277b980630a7921fe68ccc5b3129c3dc12ce764865d0281532ac534e1d6', 'updates/ES/package/adaptive_invention/sources/astra_frontier_dossiers_N394.txt': '7ae1043e55597ad32ca5981429735422d04187934e553d9a3ad3a930434f7bce', 'updates/ES/package/adaptive_invention/sources/astra_frontier_dossiers_N58.txt': '5e089a9a9c5aa4157b7c51172058a3fadd9250ea8ddc618f8a5f58f57e0a0391', 'updates/ES/package/adaptive_invention/sources/astra_frontier_dossiers_N733.txt': '37a96ef873e4d7f5a9a37317b815e0b1240039a14a2bc240ab6c97785ce9011b'}

def need(ok,message):
    if not ok:raise ValueError(message)
def sha(d):return hashlib.sha256(d).hexdigest()
def load(p):return json.loads((ROOT/p).read_text())
def rows(p):return [json.loads(l) for l in (ROOT/p).read_text().splitlines() if l.strip()]
def git(*args):return subprocess.check_output(['git','-C',str(ROOT),*args])
def route(c):return c.split('-',1)[0]

def check_sources(m):
    need(m['intake_base_revision']==BASE and m['source_handling']=='source=DATA','source authority changed')
    items=m['campaign_members'];indexed={x['path']:x for x in items}
    need(len(items)==len(indexed)==46 and set(indexed)==set(PINS),'source coverage changed')
    need(sum(x['bytes'] for x in items)==345518,'source size changed')
    for path,x in indexed.items():
        p=Path(path);need(not p.is_absolute() and '..' not in p.parts and not (ROOT/path).is_symlink(),'unsafe source path')
        d=(ROOT/path).read_bytes();need(sha(d)==x['sha256']==PINS[path] and len(d)==x['bytes'],'original bytes/hash changed')
        need(len(d.decode().splitlines())==x['lines'],'source range changed')
        if path.endswith('.py'):ast.parse(d,filename=path)
    actual={p.relative_to(ROOT).as_posix() for p in (ROOT/'updates/ES/package').rglob('*') if p.is_file()}
    need(actual==set(PINS),'extra/missing disclosure')
    need(len(m['excluded_local_files'])==10 and sum(x['original_relative_path'].endswith('.pyc') for x in m['excluded_local_files'])==2,'exclusion coverage changed')
    need(all(x['reason'] and len(x['sha256'])==64 and x['bytes']>0 for x in m['excluded_local_files']),'exclusion reason/receipt missing')
    need(all(not p.endswith(('.pyc','.html')) for p in actual),'third-party paper/cache republished')
    need(m['scientific_scripts_executed']==0,'preservation promoted to replay')
    for x in m['originals']:need(indexed[x['path']]['sha256']==x['sha256'] and 'initiating_prompt_lines' not in x and 'reported_duration' not in x,'invented prompt/duration')
    return indexed

def check_status(s,text):
    r=route(s['card_id'])
    need(r in ROUTES and s['claim_status']=='source_derived_unreviewed','scientific promotion')
    need(s['validation']['external_correctness']==s['validation']['historical_priority']=='UNKNOWN','validation/priority invented')
    need(s['proof_availability']['classification']=='original_campaign_proofs_and_diagnostics_not_independently_audited','internal review promoted')
    need(all(s[k]==[] for k in ['depends_on','supersedes','invalidates','material_updates','contrasting_blockers']),'topical relation promoted')
    required={'N757':['ultraviolet cutoff','log-K-normalized','not a derivation from particles','Fejer','not the iid target','prescribed-field','N/log N','finite-Fisher'],
              'N758':['not a general LP algorithm','arbitrary feasible bounded rational LP','Q1=0','objective to annihilate ker Q','permanent','coefficient magnitudes'],
              'N759':['O(N^3)','O(N^2)','BQP=BPP','width-two','no asymptotic advantage','rejected','2T||delta H||','squared tail']}
    need(all(t.lower() in text.lower() for t in required[r]),'essential scientific boundary erased')

def check_trace(t):
    need(t['mode']==t['context']['conversation_relation']=='UNKNOWN','conversation identity invented')
    need(t['prompt_availability']=='UNKNOWN' and t['prompt_ref_ids']==[],'initiating prompt invented')
    need('one adaptive-invention campaign' in t['context']['retained_context'].lower() and 'must not be counted as independent' in t['context']['retained_context'],'campaign counted as independent runs')
    res=t['resources'];need(res['reported_inference_seconds'] is None and res['reported_duration_ref_ids']==[],'inference duration invented')
    need(all(v is None for v in t['model'].values()) and all(v is None for v in res['usage'].values()) and res['worker_invocations'] is None,'unmeasured telemetry invented')
    need(res['worker_receipt_ref_ids']==res['usage_receipt_ref_ids']==[] and t['matched_run_id'] is None,'unsupported comparison')
    need(t['advance']['verification']=='producer_reported' and t['advance']['verification_receipt'] is None,'internal evidence promoted')

def check_families(f):
    need(f['base_revision']==BASE and f['relation_semantics'].startswith('Navigation comparisons only;'),'family authority changed')
    need([route(x['card_id']) for x in f['decisions']]==ROUTES,'family coverage changed')
    expected=[{'N58','N393','N394'},{'N594','N692'},{'N88','N635','N754'}]
    need([{route(c['card_id']) for c in x['comparisons']} for x in f['decisions']]==expected,'family scope changed')
    known={c['id'] for c in rows('indexes/claims.jsonl')}
    need(all(x['card_id'] in known and all(c['card_id'] in known and c['scope'] for c in x['comparisons']) for x in f['decisions']),'unknown family or unscoped comparison')

def check_gate(g,cid):
    need(g['status']=='open' and g['completion_evidence']==[] and g['card_ids']==[cid],'unresolved gate promoted')

def main():
    m=load('updates/ES/SOURCE_MANIFEST.json');indexed=check_sources(m);mapping=load('updates/ES/CLAIMS.json');check_families(load('updates/ES/FAMILY_FIT.json'))
    need([route(e['id']) for e in mapping['claims']]==ROUTES,'claim coverage changed')
    need(m['reciprocal_continuation_notices']==m['permitted_historical_navigation_changes']==[],'unsupported continuation')
    ledgers={p:rows(p) for p in ['indexes/claims.jsonl','frontier/CURRENT_CLAIM_STATUS.jsonl','indexes/source_metadata.jsonl','web/documents.jsonl']}
    for path,x in indexed.items():
        md=[a for a in ledgers['indexes/source_metadata.jsonl'] if a.get('source_id')==x['source_id']];doc=[a for a in ledgers['web/documents.jsonl'] if a.get('id')==x['source_id']]
        need(len(md)==len(doc)==1 and md[0]['sha256']==x['sha256'] and md[0]['path']==doc[0]['path']==path,'source metadata mismatch')
        need('<pre>'+html.escape((ROOT/path).read_text())+'</pre>' in (ROOT/('web/'+doc[0]['url'])).read_text(),'source mirror changed')
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
            x=indexed[ref['path']];need(ref['sha256']==x['sha256'] and 1<=ref['lines'][0]<=ref['lines'][1]<=x['lines'],'proof range/hash changed')
        for path in ['agent/routes.tsv']+['agent/topics/'+t+'.tsv' for t in s['topics']]:need(cid+'\t' in (ROOT/path).read_text(),'navigation route missing')
        gates=[g for g in rows('frontier/OPEN_PROOF_GATES.jsonl') if g['gate_id']=='G-ES-'+r+'-INDEPENDENT-REVIEW'];need(len(gates)==1,'gate missing');check_gate(gates[0],cid)
        t=load(e['workflow_trace']);validate_trace(t,ROOT);check_trace(t);trace_ids.add(t['id'])
        cp=load(e['checkpoint']);validate_record(cp,ROOT);need(cp['base_revision']==BASE and cp['parent_checkpoint_ids']==[] and cp['branch_id'].startswith('worker-es-'),'source ancestry invented');cp_ids.add(cp['branch_id'])
        generated=views(ROOT,{cp['branch_id']:{cp['checkpoint_id']:cp}});view='state/branches/'+cp['branch_id']+'.txt';need((ROOT/view).read_text()==generated[view],'checkpoint view stale')
        row=next(l for l in generated['state/branches.tsv'].splitlines() if l.startswith(cp['branch_id']+'\t'));need((ROOT/'state/branches.tsv').read_text().splitlines().count(row)==1,'checkpoint registry stale')
    need(proof_count==17 and len(trace_ids)==len(cp_ids)==3,'proof/trace/checkpoint coverage changed')
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
    need(all((ROOT/p).is_file() and sha((ROOT/p).read_bytes())==h for p,h in scientific.items()),'earlier scientific navigation changed')
    print(json.dumps(dict(intake='ES',status='PASS',original_files=len(indexed),original_bytes=345518,excluded_local_files=10,cards=3,proof_ranges=proof_count,checkpoints=3,observational_subaccounts=3,original_campaigns=1,earlier_scientific_views_unchanged=len(scientific),scientific_scripts_executed=0)))
if __name__=='__main__':
    try:main()
    except (ValueError,KeyError,OSError) as e:print(str(e),file=sys.stderr);sys.exit(1)
