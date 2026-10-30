"""Finite actual-label and quantum-algebra regressions; not threshold simulations."""
from pathlib import Path
from itertools import product
from collections import Counter
import numpy as np, json
ROOT=Path('producer-workspace/shared')
src=(ROOT/'native_locc_rollback_integration_20261030/check_extended_owner_table.py').read_text().split('states=list(product(')[0]
src=src.replace("if l=='f':continue", "if l in {'f','e'}:continue")
ns={};exec(src,ns)
oldviolates=ns['violates']; oldtrans=ns['trans']
ns['violates']=lambda h,p,j,l: False if p[0]=='PARK' else oldviolates(h,p,j,l)
phases=[p+[('PARK',0)] for p in ns['phases']]
locks=[p+('e',) for p in ns['lockoptions']]
nstates=nedges=natomic=0; counts=Counter()
def trans(s,pauses):
 for ss,kind,coh in oldtrans(s):
  h=next((h for h in range(2) if s[0][h]!=ss[0][h]),None)
  if kind=='load_reset' and pauses[h]:continue
  if kind=='ready_reset' and pauses[h]:ss=ns['ch'](ss,h,('PARK',0))
  yield ss,kind,coh
 for h,p in enumerate(s[0]):
  if p[0]=='PARK':
   if pauses[h]:yield s,'quiescent_reset',False
   else:yield ns['ch'](s,h,('Q',0)),'unpark_reset',False
 for x,l in enumerate(s[1]):
  if l=='f':yield ns['ch'](s,q=x,l='e'),'atomic_FREE_ERASE',False
  if l=='e':yield ns['ch'](s,q=x,l='f'),'erasure_tag_cleanup',False
for pauses in product((0,1),repeat=2):
 for ps in product(*phases):
  for ls in product(*locks):
   s=(ps,ls);nstates+=1
   before=tuple(ns['flag'](h,ps[h],ls) for h in range(2))
   for ss,kind,coh in trans(s,pauses):
    nedges+=1;counts[kind]+=1
    after=tuple(ns['flag'](h,ss[0][h],ss[1]) for h in range(2))
    assert before==after if coh else all(a<=b for a,b in zip(after,before)),(s,ss,kind)
    if kind in {'atomic_FREE_ERASE','erasure_tag_cleanup'}:
     natomic+=1;assert before==after
     for h in range(2):
      assert tuple(l==f'o{h}' for l in ls)==tuple(l==f'o{h}' for l in ss[1])
      assert tuple(l==f'z{h}' for l in ls)==tuple(l==f'z{h}' for l in ss[1])
    if kind=='acquire':assert 'e' not in [ls[q] for q in range(3) if ls[q]!=ss[1][q]]
# Small complete SEAL predicate graph. Native PARK/W modeled as three states:
# active, PARK dirty, PARK W0; arbitrary transitions outside held PARK are allowed.
d=2
aph=[('IDLE',),('S',0),('S',1),('S',2)]+[('E',j,b) for j in range(d) for b in (0,1)]+[('V',j) for j in range(d+1)]+[('H',),('R',0),('R',1),('R',2)]+[('F',j,b) for j in range(d) for b in (0,1)]
def cert(c,p,w):
 t=c[0]
 if t in {'IDLE','R','F'}:return True
 if t=='S':return all(p[k] for k in range(c[1]))
 if t=='E':return all(p[k] for k in range(c[1]+1))
 if t in {'V','H'}:
  j=c[1] if t=='V' else d
  return all(p) and all(w[k]==2 for k in range(j))
 raise ValueError(c)
def change(s,c=None,p=None,w=None,a=None):return (s[0] if c is None else c,s[1] if p is None else p,s[2] if w is None else w,s[3] if a is None else a)
def setp(s,j,b):
 p=list(s[1]);p[j]=b;return tuple(p)
