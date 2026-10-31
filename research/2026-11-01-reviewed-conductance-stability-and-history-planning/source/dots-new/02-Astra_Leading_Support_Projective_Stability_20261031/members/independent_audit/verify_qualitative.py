#!/usr/bin/env python3
"""Independent qualitative receipt controls, including repaired accounting regression."""
from pathlib import Path
from fractions import Fraction as F
import importlib.util,sys,json,copy,hashlib
from verify_projective import p,support
HERE=Path(__file__).resolve().parent
sys.modules['projective_mass']=p

def load(name,file):
 spec=importlib.util.spec_from_file_location(name,HERE/file);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
s=load('qualitative_receiver','frozen_structural_receiver.py')
old=load('original_receiver','original_structural_receiver_be9c6a31.py')
sp,raw=p.demo_network();rec=p.recognize(sp,raw);receipt=s.acquire(sp,raw)
assert support(rec,receipt['support_witness'])
assert s.verify(sp,raw,receipt)['verified']
original=json.loads((HERE/'frozen_qualitative_results.json').read_text())
assert original['receipt']==receipt and s.verify(sp,raw,receipt)==original['independent_raw_receiving_pass']

badzero=copy.deepcopy(receipt);badzero['support_witness']['support_reaction_tests']=0;badzero['work']['support_reaction_tests']=0;badzero['work']['support_coordinate_tests_upper']=0
assert old.verify(sp,raw,badzero)['verified']
try:s.verify(sp,raw,badzero)
except ValueError as exc:zero_reason=str(exc)
else:raise AssertionError('zero-work accounting regression not repaired')

rejected=[]
for kind in ['theorem_hash','raw_hash','pivot','leading_order','immigration','conclusions','numerical_output','Euler_execution','degree_execution','stationary_law','seed_omission','reaction_index','added_species','before_support','zero_work','receipt_work_only','coordinate_work']:
 r=copy.deepcopy(receipt)
 if kind=='theorem_hash':r['theorem_sha256']='0'*64
 elif kind=='raw_hash':r['raw_sha256']='0'*64
 elif kind=='pivot':r['role']['pivot']=1
 elif kind=='leading_order':r['role']['leading_order']=3
 elif kind=='immigration':r['role']['immigration']='2'
 elif kind=='conclusions':r['conclusions']=['global irreducibility']
 elif kind=='numerical_output':r['quantitative_output']='Foster radius 1'
 elif kind=='Euler_execution':r['work']['Euler_steps_executed']=1
 elif kind=='degree_execution':r['work']['polynomial_degrees_searched']=1
 elif kind=='stationary_law':r['work']['stationary_fiber_laws_used']=1
 elif kind=='seed_omission':r['support_witness']['trials'].pop()
 elif kind=='reaction_index':r['support_witness']['trials'][1]['steps'][0]['internal_row']=1
 elif kind=='added_species':r['support_witness']['trials'][1]['steps'][0]['added']=[0]
 elif kind=='before_support':r['support_witness']['trials'][1]['steps'][0]['before']=[1,2]
 elif kind=='zero_work':r=badzero
 elif kind=='receipt_work_only':r['work']['support_reaction_tests']+=1
 else:r['work']['support_coordinate_tests_upper']-=1
 try:s.verify(sp,raw,r)
 except (ValueError,KeyError):rejected.append(kind)
 else:raise AssertionError('tamper accepted '+kind)

z=(0,0,0);A=(1,0,0);B=(0,1,0);C=(0,0,1);BB=(0,2,0);CC=(0,0,2)
stable=[(z,A,1),(A,z,1),(A,B,1),(B,A,1),(A,C,1),(C,A,1),(BB,CC,1),(CC,BB,1)]
negative=s.acquire(sp,stable);assert negative['status']=='STRICT_TOP_CONE_OBSTRUCTED' and negative['network_stability']=='UNKNOWN'
assert not support(p.recognize(sp,stable),negative['support_witness'])
for kind in ['nonclosed_face','false_recurrence_upgrade','false_instability_claim']:
 r=copy.deepcopy(negative)
 if kind=='nonclosed_face':r['support_witness']['closed_face_support']=[1]
 elif kind=='false_recurrence_upgrade':r.update(status='QUALITATIVE_CERTIFIED',conclusions=s.CONCLUSIONS);r['support_witness']['accessible']=True
 else:r['network_stability']='UNSTABLE'
 try:s.verify(sp,stable,r)
 except ValueError:rejected.append(kind)
 else:raise AssertionError('negative receipt tamper accepted '+kind)

