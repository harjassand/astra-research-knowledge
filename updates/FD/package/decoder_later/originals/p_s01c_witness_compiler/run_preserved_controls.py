#!/usr/bin/env python3
"""Rerun the original safe-W/raw implementations without parameter changes."""
import hashlib
import json
from pathlib import Path
import time

import run_witness as rw
wc,fd,ac=rw.wc,rw.fd,rw.ac
HERE=Path(__file__).resolve().parent


def run(n,r,d,seed,prefix_length=None):
    cases=[]
    for mode in ('safe_subspace','raw_body'):
        source=rw.Teacher(n,r,d,seed,prefix_length)
        out,model,prefix=fd.acquire(n,r,d,source.query,seed+1000000,n**-2,prefix_length,mode)
        out['case']=dict(n=n,r=r,degree=d,seed=seed,mode='preserved_'+mode,
                         prefix_length=prefix_length,source_r=None,forced_failure=False)
        out['source_pin']=source.pin()
        out['source_acquisition']=source.receipt()
        out['parameter_checks']=rw.reference.check_parameters(out['parameters'])
        out['learner_local_seconds_estimate']=max(0,out['acquisition_seconds']-source.callback_seconds)
        out['witness_totals']=dict(global_drop=0,paid_dictionaries=0,outer_epochs=0)
        out['parameters']['control_budget']='unchanged original safe-W/raw parameters'
        if model is not None:
            out=rw.verify(source,out,model,prefix,prefix_length)
        out['source_after_test_only_verification']=source.receipt()
        out=rw.resource_proxy(out,n)
        cases.append(out)
        print(json.dumps(rw.summary(out)),flush=True)
    assert len({case['source_pin'] for case in cases})==1
    label=f'n{n}_r{r}_d{d}_seed{seed}'+('' if prefix_length is None else f'_prefix{prefix_length}')
    receipt=dict(scope='preserved original implementations; identical source and beta, original differing raw budgets',
                 beta=n**-2,precision='exact GF(2) and strict integer rank comparisons',cases=cases,
                 source_hashes={str(p.relative_to(HERE)):hashlib.sha256(p.read_bytes()).hexdigest()
                    for p in (HERE/'reference_snapshot').rglob('*.py')})
    (HERE/f'preserved_receipt_{label}.json').write_text(json.dumps(receipt,indent=2)+'\n')


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--case',required=True)
    parser.add_argument('--prefix-k',type=int)
    args=parser.parse_args()
    run(*map(int,args.case.split(':')),args.prefix_k)
