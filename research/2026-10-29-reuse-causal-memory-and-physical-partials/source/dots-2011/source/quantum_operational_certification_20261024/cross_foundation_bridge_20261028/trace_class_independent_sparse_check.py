#!/usr/bin/env python3
"""Exact sparse-label diagnostics, not an infinite-dimensional proof by cutoff.
Labels are dictionary keys; no counter Hilbert-space dimension or boundary exists.
"""
from pathlib import Path
from hashlib import sha256
from itertools import product
import sympy as s
import json
P=Path(__file__).resolve().parent
I=s.eye(2);X=s.Matrix([[0,1],[1,0]]);Z=s.diag(1,-1);U=s.diag(I,X,Z)
z=s.diag(1,0);n=s.diag(0,1);plus=s.ones(2)/2;rho=s.ones(3)/3

def clean(A):return A.applyfunc(s.expand)
def trace(A):return s.expand(s.trace(A))
def fun(F,A):
    d=F.rows;k=A.rows//d
    return clean(sum((F[j,i]*A[i*k:(i+1)*k,j*k:(j+1)*k] for i,j in product(range(d),repeat=2)),s.zeros(k)))
def summat(vals,n):return clean(sum(vals,s.zeros(n)))
def aggregate(a):
    d=next(iter(a.values())).rows
    return summat([v for (i,j),v in a.items() if i==j],d)
def endpoint(a):return fun(s.eye(3),aggregate(a))
def native(a):
    d=next(iter(a.values())).rows//6;v=s.kronecker_product(U,s.eye(d))
    return {(i+1,j+1):clean(v*x*v.H) for (i,j),x in a.items()}
def local(a,L):
    r=next(iter(a.values())).rows//6;v=s.kronecker_product(s.eye(3),L,s.eye(r))
    return {k:clean(v*x*v.H) for k,x in a.items()}
def subtract(a,b):
    d=next(iter(a.values())).rows
    return {k:clean(a.get(k,s.zeros(d))-b.get(k,s.zeros(d))) for k in set(a)|set(b)}
def cb(T,r,e):
    us=[I,X,Z]
    return clean(s.Matrix([[T[i,j]*trace(e*us[i]*r*us[j].H) for j in range(3)] for i in range(3)]))
Fs=[s.eye(3),s.diag(0,s.Rational(1,4),0),s.diag(s.Rational(1,4),s.Rational(1,4),0)]
core=[(0,rho),(1,cb(rho,z,n/4)),(1,cb(rho,plus,plus/4))]
H=s.Matrix([[trace(F*T) for k,T in core] for F in Fs]);Hi=H.inv();m=H[0,:]
assert H.det()==s.Rational(1,6912)
def pi(a):
    ag=aggregate(a);ys=[fun(F,ag) for F in Fs]
    return [summat([Hi[j,i]*ys[i] for i in range(3)],ys[0].rows) for j in range(3)]
def lift(xs):
    out={}
    for (k,T),x in zip(core,xs):out[k,k]=out.get((k,k),s.zeros(3*x.rows))+s.kronecker_product(T,x)
    return {k:clean(v) for k,v in out.items()}
b=s.Matrix([1,0,0,1]);bell=b*b.H/2
Q=s.Matrix([[s.Rational(3,5),-s.Rational(4,5)],[s.Rational(4,5),s.Rational(3,5)]])
Ls=[s.diag(1,s.Rational(3,5))*Q,s.Matrix([[0,s.Rational(4,5)],[0,0]])*Q]
assert sum((L.H*L for L in Ls),s.zeros(2))==I
labels=[0,11,10**40,10**100]
complete_checks=0;kernel_checks=0;aggregate_checks=0;nonzero_sections=0
for label in labels:
    a={(label,label):s.kronecker_product(rho,bell)}
    for depth in range(1,5):
        ag=aggregate(a);v=s.kronecker_product(U,I)
        a=native(a)
        assert aggregate(a)==clean(v*ag*v.H);aggregate_checks+=1
        xx=pi(a);section=lift(xx);err=subtract(a,section)
        if any(v!=s.zeros(12) for v in err.values()):nonzero_sections+=1
        assert endpoint(err)==s.zeros(4)
        assert endpoint(a)==summat([m[j]*xx[j] for j in range(3)],4);complete_checks+=1
        for L in Ls:
            continuation=native(local(err,L))
            assert endpoint(continuation)==s.zeros(4);kernel_checks+=1
        # Composition after replacing the physical representative by the section.
        assert pi(native(local(a,Q)))==pi(native(local(section,Q)))
# Coherent counter off-diagonal blocks: a separate finite-rank Hermitian input,
# not falsely described as an actual reachable state from the product reset.
large=10**100
A=s.kronecker_product(rho,bell)
B=s.I*s.kronecker_product(s.diag(1,0,-1),bell)
insertion={(0,0):A,(large,large):-A,(0,large):B,(large,0):B.H}
assert aggregate(insertion)==s.zeros(12)
for depth in range(5):
    insertion=native(local(insertion,Q))
    assert aggregate(insertion)==s.zeros(12) and endpoint(insertion)==s.zeros(4)
# Label arithmetic has no wraparound or fixed cutoff.
assert (large+5,large+5) in insertion and (5,large+5) in insertion
# The support-separation identity for arbitrary integer n is proved analytically
# in the audit; these labelled representatives only inspect selected finite cases.
support_states=[{(k,k):rho} for k in labels]
assert all(set(a).isdisjoint(set(b)) for i,a in enumerate(support_states) for b in support_states[i+1:])
assert all(trace(aggregate(a))==1 for a in support_states)
out={
 'status':'PASS_INDEPENDENT_EXACT_SPARSE_LABEL_TRACE_CLASS_DIAGNOSTICS',
 'source_sha256':sha256((P/'TRACE_CLASS_COMPLETE_QUOTIENT_EXTENSION.md').read_bytes()).hexdigest(),
 'script_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
 'independent_code_imports_author_code':False,'finite_pointer_dimension':3,'observable_rank_in_architecture':3,
 'counter_labels':[str(x) for x in labels],'counter_cutoff_or_matrix_dimension':None,
 'complete_endpoint_checks':complete_checks,'complete_invisible_suffix_checks':kernel_checks,
 'aggregate_intertwining_checks':aggregate_checks,'nonzero_section_differences':nonzero_sections,
 'offdiagonal_counter_cancellation_steps':5,'finite_raw_core_determinant':str(H.det()),
 'infinity_proved_by_finite_tests':False,'infinite_reachable_claim_basis':'Separate analytic orthogonal-support proof for every nonnegative integer depth',
 'normality_claim_basis':'Separate analytic bounded-isometry/predual proof',
 'source_calls':0,'episode_starts':0,'random_draws':0,'sampled_outcomes':0,'hardware_executions':0,
 'generic_fit_QE_decoder_or_compiler_executed':False,'floating_point_used':False}
(P/'trace_class_independent_sparse_check.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
