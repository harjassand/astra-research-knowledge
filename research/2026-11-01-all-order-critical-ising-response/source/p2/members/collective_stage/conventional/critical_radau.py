"""Classical two-moment Gauss--Radau bounds for the collective Ising response.

The microscopic degree-three compiler is explicitly reused from root/critical_response.py.
This file adds no target-process approximation: it evaluates the sharp classical
moment bounds using exact rational endpoints for the acquired reference scalar.
Floating LU only proposes a vector whose error is checked with integer arithmetic.

Primary quadrature source: Gene H. Golub, Matrix Computation and the Theory of
Moments, https://web.stanford.edu/class/cme324/mmq2.pdf , Theorem 2.
"""
import os
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
from fractions import Fraction as F
import importlib.util
import json
from pathlib import Path
import sys
import time

import numpy as np
from scipy.sparse.linalg import splu

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

SOURCE = Path(__file__).resolve().parents[1] / "root" / "critical_response.py"
spec = importlib.util.spec_from_file_location("root_critical_compiler", SOURCE)
compiler = importlib.util.module_from_spec(spec)
spec.loader.exec_module(compiler)


def radau(chi0, ritz, residual_lower, residual_upper, m=F(1), M=F(2)):
    """Exact endpoints. Inputs are fractions; residual interval encloses r K0^-1 r.

    Here f is a K0 eigenvector and r=f-K*(<f,f>/<f,Kf>)*f.
    For more general f supply the first two B=K0^-1/2 K K0^-1/2 moments directly.
    """
    a = chi0 / ritz
    if a == m or a == M:
        assert residual_lower <= 0 <= residual_upper
        return chi0 / a, chi0 / a, a, F(0), F(0)
    assert m < a < M
    v_lower = max(F(0), a*a*residual_lower/chi0)
    v_upper = min((a-m)*(M-a), a*a*residual_upper/chi0)
    assert 0 <= v_lower <= v_upper

    def endpoint(c, v):
        # Algebraic form avoids separately computing the second quadrature node.
        return chi0 * (a-c+v/c) / (a*(a-c)+v)

    return endpoint(M, v_lower), endpoint(m, v_upper), a, v_lower, v_upper


def microscopic_data(n, bits=100, refinements=2):
    """Acquire the scalar via the shared exact degree-three reference construction."""
    problem = compiler.build(n)
    dim = len(problem["triples"])
    rhs = np.zeros(dim); rhs[problem["ti"]] = 1
    lu = splu(problem["H"])
    scale = 1 << bits
    xnum = [round(float(x)*scale) for x in lu.solve(rhs)]
    for _ in range(refinements):
        residue = compiler.exact_residual(problem, xnum, bits)
        correction = lu.solve(np.array([float(F(z, problem["den"]*scale)) for z in residue]))
        xnum = [x+round(float(z)*scale) for x, z in zip(xnum, correction)]
    residue = compiler.exact_residual(problem, xnum, bits)
    residue_one = F(sum(map(abs, residue)), problem["den"]*scale)
    gamma = F(n*n-1, n*n+1)
    variance = F(problem["gm"][0], problem["cden"])
    cross = F(problem["gt"][0], problem["cden"])
    energy = (F(3, 2)-gamma)*variance-F(1, 2)*cross
    trial = variance/energy
    ritz = variance*trial
    chi0 = variance/(1-gamma)
    gn = [problem["gt"][j+1]*problem["gm"][0]-problem["gt"][0]*problem["gm"][j+1]
          for j in range(dim)]
    gd = problem["cden"]*problem["gm"][0]
    scalar = F(sum(g*x for g, x in zip(gn, xnum)), gd*scale)
    scalar_error = F(max(map(abs, gn)), gd)*residue_one/(3*(1-gamma))
    multiplier = (trial/2)**2
    rlower = multiplier*max(F(0), scalar-scalar_error)
    rupper = multiplier*max(F(0), scalar+scalar_error)
    return chi0, ritz, rlower, rupper, dim, scalar_error


def fraction_pair(x):
    return [str(x.numerator), str(x.denominator)]


def solve(n):
    start = time.perf_counter()
    chi0, ritz, rlower, rupper, dim, scalar_error = microscopic_data(n)
    lower, upper, a, vlower, vupper = radau(chi0, ritz, rlower, rupper)
    midpoint = (lower+upper)/2
    v = (vlower+vupper)/2
    vmax = (a-1)*(2-a)
    result = {
        "n": n,
        "reference_triple_orbits": dim,
        "microscopic_model": "periodic zero-field Ising; exp(2J)=n; clocks=1; A_same=1,A_opposite=2",
        "lower": float(lower), "upper": float(upper),
        "relative_width": float((upper-lower)/lower),
        "midpoint": float(midpoint),
        "midpoint_relative_error_certificate": float((upper-lower)/(lower+upper)),
        "lower_fraction": fraction_pair(lower), "upper_fraction": fraction_pair(upper),
        "reference_response": float(chi0), "unimproved_ritz": float(ritz),
        "original_relative_width": float(rupper/ritz),
        "normalized_spectral_mean": float(a), "normalized_spectral_variance": float(v),
        "variance_deficit_from_endpoint_measure": float(vmax-v),
        "reference_scalar_error_bound": float(scalar_error),
        "seconds": time.perf_counter()-start,
        "status": "Exact rational endpoints; classical two-moment Gauss--Radau; shared microscopic degree-three compiler"
    }
    return result


def check_dense():
    path = Path(__file__).with_name("critical_ising_dense_results.json")
    rows = []
    for row in json.loads(path.read_text()):
        # This audit deliberately evaluates the same moment formulas from the
        # independent full-spin-space floating solve. It is not a new certificate.
        c0, L, R = row["glauber_response"], row["linear_ritz_lower"], row["reference_residual_norm"]
        a = c0/L; v = a*a*R/c0
        def q(c): return c0*(a-c+v/c)/(a*(a-c)+v)
        lower, upper = q(2), q(1)
        exact = row["exact_response"]
        assert lower <= exact*(1+1e-11) and exact <= upper*(1+1e-11)
        rows.append({"n": row["n"], "direct_response": exact,
                     "radau_lower": lower, "radau_upper": upper,
                     "relative_width": (upper-lower)/lower,
                     "midpoint_relative_error": abs((lower+upper)/2-exact)/exact})
    return rows


if __name__ == "__main__":
    results = {"independent_dense_audit": check_dense(), "exact_rational_enclosures": []}
    for n in [8, 16, 32, 64, 128, 256]:
        result = solve(n)
        results["exact_rational_enclosures"].append(result)
        print(json.dumps({k: result[k] for k in ["n", "reference_triple_orbits", "lower", "upper", "relative_width", "seconds"]}), flush=True)
        Path(__file__).with_name("critical_radau_results.json").write_text(json.dumps(results, indent=2)+"\n")
