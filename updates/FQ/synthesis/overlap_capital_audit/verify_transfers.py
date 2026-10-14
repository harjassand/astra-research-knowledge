#!/usr/bin/env python3
"""Exact finite checks for the overlap audit's explicit new constructions.

These checks establish arithmetic and finite examples. They do not independently
validate analytic source theorems, universal claims, historical novelty, or
physical acquisition. No source package is imported or modified.
"""
from fractions import Fraction as Q
from pathlib import Path
import json


def mm(a, b):
    return [[sum((a[i][k]*b[k][j] for k in range(len(b))), Q(0))
             for j in range(len(b[0]))] for i in range(len(a))]


def kron(a, b):
    return [[x*y for x in rowa for y in rowb] for rowa in a for rowb in b]


def eye(n):
    return [[Q(i == j) for j in range(n)] for i in range(n)]


def tr(a):
    return sum((a[i][i] for i in range(len(a))), Q(0))


def partial_e(a, da=4, de=2):
    return [[sum((a[i*de+k][j*de+k] for k in range(de)), Q(0))
             for j in range(da)] for i in range(da)]


def fstar_ramp():
    # Fstar(diag(1,x)); definitions are those of FE, not a normalized surrogate.
    co = [Q(1), -Q(29, 10), Q(7, 2), -Q(29, 10), Q(1)]
    at_i = sum(co)
    linear_unit_action = sum(c/Q(i+1) for i, c in enumerate(co))
    assert at_i == -Q(3, 10)
    assert linear_unit_action == Q(23, 120)
    eps = Q(1, 2)
    ramp_action = eps**4 * linear_unit_action
    exponential_action = at_i * (1-eps**4)/4
    total_action = ramp_action + exponential_action
    assert total_action == -Q(7, 120)
    norm_ramp = eps**4 * (1 + Q(2, 3) + Q(1, 5))
    norm_exponential = 1-eps**4
    total_norm = norm_ramp + norm_exponential
    assert total_norm == Q(253, 240)
    eta = Q(1, 36000)
    bridge_lower_constant = -2*total_action + 2*eta*total_norm
    assert bridge_lower_constant == Q(504253, 4320000)
    assert 4*(1-Q(3, 4))-1 == 0
    return dict(fstar_at_identity=str(at_i), linear_ramp_unit_action=str(linear_unit_action),
                entry_action=str(total_action), entry_norm4_energy=str(total_norm),
                bridge_lower_constant_if_FE_margin_valid=str(bridge_lower_constant),
                additional_bridge_term="E_bridge/36000", critical_trace_exponent="3/4")


def explicit_response_current():
    cases=[]
    for m in (2, 3, 5, 8, 25):
        flux=[Q(1,i) for i in range(1,m)] + [Q(1,m)]
        source=[Q(0)]*m
        for i in range(1,m):
            source[i-1] += flux[i-1]
            source[i] -= Q(i,i+1)*flux[i-1]
        source[-1] += flux[-1]
        assert source == [Q(1)] + [Q(0)]*(m-1)
        for e in (Q(1,10**6), Q(1,3), Q(2)):
            energy=sum((flux[i-1]**2/Q(i+1,i) for i in range(1,m)),Q(0)) + flux[-1]**2/e
            exact=Q(m-1,m)+1/(m*m*e)
            assert energy==exact
            cases.append(dict(m=m,e=str(e),source_current_energy=str(energy)))
    return dict(cases=cases, interior_flux="f_i=1/i", terminal_flux="f_m=1/m",
                robust_uncertainty_interval="[(m-1)/m+1/(m^2*e_plus),(m-1)/m+1/(m^2*e_minus)]",
                zero_lower_endpoint="unbounded upper response if e_minus=0")


def invisible_bath_reflection():
    bell=[[Q(0) for _ in range(4)] for _ in range(4)]
    for i in (0,3):
        for j in (0,3): bell[i][j]=Q(1,2)
    z0=[[Q(1),Q(0)],[Q(0),Q(0)]]
    flip=[[Q(0),Q(1)],[Q(1),Q(0)]]
    bath_flip=kron(eye(4),flip)
    cz=eye(8)
    for i in range(8):
        if ((i>>1)&1) and (i&1): cz[i][i]=-Q(1)
    effect=mm(mm(cz,kron(bell,eye(2))),cz)
    rho=kron(bell,z0)
    altered=mm(mm(bath_flip,rho),bath_flip)
    assert mm(bath_flip,bath_flip)==eye(8)
    assert partial_e(rho)==partial_e(altered)==bell
    scores=(tr(mm(effect,rho)),tr(mm(effect,altered)))
    assert scores==(Q(1),Q(0))
    conditional_effect=[[sum((bell[a][b]*effect[b*2+e][a*2+f]
                                      for a in range(4) for b in range(4)),Q(0))
                         for f in range(2)] for e in range(2)]
    assert conditional_effect==[[Q(1),Q(0)],[Q(0),Q(0)]]
    return dict(ideal_score=str(scores[0]),hidden_bath_score=str(scores[1]),
                reduced_data_reference_identical=True,bath_reflection_square_identity=True,
                conditional_effect_eigenvalues=["1","0"],sharp_score_spoof_radius="1")


if __name__ == '__main__':
    result=dict(status="PASS",scope="exact arithmetic and finite witnesses only",
                fstar_open_strips=fstar_ramp(), response_current=explicit_response_current(),
                invisible_bath=invisible_bath_reflection(),historical_novelty="UNKNOWN",
                independent_correctness="UNKNOWN",physical_capability="NOT_ESTABLISHED")
    target=Path(__file__).with_name('transfer_verification.json')
    target.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
