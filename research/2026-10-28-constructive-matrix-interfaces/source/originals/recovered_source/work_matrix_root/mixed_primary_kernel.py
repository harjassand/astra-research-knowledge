#!/usr/bin/env python3
"""Actual-q profile kernel with separately truncated primary degrees."""
from pathlib import Path
import itertools,math,sys,time
from fractions import Fraction
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/p) for p in ('work_matrix_root','work_norm_frontier_agent','work_norm_slice_agent')]
from structured_pfaffian import complete_coefficients,_center
from cyclic_primary_pfaffian import coefficient_degree_bound
from fat_hook_hall import FatHookBasis,evaluate,n_stat

def coefficient_ring(specifications):
    states=list(itertools.product(*(range(s['maximum']+1) for s in specifications)))
    index={state:i for i,state in enumerate(states)};splits=[]
    for state in states:
        splits.append([(index[left],index[tuple(x-y for x,y in zip(state,left))])
            for left in itertools.product(*(range(x+1) for x in state))])
    physical=[sum(s['degree']*k for s,k in zip(specifications,state)) for state in states]
    return states,index,splits,physical

def manufactured_coefficient_bound(t,q,specifications,states,physical):
    """Bound each cleared coefficient using its finite exact Cauchy sum."""
    norms=[];clearers=[]
    for spec in specifications:
        d=spec['degree'];m=spec['maximum'];xs=tuple(spec['cyclic']);ys=tuple(spec['semisimple']);Q=q**d
        row=[];den=[];normalizer=1
        for k in range(m+1):
            basis=FatHookBasis(k,len(xs),len(ys),Q)
            row.append(sum((abs(evaluate(poly,xs+ys))/Q**n_stat(shape)
                for lead,shape,coefficient,poly in basis.entries),Fraction(0)))
            if k and ys:normalizer*=1-Q**k
            den.append(normalizer)
        norms.append(row);clearers.append(den)
    bounds=[];normalizers=[]
    for state,c in zip(states,physical):
        normalizer=math.prod(den[k] for den,k in zip(clearers,state))
        bound=Fraction(4*(t+1)*q**coefficient_degree_bound(t,c)*abs(normalizer))
        for row,k in zip(norms,state):bound*=row[k]
        bounds.append((bound.numerator+bound.denominator-1)//bound.denominator)
        normalizers.append(normalizer)
    bound=max(1,*bounds);bits=(2*bound+1).bit_length();a=q.bit_length()-1
    return dict(bound=bound,bounds=bounds,normalizers=normalizers,output_bits=bits,
        cutoff=(bits+a-1)//a,computed_from_finite_cauchy_coefficients=True)


def mixed_minor_numerator(t,base,specifications,states,splits,physical,modulus,cutoff):
    """Explicit division-free structured actions in the multigraded ring."""
    started=time.perf_counter();odd=t%2;m=(t+1)//2;e=len(states)-1
    L=2*cutoff+t+max(physical);size=L+odd;components=1+odd;period=8;phase_ring=True;boundary=1
    per_primary=[complete_coefficients(base,s['degree'],s['maximum'],modulus,
        general_alphabets=(tuple(s['cyclic']),tuple(s['semisimple']))) for s in specifications]
    hs=[math.prod(row[k] for row,k in zip(per_primary,state))%modulus for state in states]
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
                for k,right in splits[degree]:
                    if not hs[k]:continue
                    shift=physical[k]
                    if shift>=L:continue
                    if transposed:A[:,:,shift:L]+=hs[k]*T[component][right][:,:,:L-shift]
                    else:A[:,:,:L-shift]+=hs[k]*T[component][right][:,:,shift:L]
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
        coefficient_states=len(states),coefficient_convolution_pairs=sum(map(len,splits)),sentinel_degree=odd,boundary_group_algebra_rank=period,dense_matrix_products=0,
        normalization_degree_cutoff=cutoff,ring_modulus_bits=modulus.bit_length(),
        operation_counts=counters,seconds=time.perf_counter()-started)

def mixed_primary_profile_kernel(t,q,specifications):
    """Four exact rational profile components per primary multidegree."""
    begun=time.perf_counter()
    if type(t) is not int or t<1 or type(q) is not int or q<2 or q&(q-1):
        raise ValueError('positive dimension and binary cardinality required')
    for spec in specifications:
        if type(spec['degree']) is not int or spec['degree']<1 or type(spec['maximum']) is not int or spec['maximum']<0:
            raise ValueError('positive degree and nonnegative truncation required')
        if not spec['cyclic'] and not spec['semisimple']:raise ValueError('nonempty primary alphabet required')
        if any(type(x) is not int for x in tuple(spec['cyclic'])+tuple(spec['semisimple'])):
            raise ValueError('integer evaluation alphabet required')
    states,index,splits,physical=coefficient_ring(specifications)
    if max(physical)>t:raise ValueError('physical degree exceeds ambient size')
    bound=manufactured_coefficient_bound(t,q,specifications,states,physical)
    a=q.bit_length()-1;r=t//2;shift=r*r if t%2 else r*(r-1)
    modulus=1<<(bound['output_bits']+a*shift);small=1<<bound['output_bits']
    raw,metadata=mixed_minor_numerator(t,q,specifications,states,splits,physical,modulus,bound['cutoff'])
    divisor=q**shift;prefactor=math.prod(1-q**j for j in range(1,t+1));values={}
    for i,(state,c) in enumerate(zip(states,physical)):
        residues=[];normalizer=bound['normalizers'][i]
        for value in raw[i]:
            if value%divisor:raise AssertionError('mixed q-shift divisibility failed')
            residue=(value//divisor)*prefactor*normalizer%small
            residues.append(residue-small if residue>=small//2 else residue)
        if any(residues[j] for j in range(8) if (c-j)%2):raise AssertionError('mixed phase parity failed')
        row=[residues[(c-2*h)%8] for h in range(4)]
        if sum(map(abs,row))>bound['bounds'][i]:raise AssertionError('mixed coefficient exceeded its bound')
        values[state]=[Fraction(value,normalizer) for value in row]
    if values[states[0]]!=[1,0,0,0]:raise AssertionError('mixed empty normalization failed')
    metadata.update(field_degree=a,ambient_size=t,primary_degrees=[s['degree'] for s in specifications],
        primary_maxima=[s['maximum'] for s in specifications],normalization_q_shift=shift,
        modulus_bits=modulus.bit_length(),output_bound=bound['bound'],
        independently_truncated_primary_degrees=True,newton_divisions=0,
        enumerated_unrestricted_partitions=0,seconds=time.perf_counter()-begun)
    return values,metadata
