#!/usr/bin/env python3
"""Retaining comparisons and exact limitations; no optimality claim."""
from pathlib import Path
import gzip
import hashlib
import json
import math
import re
import sympy as s
from retained_large_acquisition import R,integer_step,integer_output

ROOT=Path(__file__).resolve().parent


def ceil_ln_upper(x):
    """Integer K with exp(K)>=x, certified by an exact lower series sum."""
    x=R(x);K=0
    while True:
        term=R(1);lower=R(1)
        for j in range(1,8*K+32):term*=R(K,j);lower+=term
        if lower>=x:return K
        K+=1


def rational_bits(obj):
    answer=0
    if type(obj) is int:return abs(obj).bit_length()
    if isinstance(obj,str) and re.fullmatch(r'[+-]?\d+(?:/\d+)?',obj):
        x=R(obj);return max(abs(int(x.p)).bit_length(),int(x.q).bit_length())
    if isinstance(obj,dict):
        for v in obj.values():answer=max(answer,rational_bits(v))
    if isinstance(obj,list):
        for v in obj:answer=max(answer,rational_bits(v))
    return answer


def main():
    old=json.loads((ROOT/'large_4096_result.json').read_text())
    new=json.loads((ROOT/'retained_large_4096_result.json').read_text())
    a=json.loads(gzip.decompress((ROOT/'large_4096_observations.json.gz').read_bytes()))['records']
    b=json.loads(gzip.decompress((ROOT/'retained_large_4096_observations.json.gz').read_bytes()))['records']
    checks=0
    def ck(ok):
        nonlocal checks
        assert ok;checks+=1
    ck(b==a[:len(b)]);ck(new['source_ledger']==old['source_ledger'][:len(new['source_ledger'])])
    ck(new['partition']==old['partition']);ck(new['alpha']==old['alpha'])
    ck(new['logical_forward_calls']<old['logical_forward_calls']);ck(R(new['total_bound'])<=R(new['epsilon']))
    query=new['screening'];eps=R(new['epsilon']);delta=R(new['delta']);q=query['distinct_schedules'];L=new['length']
    K=ceil_ln_upper(2*q/delta);N=int(s.ceiling(K/(2*eps*eps)))
    mc_tree=(query['retained_chronological_MC_trie_nodes']-1)*N
    # All generated words with a fixed count can be enclosed without
    # exponential planning, using componentwise positive interval propagation.
    compiled=new['compiled'];operators=[]
    for z in compiled['operators']:operators.append(s.Matrix(z['numerators'])/z['denominator'])
    u=s.Matrix(compiled['initial_grid_state'])/(1<<compiled['bits'])
    ell=s.Matrix(compiled['output']['numerators'])/compiled['output']['denominator']
    intervals={(0,0):(u,u)}
    for length in range(1,L+1):
        for n0 in range(length+1):
            n1=length-n0;candidates=[]
            if n0:
                lo,hi=intervals[n0-1,n1];candidates.append((operators[0]*lo,operators[0]*hi))
            if n1:
                lo,hi=intervals[n0,n1-1];candidates.append((operators[1]*lo,operators[1]*hi))
            low=s.Matrix([min(x[0][i] for x in candidates) for i in range(new['rank'])])
            high=s.Matrix([max(x[1][i] for x in candidates) for i in range(new['rank'])])
            ck(all(x<=y for x,y in zip(low,high)));intervals[n0,n1]=(low,high)
    widths=[(ell*(intervals[k,L-k][1]-intervals[k,L-k][0]))[0] for k in range(L+1)]
    worst_width=max(widths);cache_bound=worst_width/2+R(new['total_bound'])
    ck(cache_bound>eps)
    # The L2 testing promise is stronger than tolerant TV, even with bounded
    # point masses. Exact example from LARGE_PRIOR_AND_LIMITS.md.
    n=4096;c=R(1,2);pairs=16;tv=pairs*c/n;v=2*pairs*c*c/n;theta=R(1,100)
    ck(tv<=theta/4);ck(v>theta*theta/16);ck(1+c<2)
    result={'status':'PASS','checks':checks,'same_actual_observation_prefix':True,
            'old_logical_calls':old['logical_forward_calls'],'retained_logical_calls':new['logical_forward_calls'],
            'old_over_retained_ratio':float(R(old['logical_forward_calls'],new['logical_forward_calls'])),
            'retained_source_reuse':'Same outgoing batches simultaneously validate small leakage and estimate fine action; fixed-round union confidence, no extra independence premise.',
            'ordinary_method_comparator':'Ordinary community/spectral/Krylov/range methods plus this acquired certificate are entitled to the same representation, observations and retained implementation. No exclusive algorithm win asserted.',
            'sharper_retained_MC_sufficient':{'confidence_natural_log_upper':K,'rollouts_per_word':N,
              'retained_chronological_prefix_calls':mc_tree,'unshared_calls':q*L*N,
              'retained_MC_over_acquisition_ratio':float(R(mc_tree,new['logical_forward_calls'])),
              'scope':'A sharper natural-log Hoeffding upper budget, NOT a minimax lower bound or a claim against best variance/KL/adaptive goal-oriented prediction. Prefix-sharing rollout construction is priced, not executed.'},
            'action_count_cache_test':{'positive_interval_states':len(intervals),
              'largest_coarse_interval_width':str(worst_width),
              'uniform_true_error_bound_for_midpoint_cache':str(cache_bound),
              'status':'THIS_INTERVAL_CERTIFICATE_FAILS; not impossibility of another count-only approximation'},
            'tolerant_TV_counterexample':{'n':n,'modified_pairs':pairs,'c':str(c),'TV':str(tv),
              'scaled_L2_squared':str(v),'theta':str(theta),'point_mass_n_max':'3/2'},
            'finite_bit_storage':{'maximum_serialized_rational_component_bits':rational_bits(new),
              'maximum_serialized_transcript_integer_bits':rational_bits(b),
              'norm_grid_bits':max(x['grid_bits'] for x in new['norm_certificates']),
              'norm_peak_accumulator_bits':new['sparse_norm_peak_accumulator_bits'],
              'query_grid_bits':compiled['bits'],'query_common_coefficient_bits':compiled['common_denominator_coefficient_bits'],
              'query_peak_accumulator_bits':query['query_peak_accumulator_bits'],
              'scope':'Scans all retained serialized rational entries; not an instrumented maximum for every SymPy intermediate during acquisition.'},
            'source_hashes':{name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in
              ['large_strong_comparison.py','retained_large_4096_result.json','large_4096_result.json']}}
    (ROOT/'large_strong_comparison_results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))


if __name__=='__main__':main()
