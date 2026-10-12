#!/usr/bin/env python3
"""Source, scope and compatibility guards. Never runs archived scientific code."""
import ast
import hashlib
import html
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from evaluation.workflow_trace import validate as validate_trace
from state.publish_checkpoint import validate_record, views

BASE = 'e4a64ea238d3d17744fb134528a78f7712041a5c'
PREFIX = 'updates/EL/package/primitive_genesis/'
HISTORICAL_TOOLING = {'updates/EE/validate.py': 'f3eff780ee11091c984a84e5d8f6122f80c1c1e67d9afad762f20cbc70d262cd', 'updates/EE/test_validate.py': 'd1f1f28820b632fc544c4b609f0ad652ce0a3deedc76e3f9d7751d5e3db3a7a0'}
EXPECTED = {'N735':['C1','C2','C3','C4'], 'N736':['C5','C6','C15'],
            'N737':['C7','C8','C9','C16'], 'N738':[]}
SOURCE_ONLY = ['C10','C11','C12','C13','C14']
COLLECTION_HASHES = {
    'originals':'4947d256a8b56f68e996f695a345bf506d5302eacb28ec6222e8bd220d12a32e',
    'derived_extractions':'f6918d70423723b73049f8c1862aa123c2e27195f6e12fa27316a5b7a6537139'}
SCOPES = {
    'N735':dict(exact_bit_implementation='OPEN',passive_slowdown_removed=False),
    'N736':dict(certificate='sufficient_frozen_on_policy_whole_path',
                 posterior_replicas_from_hidden_state_copies=False,noisy_unknown_simulator_assay='OPEN'),
    'N737':dict(dynamics='constructed_modified',support_potential_acquisition='charged',universal_cubic_root=False),
    'N738':dict(output='full_joint_endpoint_additive_tv',relative_rare_failure_accuracy=False,
                 fault_history=False,summary_replaces_jump_law=False,
                 finite_bit_status='proof candidate',implementation='not supplied')}
PERMITTED = {f'frontier/{folder}/{route}.{ext}' for folder,ext in
             [('dossiers','txt'),('connections','json')] for route in ['N713','N718']}


def need(condition, message):
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
    need(len(manifest['originals'])==60 and sum(x['bytes'] for x in manifest['originals'])==872416,
         'original source extent changed')
    all_sources = {}
    scripts = 0
    for group in ['originals','derived_extractions']:
        collection = [{f:x[f] for f in ['original_relative_path','path','sha256','bytes']}
                      for x in manifest[group]]
        need(sha(json.dumps(collection,sort_keys=True,separators=(',',':')).encode())==COLLECTION_HASHES[group],
             'frozen source collection identity changed')
        for item in manifest[group]:
            p=Path(item['path'])
            need(not p.is_absolute() and '..' not in p.parts and p.parts[:3]==('updates','EL','package'),
                 'unsafe source path')
            need(item['path'] not in all_sources and not (ROOT/p).is_symlink(), 'duplicate/symlink source')
            data=(ROOT/p).read_bytes()
            need(sha(data)==item['sha256'] and len(data)==item['bytes'], 'source bytes changed')
            if item['lines'] is not None:
                need(len(data.decode().splitlines())==item['lines'], 'source line extent changed')
            if p.suffix=='.py':
                ast.parse(data,filename=str(p));scripts+=1
            all_sources[item['path']]=item
    need(scripts==8, 'scientific script coverage changed')
    actual={p.relative_to(ROOT).as_posix() for p in (ROOT/'updates/EL/package').rglob('*') if p.is_file()}
    need(actual==set(all_sources), 'extra or missing disclosure')
    checked=0
    for receipt in manifest['producer_manifests']:
        producer=load(receipt['path'])
        need(sha((ROOT/receipt['path']).read_bytes())==receipt['sha256'] and
             len(producer['files'])==receipt['member_hashes_checked'], 'producer manifest changed')
        for name,r in producer['files'].items():
            item=all_sources[str(Path(receipt['path']).parent/name)]
            need(item['sha256']==r['sha256'] and item['bytes']==r['bytes'], 'producer member mismatch')
            checked+=1
    need(checked==manifest['producer_member_hashes_checked']==11, 'producer coverage changed')
    extension=load(PREFIX+'astra_capital/EXTENSION_MANIFEST.json')
    need(extension['frozen_main_manifest_sha256']==sha((ROOT/(PREFIX+'astra_capital/MANIFEST.json')).read_bytes()),
         'frozen main manifest changed')
    derived=next(x for x in manifest['derived_extractions'] if x['original_relative_path']=='@text')
    pdf=next(x for x in manifest['originals'] if x['original_relative_path']=='@pdf')
    need(pdf['pages']==6 and derived['original_sha256']==pdf['sha256'] and
         len(derived['page_map'])==6, 'PDF lineage/page count changed')
    prose=(ROOT/derived['path']).read_text().splitlines()
    for i,page in enumerate(derived['page_map'],1):
        a,b=page['lines'];need(page['pdf_page']==i and 1<=a<=b<=len(prose) and
                            prose[a-2]==f'=== ORIGINAL PDF PAGE {i} ===', 'PDF page range changed')
    equations=next(x for x in manifest['derived_extractions'] if x['original_relative_path']=='@equations')
    need(equations['original_sha256']==pdf['sha256'] and
         'NOT ORIGINAL AUTHOR BYTES' in (ROOT/equations['path']).read_text(), 'visual transcription relabeled')
    return all_sources


