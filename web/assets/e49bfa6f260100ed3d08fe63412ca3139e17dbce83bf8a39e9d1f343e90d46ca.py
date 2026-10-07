#!/usr/bin/env python3
"""Independent exact trace/transcript checks for the owned compiler output.

Does not import the compiler and does not treat finite checks as an all-N
proof. Exact Gaussian-rational Clifford density transformations are checked.
"""
import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import time

HERE=Path(__file__).resolve().parent
def z(a=0,b=0): return (F(a),F(b))
def za(x,y): return (x[0]+y[0],x[1]+y[1])
def zm(x,y): return (x[0]*y[0]-x[1]*y[1],x[0]*y[1]+x[1]*y[0])
def zb(x): return (x[0],-x[1])
def mm(A,B):
    return [[za(zm(A[i][0],B[0][j]),zm(A[i][1],B[1][j])) for j in range(2)] for i in range(2)]
def adj(A): return [[zb(A[j][i]) for j in range(2)] for i in range(2)]
def scale(A,a): return [[(r*a,i*a) for r,i in row] for row in A]
def madd(A,B): return [[za(x,y) for x,y in zip(ar,br)] for ar,br in zip(A,B)]
def transform(rho,gate):
    if gate=='H':
        U=[[z(1),z(1)],[z(1),z(-1)]]
        return scale(mm(mm(U,rho),adj(U)),F(1,2))
    if gate=='S': U=[[z(1),z()],[z(),z(0,1)]]
    elif gate=='X': U=[[z(),z(1)],[z(1),z()]]
    else: raise ValueError(gate)
    return mm(mm(U,rho),adj(U))
