#!/usr/bin/env python3
"""Exact rational finite-alphabet hidden-memory importance-sampling theorem replay.

Every proposed coin kernel, path probability, likelihood, expectation, and
sample bound is a Python Fraction. A hidden, history-dependent drift is below
known one-sided B each step. This is an independent exact calculation, not a
claim about an actual physical device or exact finite-duration fair-bit draw.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from math import comb
from pathlib import Path
import json

N=12
S0=F(0)
B_STEP=-F(1,32)  # known upper bound to ACTUAL drift increment
NOISE_STEP=F(1,8)
A=F(1,2)
C=F(255)

@lru_cache(None)
def h(k,s):
    """H_k(s) is exact one plus C times binomial upper-tail probability."""
    n=N-k
    successes=0
    for heads in range(n+1):
        future=s + n*B_STEP + (2*heads-n)*NOISE_STEP
        if future>=A:
            successes+=comb(n,heads)
    return F(1)+C*F(successes,2**n)

def qplus(k,s):
    return F(1,2)*h(k+1,s+B_STEP+NOISE_STEP)/h(k,s)

def update(s,hidden,z):
    # Arbitrary hidden memory and visible-dependent physical drift, both untaught.
    debit=F(1+(hidden%3==0)+(s>0),64)
    s2=s+B_STEP-debit + NOISE_STEP*z
    hidden2=(5*hidden+(3 if z==1 else 1))%17
    return s2,hidden2

def exact_audit():
    H0=h(0,S0)
    K=H0/(1+C)
    true_success=0
    prob_q=F(0)
    exact_q_success=F(0)
    weighted_success=F(0)
    bounded_max=F(0)
    above_bound=0
    max_prob_bits=0
    max_weight_bits=0
    for tape in product((-1,1),repeat=N):
        s=S0;hidden=7;proposal_prob=F(1);weight=F(1)
        for k,z in enumerate(tape):
            qp=qplus(k,s)
            assert 0<qp<1
            qz=qp if z==1 else 1-qp
            assert qz>0
            proposal_prob*=qz
            weight*=F(1,2)/qz
            max_prob_bits=max(max_prob_bits,qp.numerator.bit_length(),qp.denominator.bit_length())
            s,hidden=update(s,hidden,z)
        event=int(s>=A)
        true_success+=event
        prob_q+=proposal_prob
        exact_q_success+=event*proposal_prob
        weighted_success+=event*proposal_prob*weight
        bounded_max=max(bounded_max,event*weight)
        above_bound+=event*weight>K
        max_weight_bits=max(max_weight_bits,weight.numerator.bit_length(),weight.denominator.bit_length())
    expected=F(true_success,2**N)
    assert prob_q==1,(prob_q, 'not normalized')
    assert expected==weighted_success,(expected,weighted_success)
    assert above_bound==0,(bounded_max,K)
    result={'n':N,'baseline_success_count':true_success,
        'baseline_exact_probability':str(expected),
        'baseline_probability_float':float(expected),
        'twisted_exact_success_probability':str(exact_q_success),
        'twisted_success_probability_float':float(exact_q_success),
        'twisted_weighted_expectation_exact':str(weighted_success),
        'twisted_weighted_expectation_float':float(weighted_success),
        'max_likelihood_weighted_success_exact':str(bounded_max),
        'max_likelihood_weighted_success_float':float(bounded_max),
        'pathwise_bound_exact':str(K),'pathwise_bound_float':float(K),
        'qpath_probabilities_exactly_sum_to_one':prob_q==1,
        'unbiasedness_exact':expected==weighted_success,
        'weight_cap_verified_for_all_tapes':above_bound==0,
        'number_of_enumerated_paths':2**N,
        'largest_one_step_coin_ratio_bit_length':max_prob_bits,
        'largest_likelihood_ratio_bit_length':max_weight_bits,
        'hidden_drift':'actual step B_STEP - [1 + 1{hidden mod3=0} + 1{S>0}]/64',
        'hidden_update':'h <- (5h + (3 for + noise or 1 for - noise)) mod17',
        'noise_contract':'exact external iid fair bits on baseline, exact rational adaptive coin under twist',
        'sampling_cost':'Exact rational q coin can be sampled with rejection fair bits; expected finite random-bit time, unbounded worst case.'}
    dst=Path(__file__).with_name('exact_binary_twist_results.json')
    dst.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':exact_audit()
