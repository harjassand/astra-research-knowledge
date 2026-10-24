#!/usr/bin/env python3
"""Owned nonlinear network operation and independent transfer diagnostics.

Model execution only: does not instantiate a material, contact/skin continuum,
or hydraulically driven gap switch. Physical actuation work remains unknown.
"""
from pathlib import Path
import json
import math
import numpy as np


def ring_laplacian(n, weight):
    out = np.zeros((n, n))
    for i in range(n):
        j = (i+1) % n
        out[i, i] += weight
        out[j, j] += weight
        out[i, j] -= weight
        out[j, i] -= weight
    return out


N = 12
Y = .8*np.eye(N)+ring_laplacian(N, 2.)
Z = np.linalg.inv(Y)
ONES = np.ones(N)
NU = 1.
S_SOLID = 1.
KAPPA = 1.
ETA0 = .2


def resistance(h, mean_gap):
    d = mean_gap-h
    if np.any(d <= S_SOLID):
        raise ValueError("pore closure: model interval left")
    return d*d/(KAPPA*(d-S_SOLID))


def branch_eta(j):
    return ETA0*np.arcsinh(j)


def current(h, mean_current, mean_gap, pressure=None, b=.5):
    r = resistance(h, mean_gap)
    offset = np.zeros(N) if pressure is None else b*pressure
    j = mean_current*ONES.copy()
    v = np.mean(Z@j+r*j+branch_eta(j)+offset)
    for _ in range(25):
        residual = Z@j+r*j+branch_eta(j)+offset-v
        target = N*mean_current-j.sum()
        if max(np.max(np.abs(residual)), abs(target)) < 2e-13:
            return j, v
        jac = Z+np.diag(r+ETA0/np.sqrt(1+j*j))
        u = np.linalg.solve(jac, ONES)
        w = np.linalg.solve(jac, residual)
        dv = (target+w.sum())/u.sum()
        j += -w+dv*u
        v += dv
    raise RuntimeError("nonlinear current solve did not converge")


def rhs(h, mean_current, mean_gap):
    j, _ = current(h, mean_current, mean_gap)
    return NU*(j-mean_current)


def rk4(function, x, step):
    a = function(x)
    b = function(x+.5*step*a)
    c = function(x+.5*step*b)
    d = function(x+step*c)
    return x+step*(a+2*b+2*c+d)/6


def phase(h, mean_current, mean_gap, duration=1., steps=200):
    start = h.copy()
    dt = duration/steps
    variance = [float(h@h/N)]
    low, high = [float(h.min())], [float(h.max())]
    dissipated = 0.
    for _ in range(steps):
        j, _ = current(h, mean_current, mean_gap)
        dissipated += dt*(j@(Z@j)+np.sum(resistance(h, mean_gap)*j*j)
                          +j@branch_eta(j))
        h = rk4(lambda x: rhs(x, mean_current, mean_gap), h, dt)
        assert abs(h.sum()) < 2e-12
        variance.append(float(h@h/N))
        low.append(float(h.min()))
        high.append(float(h.max()))
    return h, {
        "mean_current": mean_current,
        "mean_gap": mean_gap,
        "duration": duration,
        "mean_deposited_height": NU*mean_current*duration,
        "variance_ratio": variance[-1]/variance[0],
        "maximum_variance_step_increase": max(np.diff(variance)),
        "maximum_height_step_increase": max(np.diff(high)),
        "maximum_negative_minimum_step": max(-np.diff(low)),
        "electrical_overpotential_dissipation": float(dissipated),
        "mean_zero_residual": float(abs(h.sum())),
        "start_range": [float(start.min()), float(start.max())],
        "end_range": [float(h.min()), float(h.max())],
    }


def graph_identity(h):
    j0, gap = 1., 1.6
    j, _ = current(h, j0, gap)
    r = resistance(h, gap)
    delta = j-j0
    secant = np.where(np.abs(delta)>1e-10,
                      (branch_eta(j)-branch_eta(j0))/np.where(np.abs(delta)>1e-10, delta, 1),
                      ETA0/math.sqrt(1+j0*j0))
    matrix = Z+np.diag(r+secant)
    inverse = np.linalg.inv(matrix)
    v = inverse@ONES
    a = inverse-np.outer(v, v)/v.sum()
    q = j0*r+branch_eta(j0)
    assert np.max(np.abs(delta+a@q)) < 2e-13
    off = a.copy()
    np.fill_diagonal(off, -np.inf)
    assert off.max() < 0
    pair = sum(-a[i, k]*(h[i]-h[k])*(q[i]-q[k])
               for i in range(N) for k in range(i+1, N))
    assert abs(h@a@q-pair) < 2e-13
    return {
        "current_identity_residual": float(np.max(np.abs(delta+a@q))),
        "laplacian_row_residual": float(np.max(np.abs(a@ONES))),
        "maximum_off_diagonal": float(off.max()),
        "variance_derivative": float(NU*h@delta),
        "pair_identity_residual": float(abs(h@a@q-pair)),
    }


