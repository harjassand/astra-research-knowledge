from pathlib import Path
from fractions import Fraction as F
from copy import deepcopy
import sys,json,hashlib,time,builtins
A=Path(__file__).resolve().parent;sys.path.insert(0,str(A/'replay_v2'));import common_box as C
checks=0;cats={};refusals=[];start=time.perf_counter()
def ok(z,k):
 global checks
 assert z,k
 checks+=1;cats[k]=cats.get(k,0)+1

def no(fn,k,allowed=(C.Unsupported,C.BudgetRefusal)):
 try:fn()
 except allowed as e:refusals.append({'test':k,'class':type(e).__name__,'reason':str(e)});ok(True,k)
 else:raise AssertionError('false admission '+k)
raw=C.fixture();p=C.construct(raw);orig=C.canonical_bytes(p)
receipt=C.tail_recipe(p,10,F(1),24,event_threshold=100);node=receipt['max_count_upper']['args'][1]['args'][2]['args'][1]['args'][1]
ok(node is not p['CF_expression'],'returned tail source expression detached')
node['coefficient']=F(0);ok(C.canonical_bytes(p)==orig,'returned tail mutation preserves acquired certificate')
branch=receipt['event_count_upper']['args'][1]['args'][0]
ok(branch is not receipt['max_count_upper'] and branch['args'][1]['args'][2]['args'][1]['args'][1]['coefficient']==p['CF_prefactor'],'event/count returned proof branches independently owned')
ok(C.tail_recipe(p,10,F(1),24)['max_count_upper']['args'][1]['args'][2]['args'][1]['args'][1]['coefficient']==p['CF_prefactor'],'later tail receipts retain valid positive head')
L=C.RiskLedger(F(1,10));z=L.reserve(F(1,20));snapshot=L.allocations;z['failure']=F(9);z['spent']=F(-1);ok(L.spent==F(1,20)and L.allocations==(F(1,20),),'reservation output detached from ledger proof state')
for name,value in [('spent',F(0)),('total',F(9)),('allocations',())]:
 no(lambda name=name,value=value:setattr(L,name,value),'public ledger assignment refused',(AttributeError,))
 no(lambda name=name:delattr(L,name),'public ledger deletion refused',(AttributeError,))
no(lambda:snapshot.append(F(1,5)),'public allocation view immutable',(AttributeError,))
L.reserve(F(1,20));ok(snapshot==(F(1,20),)and L.allocations==(F(1,20),F(1,20)),'old allocation snapshot not changed by next reservation')
ok(L.reserve(F(1,100))['status']=='REJECT_NO_ALLOCATION'and L.spent==L.total,'overspend still refused after output mutation attempts')
# Independently count full expanded trees; repeated aliases count repeatedly.
def measure(x,depth=0):
 vals=[(1,depth,abs(x).bit_length()if type(x)is int else max(x.numerator.bit_length(),x.denominator.bit_length())if type(x)is F else 0,len(x)if type(x)is str else 0)]
 if type(x)is dict:
  for k,v in x.items():vals.extend([measure(k,depth+1),measure(v,depth+1)])
 elif type(x)in(list,tuple):vals.extend(measure(v,depth+1)for v in x)
 return sum(v[0]for v in vals),max(v[1]for v in vals),max(v[2]for v in vals),max(v[3]for v in vals)
nodes,dep,bits,chars=measure(p);ok(C._check_tree(p)==nodes,'independent exact expanded proof-tree count')
for key,limit in [('max_nodes',nodes),('max_depth',dep),('max_atom_bits',bits),('max_string_chars',chars)]:
 ok(C.receive(raw,p,**{key:limit})['certificate_sha256']==C.digest(p),'exact direct certificate structural/atom budget admits')
 no(lambda key=key,limit=limit:C.receive(raw,p,**{key:limit-1}),'one below direct certificate structural/atom budget refuses')
for key in ['max_nodes','max_depth','max_atom_bits','max_string_chars']:
 for bad in [True,False,F(1),1.0,-1,None,'1']:
  no(lambda key=key,bad=bad:C.receive(raw,p,**{key:bad}),'strict receiving structural budget type')
enc=json.loads(orig);en,ed,eb,ec=measure(enc)
ok(C.receive_wire(raw,orig,max_nodes=en,max_depth=ed,max_atom_bits=bits,max_string_chars=ec)['certificate_sha256']==C.digest(p),'actual canonical wire with exact encoded-tree budgets')
for key,val in [('max_nodes',en-1),('max_depth',ed-1),('max_atom_bits',bits-1),('max_string_chars',ec-1)]:no(lambda key=key,val=val:C.receive_wire(raw,orig,**{key:val}),'one below encoded wire structural/atom budgets')
malformed=[b'['*1100+b'0'+b']'*1100,b'{"QHEX":["0x1","0x0"]}\n',b'{"QHEX":["0x1"]}\n',b'{',b'NaN\n',b'Infinity\n',b'-Infinity\n',b'1.0\n',b'1e3\n',b'true\n',b'null\n',b'false\n',b'{"a":1,"a":2}\n',b'\xff',b'\xef\xbb\xbf{}\n',b'0'*5000+b'\n',b'9'*5000+b'\n',b'"unterminated',b'{"QHEX":"xy"}\n',b'{"ZHEX":true}\n',b'{"QHEX":["0x1","-0x1"]}\n',b'{"QHEX":["0x2","0x2"]}\n',b'{"QHEX":["0x01","0x1"]}\n',b'{"QHEX":["0X1","0x1"]}\n',b'{"QHEX":["+0x1","0x1"]}\n',b'{"QHEX":["-0x0","0x1"]}\n',b'{"QHEX":["0x1","0x1"],"extra":0}\n',b'{"ZHEX":"0x1"}\n']
for wire in malformed:no(lambda wire=wire:C.receive_wire(raw,wire),'malformed/deep numeric wire controlled refusal')
for tag in [{'QHEX':[]},{'QHEX':[1,2]},{'QHEX':('0x1','0x1')},{'ZHEX':False},{'QHEX':['0x1','0x1'],'ZHEX':'0x1'}]:no(lambda tag=tag:C.decode(tag),'strict direct wire-tag schema')
for n in [4096,4097,5001]:
 x=(1<<(n-1))+1;tag=C.encode(x);decoded=C.decode(tag,max_atom_bits=n);ok(decoded==x,'decimal versus tagged integer boundary exact')
 no(lambda tag=tag,n=n:C.decode(tag,max_atom_bits=n-1),'decoded integer atom one bit below')
