#!/usr/bin/env python3
"""Finite exact checks and explicitly non-interval numerical diagnostics.

Only writes EXTENSION_VERIFICATION_RESULTS.json beside this script. The proof is
in CONDITIONAL_VARIANCE_EXTENSION.md; passing this file is not independent proof
review, a physical acquisition experiment, or historical-priority evidence.
"""
from collections import defaultdict
from fractions import Fraction as F
from itertools import product
from math import comb, factorial
from pathlib import Path
import hashlib
import json
import platform

import mpmath as mp

BASE = Path(__file__).resolve().parent
ALPHA, C, DELTA = F(1, 2), F(1, 2), F(1, 4)
EXACT = 0
NUMERICAL = 0


def check(condition, label):
    global EXACT
    if not condition:
        raise AssertionError(label)
    EXACT += 1


def numerical(condition, label):
    global NUMERICAL
    if not condition:
        raise AssertionError("numerical diagnostic: " + label)
    NUMERICAL += 1


def squared(v):
    return sum(x * x for x in v)


def full_row(source, destination, rate):
    v = [F(0)] * 6
    v[source] -= rate
    v[destination] += rate
    return tuple(v)


def family_edges(m):
    """Index-free sparse explicit generator: source, destination, rate, labels."""
    n_context = 2**m
    edges = []
    for h in range(n_context):
        bits = tuple(int(x) for x in f"{h:0{m}b}")
        for z in (-1, 1):
            for j in range(m + 1):
                label = 0 if j == 0 else 2 * (j % 2) + bits[j - 1]
                dest_label = 4 if j == m else 2 * ((j + 1) % 2) + bits[j]
                edges.append(((h, z, j), (h, z, j + 1), F(1), label, dest_label))
            label = 4
            edges.append(((h, z, m + 1), "B", C + DELTA * z, label, 5))
    return edges


generator_results = []
for m in range(1, 5):
    edges = family_edges(m)
    check(len(edges) + 1 == 2 * 2**m * (m + 2) + 1, "explicit state count")
    check(all(a != b for _, _, _, a, b in edges), "all jumps visible")
    check(all(0 < q <= 1 for _, _, q, _, _ in edges), "target exit bound")
    check(all(squared(full_row(a, b, q)) <= 2 for _, _, q, a, b in edges), "row norm bound")
    for a in range(6):
        synthesis_ok, product_bound = True, True
        for _, _, q, source, dest in edges:
            d = int(dest == a) - int(source == a)
            gp, gm = F(2) ** d, F(2) ** (-d)
            synthesis_ok &= (gp - gm) / 3 == F(d, 2)
            synthesis_ok &= tuple((x - y) / 3 for x, y in zip(
                full_row(source, dest, q * gp),
                full_row(source, dest, q * gm),
            )) == full_row(source, dest, q * F(d, 2))
            for aa, sign in product(range(6), (-1, 1)):
                dd = sign * (int(dest == aa) - int(source == aa))
                product_bound &= q * gp * F(2) ** dd <= 4
                product_bound &= q * gm * F(2) ** dd <= 4
        check(synthesis_ok, "exact geometric signed synthesis, full rows")
        check(product_bound, "all selected pair-product rate bounds")
    prefix_errors = []
    for (h, z, j), _, q, source, dest in edges:
        if j < m:
            pred = [F(0)] * 6
            pred[source] = -1
            pred[2 * ((j + 1) % 2)] += F(1, 2)
            pred[2 * ((j + 1) % 2) + 1] += F(1, 2)
            error = tuple(x - y for x, y in zip(full_row(source, dest, q), pred))
            prefix_errors.append(squared(error))
        elif j == m:
            check(full_row(source, dest, q) == full_row(source, 4, F(1)), "last prefix step exact")
    check(set(prefix_errors) == {F(1, 2)}, "constant prefix hidden-rate variance")
    generator_results.append({"m": m, "hidden_states": len(edges) + 1, "edges": len(edges)})


