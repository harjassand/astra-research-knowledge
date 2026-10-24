#!/usr/bin/env python3
"""Finite exact-structure checks for the doped projected-pairing construction.

This enumerates small REAL rational fixtures. It is not an implementation of
the asymptotic KP evaluator, a general sampler, or a materials calculation.
"""
from collections import defaultdict
from fractions import Fraction as Q
from functools import lru_cache
from itertools import combinations
import cmath
import json
from math import comb, pi
from pathlib import Path


def partial_matchings(f, sites):
    sites = tuple(sorted(sites))
    if not sites:
        yield ()
        return
    i = sites[0]
    yield from partial_matchings(f, sites[1:])
    for j in sites[1:]:
        if f[i][j]:
            for rest in partial_matchings(f, tuple(v for v in sites if v not in (i, j))):
                yield ((i, j),) + rest


def create(mask, index):
    if mask >> index & 1:
        return None
    return mask | (1 << index), (-1) ** ((mask & ((1 << index)-1)).bit_count())


def annihilate(mask, index):
    if not mask >> index & 1:
        return None
    return mask ^ (1 << index), (-1) ** ((mask & ((1 << index)-1)).bit_count())


def bond_create(state, edge):
    i, j = edge
    out = defaultdict(Q)
    for mask, value in state.items():
        for a, b, sign in ((2*i, 2*j+1, 1), (2*i+1, 2*j, -1)):
            right = create(mask, b)
            left = create(right[0], a) if right is not None else None
            if left is not None:
                out[left[0]] += value*sign*right[1]*left[1]
    return {a:b for a,b in out.items() if b}


def bond_annihilate(state, edge):
    i, j = edge
    out = defaultdict(Q)
    for mask, value in state.items():
        for a, b, sign in ((2*i, 2*j+1, 1), (2*i+1, 2*j, -1)):
            right = annihilate(mask, a)
            left = annihilate(right[0], b) if right is not None else None
            if left is not None:
                out[left[0]] += value*sign*right[1]*left[1]
    return {a:b for a,b in out.items() if b}


@lru_cache(None)
def bond_state(matching):
    out = {0:Q(1)}
    for edge in matching:
        out = bond_create(out, edge)
    assert sum(value*value for value in out.values()) == 2**len(matching)
    return out


def inner(a, b):
    return sum((value*b.get(mask, Q(0)) for mask,value in a.items()), Q(0))


def weight(f, matching):
    out = Q(1)
    for i,j in matching:
        out *= f[i][j]
    return out


def occupied(matching):
    return sum(1 << i for edge in matching for i in edge)


def full_state(f):
    out = defaultdict(Q)
    for matching in partial_matchings(f, range(len(f))):
        value = weight(f, matching)
        for mask, amplitude in bond_state(matching).items():
            out[mask] += value*amplitude
    return {a:b for a,b in out.items() if b}


