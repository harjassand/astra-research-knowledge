#!/usr/bin/env python3
"""Reproduce a false q^6 reduction if unused-layer verification is omitted."""
import json
from pathlib import Path
import top_digit_deflation_audit as a

def run():
    h,e=7,4
    R=a.ChainRing(h,e)
    H={(2,0,1):1,(0,3,0):1,(0,0,3):1,(1,1,1):1}
    def value(x):
        xs=[(x>>(i*R.m))&((1<<R.m)-1) for i in range(3)]
        return R.functional(a.ring_polynomial(R,H,xs))
    raw=a.extract_anf(value,3*R.m)
    changed=set(raw)
    changed.symmetric_difference_update({1<<(2*R.d)})
    base=a.brute_sum(raw,3*R.m)
    changed_sum=a.brute_sum(changed,3*R.m)
    center,_=a.gradient_data(changed,h,e)
    try:
        a.count_by_forcing(changed,h,e)
    except ValueError as exc:
        rejection=str(exc)
    else:
        raise AssertionError('compression gate should reject this input')
    assert center==[0,0,0] and base!=0 and changed_sum==0
    out=dict(status='decisive compression-gate counterexample verified',d=R.d,e=e,n=3*R.m,
        unchanged_residue_center=center,added_linear_bit=2*R.d,base_signed_count=base,
        perturbed_signed_count=changed_sum,rejection=rejection,raw_anf=sorted(changed))
    Path(__file__).with_name('top_digit_compression_failure.json').write_text(json.dumps(out,indent=2)+'\n')
    return out

if __name__=='__main__':
    print(json.dumps({k:v for k,v in run().items() if k!='raw_anf'}))
