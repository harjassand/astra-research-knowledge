"""Root-authorized delta1 extension and decisive negative/rejection controls."""
from copy import deepcopy
from fractions import Fraction as F
import json
from pathlib import Path
import random
import time

from dicke_compiler import (as_record,from_record,compile_state,verify_model,
                            exp_negative_interval,numeric_quadrature,sample_product)
from check_dicke_compiler import independent_population_error

HERE=Path(__file__).resolve().parent


def run():
    start=time.perf_counter()
    rng=random.Random(20261008)
    records=[]
    models=[]
    for n in [2,3,8,16,32,64]:
        for h in ['0','1/3']:
            model=compile_state(n,'1',h,epsilon='1e-20')
            assert verify_model(model)
            numeric=independent_population_error(model)
            sample=sample_product(model,rng)
            assert sample['random_bits_consumed']==model['predetermined_random_bits_per_sample']
            models.append(model)
            records.append({'n':n,'delta':'1','h':h,'verified':True,
                            'compile_seconds':model['compile_seconds'],
                            'node_count':len(model['node_integers']),
                            'total_trace_distance_upper':model['total_output_trace_distance_upper'],
                            'numeric_population_diagnostic':numeric,
                            'finite_sample_PSD_exact':True})
    control=next(m for m in models if m['n']==8 and from_record(m['h'])==F(1,3))
    corruptions=[]
    for name,mutate in [
        ('node_outside_support',lambda m:m['node_integers'].__setitem__(0,'-1')),
        ('node_inside_support_but_wrong',lambda m:m['node_integers'].__setitem__(1,'0')),
        ('weight_normalization_corrupted',lambda m:m['weight_integers'].__setitem__(0,str(int(m['weight_integers'][0])+1))),
        ('false_zero_population_certificate',lambda m:m['certificate'].__setitem__('target_trace_distance_upper',as_record(0))),
        ('false_zero_total_error',lambda m:m.__setitem__('total_output_trace_distance_upper',as_record(0))),
        ('false_zero_phase_bias',lambda m:m.__setitem__('phase_uniform_TV_upper',as_record(0))),
        ('illegal_parameter_domain',lambda m:m.__setitem__('delta',as_record(2))),
        ('wrong_phase_modulus',lambda m:m.__setitem__('phase_modulus',1)),
        ('wrong_phase_sampling_bits',lambda m:m.__setitem__('phase_sampling_bits',0)),
        ('wrong_density_precision',lambda m:m.__setitem__('density_bits',1)),
        ('wrong_format',lambda m:m.__setitem__('format','UNVERIFIED_GENERIC_STATE')),
        ('wrong_component_count',lambda m:m.__setitem__('component_count',1)),
        ('wrong_random_bit_count',lambda m:m.__setitem__('predetermined_random_bits_per_sample',0)),
        ('wrong_node_dimension',lambda m:m['node_integers'].append('0')),
        ('inflated_component_phase_budget',lambda m:m.__setitem__('phase_uniform_TV_upper',as_record(F(1,10)))),
        ('inflated_component_density_budget',lambda m:m.__setitem__('finite_density_trace_distance_upper',as_record(F(1,10)))),
    ]:
        bad=deepcopy(control)
        mutate(bad)
        try:
            verify_model(bad)
        except (AssertionError,ValueError,ArithmeticError):
            corruptions.append({'name':name,'status':'REJECTED'})
        else:
            raise AssertionError('corruption accepted: '+name)
    # Outside-domain obstruction is mathematical, not merely the input guard.
    alo,ahi,_=exp_negative_interval(F(1),180)
    p2lo,p2hi=alo/(1+2*ahi),ahi/(1+2*alo)
    determinant=(p2lo-F(1,4),p2hi-F(1,4))
    assert determinant[1]<0
    witness_gap=1/(1+2*ahi)-F(1,2)
    assert witness_gap>0
    guard_rejected=bypass_cholesky_rejected=False
    try:
        compile_state(2,'2','0')
    except ValueError:
        guard_rejected=True
    try:
        numeric_quadrature(2,F(2),F(0),100)
    except (ValueError,ArithmeticError):
        bypass_cholesky_rejected=True
    assert guard_rejected and bypass_cholesky_rejected
    outside={'n':2,'delta':'2','h':'0',
             'ordinary_moment_H_determinant_interval':[as_record(x) for x in determinant],
             'proof':'H=[[1,1/2],[1/2,a/(1+2a)]], a=exp(-1)<1/2; determinant<0',
             'separable_witness':'Dicke Bell-state population <=1/2 for every separable state',
             'target_trace_distance_from_any_separable_state_lower':as_record(witness_gap),
             'input_guard_rejected':guard_rejected,'bypass_Cholesky_rejected':bypass_cholesky_rejected}
    # Exercise accepted adaptive refinement, as distinct from fail-closed path.
    refined=compile_state(8,'1','1/3',epsilon='1e-5',bits=2,density_bits=2,max_attempts=3)
    assert verify_model(refined)
    assert len(refined['acquisition_attempts'])>=2
    result={'status':'PASS','cases':len(records),'records':records,'models':models,
            'corruption_controls':corruptions,'outside_domain_control':outside,
            'adaptive_refinement_attempts':refined['acquisition_attempts'],
            'elapsed_seconds':time.perf_counter()-start,
            'preserved_half_receipt':'half_domain/MANIFEST.json; accepted 70-case suite untouched',
            'mathematical_domain_source':'c07_s02 AXIAL_ONE_CERTIFICATE and authorized independent audits; no priority/external validation claim'}
    text=json.dumps(result,indent=2)+'\n'
    (HERE/'delta1_checks.json').write_text(text)
    print(json.dumps({'status':'PASS','cases':len(records),'corruptions':len(corruptions),
                      'elapsed_seconds':time.perf_counter()-start,'output_bytes':len(text.encode())}),flush=True)


if __name__=='__main__':
    run()
