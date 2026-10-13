#!/usr/bin/env python3
"""EZ byte, scope, provenance and append-only validator. Not scientific truth."""
import ast
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from zipfile import ZipFile

ROOT=Path(__file__).resolve().parents[2]
BASE='f437df815bef12f123ae4fe313d861ec1c862bc4'
sys.path.insert(0,str(ROOT))
from state.publish_checkpoint import validate_record,views
from technology.validate import validate as validate_tech
from evaluation.workflow_trace import validate as validate_trace

def need(x,m):
    if not x:raise ValueError(m)
def load(p):return json.loads((ROOT/p).read_text())
def rows(p):return [json.loads(l) for l in (ROOT/p).read_text().splitlines() if l.strip()]
def sha(p):return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
def git(*args):return subprocess.check_output(['git','-C',str(ROOT),*args])
def check_ref(r):
    need(sha(r['path'])==r['sha256'],'evidence SHA changed: '+r['path'])
    if r.get('lines'):
        a,b=r['lines'];need(1<=a<=b<=len((ROOT/r['path']).read_text().splitlines()),'bad inclusive range')

def main():
    manifest=load('updates/EZ/SOURCE_MANIFEST.json')
    need(manifest['base_revision']==BASE and manifest['missing_artifacts']==[],'pin or missing sources changed')
    originals=manifest['original_files'];need(len(originals)==51 and sum(v['bytes'] for v in originals)==4086545,'original inventory changed')
    pasted_pins={'source_spectrum':'3f6c416eca04ae0094c951281e1ccf36208b00d82ac5541b8682ce8215db2417','operational_decision':'ad0de434950c18436a8a4c32db36606446ca6d17db4c108eef82ae24e306c722','lattice_loop':'1f10e1ec3d0417b9b6d43668743e1e2e4e77651f70f355e60d914b48c4205172'}
    for slug,pin in pasted_pins.items():need(sha('updates/EZ/package/'+slug+'/ORIGINAL_PASTED_SOURCE.txt')==pin,'paste bytes changed')
    receipts=manifest['input_receipts'];need(len(receipts)==5,'input alias receipts lost')
    alias=[r for r in receipts if r['submission']=='operational_decision']
    need(len(alias)==3 and len({r['preserved_path'] for r in alias})==1 and len({r['sha256'] for r in alias})==1,'duplicate Frontier paste treated as separate work')
    derived=load('updates/EZ/DERIVED_MANIFEST.json')['records']
    need(len(derived)==58,'derived inventory changed')
    records=originals+derived
    for v in records:
        need(sha(v['path'])==v['sha256'] and (ROOT/v['path']).stat().st_size==v['bytes'],'source/derived artifact changed: '+v['path'])
        if 'lines' in v:need(len((ROOT/v['path']).read_text().splitlines())==v['lines'],'source line count changed')
        if v['path'].endswith('.py'):ast.parse((ROOT/v['path']).read_bytes(),filename=v['path'])
    hashes=0
    for bundle in manifest['bundles']:
        p=bundle['producer_manifest'];producer=load(p);pins=producer['files'];need(len(pins)==bundle['producer_hashes_checked'],'producer coverage changed')
        for name,pin in pins.items():
            f=str(Path(p).parent/name);need(sha(f)==(pin['sha256'] if isinstance(pin,dict) else pin),'producer hash mismatch')
            if isinstance(pin,dict):need((ROOT/f).stat().st_size==pin['bytes'],'producer byte length mismatch')
            hashes+=1
        if bundle['kind']=='archive':
            need(sha(bundle['path'])==bundle['sha256'],'original ZIP changed')
            with ZipFile(ROOT/bundle['path']) as z:
                need(z.testzip() is None and len(z.infolist())==bundle['members']==7,'ZIP CRC/members failed')
                dest=ROOT/Path(bundle['path']).parent/'recovered'
                for m in z.infolist():
                    if not m.is_dir():need((dest/m.filename).read_bytes()==z.read(m),'recovered ZIP member changed')
    need(hashes==44,'producer hash total changed')
    maps=load('updates/EZ/CLAIMS.json')['claims'];need(len(maps)==4,'claim count changed')
    ledger={v['card_id']:v for v in rows('frontier/CURRENT_CLAIM_STATUS.jsonl')};claims={v['id']:v for v in rows('indexes/claims.jsonl')}
    cat={v['id']:v for v in load('indexes/agent_catalog.json')['claims']};web={v['id']:v for v in load('web/catalog.json')}
    gates=rows('frontier/OPEN_PROOF_GATES.jsonl');proofs=0
    for m in maps:
        cid=m['id'];s=load('frontier/cards/'+cid+'.json')
        need(s==ledger[cid] and s['claim_status']==claims[cid]['status']=='source_derived_unreviewed','scientific status mismatch/promotion')
        need(sha(s['card_path'])==s['card_sha256']==cat[cid]['card_sha256'],'card SHA mismatch')
        need(claims[cid]['source_paths']==web[cid]['source_paths'] and claims[cid]['source_ids']==web[cid]['source_ids'],'web source linkage mismatch')
        need(claims[cid]['depends_on']==[d['target'] for d in s['depends_on']]==cat[cid]['dependencies']['depends_on'],'dependency mismatch')
        need(s['validation']['external_correctness']==s['validation']['historical_priority']=='UNKNOWN','validation invented')
        need(s['supersedes']==s['invalidates']==[],'unscoped supersession/invalidation')
        for r in s['proof_availability']['located_proof_sources']+s['proof_availability']['available_evidence_sources']:check_ref(r)
        proofs+=len(s['proof_availability']['located_proof_sources'])
        cg=[g for g in gates if g['gate_id'].startswith('G-EZ-') and cid in g['card_ids']]
        need(len(cg)==2 and all(g['status']=='open' and g['completion_evidence']==[] for g in cg),'open gate promoted')
        for topic in s['topics']:
            p='agent/topics/'+topic+'.tsv';content=(ROOT/p).read_text()
            need(content.startswith(git('show',BASE+':'+p).decode()),'historical topic route rewritten')
            need(sum(l.startswith(cid+'\t') for l in content.splitlines())==1,'topic route missing/duplicated')
            need(topic+': '+p+' ('+str(len(content.splitlines())-1)+' cards)' in (ROOT/'agent/topics.txt').read_text(),'topic count stale')
        cp=load(m['checkpoint']);validate_record(cp,ROOT)
        need(cp['base_revision']==BASE and cp['parent_checkpoint_ids']==[],'new branch ancestry guessed')
        vs=views(ROOT,{cp['branch_id']:{cp['checkpoint_id']:cp}});p='state/branches/'+cp['branch_id']+'.txt'
        need((ROOT/p).read_text()==vs[p],'new branch view stale')
        row=next(l for l in vs['state/branches.tsv'].splitlines() if l.startswith(cp['branch_id']+'\t'))
        need((ROOT/'state/branches.tsv').read_text().splitlines().count(row)==1,'new branch registry row absent/duplicate')
        if m['workflow_trace']:
            tr=load(m['workflow_trace']);validate_trace(tr,ROOT)
            need(tr['mode']==tr['context']['conversation_relation']=='UNKNOWN','retained-context mode inferred')
            need(all(v is None for v in tr['model'].values()) and all(v is None for v in tr['resources']['usage'].values()),'unobserved model/usage inferred')
    bridges=load('updates/EZ/BRIDGES.json')['bridges'];need(len(bridges)==8,'bridge count')
    canonical={b['id']:b for b in load('mechanisms/bridge_candidates.json')['bridges']}
    for b in bridges:
        need(b==canonical[b['id']] and b['state']==b['status'],'canonical bridge mismatch')
        need(all(k in b for k in ['source_interface','destination_interface','missing_lemma','cost','evidence_refs']),'paired interface incomplete')
        for r in b['evidence_refs']:check_ref(r)
    for tid in ['T-payoff-certified-local-quantum-control','T-phase-controlled-lattice-ion-transport']:
        t=load('technology/records/'+tid+'/v0001.json');validate_tech(t,ROOT)
        need(t['stage']=='simulation' and any(g['stage']=='experiment' and g['decision']=='open' for g in t['gates']),'physical readiness promoted')
    # Exact historical append-only ledgers and immutable semantic objects.
    prefixes=['indexes/claims.jsonl','indexes/source_metadata.jsonl','frontier/CURRENT_CLAIM_STATUS.jsonl','frontier/OPEN_PROOF_GATES.jsonl','agent/SEMANTIC_NOTICES.jsonl','agent/routes.tsv','state/branches.tsv','web/documents.jsonl']
    for p in prefixes:need((ROOT/p).read_bytes().startswith(git('show',BASE+':'+p)),'historical ledger prefix changed: '+p)
    for p,key in [('indexes/agent_catalog.json','claims'),('indexes/agent_graph.json','nodes'),('indexes/agent_graph.json','edges'),('mechanisms/bridge_candidates.json','bridges')]:
        before=json.loads(git('show',BASE+':'+p))[key];need(load(p)[key][:len(before)]==before,'historical semantic entries changed')
    before=json.loads(git('show',BASE+':indexes/query_aliases.json'));need(all(load('indexes/query_aliases.json').get(k)==v for k,v in before.items()),'historical aliases changed')
    before=json.loads(git('show',BASE+':web/catalog.json'));need(load('web/catalog.json')[:len(before)]==before,'historical web records changed')
    changed=git('diff','--name-only',BASE).decode().splitlines()
    immutable=('cards/','frontier/cards/','state/checkpoints/','technology/records/','evaluation/workflows/records/','updates/')
    for p in changed:
        if p.startswith(immutable):need(p.startswith('updates/EZ/'),'historical immutable artifact changed: '+p)
    publication=load('updates/EZ/PUBLICATION_STATUS.json')
    need(publication['standard_publisher_exit_code']!=0 and len(publication['individually_validated_new_checkpoints'])==4,'global failure/fallback misreported')
    for r in publication['inherited_records_preserved']:
        need(sha(r['path'])==r['sha256']==hashlib.sha256(git('show',BASE+':'+r['path'])).hexdigest(),'inherited malformed checkpoint modified')
    print(json.dumps(dict(status='PASS',base_revision=BASE,original_files=len(originals),original_bytes=sum(v['bytes'] for v in originals),producer_hashes=hashes,derived_and_replay_files=len(derived),cards=4,proof_routes=proofs,paired_bridges=8,individual_checkpoints=4,global_checkpoint_validation='inherited failure preserved;not passed',scientific_truth_checked=False),indent=2))

if __name__=='__main__':main()
