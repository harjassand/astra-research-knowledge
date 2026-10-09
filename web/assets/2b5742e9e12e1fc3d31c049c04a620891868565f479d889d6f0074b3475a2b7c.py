#!/usr/bin/env python3
"""Numerical scaling check for the half-space edge weighted Rayleigh quotient.

The proof in v1.txt is analytic. This script checks its dilation prediction on
a periodic box: for m(d) ~ d^(3/2), a smooth test bump at distance/width eps
from the edge has H^(1/2) Hessian energy O(1), weighted norm squared
O(eps^(-1/2)), and decay-rate quotient O(sqrt(eps)).
"""

import numpy as np


LBOX = 8.0
N = 1 << 15
DX = LBOX / N
X = -LBOX / 2 + DX * np.arange(N)
K = 2 * np.pi * np.fft.fftfreq(N, d=DX)


def bump(t):
    """C-infinity positive bump on (1, 2), zero elsewhere."""
    out = np.zeros_like(t)
    inside = (t > 1.0) & (t < 2.0)
    z = t[inside]
    out[inside] = np.exp(-1.0 / ((z - 1.0) * (2.0 - z)))
    return out


def interior_corrector():
    """Fixed even smooth unit-mass corrector, away from both edges."""
    out = np.zeros_like(X)
    for center in (-1.5, 1.5):
        t = (X - (center - 0.25)) / 0.5
        inside = (t > 0.0) & (t < 1.0)
        z = t[inside]
        out[inside] += np.exp(-1.0 / (z * (1.0 - z)))
    return out / (DX * out.sum())


ETA = interior_corrector()


def weighted_rayleigh(eps):
    # Two symmetric edge bumps remove the translation-odd direction.
    d = -X
    right = bump(d / eps)
    left = bump((2.0 - d) / eps)
    v = right + left

    # c is constant here; subtract a fixed interior function to impose
    # the normalized-amplitude tangent condition integral(v)=0.
    mass = DX * v.sum()
    v = v - mass * ETA

    # Periodic Fourier approximation to <v, |D|v> on the large box.
    vhat = DX * np.fft.fft(v)
    kinetic = (np.abs(K) * np.abs(vhat) ** 2).sum() / LBOX

    # Lower-order slip-weakening term. Its contribution vanishes as O(eps).
    beta = 0.3
    hessian = kinetic - beta * DX * np.dot(v, v)

    # m(d)=d^(3/2), the mobility profile inherited from W*~A*d^(3/2).
    active = (X > -2.0) & (X < 0.0)
    edge_distance = np.minimum(-X[active], X[active] + 2.0)
    mobility = np.maximum(edge_distance, 1e-300) ** 1.5
    weighted_norm2 = DX * np.sum(v[active] ** 2 / mobility)
    return hessian, weighted_norm2, hessian / weighted_norm2


if __name__ == "__main__":
    print("eps       Q_H             ||v||_Hm^2      Q_H/||v||_Hm^2   rate/sqrt(eps)")
    for eps in (0.25, 0.125, 0.0625, 0.03125, 0.015625):
        q, norm2, rate = weighted_rayleigh(eps)
        print(f"{eps:<9.4g} {q:<15.8g} {norm2:<15.8g} {rate:<17.8g} {rate / np.sqrt(eps):.8g}")
