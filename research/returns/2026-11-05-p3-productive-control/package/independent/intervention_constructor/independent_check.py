"""Independent exhaustive verification of the illustrative two-mode model.

The recursion is checked against every stationary deterministic policy by
solving its absorbing-chain linear system. This is mathematical validation,
not validation of any physical interface or of the statistical assumptions.
"""
from itertools import product
import json
import math
import numpy as np

MODES = ((.1, .2, 3.), (.2, .7, 2.))


def check(N):
    ds, policy, previous = [], [], 0.
    for i in range(N):
        scores = [(r+q*previous)/p for p,q,r in MODES]
        a = int(np.argmax(scores))
        previous = scores[a]
        ds.append(previous)
        policy.append(a)
    V = np.cumsum(ds[::-1])[::-1]
    best = np.zeros(N)
    for pi in product(range(len(MODES)), repeat=N):
        P, rewards = np.zeros((N,N)), np.zeros(N)
        for i,a in enumerate(pi):
            p,q,r = MODES[a]
            rewards[i] = r
            P[i,i] += 1-p-q
            P[i,max(0,i-1)] += q
            if i+1<N:
                P[i,i+1] += p
        best = np.maximum(best, np.linalg.solve(np.eye(N)-P, rewards))
    error = float(np.max(np.abs(best/V-1)))
    assert error < 2e-10
    assert np.isclose(V[0],13.6*(3.5**N-1)-4*N)
    assert policy == [0] + [1]*(N-1)
    return {"N":N,"policies_checked":2**N,"policy":policy,
            "optimal_work":float(V[0]),"max_relative_error":error}


def value(N,q):
    rho=q/.2
    return (30+10/(rho-1))*(rho**N-1)/(rho-1)-10*N/(rho-1)


def sensitivity(N,h=.2):
    q=.7
    q_alt=q+h/N
    probs=(.2,q,.8-q)
    alternate=(.2,q_alt,.8-q_alt)
    kl=sum(p*math.log(p/z) for p,z in zip(probs,alternate))
    return {"N":N,"perturbation":h/N,
            "relative_mean_change":value(N,q_alt)/value(N,q),
            "one_cycle_KL":kl,"N_squared_times_KL":N*N*kl}


if __name__ == "__main__":
    print(json.dumps({
        "scope":"Mathematical model verification only",
        "exhaustive_checks":[check(N) for N in range(1,9)],
        "forecast_sensitivity":[sensitivity(N) for N in (20,40,80,160)],
        "limiting_relative_mean_change":math.exp(.2/.7),
    },indent=2))
