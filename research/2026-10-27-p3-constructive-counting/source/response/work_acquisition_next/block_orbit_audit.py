#!/usr/bin/env python3
"""Independent checks of root's GL-orbit block-row compiler.

This is a finite validator, not the asymptotic replacement-form engine.
"""
from itertools import product, combinations
from pathlib import Path
import json
import random
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'work_mixed_root'))
from mixed_quadratic_compiler import independent, multiply, transpose, inverse, quadratic
from diagonal_completion_compiler import symmetric, off_diagonal


def rank(rows):
    return len(independent(rows))


def gl(b):
    return [list(x) for x in product(range(1<<b),repeat=b) if rank(x)==b]


def blocks(B,b):
    s=len(B)//b
    return [[[ (B[b*a+i]>>(b*z))&((1<<b)-1) for i in range(b)]
             for z in range(s)] for a in range(s)]


def diag(G,b):
    return [row<<(a*b) for a,g in enumerate(G) for row in g]


def transform(B,G):
    return multiply(multiply(G,B),transpose(G,len(G)))


def profile_distance(X,Y,group):
    best=None
    for G in group:
        cost=sum(rank([a^z for a,z in zip(multiply(G,x),y)]) for x,y in zip(X,Y))
        if best is None or cost<best[0]:
            best=(cost,G)
    return best


def acquire(B,b,c,group):
    n=len(B); s=n//b
    profiles=blocks(B,b)
    comparisons=[[profile_distance(x,y,group) for y in profiles] for x in profiles]
    distances=[[a[0] for a in row] for row in comparisons]
    assert all(distances[a][z]==distances[z][a] for a in range(s) for z in range(s))
    assert all(distances[a][z]<=distances[a][h]+distances[h][z]
               for a in range(s) for z in range(s) for h in range(s))
    F=list(range(c))
    def objective(F):
        return sum(min(distances[a][f] for f in F) for a in range(s))
    history=[objective(F)]
    while True:
        improvement=None
        for old in F:
            for new in range(s):
                if new in F:
                    continue
                candidate=sorted([f for f in F if f!=old]+[new])
                cost=objective(candidate)
                if cost<history[-1] and (improvement is None or cost<improvement[0]):
                    improvement=(cost,candidate)
        if improvement is None:
            break
        value,F=improvement
        history.append(value)
    optimum=min(objective(list(O)) for O in combinations(range(s),c))
    assert history[-1]<=5*optimum
    assignment=[min(F,key=lambda f:(distances[a][f],f)) for a in range(s)]
    localG=[comparisons[a][assignment[a]][1] for a in range(s)]
    G=diag(localG,b)
    transformed=transform(B,G)
    GT=transpose(G,n)
    # The model uses the RAW facility row, right-multiplied by G^T.
    X=[]
    for a in range(s):
        f=assignment[a]
        X.extend(multiply(B[b*f:b*(f+1)],GT))
    A=sum((a^z).bit_count() for a,z in zip(transformed,X))
    assert A<=b*b*history[-1]
    distinct=sorted(set(assignment))
    classes=[[b*a+i for a in range(s) if assignment[a]==f] for f in distinct for i in range(b)]
    C=[0]*n
    for p,I in enumerate(classes):
        for J in classes[p:]:
            ones=sum((transformed[i]>>j)&1 for i in I for j in J)
            bit=int(2*ones>len(I)*len(J))
            if bit:
                for i in I: C[i]|=sum(1<<j for j in J)
                for j in J: C[j]|=sum(1<<i for i in I)
    E=sum((a^z).bit_count() for a,z in zip(transformed,C))
    assert symmetric(C) and E<=3*A and rank(C)<=b*c
    residual=[a^z for a,z in zip(transformed,off_diagonal(C))]
    edges=sum(row.bit_count() for row in residual)//2
    assert 2*edges<=3*A
    return dict(G=G,C=C,Bprime=transformed,X=X,classes=classes,
                kappa=history[-1],metric_optimum=optimum,hamming_model_cost=A,
                directed_majority_error=E,residual_edges=edges,rank=rank(C),
                objective_history=history)


