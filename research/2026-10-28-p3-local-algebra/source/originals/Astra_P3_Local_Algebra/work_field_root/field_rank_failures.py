#!/usr/bin/env python3
"""Decisive boundary examples and the actual counter's streaming check."""
from field_rank_decoder import *
from field_kloosterman import kloosterman_dwork,irreducible_binary


def run():
    h=0x409; d=10; n=30; B=[0]*n
    for i in range(d):
        for j in range(i+1,d):
            x,y=1<<i,1<<j
            value=gf_trace(gf_mul(gf_mul(x,x,h),y,h)^gf_mul(x,gf_mul(y,y,h),h),h)
            if value: B[i]^=1<<j; B[j]^=1<<i
    factors,linear=symplectic_factors(B); assert len(factors)==8
    D=[0]*n
    for a,b in zip(factors[:4:2],factors[1:4:2]):
        for i in range(n): D[i]^=(b if a>>i&1 else 0)^(a if b>>i&1 else 0)
    other=[x^y for x,y in zip(B,D)]
    assert len(span(D))==len(span(other))==4
    try: acquire_quadratic_base(D,h)
    except ValueError as e: rejection=str(e)
    else: raise AssertionError('a unique-radius decoder accepted ambiguous midpoint')
    # Both compatible codewords are in the trace-quadratic family.
    for C in [[0]*n,B]:
        base,defect,_=acquire_quadratic_base(C,h)
        assert base==C and not any(defect)
    saved=json.loads(Path(__file__).with_name('field_rank_results.json').read_text())['cases'][0]
    streamed=compile_rank_perturbed(set(saved['raw_polynomial']),saved['original_variables'])
    assert streamed['signed_count']==saved['signed_count']
    assert streamed['walsh_leaf_count']==4 and streamed['walsh_leaves']==[]
    rejected=[]
    for a,mod in [(1,0),(1,1),(1,0b10101),(16,0b10011),(-1,0b10011)]:
        try:kloosterman_dwork(a,mod)
        except ValueError as e: rejected.append(dict(coefficient=a,modulus=mod,reason=str(e)))
        else:raise AssertionError('invalid public backend input accepted')
    return dict(status='all exact assertions passed',ambiguity=dict(
        field_modulus=h,extension_degree=d,original_variables=n,unique_radius=3,
        compatible_codewords=[[0]*n,B],received=D,error_ranks=[4,4],
        decoder_rejection=rejection,meaning='nonunique planted representation; not a counting lower bound'),
        streaming=dict(signed_count=streamed['signed_count'],zero_count=streamed['zero_count'],
            leaves_processed=streamed['walsh_leaf_count'],leaves_retained=0),
        invalid_backend_rejections=rejected)


if __name__=='__main__':
    data=run(); Path(__file__).with_name('field_rank_failures_results.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps(dict(status=data['status'],boundary=data['ambiguity']['error_ranks'],streaming=data['streaming'])))