def hydraulic_identity(h):
    pressure = .04*np.cos(2*np.pi*np.arange(N)/N)
    mean_current, gap, b = 1., 1.6, .5
    storage = .1*np.eye(N)
    hydraulic = .2*np.eye(N)+ring_laplacian(N, .1)
    j, _ = current(h, mean_current, gap, pressure, b)
    dh = NU*(j-mean_current)
    dp = np.linalg.solve(storage, dh-hydraulic@pressure)
    delta = j-mean_current
    eta_secant = (branch_eta(j)-branch_eta(mean_current))/delta
    matrix = Z+np.diag(resistance(h, gap)+eta_secant)
    e_dot = (mean_current*resistance(h, gap)@dh
             +b*pressure@(storage@dp))
    negative = -dh@(matrix@dh)/NU-b*pressure@(hydraulic@pressure)
    assert abs(e_dot-negative) < 2e-13
    return {"storage_pressure_energy_derivative": float(e_dot),
            "negative_dissipation": float(negative),
            "identity_residual": float(abs(e_dot-negative)),
            "scope": "One instantaneous state; reciprocal hydraulic source/work map specified, not acquired."}


def skin_checks():
    # Independently solve potential coefficients A cosh(qz)+B sinh(qz),
    # jb,jt,W for the moving-face boundary conditions, not only evaluate N/D.
    rng = np.random.default_rng(20261024)
    errors = []
    for _ in range(20):
        q, b, ks = rng.uniform(.05, 4), rng.uniform(.01, .5), rng.uniform(.2, 2)
        j0, rh, r, upstream, gamma = .8, .7, .3, .4, .02
        p, c, s = ks*q, math.cosh(q*b), math.sinh(q*b)
        g, chi = j0/ks, gamma*q*q
        # Variables [A, B, jb, jt, W], unit height h=1.
        a = np.array([[1.,0.,-r,0.,0.],
                      [c,s,0.,0.,-1.],
                      [0.,-p,1.,0.,0.],
                      [-p*s,-p*c,0.,1.,0.],
                      [0.,0.,0.,upstream,1.]])
        target = np.array([chi-g,-g,0.,0.,-j0*rh])
        direct = np.linalg.solve(a, target)[2]
        numerator = (-j0*rh+g*(c-1+upstream*p*s)
                     -chi*(c+upstream*p*s))
        denominator = r*c+s/p+upstream*(c+r*p*s)
        errors.append(abs(direct-numerator/denominator))
    assert max(errors) < 1e-12
    solid, gap, kl = 1e-6, 1.6e-6, 1.
    rp = gap*gap/(kl*(gap-solid))
    rh = (solid*solid/(gap-solid)**2-1)/kl
    j0, gamma, ks, b, r = 10., 5e-11, .1, 1e-8, 1e-4
    ell = math.sqrt(ks*gamma/j0)
    lmax = rp+20e-6/.5
    beta = b/ell
    right = math.cosh(beta)-1+lmax*ks/ell*math.sinh(beta)
    qm = 2*math.pi/100e-9
    transmission = 1/(math.cosh(qm*b)+r*ks*qm*math.sinh(qm*b))
    assert ks*rh > right
    return {"random_boundary_linear_system_count": len(errors),
            "maximum_transfer_formula_residual": float(max(errors)),
            "design_specification_only": True,
            "all_q_sufficient_left": ks*rh,
            "all_q_sufficient_right": right,
            "ell_cap_m": ell,
            "ell_spread_m": math.sqrt(r*ks*b),
            "100nm_injection_transmission": transmission}


def main():
    x = 2*np.pi*np.arange(N)/N
    initial = .14*np.sin(x)+.025*np.cos(3*x)
    initial -= initial.mean()
    plated, p = phase(initial, 1., 1.6)
    returned, reverse = phase(plated, -1., 1.6)
    programmed, switched = phase(plated, -1., 2.4)
    assert np.max(np.abs(returned-initial)) < 2e-9
    assert p["maximum_variance_step_increase"] < 0
    assert switched["maximum_variance_step_increase"] < 0
    assert p["maximum_height_step_increase"] <= 1e-13
    assert switched["maximum_height_step_increase"] <= 1e-13
    result = {
        "scope": "OWNED_NONLINEAR_COLUMN_OPERATION_AND_LINEAR_SKIN_DIAGNOSTIC",
        "graph": {"patches": N, "reservoir_conductance": .8,
                  "ring_edge_conductance": 2., "nonlinear_activation": ".2 asinh(j)"},
        "identity": graph_identity(initial),
        "fixed_geometry": {"plating": p, "stripping": reverse,
                           "return_error": float(np.max(np.abs(returned-initial)))},
        "programmed_geometry": {"plating": p, "stripping": switched,
                                "cycle_variance_ratio": float(programmed@programmed/(initial@initial)),
                                "extra_common_gap_stroke": .8,
                                "actuator_work": "UNKNOWN: no acquired force law",
                                "switching_hydraulics": "NOT_EXECUTED: static column model only"},
        "hydraulic_port": hydraulic_identity(initial),
        "skin": skin_checks(),
        "limits": "Conditional network/linear continuum mathematics. Pore-to-metal deformation, skin material, finite-amplitude repaired interface and real cycle actuation remain unacquired. No hardware or superiority claim.",
    }
    output = Path(__file__).with_name("SHAPE_FEEDBACK_RESULTS.json")
    output.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
