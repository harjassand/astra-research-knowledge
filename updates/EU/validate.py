#!/usr/bin/env python3
"""Preservation and evidence-boundary checks; archived scientific code stays data."""
import ast,hashlib,html,json,stat,subprocess,sys
from pathlib import Path,PurePosixPath
from zipfile import ZipFile
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from evaluation.workflow_trace import validate as validate_trace
from state.publish_checkpoint import validate_record,views
BASE='da0a23e56c83271667b701a400595270bcbac785'
PINS={'updates/EU/package/sign_divisor/ORIGINAL_PASTED_SOURCE.txt': '1b6c2e0fd6b0ee2b0f817d5cbc6e875f2fe0f236d355538a416f1ca946709346', 'updates/EU/package/sign_divisor/astra_sign_divisor_research.zip': '236db173eda49cbf43a8c5075534f3add92ffce8291072961624fbb699b213b3', 'updates/EU/package/sign_divisor/recovered/astra_sign_divisor/MANIFEST.json': '97091c5b2a00e107f3a92fb2ec79eff8a065777aa10889b10601a6e345a5969d', 'updates/EU/package/sign_divisor/recovered/astra_sign_divisor/README.md': '3151e52598b8de19706b1cfc1b885b9a78d045e311a071caa63fd82836e42280', 'updates/EU/package/sign_divisor/recovered/astra_sign_divisor/RESEARCH_NOTE.md': '007100eb706f79aaf0f2db8bacce22ae69ed11ee38c8a114218115055e445781', 'updates/EU/package/sign_divisor/recovered/astra_sign_divisor/checks.json': '16cebcef6751dc831a01b96e1e149d6fd3f610d036a0a343afdca10e56deb8a6', 'updates/EU/package/sign_divisor/recovered/astra_sign_divisor/verify.py': '4c1ee90ba20227fc57331f5e9854562b00d97da6863118d12793af4694fff48a'}

def need(ok,message):
    if not ok:raise ValueError(message)
def sha(d):return hashlib.sha256(d).hexdigest()
def load(p):return json.loads((ROOT/p).read_text())
def rows(p):return [json.loads(l) for l in (ROOT/p).read_text().splitlines() if l.strip()]
def git(*args):return subprocess.check_output(['git','-C',str(ROOT),*args])
def route(c):return c.split('-',1)[0]

def check_sources(m):
    need(m['intake_base_revision']==BASE and m['source_handling']=='source=DATA','source authority changed')
    need(len(m['originals'])==len(m['recovered_packages'])==1,'source coverage changed')
    pkg=m['recovered_packages'][0];items=m['originals']+[pkg]+pkg['members'];indexed={x['path']:x for x in items}
    need(len(items)==len(indexed)==7 and set(indexed)==set(PINS),'source coverage changed')
    need(sum(x['bytes'] for x in items)==85754 and m['originals'][0]['lines']==216,'source extent changed')
    need(m['scientific_scripts_executed']==0 and pkg['verification']['scientific_code_execution']==pkg['verification']['independent_proof_review']=='not performed','integrity promoted to scientific replay')
    for path,x in indexed.items():
        p=PurePosixPath(path);need(not p.is_absolute() and '..' not in p.parts and not (ROOT/path).is_symlink(),'unsafe original path')
        d=(ROOT/path).read_bytes();need(sha(d)==x['sha256']==PINS[path] and len(d)==x['bytes'],'original bytes/hash changed')
        if 'lines' in x:need(len(d.decode().splitlines())==x['lines'],'source line extent changed')
        if path.endswith('.py'):ast.parse(d,filename=path)
    actual={p.relative_to(ROOT).as_posix() for p in (ROOT/'updates/EU/package').rglob('*') if p.is_file()};need(actual==set(PINS),'extra/missing public disclosure')
    with ZipFile(ROOT/pkg['archive_path']) as z:
        need(z.testzip() is None,'ZIP CRC failure');names=z.namelist();need(len(names)==len(set(names))==5 and set(names)=={x['archive_member'] for x in pkg['members']},'ZIP member coverage changed')
        for info in z.infolist():
            p=PurePosixPath(info.filename);need(not p.is_absolute() and '..' not in p.parts and chr(92) not in info.filename and not stat.S_ISLNK(info.external_attr>>16) and not info.is_dir(),'unsafe ZIP member')
            x=next(x for x in pkg['members'] if x['archive_member']==info.filename);need(z.read(info)==(ROOT/x['path']).read_bytes(),'extracted member changed')
        producer=json.loads(z.read('astra_sign_divisor/MANIFEST.json'))['files'];need(len(producer)==pkg['producer_hashes_checked']==4 and set(producer)=={n.removeprefix('astra_sign_divisor/') for n in names if not n.endswith('/MANIFEST.json')},'producer manifest coverage changed')
        for n,h in producer.items():need(sha(z.read('astra_sign_divisor/'+n))==h,'producer digest mismatch')
    return indexed

