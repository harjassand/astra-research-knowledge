import sys,json,hashlib,gzip,random,itertools,time
from pathlib import Path
from fractions import Fraction as F
from math import isqrt
P=Path(__file__).resolve().parent.parent;sys.path.insert(0,str(P))
from finite_povm_synthesis_v1 import C,Z,O,eye,mm,adj,target_matrix
from finite_pruned_receiver_v1 import enumerate_exact,compact_default,prune,draw_below
import numpy as np
R={'status':'RUNNING','checks':[]}; OUT=Path(__file__).parent

def emit(s):
 R['checks'].append(s);print(s,flush=True);(OUT/'results.json').write_text(json.dumps(R,indent=2)+'\n')
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
manifest=json.loads((P/'PRUNING_CONTROL_REVIEW_INPUTS_v1.json').read_text())
for r in manifest['files']:
 p=P/r['path'];assert p.stat().st_size==r['bytes'] and digest(p)==r['sha256']
R['manifest_sha256']=digest(P/'PRUNING_CONTROL_REVIEW_INPUTS_v1.json');R['files']=manifest['files'];R['dependencies']={}
for p in [P/'certified_projection_v1.py']+list(P.glob('memory_certificates_seed*_N4096_v2.json.gz'))+list(P.glob('memory_records_seed*_N4096_v2.npy')):R['dependencies'][p.name]=digest(p)
emit('All 15 frozen file hashes and sizes verified; supplemental dependency hashes recorded.')
pruned=json.loads((P/'check_pruned_receiver_v1.json').read_text())['runs']
for r in pruned:
 seed=r['seed']
 with gzip.open(P/f'memory_certificates_seed{seed}_N4096_v2.json.gz','rt') as f:E=[[F(x) for x in v] for v in json.load(f)[-1]['output_E']]
 assert len(E)==9 and all(v[0]>=0 and v[0]**2>=sum(x*x for x in v[1:]) for v in E)
 assert [sum(v[j] for v in E) for j in range(4)]==[1,0,0,0]
 leaves=list(enumerate_exact(E));assert len(leaves)==32 and sum(p for p,w in leaves)==1
 for p,w in leaves:
  assert p>0 and sum(x>0 for x in w)==4
  assert all(x>=0 for x in w)
  assert [sum(w[i]*E[i][j] for i in range(9)) for j in range(4)]==[1,0,0,0]
 assert all(sum(p*w[i]*E[i][j] for p,w in leaves)==E[i][j] for i in range(9) for j in range(4))
 known=list(dict.fromkeys(int(x[2]) for x in np.load(P/f'memory_records_seed{seed}_N4096_v2.npy')))
 labels,cols,ds=compact_default(known,E,16,random.Random(seed));out,st=prune(labels,cols,random.Random(seed+1))
 assert [a for a,e in out]==r['sampled_output_labels'] and [[str(x) for x in e] for a,e in out]==r['sampled_output_effects']
 assert st['draws']==5 and ds['draws']==1 and F(r['whole_channel_coupling_bound'])==F(6,2**128)
 emit(f'Pruning seed {seed}: all 32 leaves physical, exact mean identity, sampled effects reproduced; deterministic six-draw cap bound verified.')
class Fixed:
 def __init__(self,x):self.x=x
 def getrandbits(self,b):return self.x
for A in range(1,11):
 for n in range(A):
  for known in itertools.combinations(range(A),n):
   actual=[compact_default(known,[],A,Fixed(k))[0][-1] for k in range(A-n)]
   assert actual==[a for a in range(A) if a not in known]
for d in range(1,100):
 b=(d-1).bit_length();assert F(2**b-d,2**b)<F(1,2)
 if 2**b>d:assert draw_below(d,Fixed(2**b-1))==(0,True,128*b)
emit('Default rank map exhaustively checked for every proper observed subset of alphabets 1..10; rejection failure law and forced-cap fallback checked.')
def parse(z):return C(F(z[0]),F(z[1]))
def mat(raw):return [[parse(z) for z in row] for row in raw]
def rows(U,indices,M):
 old=[U[i][:] for i in indices]
 for i,row in zip(indices,mm(M,old)):U[i]=row

def primitive_matrix(p):
 U=eye(8);a=sum(v<<j for j,v in p['controls']);rows(U,[a,a|(1<<p['target'])],mat(p['matrix']));return U