q=F((1<<5000)+1,(1<<4999)+3);ok(C.decode(C.encode(q),max_atom_bits=5001)==q,'huge reduced rational hex received without decimal-limit bypass')
no(lambda:C.decode(C.encode(q),max_atom_bits=5000),'rational atom exact bit guard')
# Preflights must reject malformed proof data before expensive raw recomputation.
real=C.construct;called=[]
def forbidden(*a,**kw):called.append(1);raise AssertionError('unreceived tree reached raw computation')
C.construct=forbidden
cycle=[];cycle.append(cycle);deep=0
for _ in range(1100):deep=[deep]
for value in [cycle,deep,{1:0},[False],{'x':object()}]:no(lambda value=value:C.receive(raw,value),'malformed direct tree stopped before raw construction')
for wire in malformed:no(lambda wire=wire:C.receive_wire(raw,wire),'malformed wire stopped before raw construction')
ok(not called,'all malformed preflights avoid scientific recomputation');C.construct=real
# Shared DAG is explicitly charged as expanded work; no free alias fanout.
dag=0
for _ in range(8):dag=[dag,dag]
cn=measure(dag)[0];ok(C._check_tree(dag,max_nodes=cn)==cn,'shared acyclic containers charged at every occurrence')
no(lambda:C._check_tree(dag,max_nodes=cn-1),'shared DAG expanded work budget')
dag=0
for _ in range(60):dag=[dag,dag]
no(lambda:C._check_tree(dag,max_nodes=1000),'exponential DAG expansion refused by finite scheduled budget')
# Saturated pending-stack regression: do not expand an individually fitting child
# when its queued siblings already consume the global node allowance.
seen=[];realrev=builtins.reversed
def observe(x):seen.append(len(x));return realrev(x)
C.reversed=observe
no(lambda:C._check_tree([list(range(8))]+[0]*5,max_nodes=10),'queued siblings paid before child expansion')
ok(seen==[6],'overbudget child not pushed or reversed');del C.reversed
# Externally bound resource original tasks, not self-declared claim semantics.
args={'initial_total_upper_bound':10,'horizon':F(1),'failure':F(1,100)};b=C.resource_budget(p,10,F(1),F(1,100))
ok(C.receive_resource_budget(raw,b,**args)['budget_sha256']==C.digest(b),'actual original resource task received')
for key in args:
 alt=dict(args);alt[key]=args[key]+(1 if key=='initial_total_upper_bound'else F(1,1000))
 no(lambda alt=alt:C.receive_resource_budget(raw,b,**alt),'every separately supplied original request field bound')
 other=C.resource_budget(p,alt['initial_total_upper_bound'],alt['horizon'],alt['failure'])
 no(lambda other=other:C.receive_resource_budget(raw,other,**args),'valid different task cannot substitute for original request')
 no(lambda key=key:C.receive_resource_budget(raw,b,**{k:v for k,v in args.items()if k!=key}),'missing required external task is a Python signature error',(TypeError,))
for key in args:
 for bad in [True,1.0,'1',None,F(-1)]:
  alt=dict(args);alt[key]=bad;no(lambda alt=alt:C.receive_resource_budget(raw,b,**alt),'malformed separately supplied resource task controlled refusal')
def leaves(o,path=()):
 if type(o)is dict:
  for k,v in o.items():yield from leaves(v,path+(k,))
 elif type(o)is list:
  for k,v in enumerate(o):yield from leaves(v,path+(k,))
 else:yield path,o
for path,v in leaves(b):
 z=deepcopy(b);o=z
 for k in path[:-1]:o=o[k]
 o[path[-1]]=v+1 if type(v)in(int,F)else v+'__forged'
 no(lambda z=z:C.receive_resource_budget(raw,z,**args),'every resource proof field bound to actual external request')
ok(C.canonical_bytes(p)==orig,'all returned resource/recipe mutations leave scalar certificate untouched')
report={'status':'PASS','checks':checks,'expected_refusals':len(refusals),'categories':cats,'refusals':refusals,'source_sha256':hashlib.sha256(Path(C.__file__).read_bytes()).hexdigest(),'direct_tree':dict(nodes=nodes,depth=dep,atom_bits=bits,string_chars=chars),'wire_tree':dict(nodes=en,depth=ed,encoded_atom_bits=eb,string_chars=ec),'seconds':time.perf_counter()-start,'scope':'v1 ownership/ledger/wire failures repaired; original task bound; actual count observation and rate predictability remain external contracts'}
(A/'repair_v2_results.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items()if k!='refusals'},indent=2))
