#!/usr/bin/env python3
"""Exact mixed-cycle profile moments in an integral divided-power ring.

This explicit structured implementation is derived from the audited finite
minor recurrence. Runtime source replacement is not used.
"""
from pathlib import Path
import itertools,math,sys,time
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/p) for p in ('work_matrix_root','work_norm_frontier_agent','work_norm_slice_agent')]
from structured_pfaffian import _center
from cyclic_primary_pfaffian import coefficient_degree_bound
from mixed_primary_kernel import coefficient_ring

def divided_power_ring(specifications):
    states,index,splits,physical=coefficient_ring(specifications)
    weighted=[]
    for state,terms in zip(states,splits):
        weighted.append([(left,right,math.prod(math.comb(k,j)
            for k,j in zip(state,states[left]))) for left,right in terms])
    return states,index,weighted,physical

def mixed_cycle_minor_numerator(t,base,specifications,states,splits,physical,modulus,cutoff):
    """Explicit division-free structured actions in the multigraded ring."""
    started=time.perf_counter();odd=t%2;m=(t+1)//2;e=len(states)-1
    L=2*cutoff+t+max(physical);size=L+odd;components=1+odd;period=8;phase_ring=True;boundary=1
    # Divided-power coefficients of exp(sum_d p_d u_d) after the
    # physical (q-1) plethysm. Factorial normalization is in ring products.
    hs=[math.prod(pow(pow(base,s['degree'],modulus)-1,k,modulus)
        for s,k in zip(specifications,state))%modulus for state in states]
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
                for k,right,weight in splits[degree]:
                    if not hs[k]:continue
                    shift=physical[k]
                    if shift>=L:continue
                    if transposed:A[:,:,shift:L]+=(weight*hs[k])*T[component][right][:,:,:L-shift]
                    else:A[:,:,:L-shift]+=(weight*hs[k])*T[component][right][:,:,shift:L]
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


def irreducible_population(q,d):
    """Number of monic degree-d irreducibles; polynomial integer work."""
    def mobius(n):
        value=1;p=2
        while p*p<=n:
            if n%p==0:
                n//=p;value=-value
                if n%p==0:return 0
                while n%p==0:n//=p
            p+=1
        return -value if n>1 else value
    total=sum(mobius(j)*q**(d//j) for j in range(1,d+1) if d%j==0)
    assert total%d==0
    return total//d


def mixed_cycle_profile_weights(t,q,degree_counts):
    """Return L_(t,h)(prod_d p_d**k_d) for all k below acquired caps.

    Caps must be realizable by distinct irreducibles at actual q, which is
    checked here. This justifies the physical integer coefficient bound.
    """
    begun=time.perf_counter()
    if type(t) is not int or t<1 or type(q) is not int or q<2 or q&(q-1):
        raise ValueError('positive ambient size and binary cardinality required')
    counts=sorted(degree_counts.items())
    if any(type(d) is not int or d<1 or type(m) is not int or m<1 for d,m in counts):
        raise ValueError('positive distinct degree caps required')
    if sum(d*m for d,m in counts)>t:raise ValueError('physical cap exceeds ambient size')
    if any(m>irreducible_population(q,d) for d,m in counts):
        raise ValueError('cap not realizable by distinct actual-field irreducibles')
    specs=[dict(degree=d,maximum=m) for d,m in counts]
    states,index,splits,physical=divided_power_ring(specs)
    bounds=[4*(c+1)*q**coefficient_degree_bound(t,c) for c in physical]
    bound=max(bounds);bits=(2*bound+1).bit_length();a=q.bit_length()-1
    cutoff=(bits+a-1)//a;r=t//2;shift=r*r if t%2 else r*(r-1)
    modulus=1<<(bits+a*shift);small=1<<bits
    raw,metadata=mixed_cycle_minor_numerator(t,q,specs,states,splits,physical,modulus,cutoff)
    prefactor=math.prod(1-q**j for j in range(1,t+1));divisor=q**shift;weights={}
    for state,c,row,bound in zip(states,physical,raw,bounds):
        residues=[]
        for value in row:
            if value%divisor:raise AssertionError('q-shift divisibility failed')
            residue=(value//divisor)*prefactor%small
            residues.append(residue-small if residue>=small//2 else residue)
        if any(residues[j] for j in range(8) if (c-j)%2):raise AssertionError('phase parity failed')
        output=[residues[(c-2*h)%8] for h in range(4)]
        if min(output)<0 or sum(output)>bound:raise AssertionError('physical bound or positivity failed')
        weights[state]=output
    if weights[states[0]]!=[1,0,0,0]:raise AssertionError('empty normalization failed')
    metadata.update(degree_counts=counts,field_degree=a,ambient_size=t,
        original_characteristic_two_divisions=0,factorial_denominators=0,
        integral_divided_power_arithmetic=True,output_precision_bits=bits,
        distinct_degree_classes=len(counts),coefficient_states=len(states),
        stored_integer_bits=bits+a*shift,enumerated_unrestricted_partitions=0,
        time_bound='poly(a,t,prod_d(m_d+1)); at most exp(O(sqrt(t)))*poly(a,t)',
        seconds=time.perf_counter()-begun)
    return weights,metadata
