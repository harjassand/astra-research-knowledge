#!/usr/bin/env python3
"""Finite sparse-label diagnostics, NOT a truncation proof of infinite dimension."""
from pathlib import Path
from hashlib import sha256
from itertools import product
import json
import sympy as s
HERE=Path(__file__).resolve().parent
I=s.eye(2);X=s.Matrix([[0,1],[1,0]]);Y=s.Matrix([[0,-s.I],[s.I,0]]);Z=s.diag(1,-1)
zero=(I+Z)/2;plus=(I+X)/2;U=s.diag(1,1,1,-1)
Fs=[I,zero/3];H=s.Matrix([[1,s.Rational(1,6)],[s.Rational(1,6),s.Rational(1,18)]]);Hi=H.inv()
assert sum(abs(x) for x in Hi)==50
states=[(I+sign*P)/2 for P in [X,Y,Z] for sign in [1,-1]]
effects=[R/3 for R in states]
def clean(A):return A.applyfunc(s.expand)
def tr(A):return s.expand(s.trace(A))
def ptr(F,A):
    n=A.rows//2
    return clean(sum((F[b,a]*A[a*n:(a+1)*n,b*n:(b+1)*n]
                     for a,b in product(range(2),repeat=2)),s.zeros(n)))
def en(A):return sum(abs(s.re(z))+abs(s.im(z)) for z in A)
def aggregate(blocks):
    dim=next(iter(blocks.values())).rows
    return clean(sum((A for (n,m),A in blocks.items() if n==m),s.zeros(dim)))
def endpoint(blocks):return ptr(I,aggregate(blocks))
def extract(blocks):
    a=aggregate(blocks);ys=[ptr(F,a) for F in Fs]
    return [clean(sum((Hi[j,i]*ys[i] for i in range(2)),s.zeros(ys[0].rows))) for j in range(2)]
def lift(xs):return {(0,0):s.kronecker_product(plus,xs[0]),(1,1):s.kronecker_product(zero/6,xs[1])}
def subtract(a,b):
    dim=next(iter(a.values())).rows;keys=set(a)|set(b)
    return {k:clean(a.get(k,s.zeros(dim))-b.get(k,s.zeros(dim))) for k in keys}
def port(blocks):
    dim=next(iter(blocks.values())).rows;W=s.kronecker_product(U,s.eye(dim//4))
    return {(n+1,m+1):clean(W*A*W) for (n,m),A in blocks.items()}
def caller(blocks,L):
    dim=next(iter(blocks.values())).rows;W=s.kronecker_product(I,L,s.eye(dim//4))
    return {k:clean(W*A*W.conjugate().T) for k,A in blocks.items()}
def induce(A,rho,E):
    W=U*s.kronecker_product(A,rho)*U
    return clean(s.Matrix([[sum(E[d,b]*W[2*m+b,2*n+d] for b,d in product(range(2),repeat=2))
                           for n in range(2)] for m in range(2)]))
# A legal causal-break branch is the identity /3 on pointer memory. This propagates
# full pointer reachability from sector 1 into every later sector, without a cutoff.
for A in [I,X,Y,Z]:assert induce(A,zero,zero/3)==A/3
reached=[plus]+[induce(plus,rho,E) for rho,E in product(states,effects)]
assert s.Matrix.hstack(*[s.Matrix(list(A)) for A in reached[1:]]).rank()==4

# Same raw core is reproduced at arbitrary finite labels. Labels are sparse integers,
# not indexes into a truncated environmental matrix.
labels=[0,1,7,10**3,10**9]
raw_core_checks=0
for n in labels:
    prefixes=[{(n,n):plus},{(n+1,n+1):zero/6}]
    table=s.Matrix([[tr(F*aggregate(T)) for T in prefixes] for F in Fs])
    assert table==H;raw_core_checks+=1

bell=s.Matrix([1,0,0,1]);Bell=bell*bell.T/2
Q=s.Matrix([[s.Rational(3,5),-4*s.I/5],[s.Rational(4,5),3*s.I/5]])
assert Q.conjugate().T*Q==I
endpoint_equalities=0;kernel_checks=0;prefix_bound_checks=0
for label in labels:
    source={(label,label):s.kronecker_product(plus,Bell)}
    finite=s.kronecker_product(plus,Bell)
    for depth in range(7):
        assert list(source)==[(label+depth,label+depth)]
        assert endpoint(source)==ptr(I,finite);endpoint_equalities+=1
        xs=extract(source)
        assert sum(en(a) for a in xs)<=50
        assert tr(aggregate(source))==1;prefix_bound_checks+=1
        invisible=subtract(source,lift(xs))
        assert extract(invisible)==[s.zeros(4),s.zeros(4)]
        assert endpoint(invisible)==s.zeros(4)
        # Invisible counter-sector/section errors survive a full coherent continuation.
        continued=port(caller(port(invisible),Q))
        assert endpoint(continued)==s.zeros(4);kernel_checks+=1
        source=port(caller(source,Q))
        QQ=s.kronecker_product(I,Q,I);UU=s.kronecker_product(U,I)
        finite=clean(UU*QQ*finite*QQ.conjugate().T*UU)

# Reachable invisible generators across distinct counter sectors and pointer coherences.
generator_checks=0
for n,m in [(1,2),(7,1000),(1000,10**9)]:
    for P in [I,X,Y,Z]:
        bad={(n,n):s.kronecker_product(P,Bell),(m,m):-s.kronecker_product(P,Bell)}
        assert extract(bad)==[s.zeros(4),s.zeros(4)]
        assert endpoint(port(caller(port(bad),Q)))==s.zeros(4);generator_checks+=1
for n,P in product([1,7,10**9],[X,Y]):
    bad={(n,n):s.kronecker_product(P,Bell)}
    assert extract(bad)==[s.zeros(4),s.zeros(4)]
    assert endpoint(port(caller(port(bad),Q)))==s.zeros(4);generator_checks+=1

out={'status':'PASS exact sparse-label finite diagnostics; analytic infinite proof remains separate',
 'source_sha256':sha256((HERE/'TRACE_CLASS_COMPLETE_QUOTIENT_EXTENSION.md').read_bytes()).hexdigest(),
 'script_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
 'counter_representation':'sparse finite-support integer-labelled blocks; no truncated environmental matrix',
 'counter_labels_tested':labels,'raw_core_counter_independence_checks':raw_core_checks,
 'exact_finite_pointer_endpoint_equalities':endpoint_equalities,
 'complete_invisible_section_continuation_checks':kernel_checks,
 'complete_prefix_bound_checks':prefix_bound_checks,'reachable_invisible_generator_checks':generator_checks,
 'one_step_pointer_reachable_dimension':4,'observable_core_rank':2,'K_core':50,
 'infinite_reachable_dimension_inferred_from_tests':False,
 'infinite_reachable_dimension_proof':'analytic pairwise orthogonal nonzero counter-sector states at every depth',
 'normality_CP_TP_reason':'analytic bounded isometry W with W*W=I; not a finite numeric inference',
 'finite_physical_realization_claim':'explicit pointer realization for this witness only; no general existence claim',
 'source_calls':0,'episode_starts':0,'RNG_calls':0,'hardware_executions':0,
 'generic_fit_or_QE_executed':False,'decoder_or_compiler_executed':False,'floating_point_used':False}
(HERE/'trace_class_quotient_sparse_check.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
