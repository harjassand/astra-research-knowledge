"""Exact finite-arithmetic instance of cumulative Nystrom acquisition.

Only the Python standard library is needed.  All data and arithmetic are
Fraction values; Rademacher signs use reproducible pseudorandom bits in this
demonstration.  The probabilistic theorem assumes independent random bits.
This program is a finite fixture, not a physical experiment or a timing claim.
"""
from fractions import Fraction as F
from pathlib import Path
import json
import math
import random
import time


COUNTS = {"fraction_add": 0, "fraction_mul": 0, "fraction_div": 0,
          "max_recorded_numerator_bits": 0, "max_recorded_denominator_bits": 0}


def watch(x):
    COUNTS["max_recorded_numerator_bits"] = max(COUNTS["max_recorded_numerator_bits"], abs(x.numerator).bit_length())
    COUNTS["max_recorded_denominator_bits"] = max(COUNTS["max_recorded_denominator_bits"], x.denominator.bit_length())
    return x


def add(a, b):
    COUNTS["fraction_add"] += 1
    return watch(a + b)


def mul(a, b):
    COUNTS["fraction_mul"] += 1
    return watch(a * b)


def div(a, b):
    COUNTS["fraction_div"] += 1
    return watch(a / b)


def dot(x, y):
    z = F(0)
    for a, b in zip(x, y):
        z = add(z, mul(a, b))
    return z


def mv(a, x):
    return [dot(row, x) for row in a]


def lincomb(cols, weights, n):
    return [dot([col[i] for col in cols], weights) for i in range(n)]


def inverse(a):
    n = len(a)
    w = [list(row) + [F(i == j) for j in range(n)] for i, row in enumerate(a)]
    for k in range(n):
        pivot = next(i for i in range(k, n) if w[i][k])
        w[k], w[pivot] = w[pivot], w[k]
        scale = w[k][k]
        w[k] = [div(z, scale) for z in w[k]]
        for i in range(n):
            if i == k:
                continue
            coeff = w[i][k]
            w[i] = [add(z, -mul(coeff, y)) for z, y in zip(w[i], w[k])]
    return [row[n:] for row in w]


def determinant(a):
    w=[list(row) for row in a]
    answer=F(1)
    for k in range(len(w)):
        pivot=next((i for i in range(k,len(w)) if w[i][k]),None)
        if pivot is None:
            return F(0)
        if pivot!=k:
            w[k],w[pivot]=w[pivot],w[k];answer=-answer
        value=w[k][k];answer=mul(answer,value)
        for i in range(k+1,len(w)):
            ratio=div(w[i][k],value)
            for j in range(k+1,len(w)):
                w[i][j]=add(w[i][j],-mul(ratio,w[k][j]))
    return answer


def positive_principal_indices(s):
    """Exact PSD elimination; source PSD is a premise, not inferred here."""
    chosen = []
    for i in range(len(s)):
        if not chosen:
            schur = s[i][i]
        else:
            block = [[s[j][k] for k in chosen] for j in chosen]
            c = [s[j][i] for j in chosen]
            schur = add(s[i][i], -dot(c, mv(inverse(block), c)))
        if schur < 0:
            raise ValueError("Source PSD contract or exact arithmetic violated")
        if schur > 0:
            chosen.append(i)
    return chosen


class ExactSource:
    def __init__(self, components):
        self._components = components
        self.n = len(components[0])
        self.m = len(components)
        self.calls = {"cache": 0, "certificate": 0, "solve": 0}
        self.input_output_max_bits = 0

    def apply(self, j, x, category):
        self.calls[category] += 1
        y = mv(self._components[j], x)
        self.input_output_max_bits = max(self.input_output_max_bits,
            max(max(abs(z.numerator).bit_length(), z.denominator.bit_length()) for z in x+y))
        return y

    def combined(self, theta, x, category):
        result = [F(0)] * self.n
        for j, coeff in enumerate(theta):
            if coeff:
                y = self.apply(j, x, category)
                result = [add(a, mul(coeff, b)) for a, b in zip(result, y)]
        return result


