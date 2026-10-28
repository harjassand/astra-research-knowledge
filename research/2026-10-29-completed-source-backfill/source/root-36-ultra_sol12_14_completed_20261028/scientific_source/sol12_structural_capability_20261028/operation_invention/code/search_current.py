"""Bounded current content/structured search using the pinned public scorer.

Only current search projections and needed posting shards are loaded. Returned
matches are navigation evidence; packets and governing proofs are required.
"""
from pathlib import Path
from urllib.request import urlopen
import json,sys
HERE=Path(__file__).resolve().parents[1]
DATA_ROOT=HERE.parents[1]/'sol11_operation_discovery_20261028/capability_backchain/source_cache'
CACHE=HERE/'sources/current_shards'
sys.path.insert(0,str(DATA_ROOT))
from knowledge.model import tokens,digest,score_query,query_terms
PIN='8d51d60762b3ee28c10aaaa56e1b92da119dc1cc'
BASE='https://raw.githubusercontent.com/harjassand/astra-research-knowledge/'+PIN+'/'
def rows(name):
 return [json.loads(line) for line in (DATA_ROOT/'knowledge/current'/name).read_bytes().splitlines() if line]
def search(query,method='content',limit=6):
 records={r['id']:r for r in rows('records.jsonl')};docs=rows('documents.jsonl')
 catalog=json.loads((DATA_ROOT/'knowledge/current/catalog.json').read_bytes())
 terms={w:1. for w in tokens(query)} if method=='content' else query_terms(query,catalog['concepts'])[0]
 folder='content' if method=='content' else 'postings';posting={}
 for shard in sorted({digest(w.encode())[:2] for w in terms}):
  rel=f'knowledge/current/{folder}/{shard}.json';target=CACHE/rel
  if not target.exists():
   target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(urlopen(BASE+rel,timeout=30).read())
  posting.update(json.loads(target.read_bytes()))
 ranked,scores,matches=score_query(posting,terms);out=[];seen=set()
 for idx in ranked:
  doc=docs[idx];rec=records[doc['record_id']];group=(rec['parents'] or [rec['id']])[0]
  if group in seen:continue
  seen.add(group)
  out.append({k:rec.get(k) for k in ['id','title','statement','contract','review','review_overlays','notices','evidence']}
     |{'score':scores[idx],'document':doc['id'],'matches':sorted(matches[idx])})
  if len(out)>=limit:break
 result={'query':query,'method':method,'revision':PIN,'results':out}
 dest=HERE/'searches';dest.mkdir(exist_ok=True)
 (dest/(digest((method+query).encode())[:12]+'.json')).write_text(json.dumps(result,indent=2)+'\n')
 return result
if __name__=='__main__':
 result=search(sys.argv[1],sys.argv[2] if len(sys.argv)>2 else 'content')
 for rec in result['results']:
  print(json.dumps({k:rec[k] for k in ['id','title','statement','score','matches']},ensure_ascii=False))
