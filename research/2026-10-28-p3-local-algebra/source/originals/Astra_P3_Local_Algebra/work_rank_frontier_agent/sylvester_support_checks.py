#!/usr/bin/env python3
"""Exact tests of manufactured global support recovery, without timing claims."""
from sylvester_support import *


def first_modulus(d):
    return next(h for h in range((1<<d)|1,1<<(d+1),2) if irreducible_binary(h))


def random_base(h,b,s,rng):
    d=h.bit_length()-1; n=d*b; q=1<<d; gram=trace_gram(h)
    B=[0]*n
    for i in range(b):
        cs={t:rng.randrange(q) for t in range(1,s+1)}
        for t in range(d):
            x=1<<t; y=0
            for power,c in cs.items():
                y^=gf_mul(c,gf_pow(x,1<<power,h),h)
                y^=gf_mul(gf_pow(c,1<<(d-power),h),gf_pow(x,1<<(d-power),h),h)
            B[i*d+t]^=linear_apply(gram,y)<<(i*d)
        for j in range(i+1,b):
            cs={t:rng.randrange(q) for t in range(-s,s+1)}
            for col in range(d):
                image=xor_all(gf_mul(c,gf_pow(1<<col,1<<(t%d),h),h) for t,c in cs.items())
                functional=linear_apply(gram,image)
                B[j*d+col]^=functional<<(i*d)
                for row in bits(functional): B[i*d+row]^=1<<(j*d+col)
    assert not any(B[i]>>i&1 for i in range(n))
    return B


def defect_from_support(U,h,b):
    d=h.bit_length()-1; n=d*b; gram=trace_gram(h)
    forms=[block_apply(gram,u,d,b) for u in U]
    D=[0]*n
    for u,v in zip(forms[::2],forms[1::2]):
        for i in range(n): D[i]^=(v if u>>i&1 else 0)^(u if v>>i&1 else 0)
    return D


def run():
    rng=random.Random(204863); cases=[]
    for d,b,r,s in [(12,9,8,1),(12,17,16,1),(16,13,16,1),(24,21,32,1),(48,9,12,2)]:
        h=first_modulus(d); n=d*b; rawbase=random_base(h,b,s,rng)
        U=[rng.getrandbits(n) for _ in range(r)]; D=defect_from_support(U,h,b)
        raw=[x^y for x,y in zip(rawbase,D)]
        print(json.dumps(dict(stage='matrix acquisition',n=n,d=d,b=b,rank=r,bandwidth=s)),flush=True)
        base,defect,_,cert=acquire_sylvester_base(raw,h,s,method='one_sided')
        assert base==rawbase and defect==D and len(span(D))==r
        for _ in range(1024):
            x=rng.getrandbits(n)
            assert quadratic_value(raw,x)==quadratic_value(base,x)^quadratic_value(defect,x)
        old_accepted=True
        try:
            oldbase,olddefect,_=acquire_quadratic_base(raw,h,s)
        except ValueError: old_accepted=False
        else:
            assert oldbase==rawbase and olddefect==D
        cases.append(dict(n=n,d=d,b=b,bandwidth=s,rank=r,field_modulus=h,
            old_global_radius=(d-(2*s+1))//2,old_block_decoder_accepted=old_accepted,
            scalar_orbit_dimension=cert['scalar_orbit_dimension'],
            syndrome_rank=cert['manufactured_syndrome_rank'],
            certified_orbit_rank=cert['recovered_orbit_rank'],
            probability_bound_exponent=cert['scalar_orbit_dimension']*r-n,
            pointwise_identities=1024,seconds=cert['seconds'],
            raw_matrix=raw,planted_base=rawbase,planted_defect=D,recovered_support=cert['recovered_support']))
    # A deliberate invisible error: it lies in the compatible code itself.
    h=0x1053; d=12; b=3; n=d*b
    compatible=random_base(h,b,1,rng)
    base,defect,_,cert=acquire_sylvester_base(compatible,h,method='one_sided')
    assert base==compatible and not any(defect)
    gram=trace_gram(h); ginv=[solve(gram,1<<j) for j in range(d)]
    hidden_support=independent(block_apply(ginv,x,d,b) for x in compatible)
    sc=scalar_certificate(h,method='one_sided')
    orbit=independent(scalar_vector(c,u,h,b) for c in sc['scalar_orbit_basis'] for u in hidden_support)
    assert len(orbit)<len(sc['scalar_orbit_basis'])*len(hidden_support)
    failures=[dict(kind='invisible codeword defect',n=n,hidden_rank=len(hidden_support),
        recovered_rank=0,orbit_rank=len(orbit),required_direct_rank=len(sc['scalar_orbit_basis'])*len(hidden_support),
        meaning='exact alternative representation, not planted recovery; support promise violated')]
    # Rank saturation: generic errors too large for the scalar orbit are rejected.
    h=0x1053; d=12; b=5; n=d*b; r=12
    base=random_base(h,b,1,rng); U=[rng.getrandbits(n) for _ in range(r)]
    D=defect_from_support(U,h,b); raw=[x^y for x,y in zip(base,D)]
    try: acquire_sylvester_base(raw,h,method='one_sided')
    except ValueError as error: failures.append(dict(kind='orbit saturation',n=n,r=r,rejection=str(error)))
    else: raise AssertionError('expected manufactured-orbit rejection')
    return dict(status='all exact assertions passed',cases=cases,decisive_failures=failures,
        implemented_scope='matrix/representation acquisition; generic field point counting is a cited theorem, not executed')


if __name__=='__main__':
    result=run(); Path(__file__).with_name('sylvester_support_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(status=result['status'],cases=len(result['cases']),failures=len(result['decisive_failures']))))
