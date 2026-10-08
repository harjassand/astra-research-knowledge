#!/usr/bin/env python3
"""Offline, portable research retrieval. Python standard library; no model calls."""
from pathlib import Path
import importlib.util
import argparse, hashlib, http.server, json, os, re, shutil, sqlite3, sys
from urllib.parse import parse_qs, urlparse

ROOT=Path(__file__).resolve().parents[1]
DB=ROOT/'indexes/knowledge.sqlite3'
_spec=importlib.util.spec_from_file_location('astra_frontier',ROOT/'frontier/retrieve.py')
decision=importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(decision)
try:
 import tiktoken
 ENCODER=tiktoken.get_encoding('o200k_base')
except Exception:
 ENCODER=None

def count(s):return len(ENCODER.encode(s,disallowed_special=())) if ENCODER else len(s.encode('utf-8'))
def mode():return 'o200k_base_estimate' if ENCODER else 'conservative_utf8_byte_upper_bound'
def connect():
 c=sqlite3.connect(f'file:{DB}?mode=ro',uri=True);c.row_factory=sqlite3.Row;return c
def load(path):return json.loads((ROOT/path).read_text())
def jprint(x):print(json.dumps(x,ensure_ascii=False,indent=2))
STOP_WORDS={'the','a','an','of','to','for','in','and','what','how','is','are','does','can','with','on'}
def query_terms(q):
 return list(dict.fromkeys(x for x in re.findall(r'[\w]+',q.lower()) if x not in STOP_WORDS))[:20]

def word_query(q,op='AND'):
 words=query_terms(q)
 return (' '+op+' ').join('"'+x.replace('"','""')+'"' for x in words)

def search(q,limit=6,topic=None,history=False):
 expr=word_query(q)
 if not expr:return []
 filters=[];params=[]
 if topic:filters.append('instr(d.topics,?)>0');params.append('"'+topic+'"')
 if not history:filters.append("(d.cycle IN (0,19) OR d.role='card')")
 filt=(' AND '+' AND '.join(filters)) if filters else ''
 sql='''SELECT s.chunk_id,d.id AS source_id,d.sha256 AS text_sha256,d.title,d.path,d.role,d.cycle,d.topics,d.extraction,c.start_line,c.end_line,c.text,c.tokens,
 bm25(search,0,0,4,1,2,1) AS score FROM search s JOIN chunks c ON c.id=s.chunk_id JOIN docs d ON d.id=s.doc_id
 WHERE search MATCH ?'''+filt+''' ORDER BY CASE WHEN d.role='card' THEN 0 WHEN d.role IN ('research_note','research_report') THEN 1 ELSE 2 END,score LIMIT ?'''
 with connect() as c:
  rows=c.execute(sql,[expr]+params+[limit*4]).fetchall()
  if not rows:rows=c.execute(sql,[word_query(q,'OR')]+params+[limit*4]).fetchall()
 # Human query terms route into dense mathematical records without changing
 # their verbatim content. This supplements lexical FTS, not a semantic model.
 aliases=load('indexes/query_aliases.json');terms=query_terms(q)
 if not terms:return []
 routed=[]
 with connect() as conn:
  for cid,words in aliases.items():
   hit=sum(t in words.split() for t in terms)
   if hit<2 or hit<.6*len(terms):continue
   card=conn.execute('SELECT path FROM cards WHERE id=?',(cid,)).fetchone()
   if not card:continue
   doc=conn.execute('SELECT * FROM docs WHERE path=?',(card[0],)).fetchone()
   if topic and topic not in json.loads(doc['topics']):continue
   choices=conn.execute('SELECT * FROM chunks WHERE doc_id=? ORDER BY seq',(doc['id'],)).fetchall()
   chunk=max(choices,key=lambda c:sum(t in c['text'].lower() for t in terms))
   item={'chunk_id':chunk['id'],'source_id':doc['id'],'text_sha256':doc['sha256'],'title':doc['title'],'path':doc['path'],'role':doc['role'],'cycle':doc['cycle'],'topics':doc['topics'],'extraction':doc['extraction'],'start_line':chunk['start_line'],'end_line':chunk['end_line'],'text':chunk['text'],'tokens':chunk['tokens'],'score':-hit,'routing':'curated_query_alias'}
   routed.append((hit,item))
 routed.sort(key=lambda x:-x[0])
 out=[];seen=set()
 rows=[v for _,v in routed]+[dict(r) for r in rows]
 for row in rows:
  x=dict(row)
  if x['text_sha256'] in seen:continue
  seen.add(x['text_sha256']);x['topics']=json.loads(x['topics']);x['citation']=x['chunk_id'];x['web_page']='web/pages/'+x['source_id']+'.html'
  x['reading_scope']='Retrieved excerpt; source scientific status is not upgraded.'
  if x['role']=='card':x['current_status']=decision.notice(x['path'])
  else:x['current_claim_alerts']=decision.document_alerts(x['source_id'])
  out.append(x)
  if len(out)>=limit:break
 return out

