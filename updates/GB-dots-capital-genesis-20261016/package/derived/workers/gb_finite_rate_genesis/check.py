#!/usr/bin/env python3
"""Self-authored finite checks; no source/author code and no installs/network.

Exact symbolic identities and floating-point examples corroborate, but do not
prove, SHARP_POISSON_SYNDROME_THEOREM.md or its imported memory obligations.
Requires installed NumPy and SymPy; deliberately does not require SciPy.
"""
from __future__ import annotations

import itertools
import json
import math
from pathlib import Path
import platform
import sys
import time

import numpy as np
import sympy as sp

OUT = Path(__file__).resolve().parent
SEED = 16102026073
I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.diag([1, -1]).astype(complex)


def tensor(*factors):
    ans = np.ones((1, 1), dtype=complex)
    for f in factors:
        ans = np.kron(ans, f)
    return ans


def expm(a):
    """Scaling/squaring Taylor exponential, checked below against Hermitian eigh."""
    n = len(a)
    norm = float(np.linalg.norm(a, 1))
    s = max(0, int(math.ceil(math.log2(norm / 0.5)))) if norm else 0
    x = a / (2.0**s)
    total = np.eye(n, dtype=complex)
    term = total.copy()
    for k in range(1, 100):
        term = term @ x / k
        total += term
        if np.linalg.norm(term, 1) < 2e-17:
            break
    else:
        raise AssertionError("Taylor exponential did not converge")
    for _ in range(s):
        total = total @ total
    return total


def vec(a):
    return a.reshape(-1, order="F")


def unvec(v, d):
    return v.reshape((d, d), order="F")


def herm(rng, d):
    a = rng.normal(size=(d, d)) + 1j * rng.normal(size=(d, d))
    return (a + a.conj().T) / 2


def opnorm(a):
    return float(np.linalg.norm(a, 2))


def epsilon(j, gamma, t):
    # Stable near gamma*t=0.
    x = 2 * gamma * t
    if abs(x) < 1e-4:
        f = 1 - x / 3 + x*x / 12 - x*x*x / 60 + x**4 / 360
        return j*j*t*t*f
    return j*j*t*t * 2 * (x + math.expm1(-x)) / (x*x)


def exact_checks():
    g, r, h = sp.symbols("g r h", positive=True, real=True)
    gx, gy, gz = sp.symbols("gx gy gz", nonnegative=True, real=True)
    sid = sp.eye(2)
    sx = sp.Matrix([[0, 1], [1, 0]])
    sy = sp.Matrix([[0, -sp.I], [sp.I, 0]])
    sz = sp.diag(1, -1)
    sab = [sp.kronecker_product(p, sid) for p in (sx, sy, sz)]
    hmat = h * sp.kronecker_product(sz, sz)

    def nmap(a):
        ans = a
        for rate, pauli in zip((gx, gy, gz), sab):
            ans += rate/r * (pauli*a*pauli-a)
        ans += -sp.I/r * (hmat*a-a*hmat)
        return ans

    # Normalized Choi in input-output ordering.
    choi = sp.zeros(16)
    for a in range(4):
        for b in range(4):
            e = sp.zeros(4)
            e[a, b] = 1
            choi += sp.kronecker_product(e, nmap(e))/4
    u = sp.Matrix([1 if a == b else 0 for a in range(4) for b in range(4)])/2
    zz = sp.kronecker_product(sz, sz)
    v = sp.Matrix([zz[b, a] for a in range(4) for b in range(4)])/2
    basis = sp.Matrix.hstack(u, v)
    compression = sp.simplify(basis.conjugate().T*choi*basis)
    assert sp.simplify(compression[1, 1]) == 0
    determinant = sp.factor(compression.det())
    assert determinant == -h*h/(r*r)

    lam, tau, a, n = sp.symbols("lam tau a n", positive=True, real=True)
    s, t, x, uvar, vvar = sp.symbols("s t x uvar vvar", real=True)
    gap_integral = sp.simplify(2*sp.integrate(sp.integrate(
        sp.exp(-lam*(t-s)), (s, 0, t)), (t, 0, tau)))
    gap_formula = 2*(tau/lam-(1-sp.exp(-lam*tau))/(lam*lam))
    assert sp.simplify(gap_integral-gap_formula) == 0
    poisson_moment = sp.simplify(2*sp.exp(-lam)*sp.integrate(
        x*sp.exp(lam*x), (x, 0, 1)))
    assert sp.simplify(poisson_moment-2*(lam-1+sp.exp(-lam))/lam**2) == 0

    # Constant potential of the certificate-minimizing measure.
    potential = a/(lam+2) * (
        sp.integrate(sp.exp(-(uvar-vvar)), (vvar, 0, uvar))
        + sp.integrate(sp.exp(-(vvar-uvar)), (vvar, uvar, lam))
        + sp.exp(-uvar)+sp.exp(-(lam-uvar)))
    assert sp.simplify(potential-2*a/(lam+2)) == 0
    incumbent_gap = sp.factor(2/(n+2)-1/(n+1))
    assert incumbent_gap == n/((n+1)*(n+2))
    dephaser_identity = sp.simplify(g*(sp.kronecker_product(sz, sz)-sp.eye(4))
        -2*g*((sp.eye(4)+sp.kronecker_product(sz, sz))/2-sp.eye(4)))
    assert dephaser_identity == sp.zeros(4)

    # Full-group Choi rank/freshness example: two independent Pauli generators.
    weights = [sp.Rational(3, 4)] + [sp.Rational(1, 12)]*3
    assert sum(weights) == 1 and all(w > 0 for w in weights)
    tensor_weights = [sp.prod(ws) for ws in itertools.product(weights, repeat=3)]
    assert len(tensor_weights) == 64 and all(w > 0 for w in tensor_weights)
    return {
        "status": "PASS",
        "memory_only_randomizer_choi_compression": str(compression),
        "choi_compression_determinant": str(determinant),
        "poisson_gap_square_expectation": str(gap_integral),
        "fixed_count_poisson_average": str(poisson_moment),
        "optimal_exposure_potential": str(sp.simplify(potential)),
        "deterministic_incumbent_certificate_gap": str(incumbent_gap),
        "generator_factor_two_identity": True,
        "fresh_process_rank_three_two_generator_intervals": 64,
    }


