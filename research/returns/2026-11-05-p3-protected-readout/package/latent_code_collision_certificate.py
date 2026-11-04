"""Exact acquisition certificates for the sparse parity-collision learner.

The local fault model and specimen-source validity are premises. These checks
do not certify a device or include a separate specimen-source delta_src.
"""
from fractions import Fraction as F
from pathlib import Path
import json
from latent_code_parameter_certificate import certify as old_certificate


def exp_tail_upper(numerator,x,target):
    """Return numerator/T_m(x), a rational upper bound on numerator*exp(-x)."""
    term=F(1);partial=F(1);degree=0
    while numerator/partial>=target:
        degree+=1
        assert degree<1000
        term*=x/degree;partial+=term
    return numerator/partial,degree


def acquisition_certificate(n,q,m,t,u,delta_time,miss_target,verify_target):
    a=1-4*q;b=F(1,2)+4*q;g=F(1,2)-8*q
    assert 0<q<F(1,36) and g>0
    assert b**t<=F(1,n*n)
    # This exact inequality proves alpha=2 log(1/a)/log(1/b)<1/2.
    assert b<a**4
    expected_collisions=m*(3*n+F(n*n,4))
    ratio=expected_collisions/delta_time
    H=(ratio.numerator+ratio.denominator-1)//ratio.denominator
    runtime=expected_collisions/H
    miss,md=exp_tail_upper(F(n),m*a**t/81,miss_target)
    verify,vd=exp_tail_upper(F(2*H),u*g*g/2,verify_target)
    total=miss+runtime+verify
    return {'N':n,'q_c':str(q),'a':str(a),'b':str(b),'g':str(g),
        'discovery_rows_t':t,'basis_rounds_m':m,'verification_rows_u':u,
        'collision_cap_H':H,'calibration_copies':m*(t+u),
        'pair_records':m*n*(n-1)//2,
        'calibration_wire_readouts':n*m*(t+u),
        'expected_collision_upper_rational':str(expected_collisions),
        'miss_failure_upper_rational':str(miss),
        'runtime_abort_upper_rational':str(runtime),
        'verification_failure_upper_rational':str(verify),
        'acquisition_failure_upper_rational':str(total),
        'Taylor_degrees':{'miss':md,'verification':vd},
        'decimal_display_only':{'miss':float(miss),'runtime_abort':float(runtime),'verification':float(verify),'total':float(total)},
        'exponent_alpha_less_than_one_half_certified':True,
        'specimen_source_delta_src_included':False}


def certify():
    finite=acquisition_certificate(50,F(1,200),1000,12,244,F(3,1000),F(3102,1000000),F(3176,1000000))
    assert F(finite['acquisition_failure_upper_rational'])<F(9278,1000000)<F(1,100)
    large=acquisition_certificate(11552,F(3,1000),1848,28,348,F(1,1000),F(1,1000),F(1,1000))
    prior=old_certificate()
    total=F(large['acquisition_failure_upper_rational'])+F(prior['all_rows_failure_upper_rational'])+F(prior['rank_failure_upper_rational'])
    assert total<F(7233,1000000)<F(1,100)
    large['Bell_rows']=prior['Bell_rows']
    large['total_source_copies']=large['calibration_copies']+2*prior['Bell_rows']
    large['physical_Bell_gates']=prior['physical_Bell_gates']
    large['full_learning_failure_upper_rational']=str(total)
    large['full_learning_failure_upper_decimal_display']=float(total)
    # One additional specimen/reference row completes the sign. Both prepared
    # banks use the same q budget; their factory approximation stays separate.
    one_row=F(prior['all_rows_failure_upper_rational'])/prior['Bell_rows']
    signed_total=total+one_row
    assert signed_total<F(7251,1000000)<F(1,100)
    large['signed_completion']={
        'additional_unknown_specimens':1,
        'additional_known_encoded_references':1,
        'corrected_Bell_rows':prior['Bell_rows']+1,
        'total_prepared_banks':large['total_source_copies']+2,
        'physical_Bell_gates':large['N']*(prior['Bell_rows']+1),
        'extra_row_failure_upper_rational':str(one_row),
        'full_failure_upper_rational':str(signed_total),
        'full_failure_upper_decimal_display':float(signed_total),
        'factory_and_control_approximation_budgets_included':False,
        'reference_preparation':'Known signed stabilizer state, prepared offline before the fresh specimen is requested; all local faults included in q.'}
    return {'arithmetic':'All assertions use fractions.Fraction and positive Taylor lower bounds for exponentials',
        'finite_execution_acquisition_parameters':finite,
        'larger_analytic_capability_point':large,
        'full_failure_bound':'reported bound plus separately supplied specimen-source delta_src',
        'scope':'The larger point is an analytic certificate, not an executed simulation. The small point certifies the collision/verification procedure under its explicit stochastic-support assumptions.'}


if __name__=='__main__':
    result=certify()
    Path(__file__).with_name('latent_code_collision_certificate.json').write_text(json.dumps(result,indent=2)+'\n')
    def compact(x):
        if isinstance(x,dict):return {k:compact(v) for k,v in x.items() if not k.endswith('_rational')}
        return x
    print(json.dumps(compact(result),indent=2))