def check_status(status):
    route=status['card_id'].split('-',1)[0]
    need(status['claim_status']=='source_derived_unreviewed' and
         status['validation']['external_correctness']=='UNKNOWN', 'scientific promotion')
    need(status['depends_on']==status['supersedes']==status['invalidates']==status['contrasting_blockers']==[],
         'unsupported theorem dependency or invalidation')
    need(status['validation']['operational_scope']==SCOPES[route], 'operational scope strengthened')
    expected_prefixes={'N713','N718'} if route=='N736' else set()
    need({x['target'].split('-',1)[0] for x in status['material_updates']}==expected_prefixes,
         'scoped continuation coverage changed')


def check_trace(trace, campaign, manifest):
    need(trace['prompt_availability']=='UNKNOWN' and trace['prompt_ref_ids']==[] and
         trace['context']['conversation_relation']=='UNKNOWN' and trace['context']['retained_context'] is None,
         'prompt or context invented')
    need(trace['mode']==('source_intensive_multi_agent' if campaign else 'UNKNOWN') and
         trace['status']=='completed', 'workflow mode/mission conflated')
    r=trace['resources']
    need(all(v is None for v in trace['model'].values()) and r['worker_invocations'] is None and
         r['reported_inference_seconds'] is None and r['reported_duration_ref_ids']==[] and
         all(v is None for v in r['usage'].values()) and r['usage_receipt_ref_ids']==[],
         'unique workers or wall interval promoted to usage/inference telemetry')
    need(r['worker_receipt_ref_ids']==(['state'] if campaign else []) and
         trace['matched_run_id'] is None and trace['advance']['verification']=='producer_reported' and
         trace['advance']['verification_receipt'] is None, 'campaign attribution or independent verification invented')
    if campaign:
        team=manifest['reported_team'];state=load(PREFIX+'RESEARCH_STATE.json')
        need(team['unique_workers']==state['usage']['distinct_workers']==12 and
             team['sol_6_1_max_workers']==team['luna_max_workers']==6 and
             len(state['worker_contributions'])==12, 'reported unique worker configurations lost')
        need(manifest['observed_clock']['wall_interval_seconds']==state['observed_wall_interval_seconds']==3968,
             'observed clock provenance changed')
    else:
        need(manifest['pdf_not_attributed_to_campaign'] is True and
             [x['path'] for x in trace['refs']]==[next(x['path'] for x in manifest['originals']
               if x['original_relative_path']=='@pdf')], 'unrelated PDF attributed to campaign')



