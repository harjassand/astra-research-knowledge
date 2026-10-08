"""Finite diagnostics for quantitative_rate.txt; NumPy and Python stdlib only.

These independently construct spin-sector forms, symmetric sine states,
midpoint continuum contact integrals and full labeled edge restrictions.
They test finite algebra and sampled scalar constants, not convergence,
external validity, priority or a practically usable chain-size threshold.
Run: OPENBLAS_NUM_THREADS=1 python3 outputs/research/sol_attractive_critical/rate_checks.py
"""
import itertools
import json
import math
from pathlib import Path
import numpy as np

RNG = np.random.default_rng(81012026)
TOL = 2e-7
J, G = 1.3, 0.7


def symmetric_sines(points, modes):
    result = np.zeros((len(points), len(modes)))
    for j, mode in enumerate(modes):
        permutations = sorted(set(itertools.permutations(mode)))
        for perm in permutations:
            result[:, j] += np.prod(np.sqrt(2)*np.sin(np.pi*points*np.array(perm)), axis=1)
        result[:, j] /= math.sqrt(len(permutations))
    return result


def continuum_contact(m, modes, q):
    points = (np.arange(q)+0.5)/q
    labels = np.array(list(itertools.product(points, repeat=m-1)))
    out = np.zeros((len(modes), len(modes)))
    for i, j in itertools.combinations(range(m), 2):
        full = np.zeros((len(labels), m))
        full[:, i] = labels[:, 0]
        full[:, j] = labels[:, 0]
        for k, a in enumerate([a for a in range(m) if a not in (i, j)], 1):
            full[:, a] = labels[:, k]
        values = symmetric_sines(full, modes)
        out += 2*(values.T@values)/q**(m-1)
    return out


def sector(S, m):
    configurations = list(itertools.combinations(range(1, S+1), m))
    indices = {x:i for i, x in enumerate(configurations)}
    kinetic = np.zeros((len(configurations), len(configurations)))
    contact = np.zeros(len(configurations))
    for i, x in enumerate(configurations):
        occupied = set(x)
        kinetic[i, i] = 2*J*((1 in occupied)+(S in occupied))
        contact[i] = sum(v+1 in occupied for v in x)
        for v in x:
            for dest in (v-1, v+1):
                if 1 <= dest <= S and dest not in occupied:
                    y = tuple(sorted((occupied-{v})|{dest}))
                    kinetic[i, i] += 2*J
                    kinetic[i, indices[y]] -= 2*J
    return configurations, kinetic, np.diag(contact)


