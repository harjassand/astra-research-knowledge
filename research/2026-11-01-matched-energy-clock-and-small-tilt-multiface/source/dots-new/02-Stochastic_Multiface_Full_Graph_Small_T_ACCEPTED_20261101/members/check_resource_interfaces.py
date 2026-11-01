from pathlib import Path
from fractions import Fraction as Q
import os,sys,json,hashlib,time,copy
import independent_receiver as I
H=Path(__file__).resolve().parent;S=Path(os.environ['MULTIFACE_SOURCE_DIR']);sys.path.insert(0,str(S))
import multiface as M,receive_certificate as R,api
from certificate_guard import guard_tree
C={}
def add(k,n=1):C[k]=C.get(k,0)+n
def refuses(f,types=(Exception,)):
 try:f()
 except types:return
 raise AssertionError('expected refusal')
start=time.monotonic();raw=I.fixture();p=I.construct(raw);certificate=I.encoded(p)
# Every malformed graph is rejected before calling the expensive producer.
cyclic={};cyclic['cycle']=cyclic
cl=[];cl.append(cl)
shared=[]
deep=0
for _ in range(100):deep={'next':deep}
bad=[cyclic,{'cycle':cl},{'a':shared,'b':shared},deep,{1:'bad'},{'bad':object()},{'wide':[0]*100001}]
original=R.certificate
try:
 def forbidden(*a,**k):raise AssertionError('malformed input reached producer')
 R.certificate=forbidden
 for claim in bad:
  refuses(lambda:R.receive(raw,claim),(M.BudgetRefusal,));add('malformed_tree_rejected_before_producer')
 for claim in [None,[],True,1,'x']:
  assert R.receive(raw,claim)is False;add('non_dictionary_rejected_before_producer')
finally:R.certificate=original
for depth in [0,1,2,10,63,64]:
 tree=0
 for _ in range(depth):tree=[tree]
 receipt=guard_tree(tree,max_depth=depth,max_nodes=depth+1);assert receipt['proof_nodes']==depth+1;add('exact_tree_budget_boundaries')
 if depth:refuses(lambda:guard_tree(tree,max_depth=depth-1,max_nodes=depth+1),(M.BudgetRefusal,));add('tree_depth_boundary_refusals')
 refuses(lambda:guard_tree(tree,max_depth=depth,max_nodes=max(1,depth)),(M.BudgetRefusal,))if depth else None
for tree in [[0]*9,{'a':[0]*4,'b':[0]*4}]:
 refuses(lambda:guard_tree(tree,max_nodes=9),(M.BudgetRefusal,));add('pending_node_preallocation_refusals')
for depth,nodes in [(True,10),(-1,10),(1,True),(1,0),(Q(1),10),(1,10.0)]:
 refuses(lambda:guard_tree(certificate,max_depth=depth,max_nodes=nodes),(ValueError,));add('tree_budget_domain_refusals')
# Deep valid arithmetic must be exact or a declared budget refusal, not RecursionError.
for depth in [0,1,63,64,1100,3000]:
 expr=1
 for _ in range(depth):expr={'op':'mul','args':[expr]}
 assert R.evaluate_expression(expr,max_depth=2*depth+1,max_nodes=4*depth+10)==1
 assert I.eval_expression(expr,max_depth=depth+1,max_nodes=depth+2)==1
 add('raised_depth_iterative_exact_values')
 if depth:refuses(lambda:R.evaluate_expression(expr,max_depth=2*depth-1,max_nodes=4*depth+10),(M.BudgetRefusal,));add('raised_depth_declared_refusals')
# Guard all ignored/extra subtrees before arithmetic, and reject malformed arithmetic grammar.
expr_bad=[{'op':'mul','args':{'2':3}},{'op':'mul','args':'2'},{'op':'mul','args':None},{'op':'pow','base':2},{'op':'mul'}, {'op':'pow','base':2,'exponent':True}]
for expr in expr_bad:
 refuses(lambda:R.evaluate_expression(expr),(ValueError,M.BudgetRefusal));add('arithmetic_shape_refusals')
cycle={'op':'mul'};cycle['args']=[cycle];part={'op':'pow','base':2,'exponent':1}
for expr in [cycle,{'op':'mul','args':[part,part]}]:
 refuses(lambda:R.evaluate_expression(expr),(M.BudgetRefusal,));add('expression_cycle_alias_refusals')
for expr,truth in [({'op':'pow','base':2,'exponent':2,'ignored':3},4),({'op':'mul','args':[],'ignored':3},1)]:
 assert R.evaluate_expression(expr)==truth;add('guarded_standalone_extra_fields_disclosed')
extra={'op':'pow','base':2,'exponent':2,'ignored':[0]*100}
refuses(lambda:R.evaluate_expression(extra,max_nodes=50),(M.BudgetRefusal,));add('unused_extra_subtree_fully_charged')
# Actual huge-rate quantitative construction and wire reception, not just recognition.
big=I.fixture(2,((0,1),));big[0]=(*big[0][:2],Q(1<<20000));before=sys.get_int_max_str_digits();mine=I.construct(big);candidate=M.construct(big)
assert I.strict_equal(I.encoded(mine),M.encode(candidate));wire=json.dumps(M.encode(candidate),sort_keys=True).encode();assert I.receive(big,wire);assert R.receive(big,json.loads(wire));add('giant_rate_complete_exact_receipt',3)
assert before==sys.get_int_max_str_digits();add('global_decimal_guard_unchanged')
for value in [1<<20000,Q(1<<20000),Q(-(1<<20000),3),Q(1,1<<20000)]:
 node=I.encoded(value);assert I.eval_expression(node)==R.evaluate_expression(node)==value;add('exact_hex_tag_receiving')
for node in [I.encoded(mine['CF_expression']),I.encoded(mine['moment_bound_expression'])]:
 refuses(lambda:I.eval_expression(node,max_power_bits=10000),(I.UnknownComputation,));refuses(lambda:R.evaluate_expression(node,max_power_bits=10000),(M.BudgetRefusal,));add('giant_tagged_head_refusals')
# A low memory/expansion budget cannot be relabeled as an emitted numeric moment.
q=api.construct(big,max_masks=0);assert q['stability_refuted']is False and 'certificate'not in q and 'moment_bound_expression'not in q;add('giant_refusal_qualitative_only')
result={'status':'PASS_INDEPENDENT_TREE_RESOURCE_AND_GIANT_RATE_INTERFACES','source_manifest_sha256':hashlib.sha256((S/'AUTHOR_FREEZE_MANIFEST.json').read_bytes()).hexdigest(),'counts':C,'actual_certificate_guard':guard_tree(certificate),'giant_rate_certificate_bytes':len(wire),'giant_rate_Nstar_bits':mine['Nstar'].bit_length(),'giant_rate_t_numerator_bits':mine['t'].numerator.bit_length(),'giant_rate_t_denominator_bits':mine['t'].denominator.bit_length(),'giant_head_powers_expanded':False}
(H/'RESOURCE_INTERFACE_RESULTS.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':result['status'],'counts':C,'elapsed_seconds':time.monotonic()-start},sort_keys=True))
