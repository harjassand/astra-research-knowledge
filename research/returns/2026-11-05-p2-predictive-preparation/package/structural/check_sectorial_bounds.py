"""Diagnostics of the new sectorial companion, not a physical validation.

The continuous-family claims are proved in sectorial_passive_bridge.md.
This program checks their signs, constants, ellipse geometry, and one finite
trap trajectory. It does not implement the complete dictionary or experiment.
"""
from pathlib import Path
import json
import math
import numpy as np
from scipy.integrate import solve_ivp
from numpy.polynomial.legendre import leggauss


def filtered_factor(a: complex, h: float, w: float) -> complex:
    if a == 0:
        return 1.0 + 0.0j
    nodes, weights = leggauss(96)
    s = (nodes + 1.0) / 2.0
    ramp = np.dot(weights / 2.0, 30*s*s*(1-s)*(1-s)*np.exp(a*h*(1-s)))
    triangle = np.expm1(a*w)/(a*w)
    return complex(ramp * triangle**2)


def run():
    out = {"status": "diagnostic checks of new analytic companion"}
    margins = []
    for q in [0, .01, .1, 1, 3, 10, 100, 1e4]:
        c = 1+q
        rho = 1+1/c
        lhs = c*rho + (2-c)/rho
        margins.append(6-lhs)
        assert lhs < 4 + 1e-10
    out["minimum_sector_ellipse_margin"] = min(margins)

    worst = 0.0
    for q in [0, .1, 1, 3, 10]:
        c=1+q
        for lam in np.geomspace(1e-6, 1e3, 24):
            for ratio in [0, q/2, q]:
                a = complex(-lam, ratio*lam)
                h,w,t = .003,.004,1.0
                fa = filtered_factor(a,h,w)
                complex_l1 = abs(1-fa) * (-math.expm1(-lam*t))/lam
                bound = c*(h/2+w)
                worst = max(worst,complex_l1/bound)
                assert complex_l1 <= bound * (1+1e-9)
                assert abs(fa) <= 1+1e-12
    out["maximum_filter_bias_to_bound_ratio"] = worst
    phase = filtered_factor(complex(-.5,10), .3, .2)
    assert phase.real < 0
    out["filtered_atom_can_have_negative_zero_time_value"] = {
        "lambda": .5, "omega": 10.0, "h": .3, "w": .2,
        "filtered_at_zero_real": phase.real,
        "filtered_at_zero_imaginary": phase.imag,
        "interpretation": "The acquired filtered atom cannot itself be treated as an unfiltered passive positive-weight atom."
    }

    rates = np.array([0,.01,.2,1,5,20])
    frequencies = np.array([0,.005,.4,3,4,-10])
    weights = np.array([.1,.1,.2,.2,.2,.2])
    eig = -rates + 1j*frequencies
    z0 = np.array([.12+.2j,-.08+.1j,.04-.04j,-.1+.05j,.01+.03j,.08-.1j])
    E0 = .5 * np.dot(weights, abs(z0)**2)
    B = float(sum(weights)); Q=3.; C=1+Q; mu=1.
    A=.1; h=.2; stiffness=1000.; A_hist=.103
    G=math.sqrt(2*B*E0)+C*B*A_hist
    Phi=A+.1*A**3
    delta=(G+(1+C)*B*A+Phi)/(stiffness+mu-(C-1)*B)
    assert A+delta <= A_hist

    def command(t):
        s=min(1.,max(0.,t/h))
        u=A*(10*s**3-15*s**4+6*s**5)
        ud=0. if t>=h else A/h*30*s*s*(1-s)*(1-s)
        return u,ud

    def rhs(t,v):
        x=v[0]
        z=v[1:7]+1j*v[7:]
        u,ud=command(t)
        force=stiffness*(u+ud/stiffness-x)
        xd=force-x-.1*x**3-float(np.dot(weights,z.real))
        zd=eig*z+xd
        return np.r_[xd,zd.real,zd.imag]

    ts=np.linspace(0,2,4001)
    sol=solve_ivp(rhs,[0,2],np.r_[0.,z0.real,z0.imag],method="Radau",rtol=2e-10,atol=2e-12,t_eval=ts)
    assert sol.success
    target=np.array([command(t)[0] for t in ts])
    maxerr=float(np.max(np.abs(sol.y[0]-target)))
    assert maxerr < delta
    out["finite_trap_tracking"]={
        "Q":Q,"B":B,"E0":float(E0),"stiffness":stiffness,
        "proved_tube":delta,"sampled_tracking_error":maxerr,
        "history_radius_promise_closed":bool(A+delta<=A_hist),
        "solver":"floating Radau diagnostic, not interval validated"
    }

    old=-z0
    G_old=float(np.dot(weights,abs(old)))
    H=50.; b=.1; T=2.
    def free(t): return float(np.dot(weights,(np.exp(eig*t)*old).real))
    nd,wt=leggauss(64)
    baseline=sum(float(v)*free(H-b+(u+1)*b/2) for u,v in zip(nd,wt))/2
    drift=max(abs(free(H+t)-baseline) for t in np.linspace(0,T,2001))
    bound=C*G_old*(b+T)/(math.e*(H-b))
    assert drift<=bound
    out["complex_initial_force_aging"]={"actual_diagnostic_drift":drift,"proved_bound":bound,
        "frozen_real_force":float(weights[0]*old[0].real),"frozen_force_retained":True}
    return out


if __name__=="__main__":
    result=run()
    destination=Path(__file__).with_name("sectorial_bound_checks.json")
    destination.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))