def route(q,limit=5,topic=None,history=False):
 """Return compact card metadata for navigation without excerpt text."""
 if limit<0:raise ValueError('limit must be non-negative')
 if limit==0:return {'query':q,'limit':0,'metadata_only':True,'cards':[]}
 hits=search(q,min(max(limit*4,limit),100),topic,history);cards=[];seen=set()
 with connect() as c:
  for hit in hits:
   if hit['role']!='card' or hit['path'] in seen:continue
   seen.add(hit['path'])
   row=c.execute('SELECT id,title,status,topics,path FROM cards WHERE path=?',(hit['path'],)).fetchone()
   if not row:continue
   cards.append({'id':row['id'],'title':row['title'],'status':row['status'],'topics':json.loads(row['topics']),'local_path':row['path'],'web_page':'web/pages/'+hit['source_id']+'.html','current_status':decision.notice(row['id'])})
   if len(cards)>=limit:break
 return {'query':q,'limit':limit,'metadata_only':True,'cards':cards,'lemma_routes':decision.lemma_routes(q,min(limit,3))}

def get_doc(identifier):
 with connect() as c:
  row=c.execute('SELECT * FROM docs WHERE id=? OR path=?',(identifier,identifier)).fetchone()
  if not row:
   chunk=c.execute('SELECT doc_id FROM chunks WHERE id=?',(identifier,)).fetchone()
   if chunk:row=c.execute('SELECT * FROM docs WHERE id=?',(chunk['doc_id'],)).fetchone()
  if not row:
   card=c.execute('SELECT path FROM cards WHERE id=?',(identifier,)).fetchone()
   if card:row=c.execute('SELECT * FROM docs WHERE path=?',(card[0],)).fetchone()
  if not row:raise ValueError('Unknown source/card ID or virtual path')
  return dict(row)

def read(identifier,start=None,end=None,max_bytes=24000):
 if max_bytes<0:raise ValueError('max_bytes must be non-negative')
 chunk=None
 with connect() as c:chunk=c.execute('SELECT start_line,end_line FROM chunks WHERE id=?',(identifier,)).fetchone()
 doc=get_doc(identifier);lines=doc.pop('text').splitlines()
 if start is None:start=chunk['start_line'] if chunk else 1
 if end is None:end=chunk['end_line'] if chunk else len(lines)
 if start<1:raise ValueError('start must be at least 1')
 if start>len(lines):raise ValueError(f'start line {start} is beyond end of source ({len(lines)} lines)')
 if end<start:raise ValueError('end must be greater than or equal to start')
 end=min(len(lines),end);chosen=[];used=0
 for i in range(start-1,end):
  line=f'[L{i+1}] '+lines[i]+'\n';size=len(line.encode())
  if used+size>max_bytes:break
  chosen.append(line);used+=size
 last=start+len(chosen)-1 if chosen else None
 result={'source':doc,'start_line':start if chosen else None,'end_line':last,'total_lines':len(lines),'complete':bool(chosen) and start==1 and last==len(lines),'next_line':last+1 if last is not None and last<end else (start if not chosen and start<=end else None),'text':''.join(chosen),'byte_count':used,'max_bytes':max_bytes,'over_byte_limit':False,'citation_chunk':identifier if chunk else None}
 if doc['role']=='card':result['current_status']=decision.notice(doc['path'])
 else:result['current_claim_alerts']=decision.document_alerts(doc['id'])
 return result