def model(rng, k, js, bath_d=2, baseline_scale=5.0):
    data_d = 2**k
    d = data_d*bath_d
    h0 = np.zeros((d, d), dtype=complex)
    for label in range(data_d):
        block = herm(rng, bath_d)
        block *= baseline_scale/max(1e-14, opnorm(block))
        h0[label*bath_d:(label+1)*bath_d,
           label*bath_d:(label+1)*bath_d] = block
    vs = []
    for i, ji in enumerate(js):
        bit = 1 << (k-1-i)
        v = np.zeros_like(h0)
        for label in range(data_d):
            if label & bit:
                continue
            other = label ^ bit
            block = rng.normal(size=(bath_d, bath_d)) + 1j*rng.normal(size=(bath_d, bath_d))
            lo = slice(label*bath_d, (label+1)*bath_d)
            hi = slice(other*bath_d, (other+1)*bath_d)
            v[lo, hi] = block
            v[hi, lo] = block.conj().T
        v *= ji/opnorm(v)
        vs.append(v)
    zs = [tensor(*(Z if q == i else I2 for q in range(k)), np.eye(bath_d))
          for i in range(k)]
    for i, v in enumerate(vs):
        assert opnorm(zs[i]@v+v@zs[i]) < 1e-12
        for q in range(k):
            if q != i:
                assert opnorm(zs[q]@v-v@zs[q]) < 1e-12
    return h0, vs, zs


def generator(h, zs, gammas):
    d = len(h)
    ident = np.eye(d)
    out = -1j*(np.kron(ident, h)-np.kron(h.T, ident))
    for z, g in zip(zs, gammas):
        out += g*(np.kron(z.conj(), z)-np.eye(d*d))
    return out


