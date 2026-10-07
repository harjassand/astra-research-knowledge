"""Bounded packet adapter. No gold labels are accepted by this module."""
from pathlib import Path
import importlib.util,sys,re
ROOT=Path(__file__).resolve().parents[2]/'outputs/ASTRA_KNOWLEDGE'
sys.path.insert(0,str(ROOT/'tools'))
import knowledge
import bundle

def packet_result(text):
 ids=[];bodies={}
 # Only actual emitted blocks are used; pointer/omission mentions never count.
 for attrs,body in re.findall(r'<BLOCK\b([^>]*)>\n(.*?)</BLOCK>',text,re.S):
  p=re.search(r'path="([^"]+)"',attrs)
  if p and p[1].startswith('cards/'):
   cid=Path(p[1]).stem;ids.append(cid);bodies[cid]=body
 return {'text':text,'included_card_ids':sorted(set(ids)),'card_bodies':bodies}

def enhanced(payload):
 out={}
 for task in payload['tasks']:
  v=knowledge.packet(task['query'],budget=payload['max_tokens'],max_bytes=payload['max_bytes'])
  out[task['id']]=packet_result(v['text'])
 return {'packets':out}

def bundled(payload):
 out={}
 for task in payload['tasks']:
  v=bundle.make_bundle(task['query'],budget=payload['max_tokens'],max_bytes=payload['max_bytes'])
  bodies={}
  for attrs,body in re.findall(r'<CARD\b([^>]*)>\n(.*?)</CARD>',v['text'],re.S):
   m=re.search(r'id="([^"]+)"',attrs)
   if m:bodies[m[1]]=body
  assert set(bodies)==set(v['selected_ids'])
  # Full-card bytes must actually occur inside the corresponding block.
  for cid,body in bodies.items():assert (ROOT/'cards'/f'{cid}.txt').read_text() in body
  out[task['id']]={'text':v['text'],'included_card_ids':sorted(bodies),'card_bodies':bodies}
 return {'packets':out}