def coefficients(state, m):
    out = [Q(0)]*(m+1)
    for mask,value in state.items():
        assert mask.bit_count()%2 == 0
        out[mask.bit_count()//2] += value*value
    return out


def poly_add(a,b):
    out = [Q(0)]*max(len(a),len(b))
    for i,v in enumerate(a): out[i] += v
    for i,v in enumerate(b): out[i] += v
    return out


def poly_mul(a,b):
    out = [Q(0)]*(len(a)+len(b)-1)
    for i,v in enumerate(a):
        for j,w in enumerate(b): out[i+j] += v*w
    return out


def connected(active, edges):
    if not active:
        return False
    start = min(active)
    seen, queue = {start}, [start]
    for v in queue:
        for i,j in edges:
            if v == i and j not in seen: seen.add(j); queue.append(j)
            if v == j and i not in seen: seen.add(i); queue.append(i)
    return seen == active


def activities(f, reference):
    m = len(reference)
    owner = {i:a for a,edge in enumerate(reference) for i in edge}
    refs = set(reference)
    answer = {}
    min_excess = None
    for support in range(1,1 << m):
        cells = {a for a in range(m) if support >> a & 1}
        if len(cells)<2:
            continue
        sites = [i for a in cells for i in reference[a]]
        grouped = defaultdict(list)
        for matching in partial_matchings(f, sites):
            grouped[occupied(matching)].append(matching)
        polynomial = [Q(0)]*(len(cells)+1)
        for same_occupied in grouped.values():
            for left in same_occupied:
                for right in same_occupied:
                    weak = [edge for edge in left+right if edge not in refs]
                    active = {owner[i] for edge in weak for i in edge}
                    adjacency = [(owner[i], owner[j]) for i,j in weak]
                    if active != cells or not connected(active, adjacency):
                        continue
                    assert len(weak) >= len(cells)
                    excess = len(weak)-len(cells)
                    min_excess = excess if min_excess is None else min(min_excess,excess)
                    polynomial[len(left)] += (weight(f,left)*weight(f,right)
                                             *inner(bond_state(left),bond_state(right)))
        if any(polynomial):
            answer[support] = polynomial
    return answer, min_excess


def gas(acts, m):
    @lru_cache(None)
    def calc(support):
        if support == 0:
            return [Q(1)]
        bit = support & -support
        out = poly_mul([Q(1),Q(2)],calc(support ^ bit))
        for component,activity in acts.items():
            if component & bit and component & support == component:
                out = poly_add(out,poly_mul(activity,calc(support ^ component)))
        return out
    return calc((1 << m)-1)


def evaluate(poly,z):
    return sum(float(v)*z**i for i,v in enumerate(poly))


def pair_transfer(state, reference, a, b, k):
    sector = {mask:v for mask,v in state.items() if mask.bit_count() == 2*k}
    changed = bond_create(bond_annihilate(sector,reference[b]),reference[a])
    changed = {mask:v/Q(2) for mask,v in changed.items()
               if all(((mask >> (2*i)) & 3) != 3 for i in range(2*len(reference)))}
    return inner(sector,changed)/inner(sector,sector)


def determinant(a):
    n = len(a)
    b = [list(row) for row in a]
    value = Q(1)
    for j in range(n):
        pivot = next((i for i in range(j,n) if b[i][j]),None)
        if pivot is None: return Q(0)
        if pivot != j:
            b[j],b[pivot] = b[pivot],b[j]; value = -value
        p = b[j][j]; value *= p
        for i in range(j+1,n):
            factor = b[i][j]/p
            for l in range(j+1,n): b[i][l] -= factor*b[j][l]
    return value


def matmul(a,b):
    return [[sum((u*v for u,v in zip(row,column)),Q(0))
             for column in zip(*b)] for row in a]


def charpoly(a):
    n = len(a)
    b = [[Q(i == j) for j in range(n)] for i in range(n)]
    high = [Q(1)]
    for k in range(1,n+1):
        b = matmul(a,b)
        c = -sum((b[i][i] for i in range(n)),Q(0))/k
        high.append(c)
        for i in range(n): b[i][i] += c
    return list(reversed(high))


def chiral_identity():
    n = 4
    f = [[Q(v,7) for v in row] for row in
         ((1,2,-1,0),(3,-2,1,4),(0,2,1,-3),(-1,0,2,1))]
    charges = [Q(0)]*(n//2+1)
    for k in range(n//2+1):
        for rows in combinations(range(n),k):
            for cols in combinations(range(n),k):
                if set(rows).isdisjoint(cols):
                    charges[k] += determinant([[f[i][j] for j in cols] for i in rows])**2
    h = [[Q(0)]*(2*n) for _ in range(2*n)]
    for i in range(n):
        for j in range(n): h[i][n+j] = h[n+j][i] = 2*f[i][j]
    averaged = [Q(0)]*(n+1)
    for selected in range(1 << n):
        inds = [i if selected >> i & 1 else n+i for i in range(n)]
        p = charpoly([[h[i][j] for j in inds] for i in inds])
        averaged = [a+b/Q(2**n) for a,b in zip(averaged,p)]
    target = [Q(0)]*(n+1)
    for k,v in enumerate(charges): target[n-2*k] = (-1)**k*v
    assert averaged == target
    return {'coefficients':charges,'characteristic_average':averaged,
            'identity_exact':True,'scope':'real rational n=4; general proof in note'}


def fixture(strength):
    m = 4; n = 2*m
    reference = tuple((2*a,2*a+1) for a in range(m))
    f = [[Q(0)]*n for _ in range(n)]
    for i,j in reference: f[i][j] = f[j][i] = Q(1)
    for i,j,mult in ((0,2,1),(2,4,-1),(0,4,1),(1,3,1),
                     (3,5,1),(1,5,-1),(4,6,1),(5,7,-1)):
        f[i][j] = f[j][i] = strength*mult
    wave = full_state(f)
    direct = coefficients(wave,m)
    acts,weak_excess = activities(f,reference)
    contracted = gas(acts,m)
    assert direct == contracted
    r = Q(1,2); nodes = 8
    values = [evaluate(direct,float(r)*cmath.exp(2j*pi*j/nodes)) for j in range(nodes)]
    dft = [sum(values[j]*cmath.exp(-2j*pi*k*j/nodes) for j in range(nodes))/nodes
           /float(r)**k for k in range(m+1)]
    error = max(abs(complex(float(v))-value) for v,value in zip(direct,dft))
    assert error < 1e-10
    delta = Q(1,4); physical_degree = 3; dimer_degree = 3
    r_hi = (2-delta)/(2*delta); R = 2*r_hi
    a = 2*(physical_degree+2)**4*max(Q(1),R)*strength
    x = 8*dimer_degree*3**5*a
    S = x*x/(4*dimer_degree*(1-x)) if x<1 else None
    certificate = (strength<=1 and x<=Q(1,4) and S<=delta/4096
                   and (dimer_degree+1)*a<=delta/16)
    return {'lambda':strength,'norm_coefficients':direct,'polymer_count':len(acts),
            'min_weak_edge_power_minus_active_size':weak_excess,
            'partial_matching_gas_exact':True,
            'contains_physical_pairing_triangle':True,
            'DFT_at_half_density_error':error,
            'Z_at_reference_zero_minus_half':sum(v*(-r)**k for k,v in enumerate(direct)),
            'pair_transfer_0_3_at_k2':pair_transfer(wave,reference,0,3,2),
            'certificate':certificate,'certificate_a':a,'certificate_x':x,
            'certificate_S':S,
            'scope':'full-state enumeration, not execution of asymptotic KP FPTAS'}


def gauge_counterexample():
    f=[[Q(0)]*4 for _ in range(4)]
    f[0][1]=f[1][0]=f[2][3]=f[3][2]=Q(1)
    native=full_state(f)
    f[0][1]=f[1][0]=Q(2)  # Exactly DFD with D_0=2 and other D_i=1.
    changed=full_state(f)
    def first_pair_probability(state):
        sector={mask:v for mask,v in state.items() if mask.bit_count()==2}
        total=inner(sector,sector)
        first=sum((v*v for mask,v in sector.items() if mask & 0b1111),Q(0))
        return total,first/total
    z,p=first_pair_probability(native)
    z_changed,p_changed=first_pair_probability(changed)
    assert (z,p,z_changed,p_changed)==(Q(4),Q(1,2),Q(10),Q(4,5))
    return {'two_dimers_k1_native_first_pair_probability':p,
            'after_D0_equals2_probability':p_changed,
            'norms_native_and_DFD':[z,z_changed],
            'conclusion':'occupation filter required; no free DFD state gauge'}


def main():
    m = 4
    reference = tuple((2*a,2*a+1) for a in range(m))
    f = [[Q(0)]*(2*m) for _ in range(2*m)]
    for i,j in reference: f[i][j] = f[j][i] = Q(1)
    wave = full_state(f)
    assert coefficients(wave,m) == [Q(comb(m,k)*2**k) for k in range(m+1)]
    dicke = {}
    for k in range(1,m):
        expected = Q(k*(m-k),m*(m-1))
        observed = pair_transfer(wave,reference,0,3,k)
        assert observed == expected
        dicke[k] = observed
    result = {'status':'PASS finite exact-structure replay',
              'reference_canonical_pair_coherence':dicke,
              'hard_charge_chiral_identity':chiral_identity(),
              'visible_uncertified_fixture':fixture(Q(1,20)),
              'small_certified_fixture':fixture(Q(1,10**12)),
              'finite_hole_gauge_counterexample':gauge_counterexample(),
              'limits':['real rational small fixtures only',
                        'DFT is floating point; gas/sign identities exact fractions',
                        'small m uses exact fallback in proved algorithm',
                        'no generic sampler, ground-state or hardware inference']}
    output = Path(__file__).with_name('CANONICAL_CHECK.json')
    output.write_text(json.dumps(result,indent=2,default=str)+'\n')
    print(json.dumps(result,indent=2,default=str))


if __name__ == '__main__': main()
