#!/usr/bin/env python3
"""Bounded diagnostics of the exactly defined ccq model, not a channel proof."""
import json
import math
from pathlib import Path

import numpy as np


def g(x):
    return (x + 1) * math.log1p(x) - (x * math.log(x) if x > 0 else 0)


def gaussian_difference(r, kappa, variance):
    n = (math.sqrt(1 + 4*kappa*variance/(1+variance))-1)/2
    return 0.5*math.log((1+r*r*variance)/(1+variance))-g(n)


def discrete_difference(u, p, r, kappa, order=160, radius=9):
    # Integrate separately around each component mean. All entropies use nats.
    nodes, weights = np.polynomial.legendre.leggauss(order)
    znoise = radius*nodes
    weights = radius*weights*np.exp(-znoise*znoise/2)/math.sqrt(2*math.pi)
    gram_kernel = np.exp(-0.5*kappa*(u[:, None]-u[None, :])**2)

    def mi(scale, quantum=False):
        answer = 0.0
        quantum_entropy = 0.0
        for i in range(len(u)):
            observations = scale*u[i]+znoise
            logs = np.log(p)[None, :]-0.5*(observations[:, None]-scale*u)**2
            shift = logs.max(axis=1)
            logmix = shift+np.log(np.exp(logs-shift[:, None]).sum(axis=1))
            # The common normal-density normalization cancels.
            answer += p[i]*float(weights @ (-znoise*znoise/2-logmix))
            if quantum:
                posterior = np.exp(logs-logmix[:, None])
                roots = np.sqrt(posterior)
                grams = roots[:, :, None]*roots[:, None, :]*gram_kernel
                eigs = np.linalg.eigvalsh(grams)
                eigs = np.maximum(eigs, 0)
                entropies = -(eigs*np.log(np.maximum(eigs, 1e-300))).sum(axis=1)
                quantum_entropy += p[i]*float(weights @ entropies)
        return answer, quantum_entropy

    bob, _ = mi(r)
    eve_classical, eve_quantum = mi(1, quantum=True)
    return bob-eve_classical-eve_quantum


def main():
    nu, kappa, r = 1, 2, 3.8
    rows = []
    for size in (2, 3, 5, 9, 17):
        for kind in ("uniform", "gaussian-shaped"):
            best = (-math.inf, None)
            for width in np.geomspace(.01, 10, 20):
                u = np.linspace(-width, width, size)
                p = np.ones(size) if kind == "uniform" else np.exp(-2*(u/width)**2)
                p /= p.sum()
                value = discrete_difference(u, p, r, kappa)
                if value > best[0]:
                    best = (value, float(width))
            rows.append(dict(size=size, prior=kind, max_difference_nats=best[0], width=best[1]))
    r_bkm = 1/math.sqrt(1-2*kappa*math.log1p(1/nu)/(2*nu+1))
    result = dict(status="FLOATING_POINT_DIAGNOSTIC_ONLY", physical_local_limit="UNPROVED",
                  parameters=dict(nu=nu, kappa=kappa, r=r, eta=r/(1+r)),
                  quadrature=dict(order=160, component_radius=9), scan=rows,
                  gaussian_prefix_asymptotic_eta=r_bkm/(1+r_bkm),
                  gaussian_difference_at_variance_1=gaussian_difference(r,kappa,1))
    path = Path(__file__).with_suffix(".json")
    path.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
