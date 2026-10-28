#!/usr/bin/env python3
"""Acquire and sum phase-carrier chains with unboundedly many diamonds."""
from pathlib import Path
from functools import lru_cache
import sys,time
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'work_matrix_root'))
from matrix_affine_flag_counter import *
from matrix_affine_flag_counter import _add_scaled


def contained(A,B):
    C=BinaryCoordinates(B)
    try:
        for v in A:C.coordinates(v)
    except ValueError:return False
    return True


def intersection(A,B):
    A=canonical_binary_span(A);B=canonical_binary_span(B)
    width=max((x.bit_length() for x in A+B),default=0)
    return canonical_binary_span(apply_binary(A,w&((1<<len(A))-1))
        for w in linear_kernel(list(A)+list(B),width))


@lru_cache(None)
def gl_order(r,a):
    q=1<<a;answer=1
    for i in range(r):answer*=q**r-q**i
    return answer


@lru_cache(None)
def two_carrier_census(k,f,g,i,j,eta,theta,a):
    """j-subspaces meeting f-,g-spaces in eta,theta dimensions, intersection i."""
    if not (0<=i<=min(f,g) and f+g-i<=k and 0<=j<=k):return 0
    A=f-i;B=g-i;C=k-f-g+i;answer=0
    for e in range(i+1):
        alpha=eta-e;beta=theta-e;r=j-e
        if not (0<=alpha<=A and 0<=beta<=B and r>=0):continue
        base=gaussian_binomial(i,e,a)*(1<<(a*(i-e)*r))
        base*=gaussian_binomial(A,alpha,a)*gaussian_binomial(B,beta,a)
        for ell in range(min(A-alpha,B-beta)+1):
            inside=alpha+beta+ell;outside=r-inside
            if not 0<=outside<=C:continue
            count=gaussian_binomial(A-alpha,ell,a)*gaussian_binomial(B-beta,ell,a)*gl_order(ell,a)
            count*=gaussian_binomial(C,outside,a)*(1<<(a*(A+B-inside)*outside))
            answer+=base*count
    return answer


def acquire_diamond_chain(groups,ambient):
    """Recognize matching incomparability and manufacture its ordered spine."""
    spaces=list(groups);pairs=[];matched={}
    for j,F in enumerate(spaces):
        for G in spaces[:j]:
            if contained(F,G) or contained(G,F):continue
            if F in matched or G in matched:
                raise ValueError('phase-carrier incomparability graph is not a matching')
            matched[F]=G;matched[G]=F;pairs.append((F,G))
    spine={(),ambient};spine.update(F for F in spaces if F not in matched)
    diamonds={}
    for F,G in pairs:
        I=intersection(F,G);S=canonical_binary_span(F+G)
        if (I,S) in diamonds:raise AssertionError('duplicate diamond interval')
        diamonds[I,S]=(F,G);spine.update((I,S))
    spine=sorted(spine,key=lambda F:(len(F),F))
    for A,B in zip(spine,spine[1:]):
        if not contained(A,B):raise AssertionError('matching incomparability did not yield a chain')
    positions={F:j for j,F in enumerate(spine)}
    for I,S in diamonds:
        if positions[S]!=positions[I]+1:raise AssertionError('diamond interval has an internal spine node')
    return spine,diamonds