cases = []
quadrature_errors, gram_margins, recovery_margins = [], [], []
kinetic_margins, contact_margins, total_margins = [], [], []
bad_edge_ratios, multiple_tie_ratios = [], []
for m in range(1, 5):
    for n in (4, 5, 7):
        L, h = n+m, 1/(n+1)
        for M in (1, 2):
            p = m*(m-1)//2
            modes = list(itertools.combinations_with_replacement(range(1, M+1), m))
            labels = np.array(list(itertools.product(range(1, n+1), repeat=m)))
            samples = h**(m/2)*symmetric_sines(h*labels, modes)
            assert np.linalg.norm(samples.T@samples-np.eye(len(modes))) <= TOL
            indices = {tuple(x):i for i, x in enumerate(labels)}
            cfg, kinetic, contact = sector(L-1, m)
            recovery = np.array([math.sqrt(math.factorial(m))*samples[
                indices[tuple(x[i]-i for i in range(m))]] for x in cfg])
            gram = recovery.T@recovery
            eta = (math.factorial(m)-1)*m*(m-1)*M*h
            gram_margins.append(float(np.linalg.eigvalsh((1+eta)*np.eye(len(modes))-gram)[0]))
            assert np.linalg.eigvalsh(gram-np.eye(len(modes)))[0] >= -TOL
            assert gram_margins[-1] >= -TOL
            factors = np.array([math.prod(math.factorial(list(z).count(v))
                                         for v in set(z)) for z in labels])
            polar_recovery = np.sqrt(factors)[:, None]*samples
            sinc = np.array([math.prod(np.sinc(k*h/2) for k in mode) for mode in modes])
            cross = sinc[:, None]*(samples.T@polar_recovery)
            norm_error = gram+np.eye(len(modes))-cross-cross.T
            embedding_bound = (math.sqrt(eta)+math.pi*math.sqrt(m)*M*h/math.sqrt(12))**2
            recovery_margins.append(float(np.linalg.eigvalsh(
                embedding_bound*np.eye(len(modes))-norm_error)[0]))
            assert recovery_margins[-1] >= -TOL
            continuum_T = np.diag([2*J*math.pi**2*sum(k*k for k in mode) for mode in modes])
            continuum_B = continuum_contact(m, modes, 5*M+3) if m >= 2 else np.zeros_like(continuum_T)
            nodal_B = np.zeros_like(continuum_T)
            tie_count = np.zeros(len(labels))
            for i, j in itertools.combinations(range(m), 2):
                mask = labels[:, i] == labels[:, j]
                tie_count += mask
                nodal_B += 2/h*(samples[mask].T@samples[mask])
            quadrature_errors.append(float(np.max(np.abs(nodal_B-continuum_B))))
            assert quadrature_errors[-1] <= TOL
            actual_kin = L*L*(recovery.T@kinetic@recovery)
            actual_contact = G*L*(recovery.T@contact@recovery)
            kinetic_bound = (L*h)**2*(1+4*(math.factorial(m)-1)*p*M*h)*continuum_T
            contact_bound = L*h*G*continuum_B+4*G*L*math.factorial(m)*m*p*p*M*M*h*h*np.eye(len(modes))
            kinetic_margins.append(float(np.linalg.eigvalsh(kinetic_bound-actual_kin)[0]))
            contact_margins.append(float(np.linalg.eigvalsh(contact_bound-actual_contact)[0]))
            assert kinetic_margins[-1] >= -TOL
            assert contact_margins[-1] >= -TOL
            q = continuum_T+G*continuum_B
            const = (64*J*math.pi**2*(math.factorial(m)-1)*p*m*M**3/L
                     +16*G*math.factorial(m)*m*p*p*M*M/L)
            total_margins.append(float(np.linalg.eigvalsh((1+8*m/L)*q+const*np.eye(len(modes))
                                                         -actual_kin-actual_contact)[0]))
            assert total_margins[-1] >= -TOL
            # Direct bad-edge restriction in the full labeled cube, with
            # zero ghost nodes; this does not use the canonical matrix.
            full = np.zeros((n+2,)*m+(len(modes),))
            full[(slice(1,n+1),)*m] = samples.reshape((n,)*m+(len(modes),))
            full_energy = np.zeros_like(continuum_T)
            bad_energy = np.zeros_like(continuum_T)
            for a in range(m):
                diff = np.diff(full, axis=a).reshape((-1, len(modes)))
                shape = [n+2]*m
                shape[a] -= 1
                src = np.array(list(itertools.product(*(range(k) for k in shape))))
                dst = src.copy()
                dst[:, a] += 1
                bad = np.zeros(len(src), dtype=bool)
                for i, j in itertools.combinations(range(m), 2):
                    bad |= (src[:, i] == src[:, j]) | (dst[:, i] == dst[:, j])
                full_energy += diff.T@diff
                bad_energy += diff[bad].T@diff[bad]
            eigen, vec = np.linalg.eigh(full_energy)
            inverse_half = (vec/eigen**0.5)@vec.T
            ratio = float(np.linalg.eigvalsh(inverse_half@bad_energy@inverse_half)[-1])
            bad_edge_ratios.append(ratio/(4*p*M*h) if p else 0.)
            assert ratio <= 4*p*M*h+TOL
            multi = samples[tie_count >= 2]
            mass = float(np.linalg.eigvalsh(multi.T@multi)[-1]) if len(multi) else 0.
            multiple_tie_ratios.append(mass/(p*p*(2*M*h)**2) if p else 0.)
            assert mass <= p*p*(2*M*h)**2+TOL
            cases.append({"m":m,"n":n,"M":M,"mode_dimension":len(modes)})

# Independent finite spectral contact heat bound.
heat_ratios = []
for M in (2, 4, 8):
    modes = list(itertools.combinations_with_replacement(range(1, M+1), 2))
    B = continuum_contact(2, modes, 5*M+3)
    energy = np.array([2*J*math.pi**2*sum(k*k for k in mode) for mode in modes])
    for t in (0.0001, 0.001, 0.01, 0.1):
        weight = np.exp(-t*energy/2)
        norm = float(np.linalg.eigvalsh(weight[:, None]*B*weight[None, :])[-1])
        bound = 1/(2*math.sqrt(math.pi*J*t))
        heat_ratios.append(norm/bound)
        assert norm <= bound+TOL

# Exact matrix rational calculus, including zero embedded-complement modes.
euler_errors, lipschitz_ratios, trace_ratios = [], [], []
def positive_matrix(vals):
    q, _ = np.linalg.qr(RNG.normal(size=(len(vals), len(vals))))
    return (q*vals)@q.T

def function_matrix(a, f):
    vals, q = np.linalg.eigh(a)
    return (q*f(np.maximum(vals, 0)))@q.T

for k in (1, 2, 5, 10, 50):
    x = np.r_[0., np.logspace(-8, 8, 3000)]
    error = float(np.max((1+x/k)**(-k)-np.exp(-x)))
    euler_errors.append(k*error)
    assert error <= 2/k+TOL