preparation_results = []
for M in (1, 2, 4):
    null = {(i, b, z): F(1, 4 * M) for i, b, z in product(range(M), (0, 1), (-1, 1))}
    avg = defaultdict(F)
    for xi in product((-1, 1), repeat=M):
        mu = {(i, b, z): (1 + ALPHA * z * (-1)**b * xi[i]) / (4 * M)
              for i, b, z in null}
        check(sum(mu.values()) == 1, "alternative normalization")
        check(all(sum(mu[i, b, z] for z in (-1, 1)) == F(1, 2 * M)
                  for i, b in product(range(M), (0, 1))), "uniform context marginal")
        check(all(sum(mu[i, b, z] for i, b in product(range(M), (0, 1))) == F(1, 2)
                  for z in (-1, 1)), "exactly fair sign marginal")
        check(min(mu.values()) == F(1, 8 * M), "constant conditional support")
        for outcome, p in mu.items():
            avg[outcome] += p / 2**M
    check(dict(avg) == null, "one-reset affine mixture equals null preparation")
    preparation_results.append({"M": M, "alternatives_exhausted": 2**M})


def mixture_data_probability(ids, signs, M):
    r = len(ids)
    likelihood = F(1)
    for i in set(ids):
        pp, pm = F(1), F(1)
        for ii, w in zip(ids, signs):
            if ii == i:
                pp *= 1 + ALPHA * w
                pm *= 1 - ALPHA * w
        likelihood *= (pp + pm) / 2
    return likelihood / (2 * M)**r


mixture_results = []
for M in (1, 2, 4):
    for r in range(5):
        tv, total, no_collision_equal = F(0), F(0), True
        id_marginals = defaultdict(F)
        null_prob = F(1, (2 * M)**r)
        for ids in product(range(M), repeat=r):
            for signs in product((-1, 1), repeat=r):
                p = mixture_data_probability(ids, signs, M)
                total += p
                tv += abs(p - null_prob) / 2
                id_marginals[ids] += p
                if len(set(ids)) == r:
                    no_collision_equal &= p == null_prob
        no_collision = F(0) if r > M else F(factorial(M), factorial(M-r) * M**r)
        collision = 1 - no_collision
        union = min(F(1), F(r * (r-1), 2 * M))
        check(total == 1, "finite mixture normalization")
        check(set(id_marginals.values()) == {F(1, M**r)}, "common exact ID law")
        check(no_collision_equal, "exact equality on no-collision data")
        check(tv <= collision <= union, "finite total variation birthday bound")
        if r == 1:
            check(tv == 0, "one-reset observable indistinguishability")
        if r == 2:
            check(tv == ALPHA**2 / (2 * M), "exact two-reset TV")
        mixture_results.append({"M": M, "resets": r, "TV": str(tv),
                                "collision_probability": str(collision), "union_bound": str(union)})


hazard_results = []
for theta, q in product((-ALPHA, F(0), ALPHA), (F(0), F(1, 16), F(1, 8), F(1, 4))):
    priors = {z: (1 + theta*z)/2 for z in (-1, 1)}
    survivor_weights = {z: priors[z] * (1-z*q) for z in (-1, 1)}
    survival_factor = sum(survivor_weights.values())
    posterior = {z: w / survival_factor for z, w in survivor_weights.items()}
    post_mean = sum(z*p for z, p in posterior.items())
    l0 = C - DELTA*q
    lt = sum((C+DELTA*z)*p for z, p in posterior.items())
    gap = lt-l0
    check(survival_factor == 1-theta*q, "survival factor")
    check(post_mean == (theta-q)/(1-theta*q), "posterior sign mean")
    check(gap == DELTA*theta*(1-q*q)/(1-theta*q), "terminal hazard difference")
    raw = sum(2*(C+DELTA*z-l0)**2*p for z, p in posterior.items())
    cond = 2*gap*gap
    variance = 2*DELTA**2*(1-post_mean**2)
    check(raw == cond+variance, "conditional hidden variance decomposition")
    if theta:
        check(abs(gap) >= F(5, 48), "first terminal unit algebraic lower bound")
    else:
        check(cond == 0, "null exact conditional predictor")
    for f in ((F(0), F(0)), (F(1, 7), F(-1, 9)), (-gap, gap)):
        e = (-gap, gap)
        dual = 2*sum(x*y for x, y in zip(f, e))-squared(f)
        check(cond-dual == squared(tuple(x-y for x, y in zip(e, f))), "observable dual algebra")
    hazard_results.append({"theta": str(theta), "q": str(q), "hazard_gap": str(gap),
                           "raw_error": str(raw), "conditional_error": str(cond)})

for q in (F(0), F(1, 16), F(1, 8), F(1, 4), F(3, 4)):
    l0 = C-DELTA*q
    def raw_weight(theta):
        return sum((1+theta*z)/2 * (1-z*q) * 2*(C+DELTA*z-l0)**2 for z in (-1, 1))
    check((raw_weight(ALPHA)+raw_weight(-ALPHA))/2 == raw_weight(F(0)),
          "balanced alternatives have identical unconditioned terminal raw moment")
