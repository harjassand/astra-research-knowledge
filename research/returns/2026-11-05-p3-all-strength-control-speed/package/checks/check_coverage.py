"""Finite-dimensional falsification checks for the new coverage lemma.

These checks are floating-point examples, not a proof or interval certificate.
No inherited Astra program is run here.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from scipy.linalg import expm
from scipy.integrate import solve_ivp

SEED = 20261105
rng = np.random.default_rng(SEED)
I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.diag([1, -1]).astype(complex)
PAULIS = [I, X, Y, Z]


def kron(items):
    v = np.ones((1, 1), dtype=complex)
    for a in items:
        v = np.kron(v, a)
    return v


def tnorm(a):
    return float(np.linalg.svd(a, compute_uv=False).sum())


def random_terms(n, k, intervals=3):
    """Saturate the summed h=2||H_a|| per-site budget at Omega=1."""
    hs = []
    for _ in range(intervals):
        ts = []
        load = np.zeros(n)
        for _ in range(3*n):
            support = set(rng.choice(n, size=int(rng.integers(1,k+1)), replace=False))
            src = [PAULIS[int(rng.choice([1,2]))] if i in support
                   else PAULIS[int(rng.choice([0,3]))] for i in range(n)]
            # A shared protected receiver makes the source terms generally noncommuting.
            op = kron(src + [PAULIS[int(rng.integers(0,4))]])
            h = float(rng.uniform(0.1, 1))
            ts.append((support, h, op))
            for i in support:
                load[i] += h
        scale = 1 / float(load.max())
        H = sum((h*scale/2)*op for _, h, op in ts)
        # Large uncharged diagonal source / arbitrary receiver backgrounds.
        for _ in range(3):
            H += rng.normal()*3*kron([PAULIS[int(rng.choice([0,3]))]
                                     for _ in range(n)]
                                    + [PAULIS[int(rng.integers(0,4))]])
        hs.append(H)
    return hs


cases = []
for n in [2,3,4]:
    for k in range(1, min(n,2)+1):
        for repetition in range(20):
            B = float(rng.choice([0.2,0.5,0.8]))
            Hs = random_terms(n,k)
            source_dim = 2**n
            # Generic source sign-pair difference, all source sites transverse.
            source = kron([PAULIS[int(rng.choice([1,2]))] for _ in range(n)]) / source_dim
            a = rng.normal(size=2) + 1j*rng.normal(size=2)
            a /= np.linalg.norm(a)
            delta = np.kron(source, np.outer(a,a.conj()))
            hit = sorted(rng.choice(n, size=int(rng.integers(1,n+1)),replace=False).tolist())
            events = [(float(rng.uniform(0,B)),int(i)) for i in hit]
            # Additional hits ensure the lemma does not accidentally rely on one hit/site.
            events += [(float(rng.uniform(0,B)),int(rng.choice(hit)))
                       for _ in range(int(rng.integers(0,n+1)))]
            events += [(B*j/3, -j) for j in [1,2]]
            events.sort()
            previous = 0.0
            segment = 0
            for when, site in events + [(B,-99)]:
                U = expm(-1j*Hs[segment]*(when-previous))
                delta = U@delta@U.conj().T
                if site >= 0:
                    Zi = kron([Z if j==site else I for j in range(n)] + [I])
                    delta = (delta + Zi@delta@Zi)/2
                elif site in [-1,-2]:
                    segment = -site
                previous = when
            observed = tnorm(delta)
            bound = B**int(np.ceil(len(hit)/k))
            cases.append(dict(n=n,k=k,B=B,hit_count=len(hit),observed_norm=observed,
                              coverage_bound=bound,ratio=observed/bound))
            assert observed <= bound + 1e-10, cases[-1]

# Independently compare exact analytic meter contrast with ODE integration.
meter_cases = []
for ratio in [1.01,1.2,2,5,10,100,1000]:
    lam = 1.0
    omega = ratio
    v = np.sqrt(omega**2-lam**2)
    T = np.arctan(v/lam)/v
    analytic = np.exp(-lam*T)
    sol = solve_ivp(lambda t,y:[omega*y[1],-omega*y[0]-2*lam*y[1]],
                    [0,T],[0,1],rtol=2e-11,atol=2e-13)
    numeric = float(sol.y[0,-1])
    assert abs(analytic-numeric)<1e-9
    meter_cases.append(dict(Omega_over_lambda=ratio,duration=T,analytic_contrast=analytic,
                            numeric_contrast=numeric,absolute_difference=abs(analytic-numeric)))

report = dict(seed=SEED,scope="floating-point falsification checks, not proof or interval certificate",
              trajectory_case_count=len(cases),maximum_coverage_ratio=max(c["ratio"] for c in cases),
              trajectory_cases=cases,meter_cases=meter_cases)
out = Path(__file__).with_name("coverage_checks.json")
out.write_text(json.dumps(report,indent=2)+"\n")
print(json.dumps({k:v for k,v in report.items() if k not in ["trajectory_cases","meter_cases"]},indent=2))
print("meter_case_count",len(meter_cases))
print("saved",out)
