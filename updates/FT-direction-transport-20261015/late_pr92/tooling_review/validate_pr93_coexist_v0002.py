#!/usr/bin/env python3
"""Read-only additive adapter: exact owned PR93 gates plus preserved PR92 history."""
from pathlib import Path
import argparse,copy,hashlib,json,re,subprocess,sys
sys.dont_write_bytecode=True
ORIGINAL='updates/FT-direction-transport-20261015/validate.py'
EXPECTED='895af1e6a0656545bdd11f6f570732ad65a311bd3f7e4492dee726bac8985579'
PR92='5eb2441c93011d4fefb819b6f751f33537427dc3'
BEFORE="gates = {x['gate_id']: x for x in rows(root, 'frontier/OPEN_PROOF_GATES.jsonl') if x.get('gate_id', '').startswith('G-FT-')}"
AFTER="owned_gate_ids = set(receipt['gate_ids'])\n    gates = {x['gate_id']: x for x in rows(root, 'frontier/OPEN_PROOF_GATES.jsonl') if x.get('gate_id') in owned_gate_ids}"
IMMUTABLE=('cards/','frontier/cards/','frontier/review_cards/','updates/','state/checkpoints/','state/branches/','technology/records/','web/pages/','evaluation/workflows/records/','mechanisms/bridges/')
def adapt(raw):
 if hashlib.sha256(raw).hexdigest()!=EXPECTED:raise ValueError('preserved PR93 validator hash changed; append a new reviewed adapter version')
 source=raw.decode();assert source.count(BEFORE)==1
 access_before="'check', '--base-revision', BASE]"
 assert source.count(access_before)==1
 return source.replace(BEFORE,AFTER).replace(access_before,"'check', '--base-revision', COEXIST_PROJECTION_BASE]")
def git(root,*args):return subprocess.check_output(['git','-C',str(root),*args])
def need(v,msg):
 if not v:raise ValueError(msg)
def encoded(v):return (json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode()
def check_pr92_history(root):
 subprocess.run(['git','-C',str(root),'merge-base','--is-ancestor',PR92,'HEAD'],check=True,capture_output=True)
 old=set(git(root,'ls-tree','-r','--name-only',PR92).decode().splitlines())
 for name in git(root,'diff','--name-only',PR92).decode().splitlines():need(not(name in old and name.startswith(IMMUTABLE)),'previously published PR92 immutable bytes changed: '+name)
 for name in ['indexes/claims.jsonl','indexes/source_metadata.jsonl','frontier/CURRENT_CLAIM_STATUS.jsonl','frontier/OPEN_PROOF_GATES.jsonl','agent/SEMANTIC_NOTICES.jsonl','web/documents.jsonl','state/branches.tsv']:
  need((root/name).read_bytes().startswith(git(root,'show',PR92+':'+name)),'canonical PR92 historical registry byte prefix changed: '+name)
 for name,fields in [('indexes/agent_catalog.json',['claims']),('indexes/agent_graph.json',['nodes','edges']),('mechanisms/bridge_candidates.json',['bridges','rejected_transfers']),('web/catalog.json',[None])]:
  oldbytes=git(root,'show',PR92+':'+name);before=json.loads(oldbytes);current=json.loads((root/name).read_text());projection=copy.deepcopy(current)
  for field in fields:
   a=before[field] if field else before;b=current[field] if field else current
   need(b[:len(a)]==a,'canonical PR92 historical array value/order changed: '+name)
   if field:projection[field]=b[:len(a)]
   else:projection=b[:len(a)]
  need(encoded(projection)==oldbytes,'canonical PR92 historical JSON key order/metadata bytes changed: '+name)
 return {'pr92_pin':PR92,'previous_immutable_paths_preserved':len([p for p in old if p.startswith(IMMUTABLE)]),'canonical_registry_prefixes_preserved':True,'scope':'PR92-first canonical append order; PR93 immutable artifacts retain original bytes and Git history.'}
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--repo',type=Path,required=True);p.add_argument('--replay-dir',type=Path,required=True);p.add_argument('--projection-base-revision',required=True);p.add_argument('--pre-publication',action='store_true');p.add_argument('--report',type=Path);a=p.parse_args();root=a.repo.resolve()
 if a.report and a.report.resolve().is_relative_to(root):raise ValueError('receipt must remain outside checkout')
 need(re.fullmatch(r'[0-9a-f]{40}',a.projection_base_revision),'full checked projection ancestor required')
 subprocess.run(['git','-C',str(root),'merge-base','--is-ancestor',a.projection_base_revision,'HEAD'],check=True,capture_output=True)
 history=check_pr92_history(root);original=root/ORIGINAL;source=adapt(original.read_bytes());namespace={'__name__':'pr93_preserved_validator_scoped_v0002','__file__':str(original),'COEXIST_PROJECTION_BASE':a.projection_base_revision};exec(compile(source,str(original),'exec'),namespace)
 result=namespace['validate'](root,a.replay_dir.resolve(),a.pre_publication)
 receipt={'schema':'astra.ft-pr93-coexistence-validator.v0002','status':'PASS','original_path':ORIGINAL,'original_sha256':EXPECTED,'adapted_in_memory_sha256':hashlib.sha256(source.encode()).hexdigest(),'change':'FT gates selected by exact generator-owned IDs; access regeneration checked against the explicitly supplied current projection ancestor. Original science/source/checkpoint BASE remains untouched. Original validator bytes unchanged; additional PR92-first history audit.','history':history,'projection_base_revision':a.projection_base_revision,'result':result,'scope':'Read-only additive integrity only; no exporter, replay, publication or scientific certification.'}
 if a.report:a.report.parent.mkdir(parents=True,exist_ok=True);a.report.write_text(json.dumps(receipt,indent=2)+'\n')
 print(json.dumps(receipt,indent=2))
if __name__=='__main__':main()
