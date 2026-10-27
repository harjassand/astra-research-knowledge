#!/usr/bin/env python3
"""Independent exact checks of erasure/pruning/decoding and Walsh correction.

The existence-witness tests use hidden A,S only to select the guaranteed initial
I,E0; the candidate decoder itself receives only B,I,E0,Delta,M,r. Complete
unknown-decomposition searches are also run on small cases. Counts are exhaustive.
"""
import argparse
import itertools
import json
import math
from pathlib import Path
import random


def bits(mask):
    while mask:
        low=mask&-mask
        yield low.bit_length()-1
        mask^=low


def xor(values):
    answer=0
    for value in values:answer^=value
    return answer


def independent(vectors):
    basis={};kept=[]
    for vector in vectors:
        v=vector
        while v:
            p=v.bit_length()-1
            if p in basis:v^=basis[p]
            else:
                basis[p]=v;kept.append(vector);break
    return kept


def codewords(columns):
    for coefficient in range(1<<len(columns)):
        yield coefficient,xor(columns[i] for i in bits(coefficient))


def restrict_column(B,rows,column):
    return sum(((B[i]>>column)&1)<<j for j,i in enumerate(rows))


def alternating(B):
    return all(not (row>>i&1) for i,row in enumerate(B)) and all(
        (B[i]>>j&1)==(B[j]>>i&1) for i in range(len(B)) for j in range(i))


def qvalue(B,x):
    return sum((B[i]&x&~((1<<(i+1))-1)).bit_count() for i in bits(x))&1


def decode_candidate(B,I,E0,delta,M,r):
    n=len(B);R=[i for i in range(n) if i not in E0]
    steps=[]
    while True:
        columns=independent([restrict_column(B,R,j) for j in I])
        small=next(((a,v) for a,v in codewords(columns)
                    if v and v.bit_count()<=2*delta),None)
        if small is None:break
        coefficient,word=small
        removed=[R[i] for i in bits(word)]
        old_rank=len(columns)
        R=[v for v in R if v not in removed]
        new_rank=len(independent([restrict_column(B,R,j) for j in I]))
        assert new_rank<old_rank
        steps.append(dict(removed=removed,rank_before=old_rank,rank_after=new_rank,
                          codeword_coefficients=coefficient))
    assert len(steps)<=r
    assert sum(len(s['removed']) for s in steps)<=2*r*delta
    decoded=[]
    for j in R:
        received=restrict_column(B,R,j)
        close=[v for _,v in codewords(columns) if (v^received).bit_count()<=delta]
        assert len(close)<=1
        if not close:return None
        decoded.append(close[0])
    C=[sum(((col>>i)&1)<<j for j,col in enumerate(decoded)) for i in range(len(R))]
    if not alternating(C):return None
    if len(independent(C))>r:return None
    residual=[restrict_column(B,R,i)^C[j] for j,i in enumerate(R)]
    # B and C are symmetric, so restricting a column is also the corresponding row.
    errors=sum(row.bit_count() for row in residual)//2
    if errors>M:return None
    return dict(R=R,E=[i for i in range(n) if i not in R],I=list(I),E0=sorted(E0),
                code_columns=columns,decoded=C,residual=residual,error_edges=errors,
                prune_steps=steps)


def witness(A,S,r,M,delta):
    n=len(A);H={i for i,row in enumerate(S) if row.bit_count()>delta}
    allowed=[i for i in range(n) if i not in H]
    cols=[];I=[]
    for j in allowed:
        column=restrict_column(A,allowed,j)
        if len(independent(cols+[column]))>len(cols):
            cols.append(column);I.append(j)
    assert len(I)<=r
    J={j for i in I for j in allowed if S[i]>>j&1}
    E0=H|J
    assert len(H)<=2*M//delta and len(J)<=r*delta
    assert len(E0)<=2*M//delta+r*delta
    return I,E0


def inverse(rows):
    n=len(rows);a=[row|((1<<i)<<n) for i,row in enumerate(rows)]
    for j in range(n):
        i=next(i for i in range(j,n) if a[i]>>j&1)
        a[i],a[j]=a[j],a[i]
        for i in range(n):
            if i!=j and a[i]>>j&1:a[i]^=a[j]
    return [row>>n for row in a]


def transpose(rows,width):
    return [sum(((row>>i)&1)<<j for j,row in enumerate(rows)) for i in range(width)]


def matmul(a,b):
    return [xor(b[j] for j in bits(row)) for row in a]


