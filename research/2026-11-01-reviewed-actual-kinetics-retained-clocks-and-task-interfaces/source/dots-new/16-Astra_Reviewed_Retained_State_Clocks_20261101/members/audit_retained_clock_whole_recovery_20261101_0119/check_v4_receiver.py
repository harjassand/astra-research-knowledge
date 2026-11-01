from pathlib import Path
from fractions import Fraction as F
from copy import deepcopy
import ast,importlib.util,json,random,time
H=Path(__file__).resolve().parent;S=H/'replay_v4/retained_state_renewal_clock_20261101';spec=importlib.util.spec_from_file_location('v4',S/'receive_clock.py');c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c);checks=0;cats={};reasons=[];start=time.perf_counter()
def ok(a,k):
 global checks
 assert a,k
 checks+=1;cats[k]=cats.get(k,0)+1

def no(f,k):
 try:f()
 except c.Unknown as e:reasons.append({'test':k,'reason':str(e)});ok(True,k)
 else:raise AssertionError('false admit '+k)
old=ast.parse((H/'replay/retained_state_renewal_clock_20261101/receive_clock.py').read_text());new=ast.parse((S/'receive_clock.py').read_text());new.body=[n for n in new.body if not(isinstance(n,ast.FunctionDef)and n.name=='guard_certificate_tree')]
for n in new.body:
 if isinstance(n,ast.FunctionDef)and n.name=='verify':n.body=n.body[2:]
ok(ast.dump(old)==ast.dump(new),'exact AST unchanged except preflight guard and two added verify statements')
original=c.certify
calls=[]
def forbid(*a,**k):calls.append(1);raise AssertionError('malformed reached expensive scalar producer')
c.certify=forbid
bad=[]
for depth in [65,100,1100,10000]:
 z=0
 for _ in range(depth):z={'child':z}
 bad.append(z)
z={};z['cycle']=z;bad.append(z);z=[];z.append(z);bad.append({'cycle':z});z=[];bad.append({'left':z,'right':z})
bad += [{1:'nonstring'}, {'bad':F(1)}, {'bad':(1,2)}, {'bad':bytearray(b'1')}, {'bad':object()}, {'big':[0]*100001}, {str(i):0 for i in range(100001)}, None,[],True,1,'x']
for z in bad:no(lambda z=z:c.verify({},z),'malformed bounded proof tree UNKNOWN before recomputation')
ok(not calls,'no malformed guard path performed raw/scalar recomputation');c.certify=original
for depth in [0,1,32,63,64]:
 z=0
 for _ in range(depth):z=[z]
 stats=c.guard_certificate_tree(z);ok(stats['proof_nodes']==depth+1,'exact permitted depth boundary')
for n in [1,2,10,100,100000]:
 z=[0]*(n-1);stats=c.guard_certificate_tree(z,max_nodes=n);ok(stats['proof_nodes']==n and stats['maximum_pending_nodes']<=n,'exact visited plus pending node bound admits')
 if n>1:no(lambda z=z,n=n:c.guard_certificate_tree(z,max_nodes=n-1),'one below visited plus pending budget refuses')
for z,n in [([[0,0],[0,0]],6),({'a':[0,0],'b':[0,0]},6),({'seconds':0,'work':0,'display':0},2)]:no(lambda z=z,n=n:c.guard_certificate_tree(z,max_nodes=n),'queued-node and ignored-key scan explicitly charged')
rng=random.Random(110126)
def tree(depth=0):
 if depth>=4 or rng.randrange(4)==0:return rng.choice([None,True,False,0,1,'leaf',0.5])
 if rng.randrange(2):return [tree(depth+1)for _ in range(rng.randrange(4))]
 z={str(i):tree(depth+1)for i in range(rng.randrange(4))}
 if rng.randrange(3)==0:z['work']=object()
 return z

def count(z):
 if type(z)is dict:
  a=[count(v)for k,v in z.items()if k not in ['work','seconds','display']];return 1+sum(x for x,y in a),len(z)+sum(y for x,y in a)
 if type(z)is list:
  a=[count(v)for v in z];return 1+sum(x for x,y in a),sum(y for x,y in a)
 return 1,0
for i in range(250):
 z=tree();nodes,keys=count(z);limit=max(nodes,keys);s=c.guard_certificate_tree(z,max_nodes=limit)
 ok(s['proof_nodes']==nodes and s['keys_scanned']==keys,'independent tree node/key accounting')
 ok(1<=s['maximum_pending_nodes']<=limit,'pending allocation bounded by global finite budget')
 if limit>1:no(lambda z=z,limit=limit:c.guard_certificate_tree(z,max_nodes=limit-1),'tree minimal combined node/key limit')
small=json.loads((H/'independent_small_certificate.json').read_text());raw=json.loads((H/'independent_small_raw.json').read_text());t=c.external_from_record(small)
ok(c.verify(raw,small,**t)['status']=='PASS','v4 actual saved small external-task receiving')
b=deepcopy(small);b['work']=b;b['seconds']=object();b['event']['actual_probability']['display']=b
ok(c.verify(raw,b,**t)['status']=='PASS','ignored diagnostic cycles remain deliberately non-proof')
# Only malformed JSON-type nonfinite leaves survive the shape guard; strict
# proof equality must still reject them rather than treating NaN as evidence.
for val in [float('nan'),float('inf'),float('-inf'),True,1,1.0]:
 b=deepcopy(small);b['record_TV_error_upper']=val;no(lambda b=b:c.verify(raw,b,**t),'guard does not weaken exact typed endpoint comparison')
for row in json.loads((H/'independent_production_replays.json').read_text()):
 z=row['certificate'];t=c.external_from_record(z);r=c.verify(c.fixture(),z,**t)
 ok(r['status']=='PASS' and r['record_TV_error_upper']==z['record_TV_error_upper'],'v4 ACTUAL original production verify recomputes full source task')
nonunit=json.loads((H/'nonunit_case.json').read_text());ok(c.verify(nonunit['raw'],nonunit['certificate'],**c.external_from_record(nonunit['certificate']))['status']=='PASS','v4 nonunit last-axis original task receiving')
report={'status':'PASS','checks':checks,'categories':cats,'refusals':reasons,'seconds':time.perf_counter()-start,'source':'6ab77089b94b0052f458644b7c64895f0c7a4fed53c43c2dc5510be770124cac'};(H/'v4_independent_results.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items()if k!='refusals'},indent=2));print('UNKNOWN',len(reasons))
