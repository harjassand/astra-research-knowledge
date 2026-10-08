#!/usr/bin/env python3
"""Finite numerical diagnostics for glucose-off rescue in the PLOS core model.

These RK4 trajectories are exploratory only. They do not establish reachability
or validate the simplified model against yeast.
"""

from math import isfinite

P = dict(vu=10.0, kmg=0.1, kma=0.1, ki=3.0, atot=5.0,
         vl=10.0, kmf=1.0, kmd=0.1, kmp=2.0,
         katp=10.0, kp=0.4, pvmax=10.0, kvac=250.0, m=4.0)


def rates(y, glucose, p=P):
    f, a, pi = y
    d = p["atot"] - a
    vup = (p["vu"] * glucose * a /
           ((p["kmg"] + glucose) *
            (p["kma"] + a * (1.0 + a / p["ki"]))))
    vlo = (p["vl"] * f * d * pi /
           ((p["kmf"] + f) * (p["kmd"] + d) * (p["kmp"] + pi)))
    ptotal = pi + 2.0 * f + a
    pv = p["pvmax"] / (1.0 + (ptotal / p["kvac"]) ** p["m"])
    vp = p["kp"] * (pv - pi)
    return vup, vlo, vp, pv


def rhs(y, glucose, p=P):
    f, a, pi = y
    vu, vl, vp, _ = rates(y, glucose, p)
    return (vu - vl, -2 * vu + 4 * vl - p["katp"] * a,
            -2 * vl + p["katp"] * a + vp)


def add(x, k, dt):
    return tuple(a + dt * b for a, b in zip(x, k))


def step(y, dt, glucose, p=P):
    k1 = rhs(y, glucose, p)
    k2 = rhs(add(y, k1, dt / 2), glucose, p)
    k3 = rhs(add(y, k2, dt / 2), glucose, p)
    k4 = rhs(add(y, k3, dt), glucose, p)
    return tuple(x + dt * (a + 2*b + 2*c + d) / 6
                 for x, a, b, c, d in zip(y, k1, k2, k3, k4))


def integrate(y0, glucose, horizon=420.0, dt=0.001, p=P):
    y = tuple(y0)
    reached = None
    mins = list(y)
    for n in range(int(horizon / dt)):
        t = n * dt
        if 1.8 <= y[0] <= 2.2 and y[1] >= 0.3 and y[2] >= 1.0 and y[1] + y[2] <= 14:
            reached = reached if reached is not None else t
        y = step(y, dt, glucose, p)
        if not all(isfinite(z) for z in y):
            raise ArithmeticError((t, y))
        mins = [min(a, b) for a, b in zip(mins, y)]
    vu, vl, vp, pv = rates(y, glucose, p)
    return y, mins, reached, (vu, vl, vp, pv)


def main():
    starts = [
        ("moderate", (20.0, 0.1, 0.1)),
        ("high_fbp_low_energy", (100.0, 0.02, 0.02)),
        ("low_carbon", (5.0, 0.1, 0.1)),
        ("near_target", (3.0, 0.1, 0.1)),
        ("high_atp_low_pi", (20.0, 0.5, 0.05)),
    ]
    for name, x0 in starts:
        y, mins, reached, endrates = integrate(x0, glucose=0.0)
        print(name, "x0=", x0, "reached_safe_at=", reached,
              "final=", tuple(round(z, 6) for z in y),
              "min=", tuple(round(z, 6) for z in mins),
              "final_rates=", tuple(round(z, 6) for z in endrates))


if __name__ == "__main__":
    main()
