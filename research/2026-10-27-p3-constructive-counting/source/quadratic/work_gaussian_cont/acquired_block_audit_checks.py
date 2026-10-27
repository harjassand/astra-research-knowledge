#!/usr/bin/env python3
"""Adversarial exact audit of acquired cubic blocks and retained certificates.

Small exhaustive checks only. No asymptotic phase-counter execution.
"""
import argparse
import itertools
import json
from pathlib import Path
import random
import sys

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"work_dense_cont"))
import cubic_structure_compiler as c
from acquired_block_phase_checks import acquire,truth_sum


def independent_rank(rows):
    basis={}
    for value in rows:
        x=value
        while x:
            p=x.bit_length()-1
            if p in basis: x^=basis[p]
            else:
                basis[p]=x
                break
    return len(basis)


def independent_kernel(rows,n):
    work=list(rows)
    pivot=[]
    r=0
    for col in range(n-1,-1,-1):
        i=next((i for i in range(r,len(work)) if work[i]>>col&1),None)
        if i is None: continue
        work[r],work[i]=work[i],work[r]
        for j in range(len(work)):
            if j!=r and work[j]>>col&1: work[j]^=work[r]
        pivot.append(col);r+=1
    free=[i for i in range(n) if i not in pivot]
    return [(1<<f)|sum(1<<p for p,row in zip(pivot,work[:r]) if row>>f&1) for f in free]


def full_centroid(poly,n):
    triples={tuple(c.indices(t)) for t in poly if t.bit_count()==3}
    def tensor(i,j,k):
        return int(len({i,j,k})==3 and tuple(sorted((i,j,k))) in triples)
    rows=[]
    for i,j,k in itertools.product(range(n),repeat=3):
        left=0;middle=0;right=0
        for a in range(n):
            if tensor(a,j,k):left^=1<<(a+n*i)
            if tensor(i,a,k):middle^=1<<(a+n*j)
            if tensor(i,j,a):right^=1<<(a+n*k)
        rows.extend((left^middle,left^right))
    return independent_kernel(rows,n*n)


def field_mul(x,y,degree,modulus):
    answer=0
    while y:
        if y&1:answer^=x
        y>>=1;x<<=1
        if x>>degree:x^=modulus
    return answer


def field_trace(x,degree,modulus):
    trace=0
    for _ in range(degree):
        trace^=x
        x=field_mul(x,x,degree,modulus)
    assert trace in (0,1)
    return trace


def extension_volume(degree,modulus):
    p=set()
    for i,j,k in itertools.product(range(degree),repeat=3):
        coefficient=field_trace(field_mul(field_mul(1<<i,1<<j,degree,modulus),
                                         1<<k,degree,modulus),degree,modulus)
        if coefficient:p.add((1<<i)|(1<<(degree+j))|(1<<(2*degree+k)))
    return p,3*degree


def idempotent_audit(poly,n,name):
    assert not c.radical(poly,n)
    center=full_centroid(poly,n)
    assert len(center)<=10
    blocks,meta=c.centroid_blocks(poly,n)
    idempotents=0;nilpotents=0;patterns=set()
    for coefficients in range(1<<len(center)):
        A=c.unflat(c.xor_all(center[i] for i in c.indices(coefficients)),n)
        square=c.compose(A,A)
        if square==A:
            idempotents+=1
            pattern=[]
            for block in blocks:
                images=[c.apply(A,v) for v in block]
                if not any(images):pattern.append(0)
                else:
                    assert images==block
                    pattern.append(1)
            patterns.add(tuple(pattern))
        if any(A) and not any(square):nilpotents+=1
    assert idempotents==1<<len(blocks)==len(patterns)
    assert meta['centroid_dimension']==len(center)
    return dict(family=name,n=n,centroid_dimension=len(center),
                all_centroid_elements_enumerated=1<<len(center),
                all_idempotents=idempotents,nonzero_square_zero_elements=nilpotents,
                acquired_block_sizes=list(map(len,blocks)))


