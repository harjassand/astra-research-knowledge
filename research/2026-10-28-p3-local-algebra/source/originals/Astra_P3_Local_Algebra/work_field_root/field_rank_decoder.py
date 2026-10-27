#!/usr/bin/env python3
"""Manufacture a Gabidulin decoding interface from a raw scalar cubic.

Exact acquisition of an unknown low-rank quadratic perturbation to the
hidden-field triple-product family; no perturbation or code is supplied.
Gabidulin decoding itself is established prior machinery.
"""
import json, random, time
from pathlib import Path
from field_descent import *


def field_linear_solve(rows,rhs,h):
    if not rows: return []
    width=len(rows[0]); a=[list(row)+[b] for row,b in zip(rows,rhs)]
    pivots=[]; at=0; q=1<<(h.bit_length()-1)
    for j in range(width):
        pivot=next((i for i in range(at,len(a)) if a[i][j]),None)
        if pivot is None: continue
        a[at],a[pivot]=a[pivot],a[at]
        inv=gf_pow(a[at][j],q-2,h); a[at]=[gf_mul(c,inv,h) for c in a[at]]
        for i in range(len(a)):
            if i!=at and a[i][j]:
                c=a[i][j]; a[i]=[x^gf_mul(c,y,h) for x,y in zip(a[i],a[at])]
        pivots.append(j); at+=1
    if any(not any(row[:-1]) and row[-1] for row in a): return None
    out=[0]*width
    for i,j in enumerate(pivots): out[j]=a[i][-1]
    return out


def linearized_value(coefficients,x,h):
    out=0
    for c in coefficients:
        out^=gf_mul(c,x,h); x=gf_mul(x,x,h)
    return out


def decode_gabidulin(received,h,k=3):
    """Length d full-basis code, monic error span, right composition division."""
    d=h.bit_length()-1; t=(d-k)//2
    if not isinstance(k,int) or k<1 or t<0 or len(received)!=d:
        raise ValueError('invalid Gabidulin parameters')
    rows=[]; rhs=[]
    for j,y in enumerate(received):
        g=1<<j; powers_g=[]; powers_y=[]
        for _ in range(k+t): powers_g.append(g); g=gf_mul(g,g,h)
        for _ in range(t): powers_y.append(y); y=gf_mul(y,y,h)
        rows.append(powers_g+powers_y); rhs.append(y)
    solution=field_linear_solve(rows,rhs,h)
    if solution is None: raise ValueError('no bounded-rank field lift')
    numerator=solution[:k+t]; locator=solution[k+t:]+[1]
    remainder=numerator[:]; decoded=[0]*k
    for s in range(k-1,-1,-1):
        lead=remainder[s+t]
        coefficient=gf_pow(lead,1<<(d-t),h)
        decoded[s]=coefficient
        power=coefficient
        for j,e in enumerate(locator):
            remainder[s+j]^=gf_mul(e,power,h); power=gf_mul(power,power,h)
    if any(remainder): raise ValueError('linearized quotient has nonzero remainder')
    errors=[y^linearized_value(decoded,1<<j,h) for j,y in enumerate(received)]
    distance=len(span(errors))
    if distance>t: raise ValueError('outside unique rank-decoding radius')
    return decoded,dict(radius=t,error_rank=distance,locator=locator,
                        interpolation_numerator=numerator,decoded_coefficients=decoded)


def quadratic_matrix(poly,n,columns):
    constant=polynomial_value(poly,0)
    singles=[polynomial_value(poly,x)^constant for x in columns]
    B=[0]*n
    for i in range(n):
        for j in range(i+1,n):
            value=polynomial_value(poly,columns[i]^columns[j])^constant^singles[i]^singles[j]
            if value: B[i]^=1<<j; B[j]^=1<<i
    return B


def quadratic_vector(B):
    out=0; k=0
    for i in range(len(B)):
        for j in range(i+1,len(B)):
            out|=((B[i]>>j)&1)<<k; k+=1
    return out


def acquire_quadratic_base(B,h,bandwidth=1):
    d=h.bit_length()-1; n=len(B); b=n//d
    if not isinstance(bandwidth,int) or bandwidth<0 or 2*bandwidth>=d:
        raise ValueError('requires nonoverlapping Frobenius bandwidth')
    if b*d!=n: raise ValueError('incomplete field blocks')
    gram=trace_gram(h); base=[0]*n; certificates=[]
    for i in range(b):
        for j in range(b):
            map_columns=[]
            for col in range(d):
                functional=sum(((B[i*d+row]>>(j*d+col))&1)<<row for row in range(d))
                value=solve(gram,functional); assert value is not None
                map_columns.append(value)
            received=[linear_apply(map_columns,gf_pow(1<<col,1<<bandwidth,h)) for col in range(d)]
            decoded,cert=decode_gabidulin(received,h,k=2*bandwidth+1)
            for col in range(d):
                inv_frob=gf_pow(1<<col,1<<(d-bandwidth),h)
                image=linearized_value(decoded,inv_frob,h)
                functional=linear_apply(gram,image)
                for row in bits(functional): base[i*d+row]^=1<<(j*d+col)
            cert.update(row_block=i,column_block=j,frobenius_bandwidth=bandwidth)
            certificates.append(cert)
    if any(base[i]>>i&1 for i in range(n)) or any(((base[i]>>j)^(base[j]>>i))&1 for i in range(n) for j in range(i)):
        raise ValueError('decoded field quadratic is not alternating')
    defect=[x^y for x,y in zip(B,base)]
    return base,defect,certificates


