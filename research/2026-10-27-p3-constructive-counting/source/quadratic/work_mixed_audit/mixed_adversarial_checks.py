#!/usr/bin/env python3
"""Independent exact adversarial checks for mixed quadratic acquisition.

Uses hidden A,S only to manufacture/check the existence witness. It also
enumerates every alternating K on the cleaned basis and checks exact
mixed phase sums with finite Walsh expansion and exhaustive leaves.
"""
import itertools
import json
import random
from pathlib import Path


def bits(x):
    while x:
        b=x&-x
        yield b.bit_length()-1
        x^=b


def parity(x): return x.bit_count()&1
def transpose(rows,width):
    out=[0]*width
    for i,row in enumerate(rows):
        for j in bits(row): out[j]^=1<<i
    return out
def multiply(a,b):
    out=[]
    for row in a:
        value=0
        for j in bits(row): value^=b[j]
        out.append(value)
    return out
def rank(rows):
    pivots={}
    for row in rows:
        while row:
            p=(row&-row).bit_length()-1
            if p in pivots: row^=pivots[p]
            else: pivots[p]=row;break
    return len(pivots)
def submatrix(a,ri,ci):
    return [sum(((a[i]>>j)&1)<<t for t,j in enumerate(ci)) for i in ri]
def alt(n,edges):
    rows=[0]*n
    for i,j in edges:
        assert i!=j
        rows[i]^=1<<j;rows[j]^=1<<i
    return rows
def alt_check(a):
    return a==transpose(a,len(a)) and all(not(row>>i&1) for i,row in enumerate(a))
def edge_weight(a): return sum(row.bit_count() for row in a)//2
def quadratic(a,x):
    out=0
    for i in bits(x): out^=parity(a[i]&x&~((1<<(i+1))-1))
    return out


def column_basis(rows,width):
    columns=transpose(rows,width)
    chosen=[];current=[]
    for i,c in enumerate(columns):
        if rank(current+[c])>len(current): chosen.append(i);current.append(c)
    return chosen


def inverse(rows,n):
    a=[row|(1<<(n+i)) for i,row in enumerate(rows)]
    for col in range(n):
        p=next(i for i in range(col,n) if a[i]>>col&1)
        a[col],a[p]=a[p],a[col]
        for i in range(n):
            if i!=col and a[i]>>col&1: a[i]^=a[col]
    assert [row&((1<<n)-1) for row in a]==[1<<i for i in range(n)]
    return [row>>n for row in a]


def left_inverse(u,d):
    if d==0: return []
    chosen=[];current=[]
    for i,row in enumerate(u):
        if rank(current+[row])>len(current): chosen.append(i);current.append(row)
    assert len(chosen)==d
    inv=inverse(current,d)
    return [sum(((row>>j)&1)<<chosen[j] for j in range(d)) for row in inv]


def alternating_matrices(d):
    pairs=list(itertools.combinations(range(d),2))
    for mask in range(1<<len(pairs)):
        yield alt(d,[pair for j,pair in enumerate(pairs) if mask>>j&1])


def make_a(feature_rows,r):
    assert r%2==0
    j=alt(r,[(i,i+1) for i in range(0,r,2)])
    return multiply(multiply(feature_rows,j),transpose(feature_rows,r))


