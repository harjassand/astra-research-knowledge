#!/usr/bin/env python3
"""Acquire a bounded-Frobenius-width field base and an unknown quadratic defect.

Implements acquisition and exact representation. General field point counting
is the established Lauder--Wan theoretical evaluator, not implemented here.
The specialized complete counter is field_rank_decoder.py.
"""
from field_rank_decoder import *


def quadratic_trace_representative(certificates,h,b,bandwidth):
    """Integrate a certified alternating block matrix without a degree search."""
    d=h.bit_length()-1; result={}
    def add(exponent,coefficient):
        key=tuple(exponent); result[key]=result.get(key,0)^coefficient
    for cert in certificates:
        i,j=cert['row_block'],cert['column_block']; cs=cert['decoded_coefficients']
        if i>j: continue
        if i==j:
            if cs[bandwidth]: raise ValueError('nonalternating diagonal coefficient')
            for t in range(1,bandwidth+1):
                if cs[bandwidth-t]!=gf_pow(cs[bandwidth+t],1<<(d-t),h):
                    raise ValueError('diagonal Frobenius coefficients not adjoints')
                e=[0]*b; e[i]=1+(1<<t); add(e,cs[bandwidth+t])
        else:
            for index,coefficient in enumerate(cs):
                t=index-bandwidth; e=[0]*b
                if t>=0: e[i]=1; e[j]=1<<t
                else:
                    e[i]=1<<(-t); e[j]=1
                    coefficient=gf_pow(coefficient,1<<(-t),h)
                add(e,coefficient)
    return {e:c for e,c in result.items() if c}


def acquire_trace_form(poly,n,*,bandwidth=1):
    """Raw Boolean cubic -> field polynomial + canonical binary quadratic.

    A successful output is an exact identity. The radius guarantees recovery
    of a promised base; outside it this algorithm may reject. No original field
    presentation, coordinates, error or polynomial coefficients are inputs.
    """
    if not isinstance(n,int) or n<1 or any(not isinstance(x,int) or x<0 or x>>n or x.bit_count()>3 for x in poly):
        raise ValueError('input must be an explicit Boolean cubic ANF')
    start=time.perf_counter(); algebra,pair,trail=centroid(poly,n)
    h,columns,module_basis=acquire_field(algebra,n)
    d=h.bit_length()-1; b=len(module_basis); gram=trace_gram(h)
    B=quadratic_matrix(poly,n,columns)
    base,defect,certificates=acquire_quadratic_base(B,h,bandwidth)
    result=quadratic_trace_representative(certificates,h,b,bandwidth)
    for i,j,k in itertools.combinations(range(b),3):
        functional=sum(tensor_value(pair,columns[i*d+t],columns[j*d],columns[k*d])<<t for t in range(d))
        coefficient=solve(gram,functional); assert coefficient is not None
        e=[0]*b; e[i]=e[j]=e[k]=1
        if coefficient: result[tuple(e)]=coefficient
    constant=polynomial_value(poly,0)
    for i in range(b):
        target=0
        for t in range(d):
            x=[0]*b; x[i]=1<<t
            discrepancy=polynomial_value(poly,columns[i*d+t])^constant^gf_trace(field_polynomial_value(result,x,h),h)
            target|=discrepancy<<t
        coefficient=solve(gram,target); assert coefficient is not None
        if coefficient:
            e=tuple(int(j==i) for j in range(b)); result[e]=result.get(e,0)^coefficient
    if constant: result[(0,)*b]=next(1<<i for i in range(d) if gf_trace(1<<i,h))
    factors,linear=symplectic_factors(defect)
    return dict(original_variables=n,raw_polynomial=sorted(poly),field_modulus=h,
        field_extension_degree=d,module_dimension=b,frobenius_bandwidth=bandwidth,
        certified_field_degree=max(3,(1<<bandwidth)+1),centroid_dimension=len(algebra),
        centroid_kernel_dimensions=trail,coordinate_columns=columns,quadratic_matrix=B,
        acquired_field_quadratic=base,acquired_defect=defect,acquired_defect_rank=len(factors),
        symplectic_factors=factors,linear_correction=linear,decoding=certificates,
        field_polynomial=[dict(exponents=list(e),coefficient=c) for e,c in sorted(result.items())],
        seconds=time.perf_counter()-start)


def acquire_best_trace_form(poly,n):
    """Try every admissible bandwidth and minimize the explicit leaf-cost factor.

    The factor 2^r D^(3(b+1)) is the bandwidth-dependent part of the
    Lauder--Wan bound. This performs only polynomial-time acquisitions; it
    does not execute a generic field point counter. Centroid recomputation
    in the simple implementation adds a polynomial factor.
    """
    algebra,_,_=centroid(poly,n)
    h,_,module_basis=acquire_field(algebra,n)
    d=h.bit_length()-1; v=len(module_basis)+1
    best=None; best_score=None; trials=[]
    for bandwidth in range(1,(d-1)//2+1):
        try:
            candidate=acquire_trace_form(poly,n,bandwidth=bandwidth)
        except ValueError as error:
            trials.append(dict(bandwidth=bandwidth,accepted=False,reason=str(error)))
            continue
        score=(1<<candidate['acquired_defect_rank'])*candidate['certified_field_degree']**(3*v)
        trials.append(dict(bandwidth=bandwidth,accepted=True,
            acquired_rank=candidate['acquired_defect_rank'],degree=candidate['certified_field_degree'],
            leaf_cost_factor=score))
        if best_score is None or score<best_score: best,best_score=candidate,score
    if best is None: raise ValueError('no certified field-band decomposition')
    best['bandwidth_trials']=trials; best['leaf_cost_factor']=best_score
    return best
