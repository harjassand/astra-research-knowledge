from pathlib import Path
from fractions import Fraction as F
from copy import deepcopy
import json,os,sys
import independent_aggregate_receiver as I
sys.path.insert(0,os.environ.get('AGGREGATE_SOURCE_DIR','producer-workspace/stochastic_free_aggregate_mass_pending_20261031'));import aggregate_mass as A
r=I.parse(A.fixture());c=I.construct(A.fixture(),F(7,6));assert I.canonical(c)==I.canonical(A.construct(A.fixture(),F(7,6)))
assert c['mass_head']['q']==F(14,3)and c['mass_head']['Q']==5
count=0
for K in (2,8,17):
 s=deepcopy(c);s['plan']['mass']['K']=K;s['mass_head']=I.head(s['plan'],r);h=s['mass_head'];rho=s['plan']['mass']['rho'];BH=h['Q']**K
 for j in range(K+30):
  g=I.evaluate(I.mass_g(s,j));g1=I.evaluate(I.mass_g(s,j+1));g2=I.evaluate(I.mass_g(s,j+2))
  assert g-g1>=F(1,(j+1)**2)
  if j<K:assert g>=2*s['t']*(g2+rho)
  assert (j+1)*(g-1)+rho*F(j,2*(j+1))<=h['C']*BH+2+rho/2
  if j:assert (j+1)**2*(I.evaluate(I.mass_g(s,max(0,j-2)))-g)<=9*h['C']*BH
  count+=1
pow_count=0
for b in range(2,12):
 for e in range(20):
  value=b**e
  for cap in (F(0),F(1),F(value-1),F(value),F(value+1),F(2*value-1,2),F(2*value+1,2)):
   assert I.pow_leq(b,e,cap)==(value<=cap);pow_count+=1
# AST is actually executed, and every nested binary threshold branch is checked.
s=deepcopy(c);s['mass_head'].update(K=2,Q=2,L0=0,Jcoef=1,outer_head_coefficients=(F(1),F(1),F(1)))
ex=I.expressions(r,s);N=int(I.evaluate(ex['Nstar'],1000));H=I.evaluate(ex['H'],1000);z=I.evaluate(ex['zeta'],1000)
assert H==s['mass_head']['H_coefficients'][0]+4*s['mass_head']['H_coefficients'][1]
assert z==s['mass_head']['nu']/(2*H)
assert I.evaluate(ex['stationary_bound'],1000)['status']=='UNKNOWN_POWER_INTERMEDIATE_BUDGET'
# Full actual main expression is saved as a machine-readable AST, without expansion.
main=I.construct(A.fixture(),2);ast=I.expressions(r,main)
Path(__file__).with_name('MAIN_NESTED_AST.json').write_text(json.dumps(I.P.wire(ast),indent=2)+'\n')

wire=json.loads(json.dumps(I.P.wire(ex)))
for key in ('Bhead','cutoff_exponent','Ucut','Nstar','H','zeta'):
 assert I.evaluate(I.decode_expression(wire[key]),1000)==I.evaluate(ex[key],1000)
main_wire=json.loads(json.dumps(I.P.wire(ast)))
assert I.receive_expression_bundle(A.fixture(),2,main_wire)
bad=deepcopy(main_wire);bad['Bhead'][2]+=1
assert not I.receive_expression_bundle(A.fixture(),2,bad)
res=dict(ast_wire_expression_roundtrips=6,ast_bundle_receiving_and_mutation=True,status='PASS_FRACTIONAL_BASE_AND_NESTED_AST',fractional_q=c['mass_head']['q'],ceiling_Q=c['mass_head']['Q'],actual_K=c['mass_head']['K'],complete_fractional_receipt_sha256=I.digest(c),synthetic_fractional_head_points=count,bounded_power_order_comparisons=pow_count,synthetic_nested_threshold=N,main_ast_unexpanded=True)
Path(__file__).with_name('NESTED_FRACTIONAL_RESULTS.json').write_text(json.dumps(I.P.wire(res),indent=2)+'\n');print(json.dumps(I.P.wire(res)))