class Library:
    def __init__(self, source):
        self.source = source
        self.v = []
        self.f = [[] for _ in range(source.m)]
        self.total_stages = 0
        self.certified_boxes = []

    def append(self, v):
        assert all(dot(old, v) == 0 for old in self.v)
        assert dot(v, v) > 0
        scale = max(abs(z) for z in v)
        v = [div(z, scale) for z in v]
        self.v.append(v)
        for j in range(self.source.m):
            self.f[j].append(self.source.apply(j, v, "cache"))

    def build(self, theta, lam):
        n, d = self.source.n, len(self.v)
        cols = [[dot([self.f[j][k][i] for j in range(self.source.m)], theta)
                 for i in range(n)] for k in range(d)]
        s = [[dot(v, col) for col in cols] for v in self.v]
        inds = positive_principal_indices(s)
        cols = [cols[i] for i in inds]
        s = [[s[i][j] for j in inds] for i in inds]
        sinv = inverse(s) if s else []
        h = [[add(mul(lam, s[i][j]), dot(cols[i], cols[j]))
              for j in range(len(cols))] for i in range(len(cols))]
        hinv = inverse(h) if h else []

        def nystrom(x):
            return lincomb(cols, mv(sinv, [dot(col, x) for col in cols]), n)

        def precondition(x):
            corr = lincomb(cols, mv(hinv, [dot(col, x) for col in cols]), n)
            return [div(add(a, -b), lam) for a, b in zip(x, corr)]

        def residual(x):
            raw = self.source.combined(theta, x, "certificate")
            return [add(a, -b) for a, b in zip(raw, nystrom(x))]

        return nystrom, precondition, residual


def acquire(lib, theta, mu, delta, rng):
    if any(mu >= old_mu and all(a <= b for a,b in zip(theta,upper))
           for upper,old_mu in lib.certified_boxes):
        return []
    alpha = F(1, 16)
    fail_one = F(181, 256)
    q = 1
    while 4**q < lib.source.n / alpha:
        q += 1
    stages = []
    while True:
        lib.total_stages += 1
        stage = lib.total_stages
        delta_s = delta / (stage * (stage + 1))
        probes = 1
        while fail_one**probes > delta_s:
            probes += 1
        _, _, residual = lib.build(theta, mu)
        best, bestnorm = None, F(-1)
        before = dict(lib.source.calls)
        threshold = alpha * (mu / 2)**(2*q)
        used_probes = 0
        for _ in range(probes):
            v = [F(rng.choice((-1, 1))) for _ in range(lib.source.n)]
            for __ in range(q):
                v = residual(v)
            norm = dot(v, v)
            if norm > bestnorm:
                best, bestnorm = v, norm
            used_probes += 1
            if bestnorm > threshold:
                break  # One real violation already justifies acquisition.
        accepted = bestnorm <= threshold
        row = {"stage": stage, "dimension_before": len(lib.v), "q": q,
               "planned_probes": probes, "used_probes": used_probes, "delta": str(delta_s),
               "accepted": accepted,
               "maximum_power_norm_squared": str(bestnorm),
               "threshold": str(threshold),
               "primitive_calls_this_test": lib.source.calls["certificate"] - before["certificate"]}
        if not accepted:
            # Additional audit query, honestly charged; algorithm does not need it.
            ev = residual(best)
            rayleigh = div(dot(best, ev), bestnorm)
            assert rayleigh > mu / 4
            row["witness_rayleigh"] = str(rayleigh)
            row["audit_primitive_calls"] = lib.source.m
            lib.append(best)
        stages.append(row)
        if accepted:
            lib.certified_boxes = [(upper,old_mu) for upper,old_mu in lib.certified_boxes
                                  if not (mu <= old_mu and all(a <= b for a,b in zip(upper,theta)))]
            lib.certified_boxes.append((list(theta),mu))
            return stages


def solve(lib, theta, lam, b, eps):
    if not F(0) < eps < F(1):
        raise ValueError("Target relative accuracy must lie strictly between zero and one")
    max_updates = 0
    while F(9,4) * F(1,4)**max_updates > eps**2:
        max_updates += 1
    _, precondition, _ = lib.build(theta, lam)
    x = [F(0)] * len(b)
    denominator = dot(b, precondition(b))
    if denominator == 0:
        return x, {"iterations": 0, "relative_energy_bound_squared": "0"}
    iterations = 0
    while True:
        ax = lib.source.combined(theta, x, "solve")
        r = [add(bb, -add(aa, mul(lam, xx))) for bb, aa, xx in zip(b, ax, x)]
        pr = precondition(r)
        bound_squared = div(mul(F(3, 2), dot(r, pr)), denominator)
        if bound_squared <= eps**2:
            return x, {"iterations": iterations,
                       "max_updates": max_updates,
                       "relative_energy_bound_squared": str(bound_squared),
                       "target_squared": str(eps**2)}
        if iterations >= max_updates:
            raise RuntimeError("Charged solve failure: residual test failed at the finite proved update cap")
        x = [add(a, b) for a, b in zip(x, pr)]
        iterations += 1