def adedges(s):
 c,p,w,a=s;t=c[0]
 if t!='IDLE':yield change(s,c=('S',0),a=0),'SEAL',False
 if t=='IDLE':yield change(s,c=('S',0),a=1),'consume_command',False
 if t=='S':
  j=c[1]
  if j<d:yield change(s,c=('E',j,p[j]),p=setp(s,j,1)),'assert',True
  else:yield change(s,c=('V',0)),'begin_verify',False
 if t=='E':
  j,b=c[1:]
  if p[j]==1:yield change(s,c=('S',j),p=setp(s,j,b)),'assert_reverse',True
  yield change(s,c=('S',j+1)),'assert_commit',False
 if t=='V':
  j=c[1]
  if j<d and w[j]==2:yield change(s,c=('V',j+1)),'live_verify',True
  if j>0 and w[j-1]==2:yield change(s,c=('V',j-1)),'live_unverify',True
  if j==d:yield change(s,c=('H',)),'hold',False
 if t=='H':
  if a:yield change(s,c=('S',0),a=0),'ERASE',False # maximal source: FREE guard only restricts further
  yield change(s,c=('R',0),a=0),'begin_release',False
 if t=='R':
  j=c[1]
  if j<d:yield change(s,c=('F',j,p[j]),p=setp(s,j,0)),'clear',True
  else:yield change(s,c=('IDLE',),a=0),'idle',False
 if t=='F':
  j,b=c[1:]
  if p[j]==0:yield change(s,c=('R',j),p=setp(s,j,b)),'clear_reverse',True
  yield change(s,c=('R',j+1)),'clear_commit',False
 for j in range(d):
  # held PARK W0 cannot leave; PARK dirty only refreshes. Active can retire.
  choices=(w[j],2) if p[j] and w[j] in (1,2) else (0,1,2)
  for z in choices:
   ww=list(w);ww[j]=z
   yield change(s,w=tuple(ww)),'native',False
acount=Counter();astates=bad=0
for s in product(aph,product((0,1),repeat=d),product(range(3),repeat=d),(0,1)):
 astates+=1;before=cert(*s[:3]);bad+=not before
 for ss,k,coh in adedges(s):
  after=cert(*ss[:3]);acount[k]+=1
  assert before==after if coh else (not before or after),(s,ss,k,before,after)
  if k in {'SEAL','ERASE'}:assert after
 assert before or s[0][0]!='IDLE'
# Quantum ownership-deleted forests, arbitrary unitaries on hub W + resource.
rng=np.random.default_rng(87123)
def haar(n):
 z=rng.normal(size=(n,n))+1j*rng.normal(size=(n,n));q,r=np.linalg.qr(z);return q@np.diag(np.diag(r)/np.abs(np.diag(r))).conj()
def embed2(u,q1,q2):
 out=np.zeros((8,8),complex)
 for a in range(8):
  aa=[(a>>i)&1 for i in range(3)]
  for c in range(4):
   bb=aa.copy();bb[q1]=c&1;bb[q2]=(c>>1)&1
   b=sum(v<<i for i,v in enumerate(bb));inp=aa[q1]+2*aa[q2];out[b,a]=u[c,inp]
 return out
# q0,q1 resource DATA, q2 private W.
targets=(0,1,1,0,1);U=[embed2(haar(4),2,t) for t in targets]
Fcases=0;err=0;bad_unguarded=0
for mask in product((0,1),repeat=2):
 F=[np.eye(8,dtype=complex)]
 for u,t in zip(U,targets):F.append(u@F[-1] if mask[t] else np.eye(8,dtype=complex))
 for x in range(2):
  if mask[x]:continue
  for f in F:
   for b in (0,1):
    k=np.zeros((8,8),complex)
    for a in range(8):
     if ((a>>x)&1)==b:k[a&~(1<<x),a]=1
    err=max(err,float(np.linalg.norm(f.conj().T@k@f-k,2)));Fcases+=1
# Preserve old counterexample with absent tag guard: CNOT DATA0 -> W2.
cnot=np.zeros((8,8))
for a in range(8):cnot[a^(4 if a&1 else 0),a]=1
w0=np.diag([1 if not a&4 else 0 for a in range(8)])
good=cnot@w0@cnot.T;v=np.zeros(8);v[5]=1 # D0=1,W=1 after prefix
k=np.zeros((8,8))
for a in range(8):
 if a&1:k[a&~1,a]=1
bad_unguarded=float(np.linalg.norm((np.eye(8)-good)@k@v)**2)
assert err<1e-12 and bad_unguarded==1
out={'actual_native_tag_states_all_pause_masks':nstates,'actual_native_directed_edges':nedges,'atomic_tag_edges':natomic,'tag_counts':dict(counts),'native_structural_no_creation':True,'all_own_o_z_masks_preserved_by_ERASE_and_cleanup':True,'seal_certificate_states':astates,'seal_certificate_bad_states':bad,'seal_graph_edges':dict(acount),'seal_no_creation_and_full_target_healing':True,'quantum_forest_cases':Fcases,'maximum_quantum_forest_intertwiner_error':err,'preserved_unguarded_prefix_error':bad_unguarded,'scope':'actual native label table plus finite SEAL predicate graph and random-unitary full-workspace algebra fixtures; no finite-path probability or QCA threshold simulation'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
