#!/usr/bin/env python3
"""Finite exact tests of FILTERED_INNOVATION_FT, not a device/threshold test.

All finite-source moments and all five-location marked identities are rational.
The analytic joint-MGF theorem is proved separately in the accompanying note.
"""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import json

from check_gaussian_envelope import G, eye, zeros, add, sub, scale, mul, adj


def circuit(ops):
    answer = eye(2)
    for operation in ops:
        answer = mul(operation, answer)
    return answer


def cayley_pauli(p, t):
    # (I-itP)/(I+itP), P^2=I. ||U-I||^2=4t^2/(1+t^2).
    return add(scale(eye(2), (1-t*t)/(1+t*t)),
               scale(p, G(Q(0), -2*t/(1+t*t))))


def main():
    slots = 5
    h = (Q(1), Q(1,2), Q(-1,4))
    innovation = Q(1,100)
    sigma2 = innovation**2
    r_proxy = sigma2 * sum(map(abs,h))**2
    v_proxy = sigma2 * sum((x*x for x in h), Q(0))
    # sqrt(e)>3/2: this rational envelope is larger than the theorem constant.
    q2_upper = Q(4,3)*(r_proxy+v_proxy)
    moments = {mask:Q(0) for mask in range(1,1<<slots)}
    covariance01 = Q(0)
    realizations = 0
    example_angles = None
    for signs in product((-1,1), repeat=slots+len(h)-1):
        eta = {t:innovation*signs[t+len(h)-1]
               for t in range(1-len(h), slots)}
        theta = [sum((h[j]*eta[t-j] for j in range(len(h))),Q(0))
                 for t in range(slots)]
        for mask in moments:
            value=Q(1)
            for t in range(slots):
                if mask>>t&1:
                    value *= theta[t]**2
            moments[mask] += value
        covariance01 += theta[0]*theta[1]
        realizations += 1
        if example_angles is None:
            example_angles = theta
    moments = {mask:moment/realizations for mask,moment in moments.items()}
    covariance01 /= realizations
    assert covariance01 == Q(3,8)*sigma2 and covariance01 != 0
    for mask,moment in moments.items():
        assert moment <= q2_upper**mask.bit_count(), (mask,moment)

    ident = eye(2)
    pauli_x = [[G.of(0),G.of(1)],[G.of(1),G.of(0)]]
    pauli_z = [[G.of(1),G.of(0)],[G.of(0),G.of(-1)]]
    ideals = [cayley_pauli(pauli_x if t%2 else pauli_z,Q(t+1,7))
              for t in range(slots)]
    noisy=[]
    faults=[]
    for t,theta in enumerate(example_angles):
        axis=pauli_z if t%2 else pauli_x
        error=cayley_pauli(axis,theta/2)
        actual=mul(error,ideals[t])
        fault=sub(actual,ideals[t])
        assert mul(adj(actual),actual)==ident
        assert mul(adj(ideals[t]),ideals[t])==ident
        exact_strength=theta**2/(1+theta**2/4)
        assert mul(adj(fault),fault)==scale(ident,exact_strength)
        assert exact_strength<=theta**2
        noisy.append(actual)
        faults.append(fault)
    assert mul(ideals[0],ideals[1]) != mul(ideals[1],ideals[0])
    paths={mask:circuit([faults[t] if mask>>t&1 else ideals[t]
                         for t in range(slots)])
           for mask in range(1<<slots)}
    identity_count=0
    for selected in range(1,1<<slots):
        expanded=zeros(2)
        for mask,path in paths.items():
            if mask&selected==selected:
                expanded=add(expanded,path)
        factor=circuit([faults[t] if selected>>t&1 else noisy[t]
                        for t in range(slots)])
        assert expanded==factor
        identity_count+=1

    output={
        'scope':'exact finite correlated-source moments and full marked circuit identities only; no physical data or all-size numerical threshold assertion',
        'slots':slots,
        'independent_fresh_innovations':slots+len(h)-1,
        'innovation_realizations':realizations,
        'filter':[str(x) for x in h],
        'R':str(r_proxy),
        'V':str(v_proxy),
        'rational_upper_for_epsilon_squared':str(q2_upper),
        'nonzero_neighbor_angle_covariance':str(covariance01),
        'marked_sets_moment_checked':len(moments),
        'marked_sets_full_factorization_checked':identity_count,
        'all_unmarked_actual_unitaries_retained':True,
        'ideal_controls_noncommuting':True,
        'locationwise_lipschitz_bound_checked_exactly':True,
        'max_moment_ratio_to_rational_bound':str(max(
            moment/q2_upper**mask.bit_count() for mask,moment in moments.items())),
        'moments':[{ 'marked_slots':[t for t in range(slots) if mask>>t&1],
                     'moment':str(moment),
                     'upper':str(q2_upper**mask.bit_count())}
                    for mask,moment in moments.items()],
        'status':'PASS'
    }
    path=Path(__file__).with_suffix('.json')
    path.write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({k:v for k,v in output.items() if k!='moments'},indent=2))


if __name__=='__main__':
    main()
