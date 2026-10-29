"""Independent word-Pauli enumeration for the specified Chao-Reichardt gadget.
No imports from author code. Projective phases cannot change stabilizer cosets.
"""
from pathlib import Path
from itertools import product
import json,hashlib
D=Path(__file__).parent
P='IXZY'; G=['XZZXI','IXZZX','XIXZZ','ZXIXZ']; zero=(0,)*7
word=lambda t:tuple(P.index(c) for c in t)+(0,)*(7-len(t))
mul=lambda a,b:tuple(x^y for x,y in zip(a,b))
stab={zero}
for g in G:stab|={mul(x,word(g)) for x in list(stab)}
canon=lambda x:min(mul(x,g) for g in stab)
def sy(e):return tuple(sum(((a&1)*(b>>1)+(a>>1)*(b&1)) for a,b in zip(e,word(g)))%2 for g in G)
def single(q,p):return tuple(p if j==q else 0 for j in range(7))
w1=[zero]+[single(q,p) for q in range(5) for p in [1,3,2]]
normal={sy(e):e for e in w1};correctable={canon(e) for e in w1}
def ops(k,flag):
 r=[('prepZ',(5,))]+([('prepX',(6,))] if flag else [])
 supp=[(i,p) for i,p in enumerate(G[k]) if p!='I']
 for n,(q,p) in enumerate(supp):
  if flag and n in [1,3]:r.append(('CX',(6,5)))
  if p=='X':r.append(('H',(q,)))
  r.append(('CX',(q,5)))
  if p=='X':r.append(('H',(q,)))
 return r+[('measureZ',(5,)),('readoutZ',(5,))]+([('measureX',(6,)),('readoutX',(6,))] if flag else [])
def variants(k,flag,tag):
 r=[]
 for j,(kind,qs) in enumerate(ops(k,flag)):
  loc=(tag,k,j,'gate')
  if kind.startswith(('measure','readout')):r.append((loc,None))
  else:
   for tup in product(range(4),repeat=len(qs)):
    if any(tup):r.append((loc,tuple(tup[qs.index(q)] if q in qs else 0 for q in range(7))))
  for q in range(7):
   if q not in qs:r.extend(((tag,k,j,'idle'+str(q)),single(q,p)) for p in [1,2,3])
 return r
def check(e,k,flag,tag,fault=None):
 e=list(e[:5])+[0,0];bits=[0,0]
 for j,(kind,qs) in enumerate(ops(k,flag)):
  if kind.startswith('prep'):e[qs[0]]=0
  elif kind=='H':
   q=qs[0];e[q]=((e[q]&1)<<1)|(e[q]>>1)
  elif kind=='CX':
   a,b=qs; xa,za=e[a]&1,e[a]>>1;xb,zb=e[b]&1,e[b]>>1
   e[a]=xa|((za^zb)<<1);e[b]=(xb^xa)|(zb<<1)
  elif kind=='measureZ':bits[0]=e[5]&1
  elif kind=='measureX':bits[1]=e[6]>>1
  if fault and fault[0]==(tag,k,j,'gate'):
   if fault[1] is None:bits[int(kind.endswith('X'))]^=1
   else:e=list(mul(e,fault[1]))
  if fault and fault[0][:3]==(tag,k,j) and fault[0][3].startswith('idle'):e=list(mul(e,fault[1]))
 return tuple(e[:5])+ (0,0),tuple(bits)
tables=[]
for k in range(4):
 t={}
 for f in variants(k,True,'F'):
  e,(s,b)=check(zero,k,True,'F',f)
  if b:
   syn=sy(e)
   if syn in t:assert canon(mul(e,t[syn]))==zero
   else:t[syn]=e
 tables.append(t)
def run(e=zero,fault=None):
 record=[]
 for k in range(4):
  e,(s,f)=check(e,k,True,'F',fault);record.append((k,s,f))
  if s or f:
   synd=[]
   for h in range(4):
    e,b=check(e,h,False,'U',fault);synd.append(b[0])
   record.append(('U',tuple(synd)))
   correction=(tables[k] if f else normal).get(tuple(synd))
   if correction is None:return None,record
   # Execute local correction gates, not an unexecuted tracked frame.
   for q,p in enumerate(correction[:5]):
    if not p:continue
    e=mul(e,single(q,p))
    if fault and fault[0]==('C',k,q,'gate'):e=mul(e,fault[1])
    if fault and fault[0][:3]==('C',k,q) and fault[0][3].startswith('idle'):e=mul(e,fault[1])
   return e[:5]+(0,0),record
 return e,record
assert len(normal)==16
for e in w1:assert canon(run(e)[0])==zero
# Stronger fault-free arbitrary Pauli input: result matches ideal syndrome recovery.
for xs in product(range(4),repeat=5):
 e=xs+(0,0);out,_=run(e);assert canon(out)==canon(mul(e,normal[sy(e)]))
faults=[f for k in range(4) for f in variants(k,True,'F')]
results=[]
for fault in faults:
 out,rec=run(fault=fault);assert out is not None and canon(out) in correctable
 results.append({'location':fault[0],'fault':fault[1],'output':''.join(P[x] for x in out[:5]),'record':rec})
# Compare saved author records independently, including branch outcomes, modulo stabilizers.
author=D/'flagged_five_qubit_storage_check_20261028.json';A=json.loads(author.read_text())
def fromint(e):return tuple(((e>>q)&1)|(((e>>(7+q))&1)<<1) for q in range(7))
lookup={(tuple(r['location']),None if r['fault'][0]=='flip' else fromint(r['fault'][1])):r for r in A['all_fault_results']}
for r in results:
 a=lookup[(tuple(r['location']),r['fault'])]
 assert canon(word(r['output']))==canon(word(a['output']))
 assert json.dumps(r['record'])==json.dumps(a['record'])
# Two-fault-domain negative control: an existing input error plus one EC fault need not work.
negative=None
for e in w1[1:]:
 for f in faults:
  out,rec=run(e,f)
  if out is None or canon(out) not in correctable:
   negative={'input':''.join(P[x] for x in e[:5]),'fault_location':f[0],'fault_word':f[1],'residual':None if out is None else ''.join(P[x] for x in out[:5]),'record':rec};break
 if negative:break
assert negative is not None
def locations(oplist):return sum(1+7-len(qs) for kind,qs in oplist)
flag_locations=[locations(ops(k,True)) for k in range(4)]
plain_locations=[locations(ops(k,False)) for k in range(4)]
assert flag_locations==[106]*4 and plain_locations==[73]*4
maxcor=max(sum(bool(p) for p in e[:5]) for t in tables for e in t.values())
assert maxcor==3
assert sum(flag_locations+plain_locations)+7*maxcor==737
assert sum(len(ops(k,True))+len(ops(k,False)) for k in range(4))+maxcor==111
out={'status':'PASS_INDEPENDENT_SINGLE_FAULT_GADGET_ENUMERATION','one_error_faultfree_cases':16,'all_Pauli_input_faultfree_cases':1024,'clean_input_single_fault_cases':len(results),'record_comparisons':len(results),'flag_table_sizes':list(map(len,tables)),'outside_claim_two_fault_counterexample':negative,'scope':'Exact Pauli propagation with executed conditional physical corrections; correction-fault branches unreachable as sole clean-input fault. Coherent extension and one-cycle bound independently reviewed in receipt','conservative_max_locations':737,'conservative_max_serial_slots':111,'bindings':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),author,D/'flagged_five_qubit_storage_check_20261028.py',D/'flagged_five_qubit_storage_round_20261028.md']}}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
