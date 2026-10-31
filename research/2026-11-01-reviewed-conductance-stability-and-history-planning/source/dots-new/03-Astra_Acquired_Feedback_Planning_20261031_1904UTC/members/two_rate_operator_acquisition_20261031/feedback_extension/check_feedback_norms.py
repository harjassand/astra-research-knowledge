#!/usr/bin/env python3
"""Acquire all finite block-feedback complement norms from frozen observations."""
from pathlib import Path
import gzip
import hashlib
import json
import sys
import time

ROOT=Path(__file__).resolve().parent;PARENT=ROOT.parent
sys.path.insert(0,str(PARENT))
from sparse_norm_probe import upper_norm,R
from quadratic_leakage import sqrt_up
from retained_large_acquisition import compression


def main():
    start=time.perf_counter();model=json.loads((PARENT/'history_sensitive_4096_result.json').read_text())
    records=json.loads(gzip.decompress((PARENT/'history_sensitive_4096_observations.json.gz').read_bytes()))['records']
    coarse=[x for x in records if x['kind']=='coarse'];parts=model['partition'];n=model['n'];r=len(parts);m=model['m']
    assert m==2 and len(coarse)==2 and len({x['N'] for x in coarse})==1
    N=coarse[0]['N'];certificates=[];total_ops=0
    for mask in range(1<<r):
        policy=[(mask>>g)&1 for g in range(r)];rows=[None]*n
        for g,part in enumerate(parts):
            for i in part:rows[i]=coarse[policy[g]]['counts'][i]
        actual_total=sum(v for row in rows for _,v in row)
        # upper_norm normalizes by the count total; rescale to the common
        # observation denominator afterward. A selected-row C need not be stochastic.
        cert=upper_norm(rows,actual_total,parts,R(model['delta'])/(8*(1<<r)),seed=2000003+mask)
        bound=R(actual_total,N)*R(cert['upper']);total_ops+=cert['sparse_integer_products']
        certificates.append({'policy':policy,'selected_count_total':actual_total,'common_observation_denominator':N,
                             'scaled_norm_upper':str(bound),'certificate':cert})
        print(mask,float(bound),cert['execution_seconds'],flush=True)
    alpha=max(R(x['scaled_norm_upper']) for x in certificates)+sqrt_up(m)*R(model['coarse_spectral_radius'])
    enter=sqrt_up(m)*R(model['cross_rounds'][-1]['enter']);leave=R(model['cross_rounds'][-1]['leave'])
    comp=compression(enter,leave,alpha,model['length']);fine=R(model['fine_rounds'][-1]['propagated_bound'])
    eps=R(model['epsilon']);status='MODEL_ADMISSION' if comp+fine<eps else 'INCONCLUSIVE_THIS_CERTIFICATE'
    out={'status':status,'alpha':str(alpha),'enter':str(enter),'leave':str(leave),
         'compression_bound':str(comp),'fine_bound':str(fine),'model_bound':str(comp+fine),
         'epsilon':str(eps),'delta':model['delta'],'policies':certificates,
         'additional_forward_calls':0,'retained_forward_calls':model['logical_forward_calls'],
         'additional_integer_products':total_ops,'original_already_paid_norm_integer_products':model['sparse_norm_integer_products'],
         'seconds':time.perf_counter()-start,
         'scope':'Exploratory acquired macro-Markov-feedback family; no execution of equipment, no optimal microscopic/history feedback claim, no independent review.',
         'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         'base_result_sha256':hashlib.sha256((PARENT/'history_sensitive_4096_result.json').read_bytes()).hexdigest()}
    (ROOT/'feedback_norm_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(status,float(alpha),float(comp+fine),total_ops,flush=True)


if __name__=='__main__':main()