def check_continuation_projection(earlier, newer_id, notice):
    """Only the exact notice, its relation and snapshot metadata may be added."""
    path = 'frontier/dossiers/'+earlier+'.txt'
    old = git('show',BASE+':'+path).decode().splitlines()
    now = (ROOT/path).read_text().splitlines()
    pos = now.index('SEMANTIC NOTICE '+notice['notice_id'])
    need(now[pos-1]=='' and now[pos+1]==notice['status']+': '+notice['clarification'],
         'continuation notice projection changed')
    del now[pos-1:pos+2]
    old[1] = now[1] = '<snapshot metadata>'
    need(now==old, 'earlier dossier mathematics changed: '+earlier)
    path = 'frontier/connections/'+earlier+'.json'
    old,now = json.loads(git('show',BASE+':'+path)),load(path)
    need(set(now)==set(old) and all(now[k]==old[k] for k in old if k not in ['nodes','edges','snapshot']),
         'earlier connection scientific fields changed')
    extra_nodes = [n for n in now['nodes'] if n not in old['nodes']]
    extra_edges = [e for e in now['edges'] if e not in old['edges']]
    need(all(n in now['nodes'] for n in old['nodes']) and len(now['nodes'])==len(old['nodes'])+1 and
         extra_nodes==[dict(id=newer_id,node_kind='claim')], 'earlier connection nodes changed')
    target = next(c for c in notice['card_ids'] if c.startswith(earlier+'-'))
    need(all(e in now['edges'] for e in old['edges']) and len(now['edges'])==len(old['edges'])+1 and
         extra_edges==[dict(composition=notice['clarification'],kind='material_update',
                           raw_kind='source_reported_scoped_interface_extension',source='EL intake',
                           **{'from':newer_id,'to':target})], 'earlier connection edges changed')