def check_status(s,text):
    need(route(s['card_id'])=='N761' and s['claim_status']=='source_derived_unreviewed','scientific promotion')
    need(s['validation']['external_correctness']==s['validation']['historical_priority']=='UNKNOWN','correctness/priority invented')
    need(s['proof_availability']['classification']=='original_proof_accounts_and_recovered_producer_artifacts_not_independently_audited','availability promoted to proof audit')
    need([x['target'] for x in s['depends_on']]==['external:EU_KANE_GAUSSIAN_THRESHOLD_NOISE','external:EU_GAUSSIAN_HYPERCONTRACTIVITY'],'imported premise coverage changed')
    need(all(s[k]==[] for k in ['supersedes','invalidates','material_updates','contrasting_blockers']),'topical comparison promoted')
    required=['strictly positive almost everywhere','sign-changing','affine hull, not full support','coordinatewise','not original latent dimension','Omega(n) exact versus Omega(sqrt(n))','Polynomial degree is not runtime','O(nk)','real factorization','sign-changing classification','optimum-basis','arbitrary leakage','Singular Gaussians','historical novelty UNKNOWN','sufficient separable','pair data and full-law','Floating examples are not certified PSD','supplies no corresponding statement/proof','No exceptional foundational']
    need(all(x.lower() in text.lower() for x in required),'essential scientific boundary erased')

def check_trace(t):
    need(t['mode']=='independent_selective_capital' and t['context']['conversation_relation']=='UNKNOWN','unobserved workflow/context invented')
    need(t['prompt_availability']=='exact' and t['prompt_ref_ids']==['prompt'],'prompt provenance changed')
    res=t['resources'];need(res['reported_inference_seconds']==2597 and res['reported_duration_ref_ids']==['duration'],'reported duration changed')
    need(all(v is None for v in t['model'].values()) and all(v is None for v in res['usage'].values()) and res['worker_invocations'] is None,'unmeasured model/usage invented')
    need(res['worker_receipt_ref_ids']==res['usage_receipt_ref_ids']==[] and t['matched_run_id'] is None,'unsupported comparison')
    need(t['advance']['verification']=='producer_reported' and t['advance']['verification_receipt'] is None,'producer diagnostics promoted')
    refs={x['id']:x for x in t['refs']};need(refs['prompt']['lines']==[1,23] and refs['duration']['lines']==[24,24] and refs['result']['lines']==[35,216],'prompt/duration/result range changed')

def check_families(f):
    need(f['base_revision']==BASE and f['relation_semantics'].startswith('Navigation comparisons only;'),'family authority changed')
    need(len(f['decisions'])==1 and route(f['decisions'][0]['card_id'])=='N761','family coverage changed')
    comparisons=f['decisions'][0]['comparisons'];need([route(x['card_id']) for x in comparisons]==['N26','N629','N630','N631','N632'] and all(x['scope'] for x in comparisons),'family comparison missing/unscoped')
    known={x['id'] for x in rows('indexes/claims.jsonl')};need(all(x['card_id'] in known for x in comparisons),'family target unknown')

def check_gate(g,cid):need(g['status']=='open' and g['completion_evidence']==[] and g['card_ids']==[cid],'unresolved gate promoted')

