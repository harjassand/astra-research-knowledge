"""Small finite diagnostics for the attractive-resonance tail proof.

Run: OPENBLAS_NUM_THREADS=1 python3 outputs/research/sol_attractive_critical/checks.py
Requires NumPy only. These tests do not establish any infinite limit or novelty.
"""
import itertools
import json
import math
from pathlib import Path
import numpy as np

TOL = 3e-9
J, TAU, B = 1.0, 0.11, 0.7
ALPHA = 0.5
GMIN = 0.03
C = 1 + 2 * sum(math.exp(-4 * J * TAU * k*k) for k in range(1, 100))
C_COERC = min(GMIN / 96, J / 72)
A = math.e * C * math.exp(TAU * (B + C_COERC))


def sector(S, m):
    configs = list(itertools.combinations(range(S), m))
    index = {x: i for i, x in enumerate(configs)}
    hn = np.zeros((len(configs), len(configs)))
    end = np.zeros(len(configs))
    contact = np.zeros(len(configs))
    for k, x in enumerate(configs):
        xs = set(x)
        end[k] = (0 in xs) + (S-1 in xs)
        contact[k] = sum(i+1 in xs for i in x if i+1 < S)
        for i in x:
            for j in (i-1, i+1):
                if 0 <= j < S and j not in xs:
                    y = tuple(sorted((xs-{i}) | {j}))
                    hn[k, k] += 2 * J
                    hn[k, index[y]] -= 2 * J
    return configs, hn, hn + np.diag(2*J*end), np.diag(contact)


def heat(h, t):
    ev, vec = np.linalg.eigh(h)
    return (vec * np.exp(-t * ev)) @ vec.T


def embedded(S, terms):
    out = np.array([[1.]])
    for i in range(S):
        out = np.kron(out, terms.get(i, np.eye(2)))
    return out


def independent_spin(S):
    x = np.array([[0., 1.], [1., 0.]])
    y = np.array([[0., -1j], [1j, 0.]])
    z = np.diag([1., -1.])
    n = np.diag([0., 1.])
    h = np.zeros((2**S, 2**S), complex)
    for i in range(S-1):
        h += J * (np.eye(2**S) - embedded(S, {i:x, i+1:x})
                  - embedded(S, {i:y, i+1:y})
                  - embedded(S, {i:z, i+1:z}))
    h += J*(np.eye(2**S)-embedded(S, {0:z}))
    h += J*(np.eye(2**S)-embedded(S, {S-1:z}))
    w = sum((embedded(S, {i:n, i+1:n}) for i in range(S-1)),
            np.zeros_like(h))
    return h, w


out = {"status": "FINITE-EVIDENCE", "tolerance": TOL,
       "public_constants": {"J":J,"tau":TAU,"B":B,"g_min":GMIN,
                            "alpha":ALPHA,"c":C_COERC,"C":C,"A":A}}

spin_err = []
for S in range(1, 7):
    hs, ws = independent_spin(S)
    for m in range(S+1):
        cfg, hn, hc, w = sector(S, m)
        ids = [sum(1 << (S-1-i) for i in x) for x in cfg]
        spin_err.append(float(np.max(np.abs(hs[np.ix_(ids,ids)]-hc))))
        spin_err.append(float(np.max(np.abs(ws[np.ix_(ids,ids)]-w))))
assert max(spin_err) <= TOL
out["independent_spin_vs_graph"] = {"sector_cases":27,
    "S_range":[1,6],"max_error":max(spin_err)}

local_margin = []
for ell in range(2, 10):
    for n in range(2, ell+1):
        _, hn, _, w = sector(ell, n)
        for a in (0.02, 0.7, 5.0):
            lower = n * min(a/(8*ell), J*(1-ALPHA)/ell**2)
            local_margin.append(float(np.linalg.eigvalsh((1-ALPHA)*hn+a*w)[0]-lower))
assert min(local_margin) >= -TOL
out["conditional_particle_robin_local_exclusion"] = {
    "cases":len(local_margin),"ell_range":[2,9],"min_margin":min(local_margin)}

coerc_margin, partition_log_margin, trace_log_margin, correlation_margin = [], [], [], []
for S in range(1, 11):
    L = S+1
    t = ALPHA*TAU*L**2
    _, h1, _, _ = sector(S, 1)
    p = heat(h1, t)
    for m in range(S+1):
        cfg, hn, hc, w = sector(S, m)
        evn, vn = np.linalg.eigh(hn)
        trace = float(np.exp(-t*evn).sum())
        trace_log_margin.append(m*math.log(math.e*C)-math.log(trace))
        diagonal = ((vn**2)*np.exp(-t*evn)).sum(axis=1)
        for i, x in enumerate(cfg):
            bound = math.prod(float(p[j, list(x)].sum()) for j in x)
            correlation_margin.append(bound-float(diagonal[i]))
        for g in (GMIN, 0.4, 2.0, 12.0):
            h = hc + g/L*w
            if m >= 2:
                c_g = min(g/96, J/72)
                coerc_margin.append(float(np.linalg.eigvalsh(h-ALPHA*hc)[0]
                                          -c_g*m*m/(L*L)))
            ev = np.linalg.eigvalsh(h)
            logz = float(np.log(np.exp(-TAU*L*L*ev).sum()) + TAU*B*m)
            logbound = m*math.log(A)-TAU*C_COERC*m*m
            partition_log_margin.append(logbound-logz)
assert min(coerc_margin) >= -TOL
assert min(partition_log_margin) >= -TOL
assert min(trace_log_margin) >= -TOL
assert min(correlation_margin) >= -TOL
out["retained_kinetic_coercivity"] = {"cases":len(coerc_margin),
    "S_range":[1,10],"g_values":[GMIN,0.4,2.0,12.0],"min_margin":min(coerc_margin)}
out["all_sector_partition_bound"] = {"cases":len(partition_log_margin),
    "S_range":[1,10],"min_log_margin":min(partition_log_margin)}
out["sector_heat_trace"] = {"cases":len(trace_log_margin),
    "min_log_margin":min(trace_log_margin)}
out["individual_return_probability_product"] = {
    "cases":len(correlation_margin),"min_margin":min(correlation_margin)}

# Check the supersolution generator identity for every selected set, using
# independent pointwise algebra for random one-site values.
rng = np.random.default_rng(91027)
identity_error = []
for S in range(2, 9):
    for trial in range(4):
        u = rng.uniform(0.05, 0.95, S)
        du = np.zeros(S)
        for i in range(S-1):
            du[i] += 2*J*(u[i+1]-u[i])
            du[i+1] += 2*J*(u[i]-u[i+1])
        for k in range(1, S+1):
            cfg, hn, _, _ = sector(S, k)
            f = np.array([math.prod(u[i] for i in x) for x in cfg])
            df = np.array([sum(du[i]*math.prod(u[j] for j in x if j != i)
                               for i in x) for x in cfg])
            target = []
            for x in cfg:
                xs = set(x)
                target.append(sum(2*J*(u[i]-u[i+1])**2
                                  * math.prod(u[j] for j in x if j not in (i,i+1))
                                  for i in range(S-1) if i in xs and i+1 in xs))
            identity_error.extend(abs(df+hn@f-np.array(target)))
assert max(identity_error) <= TOL
out["occupation_moment_supersolution_identity"] = {
    "pointwise_cases":len(identity_error),"S_range":[2,8],
    "max_error":float(max(identity_error))}

out["all_checks_passed"] = True
Path(__file__).with_suffix(".json").write_text(json.dumps(out, indent=2)+"\n")
print(json.dumps(out, indent=2))
