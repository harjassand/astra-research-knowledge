#!/usr/bin/env python3
"""Exact Mobius resummation and a falsified eroder shortcut. No random draws."""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import math
import sys
import time

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'outputs/autonomous_memory'
sys.path.insert(0,str(ROOT/'outputs/reversible_currents'))
from currents import log_bounds


def runs(mask,n):
    lengths=[];current=0
    for i in range(n):
        if (mask>>i)&1:current+=1
        elif current:lengths.append(current);current=0
    if current:lengths.append(current)
    return lengths


def mobius(values,n):
    a=values[:]
    for bit in range(n):
        for mask in range(1<<n):
            if mask&(1<<bit):a[mask]-=a[mask^(1<<bit)]
    return a


def and_ring(initial,late,L,steps):
    state=initial
    for _ in range(steps):
        shifted=(state>>1)|((state&1)<<(L-1))
        state&=shifted
    return state|late


def main():
    start=time.perf_counter()
    n=8;k=3;eta=F(1,50)
    b=[int(max(runs(mask,n),default=0)>=k) for mask in range(1<<n)]
    a=mobius(b,n)
    for mask in range(1<<n):
        assert b[mask]==sum(a[sub] for sub in range(1<<n) if sub&mask==sub)
        if any(m<k for m in runs(mask,n)):assert a[mask]==0
    weight=sum((abs(c)*eta**mask.bit_count() for mask,c in enumerate(a)),F(0))
    q=8*eta;small_A=F(n,4)*q**k/(1-q)
    assert 0<small_A<1 and weight<=small_A/(1-small_A)
    L=512;N=L*L;k=L;d=2
    q=2*d*d*eta;A=F(N,d*d)*q**k/(1-q)
    assert 0<A<F(1,2)
    bound=2*A/(1-A)
    logarithm_upper=log_bounds(4,64)[1]+log_bounds(A,64)[1]
    assert logarithm_upper<-925
    # A specific minimal bad eroder witness, not a mere proposed falsifier.
    L2=12;steps=4;full=(1<<L2)-1
    early=(1<<(L2-1))-1
    late=full^((1<<(L2-1-steps))-1)
    assert and_ring(early,late,L2,steps)==full
    deleted=0
    for i in range(L2):
        if (early>>i)&1:
            assert and_ring(early^(1<<i),late,L2,steps)!=full;deleted+=1
        if (late>>i)&1:
            assert and_ring(early,late^(1<<i),L2,steps)!=full;deleted+=1
    assert deleted==16
    def compact(x,upper=False):
        scale=2**112;v=x*scale
        value=-((-v.numerator)//v.denominator) if upper else v.numerator//v.denominator
        return str(F(value,scale))
    result={'status':'MOBIUS_LOCAL_RESUMMATION_PASSED_ERODER_SHORTCUT_REFUTED',
        'finite_exact_inversion':{'locations':n,'run_threshold':3,'all_subsets':1<<n,
            'nonzero_coefficients':sum(c!=0 for c in a),
            'all_small_component_coefficients_cancel_exact':True,
            'exact_weight':str(weight),'polymer_weight_upper':str(small_A/(1-small_A))},
        'same_large_scan_predicate_repaired':{'N':N,'k':k,'graph_degree':d,'eta':str(eta),
            'q':str(q),'polymer_activity_A':str(A),'joint_diamond_bound_rational':str(bound),
            'joint_bound_log_upper_certified':compact(logarithm_upper,True),
            'joint_bound_log_upper_preview':float(logarithm_upper),
            'joint_error_less_than_exp_minus_925':True,
            'old_scan_log_lower':587.5447135978345,
            'noise_strength_graph_and_badness_unchanged':True,
            'scope':'conditional operator-norm certificate; no physical memory/decoder constructed for this line diagnostic'},
        'eroder_shortcut_counterexample':{'rule':'x_i next=x_i*x_(i+1), with OR births',
            'ring_size':L2,'time_separation':steps,
            'early_birth_sites':[i for i in range(L2) if (early>>i)&1],
            'late_birth_sites':[i for i in range(L2) if (late>>i)&1],
            'bad_final_state':'all ones','births_in_minimal_witness':deleted,
            'all_single_deletions_destroy_badness_exact':True,
            'full_witness_Mobius_coefficient':1,'separate_fault_component_sizes':[11,5],
            'minimum_number_of_births_for_any_badness':12,
            'counterexample_scope':'eroder property alone does not imply static-birth Mobius cluster support'},
        'Astra_sweep_Mobius_hypothesis':'NOT_PROVED; causal envelope and overlapping explanations remain',
        'low_dimensional_autonomous_memory':'NOT_ACHIEVED','physical_experiments':0,'new_random_draws':0,
        'code_SHA256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'CPU_wall_seconds':time.perf_counter()-start}
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/'mobius_resummation.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'seconds':result['CPU_wall_seconds'],
        'large_repaired_joint_log_upper':float(logarithm_upper),'eroder_minimal_witness_births':deleted,
        'Astra_sweep_Mobius_hypothesis':result['Astra_sweep_Mobius_hypothesis'],'new_random_draws':0},indent=2))


if __name__=='__main__':main()
