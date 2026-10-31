#!/usr/bin/env python3
"""Nonmutating exact receiving, conditional on external fresh iid provenance.

Typed API (assertions enabled), not an arbitrary-JSON security boundary. The
caller binds its task/source artifact externally; no trust in record scalar
norm/error summaries. CLI writes only its explicitly named output JSON.
"""
from pathlib import Path
import argparse
import copy
import gzip
import hashlib
import json
import sys
import time
import sympy as s
ROOT=Path(__file__).resolve().parent;PARENT=ROOT.parent;sys.path.insert(0,str(PARENT))
from check_retained_large_acquisition import replay as replay_base
from retained_large_acquisition import R,compression,sqrt_up
from sparse_norm_probe import upper_norm
from plan_feedback import exact_dp,pack,unpack
sys.path.insert(0,str(PARENT.parent/'robust_operator_reuse_20261031'/'finite_observation'))
from robust_replay import norm_up
BASE_SHA='dc7583f0aa94e06f7440a6109a2dbef128b1db35538664a1880f8a5c4c146568'
OBS_SHA='f9ec8eedc6465e9b552f48fdbe15f9f6e3e7ca9e2f78553e4d954d6b697fdd85'


def preflight(model,local,*,expected_b,expected_ell_num,expected_ell_den,
              expected_length,expected_tolerance,expected_confidence,
              expected_generators,expected_base_sha,base_bytes):
    assert type(expected_length) is int and expected_length>=0
    assert type(expected_generators) is int and expected_generators>0
    assert not isinstance(expected_tolerance,(bool,float)) and R(expected_tolerance)>0
    assert not isinstance(expected_confidence,(bool,float)) and 0<R(expected_confidence)<1
    assert (model['length'],model['m'])==(expected_length,expected_generators)
    assert (R(model['epsilon']),R(model['delta']))==(R(expected_tolerance),R(expected_confidence))
    assert (model['task_b'],model['task_ell_numer'],model['task_ell_denominator'])==(expected_b,expected_ell_num,expected_ell_den)
    assert hashlib.sha256(base_bytes).hexdigest()==expected_base_sha and json.loads(base_bytes)==model
    assert local['base_result_sha256']==expected_base_sha
    assert R(model['coarse_spectral_radius'])==R(1,4)
    n=model['n'];r=model['rank'];m=expected_generators;parts=model['partition']
    assert n==len(expected_b)==len(expected_ell_num) and len(parts)==r
    assert sorted(i for p in parts for i in p)==list(range(n)) and all(parts)
    assert all(type(x) is int and x in (0,1) for x in expected_b+expected_ell_num)
    assert type(expected_ell_den) is int and sum(expected_ell_num)==expected_ell_den>0
    assert all(len({(expected_b[i],expected_ell_num[i]) for i in p})==1 for p in parts)
    assert local['local_operator_count']==m*r*r and len(local['local_certificates'])==m*r*r
    labels=[(x['a'],x['source_block'],x['target_block']) for x in local['local_certificates']]
    assert labels==[(a,g,h) for a in range(m) for g in range(r) for h in range(r)]
    for x in local['local_certificates']:
        a,g,h=x['a'],x['source_block'],x['target_block'];c=x['certificate']
        assert all(type(z) is int for z in (a,g,h,x['observed_count_total'],x['embedded_dimension']))
        assert x['observed_count_total']>=0 and x['embedded_dimension']==len(parts[g])+len(parts[h])
        if x['observed_count_total']:
            assert R(c['delta'])==R(expected_confidence)/(8*m*r*r)
        else: assert c=={'status':'EXACT_ZERO_OBSERVED_BLOCK','sparse_integer_products':0}
    assert local['additional_forward_calls']==0


