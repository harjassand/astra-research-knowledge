"""Strict classical receiver: local outcome histograms -> reusable Clifford.

Reads only declared contract/discovery/validation files. It never imports
source_acquire, an unknown Clifford, junk, probabilities or truth audit.
"""

from fractions import Fraction as F
import argparse
import hashlib
import itertools
import json
from math import isqrt
from pathlib import Path
import time

from pauli_compiler import canonical,compile_pairs,route_line,apply

BASE=Path(__file__).resolve().parent
CODE=(0,1,3,2)


def sqrt_upper(x,bits=40):
    x=F(x)
    if x<0:raise ValueError('negative radicand')
    D=1<<bits;n=isqrt((x.numerator*D*D)//x.denominator)
    if n*n*x.denominator<x.numerator*D*D:n+=1
    out=F(n,D);assert out*out>=x
    return out


def walsh(hist):
    out=list(hist);stride=1
    while stride<len(out):
        for i in range(0,len(out),2*stride):
            for j in range(stride):
                a,b=out[i+j],out[i+j+stride];out[i+j]=a+b;out[i+j+stride]=a-b
        stride*=2
    return out


def dump(name,data):
    (BASE/name).write_text(json.dumps(data,sort_keys=True,indent=2)+'\n')


def check_contract(c):
    """This executable port is q=1; the mathematical theorem allows all q."""
    assert c['q']==1 and isinstance(c['n'],int) and c['n']>=1
    assert isinstance(c['source_id'],str) and c['source_id']
    assert isinstance(c['output_site'],int) and 0<=c['output_site']<c['n']
    patch=c['patch']
    assert isinstance(patch,list) and patch and len(set(patch))==len(patch)
    assert all(isinstance(j,int) and 0<=j<c['n'] for j in patch)
    for key in ('discovery_shots_per_setting','validation_shots_per_candidate','concentration_log_upper'):
        assert isinstance(c[key],int) and c[key]>0
    error=F(c['discovery_absolute_error'])
    assert 0<error<1
    # Pay the displayed joint discovery+validation risk at this contract.
    assert c['discovery_shots_per_setting']*error*error/2>=c['concentration_log_upper']


def discover(c):
    check_contract(c)
    start=time.perf_counter();data=json.loads((BASE/'DISCOVERY_HISTOGRAMS.json').read_text())
    assert data['source_id']==c['source_id'] and c['q']==1
    patch=c['patch'];w=len(patch);n=c['n'];shots=c['discovery_shots_per_setting']
    assert len(set(patch))==w and all(0<=j<n for j in patch)
    accum={r:[0]*(4**w) for r in(1,3)};trials={r:[0]*(4**w) for r in(1,3)}
    seen=set();reads=0
    for row in data['rows']:
        ref=row['reference'];axes=tuple(row['axes']);hist=row['histogram']
        assert ref in accum and len(axes)==w and all(a in(1,2,3) for a in axes)
        assert (ref,axes) not in seen;seen.add((ref,axes))
        assert len(hist)==1<<(w+1) and all(isinstance(a,int) and a>=0 for a in hist)
        assert sum(hist)==shots;reads+=shots
        wh=walsh(hist)
        for mask in range(1<<w):
            code=sum((axes[j]<<(2*j)) for j in range(w) if (mask>>j)&1)
            accum[ref][code]+=wh[mask|(1<<w)];trials[ref][code]+=shots
    assert len(seen)==2*3**w
    candidates=[];pair=[]
    for ref in(1,3):
        scores=[F(a,b) for a,b in zip(accum[ref],trials[ref])]
        best=max(range(1,4**w),key=lambda i:(abs(scores[i]),-i))
        x=z=0
        for j,site in enumerate(patch):
            v=CODE[(best>>(2*j))&3];x|=(v&1)<<site;z|=((v>>1)&1)<<site
        p=canonical(x,z,scores[best]<0);pair.append(p)
        candidates.append({'reference':ref,'physical_pauli':list(p),
                           'discovery_correlation':str(abs(scores[best])),
                           'shots':c['validation_shots_per_candidate']})
    gates=compile_pairs([pair],n,[c['output_site']]);routed=route_line(gates)
    # Literal exact ALL-state routing validation on a complete generator basis.
    for i in range(n):
        for p in((1<<i,0,0),(0,1<<i,0)):
            assert apply(p,gates)==apply(p,routed)
    for ref,p in zip((1,3),pair):
        dest=c['output_site'];expected=(1<<dest,0,0) if ref==1 else(0,1<<dest,0)
        assert apply(p,routed)==expected
    # No global support search: the contract supplied ONE five-site patch.
    request={'source_id':c['source_id'],'candidates':candidates,
             'declaration':'fresh independent source programs, fixed shots, no payload used'}
    dump('VALIDATION_REQUEST.json',request)
    dump('DECODER.json',{'source_id':c['source_id'],'n':n,'q':1,
         'output_site':c['output_site'],'candidates':candidates,
         'gates':gates,'routed_gates':routed,
         'gate_count':len(gates),'nearest_neighbor_gate_count':len(routed),
         'routed_CNOT_count':sum(g[0]=='CX' for g in routed),
         'all_2n_generator_routing_checks':2*n,
         'fresh_source_calls_during_each_late_payload':0,
         'output':'apply stored known Clifford; retain output wire and discard all other wires'})
    dump('DISCOVERY_RECEIVER_EXECUTION.json',{'scope':'actual classical record-to-circuit execution',
         'declared_source_reads_consumed':reads,'candidate_count':2*4**w,
         'classical_circuit_gate_count':len(gates),'nearest_neighbor_gate_count':len(routed),
         'source_or_model_oracle_calls_by_receiver':0,
         'seconds_after_imports':time.perf_counter()-start})
    print('stored',len(gates),'gates,',len(routed),'nearest-neighbor gates')


def validate(c):
    check_contract(c)
    start=time.perf_counter();req=json.loads((BASE/'VALIDATION_REQUEST.json').read_text())
    data=json.loads((BASE/'VALIDATION_COUNTS.json').read_text())
    assert req['source_id']==data['source_id']==c['source_id']
    assert data['request_sha256']==hashlib.sha256((BASE/'VALIDATION_REQUEST.json').read_bytes()).hexdigest()
    assert len(data['rows'])==len(req['candidates'])==2
    assert [r['reference'] for r in req['candidates']]==[1,3]
    pairs=[[tuple(r['physical_pauli']) for r in req['candidates']]]
    assert all(len(p)==3 and all(isinstance(x,int) for x in p) for p in pairs[0])
    gates=compile_pairs(pairs,c['n'],[c['output_site']]);routed=route_line(gates)
    ell=c['concentration_log_upper'];bounds=[];reads=0
    for request,row in zip(req['candidates'],data['rows']):
        assert row['reference']==request['reference'] and row['physical_pauli']==request['physical_pauli']
        m=row['shots'];bad=row['bad']
        assert isinstance(m,int) and isinstance(bad,int)
        assert m==request['shots']==c['validation_shots_per_candidate'] and 0<=bad<=m
        empirical=F(bad,m);a=F(ell,m)
        pU=min(F(1),empirical+a+sqrt_upper(a*a+2*a*empirical))
        bounds.append(pU);reads+=m
    infid=min(F(1),sum(bounds));feL=1-infid
    diamond=min(F(1),2*sqrt_upper(infid))
    # e>=8/3 pays both discovery union and two fresh validation tests.
    M=2*4**len(c['patch']);risk=(2*M+2)*F(3,8)**ell
    assert risk<F(1,1000)
    accepted=feL>=F(49,50)
    result={'source_id':c['source_id'],'accepted':accepted,
            'contract_scope':'fixed memoryless quantum source + fresh independent ideal measurement law; seeded numerical application is not that qualification',
            'pipeline_data_inputs_only':['INPUT_CONTRACT.json','DISCOVERY_HISTOGRAMS.json','VALIDATION_REQUEST.json','VALIDATION_COUNTS.json'],
            'validation_data_inputs_only':['INPUT_CONTRACT.json','VALIDATION_REQUEST.json','VALIDATION_COUNTS.json'],
            'qualified_controller':{'routed_gates':routed,'output_site':c['output_site'],
                                    'gate_count':len(routed),'fresh_late_payload_source_calls':0},
            'qualified_request_sha256':data['request_sha256'],
            'bad_probability_upper_by_generator':list(map(str,bounds)),
            'Bell_fidelity_lower':str(feL),'Bell_fidelity_lower_decimal':float(feL),
            'all_input_halfdiamond_upper':str(diamond),'all_input_halfdiamond_upper_decimal':float(diamond),
            'ideal_joint_error_probability_upper':str(risk),
            'validation_source_calls':reads,
            'total_source_calls':reads+2*3**len(c['patch'])*c['discovery_shots_per_setting'],
            'all_late_payloads_reuse':'fixed stored circuit and fixed memoryless source; T uses add at mostT times the one-use diamond bound',
            'physical_known_gate_error':'add sum full gate diamond errors/2; not acquired',
            'hardware_acquisition':'NOT_ACQUIRED','source_truth_or_probabilities_read':False,
            'seconds_after_imports':time.perf_counter()-start}
    dump('QUALIFIED_DECODER.json',result)
    print('accepted',accepted,'Bell lower',float(feL),'halfdiamond upper',float(diamond))


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('mode',choices=['discover','validate'])
    a=ap.parse_args();c=json.loads((BASE/'INPUT_CONTRACT.json').read_text())
    (discover if a.mode=='discover' else validate)(c)


if __name__=='__main__':main()