check(F(2, 3)*2*F(5, 48)**2*F(1, 3) == F(25, 5184), "exact occupation constant")
check(F(25, 5184) > F(1, 256), "risk separation threshold")
check(F(2, 3)*ALPHA*F(1, 2)*F(1, 4) > F(1, 32), "elementary fixed-alternative path-gap constant")


def finite_collision_moments(M, q, xi, alpha, a0=F(1, 2), d0=F(1, 4)):
    outcomes = []
    for i, b, out in product(range(M), (0, 1), (0, 1)):
        mean_B = a0+d0*alpha*(-1)**b*xi[i]
        p = F(1, 2*M) * (mean_B if out else 1-mean_B)
        v = (-1)**b*(out-a0)/d0
        outcomes.append((i, v, p))
    mean, second = F(0), F(0)
    for trial in product(outcomes, repeat=q):
        p = F(1)
        for _, _, pp in trial:
            p *= pp
        s = sum((x[1]*y[1] if x[0] == y[0] else F(0))
                for j, x in enumerate(trial) for y in trial[j+1:])
        mean += p*s
        second += p*s*s
    return mean, second-mean*mean


collision_moment_results = []
for M in (1, 2):
    for q in (2, 3, 4):
        for xi in product((-1, 1), repeat=M):
            for alpha in (F(0), ALPHA):
                mean, var = finite_collision_moments(M, q, xi, alpha)
                v2 = F(4)
                aq = F(q*(q-1), 2)
                expected_mean = aq*alpha**2/M
                expected_var = (aq*(v2**2/M-alpha**4/M**2)
                                + 6*comb(q, 3)*alpha**2*(v2-alpha**2)/M**2)
                upper = aq*F(2)**4/M + 6*comb(q, 3)*alpha**2*F(2)**2/M**2
                check(mean == expected_mean, "collision statistic exact mean")
                check(var == expected_var, "collision statistic exact variance")
                check(var <= upper, "collision statistic variance envelope")
        collision_moment_results.append({"M": M, "accepted_episodes": q,
                                         "all_sign_maps_and_null_checked": True})


# Exact finite conditional-closure fixture with multiple hidden draws per history.
history_mass = (F(1, 10), F(1, 5), F(3, 10), F(2, 5))
context = (0, 0, 1, 1)
theta_history = (F(-1, 2), F(1, 3), F(1, 4), F(-1, 5))
pred_rate = (F(2, 5), F(3, 5))
bar = [C+DELTA*t for t in theta_history]
e = [(-x+pred_rate[c], x-pred_rate[c]) for x, c in zip(bar, context)]
dcond = sum(w*squared(v) for w, v in zip(history_mass, e))
finite_term, closure = F(0), F(0)
for cc in range(2):
    mass = sum(w for w, ccc in zip(history_mass, context) if ccc == cc)
    mc = tuple(sum(w*v[a] for w, v, ccc in zip(history_mass, e, context) if ccc == cc)
               for a in range(2))
    finite_term += squared(mc)/mass
    for w, v, ccc in zip(history_mass, e, context):
        if ccc == cc:
            closure += w*squared(tuple(x-y/mass for x, y in zip(v, mc)))
check(dcond == finite_term+closure, "finite observed context exact projection identity")
check(closure > 0, "finite closure error cannot be silently dropped")


# Scope check: all files named by the frozen main manifest still match it.
main_manifest = json.loads((BASE/"MANIFEST.json").read_text())
for name, info in main_manifest["files"].items():
    content = (BASE/name).read_bytes()
    check(hashlib.sha256(content).hexdigest() == info["sha256"], "frozen main integrity: "+name)
    check(len(content) == info["bytes"], "frozen main byte count: "+name)