def replay(model,records,local,*,expected_b,expected_ell_num,expected_ell_den,
           expected_length,expected_tolerance,expected_confidence,
           expected_generators,expected_base_sha,base_bytes,packed_directory=ROOT):
    args=dict(expected_b=expected_b,expected_ell_num=expected_ell_num,
              expected_ell_den=expected_ell_den,expected_length=expected_length,
              expected_tolerance=expected_tolerance,expected_confidence=expected_confidence,
              expected_generators=expected_generators,expected_base_sha=expected_base_sha,base_bytes=base_bytes)
    preflight(model,local,**args)
    baseargs={k:v for k,v in args.items() if k not in ('expected_base_sha','base_bytes')}
    checks=replay_base(model,records,**baseargs)
    def ck(ok):
        nonlocal checks
        assert ok;checks+=1
    parts=model['partition'];n=model['n'];r=model['rank'];m=model['m'];L=expected_length
    coarse=[x for x in records if x['kind']=='coarse'];N=coarse[0]['N']
    ck(len(coarse)==m and all(x['N']==N and x['a']==a for a,x in enumerate(coarse)))
    which=[0]*n;within=[0]*n
    for g,p in enumerate(parts):
        for j,i in enumerate(p):which[i]=g;within[i]=j
    U=s.zeros(r);products=0
    for x in local['local_certificates']:
        a,g,h=x['a'],x['source_block'],x['target_block'];src=parts[g];dest=parts[h]
        k=len(src);d=k+len(dest);rows=[[] for _ in range(d)]
        for ii,i in enumerate(src):rows[ii]=[(k+within[j],v) for j,v in coarse[a]['counts'][i] if which[j]==h]
        total=sum(v for row in rows for _,v in row);ck(total==x['observed_count_total'])
        if total:
            z=upper_norm(rows,total,[list(range(k)),list(range(k,d))],
                         R(expected_confidence)/(8*m*r*r),forced_probe=x['certificate']['probe'])
            for key in z:
                if key!='execution_seconds':ck(z[key]==x['certificate'][key])
            v=R(n*total,d*N)*R(z['upper']);products+=z['sparse_integer_products']
        else:v=R(0)
        ck(v==R(x['scaled_block_norm_upper']));U[g,h]=max(U[g,h],v)
    u=norm_up(U,s.eye(r),bits=30);alpha=u+sqrt_up(m)*R(model['coarse_spectral_radius'])
    ein=sqrt_up(m)*R(model['cross_rounds'][-1]['enter']);eout=R(model['cross_rounds'][-1]['leave'])
    comp=compression(ein,eout,alpha,L);fine=R(model['fine_rounds'][-1]['propagated_bound']);E=comp+fine
    ck(local['comparison_matrix']==[[str(U[g,h]) for h in range(r)] for g in range(r)])
    for key,value in [('comparison_matrix_norm_upper',u),('alpha',alpha),('enter',ein),('leave',eout),
                      ('compression_bound',comp),('fine_bound',fine),('model_bound',E)]:ck(R(local[key])==value)
    ck(local['additional_integer_products']==products)
    ck(local['status']=='MODEL_ADMISSION' and E<R(expected_tolerance))
    plan=exact_dp(model);value=R(plan['coarse_optimal_value'])
    expected_files={'block_map.bin':(which,max(1,(r-1).bit_length())),
      'policy_by_remaining_steps.bin':([v for row in plan['policy_by_remaining_steps'] for v in row],max(1,(m-1).bit_length())),
      'initial_support.bin':(expected_ell_num,1),'terminal_indicator.bin':(expected_b,1)}
    packed={}
    for name,(values,bits) in expected_files.items():
        data=(Path(packed_directory)/name).read_bytes();ck(data==pack(values,bits));ck(unpack(data,len(values),bits)==values)
        packed[name]={'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'entries':len(values),'entry_bits':bits}
    old_products=sum(x['sparse_integer_products'] for x in model['norm_certificates'])
    return {'status':'PASS_POLYNOMIAL_OFFLINE_FEEDBACK','checks':checks,'plan':plan,
      'model_error_bound':str(E),'model_error_bound_float':float(E),'alpha':str(alpha),
      'true_value_interval':[str(max(R(0),value-E)),str(min(R(1),value+E))],
      'regret_within_acquired_block_markov_class':str(2*E),
      'confidence':str(expected_confidence),'norm_confidence_route':'Prespecified polynomial block comparison only; enumeration bound not used or selected.',
      'base_result_sha256':expected_base_sha,'length':L,'generators':m,
      'logical_forward_calls_retained':model['logical_forward_calls'],'additional_forward_calls':0,
      'base_norm_integer_products':old_products,'polynomial_norm_integer_products':products,
      'this_receiving_norm_integer_products':old_products+products,
      'packed_files':packed,'packed_map_policy_task_bytes':sum(x['bytes'] for x in packed.values()),
      'coarse_hot_model_bytes':model['compiled_payload_bytes'],
      'scope':'Typed exact algebra receiving under authentic iid, nonanticipating sample sizes/supports, fresh independent probes and unchanged source premises. Does not authenticate those premises. Offline explicit-state simulator only; no physical sensor or arbitrary-history/microscopic policy guarantee.'}


def run():
    start=time.perf_counter();base=(PARENT/'history_sensitive_4096_result.json').read_bytes()
    raw=(PARENT/'history_sensitive_4096_observations.json.gz').read_bytes()
    assert hashlib.sha256(base).hexdigest()==BASE_SHA and hashlib.sha256(raw).hexdigest()==OBS_SHA
    model=json.loads(base);records=json.loads(gzip.decompress(raw))['records']
    for name,digest in model['source_hashes'].items():assert hashlib.sha256((PARENT/name).read_bytes()).hexdigest()==digest
    local=json.loads((ROOT/'block_comparison_results.json').read_text())
    assert local['source_sha256']==hashlib.sha256((ROOT/'check_block_comparison.py').read_bytes()).hexdigest()
    # The fixture's public task is separately bound by the externally pinned
    # source-result artifact. The callable API above accepts caller task data.
    args=dict(expected_b=model['task_b'],expected_ell_num=model['task_ell_numer'],expected_ell_den=model['task_ell_denominator'],
              expected_length=24,expected_tolerance=R(1,50),expected_confidence=R(1,1000),expected_generators=2,expected_base_sha=BASE_SHA,base_bytes=base)
    adversarial=0
    cases=[('expected_length',23),('expected_length',True),('expected_tolerance',R(1,25)),('expected_tolerance',.02),
           ('expected_confidence',R(1,100)),('expected_generators',1),('expected_base_sha','0'*64),
           ('expected_b',[0]*model['n'])]
    for key,v in cases:
        bad=args.copy();bad[key]=v
        try:preflight(model,local,**bad)
        except AssertionError:adversarial+=1
        else:raise AssertionError('external task substitution accepted')
    mutations=[]
    x=copy.deepcopy(local);x['local_certificates'].pop();mutations.append(x)
    x=copy.deepcopy(local);x['local_certificates'][0]['source_block']=1;mutations.append(x)
    x=copy.deepcopy(local);x['local_certificates'][0]['certificate']['delta']='1/10';mutations.append(x)
    x=copy.deepcopy(local);x['local_certificates'][0]['observed_count_total']=-1;mutations.append(x)
    for x in mutations:
        try:preflight(model,x,**args)
        except AssertionError:adversarial+=1
        else:raise AssertionError('missing/altered local certificate accepted')
    out=replay(model,records,local,**args);out['adversarial_preflight_rejections']=adversarial
    # Historical enumeration is NOT evidence for final admission. Its measured
    # work is still charged; preserving its hash binds the actual record.
    enumraw=(ROOT/'feedback_norm_results.json').read_bytes();enum=json.loads(enumraw)
    out['historical_enumeration_record_sha256']=hashlib.sha256(enumraw).hexdigest()
    out['historical_enumeration_integer_products']=enum['additional_integer_products']
    out['cumulative_experiment_norm_integer_products']=out['base_norm_integer_products']+out['polynomial_norm_integer_products']+enum['additional_integer_products']
    out['seconds']=time.perf_counter()-start
    out['source_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    return out


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    result=run();args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['status','checks','adversarial_preflight_rejections','model_error_bound_float','cumulative_experiment_norm_integer_products','seconds']},indent=2))