def main():
    m=load('updates/EL/SOURCE_MANIFEST.json');mapping=load('updates/EL/CLAIMS.json')
    need(m['intake_base_revision']==mapping['base_revision']==BASE and m['source_handling']=='source=DATA' and
         m['campaign_status']=='NORTH_STAR_NOT_ESTABLISHED', 'base/source/mission scope changed')
    need(m['historical_tooling_refactor']['files']==HISTORICAL_TOOLING, 'historical tooling receipt changed')
    source_by_path=check_sources(m);ledger=load(PREFIX+'CLAIM_LEDGER.json')
    need(len(ledger['claims'])==16 and [x['id'] for x in mapping['retained_source_only_claims']]==SOURCE_ONLY,
         'source-only claim coverage changed')
    need(next(x['status'] for x in mapping['retained_source_only_claims'] if x['id']=='C14')=='NOT_ESTABLISHED',
         'mission promoted')
    need(len(mapping['claims'])==4, 'mechanism count changed')
    ledgers={p:rows(p) for p in ['indexes/claims.jsonl','frontier/CURRENT_CLAIM_STATUS.jsonl',
                               'indexes/source_metadata.jsonl','web/documents.jsonl']}
    for item in source_by_path.values():
        meta=[x for x in ledgers['indexes/source_metadata.jsonl'] if x.get('source_id')==item['source_id']]
        docs=[x for x in ledgers['web/documents.jsonl'] if x['id']==item['source_id']]
        need(len(meta)==len(docs)==1 and meta[0]['sha256']==item['sha256'] and
             meta[0]['path']==docs[0]['path']==item['path'], 'source index mismatch')
        web=(ROOT/('web/'+docs[0]['url'])).read_text()
        if item['lines'] is not None:
            need('<pre>'+html.escape((ROOT/item['path']).read_text())+'</pre>' in web, 'source mirror changed')
        else:
            need(item['path'] in web, 'PDF mirror locator missing')
    trace_paths=set();checkpoint_paths=set();covered=[];proof_count=0
    for entry in mapping['claims']:
        cid=entry['id'];route=cid.split('-',1)[0]
        need(entry['source_ledger_claim_ids']==EXPECTED[route], 'claim scope mapping changed')
        covered+=entry['source_ledger_claim_ids'];trace_paths.add(entry['workflow_trace']);checkpoint_paths.add(entry['checkpoint'])
        status=load('frontier/cards/'+cid+'.json');check_status(status)
        current=[x for x in ledgers['frontier/CURRENT_CLAIM_STATUS.jsonl'] if x['card_id']==cid]
        claims=[x for x in ledgers['indexes/claims.jsonl'] if x['id']==cid]
        catalogs=[x for x in load('indexes/agent_catalog.json')['claims'] if x['id']==cid]
        need(current==[status] and len(claims)==len(catalogs)==1 and
             entry['status']==claims[0]['status']==status['claim_status'], 'claim/status coverage mismatch')
        card=(ROOT/status['card_path']).read_bytes()
        need(sha(card)==status['card_sha256']==catalogs[0]['card_sha256'] and
             (ROOT/('frontier/review_cards/'+cid+'.txt')).read_bytes().endswith(card), 'card identity mismatch')
        primary=source_by_path[entry['source_path']]
        need(primary['source_id']==entry['source_id'] and primary['sha256']==entry['source_sha256'], 'primary pointer mismatch')
        proofs=status['proof_availability']['located_proof_sources'];proof_count+=len(proofs)
        for ref in proofs+status['proof_availability']['available_evidence_sources']:
            item=source_by_path[ref['path']];a,b=ref['lines']
            need(ref['sha256']==item['sha256'] and 1<=a<=b<=item['lines'], 'proof range/hash invalid')
        need(cid+'\t' in (ROOT/'agent/routes.tsv').read_text(), 'legacy route missing')
        for topic in status['topics']:
            need(cid+'\t' in (ROOT/('agent/topics/'+topic+'.tsv')).read_text(), 'topic route missing')
        need(any(cid in g['card_ids'] and g['status']=='open' for g in rows('frontier/OPEN_PROOF_GATES.jsonl')),
             'decisive gate missing')
    need(sorted(covered+SOURCE_ONLY)==sorted(x['id'] for x in ledger['claims']) and proof_count==20,
         'sixteen source claims or decisive ranges lost')
    need(len(trace_paths)==len(checkpoint_paths)==2 and
         len({x['workflow_trace'] for x in mapping['claims'][:3]})==1 and
         mapping['claims'][3]['workflow_trace'] not in {x['workflow_trace'] for x in mapping['claims'][:3]},
         'campaign resources duplicated or PDF mixed with campaign')
    for path in trace_paths:
        trace=load(path);validate_trace(trace,ROOT);check_trace(trace,'primitive-genesis' in path,m)
    for path in checkpoint_paths:
        cp=load(path);validate_record(cp,ROOT)
        need(cp['base_revision']==BASE and cp['parent_checkpoint_ids']==[], 'original checkpoint ancestry invented')
        v=views(ROOT,{cp['branch_id']:{cp['checkpoint_id']:cp}});view='state/branches/'+cp['branch_id']+'.txt'
        need((ROOT/view).read_text()==v[view], 'checkpoint view stale')
        row=next(l for l in v['state/branches.tsv'].splitlines() if l.startswith(cp['branch_id']+'\t'))
        need((ROOT/'state/branches.tsv').read_text().splitlines().count(row)==1, 'checkpoint row mismatch')
    for p in list(ledgers)+['agent/SEMANTIC_NOTICES.jsonl','frontier/OPEN_PROOF_GATES.jsonl','state/branches.tsv','agent/routes.tsv']:
        need((ROOT/p).read_bytes().startswith(git('show',BASE+':'+p)), 'historical ledger rewritten')
    for p,fields in [('indexes/agent_catalog.json',['claims']),('indexes/agent_graph.json',['nodes','edges'])]:
        old,now=json.loads(git('show',BASE+':'+p)),load(p)
        for field in fields:
            need(now[field][:len(old[field])]==old[field], 'historical graph/catalog rewritten')
    graph=load('indexes/agent_graph.json');node_ids={x['id'] for x in graph['nodes']}
    need(len(node_ids)==len(graph['nodes']) and all(e['from'] in node_ids and e['to'] in node_ids for e in graph['edges']),
         'graph integrity')
    for entry in mapping['claims']:
        c=next(x for x in ledgers['indexes/claims.jsonl'] if x['id']==entry['id'])
        need(set(c['source_ids'])=={e['to'] for e in graph['edges'] if e['from']==entry['id'] and e['kind']=='provenance'},
             'provenance coverage')
    notices=rows('agent/SEMANTIC_NOTICES.jsonl')
    need(len(m['reciprocal_continuation_notices'])==2, 'reciprocal notice coverage')
    for nid in m['reciprocal_continuation_notices']:
        matches=[x for x in notices if x['notice_id']==nid];need(len(matches)==1, 'reciprocal notice missing/duplicate')
        need(len(matches[0]['card_ids'])==2 and len(matches[0]['material_updates'])==2, 'reciprocal scope missing')
        earlier=next(c.split('-',1)[0] for c in matches[0]['card_ids'] if not c.startswith('N736-'))
        newer_id=next(c for c in matches[0]['card_ids'] if c.startswith('N736-'))
        check_continuation_projection(earlier,newer_id,matches[0])
    old_aliases=json.loads(git('show',BASE+':indexes/query_aliases.json'));now_aliases=load('indexes/query_aliases.json')
    need(all(now_aliases.get(k)==v for k,v in old_aliases.items()), 'old aliases changed')
    old_paths=set(git('ls-tree','-r','--name-only',BASE).decode().splitlines())
    changed=set(git('diff','--name-only',BASE,'--','updates','cards','frontier/cards','state/checkpoints','state/branches',
                    'evaluation','technology/records').decode().splitlines())
    need(changed & old_paths == set(HISTORICAL_TOOLING), 'old original/status/checkpoint/evaluation changed')
    need(all(sha((ROOT/p).read_bytes())==digest for p,digest in HISTORICAL_TOOLING.items()),
         'historical test-guard refactor changed outside pinned scope')
    outputs=json.loads(git('show',BASE+':agent/access_manifest.json'))['outputs']
    scientific={p:d for p,d in outputs.items() if p.startswith(('frontier/dossiers/','frontier/connections/','frontier/proof_ranges/'))}
    differences={p for p,d in scientific.items() if sha((ROOT/p).read_bytes())!=d}
    need(set(m['permitted_historical_navigation_changes'])==PERMITTED and differences==PERMITTED,
         'earlier scientific navigation changed outside exact notices')
    print(json.dumps(dict(intake='EL',status='PASS',original_files=60,original_bytes=872416,
        campaign_original_files=59,original_pdfs=1,derived_objects=3,producer_member_hashes_checked=11,
        source_ledger_claims=16,mechanism_cards=4,proof_ranges=20,observational_traces=2,
        record_level_checkpoints=2,reported_unique_workers=12,all_worker_invocations='UNKNOWN',
        reported_inference_seconds='UNKNOWN',scientific_scripts_ast_only=8,scientific_scripts_executed=0,
        unchanged_earlier_scientific_routes=len(scientific)-len(differences),scoped_notice_views=sorted(differences),
        independent_scientific_verification='not performed'),sort_keys=True))


if __name__=='__main__':
    try:
        main()
    except (ValueError,OSError,KeyError,subprocess.CalledProcessError) as error:
        raise SystemExit(str(error))