def witness(a,s,delta):
    n=len(a);b=[x^y for x,y in zip(a,s)]
    h={i for i,row in enumerate(s) if row.bit_count()>delta}
    c=[i for i in range(n) if i not in h]
    ac=submatrix(a,c,c)
    pivot_local=column_basis(ac,len(c))
    pivots=[c[i] for i in pivot_local]
    j={v for i in pivots for v in c if s[v]>>i&1}
    removed=h|j
    remain=[i for i in range(n) if i not in removed]
    raw_u=submatrix(b,remain,pivots)
    assert raw_u==submatrix(a,remain,pivots)
    surviving=column_basis(raw_u,len(pivots))
    chosen_pivots=[pivots[i] for i in surviving]
    u=submatrix(b,remain,chosen_pivots)
    d=len(chosen_pivots)
    assert rank(u)==d
    target=submatrix(a,remain,remain)
    ell=left_inverse(u,d)
    assert multiply(ell,u)==[1<<i for i in range(d)]
    k=multiply(multiply(ell,target),transpose(ell,len(remain)))
    assert alt_check(k)
    recovered=multiply(multiply(u,k),transpose(u,d))
    assert recovered==target
    br=submatrix(b,remain,remain)
    residual=[x^y for x,y in zip(br,recovered)]
    budget=edge_weight(s)
    assert edge_weight(residual)<=budget
    assert len(removed)<=2*budget//(delta+1)+len(pivots)*delta
    # Search K without using A; the hidden factorization merely proves one exists.
    tested=0;accepted=None
    for candidate in alternating_matrices(d):
        tested+=1
        low=multiply(multiply(u,candidate),transpose(u,d))
        sparse=[x^y for x,y in zip(br,low)]
        if edge_weight(sparse)<=budget:
            accepted=(candidate,sparse)
            break
    assert accepted is not None
    return dict(b=b,h=sorted(h),initial_pivots=pivots,removed=sorted(removed),
                remain=remain,chosen_pivots=chosen_pivots,u=u,k=k,
                rank_a=rank(a),rank_a_remaining=rank(target),clean_basis_rank=d,
                budget=budget,delta=delta,accepted_k=accepted[0],
                accepted_residual=accepted[1],k_candidates_tested=tested)


def evaluate_poly(poly,x): return sum((x&s)==s for s in poly)&1


def restrict_poly(poly,n,remain,removed,assignment):
    rloc={v:i for i,v in enumerate(remain)}
    eloc={v:i for i,v in enumerate(removed)}
    result=set()
    for term in poly:
        out=0;vanish=False
        for i in bits(term):
            if i in eloc:
                if not assignment>>eloc[i]&1: vanish=True;break
            else: out|=1<<rloc[i]
        if not vanish:
            if out in result: result.remove(out)
            else: result.add(out)
    return result


def mixed_sum(poly,w):
    b=w['b'];n=len(b);r=w['remain'];e=w['removed']
    u=w['u'];d=w['clean_basis_rank'];k=w['accepted_k'];s=w['accepted_residual']
    low=multiply(multiply(u,k),transpose(u,d))
    correction=sum(quadratic(k,row)<<i for i,row in enumerate(u))
    for z in range(1<<len(r)):
        linear_forms=sum(parity(sum(((u[i]>>j)&1)<<i for i in range(len(r)))&z)<<j
                         for j in range(d))
        assert quadratic(low,z)==(quadratic(k,linear_forms)^parity(correction&z))
    walsh=[sum((-1)**(quadratic(k,y)^parity(alpha&y)) for y in range(1<<d))
           for alpha in range(1<<d)]
    result=0;leaf_sums=0
    for assignment in range(1<<len(e)):
        fixed=sum(((assignment>>j)&1)<<v for j,v in enumerate(e))
        boundary_constant=quadratic(b,fixed)
        boundary_linear=sum(parity(b[v]&fixed)<<j for j,v in enumerate(r))
        restricted=restrict_poly(poly,n,r,e,assignment)
        numerator=0
        for alpha,coefficient in enumerate(walsh):
            if not coefficient: continue
            frequency=sum(parity(row&alpha)<<i for i,row in enumerate(u))
            linear=boundary_linear^correction^frequency
            zsum=sum((-1)**(evaluate_poly(restricted,z)^quadratic(s,z)^parity(linear&z)^boundary_constant)
                     for z in range(1<<len(r)))
            numerator+=coefficient*zsum;leaf_sums+=1
        assert numerator%(1<<d)==0
        result+=numerator//(1<<d)
    direct=sum((-1)**(evaluate_poly(poly,x)^quadratic(b,x)) for x in range(1<<n))
    assert result==direct
    return result,leaf_sums


