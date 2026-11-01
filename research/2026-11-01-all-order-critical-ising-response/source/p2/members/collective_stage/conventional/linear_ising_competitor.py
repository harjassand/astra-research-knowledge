"""Exact O(n) response for linear observables, zero-field open Ising chain.

Heat-bath refresh clocks can differ arbitrarily. The linear spin span is
invariant, and its Dirichlet matrix is diagonal. Thus chi=sum_i (C a)_i^2 /
(nu_i E Var(sigma_i | all others)); C a is acquired by two transfer recurrences.
This is a conventional closure, not a solution after kinetic modulation.
"""
import json
import math
from pathlib import Path
import time

import numpy as np
import scipy.linalg as la


def response(couplings, clocks, a):
    couplings, clocks, a = map(np.asarray, (couplings, clocks, a))
    n = len(clocks)
    t = np.tanh(couplings)
    left, right = a.copy(), a.copy()
    for i in range(1, n):
        left[i] += t[i-1]*left[i-1]
    for i in range(n-2, -1, -1):
        right[i] += t[i]*right[i+1]
    Ca = left + right - a
    v = np.ones(n)
    v[0], v[-1] = 1-t[0]**2, 1-t[-1]**2
    for i in range(1, n-1):
        plus = math.tanh(couplings[i-1]+couplings[i])
        minus = math.tanh(couplings[i-1]-couplings[i])
        alpha, beta = (plus+minus)/2, (plus-minus)/2
        v[i] = 1-alpha*alpha-beta*beta-2*alpha*beta*t[i-1]*t[i]
    return float(np.sum(Ca*Ca/(clocks*v)))


def full_check(couplings, clocks, a):
    n, N = len(clocks), 1 << len(clocks)
    states = np.arange(N)
    spins = 1-2*((states[:, None] >> np.arange(n))&1)
    p = np.exp(np.sum(couplings[None, :]*spins[:, :-1]*spins[:, 1:], axis=1))
    p /= np.sum(p)
    K = np.zeros((N, N))
    for x in range(N):
        for i in range(n):
            y = x ^ (1 << i)
            rate = clocks[i]*p[y]/(p[x]+p[y])
            K[x, x] += rate; K[x, y] -= rate
    f = spins @ a
    # Add mean projection to remove null space exactly at the mathematical level.
    u = la.solve(K+np.ones((N, 1))*p[None, :], f)
    return {"response": float(np.dot(p*f, u)),
            "relative_residual": float(np.linalg.norm(K @ u-f)/np.linalg.norm(f))}


def main():
    rows=[]
    for n, decades in [(8, 4), (256, 12), (65536, 12)]:
        couplings = .7+.2*np.cos(np.arange(n-1)*.63)
        clocks = 10.**(-decades*((17*np.arange(n))%n)/max(n-1,1))
        a = np.ones(n)/math.sqrt(n)
        tic=time.perf_counter()
        chi=response(couplings,clocks,a)
        row={"n":n,"clock_decades":decades,"response":chi,
             "seconds":time.perf_counter()-tic,"method":"exact linear closure, two transfer recurrences"}
        if n<=8:
            row["full_state_check"]=full_check(couplings,clocks,a)
        rows.append(row)
    Path(__file__).with_name("linear_ising_results.json").write_text(json.dumps(rows,indent=2)+"\n")
    print(json.dumps(rows,indent=2))


if __name__=="__main__":
    main()
