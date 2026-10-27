#!/usr/bin/env python3
"""Exact decoding, acquisition and signed-count validators."""
import json,random,time
from pathlib import Path
from field_rank_decoder import *


def truth_sum(poly,n):
    size=1<<n; universe=(1<<size)-1; variables=[]
    for i in range(n):
        run=1<<i; word=((1<<run)-1)<<run; length=2*run
        while length<size: word|=word<<length; length*=2
        variables.append(word)
    truth=0
    for term in poly:
        value=universe
        for i in bits(term): value&=variables[i]
        truth^=value
    return size-2*truth.bit_count()


def random_defect(n,r,rng):
    forms=[]
    while len(forms)<r:
        x=rng.randrange(1,1<<n)
        if len(span(forms+[x]))>len(forms): forms.append(x)
    B=[0]*n
    for u,v in zip(forms[::2],forms[1::2]):
        for i in range(n): B[i]^=(v if u>>i&1 else 0)^(u if v>>i&1 else 0)
    assert len(span(B))==r
    return B


def congruence(B,columns):
    n=len(B); out=[0]*n
    for i,u in enumerate(columns):
        for j,v in enumerate(columns):
            val=xor_all((B[k]&v).bit_count()&1 for k in bits(u))
            out[i]|=val<<j
    return out


def run():
    rng=random.Random(72919); decodes=[]
    for h in [0b100101,0b1000011,0b10000011,0x11b,0x409]:
        d=h.bit_length()-1; q=1<<d; t=(d-3)//2
        for error_rank in range(t+1):
            for repetition in range(3):
                f=[rng.randrange(q) for _ in range(3)]
                error_basis=[]
                while len(error_basis)<error_rank:
                    x=rng.randrange(1,q)
                    if len(span(error_basis+[x]))>len(error_basis): error_basis.append(x)
                errors=[linear_apply(error_basis,rng.randrange(1<<error_rank)) for _ in range(d)]
                received=[linearized_value(f,1<<i,h)^errors[i] for i in range(d)]
                acquired,cert=decode_gabidulin(received,h)
                assert acquired==f
                decodes.append(dict(d=d,modulus=h,error_rank=len(span(errors)),decoded=f,certificate=cert))
    cases=[]
    for h,r,seed in [(0b10000011,2,7101),(0x11b,2,8101),(0x409,2,10101),(0x1053,4,12101)]:
        raw,n,oracle,old_count,metadata=fixture(h,seed)
        rng=random.Random(seed+10); defect=random_defect(n,r,rng)
        for i in range(n):
            for j in range(i+1,n):
                if defect[i]>>j&1:
                    term=(1<<i)|(1<<j)
                    if term in raw: raw.remove(term)
                    else: raw.add(term)
        print(json.dumps({'stage':'decode_and_count','n':n,'defect_rank':r}),flush=True)
        acquired=compile_rank_perturbed(raw,n,retain_leaf_data=True)
        transformed=congruence(defect,acquired['coordinate_columns'])
        assert acquired['acquired_defect']==transformed
        assert acquired['acquired_defect_rank']==r
        if n<=24:
            exact=truth_sum(raw,n); assert acquired['signed_count']==exact
            acquired['exhaustive_truth_assignments']=1<<n
        else: acquired['exhaustive_truth_assignments']=0
        fpoly={tuple(t['exponents']):t['coefficient'] for t in acquired['field_polynomial']}
        d=acquired['field_extension_degree']; q=1<<d
        for _ in range(1024):
            y=rng.randrange(1<<n); x=linear_apply(acquired['coordinate_columns'],y)
            values=[(y>>(d*i))&(q-1) for i in range(3)]
            assert polynomial_value(raw,x)==(gf_trace(field_polynomial_value(fpoly,values,acquired['field_modulus']),acquired['field_modulus'])^quadratic_value(transformed,y))
            factored=xor_all(((a&y).bit_count()&1)*((b&y).bit_count()&1) for a,b in zip(acquired['symplectic_factors'][::2],acquired['symplectic_factors'][1::2]))^((acquired['linear_correction']&y).bit_count()&1)
            assert factored==quadratic_value(transformed,y)
        acquired.update(metadata,planted_defect=defect,pointwise_identity_checks=1024)
        cases.append(acquired)
        Path(__file__).with_name('field_rank_results.json').write_text(json.dumps(dict(status='all completed cases passed',decoder_cases=decodes,cases=cases),indent=2)+'\n')
        print(json.dumps({k:acquired[k] for k in ['original_variables','acquired_defect_rank','signed_count','zero_count','seconds']}),flush=True)
    return dict(status='all exact assertions passed',decoder_cases=decodes,cases=cases)


if __name__=='__main__':
    result=run(); Path(__file__).with_name('field_rank_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(status=result['status'],decoder_tests=len(result['decoder_cases']),raw_cases=len(result['cases']))))
