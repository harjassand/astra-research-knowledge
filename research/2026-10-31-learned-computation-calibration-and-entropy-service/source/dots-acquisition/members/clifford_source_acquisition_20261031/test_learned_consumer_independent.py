"""Independent composition boundary tests; not teacher-truth verification."""
import copy, json
from pathlib import Path
from learn_affine_source import learn_and_compile, SCOPE
from acquire_learned_pauli_consumer import acquire_learned_coupling
P=Path(__file__).parent
T=json.loads((P/'examples/learned_history.transcript.json').read_text())
R=learn_and_compile(T)
C={'system_qubits':1,'terms':[{'coefficient':'1','system_x':1,'system_z':0,'source_x':0,'source_z':1}]}
def reject(t,r,c):
    try: acquire_learned_coupling(t,r,c)
    except ValueError: return
    raise AssertionError('invalid composition accepted')
rejects=0
for r in [None,[],0,'',{}, {'transcript_digest':R['transcript_digest']}]:
    reject(T,r,C); rejects+=1
for t in [None,[],{},dict(T,unknown=True)]:
    reject(t,R,C); rejects+=1
for key,value in SCOPE.items():
    r=copy.deepcopy(R); r[key]=int(value) if isinstance(value,bool) else 'forged'
    reject(T,r,C); rejects+=1
for key in ['unconditional_model_failure_upper_bound','admitted_transcript_average_failure_upper_bound']:
    r=copy.deepcopy(R)
    if key.startswith('unconditional'): r['query_plan']['proved_failure_upper_bound']='0'
    else: r[key]='0'
    reject(T,r,C); rejects+=1
for c in [None,[],{},dict(C,system_qubits=True)]:
    reject(T,R,c); rejects+=1
c=copy.deepcopy(C); c['terms'][0]['source_x']=1; c['terms'][0]['coefficient']='1/'+str(2**300)
reject(T,R,c); rejects+=1
# Exact combined cancellation, not termwise syntactic rejection.
c=copy.deepcopy(C); term=dict(c['terms'][0],source_x=1,coefficient='1/3')
c['terms'] += [term,dict(term,coefficient='-1/3')]
a=acquire_learned_coupling(T,R,c)
assert a['source_diagonal_coupling_verified'] is True
assert a['future_control_instrument_algebra_verified'] is False
assert a['downstream_simulation_executed'] is False
assert a['acquisition_query_count']==len(R['query_plan']['inputs'])
assert all(a[k]==v and (type(v)!=bool or a[k] is v) for k,v in SCOPE.items())
before=copy.deepcopy((T,R,C)); acquire_learned_coupling(T,R,C); assert before==(T,R,C)
# Unknown injected confidence/output claims are never copied through.
r=copy.deepcopy(R); r['downstream_simulation_executed']=True; r['posterior_truth']=True
out=acquire_learned_coupling(T,r,C)
assert out['downstream_simulation_executed'] is False and 'posterior_truth' not in out
rare=json.loads((P/'examples/rare_wrong_admitted_transcript.json').read_text())
out=acquire_learned_coupling(rare['transcript'],rare['record'],C)
assert out['model_family_promise_verified_from_data'] is False and out['rare_postselection_covered'] is False
result={'passed':True,'rejected_cases':rejects,'exact_cancellation_accepted':True,'input_mutation':False,'untrusted_extra_claims_not_propagated':True,'wrong_admitted_record_retains_limits':True}
(P/'learned_consumer_independent_checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
