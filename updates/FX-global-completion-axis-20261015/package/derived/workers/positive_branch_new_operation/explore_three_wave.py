#!/usr/bin/env python3
"""Compatible three-wave exploration; numerical discovery only, never a QC proof.

v = x sin(x_1) + y sin(x_2) + z sin(x_1+x_2).
The affine background is minimized analytically, through a 4x4 moment matrix.
No heat/SOS correction or unconstrained matrix Young measure is searched.
"""

import itertools
import json
import argparse
from pathlib import Path

import numpy as np
import scipy.optimize as opt
import sympy as sp


OUT = Path(__file__).resolve().parent
r = sp.Symbol("r", positive=True)
a, b, c, d = vars4 = sp.symbols("a b c d", real=True)
u = a*a + c*c
j = a*d - b*c
H = ((a-d)**2 + (b+c)**2)**2
F = 3*r/(8*(r+2))*H + r*(r-1)/6*u*u + j*j + r*u*j
Texpr = np.empty((4, 4, 4, 4), dtype=object)
for ii in itertools.product(range(4), repeat=4):
    Texpr[ii] = sp.diff(F, *(vars4[k] for k in ii))/24
Tfn = sp.lambdify(r, Texpr.tolist(), "numpy", cse=True)


def waves(p):
    p = np.asarray(p)
    target = p[:6].reshape(3, 2)
    directions = np.eye(2) if p.size == 6 else p[6:].reshape(2, 2)
    covectors = np.vstack([directions, directions[0]+directions[1]])
    return np.array([np.outer(a, k).reshape(4)
                     for a, k in zip(target, covectors)])


def moments(T, p):
    W = waves(p)
    W /= np.linalg.norm(W)
    quartic = lambda x, y, z, w: np.einsum("ijkl,i,j,k,l", T, x, y, z, w)
    A = 3/8*sum(quartic(x, x, x, x) for x in W)
    A += 3/2*sum(quartic(W[i], W[i], W[j], W[j])
                 for i in range(3) for j in range(i))
    K = 3*np.einsum("ijkl,nk,nl->ij", T, W, W)
    cubic = 6*np.einsum("ijkl,j,k,l->i", T, *W)
    ev, U = np.linalg.eigh(K)
    co = U.T @ cubic
    scale = max(1.0, np.max(np.abs(ev)))
    inverse = 1/np.maximum(ev, 1e-12*scale)
    B = -0.5*U @ (inverse*co)
    # Evaluate the actual affine polynomial at the regularized background.
    # This cannot create a spurious negative gap when K is nearly singular.
    gap = A + np.dot(cubic, B) + B @ K @ B
    return A, K, cubic, B, gap, ev, W


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--general", action="store_true")
    parser.add_argument("--relative", action="store_true")
    parser.add_argument("--starts", type=int, default=36)
    args = parser.parse_args()
    rng = np.random.default_rng(20261015)
    records = []
    for rval in [0.1, 0.5, 1.0, 2.0, 4.0, 10.0, 100.0]:
        T = np.asarray(Tfn(rval), dtype=float)/(1+rval*rval)
        def objective(p):
            vals = moments(T, p)
            return vals[4]/max(vals[0], 1e-14) if args.relative else vals[4]
        best = None
        for start in range(args.starts):
            p0 = rng.normal(size=10 if args.general else 6)
            result = opt.minimize(objective, p0, method="BFGS",
                                  options={"maxiter":350, "gtol":1e-10})
            vals = moments(T, result.x)
            score = objective(result.x)
            if best is None or score < best[0]:
                best = (score, result, vals)
        _, result, vals = best
        A, K, cubic, B, gap, ev, W = vals
        record = {"r":rval, "tensor_scale":"1/(1+r^2)",
                  "gap":float(gap), "zero_background_energy":float(A),
                  "K_eigenvalues":ev.tolist(), "background":B.tolist(),
                  "wave_matrices":W.tolist(), "parameters":result.x.tolist(),
                  "optimizer_success":bool(result.success),
                  "optimizer_message":str(result.message),
                  "general_covectors":args.general,
                  "relative_gap":float(gap/A),
                  "starts":args.starts,
                  "scope":"finite numerical compatible family; no universal conclusion"}
        records.append(record)
        print(json.dumps(record), flush=True)
    name = "THREE_WAVE_GENERAL_DISCOVERY.json" if args.general else "THREE_WAVE_DISCOVERY.json"
    (OUT/name).write_text(json.dumps(records, indent=2)+"\n")


if __name__ == "__main__":
    main()