for d in (3, 7, 12):
    for trial in range(4):
        tau = 0.3
        r1 = positive_matrix(np.r_[np.zeros(d//3), RNG.random(d-d//3)])
        r2 = positive_matrix(RNG.random(d))
        k = 7
        b1 = function_matrix(r1, lambda x:(k/tau)*x/(1+(k/tau-1)*x))
        b2 = function_matrix(r2, lambda x:(k/tau)*x/(1+(k/tau-1)*x))
        eta = np.linalg.norm(r1-r2, 2)
        ratio = np.linalg.norm(np.linalg.matrix_power(b1,k)-np.linalg.matrix_power(b2,k), 2)/(k*k*eta/tau)
        lipschitz_ratios.append(float(ratio))
        assert ratio <= 1+TOL
        energy = np.sort(RNG.random(d)*10+0.1)
        t1 = positive_matrix(np.exp(-tau*energy))
        t2 = positive_matrix(np.exp(-tau*(RNG.random(d)*14+0.2)))
        omega = np.linalg.norm(t1-t2, 2)
        Bhalf = max(np.sqrt(np.maximum(np.linalg.eigvalsh(t1),0)).sum(),
                    np.sqrt(np.maximum(np.linalg.eigvalsh(t2),0)).sum())
        trace_error = np.linalg.svd(t1-t2, compute_uv=False).sum()
        for K in (0, d//2, d-1):
            R = energy[K]
            bound = (K*omega+2*math.sqrt(2*Bhalf*K*omega)
                     +6*Bhalf*math.exp(-tau*R/4)+2*Bhalf*omega**0.25)
            trace_ratios.append(float(trace_error/bound))
            assert trace_error <= bound+TOL

# Public explicit F_m majorant, no many-body diagonalization.
constant_ratios = []
for jp, gmin, gmax in ((0.1,0.01,0.1),(1.,0.1,2.),(5.,0.03,10.)):
    kstar = 1+math.sqrt(gmax)/2*math.sqrt(math.gamma(0.25)/(4*math.sqrt(math.pi*jp)*math.gamma(0.75)))
    dstar = 1+2*gmax/math.sqrt(2*jp)
    astar = math.sqrt(dstar)*kstar*(2*jp*math.pi**2)**(-0.125)
    zstar = kstar*(2*jp*math.pi**2)**(-0.625)
    tstar = math.sqrt(2)+math.pi/math.sqrt(3)+zstar
    dst = gmin**(-0.5)+math.sqrt(2/jp)
    e0 = 2*math.sqrt(gmax/jp)+gmax/jp
    l0 = e0+2*dst+dst*dst
    es = 8*(1+astar)**2+32*jp*math.pi**2+4*gmax
    us = 2*astar+astar*astar+es+2*tstar+tstar*tstar
    fstar = dst+math.sqrt(us+l0)
    for m in range(1, 101):
        p = m*(m-1)/2
        mf = float(math.factorial(m))
        km = 1+math.sqrt(gmax)/2*math.sqrt(p*math.gamma(0.25)/(2*math.sqrt(math.pi*jp)*math.gamma(0.75)))
        dm = 1+4*gmax*p/math.sqrt(2*jp)
        am = math.sqrt(dm)*km*(2*jp*math.pi**2)**(-0.125)
        zm = km*(2*jp*math.pi**2)**(-0.625)
        tm = math.sqrt(2*(mf-1)*m*(m-1))+math.pi*math.sqrt(m/3)+zm
        d0 = gmin**(-0.5)+math.sqrt(2*m*3**m/jp)
        b0 = math.sqrt(m*3**m/jp)
        em0 = 2*math.sqrt(2*gmax*p)*b0+2*gmax*p*b0*b0
        lm0 = em0+2*d0+d0*d0
        em = 8*m*(1+am)**2+64*jp*math.pi**2*(mf-1)*p*m+16*gmax*mf*m*p*p
        um = 2*am+am*am+em+2*tm+tm*tm
        fm = d0+math.sqrt(um+lm0)
        major = fstar*(m+1)**3*math.sqrt(mf)*3**(m/2)
        constant_ratios.append(fm/major)
        assert fm <= major*(1+1e-12)

out = {"status":"FINITE-EVIDENCE","all_checks_passed":True,
       "low_sine_cases":len(cases),"m_range":[1,4],"n_values":[4,5,7],"M_values":[1,2],
       "max_exact_contact_quadrature_error":max(quadrature_errors),
       "min_Gram_majorant_margin":min(gram_margins),
       "min_cell_recovery_norm_margin":min(recovery_margins),
       "min_bad_edge_kinetic_form_margin":min(kinetic_margins),
       "min_multiple_tie_contact_form_margin":min(contact_margins),
       "min_total_recovery_form_margin":min(total_margins),
       "max_bad_edge_ratio_over_bound":max(bad_edge_ratios),
       "max_multiple_tie_mass_over_bound":max(multiple_tie_ratios),
       "contact_heat_cases":len(heat_ratios),"max_contact_heat_ratio":max(heat_ratios),
       "Euler_scalar_cases":len(euler_errors),"max_k_times_Euler_error":max(euler_errors),
       "rational_matrix_cases":len(lipschitz_ratios),"max_rational_Lipschitz_ratio":max(lipschitz_ratios),
       "positive_trace_cases":len(trace_ratios),"max_positive_trace_upgrade_ratio":max(trace_ratios),
       "explicit_majorant_cases":len(constant_ratios),"max_Fm_majorant_ratio":max(constant_ratios),
       "limitation":"Finite sampled algebra only; no external validation, asymptotic theorem test or practical L threshold.",
       "cases":cases}
Path(__file__).with_suffix(".json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({k:v for k,v in out.items() if k!="cases"},indent=2))