def affine_diamond_histogram(components,a,ap):
    """Actual module rows -> signed histogram; module origin is acquired upstream."""
    begun=time.perf_counter();carriers=[];zeros=[];d=c=0
    for item in components:
        E=canonical_binary_span(item['target_rows']);F=canonical_binary_span(item['phase_kernel_rows'])
        g,rem=divmod(len(E),ap);f,rem2=divmod(len(F),ap)
        s=item['matrix_degree'];h=item['natural_multiplicity'];t=item['phase_rank']
        if rem or rem2 or not 0<=g<=s or not 0<=t<=s or not max(0,g-t)<=f<=min(g,s-t):
            raise ValueError('invalid actual target/phase module ranks')
        if not contained(F,E):raise ValueError('phase carrier lies outside target carrier')
        record=dict(target_rows=E,phase_kernel_rows=F,target_rank=g,phase_image_rank=f,
            matrix_degree=s,natural_multiplicity=h,phase_rank=t)
        (carriers if g else zeros).append(record);d+=h*s;c+=a*s*s
    k=carriers[0]['target_rank'] if carriers else 0;ambient=carriers[0]['target_rows'] if carriers else ()
    if any(x['target_rows']!=ambient for x in carriers):raise ValueError('nonzero target carriers do not coincide')
    groups={():[],ambient:[]}
    for item in carriers:groups.setdefault(item['phase_kernel_rows'],[]).append(item)
    spine,diamonds=acquire_diamond_chain(groups,ambient)
    for F in spine:
        if len(F)%ap:raise AssertionError('manufactured spine has nonintegral natural dimension')
    zero_polynomial=[1]
    for item in zeros:
        zero_polynomial=polynomial_product(zero_polynomial,signed_rectangular_rank_polynomial(
            item['matrix_degree'],item['matrix_degree'],item['phase_rank'],item['natural_multiplicity'],a))
    @lru_cache(None)
    def group_polynomial(F,j,eta):
        f=len(F)//ap;value=[1]
        for item in groups.get(F,[]):
            s=item['matrix_degree'];r=s-k+j;tau=item['phase_rank']-k+j+f-eta
            value=polynomial_product(value,signed_rectangular_rank_polynomial(s,r,tau,item['natural_multiplicity'],a))
        return tuple(value)
    moments=[];state_count=transition_count=0
    for j in range(k+1):
        states={0:polynomial_product(zero_polynomial,group_polynomial((),j,0))}
        for lower,upper in zip(spine,spine[1:]):
            i=len(lower)//ap;s_dim=len(upper)//ap;updated={}
            if (lower,upper) not in diamonds:
                gap=s_dim-i
                for e,poly in states.items():
                    for t in range(e,min(j,s_dim)+1):
                        delta=t-e
                        if delta>gap or j-t>k-s_dim:continue
                        scale=gaussian_binomial(gap,delta,a)*(1<<(a*(i-e)*delta))
                        value=polynomial_product(poly,group_polynomial(upper,j,t))
                        _add_scaled(updated.setdefault(t,[]),value,scale);transition_count+=1
            else:
                F,G=diamonds[lower,upper];A=len(F)//ap-i;B=len(G)//ap-i
                if A+B!=s_dim-i:raise AssertionError('diamond quotient is not a direct sum')
                for e,poly in states.items():
                    for t in range(e,min(j,s_dim)+1):
                        if t-e>A+B or j-t>k-s_dim:continue
                        lift=1<<(a*(i-e)*(t-e))
                        for alpha in range(min(A,t-e)+1):
                            for beta in range(min(B,t-e-alpha)+1):
                                ell=t-e-alpha-beta
                                if ell>min(A-alpha,B-beta):continue
                                scale=lift*gaussian_binomial(A,alpha,a)*gaussian_binomial(B,beta,a)
                                scale*=gaussian_binomial(A-alpha,ell,a)*gaussian_binomial(B-beta,ell,a)*gl_order(ell,a)
                                value=polynomial_product(poly,group_polynomial(F,j,e+alpha))
                                value=polynomial_product(value,group_polynomial(G,j,e+beta))
                                value=polynomial_product(value,group_polynomial(upper,j,t))
                                _add_scaled(updated.setdefault(t,[]),value,scale);transition_count+=1
            if any(len(x)>d+1 for x in updated.values()):raise AssertionError('diamond polynomial exceeds actual dual rank')
            states=updated;state_count+=len(states)
        if set(states)!={j}:raise AssertionError('final ambient did not force the final dimension')
        moments.append(states[j])
    exact=[];histogram={}
    for rho in range(k+1):
        value=moments[rho]+[0]*(d+1-len(moments[rho]))
        for u in range(rho):_add_scaled(value,exact[u],-gaussian_binomial(k-u,rho-u,a))
        exact.append(value)
        for t,x in enumerate(value):
            if x:histogram[t,rho]=x
    if histogram.get((0,0))!=1:raise AssertionError('zero matrix lost')
    if sum(histogram.values())!=(1<<c if all(x['phase_rank']==0 for x in components) else 0):
        raise AssertionError('diamond transform lost signed mass')
    return histogram,dict(target_rank=k,dual_maximum_rank=d,codimension=c,
        phase_spine_dimensions=[len(F)//ap for F in spine],phase_spine_row_bases=[list(F) for F in spine],
        phase_diamonds=[dict(intersection_dimension=len(I)//ap,sum_dimension=len(S)//ap,
            first_dimension=len(F)//ap,second_dimension=len(G)//ap,
            first_rows=list(F),second_rows=list(G)) for (I,S),(F,G) in diamonds.items()],
        target_row_basis=list(ambient),zero_target_components=len(zeros),
        transfer_dimension_states=state_count,transfer_transitions=transition_count,
        histogram_states=len(histogram),characters_enumerated=0,subspaces_enumerated=0,
        seconds=time.perf_counter()-begun)


def affine_matrix_diamond_target(certificate,compression,target,affine_hom_offset=0):
    acquired=acquire_matrix_phase_carriers(certificate,compression,target,affine_hom_offset)
    if 'population' in acquired:return acquired
    C=certificate['nucleus'];a=C['field_degree'];p=C['left_matrix_rows'];d=C['inner_dimension'];ap=a*p
    histogram,flag=affine_diamond_histogram(acquired['components'],a,ap);k=flag['target_rank']
    if acquired['target_rank']!=k:raise AssertionError('flag lost original target rank')
    if flag['dual_maximum_rank']!=d or flag['codimension']!=compression['codimension']:raise AssertionError('flag changed acquired dimensions')
    total=sum(weight*signed_universal_product(p,d,d,a,k,t,rho) for (t,rho),weight in histogram.items())
    answer,rem=divmod(total,1<<compression['codimension'])
    if rem or not 0<=answer<=1<<C['input_bits']:raise AssertionError('invalid original-input affine count')
    return dict(population=answer,matrix_target_rank=k,codimension=compression['codimension'],
        phase_carrier_acquisition=acquired['phase_carrier_acquisition'],diamond_certificate=flag,
        rank_pair_histogram={f'{t},{rho}':v for (t,rho),v in sorted(histogram.items())},
        histogram_states=len(histogram),characters_enumerated=0,original_assignments_enumerated=0)
