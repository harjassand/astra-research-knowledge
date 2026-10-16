"""Pinned-only bounded payload acquisition; no decoding; durable cumulative ledger."""
import concurrent.futures,hashlib,json,pathlib,threading,time,urllib.request
ROOT=pathlib.Path(__file__).resolve().parent
MAN=pathlib.Path('/workspace/shared/stm_prediction_protocol/split_manifest.json')
CAP=350_000_000
lock=threading.Lock(); stop=threading.Event()
ledger_path=ROOT/'acquisition_ledger.json'
ledger=json.loads(ledger_path.read_text()) if ledger_path.exists() else {'received_payload_bytes':0,'attempts':[],'verified':{}}
def save():
 p=ledger_path.with_suffix('.tmp');p.write_text(json.dumps(ledger,indent=2));p.replace(ledger_path)
def fetch(item):
 eid=str(item['episode_id']); out=ROOT/'acquired'/f'{int(eid):05d}.npy'
 with lock:
  if eid in ledger['verified']:
   b=out.read_bytes()
   if len(b)!=item['bytes'] or hashlib.sha256(b).hexdigest()!=ledger['verified'][eid]['sha256']:raise RuntimeError('Existing verified file changed')
   return
  if stop.is_set():return
  # Reserve full expected response before each stream. No retry or range requests.
  reserved=sum(a['reserved_remaining'] for a in ledger['attempts'])
  if ledger['received_payload_bytes']+reserved+item['bytes']+1>CAP:raise RuntimeError('Budget reservation failed')
  a={'episode_id':int(eid),'received':0,'reserved_remaining':item['bytes']+1,'status':'started'};ledger['attempts'].append(a);save()
 url=f"https://raw.githubusercontent.com/SINGROUP/Atom_manipulation_with_RL/{manifest['commit']}/{item['path']}"
 chunks=[]
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'Accept-Encoding':'identity'}),timeout=120) as r:
   if r.status!=200:raise RuntimeError('HTTP status')
   while True:
    # At most expected+1 bytes consumed, then abort mismatch.
    b=r.read(min(65536,item['bytes']+1-a['received']))
    if not b:break
    with lock:
     ledger['received_payload_bytes']+=len(b);a['received']+=len(b);a['reserved_remaining']-=len(b);save()
    chunks.append(b)
    if a['received']>item['bytes']:raise RuntimeError('Payload exceeds expected size')
  b=b''.join(chunks)
  sha1=hashlib.sha1(f'blob {len(b)}\0'.encode()+b).hexdigest();sha256=hashlib.sha256(b).hexdigest()
  if len(b)!=item['bytes'] or sha1!=item['git_blob_sha1']:raise RuntimeError('Size or Git blob hash mismatch')
  out.write_bytes(b)
  with lock:
   a.update(status='verified',reserved_remaining=0);ledger['verified'][eid]={'bytes':len(b),'git_blob_sha1':sha1,'sha256':sha256,'source_url':url};save()
 except Exception as e:
  stop.set()
  with lock:a.update(status='failed',error=type(e).__name__+': '+str(e),reserved_remaining=0);save()
  raise
manifest=json.loads(MAN.read_text())
items=[dict(e,split=s) for s,part in manifest['splits'].items() for e in part['episodes']]
if len(items)!=220 or sum(e['bytes'] for e in items)!=210_440_337:raise RuntimeError('Manifest totals changed')
if any(a['status']=='started' for a in ledger['attempts']):raise RuntimeError('Interrupted ledger: manual audit required, no automatic retry')
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
 futures=[pool.submit(fetch,e) for e in items]
 for f in concurrent.futures.as_completed(futures):
  f.result()
  n=len(ledger['verified'])
  if n%20==0:print(f'Verified {n}/220; cumulative received {ledger["received_payload_bytes"]}',flush=True)
print(json.dumps({'verified_files':len(ledger['verified']),'received_payload_bytes':ledger['received_payload_bytes']}))