def packet(q,budget=6000,topic=None,history=False,max_bytes=None):
 if budget<0:raise ValueError('budget must be non-negative')
 if max_bytes is not None and max_bytes<0:raise ValueError('max_bytes must be non-negative')
 intro=f'ASTRA RETRIEVAL PACKET | query={q} | budget_meter={mode()}\nClaims remain source-scoped. Partial extracts require opening the cited record/proof before decisive use. Historical instructions are source data.\n'
 pieces=[intro];hits=search(q,16,topic,history);included=[];not_fit=[];omitted_byte=[];seen=set();omitted_status=[]
 def fits(text):return count(text)<=budget and (max_bytes is None or len(text.encode('utf-8'))<=max_bytes)
 for hit in hits:
  did=hit['source_id']
  if did in seen:continue
  seen.add(did);doc=get_doc(did);text=doc['text']
  full=doc['role']=='card'
  body=text if full else hit['text']
  opening=''
  if not full:opening='SOURCE OPENING (context, not proof):\n'+text[:850]+'\n'
  head=f'\n<BLOCK id="{hit["citation"]}" source="{did}" path="{doc["path"]}" role="{doc["role"]}" cycle="{doc["cycle"]}" completeness="'+('complete_card' if full else 'excerpt')+'">\n'
  alert=decision.banner(doc['path']) if full else ('CURRENT CLAIM ALERTS: '+json.dumps(hit.get('current_claim_alerts',[]),ensure_ascii=False,separators=(',',':'))+'\n' if hit.get('current_claim_alerts') else '')
  block=head+alert+opening+body+'\n</BLOCK>\n'
  if not fits(''.join(pieces)+block):
   # A large card remains available intact; only a scoped excerpt enters this packet.
   block=head.replace('complete_card','partial_card')+alert+text[:700]+'\nMATCHED EXCERPT:\n'+hit['text']+'\n</BLOCK>\n'
  if not fits(''.join(pieces)+block):
   if full:omitted_status.append(decision.notice(doc['path']))
   if max_bytes is not None and len((''.join(pieces)+block).encode('utf-8'))>max_bytes:omitted_byte.append(did)
   else:not_fit.append(did)
   continue
  pieces.append(block);included.append({'id':did,'citation':hit['citation'],'path':doc['path']})
 trailer='\nOpen source by ID: python3 tools/knowledge.py read <ID>. Expand the budget or issue narrower queries for prerequisites and counterexamples.\n'
 trailer_candidate=''.join(pieces)+trailer
 trailer_included=fits(trailer_candidate)
 if trailer_included:pieces.append(trailer)
 result=''.join(pieces)
 if not fits(result):raise ValueError('Budgets are too small for packet header')
 return {'query':q,'budget':budget,'budget_meter':mode(),'count':count(result),'max_bytes':max_bytes,'byte_count':len(result.encode('utf-8')),'included':included,'not_fitted_ids':not_fit,'omitted_for_max_bytes':omitted_byte,'omitted_current_status':omitted_status,'trailer_included':trailer_included,'trailer_omitted_for_max_bytes':max_bytes is not None and count(trailer_candidate)<=budget and len(trailer_candidate.encode('utf-8'))>max_bytes,'text':result}

