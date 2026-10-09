#!/usr/bin/env python3
"""Check the anastrophy/Poincare release cap for the v1 2-D fields."""

import numpy as np
from diagnostics import bump, one_case


def integ(v, dx):
    return float(np.sum(v) * dx)


def one_anastrophy(eps, nx=16384, ny=2048):
    x = np.linspace(-np.pi, np.pi, nx, endpoint=False)
    y = np.linspace(-np.pi, np.pi, ny, endpoint=False)
    dx, dy = 2*np.pi/nx, 2*np.pi/ny
    f = bump(x/eps)[0]
    g = 0.5*(1+np.cos(y))
    e_raw, scale, *_ = one_case(eps, nx=nx, ny=ny)

    # A=A0+eps*f(x/eps)g(y), A0=cos(x)-cos(y).
    cross = (integ(np.cos(x)*f, dx)*integ(g, dy)
             - integ(f, dx)*integ(np.cos(y)*g, dy))
    bump_sq = integ(f**2, dx)*integ(g**2, dy)
    integral_a_sq = 4*np.pi**2 + 2*eps*cross + eps**2*bump_sq
    integral_a = eps*integ(f, dx)*integ(g, dy)
    volume = 4*np.pi**2
    integral_a_sq_mean_zero = integral_a_sq - integral_a**2/volume
    anastrophy = 0.5*scale**2*integral_a_sq_mean_zero
    energy = 2*np.pi**2
    return e_raw, scale, anastrophy, energy-anastrophy


if __name__ == "__main__":
    print("eps       E_fast(raw)   scale       anastrophy   release cap")
    for eps in (0.1, 0.05, 0.025, 0.01, 0.005):
        e, s, a2, cap = one_anastrophy(eps)
        print(f"{eps:0.3f}  {e:12.8f}  {s:9.6f}  {a2:11.7f}  {cap:11.7f}")
