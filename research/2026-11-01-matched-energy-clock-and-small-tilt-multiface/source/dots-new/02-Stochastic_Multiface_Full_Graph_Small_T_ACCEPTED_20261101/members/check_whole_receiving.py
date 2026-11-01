"""Independent reconstruction versus frozen candidate; controlled source override.
The candidate is used only on the comparison side. It is never imported by receiver.
"""
from pathlib import Path
from fractions import Fraction as Q
from itertools import combinations,permutations
from copy import deepcopy
from random import Random
import sys,os,json,hashlib,time
import independent_receiver as I
HERE=Path(__file__).resolve().parent
SOURCE=Path(os.environ.get('MULTIFACE_SOURCE_DIR',str(HERE/'frozen_source'))).resolve()
sys.path.insert(0,str(SOURCE))
import multiface as M,api,receive_certificate as R
C={}
def count(k,n=1):C[k]=C.get(k,0)+n
def reject(fn,classes=(Exception,)):
 try:fn()
 except classes:return
 raise AssertionError('expected refusal')
def canon(x):return json.dumps(x,sort_keys=True,indent=2)+'\n'
def rawtests():
 rng=Random(271828)
 for n in range(2,5):
  pairs=list(combinations(range(n),2))
  for mask in range(1,1<<len(pairs)):
   E=tuple(e for k,e in enumerate(pairs)if mask>>k&1)
   for sparse in [False,True]:
    raw=I.fixture(n,E,perturb=True,sparse=sparse)
    # Unequal positive rationals, including duplicate-channel aggregation.
    raw=[(u,v,k*Q(1+(j%5),1+(j%3)))for j,(u,v,k)in enumerate(raw)]
    raw=[(u,v,k/3)for u,v,k in raw]+[(u,v,2*k/3)for u,v,k in raw]
    rng.shuffle(raw)
    mine=I.encoded(I.construct(raw));candidate=M.encode(M.construct(raw))
    assert I.strict_equal(mine,candidate)
    assert I.strict_equal(I.encoded(I.acquire(raw)),M.encode(M.recognize(raw)))
    count('exact_raw_and_complete_receipt_fixtures')
 raw=I.fixture();p=I.construct(raw);reference=I.encoded(p)
 for perm in permutations(range(6)):
  def relabel(u):
   v=[0]*6
   for i,xi in enumerate(u):v[perm[i]]=xi
   return tuple(v)
  varied=[(relabel(u),relabel(v),k)for u,v,k in raw]
  mine=I.construct(varied);candidate=M.construct(varied)
  assert I.strict_equal(I.encoded(mine),M.encode(candidate))
  assert all(mine[k]==p[k]for k in ['P','eps','t','e','H','Nstar','nu','zeta'])
  assert mine['raw']['A']==perm[0]
  count('species_permutation_full_receipts')
 for variant in [list(reversed(raw)),raw[1:]+raw[:1]]:
  assert I.strict_equal(M.encode(M.construct(variant)),reference);count('raw_order_canonical_receipts')
 duplicate=[(u,v,k/2)for u,v,k in raw]*2
 assert I.strict_equal(M.encode(M.construct(duplicate)),reference);count('duplicate_normalization')
 # Strict domain rejection, not an unsupported-mathematics conclusion.
 bad=[]
 bad += [[],raw[:-1],[(raw[0][0],raw[0][1],0)]+raw[1:],[(raw[0][0],raw[0][1],-1)]+raw[1:]]
 for rate in [True,1.0,'1',None]:bad.append([(raw[0][0],raw[0][1],rate)]+raw[1:])
 for countval in [-1,False,0.0,'0']:
  u=list(raw[0][0]);u[1]=countval;bad.append([(u,raw[0][1],raw[0][2])]+raw[1:])
 bad.append([(raw[0][0][:-1],raw[0][1],1)]+raw[1:])
 bad.append(raw+[(raw[0][0],raw[0][0],1)])
 def vector(*idx):return tuple(idx.count(i)for i in range(6))
 for u,v in [(vector(),vector(1)),(vector(0),vector(1)),(vector(0,0),vector(0,1)),(vector(0,0),vector(1,1)),(vector(0,0,0),vector(1,2,3)),(vector(1,2),vector(4,5))]:bad.append(raw+[(u,v,Q(1)),(v,u,Q(1))])
 # Remove a satellite's only active-source family or a hub's amplification pair.
 bad.append([(u,v,k)for u,v,k in raw if u!=vector(0,5) and v!=vector(0,5)])
 bad.append([(u,v,k)for u,v,k in raw if not({u,v}=={vector(0,0),vector(1,2)})])
 for rr in bad:
  reject(lambda rr=rr:I.acquire(rr));reject(lambda rr=rr:M.recognize(rr));count('raw_domain_rejections')
 return raw,p,reference