mp.mp.dps = 80
numerical_results = []
c, delta, alpha = mp.mpf("0.5"), mp.mpf("0.25"), mp.mpf("0.5")
for m in (1, 2, 4, 8):
    a = m+1
    T = 4*a
    def arrival_cdf(x):
        if x <= 0:
            return mp.mpf(0)
        return mp.gammainc(a, 0, x)/mp.factorial(a-1)
    def l0(s):
        return c-delta*mp.tanh(delta*s)
    def surv(theta, s):
        return mp.exp(-c*s)*(mp.cosh(delta*s)-theta*mp.sinh(delta*s))
    def gap(theta, s):
        qq = mp.tanh(delta*s)
        return delta*theta*(1-qq*qq)/(1-theta*qq)
    def raw_integrand(theta, s):
        return sum((1+theta*z)/2 * mp.exp(-(c+delta*z)*s)
                   * 2*(c+delta*z-l0(s))**2 for z in (-1, 1))
    cond = mp.quad(lambda s: arrival_cdf(T-s)*sum(
        surv(theta, s)*gap(theta, s)**2 for theta in (-alpha, alpha)), [0, 1, 4, T])/T
    raw0 = mp.quad(lambda s: arrival_cdf(T-s)*raw_integrand(0, s), [0, 1, 4, T])/T
    rawalt = mp.quad(lambda s: arrival_cdf(T-s)*(raw_integrand(alpha, s)
                        + raw_integrand(-alpha, s))/2, [0, 1, 4, T])/T
    prefix = sum(mp.gammainc(j+1, 0, T)/mp.factorial(j) for j in range(m))/(2*T)
    retained_tv = arrival_cdf(T-1)*alpha*mp.exp(-c)*mp.sinh(delta)
    crossing = mp.log((c+delta)/(c-delta))/(2*delta)
    def full_gap_at_arrival(t):
        age = min(T-t, crossing)
        return (mp.exp(-(c-delta)*age)-mp.exp(-(c+delta)*age))
    path_tv = alpha/2 * mp.quad(lambda t: mp.exp(-t)*t**(a-1)/mp.factorial(a-1)
                            * full_gap_at_arrival(t), [0, T-crossing, T])
    numerical(abs(raw0-rawalt) < mp.mpf("1e-70"), "identical integrated raw moments")
    numerical(cond > mp.mpf(25)/(5184*T), "occupation analytic lower bound")
    numerical(prefix+raw0 > cond, "conditional variance remains positive")
    numerical(retained_tv > mp.mpf(1)/32, "retained visible path gap")
    numerical(path_tv >= retained_tv, "full visible path gap dominates retained statistic")
    numerical(arrival_cdf(T-1) >= mp.mpf(2)/3, "arrival probability bound")
    numerical_results.append({
        "m": m, "T": T, "D_cond_alternative": mp.nstr(cond, 35),
        "analytic_D_cond_lower_bound": mp.nstr(mp.mpf(25)/(5184*T), 35),
        "D_raw_null_and_all_alternatives": mp.nstr(prefix+raw0, 35),
        "retained_visible_path_TV": mp.nstr(retained_tv, 35),
        "full_visible_path_TV": mp.nstr(path_tv, 35),
        "arrival_probability": mp.nstr(arrival_cdf(T-1), 35),
    })

result = {
    "status": "PASS_local_finite_checks; independent_proof_review_UNKNOWN",
    "script": "verify_extension.py",
    "python": platform.python_version(), "mpmath": mp.__version__, "mpmath_digits": mp.mp.dps,
    "exact_fraction_assertions": EXACT,
    "non_interval_numerical_diagnostics": NUMERICAL,
    "proof_scope": "Analytic proofs in CONDITIONAL_VARIANCE_EXTENSION.md. Enumeration and numerical checks supplement them; no physical assay or complete arbitrary-controller simulator is claimed.",
    "generators": generator_results,
    "preparations": preparation_results,
    "finite_mixture_TV": mixture_results,
    "terminal_hazard_fractions": hazard_results,
    "collision_statistic_moments": collision_moment_results,
    "finite_closure_fixture": {"D_cond": str(dcond), "finite_context_term": str(finite_term),
                                "closure_error": str(closure)},
    "numerical_occupation_and_path_diagnostics": numerical_results,
    "frozen_main_manifest_all_hashes_match": True,
    "limitations": [
        "Floating numerical integrations are not interval certificates and are not used to prove the exact constants.",
        "The collision-statistic variance identity is exactly checked using a rational binary sensor; the physical exponential terminal sensor obeys the same proved identity.",
        "No claim that the arbitrary sign-map initial preparation can be implemented with polynomial physical or description resources.",
        "No empirical execution of conditional replicas, product probes, or critic learning is included."
    ]
}
(BASE/"EXTENSION_VERIFICATION_RESULTS.json").write_text(json.dumps(result, indent=2)+"\n")
print(json.dumps({"status": result["status"], "exact_fraction_assertions": EXACT,
                  "non_interval_numerical_diagnostics": NUMERICAL,
                  "frozen_main_manifest_all_hashes_match": True}, indent=2))
