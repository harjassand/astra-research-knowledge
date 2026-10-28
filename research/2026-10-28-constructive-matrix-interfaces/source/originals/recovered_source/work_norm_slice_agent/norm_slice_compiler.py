#!/usr/bin/env python3
"""Exact universal cubic restriction of one split finite-field trace norm.

The output is a representation and normalization, NOT a counting algorithm.
No source assignments are enumerated by the compiler. Field construction,
CRT interpolation, trace duality, affine constraints, and optional raw ANF
expansion are explicit. See NORM_SLICE_UNIVERSALITY.md for charged costs.
"""
from pathlib import Path
from functools import lru_cache
import itertools,math,sys
ROOT=Path(__file__).resolve().parents[1]
for folder in ('work_field_root','work_ring_count_agent'):
    sys.path.insert(0,str(ROOT/folder))
from field_kloosterman import gf_mul,gf_pow,irreducible_binary,binary_remainder
from field_descent import linear_apply,nullspace_rows,span,bits
from circuit_field_packing import power_two_field_modulus

def polynomial_product(a,b):
    out=0
    while b:
        if b&1:out^=a
        a<<=1;b>>=1
    return out

def polynomial_division(a,b):
    if not b:raise ZeroDivisionError('zero polynomial divisor')
    quotient=0
    while a and a.bit_length()>=b.bit_length():
        shift=a.bit_length()-b.bit_length();quotient^=1<<shift;a^=b<<shift
    return quotient,a

def polynomial_inverse(a,h):
    old_r,r=h,binary_remainder(a,h);old_s,s=0,1
    while r:
        quotient,remainder=polynomial_division(old_r,r)
        old_r,r=r,remainder;old_s,s=s,old_s^polynomial_product(quotient,s)
    if old_r!=1:raise ValueError('polynomial is not a unit')
    return binary_remainder(old_s,h)

@lru_cache(maxsize=None)
def deterministic_field(degree):
    return power_two_field_modulus(degree)

def trace_powers(h,last):
    """Tr(alpha^j), by Newton sums and the defining linear recurrence."""
    a=h.bit_length()-1;s=[a&1]
    for k in range(1,last+1):
        value=((k&1)&((h>>(a-k))&1)) if k<=a else 0
        for i in range(1,min(k-1,a)+1):value^=((h>>(a-i))&1)&s[k-i]
        s.append(value)
    return s

def trace_mask(h):
    a=h.bit_length()-1
    return sum(value<<i for i,value in enumerate(trace_powers(h,a-1)))

def trace_functional_scalar(h,functional):
    """c with Tr(c*v)=the supplied coefficient-linear functional of v."""
    a=h.bit_length()-1
    derivative=sum(((h>>j)&1)<<(j-1) for j in range(1,a+1,2))
    numerator=0
    for i in bits(functional):numerator^=h>>(i+1)
    c=gf_mul(numerator,polynomial_inverse(derivative,h),h)
    tm=trace_mask(h);current=c
    for i in range(a):
        if ((tm&current).bit_count()&1)!=((functional>>i)&1):
            raise AssertionError('trace-dual coefficient identity failed')
        current<<=1
        if current>>a:current^=h
    if not c:raise AssertionError('nonzero functional had zero trace coefficient')
    return c,tm

def crt_slots(count):
    moduli=[]
    for degree in itertools.count(1):
        for lower in range(1<<degree):
            p=(1<<degree)|lower
            if irreducible_binary(p):moduli.append(p)
            if len(moduli)==count:break
        if len(moduli)==count:break
    product=1
    for p in moduli:product=polynomial_product(product,p)
    idempotents=[]
    for p in moduli:
        quotient,remainder=polynomial_division(product,p)
        assert not remainder
        E=polynomial_product(quotient,polynomial_inverse(quotient,p))
        idempotents.append(E)
    for i,E in enumerate(idempotents):
        for j,p in enumerate(moduli):
            if binary_remainder(E,p)!=int(i==j):raise AssertionError('CRT identity failed')
    return moduli,idempotents,product