def tau(m):
    x,y,t=m
    return [[z((1+t)/2),z(x/2,-y/2)],[z(x/2,y/2),z((1-t)/2)]]


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--name',default='cutoff_euler_R128')
    args=ap.parse_args()
    start=time.perf_counter()
    path=HERE/'evidence'/(args.name+'.json')
    d=json.loads(path.read_text())
    N,R,T,K=[d['input'][key] for key in ['N','R','T','seed_cap']]
    rho=F(d['input']['cutoff_radius'])
    assert len(d['paths'])==R
    c=d['certificates']
    point,log_guard=F(c['uniform_enforced_endpoint_guard_upper']),F(c['uniform_enforced_logweight_guard_upper'])
    assert F(c['max_path_endpoint_l2_error_upper'])<=point
    assert F(c['max_path_logweight_error_upper'])<=log_guard
    assert F(c['categorical_TV_upper'])<=F(c['categorical_uniform_guard_upper'])
    for p in d['paths']:
        assert len(p['steps'])==T and len(p['seed']['attempts'])<=K
        assert F(p['seed']['numeric_accept_error_upper'])<=F(1,1<<60)
        assert F(p['seed']['seed_pointwise_error_on_matching_decisions'])<=F(1,1<<40)
        assert F(p['endpoint_coupling_l2_upper'])<=point
        for step in p['steps']:
            assert F(step['numeric_update_l2_error_upper'])<=F(1,1<<48)
            for pivot in step['guards']['Cholesky_pivot_intervals']:
                assert F(pivot['lo'])>0
        endpoint=list(map(F,p['endpoint_rational']))
        assert sum(x*x for x in endpoint)<=rho*rho
    # Independently reconstruct the conservative finite output budget sum.
    total=sum(F(c[k]) for k in ['normal_tail_union_upper','heat_seed_exhaustion_union_upper',
      'seed_decision_disagreement_union_upper','relative_logweight_law_TV_upper','categorical_uniform_guard_upper'])+F(N,2)*point
    assert F(c['complete_finite_bit_output_trace_error_upper'])==min(F(1),total)
    # Uniform integer categorical rule exactly selects the saved index.
    weights=d['selection']['integer_weights']
    denom=1<<d['selection']['denominator_bits']
    assert all(x>=0 for x in weights) and sum(weights)==denom
    u=d['selection']['uniform_integer'];assert 0<=u<denom
    cumulative=0
    for selected,w in enumerate(weights):
        cumulative+=w
        if u<cumulative: break
    assert selected==d['selection']['selected_index']
    # Verify every normal word/enclosure contract without rerunning peer code.
    normal_count=normal_bits=0
    transcript_path=Path(d['evidence']['normal_transcript'])
    with transcript_path.open() as stream:
        for line in stream:
            n=json.loads(line)
            bits=n['exact_fair_random_bit_count'];raw=n['uniform_integer']
            assert 0<=raw<(1<<bits)
            assert F(n['uniform_prefix_rational'])==F(raw,1<<bits)
            assert F(n['max_observed_cdf_interval_width'])<=F(n['cdf_interval_width_budget'])
            assert F(n['ideal_clipped_normal_coupling_error_upper'])<F(n['h'])
            assert -F(n['L'])<=F(n['output_rational'])<=F(n['L'])
            normal_count+=1;normal_bits+=bits
    assert normal_count==d['evidence']['complete_normal_draws']
    assert normal_bits==d['costs']['actual_normal_fair_bits']
    # Check the entire local circuit table by exact density conjugation.
    circuits=d['Clifford_output']['circuit_table']
    projectors={}
    axes={'X':[F(1),F(0),F(0)],'Y':[F(0),F(1),F(0)],'Z':[F(0),F(0),F(1)]}
    for label,gates in circuits.items():
        state=tau([F(0),F(0),F(1)])
        for gate in gates: state=transform(state,gate)
        sign=1 if label[0]=='+' else -1
        expected=tau([sign*x for x in axes[label[1]]])
        assert state==expected
        projectors[label]=state
    integers=d['Clifford_output']['integer_Bloch_coefficients']
    local_den=1<<d['Clifford_output']['Bloch_denominator_bits']
    m=[F(x,local_den) for x in integers]
    assert list(map(F,d['emitted_local_rational_Bloch']))==m
    assert sum(x*x for x in m)<=rho*rho
    l1=sum(map(abs,m),F(0));assert l1<1
    mixture=scale(tau([F(0)]*3),1-l1)
    for axis,x in zip('XYZ',m):
        mixture=madd(mixture,scale(projectors[('+' if x>=0 else '-')+axis],abs(x)))
    assert mixture==tau(m)
    # Decode every independent local word and reproduce gates/counts exactly.
    categories=d['Clifford_output']['axis_categories']
    counts={label:0 for label in circuits}
    gatecounts={'X':0,'H':0,'S':0}
    words_path=Path(d['Clifford_output']['complete_random_word_transcript'])
    data=words_path.read_bytes();assert len(data)==9*N
    for offset in range(0,len(data),9):
        raw=int.from_bytes(data[offset:offset+9],'big')
        assert raw<(1<<65)
        selector,coin=raw>>1,raw&1
        cumulative=0
        for axis,sign,w in categories:
            cumulative+=w
            if selector<cumulative: break
        label=('-Z' if coin else '+Z') if axis==3 else ('+' if sign>0 else '-')+'XYZ'[axis]
        counts[label]+=1
        for gate in circuits[label]: gatecounts[gate]+=1
    assert counts==d['Clifford_output']['pure_state_counts']
    assert gatecounts==d['Clifford_output']['actual_gate_description_counts']
    assert sum(gatecounts.values())<=3*N
    assert d['costs']['actual_local_Clifford_fair_bits']==65*N
    evidence_files=[path,transcript_path,words_path]
    result={'status':'PASS_EXACT_OWNED_ARITHMETIC_AND_CLIFFORD_TRANSCRIPT_AUDIT','fixture':args.name,
      'all_normal_transcript_rows':normal_count,'all_local_words':N,'six_Clifford_projectors_exact':True,
      'local_mixture_matrix_exact':True,'all_completed_guards_pass':True,'uniform_budget_sum_exact':True,
      'finite_bit_error_upper':c['complete_finite_bit_output_trace_error_upper'],
      'separate_cutoff_Euler_error_upper':c['continuous_cutoff_Euler_trace_error_upper'],
      'separate_importance_error_upper':c['averaged_importance_trace_error_upper'],
      'Gibbs_error_upper':c['full_Gibbs_trace_error_upper'],
      'files':[{ 'path':str(p),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in evidence_files],
      'costs':{'wall_seconds':time.perf_counter()-start},
      'limits':['This verifies saved finite guards, exact matrices and complete transcripts, not Gaussian entropy or hardware.',
        'All-N coefficient/coupling/quantum comparison remains the analytic proof; no proof is inferred from this replay.']}
    out=HERE/'evidence'/(args.name+'_audit.json')
    out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'output':str(out),'status':result['status'],'normal_rows':normal_count,
       'local_words':N,'wall_seconds':result['costs']['wall_seconds']}))


if __name__=='__main__': main()
