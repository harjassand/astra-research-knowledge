#!/usr/bin/env python3
"""Finite RK4 diagnostics for the full PLOS core model (including H and dilution).

The source model is the PLOS 2021 S1 CellML file.  These runs are diagnostics,
not validated numerics, a basin proof, or validation against living yeast.
All concentrations are mM, time is min.  The IC genotype is Table 2.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite, log
from typing import Callable


@dataclass(frozen=True)
class Params:
    vu: float = 10.92211
    vl: float = 5.65143
    katp: float = 4.82003
    kp: float = 2.07099
    hmax: float = 1.0
    kmg: float = 0.1
    kma: float = 0.1
    ki: float = 3.0
    atot: float = 5.0
    kmf: float = 1.0
    kmd: float = 0.1
    kmp: float = 2.0
    pvmax: float = 10.0
    kvac: float = 250.0
    m: int = 4
    vatpm: float = 0.0
    taug: float = 90.0
    taud: float = 420.0
    vatprb: float = 12.7
    vatpri: float = 0.46
    vatper: float = 5.0
    vu_ref: float = 10.0
    vl_ref: float = 10.0
    katp_ref: float = 10.0
    kp_ref: float = 0.3

    @property
    def ug(self) -> float:
        return log(2.0) / (self.taug * (self.vatprb - self.vatper - self.vatpm))

    @property
    def ud(self) -> float:
        # vatpgri is negative; this sign makes H decrease when vatpg < 0.
        return 1.0 / (self.taud * (self.vatpri - self.vatper - self.vatpm))

    @property
    def vatpe(self) -> float:
        # CellML defines the enzyme-expression ATP cost from the fourth-power
        # genotype/reference ratio.  The published IC value 2.63 is rounded.
        reference = self.vu_ref**4 + self.vl_ref**4 + self.katp_ref**4 + self.kp_ref**4
        genotype = self.vu**4 + self.vl**4 + self.katp**4 + self.kp**4
        return self.vatper * genotype / reference


def fluxes(y: tuple[float, float, float, float], glucose: float, p: Params):
    f, a, pi, h = y
    d = p.atot - a
    vup = (p.vu * glucose * a / ((p.kmg + glucose) *
            (p.kma + a * (1.0 + a / p.ki))))
    vlo = (p.vl * f / (p.kmf + f) * d / (p.kmd + d) *
           pi / (p.kmp + pi))
    ptotal = pi + 2.0 * f + a
    pivac = p.pvmax / (1.0 + (ptotal / p.kvac) ** p.m)
    vp = p.kp * (pivac - pi)
    vatp = p.katp * a
    vatpg = vatp - p.vatpe - p.vatpm
    mu = p.ug * vatpg if h >= p.hmax and vatpg > 0.0 else 0.0
    return vup, vlo, vatp, vp, pivac, vatpg, mu


def rhs(y: tuple[float, float, float, float], glucose: float, p: Params):
    f, a, pi, h = y
    vup, vlo, vatp, vp, _, vatpg, mu = fluxes(y, glucose, p)
    if vatpg <= 0.0:
        hdot = -p.ud * vatpg
    elif h < p.hmax:
        hdot = p.ug * vatpg
    else:
        hdot = 0.0
    return (vup - vlo - mu * f,
            -2.0 * vup + 4.0 * vlo - vatp - mu * a,
            -2.0 * vlo + vatp + vp - mu * pi,
            hdot)


def _add(x, k, dt):
    return tuple(a + dt * b for a, b in zip(x, k))


def step(y, dt, glucose, p: Params):
    k1 = rhs(y, glucose, p)
    k2 = rhs(_add(y, k1, dt / 2), glucose, p)
    k3 = rhs(_add(y, k2, dt / 2), glucose, p)
    k4 = rhs(_add(y, k3, dt), glucose, p)
    z = tuple(x + dt * (a + 2*b + 2*c + d) / 6
              for x, a, b, c, d in zip(y, k1, k2, k3, k4))
    # H is a bounded health reserve; a trajectory reaching H=0 has died.
    return z[:3] + (min(p.hmax, max(0.0, z[3])),)


def integrate(y0, policy: Callable[[float, tuple, Params], float],
              horizon=500.0, dt=0.005, p=Params()):
    y = tuple(y0)
    switch = None
    first_dead = None
    for n in range(int(horizon / dt)):
        t = n * dt
        glucose = policy(t, y, p)
        if not isfinite(glucose) or glucose < 0:
            raise ValueError((t, glucose))
        if first_dead is None and y[3] <= 0.0:
            first_dead = t
        y = step(y, dt, glucose, p)
        if not all(isfinite(v) for v in y):
            raise ArithmeticError((t, y))
    return y, first_dead


def off_then_fixed(threshold=5.0, restart=0.1):
    def policy(t, y, p):
        return 0.0 if y[0] > threshold else restart
    return policy


def timed_off_then_fixed(off_time=80.0, restart=0.1):
    def policy(t, y, p):
        return 0.0 if t < off_time else restart
    return policy


def fixed(glucose):
    return lambda t, y, p: glucose


def main():
    initial = [(f, 0.02, 0.02, h)
               for f in (5.0, 20.0, 100.0, 200.0, 300.0)
               for h in (0.1, 0.5, 1.0)]
    for label, policy in (
        ("F-trigger 5 -> 0.1", off_then_fixed()),
        ("80-min open-loop off -> 0.1", timed_off_then_fixed()),
    ):
        print("POLICY", label)
        for y0 in initial:
            y, dead = integrate(y0, policy, horizon=500.0, dt=0.005)
            print(" ", y0, "dead_at", dead, "final", tuple(round(x, 6) for x in y))

    print("FIXED-GLUCOSE GRID; initial FBP 300, ATP=Pi=0.02, H=Hmax")
    for g in (0.005, 0.01, 0.02, 0.03, 0.05, 0.1, 0.15, 0.2, 0.5, 2.0):
        y, dead = integrate((300.0, 0.02, 0.02, 1.0), fixed(g),
                            horizon=500.0, dt=0.005)
        print(" ", g, "dead_at", dead, "final", tuple(round(x, 6) for x in y))

    print("±10% GENOTYPE CORNERS; 80-min open-loop off -> 0.1")
    base = Params()
    for vu_sign in (-1, 1):
        for vl_sign in (-1, 1):
            for k_sign in (-1, 1):
                for kp_sign in (-1, 1):
                    p = Params(vu=base.vu * (1 + 0.1 * vu_sign),
                               vl=base.vl * (1 + 0.1 * vl_sign),
                               katp=base.katp * (1 + 0.1 * k_sign),
                               kp=base.kp * (1 + 0.1 * kp_sign))
                    y, dead = integrate((300.0, 0.02, 0.02, 1.0),
                                        timed_off_then_fixed(),
                                        horizon=500.0, dt=0.005, p=p)
                    print(" ", vu_sign, vl_sign, k_sign, kp_sign,
                          "dead_at", dead, "final", tuple(round(x, 5) for x in y))


if __name__ == "__main__":
    main()
