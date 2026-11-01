"""Exact small-state audit of clock-weighted martingale innovation bases.

This probes a proposed preconditioner, not a compact many-body algorithm. It
enumerates every configuration and every basis vector (n <= 9 in defaults).
"""

import json
import math
from pathlib import Path

import numpy as np
import scipy.linalg as la


def matrices(n, J, clocks, order, fields=None):
    N = 1 << n
    states = np.arange(N)
    spins = 1 - 2*((states[:, None] >> np.arange(n)) & 1)
    fields = np.zeros(n) if fields is None else np.asarray(fields)
    logp = J * np.sum(spins[:, :-1] * spins[:, 1:], axis=1) + spins @ fields
    p = np.exp(logp - np.max(logp)); p /= np.sum(p)
    # Full heat-bath K, with site i refreshed at rate clocks[i].
    K = np.zeros((N, N))
    for x in range(N):
        for i in range(n):
            y = x ^ (1 << i)
            rate = clocks[i]*p[y]/(p[x] + p[y])
            K[x, x] += rate
            K[x, y] -= rate
    # Sequential centered, conditionally normalized innovations.
    psi = np.empty((N, n))
    prefix = np.zeros(N, dtype=np.int64)
    for k, i in enumerate(order):
        mass = np.bincount(prefix, weights=p, minlength=1 << k)
        numerator = np.bincount(prefix, weights=p*spins[:, i], minlength=1 << k)
        mean = (numerator/mass)[prefix]
        psi[:, k] = (spins[:, i] - mean)/np.sqrt(1-mean*mean)
        prefix += ((states >> i) & 1) << k
    Q = np.ones((N, N))
    lam = np.zeros(N)
    for mask in range(1, N):
        bit = mask & -mask
        k = bit.bit_length()-1
        Q[:, mask] = Q[:, mask ^ bit] * psi[:, k]
        lam[mask] = lam[mask ^ bit] + clocks[order[k]]
    gram = Q.T @ (p[:, None]*Q)
    H = Q.T @ (p[:, None]*(K @ Q))
    invroot = 1/np.sqrt(lam[1:])
    B = invroot[:, None]*H[1:, 1:]*invroot[None, :]
    ev = la.eigvalsh(B)
    return {"n": n, "J": J, "clock_min": float(min(clocks)),
            "clock_max": float(max(clocks)), "order": list(map(int, order)),
            "gram_error": float(np.linalg.norm(gram-np.eye(N), 2)),
            "B_symmetry_error": float(np.linalg.norm(B-B.T, 2)),
            "eigen_min": float(ev[0]), "eigen_max": float(ev[-1]),
            "condition": float(ev[-1]/ev[0])}


def main():
    rows = []
    rng = np.random.default_rng(1705)
    for n in [2, 4, 6, 8]:
        perm = rng.permutation(n)
        clocks = 10.**(-8*perm/max(n-1, 1))
        for J in [.2, .6, 1.2]:
            for label, order in [("physical", np.arange(n)),
                                 ("slow_first", np.argsort(clocks))]:
                row = matrices(n, J, clocks, order)
                row["ordering"] = label
                rows.append(row)
                print(json.dumps(row), flush=True)
    path = Path(__file__).with_name("innovation_probe_results.json")
    path.write_text(json.dumps(rows, indent=2)+"\n")


if __name__ == "__main__":
    main()
