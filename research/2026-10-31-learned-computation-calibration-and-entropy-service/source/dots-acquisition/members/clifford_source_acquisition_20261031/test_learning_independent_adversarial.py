"""Independent confidence arithmetic, inference and scope/alias checks."""
import copy,hashlib,json,random
from fractions import Fraction
from itertools import product
from pathlib import Path
from learn_affine_source import (query_plan,learn_and_compile,verify_learning_record,
                                validate_transcript,sample_and_compile)
from acquire_clifford_source import linear

def run():
    arithmetic=0
    for den in range(2,81):
        for num in range(1,den):
            d=Fraction(num,den);p=query_plan(2,str(d));e=p['confidence_bits']
            assert Fraction(1,1<<e)<=d/2
            assert e==0 or Fraction(1,1<<(e-1))>d/2
            assert len(p['inputs'])==5+e and p['difference_samples']==2+e
            assert Fraction(p['proved_failure_upper_bound'])==Fraction(1,1<<e)
            b=Fraction(p['proved_failure_upper_bound']);assert b/(1-b)<=d
            arithmetic+=1
    for e in [50,127,500]:
        d=Fraction(1,(1<<e)+1);p=query_plan(1,str(d))
        assert Fraction(1,1<<p['confidence_bits'])<=d/2;arithmetic+=1
    # Zero-rank branch: deterministic affine data still learns exactly, but
    # does not become a controllable-uniform source by assertion.
    calls=[]
    def deterministic(x):calls.append(x);return x^3
    t,r=sample_and_compile(2,'1/3',deterministic)
    assert calls==query_plan(2,'1/3')['inputs']
    assert r['noise_basis']==[] and r['learned_model']=={'n':2,'F_columns':[1,2],'G_columns':[],'offset':3}
    assert r['realization']['status']=='outside_controllable_uniform_class'
    assert r['admitted_transcript_average_failure_upper_bound'] is None
    # Full-rank branch: all drift/offset information is genuinely invisible.
    p=query_plan(2,'1/4');M=p['difference_samples']
    outputs=[3]+[2,1]+[3]*(M-2)+[0,2]
    full={'n':2,'failure_probability':'1/4','outputs':outputs};fr=learn_and_compile(full)
    assert fr['quotient_columns']==[0,0]
    assert fr['learned_model']['F_columns']==[0,0] and fr['learned_model']['offset']==0
    assert fr['realization']['status']=='synthesized_uniform_pure_return'
    assert verify_learning_record(full,fr)
    # Returned objects may share internal lists, but not the supplied transcript;
    # correlated record edits cannot evade fresh recomputation.
    original=copy.deepcopy(full);bad=copy.deepcopy(fr)
    assert bad['noise_basis'] is bad['learned_model']['G_columns']
    bad['noise_basis'][0]^=1
    assert full==original and not verify_learning_record(full,bad)
    bad=copy.deepcopy(fr);bad['query_plan']['inputs'][0]=1
    assert not verify_learning_record(full,bad)
    bad=copy.deepcopy(fr);bad['admitted_transcript_average_failure_upper_bound']='0'
    assert not verify_learning_record(full,bad)
    bad=copy.deepcopy(fr);bad['query_plan']['proved_failure_upper_bound']='0'
    assert not verify_learning_record(full,bad)
    scope_keys=['model_family_promise_verified_from_data','rare_postselection_covered','known_clock_rate_required',
                'unknown_quantum_backaction_or_coupling_identified']
    for key in scope_keys:
        bad=copy.deepcopy(fr);bad[key]=not bad[key];assert not verify_learning_record(full,bad)
        bad=copy.deepcopy(fr);bad[key]=int(fr[key]);assert not verify_learning_record(full,bad)
    malformed=[None,[],0,'x',{},dict(full,n=0),dict(full,n=True),dict(full,outputs=tuple(outputs)),
               dict(full,outputs=outputs+[0]),dict(full,outputs=outputs[:-1]),dict(full,extra=True)]
    for delta in [True,False,0,1,'1/0','-1/2','3/2',.25,'1e-3']:
        malformed.append(dict(full,failure_probability=delta))
    for value in [True,-1,4,0.,None,[],{}]:
        out=outputs[:];out[0]=value;malformed.append(dict(full,outputs=out))
    for value in malformed:
        try:validate_transcript(value)
        except ValueError:pass
        else:raise AssertionError('Invalid transcript accepted')
        assert verify_learning_record(value,fr) is False
    for bad in [None,[],0,'x',{},dict(fr,query_plan=None),dict(fr,learned_model=None),dict(fr,realization=None)]:
        assert verify_learning_record(full,bad) is False
    # Enumerate actual full-noise n=1 transcripts at a non-dyadic confidence.
    p=query_plan(1,'2/3');admitted=wrong=total=0
    for outputs in product(range(2),repeat=len(p['inputs'])):
        t={'n':1,'failure_probability':'2/3','outputs':list(outputs)};r=learn_and_compile(t)
        assert verify_learning_record(t,r);total+=1
        if r['realization']['status']=='synthesized_uniform_pure_return':
            admitted+=1;wrong+=len(r['noise_basis'])!=1
    assert admitted>0 and Fraction(wrong,admitted)<=Fraction('2/3')
    root=Path(__file__).parent
    rare=json.loads((root/'examples/rare_wrong_admitted_transcript.json').read_text())
    assert verify_learning_record(rare['transcript'],rare['record'])
    assert len(rare['record']['noise_basis'])<2
    assert rare['record']['model_family_promise_verified_from_data'] is False
    # A nonlinear kernel can match every training-input distribution exactly.
    # This is OUTSIDE the promise and must not be called certified teacher truth.
    rng=random.Random(1142)
    def nonlinear(x):return linear([2,1],x)^(2 if x==3 else 0)^rng.randrange(2)
    nt,nr=sample_and_compile(2,'1/1048576',nonlinear)
    assert verify_learning_record(nt,nr) and nr['realization']['status']=='synthesized_uniform_pure_return'
    model=nr['learned_model'];learned_support={linear(model['F_columns'],3)^model['offset']^u for u in [0,1]}
    actual_support={linear([2,1],3)^2^u for u in [0,1]}
    assert learned_support!=actual_support and nr['model_family_promise_verified_from_data'] is False
    record={'source_sha256':hashlib.sha256((root/'learn_affine_source.py').read_bytes()).hexdigest(),
            'exact_confidence_boundary_checks':arithmetic,'zero_and_full_rank_branches':True,
            'alias_and_confidence_tampering_rejected':True,'scope_boolean_tampering_rejected':8,
            'malformed_transcripts_rejected':len(malformed),'malformed_records_rejected':8,
            'one_bit_full_noise_transcripts':total,'one_bit_admitted':admitted,
            'one_bit_admitted_wrong':wrong,'verified_wrong_dataset_not_promoted_to_truth':True,
            'nonlinear_outside_promise_counterexample_retained':True,'passed':True}
    path=root/'learning_independent_adversarial_checks.json';path.write_text(json.dumps(record,indent=2)+'\n');print(path.read_text())

if __name__=='__main__':run()
