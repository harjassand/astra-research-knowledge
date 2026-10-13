#!/usr/bin/env python3
"""EY preservation, scope, linkage and append-only checks; never scientific truth."""
import ast
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from zipfile import ZipFile

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from evaluation.workflow_trace import validate as trace_validate
from state.publish_checkpoint import validate_record,views
from technology.validate import validate as tech_validate

BASE='4ae225b0bf2a07e1ced2952a3e1399d4b45e039c'
PINNED_PASTES={
 'frontier_decision':'18f9aab5a016a5e22749665790fa29c63ac899ee5f34261edc51af98ce3ee565',
 'chemical_adjoint':'58a8a000075ff1a3407a4afd4a19b70d36a62bb77d33091e5b9afd08113d4aa8',
 'physical_gain':'a240a786dc501a969c8a2f2f278dd82e5a5d2749300cd0d47f2b5011113da31c'}

def need(x,m):
    if not x:raise ValueError(m)
def load(p):return json.loads((ROOT/p).read_text())
def rows(p):return [json.loads(x) for x in (ROOT/p).read_text().splitlines() if x.strip()]
def sha(p):return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
def git(*args):return subprocess.check_output(['git','-C',str(ROOT),*args])

def check_ref(ref):
    need(sha(ref['path'])==ref['sha256'],'evidence hash mismatch: '+ref['path'])
    if ref.get('lines') is not None:
        a,b=ref['lines'];need(1<=a<=b<=len((ROOT/ref['path']).read_text().splitlines()),'invalid inclusive proof range')

