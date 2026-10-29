#!/usr/bin/env python3
"""Compile the EXISTING RX/RZ input into an exact Pauli/clock recipe.

No producer code, matrix diagonalization, new replacement level or dynamics.
All operator qualifications use binary Pauli algebra; scales use integers.
"""
from __future__ import annotations
from collections import Counter
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
from time import perf_counter

BASE = Path(__file__).resolve().parents[2]
SOURCE = BASE/'a_independent'/'complexes'/'level_2.json'
HERE = Path(__file__).resolve().parent


def bits(x):
    while x:
        q=x & -x
        yield q.bit_length()-1
        x^=q


def symp(p,q):
    return ((p[0]&q[1]).bit_count()+(p[1]&q[0]).bit_count())%2


def hx(n):
    return ('-' if n<0 else '')+hex(abs(n))


def frac(x):
    return {'numerator_hex':hx(x.numerator),'denominator_hex':hx(x.denominator)}


def main():
    t0=perf_counter()
    raw=SOURCE.read_bytes()
    inp=json.loads(raw)
    N=inp['n']
    checks=[(int(x),0) for x in inp['xs']]+[(0,int(z)) for z in inp['zs']]
    M=len(checks)
    supports=[p[0]|p[1] for p in checks]
    assert all(supports)
    incidence=[[] for _ in range(N)]
    for c,p in enumerate(supports):
        for i in bits(p):incidence[i].append(c)
    assert max(map(len,incidence))<=7
    assert max(x.bit_count() for x in supports)<=7
    neighbors=[]
    for c,s in enumerate(supports):
        ns=set()
        for i in bits(s):ns.update(incidence[i])
        ns.discard(c)
        neighbors.append(ns)
        assert all(not symp(checks[c],checks[h]) for h in ns)
    assert len(set(checks))==M, 'trace obstruction uses distinct supplied checks'
    # The original code family has positive commuting CSS checks, hence no -I.
    colors=[]
    for c,ns in enumerate(neighbors):
        used={colors[h] for h in ns if h<c}
        k=0
        while k in used:k+=1
        colors.append(k)
    order=sorted(range(M),key=lambda c:(colors[c],c))
    position={c:i for i,c in enumerate(order)}
    L=8
    labels=[]
    prefixes=[]
    for c,(x,z) in enumerate(checks):
        ll=[((1<<i) if (x>>i)&1 else 0,
             (1<<i) if (z>>i)&1 else 0) for i in bits(x|z)]
        assert all((a|b).bit_count()==1 for a,b in ll)
        ll += [(0,0)]*(L-len(ll))
        labels.append(ll)
        pref=[(0,0)]
        for a,b in ll:
            old=pref[-1]
            pref.append((old[0]^a,old[1]^b))
        assert pref[-1]==checks[c]
        prefixes.append(pref[:-1])
    terms=[]
    max_q=0
    gauged_incidence=Counter()
    for c in range(M):
        for j,p in enumerate(labels[c]):
            a=(j+1)%L
            b=j
            own=(prefixes[c][a][0]^p[0]^prefixes[c][b][0],
                 prefixes[c][a][1]^p[1]^prefixes[c][b][1])
            expected=(0,0) if j<L-1 else checks[c]
            assert own==expected
            phases=[]
            for h in sorted(neighbors[c]):
                data=p if position[h]<position[c] else expected
                mask=sum(symp(pref,data)<<r for r,pref in enumerate(prefixes[h]))
                if mask:
                    assert not mask&1, 'other clocks in0 have no prefix sign'
                    phases.append([h,hex(mask)])
            active={c}|{h for h,_ in phases}
            max_q=max(max_q,len(active))
            gauged_incidence.update(active)
            terms.append({
                'clock':c,'from':b,'to':a,
                'original_data_X':hx(p[0]),'original_data_Z':hx(p[1]),
                'gauged_data_check':c if j==L-1 else None,
                'gauged_clock_diagonal_sign_masks':phases,
            })
    # Constants are uniform FAMILY constants, not fitted to the smaller input.
    w=r=7
    B=w*(r-1)
    q=1+B
    J=L*q
    assert max_q<=q and max(gauged_incidence.values())<=J
    D_rho=64*q*J*(L**q)
    rho=F(1,D_rho)
    lam=F(1,12*D_rho**L)
    Delta=F(1,4*lam**L)
    hopping=Delta*lam
    assert lam<=rho/2
    remainder=Delta*3*rho*(lam/rho)**(L+1)/(1-lam/rho)
    gap=1-2*remainder
    assert remainder<=F(1,8) and gap>=F(3,4)
    assert Delta/2>=F(3,4)
    recipe={
        'operator_convention':
            'H=Delta sum_c(I-|0><0|)_c -hopping sum_edges P*(|to><from|+h.c.); padding P=I is one-body',
        'clock_dimension':L,'data_qubits':N,'clock_qudits':M,
        'checks':[{'X':hx(p[0]),'Z':hx(p[1]),'color':colors[c]}
                  for c,p in enumerate(checks)],
        'prefix_gauge_order':order,
        'diagonal_sign_mask_convention':'bit r=1 means minus at clock state r',
        'clock_hops':terms,
        'Delta':frac(Delta),'hopping':frac(hopping),
    }
    recipe_bytes=(json.dumps(recipe,separators=(',',':'))+'\n').encode()
    (HERE/'CLOCK_HAMILTONIAN.json').write_bytes(recipe_bytes)
    result={
        'scope':'Native existing level2 exact recipe; general gap/path theorem separate; no numerical spectrum or trajectory',
        'retained_algebraic_subdivision_ell':3,
        'literal_geometric_embedding':'NOT_ACQUIRED; theorem uses primary-qualified large fixed ell separately',
        'source':str(SOURCE),'source_sha256':hashlib.sha256(raw).hexdigest(),
        'data_qubits':N,'supplied_checks':M,'clock_qudits':M,
        'clock_dimension':L,'original_at_most_two_body_hopping_terms':len(terms),
        'onsite_clock_penalties':M,
        'input_max_check_weight':max(x.bit_count() for x in supports),
        'input_max_qubit_incidence':max(map(len,incidence)),
        'exact_gauge_physical_factor_I_or_whole_check':'PASS for every hop',
        'exact_commutation_of_all_source_checks':'PASS',
        'actual_check_colors':max(colors)+1,
        'prefix_gauge_two_body_circuit_depth_upper':w*(max(colors)+1),
        'actual_max_gauged_clock_support':max_q,
        'actual_max_gauged_clock_incidence':max(gauged_incidence.values()),
        'uniform_family_q':q,'uniform_family_J':J,
        'rho':frac(rho),'lambda':frac(lam),'Delta':frac(Delta),'hopping':frac(hopping),
        'penalty_numerator_bits':Delta.numerator.bit_length(),
        'penalty_denominator_bits':Delta.denominator.bit_length(),
        'normalized_incidence_remainder_bound':frac(remainder),
        'normalized_syndrome_gap_bound':frac(gap),
        'universal_gap_lower':'3/4',
        'arbitrary_physical_perturbation_stability':'NOT_ACQUIRED',
        'full_tensor_Yin_Lucas_small_error':'NOT_ACQUIRED; trace obstruction for symmetry-preserving dressing',
        'two_body_QUBIT_implementation':'NOT_ACQUIRED',
        'recipe_bytes':len(recipe_bytes),
        'recipe_sha256':hashlib.sha256(recipe_bytes).hexdigest(),
        'elapsed_seconds':perf_counter()-t0,
    }
    (HERE/'CLOCK_RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('data_qubits','clock_qudits',
          'original_at_most_two_body_hopping_terms','actual_max_gauged_clock_support',
          'actual_max_gauged_clock_incidence','penalty_numerator_bits',
          'universal_gap_lower','elapsed_seconds')}))


if __name__=='__main__':main()
