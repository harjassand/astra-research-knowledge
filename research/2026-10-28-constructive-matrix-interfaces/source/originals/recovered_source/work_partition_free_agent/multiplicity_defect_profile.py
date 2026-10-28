#!/usr/bin/env python3
"""Two-budget power algebra acquired from primary multiplicity excess.

For s distinct primary degrees and E=sum_f(m_f-1), its state count is at
most (t+1)^s times the number of s-coloured partitions of sizes <=E.
No squarefree, semisimple or bounded-mode hypothesis is assumed.
"""
from pathlib import Path
from functools import lru_cache
import itertools
import math
import sys
import time

ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/p) for p in (
    'work_partition_free_agent','work_matrix_root','work_multiprimary_audit',
    'work_norm_frontier_agent','work_norm_slice_agent')]
from bounded_mode_beta_zero_counter import PowerModeProfileFunctional
from mixed_cycle_kernel import mixed_cycle_minor_numerator
from cyclic_primary_pfaffian import coefficient_degree_bound


def acquired_defect(primary):
    limits={};excess=0
    for item in primary:
        d,m=item['degree'],item['multiplicity']
        limits[d]=max(limits.get(d,0),m)
        excess+=m-1
    costs={}
    for d,m in limits.items():
        for j in range(1,m+1):
            r=d*j
            costs[r]=min(costs.get(r,j-1),j-1)
    modes=tuple(sorted(costs))
    return modes,tuple(costs[r] for r in modes),excess,tuple(sorted(limits))


def defect_power_ring(t,modes,costs,excess):
    """Downward closed divided powers with physical and excess bounds."""
    if (len(modes)!=len(costs) or tuple(sorted(set(modes)))!=tuple(modes)
        or any(type(r)is not int or not 1<=r<=t for r in modes)
        or any(type(c)is not int or c<0 for c in costs)
        or type(excess)is not int or excess<0):
        raise ValueError('sorted physical modes, nonnegative costs and excess required')
    states=[]
    def visit(j,physical_left,defect_left,prefix):
        if j==len(modes):states.append(prefix);return
        limit=physical_left//modes[j]
        if costs[j]:limit=min(limit,defect_left//costs[j])
        for k in range(limit+1):
            visit(j+1,physical_left-modes[j]*k,defect_left-costs[j]*k,prefix+(k,))
    visit(0,t,excess,())
    index={state:i for i,state in enumerate(states)};splits=[]
    for state in states:
        terms=[]
        for left in itertools.product(*(range(k+1) for k in state)):
            right=tuple(k-j for k,j in zip(state,left))
            terms.append((index[left],index[right],
                          math.prod(math.comb(k,j) for k,j in zip(state,left))))
        splits.append(terms)
    physical=[sum(r*k for r,k in zip(modes,state)) for state in states]
    specs=[dict(degree=r,maximum=t//r) for r in modes]
    return specs,states,index,splits,physical


@lru_cache(None)
def defect_profile_weights(t,q,modes,costs,excess):
    started=time.perf_counter()
    if type(q)is not int or q<2 or q&(q-1):raise ValueError('binary field cardinality required')
    specs,states,index,splits,physical=defect_power_ring(t,modes,costs,excess)
    bounds=[4*(c+1)*q**coefficient_degree_bound(t,c) for c in physical]
    bits=(2*max(bounds)+1).bit_length();a=q.bit_length()-1
    cutoff=(bits+a-1)//a;half=t//2
    shift=half*half if t%2 else half*(half-1)
    modulus=1<<(bits+a*shift);small=1<<bits
    raw,metadata=mixed_cycle_minor_numerator(
        t,q,specs,states,splits,physical,modulus,cutoff)
    prefactor=math.prod(1-q**j for j in range(1,t+1));divisor=q**shift
    weights={}
    for state,c,row,bound in zip(states,physical,raw,bounds):
        residues=[]
        for value in row:
            if value%divisor:raise AssertionError('profile q-shift divisibility failed')
            value=(value//divisor)*prefactor%small
            residues.append(value-small if value>=small//2 else value)
        if any(residues[j] for j in range(8) if (c-j)%2):raise AssertionError('profile phase parity failed')
        values=tuple(residues[(c-2*h)%8] for h in range(4))
        if min(values)<0 or sum(values)>bound:raise AssertionError('Hall-convex population bound failed')
        weights[state]=values
    if weights[states[0]]!=(1,0,0,0):raise AssertionError('empty profile normalization failed')
    metadata.update(ambient_size=t,field_degree=a,power_modes=modes,
        power_mode_count=len(modes),mode_defect_costs=costs,
        multiplicity_excess=excess,weighted_monomial_states=len(states),
        zero_defect_modes=[r for r,c in zip(modes,costs) if c==0],
        output_precision_bits=bits,stored_integer_bits=bits+a*shift,
        enumerated_unrestricted_partitions=0,downward_closed_defect_truncation=True,
        field_population_cap_required=False,
        time_bound='poly(a,t,M_E); M_E=#{k:sum r*k_r<=t,sum w_r*k_r<=E}',
        seconds=time.perf_counter()-started)
    return weights,metadata


class DefectProfileFunctional(PowerModeProfileFunctional):
    def __init__(self,q,t,primary):
        modes,costs,excess,degrees=acquired_defect(primary)
        self.modes=modes;self.position={r:i for i,r in enumerate(modes)}
        self.weights,self.metadata=defect_profile_weights(t,q,modes,costs,excess)
        self.metadata['acquired_distinct_degrees']=degrees
        self.metadata['acquired_degree_class_count']=len(degrees)


def defect_beta_zero_count(D,field_h,phi=(),eta=0):
    from bounded_mode_beta_zero_counter import bounded_mode_beta_zero_count
    return bounded_mode_beta_zero_count(D,field_h,phi,eta,profile_backend='defect')
