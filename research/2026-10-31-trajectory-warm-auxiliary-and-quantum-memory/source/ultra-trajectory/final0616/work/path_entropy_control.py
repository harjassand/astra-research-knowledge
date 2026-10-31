#!/usr/bin/env python3
"""Exact finite controls for realised-path entropy confidence bounds."""
from fractions import Fraction as Q
from pathlib import Path
import json
import sys
import time

ROOT=Path(__file__).resolve().parents[1]
HERE=ROOT/'outputs/reversible_currents'
sys.path.insert(0,str(HERE))
from currents import log_bounds
from dual_trace import load_certificate
from path_entropy import current_bound,current_grid_bound,dual_bound,reflection_bound,sequential_current_bound
from ctmc_reflection_control import CountedBits


def endpoint(result):
    r=result['lower_endpoint']
    return Q(int(r['numerator']),int(r['denominator']))


def source_record(b,steps,seed):
    bits=CountedBits(seed)
    state=bits.below(4);s=1 if state<2 else -1;t=1 if state%2==0 else -1
    record=[int(s<0)];net=0;p=(1+b)/2
    for _ in range(steps):
        eta=1 if bits.below(p.denominator)<p.numerator else -1
        net+=eta
        k=s*t*eta
        if k==1:t=-t
        else:s=-s
        record.append(int(s<0))
    return record,net,{'stationary_initializations':1,'transitions':steps,
        'observations':steps+1,'random_bits_generated':bits.bits,
        'synthetic_source':'exact four-state source via independent rational driving signs'}


def sharp_joint_control():
    # theta=1/4,c=1/2. Choose biased cycle p/q=(6/5)^4, so
    # the fractional-power tilted masses A and B are rational.
    p,q=Q(1296,1921),Q(625,1921)
    t=p-q;c=Q(1,2);v=t/c
    assert 0<v<1
    A,B=Q(1080,1921),Q(750,1921)
    exp_lambda_squared=(1+v)/(1-v)*Q(25,36)
    C_squared=(1-c*c*v*v)/(1-v*v)
    tilted_sum_squared=A*A*exp_lambda_squared+2*A*B+B*B/exp_lambda_squared
    assert tilted_sum_squared==C_squared
    assert A**4==p**3*q and B**4==q**3*p
    return {'theta':'1/4','cycle_forward_probability':str(p),
        'cycle_backward_probability':str(q),'v':str(v),
        'exp_lambda_squared':str(exp_lambda_squared),'C_squared':str(C_squared),
        'exact_joint_exponential_bound_equality':True,
        'all_n_reason':'iid directional increments and one-step equality, positive square roots'}


def finite_recovery_power():
    # Uniform source-specific power for a substantial fraction, in addition
    # to the all-model path-entropy coverage theorem. No extra data acquired.
    n=6000;radius=230;alpha=Q(1,120);count=42
    assert Q(radius*radius,2*n)>log_bounds(Q(80))[1]
    loM,hiM=n//2-radius,n//2+radius
    l3lo,l3hi=log_bounds(Q(3))
    endpoints={}
    for M in (loM,hiM):
        record=[0];positive=(n+M)//2
        for t in range(n):
            k=(1 if t<positive else -1)*(-1 if t%2 else 1)
            record.append(record[-1] if k==1 else 1-record[-1])
        # Each candidate is affine in the positive score M before its final
        # downward dyadic rounding. Endpoints suffice for the whole interval.
        for theta in [Q(1,2**j) for j in range(1,7)]:
            for v in [Q(j,8) for j in range(1,8)]:
                result=current_bound(record,theta,v,alpha/count)
                assert endpoint(result)+Q(1,2**96)<M*l3lo
        fixed=current_bound(record,Q(1,16),Q(1,2),alpha/count)
        assert endpoint(fixed)-Q(1,2**96)>Q(3,4)*M*l3hi
        endpoints[str(M)]={'lower_fixed_candidate':fixed['lower_preview'],
            'actual_entropy_lower':float(M*l3lo)}
    return {'source':'four-state b=1/2','transitions':n,'observed_bits':n+1,
        'one_stationary_preparation':True,'fixed_grid_coverage_risk':'1/120',
        'guarantee':'selected current-grid lower endpoint lies between 75% and 100% of actual hidden path entropy',
        'probability_at_least':'39/40','proof':
            'two-sided iid driving-sign Hoeffding: P(|M-3000|>230)<=2 exp(-529/120)<1/40; '
            'all candidate affine upper checks and one candidate 75% lower check at both endpoints',
        'endpoint_checks':endpoints,'source_power_not_a_general_hidden_model_power_claim':True}


