#!/usr/bin/env python3
"""Validate FN selected committed bytes, scoped public routes and new checkpoint; no research replay."""
from __future__ import annotations
import argparse, hashlib, html, json, subprocess, sys, zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from state.publish_checkpoint import validate_record,views
CID='N816-exact-local-mps-response-completion-and-aklt-comparator-boundaries'
PK='updates/FN/package/frontier_genesis_v1'
REV='e7ae999e957d70f98ccb9bd789c3eeb6c8229d30'
BASE='ace0cfc4437fe91c20ccd24d69e0ee4bb335e871'
def digest(b:bytes)->str:return hashlib.sha256(b).hexdigest()
def get(p):return json.loads((ROOT/p).read_text())
def assert_bytes(p,h,n=None):
 b=(ROOT/p).read_bytes();assert digest(b)==h,p
 if n is not None:assert len(b)==n,p
 return b
def rows(p):return [json.loads(s) for s in (ROOT/p).read_text().splitlines()]
def main():
 a=argparse.ArgumentParser();a.add_argument('--verify-ultra',action='store_true',help='also compare each selected member directly with the separate Ultra Git commit');a.add_argument('--ultra-repo',default='/Users/harjas/Documents/ChatGPT/ultra');args=a.parse_args()
 sm=get('updates/FN/SOURCE_MANIFEST.json');sel=get(f'{PK}/SOURCE_MANIFEST.json');cmp=get('updates/FN/SOURCE_COMPARISON.json')
 assert sm['source_commit']==sel['source_commit']==cmp['ultra_git_commit']==REV
 assert sm['base_revision']==BASE
 assert sm['selection_manifest']['sha256']==digest((ROOT/f'{PK}/SOURCE_MANIFEST.json').read_bytes())
 assert sm['full_packet_manifest_sha256']==digest((ROOT/f'{PK}/source/SOURCE_MANIFEST.json').read_bytes())
 assert sm['selected_commit_comparison']['sha256']==digest((ROOT/'updates/FN/SOURCE_COMPARISON.json').read_bytes())
 assert cmp['result']==sm['selected_commit_comparison']['status']=='PASS_EXACT_SELECTED_BYTES'
 recs=sel['records'];assert len(recs)==54==cmp['compared_count']==sm['selective_archive']['members']
 assert sum(x['readable'] for x in recs)==28==cmp['copied_readable_count']==len(sm['selected_copied_files'])
 archive=sm['selective_archive'];assert_bytes(archive['path'],archive['sha256'],archive['bytes'])
 with zipfile.ZipFile(ROOT/archive['path']) as z:
  assert z.namelist()==[x['archive_member'] for x in recs]
  assert len(set(z.namelist()))==len(recs)
  for rec in recs:
   rel=rec['archive_member'];assert not Path(rel).is_absolute() and '..' not in Path(rel).parts
   b=z.read(rel);assert digest(b)==rec['sha256'] and len(b)==rec['bytes'],rel
   if rec['readable']:
    assert assert_bytes(rec['capital_path'],rec['sha256'],rec['bytes'])==b
   if args.verify_ultra:
    original=subprocess.check_output(['git','show',f'{REV}:{rec["original_path"]}'],cwd=args.ultra_repo)
    assert original==b,rec['original_path']
 assert {x['path'] for x in sm['selected_copied_files']}=={x['capital_path'] for x in recs if x['readable']}
 for x in sm['selected_copied_files']:assert_bytes(x['path'],x['sha256'],x['bytes'])
 for x in get('updates/FN/DERIVED_MANIFEST.json')['records']:assert_bytes(x['path'],x['sha256'],x['bytes'])
 cp=f'cards/{CID}.txt';card=(ROOT/cp).read_text();status=get(f'frontier/cards/{CID}.json')
 assert status['card_sha256']==digest(card.encode()) and status['claim_status']=='source_derived_unreviewed'
 assert 'Mission NOT_ACHIEVED' in card and 'N764' in card and 'REDESIGN' in card
 assert 'Knabe' in card and 'rho' in card and 'N=20' in card
 assert (ROOT/f'frontier/review_cards/{CID}.txt').read_bytes().endswith(card.encode())
 claims=[x for x in rows('indexes/claims.jsonl') if x['id']==CID];statuses=[x for x in rows('frontier/CURRENT_CLAIM_STATUS.jsonl') if x['card_id']==CID]
 assert len(claims)==len(statuses)==1 and statuses[0]==status
 cl=claims[0];assert cl['status']=='source_derived_unreviewed'
 refs={r['source_id']:r for r in status['proof_availability']['located_proof_sources']+status['proof_availability']['available_evidence_sources']}
 assert set(refs)==set(cl['source_ids']) and len(refs)==12
 sources={x['source_id']:x for x in rows('indexes/source_metadata.jsonl') if x.get('source_id') in refs}
 docs={x['id']:x for x in rows('web/documents.jsonl') if x.get('id') in refs}
 assert set(sources)==set(docs)==set(refs)
 for sid,r in refs.items():
  assert sources[sid]['path']==docs[sid]['path']==r['path']
  b=assert_bytes(r['path'],r['sha256']);assert sources[sid]['sha256']==r['sha256']
  assert r['lines'][1]<=len(b.decode().splitlines())
  page=(ROOT/'web'/docs[sid]['url']).read_text()
  assert html.escape(b.decode()) in page
 web=[x for x in get('web/catalog.json') if x['id']==CID];assert len(web)==1 and web[0]['text']==card
 assert web[0]['source_ids']==cl['source_ids'] and web[0]['source_paths']==cl['source_paths']
 assert (ROOT/'web'/web[0]['url']).is_file()
 ac=get('indexes/agent_catalog.json');assert len([x for x in ac['claims'] if x['id']==CID and x['card_sha256']==digest(card.encode())])==1
 graph=get('indexes/agent_graph.json');assert len([x for x in graph['nodes'] if x['id']==CID])==1
 assert {x['to'] for x in graph['edges'] if x['from']==CID and x['kind']=='provenance'}==set(refs)
 own=[x for x in rows('frontier/OPEN_PROOF_GATES.jsonl') if CID in x['card_ids'] and x['gate_id'].startswith('G-FN-')]
 assert len(own)==2 and all(x['status']=='open' and x['completion_evidence']==[] and x==get(f'frontier/gates/{x["gate_id"]}.json') for x in own)
 ownb=[x for x in get('indexes/blockers.json')['blockers'] if CID in x.get('affected_cards',[]) and x['id'].startswith('B-FN-')]
 assert len(ownb)==3 and all(x==get(f'frontier/blockers/{x["id"]}.json') for x in ownb)
 route=f'{CID}\t';assert sum(x.startswith(route) for x in (ROOT/'agent/routes.tsv').read_text().splitlines())==1
 topics=(ROOT/'agent/topics.txt').read_text()
 for topic in status['topics']:
  p=f'agent/topics/{topic}.tsv';lines=(ROOT/p).read_text().splitlines()
  assert sum(x.startswith(route) for x in lines)==1,p
  assert f'{topic}: {p} ({len(lines)-1} cards)' in topics
  assert sum(x.startswith(CID+' | ') for x in (ROOT/f'topics/{topic}.txt').read_text().splitlines())==1
 cm=get('updates/FN/CLAIMS.json');assert cm['claims'][0]['id']==CID
 cpath=cm['claims'][0]['checkpoint'];ck=get(cpath);validate_record(ck,ROOT)
 assert ck['parent_checkpoint_ids']==[] and ck['base_revision']==BASE
 expected=views(ROOT,{ck['branch_id']:{ck['checkpoint_id']:ck}})[f'state/branches/{ck["branch_id"]}.txt']
 assert (ROOT/f'state/branches/{ck["branch_id"]}.txt').read_text()==expected
 assert sum(x.startswith(ck['branch_id']+'\t') for x in (ROOT/'state/branches.tsv').read_text().splitlines())==1
 for p in ['indexes/claims.jsonl','indexes/source_metadata.jsonl','frontier/CURRENT_CLAIM_STATUS.jsonl','frontier/OPEN_PROOF_GATES.jsonl','agent/routes.tsv','state/branches.tsv','web/documents.jsonl']:
  original=subprocess.check_output(['git','show',f'{BASE}:{p}'],cwd=ROOT)
  assert (ROOT/p).read_bytes().startswith(original),p
 print(json.dumps({'status':'PASS','card':CID,'source_commit':REV,'archive_members':len(recs),'readable_copies':28,'source_routes':len(refs),'gates':len(own),'blockers':len(ownb),'ultra_direct_comparison':args.verify_ultra,'scientific_correctness':'NOT_EVALUATED','physical_or_matched_advantage':'NOT_ESTABLISHED'},sort_keys=True))
if __name__=='__main__':main()