def endpoint_checks():
    rng = np.random.default_rng(SEED)
    max_ratio = 0.0
    worst = None
    total_subset_effects = 0
    max_trace_defect = 0.0
    max_exp_defect = 0.0
    cases = []
    # Direct scaling/squaring checks against known Hermitian exponentials.
    for scale in (0.01, 1., 50.):
        h = herm(rng, 8)*scale
        values, vectors = np.linalg.eigh(h)
        exact = (vectors*np.exp(-1j*values))@vectors.conj().T
        defect = opnorm(expm(-1j*h)-exact)
        max_exp_defect = max(max_exp_defect, defect)
        assert defect < 5e-12

    # Every effect optimizes over the full arbitrary bath input, rather than
    # taking one bath preparation or an averaged Choi trace.
    for k, trials in ((2, 36), (3, 4)):
        bath_d = 2
        d = 2**k*bath_d
        for trial in range(trials):
            js = rng.uniform(0.05, 0.65, k)
            gammas = rng.uniform(0.15, 5., k)
            duration = float(rng.uniform(0.01, 1.4))
            segments = 3 if trial % 2 else 1
            fractions = rng.dirichlet(np.ones(segments))
            channel = np.eye(d*d, dtype=complex)
            baseline_scale = 40.0 if trial % 7 == 0 else 3.0
            for fraction in fractions:
                h0, vs, zs = model(rng, k, js, baseline_scale=baseline_scale)
                channel = expm(generator(h0+sum(vs), zs, gammas)*duration*fraction)@channel
            identity = vec(np.eye(d))
            trace_defect = np.linalg.norm(channel.conj().T@identity-identity)
            max_trace_defect = max(max_trace_defect, float(trace_defect))
            assert trace_defect < 5e-11
            bounds = [min(1.,epsilon(j,g,duration)) for j,g in zip(js,gammas)]
            initial = slice(0,bath_d)  # fixed all-plus data sector, arbitrary bath.
            for mask in range(1,2**k):
                selected = [i for i in range(k) if mask & (1 << i)]
                diagonal = []
                for label in range(2**k):
                    flipped = all(label & (1 << (k-1-i)) for i in selected)
                    diagonal.extend([float(flipped)]*bath_d)
                projector = np.diag(diagonal)
                effect = unvec(channel.conj().T@vec(projector),d)
                compressed = effect[initial,initial]
                compressed = (compressed+compressed.conj().T)/2
                eigen = float(np.linalg.eigvalsh(compressed).max())
                bound = float(math.prod(bounds[i] for i in selected))
                ratio = eigen/bound if bound else 0.
                assert eigen <= bound+3e-12, (k,trial,selected,eigen,bound)
                total_subset_effects += 1
                if ratio > max_ratio:
                    max_ratio = ratio
                    worst = {"k":k,"trial":trial,"selected":selected,
                             "effect_max_eigenvalue":eigen,"sharp_product_bound":bound,
                             "duration":duration,"J":js.tolist(),
                             "gamma":gammas.tolist(),"segments":segments,
                             "baseline_scale":baseline_scale}
            cases.append({"k":k,"trial":trial,"segments":segments})
    return {"status":"PASS","seed":SEED,"cases":len(cases),
            "subset_effect_checks":total_subset_effects,
            "max_effect_to_sharp_product_ratio":max_ratio,"worst_case":worst,
            "max_trace_preservation_defect":max_trace_defect,
            "matrix_exp_crosscheck_defect":max_exp_defect,
            "numeric_scope":"finite seeded examples; not a proof or hardware benchmark"}


def fixed_cut_checks():
    rng = np.random.default_rng(SEED+1)
    js = [0.21,0.17]
    h0,vs,zs = model(rng,2,js,baseline_scale=6.)
    h = h0+sum(vs)
    d = len(h)
    duration = 0.8
    initial = tensor((I2+Z)/2,(I2+Z)/2,I2)
    patterns = [([0.18,0.56],[0.31,0.62]),
                ([],[0.2]),([0.1],[0.15]),
                ([0.05,0.2],[0.42,0.58])]
    worst_ratio = 0.
    max_completeness_defect = 0.
    checks = 0
    for cuts in patterns:
        events = sorted([(t,i) for i,ts in enumerate(cuts) for t in ts]
                        +[(duration,0),(duration,1)])
        branches = [(initial.copy(),(1,1),(False,False))]
        previous = 0.
        for t,i in events:
            u = expm(-1j*h*(t-previous))
            new = []
            for kraus,last,bad in branches:
                for label in (1,-1):
                    p = (np.eye(d)+label*zs[i])/2
                    out = p@u@kraus
                    nlast = list(last)
                    nbad = list(bad)
                    nbad[i] = bad[i] or label != last[i]
                    nlast[i] = label
                    new.append((out,tuple(nlast),tuple(nbad)))
            branches = new
            previous = t
        complete = sum(k.conj().T@k for k,_,_ in branches)
        defect = opnorm(complete-initial)
        max_completeness_defect = max(max_completeness_defect,defect)
        assert defect < 5e-12
        conditional = []
        for ji,ts in zip(js,cuts):
            points = [0.]+list(ts)+[duration]
            conditional.append(ji*ji*sum((b-a)**2 for a,b in zip(points,points[1:])))
        for mask in (1,2,3):
            selected = [i for i in range(2) if mask & (1 << i)]
            effect = sum((k.conj().T@k for k,_,bad in branches
                          if all(bad[i] for i in selected)), np.zeros((d,d),dtype=complex))
            compressed = effect[:2,:2]
            eigen = float(np.linalg.eigvalsh((compressed+compressed.conj().T)/2).max())
            bound = math.prod(conditional[i] for i in selected)
            assert eigen <= bound+3e-13
            worst_ratio = max(worst_ratio,eigen/bound)
            checks += 1
    return {"status":"PASS","patterns":len(patterns),"subset_checks":checks,
            "max_conditional_effect_to_bound_ratio":worst_ratio,
            "max_kraus_completeness_defect":max_completeness_defect,
            "scope":"actual projective Kraus branches; arbitrary bath effect"}