def main():
    rng=random.Random(20261104)
    fixtures=[]
    # Error mass concentrated on a high-degree row/column.
    v=[1,2,3,1,2,3,1,2,3,1]
    fixtures.append(('concentrated star corruption',make_a(v,2),alt(10,[(0,j) for j in range(1,8)]),2))
    # Both basis columns are deleted as corrupted rows; they remain usable columns.
    v=[1,2,3,1,2,3,1,2]
    fixtures.append(('both pivot indices inside removed set',make_a(v,2),alt(8,[(0,1)]),1))
    # The cleaned column span is strictly larger than col(A_RR).
    v=[1]+[2]*7
    fixtures.append(('rank two to zero, cleaned basis rank one',make_a(v,2),alt(8,[(0,1)]),1))
    # Original rank four, surviving A rank two, cleaned basis rank three.
    v=[1,2,4,8,2,4,8,6,10,14]
    fixtures.append(('rank four to two, cleaned basis rank three',make_a(v,4),alt(10,[(0,1),(2,3)]),1))
    # High-degree removal annihilates the entire low-rank principal block.
    v=[1]+[2]*7
    fixtures.append(('empty basis after high-degree deletion',make_a(v,2),alt(8,[(0,j) for j in range(1,8)]),2))
    v=[1,2,4,8,3,5,6,9,10,12]
    fixtures.append(('no sparse corruption',make_a(v,4),alt(10,[]),2))
    fixtures.append(('zero low-rank component',[0]*8,alt(8,[(0,j) for j in range(1,8)]+[(2,3)]),2))
    v=[1,1,2,2,3,3,1,1,2,2,3,3]
    a=make_a(v,2);s=alt(12,[(i,i+1) for i in range(0,12,2)])
    assert rank([x^y for x,y in zip(a,s)])==12
    fixtures.append(('observed matrix dense and full rank',a,s,1))
    v=[1,2,2,0,0,0,0,0]
    fixtures.append(('short supercode word must be punctured',make_a(v,2),alt(8,[(0,1)]),1))
    # Additional small overlapping/correlated constructions.
    for trial in range(12):
        n=8+trial%3;r=2 if trial%2==0 else 4
        v=[1<<i for i in range(r)]+[rng.randrange(1,1<<r) for _ in range(n-r)]
        a=make_a(v,r)
        all_edges=list(itertools.combinations(range(n),2))
        errors=rng.sample(all_edges,1+trial%7)
        fixtures.append((f'correlated random {trial}',a,alt(n,errors),1+trial%3))
    records=[]
    for name,a,s,delta in fixtures:
        assert alt_check(a) and alt_check(s)
        w=witness(a,s,delta)
        n=len(a)
        cubic=[sum(1<<i for i in t) for t in itertools.combinations(range(n),3)]
        poly=set(rng.sample(cubic,min(n+3,len(cubic))))
        poly.add(0)
        value,leaves=mixed_sum(poly,w)
        records.append(dict(name=name,variables=n,
                            **{key:w[key] for key in ['rank_a','rank_a_remaining','clean_basis_rank','budget','delta',
                               'h','initial_pivots','removed','chosen_pivots','k_candidates_tested']},
                            exact_mixed_phase_sum=value,exact_leaf_sums=leaves,
                            observed_matrix_rank=rank(w['b']),observed_matrix_edges=edge_weight(w['b']),
                            pivot_inside_removed=bool(set(w['initial_pivots'])&set(w['removed'])),
                            a_rows=a,s_rows=s,local_polynomial=sorted(poly)))
    by_name={r['name']:r for r in records}
    assert by_name['rank two to zero, cleaned basis rank one']['clean_basis_rank']==1
    assert by_name['rank two to zero, cleaned basis rank one']['rank_a_remaining']==0
    assert by_name['rank four to two, cleaned basis rank three']['clean_basis_rank']==3
    assert by_name['rank four to two, cleaned basis rank three']['rank_a_remaining']==2
    assert by_name['both pivot indices inside removed set']['pivot_inside_removed']
    assert by_name['empty basis after high-degree deletion']['clean_basis_rank']==0
    out=dict(status='all assertions passed',fixtures=len(records),records=records,
             limitation='Finite witness and Walsh checks use hidden decomposition and exhaustive leaf sums; no asymptotic phase counter execution.')
    Path(__file__).with_name('mixed_adversarial_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='records'},indent=2))
    for r in records[:9]:
        print(json.dumps({k:r[k] for k in ['name','rank_a','rank_a_remaining','clean_basis_rank',
                                         'removed','initial_pivots','exact_mixed_phase_sum']},sort_keys=True))


if __name__=='__main__': main()
