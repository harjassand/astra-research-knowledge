#!/usr/bin/env python3
"""Compile a graph into a distinct diagonal spectrum and decode an exact count.

This is a representation compiler and readout, not a counting oracle.
The target source is Tr(tr(XYZ)+e2(X)+tr(DX^2)) on full square matrices.
An independently supplied exact target gap/count recovers the even Hamming
coefficients of the graph's quadratic Boolean phase.
"""
from functools import lru_cache
from math import comb
from norm_slice_compiler import deterministic_field,trace_powers,trace_mask
from field_kloosterman import gf_mul
from field_descent import span,bits,linear_apply
from exponential_pfaffian_kernel import exponential_kernel,involution_numbers


def _trim(coefficients):
    out=list(coefficients)
    while len(out)>1 and not out[-1]:out.pop()
    return tuple(out)


@lru_cache(None)
def moment_polynomials(m):
    if type(m) is not int or m<1:raise ValueError('positive explicit graph size required')
    _,meta=exponential_kernel(m,2)
    polynomials=tuple(_trim(p) for p in meta['formal_q_polynomials'])
    if tuple(p[0] for p in polynomials)!=tuple((-1)**c*v for c,v in enumerate(involution_numbers(m))):
        raise AssertionError('signed involution constant identity failed')
    return polynomials


@lru_cache(None)
def trace_symplectic_pairs(field_degree,pair_count):
    """Deterministically acquire hyperbolic pairs in ker Tr modulo F2*1."""
    a=field_degree
    if type(a) is not int or a<2 or a&(a-1) or not 0<=2*pair_count<=a-2:
        raise ValueError('power-of-two even degree with enough quotient dimension required')
    h=deterministic_field(a);tm=trace_mask(h)
    if tm&1 or not tm:raise AssertionError('wrong trace radical for an even-degree field')
    powers=trace_powers(h,2*a-2)
    gram=tuple(sum(powers[i+j]<<i for i in range(a)) for j in range(a))
    pivot=(tm&-tm).bit_length()-1
    # Constant one is a radical basis vector; omit it to choose a complement.
    remaining=[(1<<j)^(((tm>>j)&1)<<pivot) for j in range(1,a) if j!=pivot]
    es=[];fs=[]
    for _ in range(pair_count):
        e=remaining[0];ef=linear_apply(gram,e)
        index=next((j for j in range(1,len(remaining)) if (ef&remaining[j]).bit_count()&1),None)
        if index is None:raise AssertionError('trace-zero quotient lost nondegeneracy')
        f=remaining[index];ff=linear_apply(gram,f)
        remaining=[w^(e if (ff&w).bit_count()&1 else 0)^
            (f if (ef&w).bit_count()&1 else 0)
            for j,w in enumerate(remaining) if j not in (0,index)]
        es.append(e);fs.append(f)
    if len(span([1]+es+fs))!=1+2*pair_count:raise AssertionError('manufactured quotient basis is dependent')
    for i in range(pair_count):
        for j in range(pair_count):
            for left,right,wanted in ((es[i],es[j],0),(fs[i],fs[j],0),(es[i],fs[j],int(i==j))):
                if ((linear_apply(gram,left)&right).bit_count()&1)!=wanted:
                    raise AssertionError('hyperbolic trace pairing certificate failed')
    return h,tm,gram,tuple(es),tuple(fs)