def run():
    rng=random.Random(2710202651)
    records=[]; pointwise=0; refinement=0
    for b,s,c,M in [(2,3,2,0),(2,4,2,1),(2,5,3,2),(3,3,2,0),(3,4,2,2),(3,6,3,5)]:
        group=gl(b); n=b*s
        labels=[a%c for a in range(s)]
        rng.shuffle(labels)
        H=[0]*(b*c)
        for i in range(b*c):
            for j in range(i+1):
                bit=rng.randrange(2)
                H[i]|=bit<<j; H[j]|=bit<<i
        canonical=[sum(((H[b*labels[a]+i]>>(b*labels[z]+j))&1)<<(b*z+j)
                       for z in range(s) for j in range(b)) for a in range(s) for i in range(b)]
        hiddenG=diag([rng.choice(group) for _ in range(s)],b)
        D=transform(canonical,hiddenG)
        assert rank(D)<=b*c
        B=off_diagonal(D)
        # All diagonal blocks are arbitrary and unknown, not merely scalar diagonal.
        for a in range(s):
            for i in range(b):
                for j in range(i):
                    if rng.randrange(2):
                        u,v=b*a+i,b*a+j
                        B[u]^=1<<v; B[v]^=1<<u
        corrupted=rng.sample(list(combinations(range(s),2)),M)
        for a,z in corrupted:
            for i in range(b):
                for j in range(b):
                    if rng.randrange(2):
                        u,v=b*a+i,b*z+j
                        B[u]^=1<<v; B[v]^=1<<u
        DB,BB=blocks(D,b),blocks(B,b)
        T=sum(rank([x^y for x,y in zip(DB[a][z],BB[a][z])])
              for a in range(s) for z in range(s))
        assert T<=2*b*M+n
        got=acquire(B,b,c,group)
        assert got['metric_optimum']<=2*T
        assert got['kappa']<=10*T
        assert 2*got['residual_edges']<=30*b*b*T
        # Independently verify the congruence-induced unary correction pointwise.
        G=got['G']; Bp=got['Bprime']
        ell=sum(quadratic(row,B)<<j for j,row in enumerate(G))
        if n<=12:
            for y in range(1<<n):
                x=0
                for j in range(n):
                    if y>>j&1: x^=G[j]
                assert quadratic(x,B)==(quadratic(y,Bp)^((ell&y).bit_count()%2))
                pointwise+=1
            # Cubic foreground remains block-local under the acquired GL gauges.
            def local(x):
                return sum(all((x>>(a*b+j))&1 for j in range(min(3,b)))
                           for a in range(s))%2
            direct=sum((-1)**(quadratic(x,B)^local(x)) for x in range(1<<n))
            pulled=0
            for y in range(1<<n):
                x=0
                for j in range(n):
                    if y>>j&1: x^=G[j]
                exponent=quadratic(y,Bp)^((ell&y).bit_count()%2)^local(x)
                pulled+=(-1)**exponent
            assert direct==pulled
            refinement+=1
        records.append(dict(b=b,blocks=s,n=n,hidden_types=c,corrupted_block_pairs=M,
                            orbit_group_size=len(group),hidden_rank=rank(D),
                            rank_metric_error=T,kappa=got['kappa'],
                            hamming_model_cost=got['hamming_model_cost'],
                            directed_majority_error=got['directed_majority_error'],
                            acquired_rank=got['rank'],residual_edges=got['residual_edges'],
                            swaps=len(got['objective_history'])-1))
    # Exhaustive scalar-block 3A rounding bound for every binary matrix up to 3x3
    # and all row-/column-constant approximants, independent of symmetry.
    rounding=0
    for a,b in [(1,3),(2,2),(2,3),(3,3)]:
        for mask in range(1<<(a*b)):
            ones=mask.bit_count(); majority_cost=min(ones,a*b-ones)
            for u in range(1<<a):
                for v in range(1<<b):
                    row=sum(((mask>>(i*b+j))&1)!=((u>>i)&1) for i in range(a) for j in range(b))
                    col=sum(((mask>>(i*b+j))&1)!=((v>>j)&1) for i in range(a) for j in range(b))
                    assert majority_cost<=2*row+col
                    assert majority_cost<=row+2*col
                    rounding+=1
    return dict(status='all exact assertions passed',fixtures=records,
                congruence_pointwise_checks=pointwise,mixed_phase_checks=refinement,
                rounding_inequalities_checked=rounding,
                scope='Independent finite audit of the root GL-orbit block-row extension; no speed claim.')


if __name__=='__main__':
    result=run()
    Path(__file__).with_name('block_orbit_audit_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))