def compile_cubic_slice(poly,n):
    """Input only raw degree<=3 Boolean ANF masks and original bit count."""
    if type(n) is not int or n<0:raise ValueError('nonnegative original bit count required')
    poly=set(poly)
    if any(type(m) is not int or m<0 or m>>n or m.bit_count()>3 for m in poly):
        raise ValueError('explicit Boolean cubic ANF required')
    # -1 denotes one and -2 denotes zero. Every other entry is an input index.
    slots=[]
    for mask in sorted(poly):
        factors=list(bits(mask));slots.append(factors+[-1]*(3-len(factors)))
    for i in range(n):slots.append([i,-2,-2])
    if not slots:slots=[[-2,-2,-2]]
    moduli,E,product=crt_slots(len(slots));R=product.bit_length()-1
    required=max(1,3*R-2);a=1<<(required-1).bit_length();h=deterministic_field(a)
    offsets=[0,0,0];columns=[[0]*n for _ in range(3)]
    for slot,e in zip(slots,E):
        for j,factor in enumerate(slot):
            if factor==-1:offsets[j]^=e
            elif factor>=0:columns[j][factor]^=e
    functional=0
    for p in moduli:
        residue=1
        for j in range(a):
            if residue&1:functional^=1<<j
            residue<<=1
            if residue>>(p.bit_length()-1):residue^=p
    c,tm=trace_functional_scalar(h,functional)
    offsets[2]=gf_mul(c,offsets[2],h)
    columns[2]=[gf_mul(c,v,h) for v in columns[2]]
    packed_columns=[sum(columns[j][i]<<(j*a) for j in range(3)) for i in range(n)]
    packed_offset=sum(offsets[j]<<(j*a) for j in range(3))
    if len(span(packed_columns))!=n:raise AssertionError('restriction map is not injective')
    constraints=nullspace_rows(packed_columns,3*a)
    if len(constraints)!=3*a-n:raise AssertionError('wrong affine codimension')
    right_sides=[(row&packed_offset).bit_count()&1 for row in constraints]
    return dict(original_variables=n,source_anf_terms=len(poly),field_degree=a,field_modulus=h,
        trace_mask=tm,trace_functional=functional,trace_scalar=c,
        crt_moduli=moduli,crt_idempotents=E,crt_product_degree=R,slots=slots,
        coordinate_columns=packed_columns,coordinate_offset=packed_offset,
        norm_core_variables=3*a,constraint_rows=constraints,constraint_rhs=right_sides,
        affine_codimension=len(constraints),phase_variables=3*a+len(constraints),
        gap_multiplier_power=len(constraints),source_assignments_enumerated=0,
        universal_counting_algorithm=False)

def source_value(poly,x):
    return sum((x&m)==m for m in poly)&1

def restricted_norm_value(certificate,x):
    a=certificate['field_degree'];h=certificate['field_modulus'];mask=(1<<a)-1
    u=linear_apply(certificate['coordinate_columns'],x)^certificate['coordinate_offset']
    X,Y,Z=[(u>>(j*a))&mask for j in range(3)]
    return (certificate['trace_mask']&gf_mul(gf_mul(X,Y,h),Z,h)).bit_count()&1

def constrained_phase_value(certificate,assignment):
    a=certificate['field_degree'];h=certificate['field_modulus'];mask=(1<<a)-1
    u=assignment&((1<<(3*a))-1);lam=assignment>>(3*a)
    X,Y,Z=[(u>>(j*a))&mask for j in range(3)]
    value=(certificate['trace_mask']&gf_mul(gf_mul(X,Y,h),Z,h)).bit_count()&1
    for j in bits(lam):value^=((certificate['constraint_rows'][j]&u).bit_count()&1)^certificate['constraint_rhs'][j]
    return value

def expand_constrained_anf(certificate,max_terms=None):
    """Explicit polynomial output; all cubic/constraint terms are charged."""
    a=certificate['field_degree'];t=certificate['affine_codimension']
    upper=a**3+t*(3*a+1)
    if max_terms is not None and upper>max_terms:raise ValueError('raw ANF expansion budget exceeded')
    tp=trace_powers(certificate['field_modulus'],3*a-3);out=set()
    for i,j,k in itertools.product(range(a),repeat=3):
        if tp[i+j+k]:out.add((1<<i)|(1<<(a+j))|(1<<(2*a+k)))
    for j,row in enumerate(certificate['constraint_rows']):
        multiplier=1<<(3*a+j)
        for i in bits(row):out.add(multiplier|(1<<i))
        if certificate['constraint_rhs'][j]:out.add(multiplier)
    return out

def decode_source_gap(certificate,phase_gap):
    shift=certificate['gap_multiplier_power'];divisor=1<<shift
    if phase_gap%divisor:raise ValueError('phase gap violates exact normalization')
    return phase_gap//divisor
