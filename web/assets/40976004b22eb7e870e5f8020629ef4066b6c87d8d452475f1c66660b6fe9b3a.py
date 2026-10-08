#!/usr/bin/env python3
"""Finite trajectory diagnostic for near-boundary initial states of BIOMD206."""

import numpy as np
from scipy.integrate import solve_ivp

P = dict(k0=50.0, k1=550.0, k2=9.8, k31=323.8, k33=5.78231e4,
         k32=7.64111e4, k34=23.7, k4=80.0, k5=9.7, k6=2000.0,
         k7=28.0, k8=85.7, k9=80.0, k10=375.0, atot=4.0, ntot=1.0,
         n=4.0, ki=1.0)

def rhs(_t, x):
    s1, at, s2, s3, na, s4, s5, s6, s6o = x
    p = P
    v1 = p["k1"] * s1 * at / (1.0 + (at / p["ki"]) ** p["n"])
    v2 = p["k2"] * s2
    v3_num = (p["k31"] * p["k32"] * s3 * na * (p["atot"] - at)
              - p["k33"] * p["k34"] * s4 * at * (p["ntot"] - na))
    v3_den = p["k33"] * (p["ntot"] - na) + p["k32"] * (p["atot"] - at)
    v3 = v3_num / v3_den
    v4 = p["k4"] * s4 * (p["atot"] - at)
    v5 = p["k5"] * s5
    v6 = p["k6"] * s6 * (p["ntot"] - na)
    v7 = p["k7"] * at
    v8 = p["k8"] * s3 * (p["ntot"] - na)
    v9 = p["k9"] * s6o
    v10 = p["k10"] * (s6 - s6o)
    return np.array([
        p["k0"] - v1,
        -2*v1 + v3 + v4 - v7,
        v1 - v2,
        2*v2 - v3 - v8,
        -v3 + v6 + v8,
        v3 - v4,
        v4 - v5,
        v5 - v6 - v10,
        0.1*v10 - v9,
    ])

def main():
    starts = [
        ("published", [1.0, 2.0, 5.0, 0.6, 0.6, 0.7, 8.0, 0.08, 0.02]),
        ("near-empty-ATP", [1.0, 1e-10, 1e-10, 1e-10, 0.6, 1e-10, 1e-10, 1e-10, 1e-10]),
        ("near-empty-ATP-high-glucose", [100.0, 1e-10, 1e-10, 1e-10, 0.6, 1e-10, 1e-10, 1e-10, 1e-10]),
    ]
    for name, x0 in starts:
        sol = solve_ivp(rhs, (0, 100), x0, method="LSODA", rtol=1e-9,
                        atol=1e-13, dense_output=False, max_step=1e-2)
        x = sol.y
        print(name, "success", sol.success, "nsteps", len(sol.t), "t_final", sol.t[-1])
        for i, sp in enumerate(("s1", "at", "s2", "s3", "nad", "s4", "s5", "s6", "s6o")):
            print(f"  {sp:4s} min={x[i].min():.6g} max={x[i].max():.6g} final={x[i,-1]:.6g}")
        print("  pool maxima", (x[1] + (4.0-x[1])).min(), x[4].min(), x[4].max())

if __name__ == "__main__":
    main()