def main():
    m=load('updates/EU/SOURCE_MANIFEST.json');indexed=check_sources(m);mapping=load('updates/EU/CLAIMS.json');check_families(load('updates/EU/FAMILY_FIT.json'))
    need(len(mapping['claims'])==1,'extra claim invented');e=mapping['claims'][0];cid=e['id'];s=load('frontier/cards/'+cid+'.json');card=(ROOT/s['card_path']).read_bytes();check_status(s,card.decode())
    need(m['reciprocal_continuation_notices']==m['permitted_historical_navigation_changes']==[],'unsupported historical continuation')
    ledgers={p:rows(p) for p in ['indexes/claims.jsonl','frontier/CURRENT_CLAIM_STATUS.jsonl','indexes/source_metadata.jsonl','web/documents.jsonl']}
    for path,x in indexed.items():
        md=[a for a in ledgers['indexes/source_metadata.jsonl'] if a.get('source_id')==x['source_id']];docs=[a for a in ledgers['web/documents.jsonl'] if a['id']==x['source_id']]
        need(len(md)==len(docs)==1 and md[0]['sha256']==x['sha256'] and md[0]['path']==docs[0]['path']==path,'source metadata mismatch')
        if 'lines' in x:need('<pre>'+html.escape((ROOT/path).read_text())+'</pre>' in (ROOT/('web/'+docs[0]['url'])).read_text(),'source mirror changed')
        else:need(docs[0]['url']=='../'+path,'original binary route missing')
    catalog=load('indexes/agent_catalog.json')['claims'];web=load('web/catalog.json')
    for pool,k in [(ledgers['frontier/CURRENT_CLAIM_STATUS.jsonl'],'card_id'),(ledgers['indexes/claims.jsonl'],'id'),(catalog,'id'),(web,'id')]:need(sum(x[k]==cid for x in pool)==1,'duplicate/missing claim')
    need(next(x for x in ledgers['frontier/CURRENT_CLAIM_STATUS.jsonl'] if x['card_id']==cid)==s,'status ledger mismatch')
    claim=next(x for x in ledgers['indexes/claims.jsonl'] if x['id']==cid);wc=next(x for x in web if x['id']==cid)
    need(claim['status']==e['status']==s['claim_status'] and claim['depends_on']==[x['target'] for x in s['depends_on']] and claim['scoped_dependencies']==[],'status/dependency mismatch')
    need(wc['source_paths']==claim['source_paths'] and wc['source_ids']==claim['source_ids'],'web provenance missing')
    need(e['source_sha256']==indexed[e['source_path']]['sha256'] and e['missing_artifacts']==[] and e['unresolved_obligations'],'source/unresolved gate mismatch')
    need(sha(card)==s['card_sha256']==next(x for x in catalog if x['id']==cid)['card_sha256'] and (ROOT/('frontier/review_cards/'+cid+'.txt')).read_bytes().endswith(card),'card hash/wrapper mismatch')
    proofs=s['proof_availability']['located_proof_sources'];need(len(proofs)==12,'proof range coverage changed')
    for ref in proofs+s['proof_availability']['available_evidence_sources']:
        x=indexed[ref['path']];need(ref['sha256']==x['sha256'],'proof hash changed')
        if 'lines' in ref:need(1<=ref['lines'][0]<=ref['lines'][1]<=x['lines'],'proof range invalid')
    for path in ['agent/routes.tsv']+['agent/topics/'+t+'.tsv' for t in s['topics']]:need(cid+'\t' in (ROOT/path).read_text(),'navigation route missing')
    gates=[g for g in rows('frontier/OPEN_PROOF_GATES.jsonl') if g['gate_id']=='G-EU-N761-INDEPENDENT-REVIEW'];need(len(gates)==1,'gate missing');check_gate(gates[0],cid)
    t=load(e['workflow_trace']);validate_trace(t,ROOT);check_trace(t)
    cp=load(e['checkpoint']);validate_record(cp,ROOT);need(cp['base_revision']==BASE and cp['parent_checkpoint_ids']==[] and cp['branch_id']=='worker-eu-sign-divisor','source ancestry invented')
    generated=views(ROOT,{cp['branch_id']:{cp['checkpoint_id']:cp}});view='state/branches/'+cp['branch_id']+'.txt';need((ROOT/view).read_text()==generated[view],'checkpoint view stale')
    row=next(l for l in generated['state/branches.tsv'].splitlines() if l.startswith(cp['branch_id']+'\t'));need((ROOT/'state/branches.tsv').read_text().splitlines().count(row)==1,'checkpoint registry stale')
    for path in list(ledgers)+['frontier/OPEN_PROOF_GATES.jsonl','state/branches.tsv','agent/routes.tsv','agent/SEMANTIC_NOTICES.jsonl']:
        need((ROOT/path).read_bytes().startswith(git('show',BASE+':'+path)),'historical ledger rewritten')
    for path,fields in [('indexes/agent_catalog.json',['claims']),('indexes/agent_graph.json',['nodes','edges'])]:
        old=json.loads(git('show',BASE+':'+path));now=load(path)
        for f in fields:need(now[f][:len(old[f])]==old[f],'historical graph/catalog rewritten')
    graph=load('indexes/agent_graph.json');nodes={x['id'] for x in graph['nodes']};need(len(nodes)==len(graph['nodes']) and all(x['from'] in nodes and x['to'] in nodes for x in graph['edges']),'graph integrity')
    need(set(claim['source_ids'])=={x['to'] for x in graph['edges'] if x['from']==cid and x['kind']=='provenance'},'claim provenance mismatch')
    old_alias=json.loads(git('show',BASE+':indexes/query_aliases.json'));need(all(load('indexes/query_aliases.json').get(k)==v for k,v in old_alias.items()),'earlier alias changed')
    old_paths=set(git('ls-tree','-r','--name-only',BASE).decode().splitlines());changed=set(git('diff','--name-only',BASE,'--','updates','cards','frontier/cards','frontier/review_cards','state/checkpoints','state/branches','evaluation','technology/records','web/pages').decode().splitlines());need(not changed & old_paths,'earlier scientific/source/checkpoint/evaluation object changed')
    outputs=json.loads(git('show',BASE+':agent/access_manifest.json'))['outputs'];scientific={p:h for p,h in outputs.items() if p.startswith(('frontier/dossiers/','frontier/connections/','frontier/proof_ranges/'))};need(all((ROOT/p).is_file() and sha((ROOT/p).read_bytes())==h for p,h in scientific.items()),'earlier scientific navigation changed')
    print(json.dumps(dict(intake='EU',status='PASS',original_files=7,original_bytes=85754,archive_members=5,producer_hashes_checked=4,cards=1,proof_ranges=12,checkpoints=1,earlier_scientific_views_unchanged=len(scientific),scientific_scripts_executed=0)))
if __name__=='__main__':
    try:main()
    except (ValueError,KeyError,OSError) as e:print(str(e),file=sys.stderr);sys.exit(1)
