from pathlib import Path
from fractions import Fraction as F
import ast,json,hashlib,sys
A=Path(__file__).resolve().parent;sys.path.insert(0,str(A/'replay_v2'));import common_box as C
checks=0;refusals=0;cats={}
def ok(v,k):
 global checks
 assert v,k
 checks+=1;cats[k]=cats.get(k,0)+1

def no(fn,k):
 global refusals
 try:fn()
 except(C.Unsupported,C.BudgetRefusal):refusals+=1;ok(True,k)
 else:raise AssertionError(k)
for q in [True,False,1.0,None,'2',F(0),F(-1)]:no(lambda q=q:C.power(q,2),'strict positive exact rational power base')
for k in [True,False,F(1),1.0,None,'1']:no(lambda k=k:C.power(F(2),k),'strict exact integer power exponent')
for q,k in [(2,-4),(F(2,3),0),(F(5,3),7)]:ok(C.power(q,k)==F(q)**k,'supported exact low-level power result')
raw=C.fixture();p=C.construct(raw);saved=C.decode(json.loads((A/'frozen_v2/resource_budget_examples.json').read_text()));tasks=[(10,F(1),F(1,100)),(10,F(1<<(2*p['Nstar'].bit_length()+20)),F(1,100)),(0,F(0),F(1,3)),(1<<1500,F(7,3),F(1,1<<200))]
for b,(U,T,a)in zip(saved,tasks):
 ok(C.receive_resource_budget(raw,b,initial_total_upper_bound=U,horizon=T,failure=a)['budget_sha256']==C.digest(b),'each saved actual resource task independently supplied and received')
 # The explicitly supplied input bound is still just a conditional contract.
 ok(b['initial_total_upper_bound']==U and b['horizon']==T and b['failure']==a,'literal task fields not a proof of actual sensing')
# Structural proof by exact AST that no arithmetic/model formula changed.
def nodes(path):return {n.name:ast.dump(n,include_attributes=False)for n in ast.parse(path.read_text()).body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
a=nodes(A/'frozen_v1/common_box.py');b=nodes(A/'frozen_v2/common_box.py')
unchanged=['rat','ceilq','encode','canonical_bytes','digest','recognize','construct','integer_budget','state','faces','multiplier','propensity','worst_scaled_drift','RateGuard','fixture','ceil_log2_at_least_one','poisson_dyadic_threshold','resource_budget']
for name in unchanged:ok(a[name]==b[name],'exact unchanged mathematical/model function AST '+name)
for name in ['COMMON_PREDICTABLE_BOX_THEOREM.md','raw_box.json','fixture_certificate.json','resource_budget_examples.json']:
 ok((A/'frozen_v1'/name).read_bytes()==(A/'frozen_v2'/name).read_bytes(),'unchanged theorem and exact scientific data '+name)
# Every newly frozen replay output is exact, no timing fields need suppression.
for name in ['common_box_results.json','box_large_tier_results.json','scalar_extreme_results.json','v2_receiving_results.json','fixture_certificate.json','resource_budget_examples.json']:
 ok((A/'frozen_v2'/name).read_bytes()==(A/'replay_v2'/name).read_bytes(),'actual copied v2 author replay byte equality '+name)
out={'status':'PASS','checks':checks,'expected_refusals':refusals,'categories':cats,'source_sha256':hashlib.sha256(Path(C.__file__).read_bytes()).hexdigest()};(A/'supplement_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