def main():
    start=time.perf_counter();alpha=Q(1,40)
    cert=load_certificate(HERE/'symmetric_dual.json')
    discrete=[]
    for name,b,seed in [('sharp_driven',Q(1,2),202610313),('reversible_null',Q(0),202610314)]:
        record,net,cost=source_record(b,6000,seed)
        (HERE/(name+'_path_record.json')).write_text(json.dumps(record)+'\n')
        # The chosen maximum across all THREE methods has overall risk alpha.
        grid=current_grid_bound(record,alpha/3)
        reflection=reflection_bound(record,Q(1,10),alpha/3)
        dual=dual_bound(cert,record,Q(1,4),alpha/3)
        best=max([grid['best'],reflection,dual],key=endpoint)
        loglo,loghi=log_bounds((1+b)/(1-b))
        actual_lo,actual_hi=min(net*loglo,net*loghi),max(net*loglo,net*loghi)
        assert endpoint(best)<=actual_lo
        row={'name':name,'source_b':str(b),'cost':cost,'net_driving_signs':net,
            'realised_hidden_entropy_expression':f'{net} log({(1+b)/(1-b)})',
            'realised_hidden_entropy_preview':float(actual_lo),
            'current_grid':grid,'reflection':reflection,'predictive_dual':dual,
            'three_method_family_risk':str(alpha),'selected':best}
        sequence=sequential_current_bound(record,alpha)
        assert endpoint(sequence['best'])<=actual_lo
        row['separate_time_uniform_rule']={'result':sequence,
            'comparison_scope':'separate rule, not selected into the three-method maximum'}
        if actual_lo>0:row['certified_fraction_of_actual_path_entropy']=float(endpoint(best)/actual_hi)
        discrete.append(row)
    # Full continuous-time path entropy, not an assumed sampled entropy.
    ctmc=json.loads((HERE/'ctmc_receipt.json').read_text())
    continuous=[]
    for r in ctmc['acquisitions']:
        record=json.loads((HERE/(r['name']+'_record.json')).read_text())
        bound=reflection_bound(record,Q(1,10),alpha)
        net=r['cost']['net_oriented_jumps']
        ratio=Q(r['forward_rate'])/Q(r['backward_rate'])
        lo,hi=log_bounds(ratio)
        actual_lo,actual_hi=min(net*lo,net*hi),max(net*lo,net*hi)
        assert endpoint(bound)<=actual_lo
        continuous.append({'name':r['name'],'bound':bound,
            'actual_full_path_entropy':f'{net} log({ratio})',
            'actual_full_path_entropy_preview':float(actual_lo),
            'acquisition_reused':'ctmc_receipt.json, no new sample or stationary preparation'})
    # Do NOT clamp a path endpoint to zero: this would fail at probability
    # 99/200 in a one-step cycle with driving sign probability101/200.
    assert Q(99,200)>alpha
    weak=current_bound([0,0],Q(1,2),Q(1,2),alpha)
    assert endpoint(weak)<0
    asymptotics=[]
    # Deterministic typical-score controls check formula convergence; these
    # are not additional acquired samples and do not prove the limit theorem.
    b=Q(1,2);elo,ehi=log_bounds(Q(3));elo*=b;ehi*=b
    for n,theta in [(1000,Q(1,8)),(10000,Q(1,16)),(100000,Q(1,32)),(1000000,Q(1,64))]:
        # A record with score n/2 is constructed at zero source-acquisition
        # claim; evaluate its actual observable score through the public API.
        positives=3*n//4;record=[0]
        for t in range(n):
            g=1 if t<positives else -1
            k=g*(-1 if t%2 else 1)
            record.append(record[-1] if k==1 else 1-record[-1])
        result=current_bound(record,theta,b,alpha)
        lower=endpoint(result)/n
        sequence=sequential_current_bound(record,alpha)
        seq_lower=endpoint(sequence['best'])/n
        asymptotics.append({'n':n,'theta':str(theta),'score_fraction':'1/2',
            'endpoint_per_step_preview':float(lower),
            'fraction_of_exact_source_rate_lower':float(lower/ehi),
            'implemented_sequential_rule_fraction':float(seq_lower/ehi),
            'implemented_sequence_theta':sequence['theta_schedule'],
            'sample_status':'constructed typical-score input, not acquired data'})
    output={'scope':__doc__,'target':'realised hidden total path entropy, NOT stationary ensemble mean rate',
        'sharp_joint_control':sharp_joint_control(),'finite_recovery_power':finite_recovery_power(),
        'discrete_acquisitions':discrete,
        'full_CTMC_path_controls':continuous,'negative_endpoint_control':{
            'clamping_to_zero_would_fail_with_probability':'99/200',
            'actual_endpoint_retained_negative':weak},
        'typical_score_limit_diagnostics':asymptotics,
        'cost_of_diagnostics':'two additional 6000-step discrete records; existing CTMC records reused; constructed inputs explicitly labelled',
        'seconds':time.perf_counter()-start,'status':'ALL_PATH_ENTROPY_FINITE_CONTROLS_PASSED'}
    (HERE/'path_entropy_receipt.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({'status':output['status'],'seconds':output['seconds'],
        'discrete':[{'name':r['name'],'actual_entropy':r['realised_hidden_entropy_preview'],
            'certified_lower':r['selected']['lower_preview'],
            'certified_fraction':r.get('certified_fraction_of_actual_path_entropy'),
            'selected_theta':r['selected'].get('theta'),'selected_v':r['selected'].get('v')}
            for r in discrete],
        'CTMC':[{'name':r['name'],'lower':r['bound']['lower_preview'],
            'actual':r['actual_full_path_entropy_preview']} for r in continuous],
        'typical_score_diagnostics':asymptotics},indent=2))


if __name__=='__main__':main()