def receivertests(raw,p,reference):
 # Read the actual frozen wire. No producer call is needed by independent receive.
 frozen=(SOURCE/'fixture_certificate.json').read_bytes();assert I.receive(raw,frozen)
 expected=canon(reference).encode();assert frozen==expected
 (HERE/'INDEPENDENT_FIXTURE_CERTIFICATE.json').write_bytes(expected)
 count('full_frozen_wire_independently_received')
 mutations=[]
 for k,val in [('status','INDEPENDENT_PASS'),('Nstar',0),('t','2'),('P',0),('M',float(p['M'])),('mask_count',True)]:
  d=deepcopy(reference);d[k]=val;mutations.append(d)
 for key,val in [('A',False),('m',6.0),('raw_sha256','0'*64),('b','999')]:
  d=deepcopy(reference);d['raw'][key]=val;mutations.append(d)
 for key,val in [('weight',1),('resource_weights',[0]*6),('Far',[])]:
  d=deepcopy(reference);d['faces'][0][key]=val;mutations.append(d)
 d=deepcopy(reference);d['faces'].pop();mutations.append(d)
 d=deepcopy(reference);d['CF_expression']['args'][2]['exponent']=0;mutations.append(d)
 d=deepcopy(reference);d['moment_bound_expression']['args'][0]='1';mutations.append(d)
 d=deepcopy(reference);d['extra']=0;mutations.append(d)
 for d in mutations:
  assert not I.receive(raw,d)
  assert not R.receive(raw,d)
  count('strict_semantic_and_type_mutation_rejections')
 # Candidate code disabled while independent receive/reconstruction executes.
 originals={k:getattr(M,k)for k in ['recognize','construct','profile','diff','face_stats','psi','value','generator']}
 def disabled(*a,**kw):raise AssertionError('candidate function called by independent receiver')
 try:
  for k in originals:setattr(M,k,disabled)
  assert I.receive(raw,frozen);count('independent_receive_candidate_functions_disabled',len(originals))
 finally:
  for k,v in originals.items():setattr(M,k,v)
 # Both large expressions remain factored. An expression refusal is not numeric output.
 for node in [p['CF_expression'],p['moment_bound_expression']]:
  for bits in [0,10000,1000000]:
   reject(lambda:I.eval_expression(node,max_power_bits=bits),(I.UnknownComputation,));reject(lambda:R.evaluate_expression(node,max_power_bits=bits),(M.BudgetRefusal,));count('actual_head_power_refusals')
 for base in [Q(-3,2),Q(0),Q(2,3),Q(3,2),Q(10001,10000)]:
  for exponent in [0,1,2,7,31]:
   expr={'op':'mul','args':[Q(2,3),{'op':'pow','base':base,'exponent':exponent}]}
   truth=Q(2,3)*base**exponent
   assert I.eval_expression(expr,10000)==R.evaluate_expression(expr,10000)==truth;count('exact_symbolic_expression_values')
 for bad in [True,-1,1.5,'100',Q(100)]:
  reject(lambda:I.eval_expression(p['CF_expression'],max_power_bits=bad),(ValueError,));reject(lambda:R.evaluate_expression(p['CF_expression'],max_power_bits=bad),(ValueError,));count('expression_budget_domain_rejections')
 for node in [True,None,{'op':'pow','base':'2','exponent':True},{'op':'pow','base':'2','exponent':-1},{'op':'add','args':[]},{'op':'pow','base':'2','exponent':1.0}]:
  reject(lambda:I.eval_expression(node),(ValueError,));reject(lambda:R.evaluate_expression(node),(ValueError,));count('expression_domain_rejections')


