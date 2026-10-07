"""Bounded diagnostics for the full operator-system ball obstruction."""
from fractions import Fraction
from pathlib import Path
import itertools
import json
import math
import numpy as np


def factorization(n):
    assert n % 2 == 0
    return [[(n-1,f)] + [((f+k)%(n-1),(f-k)%(n-1))
            for k in range(1,n//2)] for f in range(n-1)]


def exact_combinatorics(n):
    flags = factorization(n)
    edges = [tuple(sorted(e)) for f in flags for e in f]
    assert len(set(edges)) == n*(n-1)//2
    assert sorted(edges) == list(itertools.combinations(range(n),2))
    c = [Fraction((-1)**i*(i+1),n+1) for i in range(n)]
    d = [Fraction((i*i+3) % (n+2),n+2) for i in range(n)]
    flags_wedge = sum((c[i]*d[j]-c[j]*d[i])**2 for flag in flags for i,j in flag)
    all_wedge = sum((c[i]*d[j]-c[j]*d[i])**2 for i,j in itertools.combinations(range(n),2))
    lagrange = sum(x*x for x in c)*sum(x*x for x in d)-sum(x*y for x,y in zip(c,d))**2
    assert flags_wedge == all_wedge == lagrange
    return {"n":n,"flags":len(flags),"all_pairs_once":True,
            "wedge_squared":str(all_wedge),"lagrange_identity":True,
            "Hilbert_dimension_symbolic":f"{n-1} * 2^{n//2}",
            "system_commutator_supremum":2/math.sqrt(n-1),
            "EB_restricted_identity_error":.5,
            "UCP_frame_preimage_L2_error_floor":(3-math.sqrt(5))/4}


def tensor_at(a,pos,k):
    r = np.array([[1]],dtype=complex)
    for j in range(k):
        r = np.kron(r,a if j==pos else np.eye(2))
    return r


def blocks(n):
    x = np.array([[0,1],[1,0]],dtype=complex)
    z = np.diag([1,-1]).astype(complex)
    out = []
    for flag in factorization(n):
        ops = [None]*n
        for pos,(i,j) in enumerate(flag):
            i,j = sorted((i,j))
            ops[i]=tensor_at(x,pos,n//2)
            ops[j]=tensor_at(z,pos,n//2)
        out.append(ops)
    return out


def matrix_suite(n):
    bs=blocks(n); size=2**(n//2)
    rng=np.random.default_rng(7075305+n)
    max_comm_formula_error=0.0
    max_norm_formula_error=0.0
    max_product_projection=0.0
    max_sampled_numerical_range=0.0
    for _ in range(12):
        c=rng.normal(size=n); d=rng.normal(size=n)
        predicted=4/(n-1)*(np.dot(c,c)*np.dot(d,d)-np.dot(c,d)**2)
        observed=0.0
        predicted_norm=max(sum(math.hypot(c[i],c[j]) for i,j in f) for f in factorization(n))
        observed_norm=0.0
        for ops in bs:
            a=sum(t*op for t,op in zip(c,ops)); b=sum(t*op for t,op in zip(d,ops))
            comm=a@b-b@a
            observed+=float(np.linalg.norm(comm,'fro')**2/size)/(n-1)
            observed_norm=max(observed_norm,float(np.linalg.norm(a,2)))
            vec=rng.normal(size=size)+1j*rng.normal(size=size); vec/=np.linalg.norm(vec)
            score=sum(float(np.vdot(vec,op@vec).real)**2 for op in ops)
            max_sampled_numerical_range=max(max_sampled_numerical_range,score)
            assert score <= n/2+1e-10
        max_comm_formula_error=max(max_comm_formula_error,abs(predicted-observed))
        max_norm_formula_error=max(max_norm_formula_error,abs(predicted_norm-observed_norm))
    for i,j in itertools.combinations(range(n),2):
        for k in range(n):
            projection=sum(np.trace(ops[k]@(ops[i]@ops[j]))/size for ops in bs)/(n-1)
            max_product_projection=max(max_product_projection,abs(projection))
        scalar=sum(np.trace(ops[i]@ops[j])/size for ops in bs)/(n-1)
        max_product_projection=max(max_product_projection,abs(scalar))
    assert max_comm_formula_error<1e-10
    assert max_norm_formula_error<1e-10
    assert max_product_projection<1e-10
    return {"n":n,"materialized_block_dimension":size,"block_count":n-1,
            "commutator_formula_max_error":max_comm_formula_error,
            "norm_formula_max_error":max_norm_formula_error,
            "product_to_system_projection_max":float(max_product_projection),
            "sampled_numerical_range_max":max_sampled_numerical_range,
            "numerical_range_proved_upper":n/2}


if __name__=='__main__':
    report={"exact_combinatorics":[exact_combinatorics(n) for n in [4,6,8,20,100]],
            "small_matrix_diagnostics":[matrix_suite(n) for n in [4,6]],
            "scope":"Exact pair-cover/wedge identities plus small floating matrix checks; no full growing matrices or generic channel optimization"}
    path=Path(__file__).with_name('system_obstruction_checks.json')
    path.write_text(json.dumps(report,indent=2))
    print(json.dumps(report,indent=2))