def compile_diagonal_graph(adjacency,minimum_field_degree=0):
    """Return an explicit target query and exact readout data, without counting."""
    A=[list(row) for row in adjacency];m=len(A)
    if m<1 or any(len(row)!=m for row in A) or any(v not in (0,1) for row in A for v in row):
        raise ValueError('explicit nonempty binary adjacency matrix required')
    if any(A[i][i] or any(A[i][j]!=A[j][i] for j in range(i)) for i in range(m)):
        raise ValueError('symmetric zero-diagonal adjacency required')
    if type(minimum_field_degree) is not int or minimum_field_degree<0:
        raise ValueError('nonnegative field-degree lower bound required')
    moments=moment_polynomials(m)
    coefficient_bound=sum(comb(m,b)*max(abs(c) for c in moments[m-b]) for b in range(0,m+1,2))
    required=max(2*m+2,(2*coefficient_bound).bit_length(),minimum_field_degree)
    a=1<<(required-1).bit_length();q=1<<a
    h,tm,gram,es,fs=trace_symplectic_pairs(a,m)
    eigenvalues=[]
    for i in range(m):
        value=es[i]
        for j in range(i):
            if A[i][j]:value^=fs[j]
        eigenvalues.append(value)
    if len(span([1]+eigenvalues))!=m+1:raise AssertionError('spectrum is not independent modulo one')
    for i,x in enumerate(eigenvalues):
        if (tm&x).bit_count()&1:raise AssertionError('eigenvalue has nonzero absolute trace')
        for j,y in enumerate(eigenvalues):
            if ((tm&gf_mul(x,y,h)).bit_count()&1)!=A[i][j]:
                raise AssertionError('spectrum Gram matrix does not equal source graph')
    degree=max(len(moments[m-b])-1+b//2 for b in range(0,m+1,2))
    return dict(matrix_size=m,field_degree=a,field_modulus=h,eigenvalues=eigenvalues,
        beta=1,eta=0,trace_polynomial=[],original_bits=3*a*m*m,
        source='Tr(tr(XYZ)+e2(X)+tr(DX^2)), D=diag(eigenvalues)',
        normalization_q_exponent=m*m+m*(m-1)//2,
        normalized_polynomial_degree=degree,coefficient_bound=coefficient_bound,
        moment_polynomials=[list(p) for p in moments],
        trace_mask=tm,graph_adjacency=A,
        certified_trace_zero=True,certified_independent_modulo_one=True,
        target_count_computed=False)


def decode_even_hamming(query,*,gap=None,ones=None):
    """Read a supplied exact target count; this function never computes it."""
    if (gap is None)==(ones is None):raise ValueError('supply exactly one exact target gap or satisfying count')
    n=query['original_bits'];m=query['matrix_size'];a=query['field_degree'];q=1<<a
    if ones is not None:
        if type(ones) is not int or not 0<=ones<=1<<n:raise ValueError('invalid target satisfying count')
        gap=(1<<n)-2*ones
    if type(gap) is not int or abs(gap)>1<<n or gap%2:
        raise ValueError('invalid full-domain signed count')
    normalized,remainder=divmod(gap,q**query['normalization_q_exponent'])
    if remainder:raise ValueError('target gap lacks the proved normalization divisor')
    if q<=2*query['coefficient_bound']:raise ValueError('field is too small for unique balanced digits')
    coefficients=[];value=normalized
    for _ in range(query['normalized_polynomial_degree']+1):
        digit=value%q
        if 2*digit>q:digit-=q
        if abs(digit)>query['coefficient_bound']:raise ValueError('normalized coefficient exceeds its certified bound')
        coefficients.append(digit);value=(value-digit)//q
    if value:raise ValueError('normalized polynomial has excessive degree')
    moments=query['moment_polynomials'];answer={}
    for j in range(m//2+1):
        b=2*j;value=coefficients[j]
        for earlier in range(j):
            p=moments[m-2*earlier];index=j-earlier
            if index<len(p):value-=answer[2*earlier]*p[index]
        quotient,remainder=divmod(value,moments[m-b][0])
        if remainder:raise ValueError('nonintegral triangular Hamming reconstruction')
        if abs(quotient)>comb(m,b) or (quotient-comb(m,b))%2:
            raise ValueError('reconstructed Hamming coefficient is outside its exact range')
        answer[b]=quotient
    check=[0]*len(coefficients)
    for b,W in answer.items():
        for j,c in enumerate(moments[m-b]):check[j+b//2]+=W*c
    if check!=coefficients or answer[0]!=1:
        raise ValueError('supplied count fails the full normalized polynomial identity')
    return answer,dict(normalized_polynomial_coefficients=coefficients,
        normalized_value=normalized,exact_balanced_digits=True,
        exact_triangular_divisions=True,target_count_computed=False)


def recover_all_hamming(m,original_even,isolated_vertex_even):
    """Combine two even spectra using F_(G plus isolated vertex)=(1+z)F_G."""
    answer=[]
    for b in range(m+1):
        value=original_even[b] if b%2==0 else isolated_vertex_even[b+1]-original_even.get(b+1,0)
        if abs(value)>comb(m,b) or (value-comb(m,b))%2:raise ValueError('inconsistent isolated-vertex spectra')
        answer.append(value)
    if answer[0]!=1:raise ValueError('invalid empty-set coefficient')
    return answer