def factor_decoded(C):
    n=len(C)
    columns=independent([sum(((C[i]>>j)&1)<<i for i in range(n)) for j in range(n)])
    d=len(columns)
    U=transpose(columns,n)
    chosen=[];rows=[]
    for i,row in enumerate(U):
        if len(independent(rows+[row]))>len(rows):chosen.append(i);rows.append(row)
    assert len(chosen)==d
    inv=inverse(rows)
    minor=[sum(((C[i]>>j)&1)<<b for b,j in enumerate(chosen)) for i in chosen]
    K=matmul(matmul(inv,minor),transpose(inv,d))
    assert alternating(K)
    assert matmul(matmul(U,K),transpose(U,d))==C
    correction=sum(qvalue(K,row)<<i for i,row in enumerate(U))
    return U,K,correction


def check_walsh(C,rng):
    U,K,correction=factor_decoded(C)
    d=len(K);n=len(C)
    walsh=[sum(1-2*(qvalue(K,z)^((a&z).bit_count()&1)) for z in range(1<<d))
           for a in range(1<<d)]
    samples=range(1<<n) if n<=10 else [rng.randrange(1<<n) for _ in range(64)]
    checked=0
    for x in samples:
        z=xor(U[i] for i in bits(x))
        lhs=1-2*qvalue(C,x)
        assert lhs==1-2*(qvalue(K,z)^((correction&x).bit_count()&1))
        numerator=sum(w*(1-2*(((a&z).bit_count()^(correction&x).bit_count())&1))
                      for a,w in enumerate(walsh))
        assert numerator==(1<<d)*lhs
        checked+=1
    return U,K,correction,walsh,checked


def random_lowrank(n,r,rng,localized=False):
    while True:
        if localized and r>=4:
            U=[rng.randrange(4)|((1<<2) if i==n-2 else 0)|((1<<3) if i==n-1 else 0)
               for i in range(n)]
        else:U=[rng.randrange(1<<r) for _ in range(n)]
        if len(independent(U))==r:break
    K=[1<<(i^1) for i in range(r)]
    return matmul(matmul(U,K),transpose(U,r))


def error_graph(n,M,rng,avoid=()):
    edges=[(i,j) for i in range(n) for j in range(i) if i not in avoid and j not in avoid]
    chosen=rng.sample(edges,min(M,len(edges)))
    S=[0]*n
    for i,j in chosen:S[i]^=1<<j;S[j]^=1<<i
    return S,len(chosen)


