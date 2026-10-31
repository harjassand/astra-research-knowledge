#!/usr/bin/env python3
"""A stronger routing fixture: rule out action-count-only prediction too.

The changed source parameter is fixture setup, not learner information.
All acquisition, failed validation and replay remain unchanged algorithms.
"""
from pathlib import Path
import gzip
import hashlib
import json
import time
from retained_large_acquisition import (RoutingSource,acquire,screen,R,
                                       integer_step,integer_output)
from check_retained_large_acquisition import replay

ROOT=Path(__file__).resolve().parent


def main():
    source=RoutingSource(4096);source._tau=.04
    b,e,den=source.public_task();out,records=acquire(source,b,e,den,24,R(1,50))
    assert out['status']=='PASS';out['fixture_tau']='1/25';out['screening']=screen(out,50000)
    compiled=out['compiled'];pairs=[]
    for k in range(25):
        words=[[0]*k+[1]*(24-k),[1]*(24-k)+[0]*k];scores=[]
        for word in words:
            state=compiled['initial_grid_state'][:]
            for a in word:state,_=integer_step(compiled['operators'][a],state)
            scores.append(integer_output(compiled,state))
        pairs.append((abs(scores[0]-scores[1]),k,words,scores))
    spread,k,words,scores=max(pairs,key=lambda x:x[0]);E=R(out['total_bound']);eps=R(out['epsilon'])
    out['history_sensitivity']={'same_count_zero_actions':k,'words':words,'scores':list(map(str,scores)),
        'observed_model_spread':str(spread),'certified_true_spread_lower':str(spread-2*E),
        'action_count_only_epsilon_predictor_impossible':bool(spread-2*E>2*eps),
        'proof':'Both words have the same action multiset. Any count-only scalar predictor has worst error at least half their true spread.'}
    assert out['history_sensitivity']['action_count_only_epsilon_predictor_impossible']
    out['fixture_source_scope']='The driver sets hidden tau=.04; the acquire function sees only its ordinary forward interface and public task. Synthetic aggregate sampling, not billions of executed queries.'
    hashes={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in
            ['history_sensitive_case.py','retained_large_acquisition.py','large_routing_source.py','quadratic_leakage.py','sparse_norm_probe.py']}
    out['source_hashes']=hashes;stem='history_sensitive_4096'
    raw=json.dumps({'n':4096,'records':records},separators=(',',':')).encode();compressed=gzip.compress(raw,mtime=0)
    (ROOT/(stem+'_observations.json.gz')).write_bytes(compressed)
    out['transcript_uncompressed_bytes']=len(raw);out['transcript_gzip_bytes']=len(compressed)
    out['transcript_gzip_sha256']=hashlib.sha256(compressed).hexdigest()
    out['compiled_payload_bytes']=len(json.dumps(compiled,separators=(',',':')).encode())
    (ROOT/(stem+'_result.json')).write_text(json.dumps(out,indent=2)+'\n')
    checks=replay(out,records,expected_b=b,expected_ell_num=e,expected_ell_den=den,expected_length=24,expected_tolerance=eps)
    true=[]
    for word in words:
        value=b[:]
        for a in word:value=source.apply_truth(a,value)
        true.append(sum(value[i] for i in range(len(e)) if e[i])/den)
    assert all(abs(float(v)-w)<float(E) for v,w in zip(scores,true))
    receipt={'status':'PASS','exact_replay_checks':checks,'history_pair_checks':3,
             'floating_posthoc_pair_truth':true,'floating_truth_scope':'Additional numerical check only, not learner input or exact world proof.',
             'model_spread':str(spread),'certified_true_spread_lower':str(spread-2*E),
             'bound_source_hashes':hashes,
             'result_sha256':hashlib.sha256((ROOT/(stem+'_result.json')).read_bytes()).hexdigest()}
    (ROOT/(stem+'_checks.json')).write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps({'status':out['status'],'n':out['n'],'rank':out['rank'],
                     'logical_forward_calls':out['logical_forward_calls'],'bound':float(E),
                     'history_sensitivity':out['history_sensitivity'],'checks':checks},indent=2))


if __name__=='__main__':main()