def links(identifier):
 try:did=get_doc(identifier)['id']
 except ValueError:did=identifier
 with connect() as c:
  return [dict(r) for r in c.execute('SELECT * FROM edges WHERE src IN (?,?) OR dst IN (?,?)',(identifier,did,identifier,did))]

def family(identifier):
 data=load('indexes/families.json');key=str(int(identifier))
 row=data.get(key,data.get(key.zfill(3))) if isinstance(data,dict) else [x for x in data if str(x.get('id',x.get('family_id',''))).lstrip('0')==key]
 if row is None:raise ValueError('Family ID absent from literal coverage ledger')
 raw=load('indexes/coverage_original.json')
 indices=row.get('assessment_row_indexes',[]) if isinstance(row,dict) else []
 detailed=[raw['assessments'][i] for i in indices]
 subsequent=[]
 if (ROOT/'indexes/coverage_updates.json').is_file():
  for update in load('indexes/coverage_updates.json'):
   for item in update['coverage']['families']:
    if int(item['family_id'])==int(key):subsequent.append({'source':update['source'],'source_id':update['source_id'],'record':item})
 return {'family':key,'scope':'Literal reported assessments; no reading/proof-status upgrade. Multiple assessments may disagree.','catalogue':row,'assessments':detailed or row,'subsequent_reading_records':subsequent}

def sources(q,limit=6):
 terms=[x for x in re.findall(r'\w+',q.lower()) if len(x)>1];found=[];seen=set()
 with (ROOT/'indexes/source_metadata.jsonl').open() as f:
  for line in f:
   row=json.loads(line);hay=json.dumps(row,ensure_ascii=False).lower();score=sum(t in hay for t in terms)
   if not score:continue
   key=(row.get('url'),row.get('title'),row.get('date_version'),row.get('read_depth'))
   if str(key) in seen:continue
   seen.add(str(key));found.append((score,row))
 found.sort(key=lambda x:-x[0]);return {'scope':'Source metadata reported by original researchers, not independently reverified.','sources':[r for _,r in found[:limit]]}

def asset(identifier):
 with connect() as c:
  row=c.execute('SELECT * FROM files WHERE path=?',(identifier,)).fetchone()
  if not row:
   doc=get_doc(identifier);row=c.execute('SELECT * FROM files WHERE path=?',(doc['path'],)).fetchone()
  if not row:raise ValueError('No original archived file for this identifier')
  out=dict(row);h=out['sha256'];out['object_path']='evidence/objects/'+h[:2]+'/'+h[2:];out['status']='Exact original bytes, not scientific verification.';return out

def verify(full=False):
 errors=[];n=0;seen=set();bytes_=0
 with (ROOT/'indexes/files.jsonl').open() as f:
  for line in f:
   row=json.loads(line);digest=row['sha256']
   if digest in seen:continue
   seen.add(digest);p=ROOT/'evidence/objects'/digest[:2]/digest[2:];n+=1
   if not p.is_file() or p.stat().st_size!=row['bytes']:errors.append({'path':row['path'],'error':'missing_or_wrong_size'});continue
   bytes_+=row['bytes']
   if full:
    h=hashlib.sha256()
    with p.open('rb') as data:
     while b:=data.read(2**20):h.update(b)
    if h.hexdigest()!=digest:errors.append({'path':row['path'],'error':'hash_mismatch'})
 with connect() as c:integrity=c.execute('PRAGMA integrity_check').fetchone()[0]
 return {'objects':n,'bytes':bytes_,'full_hash_verification':full,'sqlite_integrity':integrity,'errors':errors,'scientific_validation':False}

