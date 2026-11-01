from pathlib import Path
from fractions import Fraction as Q
import os,sys,json,hashlib,time
import independent_glue_receiver as I
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent;SOURCE=Path(os.environ.get('GLUE_SOURCE_DIR',(ROOT if (ROOT/'free_port_glue.py').is_file() else ROOT/'stochastic_free_port_glue_pending_20261031'))).resolve();OUT=Path(os.environ.get('AUDIT_OUTPUT_DIR',HERE)).resolve();OUT.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(SOURCE));import free_port_glue as G
start=time.monotonic();raw=G.fixture();c=G.construct(raw,2);serialized=I.canonical(c);received=json.loads(serialized)
assert I.receive_symbolic(raw,2,received)
for path in [('core_profile','head'),('free_profile','head'),('symbolic_head','coefficients')]:
 bad=json.loads(serialized);bad[path[0]][path[1]][0]='0';assert not I.receive_symbolic(raw,2,bad)
def forbidden(*args,**kwargs):raise AssertionError('exhaustive numerical/cover path called')
old=[(G.C.B,'covers',G.C.B.covers),(G.C.B,'numerical',G.C.B.numerical),(G.C,'numerical',G.C.numerical),(I.B,'minimal_covers',I.B.minimal_covers),(I.B,'numerical',I.B.numerical),(I.C,'numerical',I.C.numerical)]
for mod,key,fn in old:setattr(mod,key,forbidden)
assert I.canonical(I.construct(raw,2))==serialized==I.canonical(G.construct(raw,2))
for mod,key,fn in old:setattr(mod,key,fn)
manifest=SOURCE/'frozen_core'/'AUTHOR_MANIFEST.json';assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='64be3db4d97541eef968548572887f3f518c3e3343377a05c07e693ab26cb60d'
bindings=json.loads(manifest.read_text())['files'];verified={}
for name,v in bindings.items():
 data=(manifest.parent/name).read_bytes();assert hashlib.sha256(data).hexdigest()==v['sha256'];verified[name]=v['sha256']
for name,expected in [('independent_cover_receiver.py','c27b66670ae529ea74c9b5f99b321e7d183007a8f826f3698ad85cb37ce506ee'),('independent_circuit_receiver.py','87b635fd6809eb24d4a31f364f7915e6e72b782a9eb16db9dfe3a78930a98c09')]:
 assert hashlib.sha256((HERE/'prior_independent'/name).read_bytes()).hexdigest()==expected;verified['prior_independent/'+name]=expected
# Reference-independent dyadic/log boundaries with large numerator/denominator inputs.
logchecks=0
for e in (-10000,-200,-1,0,1,200,10000):
 v=Q(1<<e)if e>=0 else Q(1,1<<(-e))
 for q in (v,v*Q(3,2),v*Q(3,4)):
  got=I.logceil(q);assert got==G.ceil_log2(q)
  lower=Q(1<<got)if got>=0 else Q(1,1<<(-got));assert lower/2<q<=lower;logchecks+=1
for e in (0,1,2,10,100,10000):
 for z in set(max(1,(1<<e)+i)for i in (-1,0,1)):
  assert I.dyadic(z)==G.dyadic(z)
  assert 0<=I.dyadic(z+1)-I.dyadic(z)<=Q(2,z);logchecks+=1
result=dict(status='PASS',seconds=time.monotonic()-start,wire_bytes=len(serialized.encode()),wire_sha256=hashlib.sha256(serialized.encode()).hexdigest(),wire_mutations=3,disabled_exhaustive_entrypoints=6,production_constructs_with_disabled_exhaustive=2,dyadic_log_checks=logchecks,source_hashes=verified,scope='Retained accepted core and prior independent primitives hash-verified; no candidate imports in receiver; fresh glue implementation reacquires all new quantities.')
(OUT/'WIRE_DEPENDENCY_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