def budgettests(raw,p):
 q=api.qualitative(raw);assert q['independent_sets_enumerated']==0
 ordered=hashlib.sha256(json.dumps(I.encoded(tuple((tuple(u),tuple(v),Q(k))for u,v,k in raw)),sort_keys=True).encode()).hexdigest()
 assert q['input_list_sha256']==ordered and q['normalized_reaction_sha256']==q['raw_sha256']
 reversed_q=api.qualitative(list(reversed(raw)))
 assert reversed_q['input_list_sha256']!=ordered and reversed_q['normalized_reaction_sha256']==q['normalized_reaction_sha256'];count('ordered_and_normalized_identity_checks',3)
 old=M.construct
 try:
  M.construct=lambda*a,**kw:(_ for _ in ()).throw(AssertionError('quantitative acquisition called'))
  assert api.qualitative(raw)==q;count('qualitative_no_subset_enumeration')
 finally:M.construct=old
 for budget in [0,1,31]:
  out=api.construct(raw,max_masks=budget)
  assert out['qualitative']==q and out['stability_refuted']is False
  assert 'certificate'not in out and 't'not in out and 'Nstar'not in out
  reject(lambda:I.construct(raw,max_masks=budget),(I.UnknownComputation,));count('mask_refusal_retains_qualitative_only')
 assert api.construct(raw,max_masks=32)['certificate']['t']==p['t'];count('mask_boundary_acquisition')
 for b in [True,-1,1.5,'32',Q(32)]:
  reject(lambda:api.construct(raw,max_masks=b),(ValueError,));count('mask_budget_domain_rejections')
 for j in [0,1,10,100]:
  k=j+p['s0'];bits=k*max(p['q'].numerator.bit_length(),p['q'].denominator.bit_length());truth=(1-p['q']**-k)/k
  assert api.pointwise_profile(p,j,max_exponent=k,max_power_bits=bits)==truth
  reject(lambda:api.pointwise_profile(p,j,max_exponent=k-1,max_power_bits=bits),(M.BudgetRefusal,))
  reject(lambda:api.pointwise_profile(p,j,max_exponent=k,max_power_bits=bits-1),(M.BudgetRefusal,))
  count('pointwise_exact_boundary_values_and_refusals',3)
 for bad in [True,-1,1.5,'1',Q(1)]:
  reject(lambda:api.pointwise_profile(p,bad),(ValueError,));count('pointwise_state_domain_rejections')
  reject(lambda:api.pointwise_profile(p,0,max_exponent=bad),(ValueError,));count('pointwise_exponent_budget_domain_rejections')
  reject(lambda:api.pointwise_profile(p,0,max_power_bits=bad),(ValueError,));count('pointwise_bit_budget_domain_rejections')
 # A 20,001-bit valid rate must not lose qualitative matching to Python decimal limits.
 giant=I.fixture(2,((0,1),));giant[0]=(*giant[0][:2],Q(1<<20000));lim=sys.get_int_max_str_digits()if hasattr(sys,'get_int_max_str_digits')else None
 out=api.qualitative(giant)
 assert out['raw_sha256']==I.acquire(giant)['raw_sha256'] and out['independent_sets_enumerated']==0
 assert (sys.get_int_max_str_digits()if hasattr(sys,'get_int_max_str_digits')else None)==lim
 refused=api.construct(giant,max_masks=0);assert refused['qualitative']==out and 'certificate'not in refused;count('giant_rational_qualitative_and_refusal',2)
 return {'mask_count':p['mask_count'],'faces':len(p['faces']),'Nstar_bits':p['Nstar'].bit_length(),'max_scalar_bits':max(abs(v.numerator).bit_length()+v.denominator.bit_length()if isinstance(v,Q)else abs(v).bit_length()for v in p.values()if type(v)is int or isinstance(v,Q)),'giant_raw_rate_bits':20001,'global_decimal_limit_unchanged':True,'CF_and_moment_unexpanded':True}

if __name__=='__main__':
 started=time.monotonic();raw,p,ref=rawtests();receivertests(raw,p,ref);cost=budgettests(raw,p)
 result={'status':'PASS_INDEPENDENT_RAW_EXACT_CERTIFICATE_SYMBOLIC_RECEIVING_AND_BUDGET_CHECKS','source_manifest_sha256':hashlib.sha256((SOURCE/'AUTHOR_FREEZE_MANIFEST.json').read_bytes()).hexdigest(),'counts':C,'costs':cost,'independent_fixture_sha256':hashlib.sha256((HERE/'INDEPENDENT_FIXTURE_CERTIFICATE.json').read_bytes()).hexdigest()}
 (HERE/'WHOLE_RECEIVING_RESULTS.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
 print(json.dumps({'status':result['status'],'counts':C,'elapsed_seconds':time.monotonic()-started},sort_keys=True))