# Break WR but rebind the input digest, to ensure graph checking is substantive.
nonwr=raw[:5]+raw[6:];r=copy.deepcopy(receipt);r['raw_sha256']=s.raw_digest(sp,s.normalized(sp,nonwr))
try:s.verify(sp,nonwr,r)
except ValueError:rejected.append('non_WR_raw_rebound')
else:raise AssertionError('non-WR accepted')
assert s.acquire(sp,nonwr)['status']=='UNSUPPORTED_RAW_ARCHITECTURE'
extra=raw+[(z,B,1),(B,z,1)];assert s.acquire(sp,extra)['status']=='UNSUPPORTED_RAW_ARCHITECTURE'
# Null normalization does not change the receipt; rate splitting is handled anew.
assert s.acquire(sp,raw+[((1,1,1),(1,1,1),F(123))])==receipt
split=[(raw[0][0],raw[0][1],F(1,3)),(raw[0][0],raw[0][1],F(2,3))]+raw[1:]
split_receipt=s.acquire(sp,split);assert split_receipt['status']=='QUALITATIVE_CERTIFIED';s.verify(sp,split,split_receipt)
perm=(2,0,1);rp=[(tuple(u[i] for i in perm),tuple(v[i] for i in perm),k) for u,v,k in raw]
permuted=s.acquire([sp[i] for i in perm],rp);assert permuted['role']['pivot']==1 and permuted['status']=='QUALITATIVE_CERTIFIED'

# A million-order encoded source: qualitative acquisition must not expand it,
# search polynomial degrees, calculate scalar Euler bounds or call stationary laws.
order=10**6;highraw=[((0,0),(1,0),1),((1,0),(0,0),1),((0,order),(1,order-1),1),((1,order-1),(0,order),1)]
old_support=p.support_certificate;blocked={k:getattr(p,k) for k in ['construct','build_cone','acquire_degree']}
def deny(*args,**kwargs):raise AssertionError('qualitative interface attempted quantitative work')
def guarded_support(rec,include_formal_bounds=True):
 assert include_formal_bounds is False
 return old_support(rec,include_formal_bounds=False)
p.support_certificate=guarded_support
for k in blocked:setattr(p,k,deny)
try:high=s.acquire(['A','B'],highraw);s.verify(['A','B'],highraw,high)
finally:
 p.support_certificate=old_support
 for k,v in blocked.items():setattr(p,k,v)
assert high['status']=='QUALITATIVE_CERTIFIED' and high['role']['leading_order']==order and high['work']['Euler_steps_executed']==high['work']['polynomial_degrees_searched']==0

invalid=[]
for name,ss,rr in [('scalar',['A'],[((0,),(1,),1),((1,),(0,),1)]),('duplicate_names',['A','A'],highraw),('float_rate',['A','B'],[(u,v,float(k)) for u,v,k in highraw])]:
 try:s.acquire(ss,rr)
 except ValueError:invalid.append(name)
 else:raise AssertionError('invalid API input accepted '+name)

print(json.dumps({'new_receiver_sha256':hashlib.sha256((HERE/'frozen_structural_receiver.py').read_bytes()).hexdigest(),
 'old_receiver_sha256':hashlib.sha256((HERE/'original_structural_receiver_be9c6a31.py').read_bytes()).hexdigest(),
 'accounting_regression':{'old_accepted_zero_work':True,'new_rejected_zero_work':True,'new_reason':zero_reason},
 'frozen_qualitative_receipt_rebuilt_exactly':True,'rejected_receipt_or_bound_raw_tampers':rejected,
 'stable_all_degree_obstruction':negative,'null_normalization_unchanged':True,'split_rate_certified':True,
 'permuted_pivot_reacquired':permuted['role']['pivot'],'million_order_qualitative_only_receipt':high,
 'guarded_quantitative_entrypoints_never_called':True,'invalid_API_cases_rejected':invalid},indent=2))
