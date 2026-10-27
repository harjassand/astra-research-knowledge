#!/usr/bin/env python3
"""Exact uniformizer support acquisitions, including small residue fields."""
from nilpotent_support import *
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'work_local_algebra_agent'))
from local_algebra_acquisition import ChainRing


def transpose_columns(columns):
    n=len(columns)
    return [sum(((columns[j]>>i)&1)<<j for j in range(n)) for i in range(n)]


def random_ring_base(h,e,b,rng):
    R=ChainRing(h,e); m=R.m; n=b*m
    gram=R.gram(); invgram=[solve(gram,1<<j) for j in range(m)]
    phi=[R.mul(1<<j,1<<j) for j in range(m)]
    adjphi=compose(invgram,compose(transpose_columns(phi),gram))
    B=[0]*n
    for i in range(b):
        a=rng.getrandbits(m)
        local=[R.mul(a,phi[j])^linear_apply(adjphi,R.mul(a,1<<j)) for j in range(m)]
        for col,x in enumerate(local): B[i*m+col]^=linear_apply(gram,x)<<(i*m)
        for j in range(i+1,b):
            alpha,beta,gamma=[rng.getrandbits(m) for _ in range(3)]
            local=[R.mul(alpha,1<<t)^R.mul(beta,phi[t])^linear_apply(adjphi,R.mul(gamma,1<<t)) for t in range(m)]
            for col,x in enumerate(local):
                functional=linear_apply(gram,x)
                B[j*m+col]^=functional<<(i*m)
                for row in bits(functional): B[i*m+row]^=1<<(j*m+col)
    assert all(not (B[i]>>i&1) for i in range(n))
    return B


def ring_defect(U,h,e,b):
    d=h.bit_length()-1; n=b*d*e; gram=trace_gram(h)
    forms=[ring_gram_apply(u,gram,d,e,b) for u in U]; D=[0]*n
    for u,v in zip(forms[::2],forms[1::2]):
        for i in range(n): D[i]^=(v if u>>i&1 else 0)^(u if v>>i&1 else 0)
    return D


def run():
    rng=random.Random(382461); cases=[]
    for h,e,b,r in [(0xb,8,3,6),(0xb,12,3,10),(0x13,8,3,8),(0x43,7,3,6),(0xb,16,3,16)]:
        d=h.bit_length()-1; n=d*e*b; base=random_ring_base(h,e,b,rng)
        U=[rng.getrandbits(n) for _ in range(r)]; D=ring_defect(U,h,e,b)
        raw=[x^y for x,y in zip(base,D)]
        recovered,error,cert=acquire_nilpotent_base(raw,h,e,b)
        assert recovered==base and error==D and cert['recovered_rank']==r
        for _ in range(1024):
            x=rng.getrandbits(n)
            assert quadratic_value(raw,x)==quadratic_value(recovered,x)^quadratic_value(error,x)
        case=dict(n=n,d=d,e=e,b=b,r=r,field_modulus=h,raw_matrix=raw,
            planted_base=base,planted_defect=D,certificate=cert,pointwise_checks=1024)
        cases.append(case)
        print(json.dumps(dict(n=n,d=d,e=e,r=r,krylov_rank=cert['krylov_rank'],seconds=cert['seconds'])),flush=True)
    # A nonordinary rank-two base candidate hidden completely in ker N.
    h=0x83; d=7; e=8; b=3; n=b*d*e
    U=[sum(rng.getrandbits(d)<<(d*(e*i+e-1)) for i in range(b)) for _ in range(2)]
    D=ring_defect(U,h,e,b)
    base,error,cert=acquire_nilpotent_base(D,h,e,b)
    assert base==D and not any(error) and len(span(D))==2
    try: recover_band_coefficients(D,h,1)
    except ValueError as failure: rejection=str(failure)
    else: raise AssertionError('the kernel example must be outside ordinary field bandwidth')
    failures=[dict(kind='annihilator kernel larger than ordinary base',n=n,d=d,e=e,
        hidden_rank=2,recovered_rank=0,base_fit_required=cert['base_fit_required'],
        necessary_field_band_test=rejection,raw_matrix=D,
        meaning='exact matrix decomposition only; complete ring counter must reject this base fit')]
    return dict(status='all exact assertions passed',cases=cases,failures=failures,
        scope='matrix acquisition executed; ordinary polynomial fit and counting belong to the root compiler')


if __name__=='__main__':
    result=run(); Path(__file__).with_name('nilpotent_support_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(status=result['status'],cases=len(result['cases']),failures=len(result['failures']))))