def main():
    started = time.perf_counter()
    n = 6
    u = list(map(F, [1, 1, 0, 0, 0, 0]))
    w = list(map(F, [0, 1, 1, 0, 0, 0]))
    components = []
    for vec, weight in ((u, F(32)), (w, F(8))):
        components.append([[weight * vec[i]*vec[j] + F(i == j, 512)
                            for j in range(n)] for i in range(n)])
    source = ExactSource(components)
    lib = Library(source)
    stages = acquire(lib, [F(1), F(1)], F(1), F(1, 100), random.Random(731))
    # Separate exact audit of the retrospective determinant potential.
    c=[[sum(mat[i][j] for mat in components) for j in range(n)] for i in range(n)]
    oldpotential=F(1);potential_audits=[]
    for d in range(1,len(lib.v)+1):
        vv=lib.v[:d]
        gram=[[dot(a,b) for b in vv] for a in vv]
        h=[[dot(a,mv(c,b)) for b in vv] for a in vv]
        augmented=[[gram[i][j]+4*h[i][j] for j in range(d)] for i in range(d)]
        potential=determinant(augmented)/determinant(gram)
        ratio=potential/oldpotential
        assert ratio>2
        potential_audits.append({"dimension":d,"exact_determinant_ratio":str(ratio),
                                 "ratio_float_for_readability":float(ratio)})
        oldpotential=potential
    fullpotential=determinant([[F(i==j)+4*c[i][j] for j in range(n)] for i in range(n)])
    assert oldpotential<=fullpotential
    tasks = []
    for theta, lam, b in [([F(1), F(0)], F(1), list(map(F, [1,2,3,4,5,6]))),
                          ([F(1,3), F(4,5)], F(2), list(map(F, [2,-1,0,1,0,0]))),
                          ([F(0), F(0)], F(1), list(map(F, [1,0,0,0,0,0])))]:
        before = dict(source.calls)
        x, info = solve(lib, theta, lam, b, F(1,1024))
        # Independent exact full-matrix solution is an audit, not learner access.
        a = [[sum(theta[k]*components[k][i][j] for k in range(2)) + lam*F(i==j)
              for j in range(n)] for i in range(n)]
        truth = mv(inverse(a), b)
        err = [xx-yy for xx, yy in zip(x, truth)]
        actual = dot(err, mv(a, err)) / dot(truth, b)
        assert actual <= F(info["relative_energy_bound_squared"])
        assert actual <= F(1,1024)**2
        info.update({"theta": list(map(str,theta)), "lambda": str(lam),
                     "actual_relative_energy_error_squared": str(actual),
                     "new_cache_calls": source.calls["cache"]-before["cache"],
                     "new_certificate_calls": source.calls["certificate"]-before["certificate"],
                     "primitive_solve_calls": source.calls["solve"]-before["solve"]})
        tasks.append(info)
    out = {"kind": "exact rational finite fixture", "n": n, "m": 2,
           "alpha": "1/16", "confidence_budget": "1/100",
           "randomness": "seeded PRNG realization; theorem assumes independent signs",
           "retained_dimension": len(lib.v), "stages": stages, "tasks": tasks,
           "exact_potential_audits":potential_audits,
           "primitive_calls": source.calls,
           "returned_scalar_coordinates": n*sum(source.calls.values()),
           "selected_arithmetic_counters_including_audit": COUNTS,
           "source_input_output_max_bits": source.input_output_max_bits,
           "wall_seconds": time.perf_counter()-started,
           "limitations": ["No physical trials", "Not a bit-complexity bound: recorded maxima do not account for Python internals or every literal expression", "Known affine PSD source and regularization floor are premises", "No probability guarantee is inferred from this single seeded run"]}
    dest=Path(__file__).resolve().parents[1]/"results"/"exact_solver.json"
    dest.write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps({"retained_dimension":len(lib.v),"stages":len(stages),"primitive_calls":source.calls,
                      "arithmetic":COUNTS,"seconds":out["wall_seconds"]},indent=2))


if __name__ == "__main__":
    main()
