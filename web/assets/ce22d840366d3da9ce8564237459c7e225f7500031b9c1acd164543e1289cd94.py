#!/usr/bin/env python3
"""Executable finite-budget noisy-parity acquisition; no known noise/margin input.
The supplied family promise is essential. The fixture simulator is not a learner oracle.
"""
from fractions import Fraction as F
from pathlib import Path
import json,random

def ceil_log2(q):
    assert q>=1
    b=max(0,q.numerator.bit_length()-q.denominator.bit_length())
    return b+(F(1<<b)<q)

def radius(L,t,N,delta):
    # ln(2^(L+1)*t*(t+1)/delta) <= L+1+ceil_log2(t*(t+1)/delta).
    k=L+1+ceil_log2(F(t*(t+1),1)/delta)
    R=F(1)
    while R*R*N < 2*k: R*=2
    while (R/2)**2*N >= 2*k: R/=2
    return R

def acquire(next_block,L,delta=F(1,10),max_blocks=32768):
    assert 0<delta<=F(1,2)
    data=[];t=1;work=0
    while (1<<t)<=max_blocks:
        N=1<<t
        while len(data)<N:
            u,x,w=next_block()
            assert u in (0,1) and w in (0,1) and 0<=x<(1<<L)
            data.append((x,u^w))
        best_count=-N-1;best=None
        for r in range(1<<L):
            score=sum(1 if (((r&x).bit_count()^y)&1)==0 else -1 for x,y in data)
            work+=N
            if score>best_count: best_count=score;best=r
        R=radius(L,t,N,delta)
        c=F(best_count,N)
        if c>=4*R:
            cert=c-R
            return {'status':'ACQUIRED','mask':best,'L':L,'blocks':N,
                    'observed_bits':N*(L+2),'certificate':str(cert),
                    'parity_evaluations':work,'mask_bits':L,'stage':t}
        t+=1
    return {'status':'UNKNOWN','blocks':len(data),'observed_bits':len(data)*(L+2),
            'parity_evaluations':work,'reason':'finite external sample budget exhausted'}

def suffix_feature(mask,x,w):
    return 1 if (((mask&x).bit_count()^w)&1)==0 else -1

if __name__=='__main__':
    fixtures=[]
    for L,eta,seed in [(5,F(0),1),(5,F(1,8),2),(8,F(1,4),3)]:
        rng=random.Random(seed);secret=rng.randrange(1<<L)
        def next_block():
            u=rng.randrange(2);x=rng.randrange(1<<L)
            noise=int(rng.randrange(eta.denominator)<eta.numerator)
            y=((secret&x).bit_count()&1)^noise
            return u,x,u^y
        out=acquire(next_block,L,max_blocks=32768)
        assert out['status']=='ACQUIRED'
        assert out['mask']==secret
        assert 0<F(out['certificate'])<=1-2*eta
        for x in range(1<<L):
            for w in (0,1):
                assert suffix_feature(out['mask'],x,w)==(1 if (((secret&x).bit_count()^w)&1)==0 else -1)
        fixtures.append({'L':L,'eta':str(eta),'secret_for_fixture_only':secret,'result':out})
    p=Path(__file__).with_name('acquisition_results.json')
    p.write_text(json.dumps({'status':'PASS','scope':'Three seeded finite fixtures; not statistical theorem validation','fixtures':fixtures},indent=2)+'\n')
    print(json.dumps({'status':'PASS','fixtures':fixtures}))
