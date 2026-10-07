"""Runnable N<=3 whole finite-alpha axial Gibbs compiler and sampler.

Bounded prototype: a direct rational K0/KN solve fits at most two spin sectors.
Every accepted output gets an independent rational full-matrix certificate.
Reads peer acquisition helper without mutating it. No polynomial LP claim.
"""
import argparse
from fractions import Fraction as F
import hashlib
from itertools import combinations
import json
import math
from pathlib import Path
import random
import time

from dicke_compiler import (as_record,from_record,compile_state,verify_model,
                            ceil_log2_reciprocal,sample_product,outward_dyadic)
from check_finite_alpha import (peer,PEER_SOURCE,recursive_record,mixture_matrix,
                                target_matrix_intervals)


def direct_small_spin_backend(qhat,columns):
    """Exact K0/KN solve for N<=3, whose spin table has at most two rows."""
    N=len(columns)-1
    if N not in (1,2,3) or len(qhat)>2:
        raise ValueError('direct bounded backend only supports N<=3')
    if len(qhat)==1:
        return [F(int(k==0)) for k in range(N+1)],F(0)
    lower_in_white=columns[0][1]
    assert lower_in_white>0 and columns[N][1]==0
    white_weight=F(qhat[1])/lower_in_white
    assert 0<=white_weight<=1
    weights=[F(0) for _ in range(N+1)]
    weights[0],weights[N]=white_weight,1-white_weight
    fit=peer.matvec([[col[b] for col in columns] for b in range(len(qhat))],weights)
    objective=peer.total_variation(qhat,fit)
    assert objective==0
    return weights,objective


def compile_whole_gibbs(N,alpha='1/2',delta='1',h='1/3',epsilon='1e-12'):
    start=time.perf_counter()
    alpha,delta,h,epsilon=map(F,(alpha,delta,h,epsilon))
    if N not in (1,2,3):
        raise ValueError('bounded whole-Gibbs compiler requires N in {1,2,3}')
    if not 0<=alpha<=16 or not 0<=delta<=1 or not abs(h)<=8:
        raise ValueError('bounded whole-Gibbs parameters: 0<=alpha<=16,0<=delta<=1,|h|<=8')
    if not F('1e-80')<=epsilon<F(1):
        raise ValueError('bounded whole-Gibbs accuracy requires 1e-80<=epsilon<1')
    w,meta=peer.acquire_k_weights(N,alpha,delta,h,epsilon,
                                  lp_backend=direct_small_spin_backend)
    assert w is not None and sum(w)==1 and min(w)>=0
    branches,bmeta=peer.acquire_branches(N,delta,h,w,epsilon)
    models=[]
    for branch in branches:
        k=branch['k']
        model=compile_state(k,delta*F(k,N),h-2*delta*branch['m']/N,
                            epsilon=min(epsilon/64,F('1e-30')))
        assert verify_model(model)
        models.append(model)
    rho=mixture_matrix(N,branches,models)
    exp_bits=max(180,ceil_log2_reciprocal(epsilon)+32)
    interval=target_matrix_intervals(N,alpha,delta,h,exp_bits)
    raw=F(0)
    for i,row in enumerate(rho):
        for j,value in enumerate(row):
            lo,hi=interval[i][j]
            raw+=max(abs(value-lo),abs(value-hi))
    matrix_bound=outward_dyadic(raw/2,exp_bits,True)
    rank_bits=max(128,ceil_log2_reciprocal(epsilon)+16)
    preparation=F(0)
    for branch,model in zip(branches,models):
        k,u=branch['k'],branch['u']
        bias=(F(math.comb(N,k)+math.comb(N-k,u),2*(1 << rank_bits))
              +from_record(model['phase_uniform_TV_upper'])
              +from_record(model['finite_density_trace_distance_upper']))
        preparation+=branch['probability']*bias
    bound=matrix_bound+preparation
    if bound>epsilon:
        raise ArithmeticError('full-state posterior certificate failed; output rejected')
    outer_bits=max(b['probability'].denominator.bit_length()-1 for b in branches)
    max_inner_bits=max(inner['predetermined_random_bits_per_sample'] for inner in models)
    result={'format':'WHOLE_AXIAL_GIBBS_CERTIFIED_BOUNDED_V1','N':N,
            'alpha':as_record(alpha),'delta':as_record(delta),'h':as_record(h),
            'epsilon':as_record(epsilon),'K_weights':recursive_record(w),
            'LP_metadata':recursive_record(meta),'branch_metadata':recursive_record(bmeta),
            'branches':recursive_record([{'k':b['k'],'u':b['u'],'probability':b['probability']} for b in branches]),
            'Dicke_models':models,'uniform_rank_bits':rank_bits,
            'outer_sampling_bits':outer_bits,'max_inner_sampling_bits':max_inner_bits,
            'predetermined_random_bits_per_sample':outer_bits+2*rank_bits+max_inner_bits,
            'target_matrix_exp_interval_bits':exp_bits,
            'full_matrix_trace_distance_upper':as_record(matrix_bound),
            'finite_sampler_additional_error_upper':as_record(preparation),
            'total_target_trace_distance_upper':as_record(bound),
            'compile_seconds':time.perf_counter()-start,
            'LP_backend':'owned direct K0/KN two-sector formula for N<=3; generic LP not called',
            'peer_source':str(PEER_SOURCE),
            'peer_source_sha256':hashlib.sha256(PEER_SOURCE.read_bytes()).hexdigest(),
            'certificate':'Independent exact joint-spin projector target intervals and candidate matrix; half entrywise L1 bounds trace distance'}
    return result