def restore(prefix,destination):
 dst=Path(destination).expanduser().resolve()
 if dst==ROOT or ROOT in dst.parents:raise ValueError('Restore into a separate new directory, not inside this knowledge store')
 if dst.exists() and any(dst.iterdir()):raise ValueError('Restore destination must be empty or new')
 dst.mkdir(parents=True,exist_ok=True);n=0
 with (ROOT/'indexes/files.jsonl').open() as f:
  for line in f:
   row=json.loads(line)
   if not row['path'].startswith(prefix):continue
   out=dst/row['path'];resolved=out.resolve()
   if dst not in resolved.parents:raise ValueError('Unsafe archived path')
   digest=row['sha256'];source=ROOT/'evidence/objects'/digest[:2]/digest[2:]
   out.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,out);out.chmod(row['mode']);n+=1
 return {'restored_files':n,'destination':str(dst),'source_changed':False}

def queue_next(topic=None,limit=5):
 queue=load('state/reading_queue.json')
 pending=[x for x in queue if x['reading_state']=='unread' and (not topic or topic in x['topics'])]
 pending.sort(key=lambda x:(x['priority'],x['id']))
 return {'remaining':len(pending),'items':pending[:limit],'meaning':'Reading is not proof reconstruction or scientific validation.'}

def mark(identifier,level,note):
 queue=load('state/reading_queue.json');found=False
 for x in queue:
  if x['id']==identifier:x['reading_state']=level;found=True;break
 if not found:raise ValueError('Unknown reading queue ID')
 (ROOT/'state/reading_queue.json').write_text(json.dumps(queue,ensure_ascii=False,indent=2)+'\n')
 with (ROOT/'state/reviews.jsonl').open('a') as f:f.write(json.dumps({'id':identifier,'level':level,'note':note},ensure_ascii=False)+'\n')
 return {'id':identifier,'reading_state':level,'scientific_status_unchanged':True}

class Handler(http.server.SimpleHTTPRequestHandler):
 def __init__(self,*a,**kw):super().__init__(*a,directory=str(ROOT),**kw)
 def do_GET(self):
  url=urlparse(self.path);query=parse_qs(url.query)
  if not url.path.startswith('/api/'):return super().do_GET()
  try:
   q=query.get('q',[''])[0];topic=query.get('topic',[None])[0]
   if url.path=='/api/search':data=search(q,min(20,int(query.get('limit',['6'])[0])),topic,query.get('history',['0'])[0]=='1')
   elif url.path=='/api/route':data=route(q,min(20,int(query.get('limit',['5'])[0])),topic,query.get('history',['0'])[0]=='1')
   elif url.path=='/api/packet':data=packet(q,min(50000,int(query.get('budget',['6000'])[0])),topic,max_bytes=int(query['max_bytes'][0]) if 'max_bytes' in query else None)
   elif url.path=='/api/read':data=read(query.get('id',[''])[0],int(query['start'][0]) if 'start' in query else None,int(query['end'][0]) if 'end' in query else None,int(query.get('max_bytes',['24000'])[0]))
   elif url.path=='/api/stats':data=load('indexes/BUILD.json')
   elif url.path=='/api/family':data=family(query.get('id',[''])[0])
   elif url.path=='/api/sources':data=sources(q,min(20,int(query.get('limit',['6'])[0])))
   elif url.path=='/api/asset':data=asset(query.get('id',[''])[0])
   elif url.path=='/api/status':data=decision.resolve(query.get('id',[''])[0])
   elif url.path=='/api/lemmas':data=decision.ranked('literature/LEMMA_ATLAS.jsonl',q,min(20,int(query.get('limit',['6'])[0])))
   else:raise ValueError('Unknown endpoint')
   body=json.dumps(data,ensure_ascii=False).encode();self.send_response(200);self.send_header('Content-Type','application/json; charset=utf-8');self.send_header('Content-Length',str(len(body)));self.end_headers();self.wfile.write(body)
  except Exception as e:
   body=json.dumps({'error':str(e)}).encode();self.send_response(400);self.send_header('Content-Type','application/json');self.end_headers();self.wfile.write(body)

