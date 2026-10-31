#!/usr/bin/env python3
"""Bounded independent first-hub clock and literal patch-comparison audit."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from collections import defaultdict
from math import prod
import importlib.util,sys,json,hashlib,copy,io,contextlib
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
spec=importlib.util.spec_from_file_location('candidate_single',HERE.parent/'compare_clock.py')
s=importlib.util.module_from_spec(spec);spec.loader.exec_module(s)
# Independent verifier already bound to the unchanged accepted protected-family source.
spec2=importlib.util.spec_from_file_location('protected_independent',ROOT/'stochastic_protected_boundary_20261031/independent_audit/verify_protected.py')
v=importlib.util.module_from_spec(spec2);spec2.loader.exec_module(v)
assert hashlib.sha256((ROOT/'stochastic_protected_boundary_20261031/protected_boundary.py').read_bytes()).hexdigest()=='5b1c44fb4c1cc8c748463a37b7272edba02aca9f0da4fd379d4c76d60a7e59eb'

def single_verify(rec,clock):
    S=rec['service'];Z=rec['satellites'];I=rec['inactive'];H=rec['hubs'];n=len(I)+1
    core=[(tuple(a[i] for i in S),tuple(b[i] for i in S),F(k)) for a,b,k in rec['reactions'] if all(a[j]==b[j]==0 for j in Z) and sum(a)<=1 and sum(b)<=1]
    states=[-1]+list(I);index={a:i for i,a in enumerate(states)};A=[[F(0)]*n for _ in states]
    events={}
    for token in states:
        e=[]
        for source,target,k in core:
            if token==-1:
                if sum(source):continue
            else:
                if not sum(source) or source.index(1)!=token:continue
            dest=-1 if not sum(target) else target.index(1)
            dest=-2 if dest in H else dest
            if dest==token:continue
            e.append((dest,k));A[index[token]][index[token]]+=k
            if dest in index:A[index[token]][index[dest]]-=k
        events[token]=e
    assert clock['accepted'] and clock['method']=='single-logical-protected-token'
    assert clock['clock_states']==['absent']+list(I) and clock['clock_linear_system_dimension']==n
    assert A==[list(map(F,row)) for row in clock['clock_matrix']]
    times=list(map(F,clock['clock_hitting_means']));assert len(times)==n and min(times)>0
    assert all(sum(a*t for a,t in zip(row,times))==1 for row in A)
    reach={-2}
    while True:
        newer=reach|{a for a in states if any(b in reach for b,k in events[a])}
        if newer==reach:break
        reach=newer
    assert all(a in reach for a in states)
    assert F(clock['uniform_activation_mean_upper'])==times[0]
    return core,events

def coupling(rec,core,events):
    S=rec['service'];Z=rec['satellites'];I=rec['inactive'];H=rec['hubs'];m=len(S);n=len(rec['species']);count=channels=nonlinear_decreases=0
    for y in product(range(5),repeat=m):
      for z in [0,1]:
        x=[0]*n
        for i,a in zip(S,y):x[i]=a
        x[Z[0]]=z
        for token in [-1]+[i for i in I if y[i]>0]:
            actual=defaultdict(F);splitmarginal=defaultdict(F);logical=defaultdict(F)
            for source,target,k in rec['reactions']:
                rate=F(k)*v.ff(x,source)
                if not rate:continue
                xp=tuple(a-u+w for a,u,w in zip(x,source,target));ss=tuple(source[i] for i in S);tt=tuple(target[i] for i in S)
                linear=all(source[j]==target[j]==0 for j in Z) and sum(source)<=1 and sum(target)<=1
                split=[]
                if linear and token==-1 and not sum(ss):
                    dest=tt.index(1);dest=-2 if dest in H else dest;split=[(dest,rate)]
                elif linear and token!=-1 and sum(ss) and ss.index(1)==token:
                    dest=-1 if not sum(tt) else tt.index(1);dest=-2 if dest in H else dest
                    split=[(dest,F(k))]
                    if rate>k:split.append((token,rate-k))
                else:
                    split=[(token,rate)]
                    if not linear and token!=-1 and ss[token]>tt[token]:nonlinear_decreases+=1
                assert sum(k0 for dest,k0 in split)==rate
                actual[xp]+=rate
                for dest,k0 in split:
                    assert k0>0
                    if dest>=0:assert xp[S[dest]]>=1
                    elif dest==-2:assert any(xp[S[h]]>0 for h in H)
                    splitmarginal[xp]+=k0
                    if dest!=token:logical[dest]+=k0
                    channels+=1
            expected=defaultdict(F)
            for dest,k in events[token]:expected[dest]+=k
            assert actual==splitmarginal and logical==expected;count+=1
    return {'joint_states':count,'split_event_terms':channels,'nonlinear_logical_survivor_decreases':nonlinear_decreases,
      'actual_marginal_exact':True,'logical_marginal_autonomous':True,'logical_support_preserved':True}

def main():
    original=s.p.construct;binary=s.p.activation_clock;calls=[]
    def capture(rec,*args,**kw):
        cert=original(rec,*args,**kw);calls.append((rec,copy.deepcopy(cert)));return cert
    s.p.construct=capture;buf=io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):s.main()
    finally:s.p.construct=original;s.p.activation_clock=binary
    replay=buf.getvalue();assert replay==(HERE/'frozen_results.json').read_text();(HERE/'replayed_results.json').write_text(replay)
    assert len(calls)==4;out=[]
    for idx,name in [(0,'frozen_demo'),(2,'parallel_arrivals')]:
        rec,cb=calls[idx];rec2,cs=calls[idx+1];assert rec==rec2
        v.verify(rec,cb) # Entire original binary-based patch certificate independently verified.
        core,events=single_verify(rec,cs['activation_clock'])
        ignored={'activation_clock','termination_witness','work'}
        assert {k:x for k,x in cb.items() if k not in ignored}=={k:x for k,x in cs.items() if k not in ignored}
        # The only altered mathematical witness uses the independently verified uniform clock.
        term=cs['termination_witness'];oldterm=cb['termination_witness'];changed={'uniform_positive_head_excess_bound','guaranteed_scalar_radius','scalar_doublings','radius_inequality_lhs','radius_inequality_rhs','ratio_monotonicity_margin'}
        assert {k:x for k,x in term.items() if k not in changed}=={k:x for k,x in oldterm.items() if k not in changed}
        mean=cs['activation_clock']['uniform_activation_mean_upper'];M=term['positive_forcing_bound_M'];excess=M*mean
        assert term['uniform_positive_head_excess_bound']==excess
        rb=term['guaranteed_scalar_radius'];c=cs['c'];T=cs['T'];degree=term['leakage_degree'];leak=term['leakage_coefficient']
        gg=prod((F(i)/(i+c) for i in range(1,rb)),start=F(1));lhs=T**rb*gg;rhs=2*leak*rb**degree*excess/cs['tail_epsilon']
        assert rb>=max(cs['initial_R'],term['forcing_radius_K']) and lhs==term['radius_inequality_lhs']>=rhs==term['radius_inequality_rhs']
        assert T*rb**(degree+1)>=(rb+c)*(rb+1)**degree
        result={'case':name,'binary_dimension':cb['activation_clock']['clock_linear_system_dimension'],'single_dimension':cs['activation_clock']['clock_linear_system_dimension'],
          'binary_mean':cb['activation_clock']['uniform_activation_mean_upper'],'single_mean':mean,
          'actual_patch_and_Foster_fields_literally_identical':True,'full_binary_patch_independently_verified':True,
          'single_termination_witness_independently_verified':True,'R':cs['R'],'head_states':len(cs['head_states'])}
        if idx==0:result['independent_coupling_challenge']=coupling(rec,core,events)
        out.append(result)
    assert out[0]['single_mean']==out[0]['binary_mean']==24
    assert out[1]['single_mean']==F(3,2)>F(5,4)==out[1]['binary_mean']
    rec=calls[0][0];clock=calls[1][1]['activation_clock'];bad=copy.deepcopy(clock);bad['clock_hitting_means'][0]+=1
    try:single_verify(rec,bad)
    except AssertionError:pass
    else:raise AssertionError('altered mean accepted')
    budget=s.single_clock(rec,max_clock_states=2);assert not budget['accepted'] and budget['required_clock_states']==3
    print(json.dumps({'comparison_source_sha256':hashlib.sha256((HERE.parent/'compare_clock.py').read_bytes()).hexdigest(),
      'accepted_dependency_sha256':'5b1c44fb4c1cc8c748463a37b7272edba02aca9f0da4fd379d4c76d60a7e59eb',
      'byte_identical_replay':True,'cases':out,'altered_single_mean_rejected':True,'clock_budget_UNKNOWN':budget,
      'first_hub_only_not_simultaneous_coverage':True,'source_files_unchanged':True},default=s.p.encode,indent=2))

if __name__=='__main__':main()
