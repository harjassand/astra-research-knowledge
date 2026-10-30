#!/usr/bin/env python3
"""Discriminating checks, separate from the constructive run.

Rebuild confidence from instrument records only; test stopped coverage across
different passive memory rates; check the global ridge-map perturbation bound.
These finite checks supplement the proof and do not prove calibration/priority.
"""
import json
import math
from pathlib import Path

import numpy as np

from causal_clipped_identification import (
    confidence_record, deadline_bound, rotation, jsonable,
)

OUT = Path(__file__).resolve().parent


def replay_instrument_record(name, expected):
    data = np.load(OUT / f"{name}_record.npz")
    reports = data["reports"]
    m = (reports.shape[1]-2)//2
    d = m
    counts = np.zeros(d, dtype=int)
    Z, V = np.zeros((m,d)), np.zeros((m,d))
    W = np.zeros((m,d), dtype=int)
    for row in reports:
        j, sign = int(row[0]), row[1]
        q, warning = row[2:2+m], row[2+m:]
        z = sign*q/float(data["r"])
        counts[j] += 1
        Z[:,j] += z
        V[:,j] += z*z
        W[:,j] += warning.astype(int)
    cert = confidence_record(counts,Z,V,W,C=float(data["C"]),r=float(data["r"]),
                             L=float(data["L"]),delta=float(data["delta"]))
    previous = expected["controller"]["confidence"]
    errors = {key:float(np.max(np.abs(np.asarray(cert[key])-np.asarray(previous[key]))))
              for key in ["center","lower","upper","entry_radii","operator_error_bound"]}
    assert max(errors.values()) < 1e-12
    return {"instrument_windows":len(reports), "maximum_recomputed_certificate_difference":max(errors.values()),
            "population_matrix_or_state_inputs":0}


def ridge_check():
    rng = np.random.default_rng(19683)
    lam = .5
    worst_ratio = 0.0
    for i in range(1000):
        m, d = 2+(i%3), 2+(i%4)
        A = rng.normal(size=(m,d))*10**rng.uniform(-4,1)
        B = A+rng.normal(size=(m,d))*10**rng.uniform(-5,1)
        KA = np.linalg.solve(A.T@A+lam*np.eye(d),A.T)
        KB = np.linalg.solve(B.T@B+lam*np.eye(d),B.T)
        ratio = lam*np.linalg.norm(KA-KB,2)/np.linalg.norm(A-B,2)
        worst_ratio = max(worst_ratio,float(ratio))
    # The sharp constant is approached for one-dimensional near-zero maps.
    e = 1e-7
    sharp_ratio = lam*(e/(e*e+lam))/e
    assert worst_ratio <= 1+1e-10
    assert sharp_ratio > .999999
    return {"random_matrix_pairs":1000,"largest_ratio_to_proved_bound":worst_ratio,
            "near_zero_scalar_ratio":sharp_ratio}


def stopped_coverage_check(replicas=256, max_per_column=8192):
    """Vectorized independent specimens, no resets within each trajectory."""
    rng = np.random.default_rng(314159265)
    m=d=2
    r,C,levels,delta=.054,.8,257,.01
    step=2*C/(levels-1)
    # A grid includes fast, oscillatory, very long memory, and mixtures.
    rate_pairs = np.array([[-.99,.99999],[-.1,.9999],[.5,.99999],[.98,.9999]])
    rho = rate_pairs[np.arange(replicas)%len(rate_pairs)]
    tau = np.sqrt(1-rho*rho)
    U,Vout = rotation(.31),rotation(-.47)
    state = np.tile([8.,-4.],(replicas,1))
    A = -np.einsum("ab,rb,bc->rac",Vout,rho,U)
    Z=np.zeros((replicas,m,d)); V=np.zeros_like(Z)
    W=np.zeros_like(Z,dtype=int)
    ever_missed=np.zeros(replicas,dtype=bool)
    stopped=np.zeros(replicas,dtype=int)
    energy_in=np.zeros(replicas)
    energy_out=np.zeros(replicas)
    largest_balance_error=0.0
    for t in range(d*max_per_column):
        j=t%d
        signs=2*rng.integers(2,size=replicas)-1
        commands=np.zeros((replicas,d));commands[:,j]=r*signs
        internal=commands@U.T
        y=(tau*state-rho*internal)@Vout.T
        state=rho*state+tau*internal
        energy_in+=r*r
        energy_out+=np.sum(y*y,axis=1)
        balance=np.sum(state*state,axis=1)+9+energy_out-89-energy_in
        largest_balance_error=max(largest_balance_error,float(np.max(np.abs(balance))))
        clipped=np.clip(y,-C,C)
        pos=(clipped+C)/step
        lower=np.floor(pos)
        q=-C+step*(lower+(rng.random(y.shape)<pos-lower))
        z=signs[:,None]*q/r
        Z[:,:,j]+=z;V[:,:,j]+=z*z;W[:,:,j]+=np.abs(y)>C
        if (t+1)%(d*512)==0:
            N=(t+1)//d
            for a in range(replicas):
                cert=confidence_record(np.array([N,N]),Z[a],V[a],W[a],
                                       C=C,r=r,L=1,delta=delta)
                missed=np.any(A[a]<cert["lower"]) or np.any(A[a]>cert["upper"])
                ever_missed[a] |= missed
                if not stopped[a] and .4/.5*cert["operator_error_bound"]<.15:
                    stopped[a]=t+1
                # (10) is a deterministic radius bound, separate from coverage.
                assert cert["operator_error_bound"] <= deadline_bound(N,r)+1e-10
    return {"replicas":replicas,"maximum_windows_per_specimen":d*max_per_column,
            "checkpoints_per_specimen":max_per_column//512,
            "rate_pairs":rate_pairs,"initial_state":[8.,-4.],"unchanged_dark_energy":9,
            "any_checkpoint_confidence_misses":int(ever_missed.sum()),
            "stopped_by_horizon":int(np.count_nonzero(stopped)),
            "minimum_stopping_windows":int(stopped[stopped>0].min()) if np.any(stopped) else None,
            "maximum_stopping_windows":int(stopped.max()),
            "maximum_accumulated_energy_balance_residual":largest_balance_error,
            "interpretation":"Finite coverage diagnostic only; not a substitute for the martingale proof."}


def main():
    results=json.loads((OUT/"RESULTS.json").read_text())
    checks={"instrument_only_replays":{},"ridge_map":ridge_check()}
    for name in ["persistent_mimo_r012","persistent_mimo_designed"]:
        checks["instrument_only_replays"][name]=replay_instrument_record(name,results[name])
    checks["stopped_coverage_diagnostic"]=stopped_coverage_check()
    (OUT/"VERIFICATION.json").write_text(json.dumps(checks,indent=2,default=jsonable)+"\n")
    print(json.dumps(checks,default=jsonable))


if __name__=="__main__":
    main()