def phase_count_check(B,record,rng):
    n=len(B);R=record['R'];E=record['E'];C=record['decoded'];S=record['residual']
    U,K,correction,walsh,checked=check_walsh(C,rng)
    d=len(K)
    P=set()
    for _ in range(n):
        P.symmetric_difference_update({sum(1<<v for v in rng.sample(range(n),min(3,n)))})
    def nonlinear(x):return sum((x&term)==term for term in P)&1
    true=sum(1-2*(qvalue(B,x)^nonlinear(x)) for x in range(1<<n))
    total=0
    for assigned in range(1<<len(E)):
        e=sum(1<<v for j,v in enumerate(E) if assigned>>j&1)
        constant=qvalue(B,e)
        cross=sum(((B[v]&e).bit_count()&1)<<j for j,v in enumerate(R))
        numerator=0
        for a,weight in enumerate(walsh):
            inner=0
            linear=correction^cross^sum(((row&a).bit_count()&1)<<j for j,row in enumerate(U))
            for x in range(1<<len(R)):
                original=e|sum(1<<v for j,v in enumerate(R) if x>>j&1)
                phase=qvalue(S,x)^nonlinear(original)^((linear&x).bit_count()&1)
                inner+=1-2*phase
            numerator+=weight*inner
        assert numerator%(1<<d)==0
        total+=(1-2*constant)*(numerator//(1<<d))
    assert total==true
    return true,checked


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',default='lowrank_sparse_audit_results.json')
    args=parser.parse_args()
    rng=random.Random(20261105)
    records=[];walsh_checks=0;count_checks=0
    for n,r,M in [(6,2,1),(8,2,2),(9,4,3),(40,2,30),(80,4,60),(100,4,80)]:
        for sample in range(4):
            localized=n>=40 and sample%2==1 and r>=4
            A=random_lowrank(n,r,rng,localized)
            S,Mactual=error_graph(n,M,rng,avoid=(n-2,n-1) if localized else ())
            B=[a^s for a,s in zip(A,S)]
            delta=max(1,math.isqrt((2*Mactual+3*r-1)//(3*r)))
            while 3*r*delta*delta<2*Mactual:delta+=1
            I,E0=witness(A,S,r,Mactual,delta)
            result=decode_candidate(B,I,E0,delta,Mactual,r)
            assert result is not None
            R=result['R']
            expected=[restrict_column(A,R,j) for j in R]
            assert result['decoded']==expected
            assert len(result['E'])<=2*Mactual//delta+3*r*delta
            _,_,correction,_,checked=check_walsh(result['decoded'],rng)
            walsh_checks+=checked
            count=None
            if n<=9:
                count,extra=phase_count_check(B,result,rng)
                walsh_checks+=extra;count_checks+=1
            records.append(dict(n=n,r=r,M=Mactual,delta=delta,initial_erased=len(E0),
                                final_erased=len(result['E']),basis_indices_erased=len(set(I)&set(result['E'])),
                                pruning_rounds=len(result['prune_steps']),
                                retained_rank=len(independent(result['decoded'])),
                                unary_correction_weight=correction.bit_count(),exact_mixed_phase_sum=count,
                                localized_rank_component=localized))
    # Explicit triangle verifies a nonzero Boolean substitution correction.
    triangle=[0b110,0b101,0b011]
    U=[[1,1],[1,0],[0,1]]
    rows=[sum(v<<i for i,v in enumerate(row)) for row in U]
    K=[0b10,0b01]
    correction=sum(qvalue(K,row)<<i for i,row in enumerate(rows))
    assert correction==1
    assert qvalue(triangle,1)==0 and qvalue(K,rows[0])==1
    # Both clean basis-column indices are erased initially; their columns remain usable.
    n=8;r=2;M=1;delta=1
    A=[0b11110000 if i<4 else 0b00001111 for i in range(n)]
    S=[0]*n;S[0]=1<<4;S[4]=1
    B=[a^s for a,s in zip(A,S)]
    I,E0=witness(A,S,r,M,delta)
    assert I==[0,4] and set(I)==E0
    result=decode_candidate(B,I,E0,delta,M,r)
    assert result is not None and result['E']==[0,4]
    value,extra=phase_count_check(B,result,rng)
    walsh_checks+=extra;count_checks+=1
    records.append(dict(n=n,r=r,M=M,delta=delta,initial_erased=len(E0),
                        final_erased=len(result['E']),basis_indices_erased=len(I),
                        pruning_rounds=0,retained_rank=2,unary_correction_weight=0,
                        exact_mixed_phase_sum=value,localized_rank_component=False,
                        family='both basis indices erased before decoding'))
    # Complete search without supplied A,S on small raw matrices.
    searches=[]
    for sample in range(4):
        if sample<3:
            n=6;r=2;M=1;delta=1
            A=random_lowrank(n,r,rng);S,_=error_graph(n,M,rng)
            B=[a^s for a,s in zip(A,S)]
        else:
            n=10;r=2;M=0;delta=1
            B=[0b1111100000 if i<5 else 0b0000011111 for i in range(n)]
        found=None;examined=0
        for isize in range(r+1):
            if found:break
            for I in itertools.combinations(range(n),isize):
                if found:break
                for esize in range(min(n,2*M//delta+r*delta)+1):
                    if found:break
                    for E0 in itertools.combinations(range(n),esize):
                        examined+=1
                        candidate=decode_candidate(B,I,set(E0),delta,M,r)
                        if candidate is not None:
                            found=candidate;break
        assert found is not None
        if sample==3:
            assert len(found['I'])==2 and not found['E']
        value,extra=phase_count_check(B,found,rng)
        walsh_checks+=extra;count_checks+=1
        searches.append(dict(n=n,candidates_examined=examined,initial_I=found['I'],
                             initial_E0=found['E0'],final_erased=found['E'],exact_mixed_phase_sum=value))
    out=dict(status='all exact assertions passed',
             scope='finite structural/Fourier audit; exhaustive small phase sums, not the asymptotic counter',
             hidden_witness_fixtures=len(records),unknown_decomposition_searches=len(searches),
             exact_mixed_phase_counts=count_checks,walsh_identity_checks=walsh_checks,
             strict_rank_drop_prunings=sum(x['pruning_rounds'] for x in records),
             fixtures_with_erased_basis_indices=sum(x['basis_indices_erased']>0 for x in records),
             explicit_triangle_correction=correction,records=records,searches=searches)
    Path(args.output).write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ('records','searches')},indent=2))


if __name__=='__main__':main()
