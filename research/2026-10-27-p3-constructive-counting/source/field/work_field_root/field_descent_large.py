#!/usr/bin/env python3
"""Larger raw hidden-field executions; all fixtures and certificates saved."""
import json, random, time
from pathlib import Path
from field_descent import *

cases=[]
for h,seed in [(0x11b,8001),(0x409,10001),(0x1002d,16001)]:
    print(json.dumps({'stage':'construct_raw_fixture','field_degree':h.bit_length()-1}),flush=True)
    raw,n,oracle,reference,metadata=fixture(h,seed)
    print(json.dumps({'stage':'compile_raw','n':n,'terms':len(raw)}),flush=True)
    result=compile_raw(raw,n)
    assert result['signed_count']==reference
    rng=random.Random(seed+1)
    fpoly={tuple(x['exponents']):x['coefficient'] for x in result['field_polynomial']}
    d=result['field_extension_degree']; q=1<<d
    for _ in range(1024):
        y=rng.randrange(1<<n); x=linear_apply(result['coordinate_columns'],y)
        values=[(y>>(d*i))&(q-1) for i in range(3)]
        assert polynomial_value(raw,x)==oracle(x)
        assert polynomial_value(raw,x)==gf_trace(field_polynomial_value(fpoly,values,result['field_modulus']),result['field_modulus'])
    result.update(metadata,random_original_and_acquired_checks=1024)
    cases.append(result)
    Path(__file__).with_name('field_descent_large_results.json').write_text(json.dumps({'status':'all completed cases passed','cases':cases},indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['original_variables','raw_cubic_terms','centroid_dimension','signed_count','zero_count','seconds']}),flush=True)