def quadratic_value(B,x):
    return xor_all((B[i]&x&~((1<<(i+1))-1)).bit_count()&1 for i in bits(x))


def symplectic_factors(B):
    rows=B[:]; n=len(B); active=(1<<n)-1; factors=[]; linear=0
    while any(rows):
        i=next(i for i,row in enumerate(rows) if row)
        j=next(bits(rows[i])); remaining=active^(1<<i)^(1<<j)
        a=rows[i]&remaining; b=rows[j]&remaining
        factors.extend([(1<<i)^b,(1<<j)^a]); linear^=a&b
        updated=[0]*n
        for v in bits(remaining): updated[v]=(rows[v]&remaining)^(b if a>>v&1 else 0)^(a if b>>v&1 else 0)
        rows=updated; active=remaining
    assert len(factors)==len(span(B))
    return factors,linear


def shift_balanced(poly,parity_mask,h,field_columns):
    d=h.bit_length()-1; gram=trace_gram(h)
    old=[solve(gram,(parity_mask>>(d*i))&((1<<d)-1)) for i in range(3)]
    out=poly.copy()
    for j in range(3):
        coefficient=xor_all(gf_mul(old[i],field_columns[j][i],h) for i in range(3))
        e=tuple(int(i==j) for i in range(3)); out[e]=out.get(e,0)^coefficient
    return {e:c for e,c in out.items() if c}


def compile_rank_perturbed(poly,n,*,retain_leaf_data=False):
    """Acquire and count; stream leaves by default to retain polynomial space.

    ``retain_leaf_data=True`` is a finite-experiment diagnostic and uses
    exponential space in the acquired defect rank. It is not needed to count.
    """
    if not isinstance(n,int) or n<9 or n%3:
        raise ValueError('requires 3d variables with d at least three')
    if any(not isinstance(term,int) or term<0 or term>>n or term.bit_count()>3 for term in poly):
        raise ValueError('input must be a Boolean ANF of degree at most three')
    start=time.perf_counter(); algebra,pair,trail=centroid(poly,n)
    h,columns,module_basis=acquire_field(algebra,n)
    if len(module_basis)!=3: raise ValueError('requires three field coordinates')
    B=quadratic_matrix(poly,n,columns)
    base,defect,decoding=acquire_quadratic_base(B,h)
    fieldpoly,fit=field_cubic_fit(poly,n,columns,pair,h,quadratic_override=quadratic_vector(base))
    balanced,field_columns,factorization=factor_cubic(fieldpoly,h)
    factors,linear=symplectic_factors(defect); r=len(factors)
    numerator=0; leaves=[]
    for selector in range(1<<r):
        parity_mask=linear^linear_apply(factors,selector)
        sign=(-1)**sum(((selector>>(2*j))&3)==3 for j in range(r//2))
        shifted=shift_balanced(balanced,parity_mask,h,field_columns)
        value,certificate=count_balanced(shifted,h)
        numerator+=sign*value
        if retain_leaf_data:
            leaves.append(dict(selector=selector,sign=sign,parity_mask=parity_mask,count=value,certificate=certificate))
    denominator=1<<(r//2)
    assert numerator%denominator==0
    signed=numerator//denominator
    return dict(original_variables=n,raw_anf_terms=len(poly),raw_cubic_terms=sum(x.bit_count()==3 for x in poly),
        field_extension_degree=h.bit_length()-1,module_dimension=3,field_modulus=h,centroid_dimension=len(algebra),
        centroid_kernel_dimensions=trail,coordinate_columns=columns,quadratic_matrix=B,
        acquired_field_quadratic=base,acquired_defect=defect,acquired_defect_rank=r,
        decoding=decoding,field_polynomial=[dict(exponents=list(e),coefficient=c) for e,c in sorted(fieldpoly.items())],
        balanced_polynomial=[dict(exponents=list(e),coefficient=c) for e,c in sorted(balanced.items())],
        field_columns=field_columns,field_fit=fit,factorization=factorization,
        symplectic_factors=factors,linear_correction=linear,walsh_leaf_count=1<<r,
        retained_leaf_data=retain_leaf_data,walsh_leaves=leaves,
        exact_numerator=numerator,exact_denominator=denominator,signed_count=signed,
        zero_count=((1<<n)+signed)//2,seconds=time.perf_counter()-start,raw_polynomial=sorted(poly))
