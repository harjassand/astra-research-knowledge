#!/usr/bin/env python3
"""Acquire a polynomial sufficient shared block-residual comparison bound.

Standard block-norm domination, not an optimal norm planner or new principle
of numerical analysis. Every local norm is learned from acquired C, not given.
"""
from pathlib import Path
import gzip
import hashlib
import json
import sys
import time
import sympy as s

ROOT=Path(__file__).resolve().parent;PARENT=ROOT.parent;sys.path.insert(0,str(PARENT))
from sparse_norm_probe import upper_norm,R
from quadratic_leakage import sqrt_up
from retained_large_acquisition import compression
sys.path.insert(0,str(PARENT.parent/'robust_operator_reuse_20261031'/'finite_observation'))
from robust_replay import norm_up


def main():
    timer=time.perf_counter();model=json.loads((PARENT/'history_sensitive_4096_result.json').read_text())
    records=json.loads(gzip.decompress((PARENT/'history_sensitive_4096_observations.json.gz').read_bytes()))['records']
    coarse=[x for x in records if x['kind']=='coarse'];parts=model['partition'];r=len(parts);m=model['m'];n=model['n']
    N=coarse[0]['N'];assert all(x['N']==N for x in coarse)
    which=[0]*n;within=[0]*n
    for g,p in enumerate(parts):
        for j,i in enumerate(p):which[i]=g;within[i]=j
    U=s.zeros(r);certificates=[];products=0;attempts=m*r*r
    for a in range(m):
        for g,src in enumerate(parts):
            for h,dest in enumerate(parts):
                k=len(src);l=len(dest);d=k+l;rows=[[] for _ in range(d)]
                for ii,i in enumerate(src):
                    rows[ii]=[(k+within[j],v) for j,v in coarse[a]['counts'][i] if which[j]==h]
                total=sum(v for row in rows for _,v in row)
                if total:
                    # Hermitian-dilation-style zero embedding, though C is
                    # only the upper-right block. The two Q blocks average
                    # the source and target groups separately.
                    cert=upper_norm(rows,total,[list(range(k)),list(range(k,k+l))],
                                    R(model['delta'])/(8*attempts),seed=3000017+a*r*r+g*r+h)
                    bound=R(n*total,d*N)*R(cert['upper']);products+=cert['sparse_integer_products']
                else:cert={'status':'EXACT_ZERO_OBSERVED_BLOCK','sparse_integer_products':0};bound=R(0)
                U[g,h]=max(U[g,h],bound)
                certificates.append({'a':a,'source_block':g,'target_block':h,'embedded_dimension':d,
                                     'observed_count_total':total,'scaled_block_norm_upper':str(bound),'certificate':cert})
        print('action',a,'products',products,flush=True)
    bound=norm_up(U,s.eye(r),bits=30)
    alpha=bound+sqrt_up(m)*R(model['coarse_spectral_radius'])
    enter=sqrt_up(m)*R(model['cross_rounds'][-1]['enter']);leave=R(model['cross_rounds'][-1]['leave'])
    comp=compression(enter,leave,alpha,model['length']);fine=R(model['fine_rounds'][-1]['propagated_bound'])
    out={'status':'MODEL_ADMISSION' if comp+fine<R(model['epsilon']) else 'INCONCLUSIVE_THIS_CERTIFICATE',
         'comparison_matrix':[[str(U[g,h]) for h in range(r)] for g in range(r)],
         'comparison_matrix_norm_upper':str(bound),'alpha':str(alpha),'enter':str(enter),'leave':str(leave),
         'compression_bound':str(comp),'fine_bound':str(fine),'model_bound':str(comp+fine),
         'local_operator_count':attempts,'additional_forward_calls':0,'additional_integer_products':products,
         'local_certificates':certificates,'seconds':time.perf_counter()-timer,
         'confidence_scope':'Replace old norm event by union of m*r*r fresh local-norm events totaling delta/8. No posterior-on-PASS interpretation.',
         'scope':'Acquired polynomial sufficient comparison geometry. Can fail conservatively; no optimal recognition or supplied small residual blocks. Exploratory, not in reviewed archive.',
         'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         'base_result_sha256':hashlib.sha256((PARENT/'history_sensitive_4096_result.json').read_bytes()).hexdigest()}
    (ROOT/'block_comparison_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ['status','alpha','model_bound','local_operator_count','additional_integer_products','seconds']},indent=2))


if __name__=='__main__':main()
