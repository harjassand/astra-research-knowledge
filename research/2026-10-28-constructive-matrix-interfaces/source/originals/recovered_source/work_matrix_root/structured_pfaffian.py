#!/usr/bin/env python3
"""Division-free minor sums using Toeplitz and semiseparable right actions.

Bird--Przezdziecki alternating truncation computes the required Pfaffian
minor coefficient. Every right product uses shifts or prefix sums,
including the odd square-zero sentinel. No dense matrix products.
"""
from pathlib import Path
import sys,time
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'work_norm_slice_agent'))
from cyclic_primary_pfaffian import _kernel_geometry,_packing_bound_bits,_balanced_coefficients
from math import factorial

def _center(A,modulus):return (A+modulus//2)%modulus-modulus//2

def complete_coefficients(base,d,e,modulus,semisimple=False,pair_alphabet=None,hybrid_alphabet=None,general_alphabets=None):
    cyclic=[1]+[(pow(base,d*k,modulus)-pow(base,d*(k-1),modulus))%modulus for k in range(1,e+1)]
    if general_alphabets is not None:
        xs,ys=general_alphabets;hs=[1]+[0]*e
        for x in xs:
            old=hs;factor=[c*pow(x,k,modulus)%modulus for k,c in enumerate(cyclic)]
            hs=[sum(old[j]*factor[k-j] for j in range(k+1))%modulus for k in range(e+1)]
        for y in ys:hs=[(hs[k]-(y*hs[k-1] if k else 0))%modulus for k in range(e+1)]
        return hs
    hs=[1]+([-1]+[0]*(e-1) if e else []) if semisimple else cyclic
    if pair_alphabet is not None:
        old=hs;hs=[sum(old[j]*old[k-j]*pow(pair_alphabet,k-j,modulus) for j in range(k+1))%modulus for k in range(e+1)]
    if hybrid_alphabet is not None:
        old=hs;hs=[(old[k]-(hybrid_alphabet*old[k-1] if k else 0))%modulus for k in range(e+1)]
    return [x%modulus for x in hs]

def minor_sum_numerator(t,d,boundary,e,base,modulus,cutoff,semisimple=False,pair_alphabet=None,hybrid_alphabet=None,general_alphabets=None,phase_ring=False):
    """Return [w^0..w^e] sum_|U|=2m Pf(B_U)Pf(C_U), sentinel selected."""
    started=time.perf_counter();odd=t%2;m=(t+1)//2;L=2*cutoff+t+d*e;size=L+odd;components=1+odd;period=8 if phase_ring else 1
    hs=complete_coefficients(base,d,e,modulus,semisimple,pair_alphabet,hybrid_alphabet,general_alphabets)
    powers=[pow(base,x//2,modulus) for x in range(L)]
    bottom_f=[powers[x] if x%2==1-odd else 0 for x in range(L)]
    bottom_g=[powers[x] if x%2==odd else 0 for x in range(L)]
    top_f=[boundary if x%2==odd else 1 for x in range(L)]
    top_g=[boundary if x%2!=odd else 1 for x in range(L)]
    sentinel=[powers[x] if not x%2 else 0 for x in range(L)]
    counters=dict(toeplitz_actions=0,semiseparable_actions=0,rank_two_actions=0,truncations=0)
    def empty():return [[np.zeros((period,size,size),dtype=object) for _ in range(e+1)] for _ in range(components)]
    def right_toeplitz(T,transposed=False):
        out=empty();counters['toeplitz_actions']+=1
        for component in range(components):
            for degree in range(e+1):
                A=out[component][degree]
                for k in range(degree+1):
                    if not hs[k]:continue
                    shift=d*k
                    if shift>=L:continue
                    if transposed:A[:,:,shift:L]+=hs[k]*T[component][degree-k][:,:,:L-shift]
                    else:A[:,:,:L-shift]+=hs[k]*T[component][degree-k][:,:,shift:L]
                if odd:A[:,:,L]+=T[component][degree][:,:,L]
                out[component][degree]=_center(A,modulus)
        return out
    def right_semiseparable(A,f,g,border=False):
        out=np.zeros((period,size,size),dtype=object);total=np.zeros((period,size),dtype=object)
        for x in range(L):
            if f[x]:total+=f[x]*A[:,:,x]
        prefix_f=np.zeros((period,size),dtype=object);prefix_g=np.zeros((period,size),dtype=object)
        for y in range(L):
            out[:,:,y]=g[y]*(total-prefix_f-f[y]*A[:,:,y])-f[y]*prefix_g
            if border:out[:,:,y]-=f[y]*A[:,:,L]
            if f[y]:prefix_f+=f[y]*A[:,:,y]
            if g[y]:prefix_g+=g[y]*A[:,:,y]
        if border:out[:,:,L]=total
        return _center(out,modulus)
    def right_bottom(T):
        out=empty();counters['semiseparable_actions']+=components*(e+1)
        for component in range(components):
            for degree in range(e+1):
                out[component][degree]=right_semiseparable(T[component][degree],bottom_f,bottom_g)
        if odd:
            for degree in range(e+1):
                A=T[0][degree];extra=np.zeros((period,size,size),dtype=object)
                for x in range(L):
                    if sentinel[x]:
                        extra[:,:,x]=-sentinel[x]*A[:,:,L]
                        extra[:,:,L]+=sentinel[x]*A[:,:,x]
                out[1][degree]=_center(out[1][degree]+extra,modulus)
                counters['rank_two_actions']+=1
        return out
    def right_C(T):return right_toeplitz(right_bottom(right_toeplitz(T)),transposed=True)
    def right_B(T):
        counters['semiseparable_actions']+=components*(e+1)
        if phase_ring:
            def one(A):
                out=np.zeros_like(A);total=np.zeros((period,size),dtype=object)
                for x in range(L):total+=np.roll(A[:,:,x],int(x%2==odd),axis=0)
                prefix_f=np.zeros_like(total);prefix_g=np.zeros_like(total)
                for y in range(L):
                    f=int(y%2==odd);g=1-f;column=A[:,:,y]
                    out[:,:,y]=np.roll(total-prefix_f-np.roll(column,f,axis=0),g,axis=0)-np.roll(prefix_g,f,axis=0)
                    if odd:out[:,:,y]-=np.roll(A[:,:,L],f,axis=0)
                    prefix_f+=np.roll(column,f,axis=0);prefix_g+=np.roll(column,g,axis=0)
                if odd:out[:,:,L]=total
                return _center(out,modulus)
            return [[one(A) for A in part] for part in T]
        return [[right_semiseparable(A,top_f,top_g,bool(odd)) for A in part] for part in T]
    def truncate(T):
        out=empty();counters['truncations']+=components*(e+1)
        for component in range(components):
            for degree in range(e+1):
                A=T[component][degree];B=np.triu(A,1);suffix=np.zeros(period,dtype=object)
                for i in range(size-1,-1,-1):B[:,i,i]=-suffix;suffix+=A[:,i,i]
                out[component][degree]=_center(B,modulus)
        return out
    identity=empty()
    for i in range(size):identity[0][0][0,i,i]=1
    T=right_C(identity)
    for p in range(1,m+1):
        T=right_B(truncate(T))
        if p<m:T=right_C(truncate(T))
    values=[[(-sum(T[odd][degree][group,i,i] for i in range(size)))%modulus for group in range(period)] for degree in range(e+1)]
    if not phase_ring:values=[row[0] for row in values]
    return values,dict(route='division-free Pfaffian minor sum by structured right actions',
        particle_positions=L,matrix_size=size,pfaffian_particle_pairs=m,
        polynomial_degree=e,sentinel_degree=odd,boundary_group_algebra_rank=period,dense_matrix_products=0,
        normalization_degree_cutoff=cutoff,ring_modulus_bits=modulus.bit_length(),
        operation_counts=counters,seconds=time.perf_counter()-started)

def normalize_numerator(values,t,d,e,base,modulus,shift,semisimple=False,hybrid_alphabet=None,general_alphabets=None):
    divisor=base**shift
    if modulus%divisor:raise ValueError('the working modulus must retain the normalization shift')
    small=modulus//divisor;prefactor=1;out=[]
    for j in range(1,t+1):prefactor=prefactor*(1-pow(base,j,small))%small
    for degree,value in enumerate(values):
        if value%divisor:raise AssertionError('Pfaffian q-shift is not exactly divisible')
        value=(value//divisor)*prefactor%small
        if semisimple or hybrid_alphabet is not None or (general_alphabets is not None and general_alphabets[1]):
            for j in range(1,degree+1):value=value*(1-pow(base,d*j,small))%small
        out.append(value)
    return out,small

def kernel_structured_boundary(t,d,boundary,actual_q,maximum=None,semisimple=False,pair_alphabet=None,hybrid_alphabet=None,general_alphabets=None):
    begun=time.perf_counter()
    e,cmax,odd,r,m,shift,R,precision,L,size,components=_kernel_geometry(t,d,maximum,semisimple,False,pair_alphabet,hybrid_alphabet,general_alphabets)
    bits=_packing_bound_bits(t,size,boundary,False,pair_alphabet,hybrid_alphabet,general_alphabets)
    base=(1<<bits)*factorial(2*t)+1;modulus=base**(precision+1)
    numerator,metadata=minor_sum_numerator(t,d,boundary,e,base,modulus,R,semisimple,pair_alphabet,hybrid_alphabet,general_alphabets)
    packed,small=normalize_numerator(numerator,t,d,e,base,modulus,shift,semisimple,hybrid_alphabet,general_alphabets)
    polynomials=[_balanced_coefficients(x,base,R) for x in packed];values=[]
    for coefficients in polynomials:
        value=0
        for c in reversed(coefficients):value=value*actual_q+c
        values.append(value)
    if values[0]!=1:raise AssertionError('empty structured-kernel normalization failed')
    metadata.update(formal_q_polynomials=polynomials,ambient_size=t,primary_degree=d,boundary=boundary,
        q_degree_bound=R,normalization_q_shift=shift,packing_base_bits=base.bit_length(),
        total_seconds=time.perf_counter()-begun)
    return values,metadata

def physical_output_bound(t,d,boundary,actual_q,maximum=None,semisimple=False,pair_alphabet=None,hybrid_alphabet=None,general_alphabets=None):
    from cyclic_primary_pfaffian import coefficient_degree_bound
    if type(actual_q) is not int or actual_q<2 or actual_q&(actual_q-1):raise ValueError('a binary field cardinality is required')
    if type(boundary) is not int:raise ValueError('an ordinary integer boundary is required')
    e,cmax,odd,r,m,shift,R0,precision,L0,size0,components=_kernel_geometry(t,d,maximum,semisimple,False,pair_alphabet,hybrid_alphabet,general_alphabets)
    exponent=max(coefficient_degree_bound(t,c) for c in range(cmax+1));constant=4;letters=1;largest=1
    if general_alphabets is not None:
        xs,ys=general_alphabets;letters=len(xs)+len(ys);largest=max((abs(x) for x in tuple(xs)+tuple(ys)),default=1)
        if ys:exponent+=d*e*(e+1)//2
    elif hybrid_alphabet is not None:
        letters=2;largest=max(1,abs(hybrid_alphabet));exponent+=d*e*(e+1)//2
    elif pair_alphabet is not None:
        letters=2;largest=max(1,abs(pair_alphabet))
        if semisimple:constant=16;exponent+=d*(e*e//4)
    bound=constant*(cmax+1)*(e+1)**letters*max(1,largest)**e*max(1,abs(boundary))**cmax*actual_q**exponent
    bits=bound.bit_length()+1;a=actual_q.bit_length()-1;cutoff=(bits+a-1)//a
    return dict(output_bound=bound,output_bits=bits,field_degree=a,cutoff=cutoff,shift=shift,
        maximum=e,original_formal_degree_bound=R0,physical_bound_q_exponent=exponent,
        bound_source='positive Hall convexity and physical subspace bounds',
        coefficient_bound_packing_used=False)

def kernel_structured_actual_q(t,d,boundary,actual_q,maximum=None,semisimple=False,pair_alphabet=None,hybrid_alphabet=None,general_alphabets=None):
    begun=time.perf_counter()
    bound=physical_output_bound(t,d,boundary,actual_q,maximum,semisimple,pair_alphabet,hybrid_alphabet,general_alphabets)
    e=bound['maximum'];shift=bound['shift'];modulus=1<<(bound['output_bits']+bound['field_degree']*shift)
    numerator,metadata=minor_sum_numerator(t,d,boundary,e,actual_q,modulus,bound['cutoff'],
        semisimple,pair_alphabet,hybrid_alphabet,general_alphabets)
    residues,small=normalize_numerator(numerator,t,d,e,actual_q,modulus,shift,semisimple,hybrid_alphabet,general_alphabets)
    values=[x-small if x>=small//2 else x for x in residues]
    if any(abs(x)>bound['output_bound'] for x in values):raise AssertionError('actual integer violates physical output bound')
    if values[0]!=1:raise AssertionError('actual-q structured empty normalization failed')
    metadata.update(bound,route='actual-q division-free structured Pfaffian',
        actual_q=actual_q,boundary=boundary,ambient_size=t,primary_degree=d,
        newton_divisions=0,exact_shift_division=True,total_seconds=time.perf_counter()-begun)
    return values,metadata

def kernel_structured_refined_actual_q_interpolation(t,d,actual_q,maximum=None,semisimple=False,pair_alphabet=None,hybrid_alphabet=None,general_alphabets=None):
    from cyclic_primary_pfaffian import _integer_interpolate
    e=t//d if maximum is None else maximum;evaluations=[];records=[];started=time.perf_counter()
    for boundary in range(t+1):
        values,metadata=kernel_structured_actual_q(t,d,boundary,actual_q,e,semisimple,pair_alphabet,hybrid_alphabet,general_alphabets)
        evaluations.append(values);records.append(metadata)
    weights=[]
    for degree in range(e+1):
        c=d*degree;polynomial=_integer_interpolate([row[degree] for row in evaluations]);row=[0]*4
        for k,value in enumerate(polynomial):
            if k>c or (c-k)%2:
                if value:raise AssertionError('actual-q boundary degree/parity mismatch')
            else:row[((c-k)//2)%4]+=value
        weights.append(row)
    return weights,dict(route='actual-q structured Pfaffian and exact boundary interpolation',
        boundary_evaluations=t+1,pfaffian_evaluations=records,dense_matrix_products=0,
        newton_divisions=0,seconds=time.perf_counter()-started)


def kernel_structured_refined_actual_q(t,d,actual_q,maximum=None,semisimple=False,pair_alphabet=None,hybrid_alphabet=None,general_alphabets=None):
    """Recover H mod 4 by one evaluation in the integral C8 group algebra.

    Coefficient u^(c-2h mod 8) is exactly the h-th class in degree c.
    This readout has no interpolation, Fourier transform, or division.
    """
    begun=time.perf_counter()
    bound=physical_output_bound(t,d,1,actual_q,maximum,semisimple,pair_alphabet,hybrid_alphabet,general_alphabets)
    e=bound['maximum'];shift=bound['shift'];modulus=1<<(bound['output_bits']+bound['field_degree']*shift)
    raw,metadata=minor_sum_numerator(t,d,1,e,actual_q,modulus,bound['cutoff'],
        semisimple,pair_alphabet,hybrid_alphabet,general_alphabets,phase_ring=True)
    residues=[]
    for group in range(8):
        row,small=normalize_numerator([entry[group] for entry in raw],t,d,e,actual_q,modulus,shift,
            semisimple,hybrid_alphabet,general_alphabets)
        residues.append([x-small if x>=small//2 else x for x in row])
    weights=[]
    for degree in range(e+1):
        c=d*degree
        if any(residues[k][degree] for k in range(8) if (c-k)%2):
            raise AssertionError('cyclic boundary coefficient has incorrect parity')
        row=[residues[(c-2*h)%8][degree] for h in range(4)]
        if sum(map(abs,row))>bound['output_bound']:
            raise AssertionError('refined coefficient l1 sum exceeds the physical bound')
        weights.append(row)
    if weights[0]!=[1,0,0,0]:raise AssertionError('empty cyclic-boundary normalization failed')
    metadata.update(bound,route='actual-q structured Pfaffian over the integral cyclic boundary ring',
        actual_q=actual_q,ambient_size=t,primary_degree=d,boundary_evaluations=1,
        boundary_ring='(Z/2^P Z)[u]/(u^8-1)',newton_divisions=0,fourier_divisions=0,
        coefficient_readout='h maps to (d*degree-2*h) modulo 8',
        exact_shift_division=True,total_seconds=time.perf_counter()-begun)
    return weights,metadata
