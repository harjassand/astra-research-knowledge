#!/usr/bin/env python3
"""Exact population check of preparation plus every depth-three binary policy.

This is a rational native model construction, not acquired sample data. A frozen
hidden bit couples weakly to a visible bit. Two past visible labels are retained;
eight actual biased kernel calls precede three adaptive service calls. All 128
deterministic service trees are enumerated separately at each retained history.
"""
from fractions import Fraction as F
from pathlib import Path
from itertools import product
import hashlib
import json


def mm(a, b):
    return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]


def dot(a,b):
    return sum(x*y for x,y in zip(a,b))


def apply(row, kernel):
    return mm([row],kernel)[0]


def expect(kernel, f):
    return [dot(row,f) for row in kernel]


def main():
    states=list(product((-1,1),repeat=2))
    coupling=F(1,100)
    beta=F(1,3)
    retention=F(1,2)
    pi=[(1+coupling*h*y)/4 for h,y in states]
    mu=[p*(1+beta*y) for p,(_,y) in zip(pi,states)]
    assert sum(pi)==sum(mu)==1
    yfun=[F(y) for h,y in states]

    def kernel(bias):
        ans=[]
        for i,(h,y) in enumerate(states):
            mean=(bias+coupling*h)/(1+bias*coupling*h)
            ans.append([F(0) if hh!=h else
                retention*F(i==j)+(1-retention)*(1+yy*mean)/2
                for j,(hh,yy) in enumerate(states)])
        invariant=[p*(1+bias*y) for p,(_,y) in zip(pi,states)]
        assert apply(invariant,ans)==invariant
        for i in range(4):
            assert sum(ans[i])==1 and min(ans[i])>=0
            for j in range(4):
                assert invariant[i]*ans[i][j]==invariant[j]*ans[j][i]
                if states[i][0]!=states[j][0]:
                    assert ans[i][j]==0
        return ans

    base=kernel(F(0))
    service=[kernel(-beta),kernel(beta)]
    reset=service[1]

    def project(f):
        means={y:sum(p*v for p,v,(_,yy) in zip(mu,f,states) if yy==y)
                 /sum(p for p,(_,yy) in zip(mu,states) if yy==y)
               for y in (-1,1)}
        return [means[y] for h,y in states]

    centered=[y-beta for y in yfun]
    variance=dot(mu,[v*v for v in centered])
    assert variance==1-beta*beta
    residual_squared=[]
    for call in service:
        ty=expect(call,yfun)
        pty=project(ty)
        e2=dot(mu,[(a-b)**2 for a,b in zip(ty,pty)])/variance
        assert e2<F(1,200)**2
        residual_squared.append(e2)
    bcenter=project(expect(reset,centered))
    kappa=dot(mu,[a*b for a,b in zip(centered,bcenter)])/variance
    assert F(0)<kappa<F(51,100)
    assert all(a==kappa*b for a,b in zip(bcenter,centered))

    # Actual previous record: baseline call/read twice, with no hidden read.
    histories={():pi}
    for _ in range(2):
        new={}
        for history,row in histories.items():
            evolved=apply(row,base)
            for y in (-1,1):
                new[history+(y,)]=[p if yy==y else F(0)
                                  for p,(_,yy) in zip(evolved,states)]
        histories=new
    assert [sum(row[i] for row in histories.values()) for i in range(4)]==pi
    B=1/(1-beta)
    M=len(histories)
    Kjoint2=sum(sum(h*h/p for h,p in zip(row,mu))/sum(row)
                for row in histories.values())
    assert Kjoint2<=B*M==6

    reset_calls=8
    prepared={}
    for history,row in histories.items():
        for _ in range(reset_calls):
            row=apply(row,reset)
        prepared[history]=row

    def law(row, policy, depth=0, node=0):
        if depth==3:
            return [sum(row)]
        out=[]
        evolved=apply(row,service[(policy>>node)&1])
        for branch,y in enumerate((-1,1)):
            selected=[p if yy==y else F(0) for p,(_,yy) in zip(evolved,states)]
            out.extend(law(selected,policy,depth+1,2*node+1+branch))
        return out

    # Every complete depth-three policy tree: seven binary actuator decisions.
    worst_joint_tv=F(0)
    maximizers=[]
    for history,original_row in histories.items():
        pz=sum(original_row)
        reference=[pz*p for p in mu]
        worst=F(-1)
        argmax=None
        for policy in range(128):
            actual_law=law(prepared[history],policy)
            target_law=law(reference,policy)
            assert sum(actual_law)==sum(target_law)==pz
            tv=sum(abs(a-b) for a,b in zip(actual_law,target_law))/2
            if tv>worst:
                worst,argmax=tv,policy
        worst_joint_tv+=worst
        maximizers.append({'old_visible_history':list(history),'policy_mask':argmax,
                           'joint_tv_contribution':str(worst)})

    # Exact conservative receiving theorem, no floating spectral estimates.
    kappa_upper=F(51,100)
    leak_upper=F(1,200)
    b_m=kappa_upper**reset_calls+leak_upper*sum(
        kappa_upper**j for j in range(reset_calls))
    # Gamma<=2; Gamma sqrt(2)<3. Three future observations give 1+3+9.
    eta_service=leak_upper*F(13,2)
    # sqrt(K_joint^2-1)<=sqrt(5)<9/4.
    certified_tv_upper=F(9,4)*(b_m/2+eta_service)
    assert worst_joint_tv<=certified_tv_upper<F(1,10)

    proof=Path(__file__).parents[1]/'FINITE_ERROR_PREDICTIVE_PREPARATION.md'
    out={
        'status':'PASS',
        'scope':'Exact population/model check; no sample acquisition, instrument calibration or physical execution.',
        'proof_sha256':hashlib.sha256(proof.read_bytes()).hexdigest(),
        'hidden_state_count':4,'hidden_bit_frozen':True,
        'coupling':str(coupling),'bias':str(beta),
        'retained_old_record':'two baseline visible labels; four possible records',
        'preparation_calls':reset_calls,'future_visible_calls':3,
        'policies_per_old_record':128,'policies_enumerated':512,
        'source_target_density_cap':str(B),'record_value_count':M,
        'actual_joint_density_norm_squared':str(Kjoint2),
        'constructed_joint_density_norm_squared_upper':str(B*M),
        'true_centered_contraction':str(kappa),
        'true_service_leakage_squared':list(map(str,residual_squared)),
        'certified_contraction_upper':str(kappa_upper),
        'certified_leakage_upper':str(leak_upper),
        'uniform_complete_record_tv_upper':str(certified_tv_upper),
        'uniform_complete_record_tv_upper_decimal':float(certified_tv_upper),
        'exact_max_complete_record_tv':str(worst_joint_tv),
        'exact_max_complete_record_tv_decimal':float(worst_joint_tv),
        'maximizing_service_trees':maximizers,
        'cost_scope':'Retained records, preparation calls and all service observations included. Finite-sample/clock/sensor errors need the existing acquisition schedule; none was executed here.'
    }
    output=Path(__file__).with_name('COMPLETE_PREPARATION_PROGRAM_EXACT_RESULTS.json')
    output.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({key:out[key] for key in [
        'status','policies_enumerated','uniform_complete_record_tv_upper_decimal',
        'exact_max_complete_record_tv_decimal','hidden_bit_frozen']},indent=2))


if __name__=='__main__':
    main()