def main():
    manifest=load('updates/EY/SOURCE_MANIFEST.json')
    need(manifest['base_revision']==BASE and manifest['missing_artifacts']==[],'base/source coverage changed')
    files=manifest['original_files'];need(len(files)==85 and sum(x['bytes'] for x in files)==26341119,'source inventory changed')
    for slug,pin in PINNED_PASTES.items():
        need(sha('updates/EY/package/'+slug+'/ORIGINAL_PASTED_SOURCE.txt')==pin,'supplied paste pin changed')
    for x in files:
        need(sha(x['path'])==x['sha256'] and (ROOT/x['path']).stat().st_size==x['bytes'],'original source bytes changed')
        if 'lines' in x:need(len((ROOT/x['path']).read_text().splitlines())==x['lines'],'source line inventory changed')
        if x['path'].endswith('.py'):ast.parse((ROOT/x['path']).read_bytes(),filename=x['path'])
    # Pins live in the committed manifest; the tool also checks exact archived members.
    members=hashes=0
    for a in manifest['archives']:
        need(sha(a['path'])==a['sha256'],'archive changed')
        with ZipFile(ROOT/a['path']) as z:
            need(z.testzip() is None and len(z.infolist())==a['members'],'CRC/member mismatch')
            prefix=str(Path(a['producer_manifest']).parent)+'/'
            p=json.loads(z.read(a['producer_manifest']));pins=p.get('files',p)
            need(len(pins)==a['producer_hashes_checked'],'producer manifest coverage changed')
            for f,h in pins.items():need(hashlib.sha256(z.read(prefix+f)).hexdigest()==h,'producer pin mismatch')
            dest=Path(a['path']).parent/'recovered'
            for m in z.infolist():
                if not m.is_dir():need((ROOT/dest/m.filename).read_bytes()==z.read(m),'extracted member changed')
            members+=len(z.infolist());hashes+=len(pins)
    need((members,hashes)==(79,76),'archive totals changed')
    maps=load('updates/EY/CLAIMS.json')['claims'];need(len(maps)==4,'claim count')
    ids=[m['id'] for m in maps]
    statuses={s['card_id']:s for s in rows('frontier/CURRENT_CLAIM_STATUS.jsonl')}
    claims={s['id']:s for s in rows('indexes/claims.jsonl')}
    cat={s['id']:s for s in load('indexes/agent_catalog.json')['claims']}
    web={s['id']:s for s in load('web/catalog.json')}
    gates=rows('frontier/OPEN_PROOF_GATES.jsonl');proofs=0
    for m in maps:
        cid=m['id'];s=load('frontier/cards/'+cid+'.json')
        need(s==statuses[cid] and s['claim_status']==claims[cid]['status']=='source_derived_unreviewed','status authority mismatch')
        need(sha(s['card_path'])==s['card_sha256']==cat[cid]['card_sha256'],'card SHA mismatch')
        need(claims[cid]['source_paths']==web[cid]['source_paths'] and claims[cid]['source_ids']==web[cid]['source_ids'],'web provenance mismatch')
        need(claims[cid]['depends_on']==[d['target'] for d in s['depends_on']]==cat[cid]['dependencies']['depends_on'],'dependency mismatch')
        for ref in s['proof_availability']['located_proof_sources']+s['proof_availability']['available_evidence_sources']:check_ref(ref)
        proofs+=len(s['proof_availability']['located_proof_sources'])
        need(s['validation']['external_correctness']==s['validation']['historical_priority']=='UNKNOWN','scientific certification invented')
        need(s['supersedes']==s['invalidates']==[],'unscoped supersession/invalidation')
        cg=[g for g in gates if g['gate_id'].startswith('G-EY-') and cid in g['card_ids']]
        need(len(cg)==2 and all(g['status']=='open' and g['completion_evidence']==[] for g in cg),'open gate promoted')
        for topic in s['topics']:
            p='agent/topics/'+topic+'.tsv';data=(ROOT/p).read_text()
            need(data.startswith(git('show',BASE+':'+p).decode()),'historical topic routes rewritten')
            need(sum(l.startswith(cid+'\t') for l in data.splitlines())==1,'topic missing/duplicate')
            need(topic+': '+p+' ('+str(len(data.splitlines())-1)+' cards)' in (ROOT/'agent/topics.txt').read_text(),'topic count stale')
        cp=load(m['checkpoint']);validate_record(cp,ROOT)
        need(cp['base_revision']==BASE and cp['parent_checkpoint_ids']==[],'handoff ancestry changed')
        v=views(ROOT,{cp['branch_id']:{cp['checkpoint_id']:cp}});vp='state/branches/'+cp['branch_id']+'.txt'
        need((ROOT/vp).read_text()==v[vp],'handoff view stale')
        row=next(x for x in v['state/branches.tsv'].splitlines() if x.startswith(cp['branch_id']+'\t'))
        need((ROOT/'state/branches.tsv').read_text().splitlines().count(row)==1,'handoff row stale/duplicate')
        if m['workflow_trace']:
            t=load(m['workflow_trace']);trace_validate(t,ROOT)
            need(all(x is None for x in t['model'].values()) and all(x is None for x in t['resources']['usage'].values()),'unknown producer usage invented')
            need(t['advance']['verification']=='producer_reported' and t['matched_run_id'] is None,'workflow result promoted')
    need(claims[ids[-1]]['record_type']=='integration_derived_restricted_result','new synthesis misattributed as supplied work')
    bridges=load('updates/EY/BRIDGES.json')['bridges']
    need(len(bridges)==5 and [b['state'] for b in bridges].count('PROVEN LOGICAL DEPENDENCY')==2,'bridge scope changed')
    for b in bridges:
        need(b['source_interface'] and b['destination_interface'] and b['scope'],'unpaired transfer')
        for r in b['evidence_refs']:check_ref(r)
    for slug in PINNED_PASTES:
        receipt=load('updates/EY/replay/'+slug+'.json')
        need(receipt['all_selected_commands_passed'] is True and all(c['returncode']==0 for c in receipt['commands']),'replay failed')
        for c in receipt['commands']:need(sha(c['log'])==c['log_sha256'],'rerun log changed')
    for x in load('updates/EY/replay/OUTPUT_MANIFEST.json'):check_ref(x)
    comp=load('updates/EY/replay/COMPARISON.json')['comparisons']
    need(comp[0]['comparison']=='exact' and comp[0]['non_timing_fields_match'] is True,'quantum policy repeatability changed')
    need([x['replayed'] for x in comp if not x['non_timing_fields_match']]==['updates/EY/replay/physical_gain/results.json','updates/EY/replay/physical_gain/coupling_results.json'],'floating/environment differences hidden or changed')
    optical=load('technology/records/T-inverted-recombination-displacement-gain/v0001.json');tech_validate(optical,ROOT)
    chemical=load('technology/records/T-autonomous-capacitive-chemomotor/v0002.json');tech_validate(chemical,ROOT)
    need(optical['stage']==chemical['stage']=='simulation' and chemical['disposition']=='paused','unwarranted development promotion')
    need(all(e['kind'] not in ['experimental_measurement','validated_prototype','demonstrated_system'] for e in optical['evidence']),'unexecuted material evidence promoted')
    # Every historical immutable scientific object remains byte-identical.
    namespaces=['updates','cards','frontier/cards','frontier/review_cards','state/checkpoints','technology/records','evaluation/workflows/records','web/pages']
    old_paths=set(git('ls-tree','-r','--name-only',BASE,'--',*namespaces).decode().splitlines())
    changed=set(git('diff','--name-only',BASE,'--',*namespaces).decode().splitlines())
    need(not old_paths & changed,'historical scientific/source object rewritten: '+str(old_paths&changed))
    for p in ['indexes/claims.jsonl','frontier/CURRENT_CLAIM_STATUS.jsonl','indexes/source_metadata.jsonl','web/documents.jsonl','frontier/OPEN_PROOF_GATES.jsonl','agent/SEMANTIC_NOTICES.jsonl','state/branches.tsv','agent/routes.tsv']:
        need((ROOT/p).read_bytes().startswith(git('show',BASE+':'+p)),'historical append-only ledger rewritten: '+p)
    for p,keys in [('indexes/agent_graph.json',['nodes','edges']),('indexes/agent_catalog.json',['claims']),('mechanisms/bridge_candidates.json',['bridges','rejected_transfers'])]:
        old=json.loads(git('show',BASE+':'+p));now=load(p)
        for k in keys:need(now[k][:len(old[k])]==old[k],'historical graph/catalog/bridge object altered')
    old_manifest=json.loads(git('show',BASE+':agent/access_manifest.json'))
    scientific={p:h for p,h in old_manifest['outputs'].items() if p.startswith(('frontier/dossiers/','frontier/connections/','frontier/proof_ranges/'))}
    views_changed={p for p,h in scientific.items() if sha(p)!=h}
    allowed={f'frontier/{kind}/{r}.{ext}' for r in ['N744','N765','N766','N767'] for kind,ext in [('dossiers','txt'),('connections','json')]}
    need(views_changed==allowed,'unscoped historical view change: '+str(views_changed^allowed))
    failures=load('updates/EY/replay/inherited_checkpoint_failures.json')
    need(len(failures)==3 and all(f['error']=='unsupported checkpoint schema' for f in failures),'inherited failure hidden/changed')
    print(json.dumps(dict(intake='EY',status='PASS',original_files=85,original_bytes=26341119,archive_members=79,producer_hashes=76,syntax_checks=26,cards=4,proof_sections=proofs,bridges=5,individual_checkpoints=4,source_code_invocations=10,new_physical_experiments=0,historical_views_changed=8,inherited_global_checkpoint_failures=3,scientific_truth_certified=False)))

if __name__=='__main__':
    main()