def verify_round(record):
    n=record['input_variables'];d=record['third_tensor_rank']
    poly=set(record['input_polynomial']);cols=record['coordinate_columns']
    assert independent_rank(cols)==n
    assert cols[:d]==record['complement_columns']
    assert cols[d:]==record['radical_basis']
    current=c.substitute(poly,n,cols)
    checks=0
    for y in range(1<<n):
        assert c.phase(poly,c.apply(cols,y))==c.phase(current,y)
        checks+=1
    removed=set()
    for update in record['gaussian_pair_updates']:
        i,j=update['variables']
        assert i not in removed and j not in removed
        assert i>=d and j>=d
        other=[v for v in range(n) if v not in removed|{i,j}]
        next_poly=set(update['output_polynomial'])
        for free in range(1<<len(other)):
            x=sum(1<<v for s,v in enumerate(other) if free>>s&1)
            signs=[c.phase(current,x|(a<<i)|(b<<j)) for a,b in itertools.product((0,1),repeat=2)]
            assert sum(signs)==2*c.phase(next_poly,x)
            # Also verify the retained A/B coefficient descriptions pointwise.
            base=c.phase(current,x)
            assert base*c.phase(current,x|(1<<i))==c.phase(set(update['affine_A']),x)
            assert base*c.phase(current,x|(1<<j))==c.phase(set(update['affine_B']),x)
            checks+=1
        current=next_poly;removed.update((i,j))
    active=record['remaining_radical_variables']
    equations=record['linear_equations']
    pre=set(record['pre_affine_polynomial'])
    for u in range(1<<d):
        total=sum(c.phase(current,u|sum(1<<v for s,v in enumerate(active) if z>>s&1))
                  for z in range(1<<len(active)))
        valid=all(((row&u).bit_count()&1)==(row>>d&1) for row in equations)
        expected=(1<<len(active))*c.phase(pre,u) if valid else 0
        assert total==expected
        checks+=1
    if 'inconsistent_equation_subset' in record:
        assert c.xor_all(equations[i] for i in record['inconsistent_equation_subset'])==1<<d
        return checks,True
    offset=record['affine_offset'];kernel=record['affine_kernel_columns']
    nout=record['output_variables'];out=set(record['output_polynomial'])
    assert len(kernel)==nout==d-independent_rank([row&((1<<d)-1) for row in equations])
    assert independent_rank(kernel)==nout
    for t in range(1<<nout):
        u=offset^c.apply(kernel,t)
        assert all(((row&u).bit_count()&1)==(row>>d&1) for row in equations)
        assert c.phase(pre,u)==c.phase(out,t)
        checks+=1
    assert record['factor_exponent']==len(removed)//2+len(active)
    assert record['factor_exponent']+nout<=n
    return checks,False


def certificate_checks():
    source=Path(__file__).resolve().parents[1]/'work_dense_cont'/'cubic_structure_results.json'
    data=json.loads(source.read_text())
    identities=0;rounds=0;zeroes=0
    for result in data['records']:
        records=result.get('radical_rounds',[])
        if 'zero_certificate' in result:
            z=result['zero_certificate']
            records=z['prior_rounds']+[z['failed_round']]
        for record in records:
            count,zero=verify_round(record)
            identities+=count;rounds+=1;zeroes+=int(zero)
        if 'core_variables' in result:
            assert result['factor_exponent']+result['core_variables']<=result['n']
    return dict(retained_rounds_verified=rounds,zero_equation_witnesses=zeroes,
                exact_retention_identity_checks=identities)


def affine_invariance_checks(rng):
    records=[]
    for blocks in (2,3,4):
        n=3*blocks
        base={7<<(3*i) for i in range(blocks)}
        expected_edges=set()
        for i,j in itertools.combinations(range(blocks),2):
            if (i+j)%3!=1 or blocks==2:
                expected_edges.add((i,j))
                base.add((1<<(3*i))|(1<<(3*j+1)))
        base.add(1);base.add(0)
        for sample in range(4):
            hidden=c.random_invertible(n,rng)
            offset=rng.randrange(1<<n)
            raw=c.substitute(base,n,hidden,offset)
            rec=acquire(raw,n)
            assert 'edge_expansion' not in rec  # Expensive diagnostic is not in acquisition.
            assert rec['core_variables']==n and rec['factor_exponent']==0
            assert rec['block_sizes']==[3]*blocks
            back=c.compose(hidden,rec['acquired_columns'])
            owner={}
            for i in range(blocks):
                touched={v//3 for col in back[3*i:3*i+3] for v in c.indices(col)}
                assert len(touched)==1
                owner[i]=next(iter(touched))
            edges={tuple(sorted((owner[i],owner[j]))) for i,j in rec['quadratic_edges']}
            assert edges==expected_edges
            value=truth_sum(raw,n)
            assert value==truth_sum(base,n)==truth_sum(set(rec['transformed_polynomial']),n)
            records.append(dict(n=n,blocks=blocks,affine_offset=offset,
                                edges=sorted(edges),weighted_bound=rec['weighted_bound'],exact_phase_sum=value))
    return records


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--output',default='acquired_block_audit_results.json')
    args=p.parse_args()
    rng=random.Random(20261104)
    indecomposable={(1<<0)|(1<<1)|(1<<5),
                    (1<<0)|(1<<2)|(1<<4),
                    (1<<1)|(1<<2)|(1<<3)}
    cases=[(indecomposable,6,'nonsemisimple primitive six-dimensional block'),
           (indecomposable|{s<<6 for s in indecomposable},12,'two nonsemisimple blocks')]
    for degree,modulus in ((2,0b111),(3,0b1011)):
        poly,n=extension_volume(degree,modulus)
        cases.append((poly,n,f'primitive volume over F_{1<<degree} viewed over F_2'))
    cases.append(({7,7<<3,7<<6},9,'three split volume blocks'))
    idempotents=[idempotent_audit(poly,n,name) for poly,n,name in cases]
    cert=certificate_checks()
    invariance=affine_invariance_checks(rng)
    out=dict(status='all exact assertions passed',scope='independent finite acquisition/certificate audit',
             idempotent_fixtures=len(idempotents),
             centroid_elements_enumerated=sum(x['all_centroid_elements_enumerated'] for x in idempotents),
             affine_disguise_fixtures=len(invariance),
             **cert,idempotents=idempotents,affine_invariance=invariance)
    Path(args.output).write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ('idempotents','affine_invariance')},indent=2))
    for record in idempotents:print(json.dumps(record,sort_keys=True))


if __name__=='__main__':main()