def local(U,g):
 t=g['target'];assert 0<=t<3
 if g['kind']=='single':
  M=mat(g['matrix']);assert mm(adj(M),M)==eye(2)
  for a in range(8):
   if not a&(1<<t):rows(U,[a,a|(1<<t)],M)
 else:
  assert g['kind']=='cnot';c=g['control'];assert c!=t and 0<=c<3
  for a in range(8):
   if a&(1<<c) and not a&(1<<t):U[a],U[a|(1<<t)]=U[a|(1<<t)],U[a]

def upper(x):
 d=2**128;n=isqrt(x.numerator*d*d//x.denominator);lo=F(n,d);hi=lo if lo*lo==x else F(n+1,d);assert lo*lo<=x<=hi*hi;return hi
# Only obtain the pure Gray-path expansion, no import-time writers.
ns={};exec(compile((P/'compile_controlled_primitives_v2.py').read_text().split('P=Path(__file__)')[0],'<pure expansion>','exec'),ns)
for mode,filename in [('thin','thin_isometry_receiver_v4.json'),('full','check_povm_synthesis_v1.json')]:
 src=json.loads((P/filename).read_text())['runs'];localsrc=json.loads((P/'compile_local_controls_v3.json').read_text())['runs']
 for idx,r in enumerate(src):
  gates=r['two_level_gates'] if mode=='thin' else r['gates'];U=eye(8);compiled=eye(8);ps=[]
  for g in gates:
   if g['kind']=='basis_phase':
    z=parse(g['phase']);assert z.norm2()==1;U[g['basis']]=[z*x for x in U[g['basis']]]
   else:
    M=mat(g['matrix']);assert mm(adj(M),M)==eye(2);rows(U,g['basis'],M)
   for p in ns['expand'](g):
    ps.append(p);a=sum(v<<j for j,v in p['controls']);rows(compiled,[a,a|(1<<p['target'])],mat(p['matrix']))
  assert U==compiled
  if mode=='full':
   savedps=json.loads((P/'compile_controlled_primitives_v2.json').read_text())['runs'][idx]
   assert ps==savedps['primitives'] and savedps['labels']==r['labels']
  effects=pruned[idx]['sampled_output_effects'];eb=[]
  for a in range(4):
   B=[row[:2] for row in U[2*a:2*a+2]];actual=mm(adj(B),B);target=target_matrix([F(x) for x in effects[a]])
   eb.append(upper(sum((actual[i][j]-target[i][j]).norm2() for i in range(2) for j in range(2))))
  ideal=sum(eb)/2;assert ideal==F(r['ideal_dilation_half_diamond_upper' if mode=='thin' else 'correction_channel_half_diamond_upper'])
  lr=r if mode=='thin' else localsrc[idx];lg=lr['local_gates'] if mode=='thin' else lr['gates'];cursor=0;bounds=[]
  for p in ps:
   # A CC-U uses three 8-gate CV blocks, 2 CXs, and 2 Xs per negative control.
   n=26+2*sum(v==0 for j,v in p['controls']);chunk=lg[cursor:cursor+n];assert len(chunk)==n;cursor+=n
   W=eye(8)
   for g in chunk:local(W,g)
   T=primitive_matrix(p);bounds.append(upper(sum((W[i][j]-T[i][j]).norm2() for i in range(8) for j in range(8))))
  assert cursor==len(lg)
  total=ideal+sum(bounds);assert total==F(lr['total_correction_channel_half_diamond_upper'])
  if mode=='thin':assert len(ps)==31 and sum(g['kind']=='cnot' for g in lg)==248 and sum(g['kind']=='single' for g in lg)==646 and total<=F('4.277e-13')
  else:assert len(ps)==68 and sum(g['kind']=='cnot' for g in lg)==544 and sum(g['kind']=='single' for g in lg)==1384
  emit(f'{mode} seed {r["seed"]}: exact gate unitarity, Gray expansion equality, four exact effect error bounds, every local primitive residual and telescoped total verified: {float(total):.17g}.')
for record in manifest['files']:
 assert digest(P/record['path'])==record['sha256']
R['status']='PASS_SCOPED_INDEPENDENT_REPLAY';emit('All requested saved circuit checks complete; no source/test output modified.')