def verify_whole_model(model):
    assert model['format']=='WHOLE_AXIAL_GIBBS_CERTIFIED_BOUNDED_V1'
    N=model['N']
    alpha,delta,h=map(from_record,(model['alpha'],model['delta'],model['h']))
    assert type(N) is int and N in (1,2,3) and 0<=alpha<=16 and 0<=delta<=1 and abs(h)<=8
    assert F('1e-80')<=from_record(model['epsilon'])<1
    assert type(model['uniform_rank_bits']) is int and model['uniform_rank_bits']>=1
    assert type(model['target_matrix_exp_interval_bits']) is int and model['target_matrix_exp_interval_bits']>=1
    assert type(model['outer_sampling_bits']) is int and model['outer_sampling_bits']>=0
    assert type(model['max_inner_sampling_bits']) is int and model['max_inner_sampling_bits']>=0
    assert type(model['predetermined_random_bits_per_sample']) is int
    branches=[{'k':b['k'],'u':b['u'],'probability':from_record(b['probability'])}
              for b in model['branches']]
    assert len(branches)==len(model['Dicke_models'])
    assert sum(b['probability'] for b in branches)==1 and min(b['probability'] for b in branches)>=0
    for b,inner in zip(branches,model['Dicke_models']):
        assert type(b['k']) is int and type(b['u']) is int
        assert 0<=b['k']<=N and 0<=b['u']<=N-b['k'] and inner['n']==b['k']
        assert b['probability'].denominator & (b['probability'].denominator-1)==0
        assert verify_model(inner)
        assert from_record(inner['delta'])==delta*F(b['k'],N)
        m=F(2*b['u']-(N-b['k']),2)
        assert from_record(inner['h'])==h-2*delta*m/N
    rho=mixture_matrix(N,branches,model['Dicke_models'])
    intervals=target_matrix_intervals(N,alpha,delta,h,model['target_matrix_exp_interval_bits'])
    error=F(0)
    for i,row in enumerate(rho):
        for j,value in enumerate(row):
            lo,hi=intervals[i][j]
            error+=max(abs(value-lo),abs(value-hi))
    assert error/2<=from_record(model['full_matrix_trace_distance_upper'])
    prep=F(0)
    rb=model['uniform_rank_bits']
    for b,inner in zip(branches,model['Dicke_models']):
        k,u=b['k'],b['u']
        prep+=b['probability']*(F(math.comb(N,k)+math.comb(N-k,u),2*(1 << rb))
                               +from_record(inner['phase_uniform_TV_upper'])
                               +from_record(inner['finite_density_trace_distance_upper']))
    assert prep<=from_record(model['finite_sampler_additional_error_upper'])
    assert prep+from_record(model['full_matrix_trace_distance_upper'])<=from_record(model['total_target_trace_distance_upper'])
    assert from_record(model['total_target_trace_distance_upper'])<=from_record(model['epsilon'])
    outer_bits=max(b['probability'].denominator.bit_length()-1 for b in branches)
    max_inner_bits=max(inner['predetermined_random_bits_per_sample'] for inner in model['Dicke_models'])
    assert model['outer_sampling_bits']==outer_bits and model['max_inner_sampling_bits']==max_inner_bits
    assert model['predetermined_random_bits_per_sample']==outer_bits+2*rb+max_inner_bits
    return True


def sample_whole_gibbs(model,rng=None):
    rng=random.SystemRandom() if rng is None else rng
    branches=model['branches']
    index=peer.sample_dyadic([from_record(b['probability']) for b in branches],rng)
    branch=branches[index]
    N,k,u=model['N'],branch['k'],branch['u']
    rb=model['uniform_rank_bits']
    choices=list(combinations(range(N),k))
    subset=choices[(rng.getrandbits(rb)*len(choices)) >> rb]
    complement=[i for i in range(N) if i not in subset]
    choices=list(combinations(complement,u))
    ones=choices[(rng.getrandbits(rb)*len(choices)) >> rb]
    component=sample_product(model['Dicke_models'][index],rng)
    pad=model['max_inner_sampling_bits']-component['random_bits_consumed']
    assert pad>=0
    if pad:
        rng.getrandbits(pad)
    states=[]
    for i in range(N):
        if i in subset:
            state=component['finite_product_local_density']
        else:
            bit=int(i in ones)
            state={'diagonal':[as_record(1-bit),as_record(bit)],
                   'upper_right_real':as_record(0),'upper_right_imag':as_record(0),
                   'PSD_and_trace_one_exact':True}
        diag=list(map(from_record,state['diagonal']))
        re,im=from_record(state['upper_right_real']),from_record(state['upper_right_imag'])
        assert sum(diag)==1 and diag[0]*diag[1]>=re*re+im*im
        states.append(state)
    return {'branch_index':index,'k':k,'u':u,'subset':list(subset),
            'random_bits_consumed':model['predetermined_random_bits_per_sample'],
            'complement_ones':list(ones),'local_density_matrices':states,
            'ensemble_target_trace_distance_upper':model['total_target_trace_distance_upper']}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--n',type=int,default=3)
    parser.add_argument('--alpha',default='3')
    parser.add_argument('--delta',default='1')
    parser.add_argument('--h',default='1/3')
    parser.add_argument('--epsilon',default='1e-12')
    parser.add_argument('--samples',type=int,default=4)
    parser.add_argument('--seed',type=int,default=20261008)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    model=compile_whole_gibbs(args.n,args.alpha,args.delta,args.h,args.epsilon)
    verify_whole_model(model)
    rng=random.Random(args.seed)
    result={'model':model,'samples':[sample_whole_gibbs(model,rng) for _ in range(args.samples)]}
    text=json.dumps(result,indent=2)+'\n'
    if args.output:
        args.output.write_text(text)
    else:
        print(text,end='')


if __name__=='__main__':
    main()
