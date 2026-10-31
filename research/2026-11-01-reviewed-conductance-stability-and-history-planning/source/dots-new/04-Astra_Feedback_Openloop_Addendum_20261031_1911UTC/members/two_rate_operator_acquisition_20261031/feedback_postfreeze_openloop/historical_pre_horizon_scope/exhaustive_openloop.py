#!/usr/bin/env python3
"""Exhaustive bounded-grid open-loop comparator; outside feedback source freeze.

Checks every length-24 word, not just a supplied list. Native uint64 safety is
proved from nonnegative stochastic integer rows D and D*2^p<2^64. Floors give
one-sided per-step error at most 2^-p; infinity contraction propagates at most
L*2^-p. This is a test comparator, not a fast general switched-word planner.
"""
from pathlib import Path
import hashlib,json,math,sys,time
import numpy as np
import sympy as s
ROOT=Path(__file__).resolve().parent;PARENT=ROOT.parent;R=s.Rational


def run(length=24,grid_bits=32,prefix_depth=4):
    start=time.perf_counter();model=json.loads((PARENT/'history_sensitive_4096_result.json').read_text())
    rec=json.loads((PARENT/'feedback_extension'/'polynomial_feedback_received.json').read_text())
    assert type(length) is int and 0<=prefix_depth<=length<=24 and type(grid_bits) is int and grid_bits>=1
    r=model['rank'];m=model['m'];assert m==2
    D=math.lcm(*(x['denominator'] for x in model['compiled']['operators']));S=1<<grid_bits
    integers=[[[v*(D//x['denominator']) for v in row] for row in x['numerators']] for x in model['compiled']['operators']]
    assert all(min(row)>=0 and sum(row)==D for M in integers for row in M)
    assert D*S<1<<64
    mats=[np.asarray(M,dtype=np.uint64) for M in integers]
    target=np.asarray([model['task_b'][p[0]]*S for p in model['partition']],dtype=np.uint64)
    initial=[R(sum(model['task_ell_numer'][i] for i in p),model['task_ell_denominator']) for p in model['partition']]
    assert initial.count(R(1))==1 and initial.count(R(0))==r-1;g=initial.index(R(1))
    products=0;peak_entries=0
    def expand(front):
        nonlocal products,peak_entries
        new=np.empty((2*len(front),r),dtype=np.uint64)
        for a,M in enumerate(mats):new[a*len(front):(a+1)*len(front)]=(front@M.T)//D
        products+=2*len(front)*r*r
        # front+new+one matmul temporary, excluding small arrays and metadata.
        peak_entries=max(peak_entries,(len(front)+len(new)+len(front))*r)
        return new
    prefixes=target.reshape(1,r)
    for _ in range(prefix_depth):prefixes=expand(prefixes)
    best=-1;code=None;total=0
    for p,seed in enumerate(prefixes):
        values=seed.reshape(1,r)
        for _ in range(length-prefix_depth):values=expand(values)
        column=values[:,g];j=int(np.argmax(column));z=int(column[j]);total+=len(values)
        if z>best:best=z;code=p+(j<<prefix_depth)
        del values
    assert total==1<<length
    word=[(code>>j)&1 for j in range(length)]
    # Exact Python-integer/SymPy replay of the maximizing grid word.
    exact=s.Matrix([int(x)//S for x in target]);grid=[int(x) for x in target]
    for a in word:
        exact=s.Matrix(integers[a])*exact/D
        grid=[sum(integers[a][i][j]*grid[j] for j in range(r))//D for i in range(r)]
    assert grid[g]==best and R(best,S)<=exact[g]<=R(best+length,S)
    lower=R(best,S);upper=R(best+length,S)
    # The old uniform model error applies to every word; its execution-grid
    # term is unnecessary because this comparator has its own paid rounding.
    open_error=R(model['cross_rounds'][-1]['compression_bound'])+R(model['fine_rounds'][-1]['propagated_bound'])
    feedback=R(rec['plan']['coarse_optimal_value']);feedback_error=R(rec['model_error_bound'])
    out={'status':'PASS_ALL_WORDS_COMPARATOR','word_length':length,'grid_bits':grid_bits,
      'explicit_words_checked':total,'coarse_optimal_interval':[str(lower),str(upper)],
      'maximizing_grid_word_backward_operator_order':word,'same_word_physical_action_order':word[::-1],
      'maximizing_word_exact_coarse_value':str(exact[g]),'source_integer_products':products,
      'peak_bulk_array_entries_bound':peak_entries,'peak_bulk_array_bytes_bound':8*peak_entries,
      'accumulator_safe_bound':D*S,'accumulator_bits_bound':(D*S).bit_length(),
      'openloop_model_error':str(open_error),'feedback_model_error':str(feedback_error),
      'feedback_coarse_value':str(feedback),
      'true_feedback_minus_best_openloop_lower':str(feedback-2*feedback_error-upper),
      'coarse_optimal_upper_float':float(upper),'feedback_coarse_value_float':float(feedback),
      'true_gap_lower_float':float(feedback-2*feedback_error-upper),
      'confidence_scope':'Uses the SAME polynomial feedback event for both policy and every open-loop word (constant action across blocks). The base open-word error is diagnostic only, not used in the gap. No additional statistical union or posterior-on-PASS assertion.',
      'scope':'Post-freeze comparator, not independently reviewed. Pays exponential full enumeration. Baseline gets identical retained coarse model and can enumerate/use stronger planning methods. Does not claim learning-acquisition superiority. Source transition count already paid; zero new observations.',
      'seconds':time.perf_counter()-start,'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
      'base_sha256':hashlib.sha256((PARENT/'history_sensitive_4096_result.json').read_bytes()).hexdigest(),
      'feedback_receipt_sha256':hashlib.sha256((PARENT/'feedback_extension'/'polynomial_feedback_received.json').read_bytes()).hexdigest()}
    return out


if __name__=='__main__':
    out=run();(ROOT/'exhaustive_openloop_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ['status','explicit_words_checked','coarse_optimal_upper_float','feedback_coarse_value_float','true_gap_lower_float','source_integer_products','seconds']},indent=2))
