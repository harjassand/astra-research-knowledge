#!/usr/bin/env python3
"""Exact small real-rational replay of the finite-block/marked construction.

No asymptotic KP evaluator or physical state acquisition is executed. Strong
internal block interference, cross-edge parity, and all canonical numerator
coefficients are checked against explicit full Fock states.
"""
from collections import defaultdict
from fractions import Fraction as Q
from functools import lru_cache
from itertools import combinations
import json
from pathlib import Path

from check_canonical_contraction import (bond_annihilate, bond_create, connected,
                                         full_state, inner, poly_add, poly_mul)


def no_double(state,n):
    return {mask:v for mask,v in state.items()
            if all(((mask >> (2*i)) & 3) != 3 for i in range(n)) and v}


def norm_poly(state,n):
    out = [Q(0)]*(n//2+1)
    for mask,v in state.items():
        out[mask.bit_count()//2] += v*v
    return out


def trim(poly):
    while len(poly)>1 and not poly[-1]: poly.pop()
    return poly


def tensor_states(states):
    out = {0:Q(1)}
    for state in states:
        new = defaultdict(Q)
        for a,v in out.items():
            assert a.bit_count()%2 == 0
            for b,w in state.items():
                assert b.bit_count()%2 == 0 and not a & b
                # Concatenating the two canonical creation words requires a
                # graded shuffle. Even parity alone does not fix its sign
                # when physical mode sets interleave.
                cross_inversions = sum((a >> (j+1)).bit_count()
                                       for j in range(b.bit_length()) if b >> j & 1)
                new[a | b] += (-1)**cross_inversions*v*w
        out = {mask:value for mask,value in new.items() if value}
    return out


def local_state(f,sites):
    n = len(f)
    allowed = set(sites)
    restricted = [[f[i][j] if i in allowed and j in allowed else Q(0)
                   for j in range(n)] for i in range(n)]
    return full_state(restricted)


def pair_operator(state,source,dest,n):
    forward = no_double(bond_create(bond_annihilate(state,source),dest),n)
    reverse = no_double(bond_create(bond_annihilate(state,dest),source),n)
    out = defaultdict(Q)
    for mask,v in forward.items(): out[mask] += v/2
    for mask,v in reverse.items(): out[mask] += v/2
    return {mask:v for mask,v in out.items() if v}


def filtered(state,sign,t,source,dest,n):
    out = defaultdict(Q,state)
    for mask,v in pair_operator(state,source,dest,n).items():
        out[mask] += sign*t*v
    return {mask:v for mask,v in out.items() if v}


def edge_branches(f,blocks,support):
    n = len(f)
    owner = {i:a for a,block in enumerate(blocks) for i in block}
    cells = {a for a in range(len(blocks)) if support >> a & 1}
    refs = [local_state(f,blocks[a]) for a in sorted(cells)]
    initial = tensor_states(refs)
    edges = [(i,j) for i in range(n) for j in range(i+1,n)
             if f[i][j] and owner[i] != owner[j]
             and owner[i] in cells and owner[j] in cells]
    branches = [((),initial)]
    for edge in edges:
        extra = []
        for selected,state in branches:
            moved = no_double(bond_create(state,edge),n)
            if moved:
                extra.append((selected+(edge,),{mask:v*f[edge[0]][edge[1]]
                                                for mask,v in moved.items()}))
        branches += extra
    return branches,owner


def exact_gas(f,blocks,filter_spec=None):
    n = len(f); M = len(blocks)
    source,dest,t,sign,mark = filter_spec if filter_spec else (None,None,None,None,None)
    bg = []
    for a,block in enumerate(blocks):
        state = local_state(f,block)
        if a == mark:
            state = filtered(state,sign,t,source,dest,n)
        bg.append(trim(norm_poly(state,n)))
    acts = {}
    parity_tests = 0
    for support in range(1,1 << M):
        cells = {a for a in range(M) if support >> a & 1}
        if len(cells)<2: continue
        branches,owner = edge_branches(f,blocks,support)
        if mark in cells:
            branches = [(es,filtered(state,sign,t,source,dest,n))
                        for es,state in branches]
        out = [Q(0)]*(n//2+1)
        for es,left in branches:
            for fs,right in branches:
                used = es+fs
                touched = {owner[i] for edge in used for i in edge}
                adjacent = [(owner[i],owner[j]) for i,j in used]
                if touched != cells or not connected(touched,adjacent): continue
                term = [Q(0)]*(n//2+1)
                for mask,v in left.items():
                    if mask in right:
                        term[mask.bit_count()//2] += v*right[mask]
                if len(used)<len(cells):
                    assert not any(term)
                    parity_tests += 1
                out = poly_add(out,term)
        if any(out): acts[support] = trim(out)

    @lru_cache(None)
    def calc(support):
        if not support: return [Q(1)]
        bit = support & -support; site=bit.bit_length()-1
        out = poly_mul(bg[site],calc(support ^ bit))
        for component,activity in acts.items():
            if component & bit and component & support == component:
                out = poly_add(out,poly_mul(activity,calc(support ^ component)))
        return trim(out)

    return calc((1 << M)-1),bg,acts,parity_tests


def moment(poly,r):
    z = sum(v*r**k for k,v in enumerate(poly))
    mean = sum(k*v*r**k for k,v in enumerate(poly))/z
    second = sum(k*k*v*r**k for k,v in enumerate(poly))/z
    return z,mean,second-mean*mean


def threshold_components(f,threshold):
    unseen = set(range(len(f)))
    out = []
    while unseen:
        a = min(unseen); unseen.remove(a)
        component,queue = [a],[a]
        for i in queue:
            for j in list(unseen):
                if abs(f[i][j])>threshold:
                    unseen.remove(j); queue.append(j); component.append(j)
        out.append(tuple(sorted(component)))
    return tuple(out)


def sufficient_family_certificates():
    # Separate from the visible .05 full-state fixture. These are exact
    # size-independent algebraic tests, not a large-lattice numerical replay.
    answer=[]
    for b,d,D in ((4,2,4),(8,4,8)):
        strength=Q(1,10**13); nu=Q(1,10); Delta=2
        v=4*strength  # R=2 and 2 sqrt(2) <= 4.
        h=2**(d+2)*2**(b*Delta)*v
        x=4*D*3**5*h
        S=x*x/(4*D*(1-x))
        passed=(x<=Q(1,4) and S<=nu*Q(1,8)/128
                and S+(D+1)*h*3**d<=nu/16)
        assert passed
        answer.append({'block_size_bound':b,'charge_degree_bound':d,
                       'block_degree_bound':D,'physical_cross_degree_bound':Delta,
                       'lambda_envelope':strength,'reference_variance_margin':nu,
                       'r0':Q(1,2),'R':2,'h':h,'x':x,'S':S,
                       'all_sufficient_tests_exact':passed,
                       'scope':'algebraic family certificate, no large-system replay'})
    return answer


def interleaved_regressions(reference_expectation):
    # Parent's minimal counterexample to the omitted-shuffle helper.
    f=[[Q(0)]*4 for _ in range(4)]
    f[0][2]=f[2][0]=f[1][3]=f[3][1]=Q(1)
    blocks=((0,2),(1,3))
    refs=[local_state(f,block) for block in blocks]
    corrected=tensor_states(refs)
    direct=full_state(f)
    assert corrected == direct
    ungraded={a | b:v*w for a,v in refs[0].items() for b,w in refs[1].items()}
    differing=sum(ungraded.get(mask,Q(0)) != direct.get(mask,Q(0))
                  for mask in set(ungraded)|set(direct))
    assert differing == 4

    # Interleave all three four-site strong blocks and add nonzero weak
    # triangles; neither block-evenness nor nested-support shortcuts suffice.
    n=12; strength=Q(1,20)
    permutation=lambda i:3*(i%4)+i//4
    blocks=tuple(tuple(permutation(4*a+c) for c in range(4)) for a in range(3))
    f=[[Q(0)]*n for _ in range(n)]
    for start in range(0,n,4):
        for i,j in ((0,1),(2,3),(0,2),(1,3)):
            a,b=permutation(start+i),permutation(start+j)
            f[a][b]=f[b][a]=Q(1)
    for i,j,mult in ((0,4,1),(4,8,-1),(0,8,1),
                     (1,5,-1),(5,9,1),(1,9,1)):
        a,b=permutation(i),permutation(j)
        f[a][b]=f[b][a]=strength*mult
    wave=full_state(f)
    branches,_=edge_branches(f,blocks,7)
    reconstructed=defaultdict(Q)
    for _,state in branches:
        for mask,v in state.items(): reconstructed[mask] += v
    assert {mask:v for mask,v in reconstructed.items() if v} == wave
    direct_poly=trim(norm_poly(wave,n))
    gas,_,_,parity=exact_gas(f,blocks)
    assert gas == direct_poly
    marked_blocks=(blocks[0]+blocks[2],blocks[1])
    source=(permutation(0),permutation(1))
    dest=(permutation(8),permutation(9))
    source=tuple(sorted(source)); dest=tuple(sorted(dest))
    t=Q(1,512); k=3; filtered_poly={}
    marked_parity={}
    for sign in (1,-1):
        changed=filtered(wave,sign,t,source,dest,n)
        expected=trim(norm_poly(changed,n))
        via_gas,_,_,tests=exact_gas(f,marked_blocks,(source,dest,t,sign,0))
        assert via_gas == expected
        filtered_poly[sign]=expected
        marked_parity[str(sign)]=tests
    sector={mask:v for mask,v in wave.items() if mask.bit_count()==2*k}
    observed=inner(sector,pair_operator(sector,source,dest,n))/direct_poly[k]
    polarized=(filtered_poly[1][k]-filtered_poly[-1][k])/(4*t*direct_poly[k])
    assert observed == polarized
    assert observed == reference_expectation  # Exact fermionic permutation covariance.
    return {'minimal_counterexample_fixed':True,
            'old_ungraded_helper_wrong_amplitude_count':differing,
            'nonzero_bridge_interleaved_blocks':blocks,
            'creator_product_and_all_canonical_gas_coefficients_exact':True,
            'unfiltered_parity_zero_terms_checked':parity,
            'marked_parity_zero_terms_checked':marked_parity,
            'marked_even_operator_source_and_destination':[source,dest],
            'marked_expectation':observed,
            'equals_contiguous_fixture_expectation_exactly':True,
            'polarization_exact':True,
            'ordering_scope':'physical orbitals interleave; exact graded shuffles used'}


def main():
    strength=Q(1,20); M=3; n=4*M
    blocks=tuple(tuple(range(4*a,4*a+4)) for a in range(M))
    f=[[Q(0)]*n for _ in range(n)]
    for start in range(0,n,4):
        for i,j in ((0,1),(2,3),(0,2),(1,3)):
            f[start+i][start+j]=f[start+j][start+i]=Q(1)
    for i,j,mult in ((0,4,1),(4,8,-1),(0,8,1),
                     (1,5,-1),(5,9,1),(1,9,1)):
        f[i][j]=f[j][i]=strength*mult
    acquired=threshold_components(f,Q(1,2))
    assert acquired == blocks
    direct=full_state(f)
    direct_poly=trim(norm_poly(direct,n))
    branches,_=edge_branches(f,blocks,(1 << M)-1)
    reconstructed=defaultdict(Q)
    for _,state in branches:
        for mask,v in state.items(): reconstructed[mask] += v
    reconstructed={a:b for a,b in reconstructed.items() if b}
    assert reconstructed == direct
    gas,bg,acts,parity=exact_gas(f,blocks)
    assert gas == direct_poly
    assert all(p == [Q(1),Q(8),Q(4)] for p in bg)
    assert all(moment(p,Q(1,2))[1:] == (Q(1),Q(1,3)) for p in bg)

    # Distant block 0 and block 2 become one finite marked fermionic region.
    marked_blocks=(blocks[0]+blocks[2],blocks[1])
    source,dest=(0,1),(8,9)
    t=Q(1,512); k=3; r=Q(1,2)
    filtered_polys={}
    marked_data={}
    for sign in (1,-1):
        changed=filtered(direct,sign,t,source,dest,n)
        exact=trim(norm_poly(changed,n))
        via_gas,bgs,activities,tests=exact_gas(
            f,marked_blocks,(source,dest,t,sign,0))
        assert via_gas == exact
        filtered_polys[sign]=exact
        marked_data[str(sign)]={'reference_polynomials':bgs,
                                'active_component_count':len(activities),
                                'parity_zero_terms_checked':tests,
                                'all_canonical_gas_coefficients_exact':True}
    numerator=inner({mask:v for mask,v in direct.items() if mask.bit_count()==2*k},
                    pair_operator({mask:v for mask,v in direct.items()
                                   if mask.bit_count()==2*k},source,dest,n))
    expected=numerator/direct_poly[k]
    polarized=(filtered_polys[1][k]-filtered_polys[-1][k])/(4*t*direct_poly[k])
    assert expected == polarized
    for sign,poly in filtered_polys.items():
        for a,b in zip(direct_poly,poly):
            assert (1-t)**2*a <= b <= (1+t)**2*a
        original_grand=moment(direct_poly,r)[0]
        changed_grand=moment(poly,r)[0]
        base_mass=direct_poly[k]*r**k/original_grand
        changed_mass=poly[k]*r**k/changed_grand
        assert changed_mass >= ((1-t)/(1+t))**2*base_mass
    result={'status':'PASS exact finite real-rational replay',
            'physical_sites':n,'strong_blocks':blocks,'threshold_acquired':acquired,
            'native_cross_lambda':strength,
            'certificate_status':'visible coupling not claimed KP-certified',
            'strong_reference_charge_polynomial':[1,8,4],
            'per_block_reference_mean_at_half':1,
            'per_block_reference_variance_at_half':'1/3',
            'projected_creator_product_equals_full_Fock_state':True,
            'unfiltered_norm_polynomial':direct_poly,
            'unfiltered_polymer_count':len(acts),
            'unfiltered_parity_zero_terms_checked':parity,
            'contains_odd_physical_cross_triangle':True,
            'marked_merged_blocks':marked_blocks,
            'marked_replay':marked_data,
            'canonical_k':k,
            'direct_pair_transfer_Hermitian_expectation':expected,
            'polarization_expectation':polarized,
            'filtered_sector_bounds_all_exact':True,
            'filtered_same_tilt_mass_transfer_exact':True,
            'separate_sufficient_family_certificates':sufficient_family_certificates(),
            'interleaved_fermionic_sign_regressions':interleaved_regressions(expected),
            'full_pair_number_mean_at_reference_tilt':moment(direct_poly,r)[1],
            'limits':['small exact full-state/gas replay only',
                      'no asymptotic KP truncation execution',
                      'no ODLRO stability/ground-state/material conclusion']}
    path=Path(__file__).with_name('BLOCK_OBSERVABLE_CHECK.json')
    path.write_text(json.dumps(result,indent=2,default=str)+'\n')
    print(json.dumps(result,indent=2,default=str))


if __name__ == '__main__': main()
