"""Concrete v1 regression attacks plus bounded/request-bound v2 receiving.
Same-author checks; independent whole audit still required.
"""
from pathlib import Path
from fractions import Fraction as F
from copy import deepcopy
import hashlib,json
import common_box as C
root=Path(__file__).resolve().parent
raw=C.fixture();p=C.construct(raw);original=C.canonical_bytes(p);counts={}
# Returned expression ownership, including independent branches of one receipt.
tail=C.tail_recipe(p,10,F(1),24,event_threshold=100)
def containers(x):
    found=set();stack=[x]
    while stack:
        v=stack.pop()
        if type(v) in (dict,list,tuple):
            found.add(id(v));stack.extend(v.values() if type(v)is dict else v)
    return found
assert not containers(p)&containers(tail)
cf=tail['max_count_upper']['args'][1]['args'][2]['args'][1]['args'][1]
assert cf==p['CF_expression'] and cf is not p['CF_expression']
cf['coefficient']=F(0)
assert C.canonical_bytes(p)==original
assert C.tail_recipe(p,10,F(1),24)['max_count_upper']['args'][1]['args'][2]['args'][1]['args'][1]['coefficient']==p['CF_prefactor']
assert not containers(tail['max_count_upper'])&containers(tail['event_count_upper'])
counts['tail_ownership_and_mutation_controls']=4
# A read-only total/spent, immutable allocation snapshots and detached receipts.
ledger=C.RiskLedger(F(1,10));before=ledger.allocations
receipt=ledger.reserve(F(1,20));snapshot=ledger.allocations
receipt['spent']=F(0);receipt['failure']=F(0)
assert before==() and snapshot==(F(1,20),) and ledger.spent==F(1,20)
failed=0
for attribute,new in [('total',F(1)),('spent',F(0)),('allocations',[])]:
    try:setattr(ledger,attribute,new)
    except AttributeError:failed+=1
    else:raise AssertionError('public ledger field writable')
try:ledger.allocations.append(F(1))
except AttributeError:failed+=1
else:raise AssertionError('allocation snapshot mutable')
try:ledger.allocations[0]=F(0)
except TypeError:failed+=1
else:raise AssertionError('allocation item mutable')
ledger.reserve(F(1,20));assert snapshot==(F(1,20),)
assert ledger.spent==sum(ledger.allocations)==ledger.total
assert ledger.reserve(F(1,100))['status']=='REJECT_NO_ALLOCATION'
counts['public_ledger_mutations_refused']=failed
# Valid canonical bytes remain exact, including the old frozen certificate.
wire=C.canonical_bytes(p);C.receive_wire(raw,wire)
assert wire==(root/'fixture_certificate.json').read_bytes()
refusals=[]
def refused(label,call):
    try:call()
    except (C.Unsupported,C.BudgetRefusal) as exc:refusals.append({'test':label,'refusal':type(exc).__name__})
    else:raise AssertionError('malformed/adversarial record admitted: '+label)
malformed={
 'deep_json':b'['*1100+b'0'+b']'*1100,
 'zero_denominator':b'{"QHEX":["0x1","0x0"]}\n',
 'negative_denominator':b'{"QHEX":["0x1","-0x1"]}\n',
 'rational_arity':b'{"QHEX":["0x1"]}\n',
 'rational_tag_nonlist':b'{"QHEX":"0x1"}\n',
 'rational_not_reduced':b'{"QHEX":["0x2","0x4"]}\n',
 'numeric_tag_extra_key':b'{"QHEX":["0x1","0x1"],"extra":0}\n',
 'bad_hex':b'{"QHEX":["NaN","0x1"]}\n',
 'wrong_atom':b'{"QHEX":[1,"0x1"]}\n',
 'invalid_json':b'{',
 'invalid_utf8':b'\xff',
 'nonfinite_nan':b'NaN',
 'nonfinite_infinity':b'Infinity',
 'float':b'1.0',
 'bool':b'true',
 'null':b'null',
 'duplicate_key':b'{"x":1,"x":2}',
 'noncanonical_negative_zero':b'-0\n',
 'noncanonical_small_integer_tag':b'{"ZHEX":"0x2"}\n',
 'noncanonical_hex_leading_zero':b'{"QHEX":["0x01","0x1"]}\n',
 'oversized_decimal':b'1'*5000,
 'incomplete_string':b'"abc',
 'bad_nesting':b'][',
 'scalar_not_certificate':b'0\n',
}
for label,payload in malformed.items():refused(label,lambda payload=payload:C.receive_wire(raw,payload))
for name,args in [('bytes',{'max_bytes':1}),('nodes',{'max_nodes':1}),('depth',{'max_depth':1}),('atom_bits',{'max_atom_bits':1}),('string_chars',{'max_string_chars':1})]:
    refused('wire_budget_'+name,lambda args=args:C.receive_wire(raw,wire,**args))
for name,args in [('bool_bytes',{'max_bytes':True}),('negative_nodes',{'max_nodes':-1}),('float_depth',{'max_depth':1.5})]:
    refused('invalid_budget_'+name,lambda args=args:C.receive_wire(raw,wire,**args))
cycle=[];cycle.append(cycle)
refused('typed_cycle',lambda:C.receive(raw,cycle))
refused('decode_cycle',lambda:C.decode(cycle))
deep=0
for i in range(1100):deep=[deep]
refused('typed_depth',lambda:C.receive(raw,deep))
refused('decode_depth',lambda:C.decode(deep))
refused('wide_tree_budget',lambda:C.decode([0]*1000,max_nodes=10))
refused('expanded_alias_budget',lambda:C.decode([[0]*10]*100,max_nodes=100))
class Evil(dict):pass
refused('dict_subclass',lambda:C.receive(raw,Evil(p)))
refused('nonstring_key',lambda:C.receive(raw,{0:1}))
# Separately held client request: changing the whole internally valid budget is
# refused against the ORIGINAL request, not accepted as an arithmetic record.
request=dict(initial_total_upper_bound=10,horizon=F(1),failure=F(1,100))
b=C.resource_budget(p,10,F(1),F(1,100));C.receive_resource_budget(raw,b,**request)
other=[C.resource_budget(p,11,F(1),F(1,100)),C.resource_budget(p,10,F(2),F(1,100)),C.resource_budget(p,10,F(1),F(1,10))]
for i,claim in enumerate(other):refused('valid_but_wrong_client_request_'+str(i),lambda claim=claim:C.receive_resource_budget(raw,claim,**request))
for key,bad in [('initial_total_upper_bound',True),('horizon',1.0),('failure',F(0))]:
    req=dict(request);req[key]=bad
    refused('invalid_external_'+key,lambda req=req:C.receive_resource_budget(raw,b,**req))
for base,exponent in [(1.5,2),(F(2),1.5),(F(0),-1),(F(2),True)]:
    refused('power_type_'+str(len(refusals)),lambda base=base,exponent=exponent:C.power(base,exponent))
counts['controlled_refusals']=len(refusals)
counts['external_request_substitutions_refused']=len(other)
result={'status':'PASS_AUTHOR_V2_RECEIVER_REGRESSIONS_NOT_INDEPENDENT','counts':counts,'refusals':refusals,'v1_canonical_certificate_bytes_preserved':True,
        'bindings':{f:hashlib.sha256((root/f).read_bytes()).hexdigest() for f in ['common_box.py','check_v2_receiving.py','COMMON_PREDICTABLE_BOX_THEOREM.md']}}
(root/'v2_receiving_results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
