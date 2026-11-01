from pathlib import Path
from fractions import Fraction as F
import sys,json,copy
A=Path(__file__).resolve().parent;sys.path.insert(0,str(A/'replay_v1'));import common_box as C
p=C.construct(C.fixture());before=C.digest(p);receipt=C.tail_recipe(p,10,F(1),24)
node=receipt['max_count_upper']['args'][1]['args'][2]['args'][1]['args'][1]
assert node is p['CF_expression'];node['coefficient']=F(0)
alias={'returned_tail_node_aliases_certificate':True,'mutating_returned_recipe_changes_certificate':C.digest(p)!=before,'next_tail_receipt_coefficient':str(C.tail_recipe(p,10,F(1),24)['max_count_upper']['args'][1]['args'][2]['args'][1]['args'][1]['coefficient'])}
ledger=C.RiskLedger(F(1,10));ledger.reserve(F(1,20));alloc=ledger.allocations;alloc.append(F(1,5));alias['public_allocations_alias']=sum(ledger.allocations)>ledger.total;ledger.spent=F(0);alias['public_spent_reset_allows_new_allocation']=ledger.reserve(F(1,10))['status']=='ADMIT_EPISODE_RISK'
probes=[]
for name,payload in [('deep_json',b'['*1100+b'0'+b']'*1100),('rational_zero_denominator',b'{"QHEX":["0x1","0x0"]}\n'),('rational_wrong_arity',b'{"QHEX":["0x1"]}\n'),('invalid_json',b'{'),('nonfinite_json',b'NaN\n')]:
 try:C.receive_wire(C.fixture(),payload)
 except Exception as e:probes.append({'test':name,'exception':type(e).__name__,'recognized_refusal':isinstance(e,(C.Unsupported,C.BudgetRefusal)),'message':str(e)})
 else:probes.append({'test':name,'unexpected_accept':True})
raw=C.fixture();g=C.RateGuard(raw);aa=g.active;raw[0]=(raw[0][0],raw[0][1],F(999),F(999));assert g.active==aa;request=list(g.active);g.select(request);request[0]=0;assert g.active[0]!=0
out={'source':'a5b1049d3af540c8cf6df2f1cf3f540ccc48827d27bf68830154637daeb1845e','alias':alias,'wire':probes,'rate_guard_input_and_request_alias_checks':'PASS','scope':'v1 exact failures; no source edits, giant allocation or physical/model inference'}
(A/'api_v1_diagnostic.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
