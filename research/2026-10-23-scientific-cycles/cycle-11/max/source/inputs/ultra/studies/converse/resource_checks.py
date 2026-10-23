#!/usr/bin/env python3
"""Exact classical entropy admissions for the NEW pooled initial-record budget."""
from collections import defaultdict
from fractions import Fraction
from itertools import product
from pathlib import Path
import json, math, time


def H(distribution):
    return -sum(float(p)*math.log(float(p)) for p in distribution.values() if p)


def marginal(joint, coords):
    out=defaultdict(Fraction)
    for labels, p in joint.items():
        out[tuple(labels[i] for i in coords)]+=p
    assert sum(out.values())==1
    return out


def run_case(D,L,r,channel):
    joint=defaultdict(Fraction)
    for ks in product(range(1,L+1),repeat=r):
        if channel=="none": zs={0:Fraction(1)}
        elif channel=="full": zs={ks:Fraction(1)}
        elif channel=="sum": zs={sum(ks):Fraction(1)}
        elif channel=="noisy_parity":
            parity=sum(ks)%2
            zs={parity:Fraction(3,4),1-parity:Fraction(1,4)}
        elif channel=="erasure_first":
            zs={0:Fraction(2,3),ks[0]:Fraction(1,3)}
        else: raise ValueError(channel)
        tails=[tuple(product(range(D**2),repeat=L-k)) for k in ks]
        probability=Fraction(1,L**r*D**(2*(r*L-sum(ks))))
        for tailvec in product(*tails):
            ys=tuple((0,)*k+tail for k,tail in zip(ks,tailvec))
            for z,pz in zs.items(): joint[(ks,ys,z)]+=probability*pz
    hk=H(marginal(joint,(0,)))
    hy=H(marginal(joint,(1,)))
    hz=H(marginal(joint,(2,)))
    hky=H(marginal(joint,(0,1)))
    hkz=H(marginal(joint,(0,2)))
    hyz=H(marginal(joint,(1,2)))
    hkyz=H(joint)
    c= hky-hy
    c_given_z=hkyz-hyz
    i_acc=hk+hz-hkz
    b=r*(L+1)*math.log(D)/2
    u=b-math.log(L)*r/2+c/2
    conditional_squash=b-(hkz-hz)/2+c_given_z/2
    spectral_squash=r*L*math.log(D)-(hyz-hz)/2
    assert math.isclose(conditional_squash,spectral_squash,abs_tol=1e-10)
    assert conditional_squash <= u+i_acc/2+1e-10
    assert c_given_z<=c+1e-10
    assert 0<=i_acc+1e-10<=r*math.log(L)+1e-10
    if channel=="none": assert math.isclose(conditional_squash,u,abs_tol=1e-10)
    if channel=="full":
        assert math.isclose(conditional_squash,b,abs_tol=1e-10)
        assert math.isclose(i_acc,r*math.log(L),abs_tol=1e-10)
    return dict(D=D,L=L,r=r,channel=channel,nonzero_joint_cells=len(joint),
                supplied_information_nats=i_acc,
                conditional_squashing_bound_nats=conditional_squash,
                claimed_information_bound_nats=u+i_acc/2,
                supply_bound_nats=b)


if __name__=="__main__":
    start,cpu=time.perf_counter(),time.process_time()
    cases=[run_case(D,L,r,channel) for D,L,r in ((2,2,1),(2,3,1),(2,2,2),(2,3,2),(3,2,2))
           for channel in ("none","full","sum","noisy_parity","erasure_first")]
    result=dict(status="PASS",cases=cases,
                total_nonzero_joint_cells=sum(x["nonzero_joint_cells"] for x in cases),
                wall_seconds=time.perf_counter()-start,cpu_seconds=time.process_time()-cpu)
    (Path(__file__).parent/"RESOURCE_RESULT.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({k:v for k,v in result.items() if k!="cases"}|{"cases":len(cases)}))