def exposure_numeric_checks():
    # Midpoint quadrature of the exact finite-peak optimizer, plus closed-form
    # count-cap expressions. No physical measurement cost is fitted.
    cases = []
    ngrid = 600
    times = (np.arange(ngrid)+.5)/ngrid
    for intensity in (0.,0.1,1.,3.,10.):
        h = 1/(intensity+2)
        exposure = np.clip((times-h)*(intensity+2),0,intensity)
        numerical = float(np.exp(-np.abs(exposure[:,None]-exposure[None,:])).mean())
        optimum = 2/(intensity+2)
        assert abs(numerical-optimum) < 2e-5
        constant = 1. if intensity == 0 else 2*(intensity-1+math.exp(-intensity))/intensity**2
        assert constant >= optimum-1e-12
        cases.append({"Lambda":intensity,"optimum":optimum,
                      "quadrature":numerical,"constant_rate_certificate":constant})
    return {"status":"PASS","quadrature_grid":ngrid,"cases":cases}


def virtual_seed_checks():
    rng=np.random.default_rng(SEED+2)
    physical_d=2
    hbase=herm(rng,physical_d)
    interactions=[herm(rng,physical_d)*0.2,herm(rng,physical_d)*0.3]
    xseeds=[tensor(X,I2),tensor(I2,X)]
    zseeds=[tensor(Z,I2),tensor(I2,Z)]
    virtual_h=tensor(np.eye(4),hbase)+sum(
        tensor(xseed,a) for xseed,a in zip(xseeds,interactions))
    patterns=[([],[]),([0.12],[0.3,0.61]),([0.2,0.51],[0.11]),
              ([0.1,0.2],[0.4,0.6])]
    duration=0.8
    largest=0.
    comparisons=0
    for cuts in patterns:
        events=sorted((t,i) for i,ts in enumerate(cuts) for t in ts)
        uvirtual=np.eye(4*physical_d,dtype=complex)
        previous=0.
        for t,i in events:
            uvirtual=tensor(zseeds[i],np.eye(physical_d))@expm(
                -1j*virtual_h*(t-previous))@uvirtual
            previous=t
        uvirtual=expm(-1j*virtual_h*(duration-previous))@uvirtual
        uf={}
        for f in itertools.product((0,1),repeat=2):
            signs=[(-1)**x for x in f]
            u=np.eye(physical_d,dtype=complex)
            previous=0.
            for t,i in events+[(duration,None)]:
                h=hbase+sum(sign*a for sign,a in zip(signs,interactions))
                u=expm(-1j*h*(t-previous))@u
                if i is not None:
                    signs[i]*=-1
                previous=t
            uf[f]=u
        for z in itertools.product((0,1),repeat=2):
            label=2*z[0]+z[1]
            actual=uvirtual[label*physical_d:(label+1)*physical_d,:physical_d]
            walsh=sum(((-1)**sum(fi*zi for fi,zi in zip(f,z)))*u
                      for f,u in uf.items())/4
            phase=(-1)**sum(len(ts)*zi for ts,zi in zip(cuts,z))
            defect=opnorm(actual-phase*walsh)
            largest=max(largest,defect)
            comparisons+=1
            assert defect < 3e-12
    return {"status":"PASS","patterns":len(patterns),
            "walsh_to_virtual_seed_kraus_comparisons":comparisons,
            "maximum_operator_defect":largest}


def main():
    started=time.perf_counter()
    result={"status":"RUNNING","python":sys.version,"executable":sys.executable,
            "numpy":np.__version__,"sympy":sp.__version__,"platform":platform.platform(),
            "authorship":"self-authored; no supplied or primary author code executed"}
    result["exact"]=exact_checks()
    result["fixed_cut_instruments"]=fixed_cut_checks()
    result["endpoint_effects"]=endpoint_checks()
    result["exposure_certificate"]=exposure_numeric_checks()
    result["virtual_seed_representation"]=virtual_seed_checks()
    result["elapsed_seconds"]=time.perf_counter()-started
    result["status"]="PASS"
    (OUT/"CHECK_RESULTS.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))


if __name__ == "__main__":
    main()
