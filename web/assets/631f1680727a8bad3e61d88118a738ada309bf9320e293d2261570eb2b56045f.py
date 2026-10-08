"""Scoped finite checks of the nodal interpolation/contact lemma.
NumPy only, deterministic quadrature exact for the relevant Q1 polynomials.
Run: OPENBLAS_NUM_THREADS=1 python3 outputs/research/sol_attractive_critical/continuum_checks.py
These checks are not a proof of convergence, external validation or priority.
"""
import itertools
import json
import math
from pathlib import Path
import numpy as np

RNG = np.random.default_rng(8102026)
TOL = 2e-9


def tensor_quadrature(dim, intervals, order=3):
    """Product Gauss rule, split at every supplied interval boundary."""
    a, b = np.array(intervals[:-1]), np.array(intervals[1:])
    x, w = np.polynomial.legendre.leggauss(order)
    nodes = ((a[:, None]+b[:, None])/2
             +(b-a)[:, None]*x[None, :]/2).ravel()
    weights = ((b-a)[:, None]*w[None, :]/2).ravel()
    indices = list(itertools.product(range(len(nodes)), repeat=dim))
    ix = np.array(indices, dtype=int)
    return nodes[ix], np.prod(weights[ix], axis=1)


def interpolate(u, h, points):
    dim = u.ndim
    n = u.shape[0]-2
    base = np.minimum(np.floor(points/h).astype(int), n)
    t = points/h-base
    val = np.zeros(len(points), dtype=complex)
    grad = np.zeros((len(points), dim), dtype=complex)
    for bits in itertools.product((0, 1), repeat=dim):
        bits = np.array(bits)
        z = base+bits
        uz = u[tuple(z.T)]
        factors = np.where(bits[None, :] == 1, t, 1-t)
        val += uz*np.prod(factors, axis=1)
        for axis in range(dim):
            transverse = np.delete(factors, axis, axis=1)
            grad[:, axis] += (uz*(1 if bits[axis] else -1)
                             *np.prod(transverse, axis=1)/h)
    return val, grad


def nearest_step(u, h, points):
    z = np.floor(points/h+0.5).astype(int)
    return u[tuple(z.T)]


cases = []
for dim in (2, 3):
    for n in range(1, 5):
        h = 1/(n+1)
        for trial in range(2):
            u = np.zeros((n+2,)*dim, dtype=complex)
            interior = tuple(slice(1, n+1) for _ in range(dim))
            u[interior] = (RNG.normal(size=(n,)*dim)
                           +1j*RNG.normal(size=(n,)*dim))
            eh = h**(dim-2)*sum(float((np.abs(np.diff(u, axis=i))**2).sum())
                                for i in range(dim))
            # Break at half-grid steps: both interpolation cells and
            # nearest-node discontinuities are then resolved.
            boundaries = np.arange(2*(n+1)+1)*h/2
            points, weights = tensor_quadrature(dim, boundaries)
            vals, grad = interpolate(u, h, points)
            kinetic = float(weights @ (np.abs(grad)**2).sum(axis=1))
            bulk_error = float(weights @ np.abs(vals-nearest_step(u,h,points))**2)
            dp, dw = tensor_quadrature(dim-1, boundaries)
            trace_errors, trace_norm_errors = [], []
            for i in range(dim):
                for j in range(i+1, dim):
                    full = np.zeros((len(dp), dim))
                    full[:, i] = dp[:, 0]
                    full[:, j] = dp[:, 0]
                    others = [a for a in range(dim) if a not in (i,j)]
                    for a, coordinate in enumerate(others, start=1):
                        full[:, coordinate] = dp[:, a]
                    trace, _ = interpolate(u, h, full)
                    step = nearest_step(u, h, full)
                    trace_errors.append(float(dw @ np.abs(trace-step)**2))
                    # Check the collapsed step normalization independently.
                    nodal = 0.
                    for z in itertools.product(range(1,n+1),repeat=dim):
                        if z[i] == z[j]:
                            nodal += abs(u[z])**2*h**(dim-1)
                    trace_norm_errors.append(abs(float(dw @ np.abs(step)**2)-nodal))
            const = dim*3**dim
            assert kinetic <= eh+TOL
            assert bulk_error <= const*h*h*eh+TOL
            assert max(trace_errors) <= const*h*eh+TOL
            assert max(trace_norm_errors) <= TOL
            cases.append({"dimension":dim,"n":n,"trial":trial,
                          "gradient_over_Eh":kinetic/eh,
                          "bulk_error_over_bound":bulk_error/(const*h*h*eh),
                          "max_contact_error_over_bound":max(trace_errors)/(const*h*eh),
                          "max_exact_collapsed_norm_error":max(trace_norm_errors)})

# All tie multiplicities at modest dimension; these include triples and
# several independent pair ties. Check exact U/K norms and contact counts.
counts = 0
min_contact_margin = math.inf
max_gram_error = 0.
for dim in range(1, 8):
    for n in range(1, 6):
        for y in itertools.combinations_with_replacement(range(n), dim):
            rs = [y.count(v) for v in set(y)]
            t = math.prod(math.factorial(r) for r in rs)
            w = math.factorial(dim)//t
            W = sum(r-1 for r in rs)
            P = sum(r*(r-1)//2 for r in rs)
            margin = W-2*P/t
            min_contact_margin = min(min_contact_margin, margin)
            assert margin >= -TOL
            max_gram_error = max(max_gram_error,
                                 abs(w*(1/math.sqrt(w))**2-1))
            assert abs(w/math.factorial(dim)-1/t) <= TOL
            counts += 1

out = {"status":"FINITE-EVIDENCE","all_checks_passed":True,
       "interpolation_cases":len(cases),
       "max_gradient_over_Eh":max(x["gradient_over_Eh"] for x in cases),
       "max_bulk_error_over_bound":max(x["bulk_error_over_bound"] for x in cases),
       "max_contact_error_over_bound":max(x["max_contact_error_over_bound"] for x in cases),
       "max_collapsed_norm_error":max(x["max_exact_collapsed_norm_error"] for x in cases),
       "multiplicity_cases":counts,"min_contact_margin":min_contact_margin,
       "max_polar_gram_error":max_gram_error,
       "cases":cases,
       "limitation":"Finite nodal algebra only; not whole-Fock trace convergence or external proof validation."}
Path(__file__).with_suffix(".json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({k:v for k,v in out.items() if k!="cases"},indent=2))