def main():
 p=argparse.ArgumentParser(description=__doc__);sub=p.add_subparsers(dest='command',required=True)
 sub.add_parser('stats')
 for cmd in ['search','packet']:
  s=sub.add_parser(cmd);s.add_argument('query');s.add_argument('--topic');s.add_argument('--history',action='store_true')
  if cmd=='search':s.add_argument('--limit',type=int,default=6)
  else:s.add_argument('--budget',type=int,default=6000);s.add_argument('--max-bytes',type=int);s.add_argument('--json',action='store_true')
 s=sub.add_parser('route');s.add_argument('query');s.add_argument('--topic');s.add_argument('--history',action='store_true');s.add_argument('--limit',type=int,default=5)
 s=sub.add_parser('read');s.add_argument('id');s.add_argument('--start',type=int);s.add_argument('--end',type=int);s.add_argument('--max-bytes',type=int,default=24000)
 s=sub.add_parser('links');s.add_argument('id')
 s=sub.add_parser('family');s.add_argument('id')
 s=sub.add_parser('sources');s.add_argument('query');s.add_argument('--limit',type=int,default=6)
 s=sub.add_parser('status');s.add_argument('id')
 for cmd,path in [('lemmas','literature/LEMMA_ATLAS.jsonl'),('gates','frontier/OPEN_PROOF_GATES.jsonl')]:
  s=sub.add_parser(cmd);s.add_argument('query');s.add_argument('--limit',type=int,default=6)
 s=sub.add_parser('asset');s.add_argument('id')
 s=sub.add_parser('verify');s.add_argument('--full',action='store_true')
 s=sub.add_parser('restore');s.add_argument('--prefix',default='literature/');s.add_argument('--dest',required=True)
 s=sub.add_parser('next');s.add_argument('--topic');s.add_argument('--limit',type=int,default=5)
 s=sub.add_parser('mark');s.add_argument('id');s.add_argument('--level',choices=['read','reconstructed','reviewed'],required=True);s.add_argument('--note',required=True)
 s=sub.add_parser('serve');s.add_argument('--host',default='127.0.0.1');s.add_argument('--port',type=int,default=8765)
 a=p.parse_args()
 if a.command=='stats':jprint(load('indexes/BUILD.json'))
 elif a.command=='search':jprint(search(a.query,a.limit,a.topic,a.history))
 elif a.command=='packet':
  v=packet(a.query,a.budget,a.topic,a.history,a.max_bytes);jprint(v) if a.json else sys.stdout.write(v['text'])
 elif a.command=='route':jprint(route(a.query,a.limit,a.topic,a.history))
 elif a.command=='read':jprint(read(a.id,a.start,a.end,a.max_bytes))
 elif a.command=='links':jprint(links(a.id))
 elif a.command=='family':jprint(family(a.id))
 elif a.command=='sources':jprint(sources(a.query,a.limit))
 elif a.command=='status':jprint(decision.resolve(a.id))
 elif a.command in ('lemmas','gates'):jprint(decision.ranked('literature/LEMMA_ATLAS.jsonl' if a.command=='lemmas' else 'frontier/OPEN_PROOF_GATES.jsonl',a.query,a.limit))
 elif a.command=='asset':jprint(asset(a.id))
 elif a.command=='verify':
  v=verify(a.full);jprint(v)
  if v['errors'] or v['sqlite_integrity']!='ok':sys.exit(1)
 elif a.command=='restore':jprint(restore(a.prefix,a.dest))
 elif a.command=='next':jprint(queue_next(a.topic,a.limit))
 elif a.command=='mark':jprint(mark(a.id,a.level,a.note))
 elif a.command=='serve':
  print(f'Knowledge index: http://{a.host}:{a.port}/web/index.html',flush=True)
  http.server.ThreadingHTTPServer((a.host,a.port),Handler).serve_forever()

if __name__=='__main__':
 try:main()
 except (ValueError,sqlite3.Error) as e:print(json.dumps({'error':str(e)}));sys.exit(2)
