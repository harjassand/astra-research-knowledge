#!/usr/bin/env python3
"""Cycle9 frozen finite identities; exact rational arithmetic, no tuning.

The native 5462-state proposal is sparse; no dense G/C is built for it.
Run with --output-dir NEW_DIRECTORY. A failing admission is preserved as
evidence and produces exit status 1 after all requested checks complete.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as F
import hashlib
import json
import math
from pathlib import Path
import resource
import sys
import time
from datetime import datetime, timezone

sys.set_int_max_str_digits(0)


def utc():
    return datetime.now(timezone.utc).isoformat()


def digest(data):
    return hashlib.sha256(data).hexdigest()


def fr(x):
    """Exact identity and short human-readable diagnostic."""
    x = F(x)
    exact = f"{x.numerator}/{x.denominator}"
    out = {"float_diagnostic": float(x), "sha256_num_slash_den": digest(exact.encode()),
           "numerator_bits": abs(x.numerator).bit_length(),
           "denominator_bits": x.denominator.bit_length()}
    if len(exact) <= 1600:
        out["exact"] = exact
    return out


def raw(x):
    x = F(x)
    return [str(x.numerator), str(x.denominator)]


def log_unit_interval(x, terms=24):
    """Rigorous bounds for log(x), 1<=x<=2, using positive atanh series."""
    assert F(1) <= x <= F(2)
    t = (x - 1) / (x + 1)
    lo = F(0)
    power = t
    for j in range(terms):
        lo += 2 * power / (2 * j + 1)
        power *= t * t
    remainder = 2 * power / ((2 * terms + 1) * (1 - t * t))
    return lo, lo + remainder


def log_bounds(x):
    """Signed rational bounds, with exact power-of-two range reduction."""
    x = F(x)
    assert x > 0
    if x < 1:
        lo, hi = log_bounds(1 / x)
        return -hi, -lo
    exponent = max(0, x.numerator.bit_length() - x.denominator.bit_length())
    y = x / (F(2) ** exponent)
    while y < 1:
        exponent -= 1
        y *= 2
    while y >= 2:
        exponent += 1
        y /= 2
    a, b = log_unit_interval(y)
    l2, u2 = log_unit_interval(F(2))
    return a + exponent * l2, b + exponent * u2


def zero_matrix(size):
    return [[F(0) for _ in range(size)] for _ in range(size)]


def step(vector, matrix):
    size = len(vector)
    return [sum((vector[i] * matrix[i][j] for i in range(size)), F(0))
            for j in range(size)]


def evolve(vector, matrix, steps):
    for _ in range(steps):
        vector = step(vector, matrix)
    return vector


def tv(a, b):
    return sum((abs(x-y) for x, y in zip(a, b)), F(0)) / 2


def imh(q, pi):
    size = len(q)
    w = [pi[i] / q[i] for i in range(size)]
    result = zero_matrix(size)
    for i in range(size):
        for j in range(size):
            if i != j:
                result[i][j] = q[j] * min(F(1), w[j] / w[i])
        result[i][i] = 1-sum(result[i])
    return result


class Checks:
    def __init__(self):
        self.counts = {}
        self.failures = []

    def check(self, condition, name, detail=None):
        self.counts[name] = self.counts.get(name, 0) + 1
        if not condition:
            self.failures.append({"check": name, "detail": detail})


def run_fixture(fixture):
    checks = Checks()
    started = utc()
    cpu0, wall0 = time.process_time(), time.monotonic()
    name, orientation = fixture["id"], fixture["orientation"]
    eta, kappa = F(fixture["eta"]), F(fixture["kappa"])
    ratio, b, p = F(fixture["R"]), F(fixture["b"]), F(fixture["p"])
    alpha, budget = F(fixture["alpha"]), F(fixture["K"])
    beta = 1-alpha
    m, depth, horizon = fixture["M"], fixture["depth"], fixture["n"]
    assert eta == F(1, 2) and kappa.denominator == 1
    exponent = int(kappa / eta)
    z = m / (ratio ** exponent) if orientation == "expansion" else ratio ** exponent / m
    chi = m / ratio if orientation == "expansion" else ratio / m
    f = chi / (1+chi)
    q = [b*z**i for i in range(depth+1)]
    pi = [p / F(horizon)**(2*(depth-i)) for i in range(depth+1)]
    q.append(1-sum(q)); pi.append(1-sum(pi))
    size = depth+2
    star, terminal = depth+1, depth
    weights = [pi[i]/q[i] for i in range(size)]
    checks.check(all(x > 0 for x in q+pi), "strict_mass_positivity")
    checks.check(sum(q) == sum(pi) == 1, "mass_normalization")
    checks.check(all(weights[i] < weights[star] for i in range(depth)),
                 "transient_weights_below_core")
    checks.check(weights[terminal] > weights[star], "terminal_weight_maximal")

    # Ordinary tree, breadth-first labels. Coalescence reverses progress levels.
    ordinary_depths = [0]
    ordinary_edges = []
    cursor = 0
    while cursor < len(ordinary_depths):
        level = ordinary_depths[cursor]
        if level < depth:
            for _ in range(m):
                child = len(ordinary_depths)
                ordinary_depths.append(level+1)
                ordinary_edges.append((cursor, child))
        cursor += 1
    native_size = len(ordinary_depths)+1
    native_star = native_size-1
    levels = [d if orientation == "expansion" else depth-d for d in ordinary_depths] + [star]
    multiplicities = [levels.count(i) for i in range(size)]
    q_native = [q[i]/multiplicities[i] for i in levels]
    pi_native = [pi[i]/multiplicities[i] for i in levels]
    proposal = [dict() for _ in range(native_size)]
    for parent, child in ordinary_edges:
        proposal[parent][child] = 1/(m+ratio)
        proposal[child][parent] = ratio/(m+ratio)
    local = [dict() for _ in range(native_size)]
    native_edge_hash = hashlib.sha256()
    for x, row in enumerate(proposal):
        outflow = sum(row.values(), F(0))
        checks.check(outflow <= 1, "native_Q_row_budget", x)
        for y, qxy in row.items():
            qyx = proposal[y][x]
            qr = qyx/qxy
            checks.check(qr in (ratio, 1/ratio), "native_reciprocal_edge_ratio", [x,y])
            squared_screen = (q_native[y]/q_native[x]) * qr**int(2*kappa)
            checks.check(squared_screen == 1, "native_squared_screen_one", [x,y])
            if squared_screen != 1:
                raise ArithmeticError("Frozen rational-screen identity failed")
            target_ratio = pi_native[y]*qyx/(pi_native[x]*qxy)
            local[x][y] = qxy*min(F(1), target_ratio)
            checks.check(pi_native[x]*local[x][y] == pi_native[y]*qyx*min(F(1),1/target_ratio),
                         "native_local_detailed_balance", [x,y])
            native_edge_hash.update(f"{x},{y},{qxy},{qr},{target_ratio},{local[x][y]}\n".encode())
        local[x][x] = 1-sum(local[x].values(), F(0))
        checks.check(local[x][x] >= 0, "native_actual_local_diagonal", x)
        checks.check(sum(local[x].values(), F(0)) == 1, "native_L_row_stochastic", x)
    # Record Q diagonals after edge tests so zero/diagonal ratios are never evaluated.
    for x in range(native_size):
        proposal[x][x] = 1-sum(proposal[x].values(), F(0))
        checks.check(sum(proposal[x].values(), F(0)) == 1, "native_Q_row_stochastic", x)

    local_level = zero_matrix(size)
    for i in range(size):
        if i < depth:
            local_level[i][i+1] = f
        if 0 < i <= depth:
            local_level[i][i-1] = f/F(horizon)**2
        local_level[i][i] = 1-sum(local_level[i])
    for x in range(native_size):
        aggregate = [F(0) for _ in range(size)]
        for y, value in local[x].items():
            aggregate[levels[y]] += value
        checks.check(aggregate == local_level[levels[x]], "native_local_lumping", x)

    global_level = imh(q, pi)
    full_level = [[(F(i == j)+alpha*global_level[i][j]+beta*local_level[i][j])/2
                   for j in range(size)] for i in range(size)]
    for label, kernel in (("G",global_level),("L",local_level),("C",full_level)):
        checks.check(all(min(row) >= 0 and sum(row) == 1 for row in kernel),
                     "quotient_stochastic_"+label)
        checks.check(step(pi,kernel) == pi, "quotient_invariant_"+label)
        checks.check(all(pi[i]*kernel[i][j] == pi[j]*kernel[j][i]
                         for i in range(size) for j in range(size)),
                     "quotient_reversible_"+label)

    native_full_materialized = False
    if native_size <= 32:
        native_full_materialized = True
        global_native = imh(q_native, pi_native)
        full_native = [[(F(x == y)+alpha*global_native[x][y]+beta*local[x].get(y,F(0)))/2
                        for y in range(native_size)] for x in range(native_size)]
        for label, native, quotient in (("G",global_native,global_level),("C",full_native,full_level)):
            for x in range(native_size):
                aggregate = [sum((native[x][y] for y in range(native_size) if levels[y] == j), F(0))
                             for j in range(size)]
                checks.check(aggregate == quotient[levels[x]], "native_full_lumping_"+label, x)
            a_native, a_level = q_native[:], q[:]
            for j in range(1,5):
                a_native, a_level = step(a_native,native), step(a_level,quotient)
                aggregate = [sum((a_native[x] for x in range(native_size) if levels[x] == i),F(0))
                             for i in range(size)]
                checks.check(aggregate == a_level, "native_first_four_laws_"+label, j)
                checks.check(all(a_native[x] == a_level[levels[x]]/multiplicities[levels[x]]
                                 for x in range(native_size)), "native_level_uniformity_"+label, j)

    # Exact actual hazards. A local forward event is distinct from a global move
    # to that same destination; the latter is a marked failure before capture.
    c = beta*f/2
    E = c+alpha*(1-b+b/(F(horizon)**2*(1-F(1,horizon**2))))/2+c/F(horizon)**2
    h0 = c+alpha*q[star]/2
    window = horizon//(2*depth)
    e = []
    g = []
    for i in range(depth):
        gi = q[star]+sum(q[i+1:depth+1],F(0))+sum(pi[:i],F(0))/weights[i]
        checks.check(gi == 1-global_level[i][i], "exact_global_out_of_level_hazard", i)
        ei = c+alpha*gi/2+(c/F(horizon)**2 if i>0 else 0)
        checks.check(h0 <= ei <= E < 1, "exact_marked_hazard_bounds", i)
        g.append(gi); e.append(ei)
    checks.check(g[0] == 1-b, "root_global_hazard_one_minus_b")
    escape = alpha*(1-p)/(2*weights[terminal])+beta*f/(2*F(horizon)**2)
    checks.check(escape == 1-full_level[terminal][terminal], "exact_terminal_union_escape")

    stage_lower = (c/E)*(1-(1-h0)**window)
    window_capture = b
    for ei in e:
        window_capture *= (c/ei)*(1-(1-ei)**window)
    conservative_capture = b*stage_lower**depth
    checks.check(conservative_capture <= window_capture, "finite_window_capture_bound")
    # Explicit marked chain: same-level movement/real rejection stays; global
    # out-of-level moves are killed, terminal absorbs only for event counting.
    marked = zero_matrix(size)
    dead = star
    for i in range(depth):
        marked[i][i] = 1-e[i]
        marked[i][i+1] = c
        marked[i][dead] = e[i]-c
    marked[terminal][terminal] = marked[dead][dead] = F(1)
    origin = [F(0)]*size; origin[0] = F(1)
    all_marked_capture = b*evolve(origin,marked,depth*window)[terminal]
    checks.check(window_capture <= all_marked_capture, "window_event_inside_marked_horizon")
    retention = (1-escape)**horizon
    certificate = conservative_capture*retention-p
    stronger_certificate = window_capture*retention-p

    q_full = evolve(q[:],full_level,horizon)
    full_tv = tv(q_full,pi)
    checks.check(full_tv >= q_full[terminal]-p >= stronger_certificate >= certificate,
                 "finite_capture_vs_original_full_law")
    # Ordinary same-input laws, at n and the deterministic alpha*n/2 budget.
    ordinary = []
    for count in sorted({horizon,int(alpha*horizon/2)}):
        law = evolve(q[:],global_level,count)
        error = tv(law,pi)
        exact_bound = sum(pi[:depth+1],F(0))+sum(q[1:depth+1],F(0))/(1-b)+b**(count+1)
        coarse_bound = p/(1-F(1,horizon**2))+b*z/((1-b)*(1-z))+b**(count+1)
        checks.check(error <= exact_bound <= coarse_bound, "ordinary_same_input_bound", count)
        ordinary.append({"steps":count,"tv":fr(error),"bound":fr(exact_bound),
                         "coarse_bound":fr(coarse_bound),"law_exact":[raw(x) for x in law]})

    # Rigorous finite admission, not a floating-point KL decision.
    kl_lo, kl_hi = F(0),F(0)
    for mass, weight in zip(pi,weights):
        lo,hi = log_bounds(weight)
        kl_lo += mass*lo
        kl_hi += mass*hi
    kl_diagnostic = sum(float(mass)*math.log(float(weight)) for mass,weight in zip(pi,weights))
    admission = kl_hi <= budget
    rejection_proved = kl_lo > budget
    checks.check(kl_lo <= kl_hi, "rigorous_KL_interval_order")
    # Admission is a separate scientific gate; preserve a failed frozen fixture.
    result = {
        "id":name,"inputs":fixture,"native_states":native_size,
        "native_directed_offdiagonal_edges":2*len(ordinary_edges),
        "native_edge_digest":native_edge_hash.hexdigest(),
        "native_dense_G_C_materialized":native_full_materialized,
        "quotient_states":size,"multiplicities":multiplicities,
        "checks":checks.counts,"identity_and_inequality_failures":checks.failures,
        "model_checks_pass":not checks.failures,
        "KL":{"lower":fr(kl_lo),"upper":fr(kl_hi),"float_diagnostic":kl_diagnostic,
               "admitted_under_frozen_K":admission,"nonadmission_proved":rejection_proved,
               "method":"24 positive atanh-series terms after exact binary range reduction; rational remainder bound"},
        "all_frozen_gates_pass":not checks.failures and admission,
        "z":fr(z),"chi":fr(chi),"f":fr(f),"weights":[fr(x) for x in weights],
        "global_hazards":[fr(x) for x in g],"marked_hazards":[fr(x) for x in e],
        "hazard_upper":fr(E),"hazard_lower":fr(h0),"window_steps":window,
        "terminal_escape":fr(escape),"retention":fr(retention),
        "conservative_capture":fr(conservative_capture),"exact_window_capture":fr(window_capture),
        "marked_horizon_capture":fr(all_marked_capture),"certificate":fr(certificate),
        "stronger_certificate":fr(stronger_certificate),"full_law_tv":fr(full_tv),
        "full_terminal_mass":fr(q_full[terminal]),"ordinary":ordinary,
        "quotient_q_exact":[raw(x) for x in q],"quotient_pi_exact":[raw(x) for x in pi],
        "quotient_G_exact":[[raw(x) for x in row] for row in global_level],
        "quotient_L_exact":[[raw(x) for x in row] for row in local_level],
        "quotient_C_exact":[[raw(x) for x in row] for row in full_level],
        "full_law_exact":[raw(x) for x in q_full],
        "cost":{"started_utc":started,"completed_utc":utc(),
                "process_cpu_seconds":time.process_time()-cpu0,
                "wall_seconds":time.monotonic()-wall0,
                "peak_RSS_KiB_linux":resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                "inference_cost":None,"discovery_cost":None},
    }
    return result


def main():
    base = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser()
    parser.add_argument("--freeze",type=Path,default=base/"evidence/PREEXECUTION_FREEZE.json")
    parser.add_argument("--output-dir",type=Path,default=base/"evidence/exact")
    args = parser.parse_args()
    if args.output_dir.exists() and any(args.output_dir.iterdir()):
        raise SystemExit("Refusing to overwrite nonempty evidence directory")
    args.output_dir.mkdir(parents=True,exist_ok=True)
    source = Path(__file__).read_bytes()
    inputs = args.freeze.read_bytes()
    freeze = json.loads(inputs)
    cpu0,wall0 = time.process_time(),time.monotonic()
    started = utc()
    results = []
    for fixture in freeze["fixtures"]:
        result = run_fixture(fixture)
        results.append(result)
        (args.output_dir/(fixture["id"]+".json")).write_text(json.dumps(result,indent=2)+"\n")
        print(json.dumps({"id":fixture["id"],"model_checks_pass":result["model_checks_pass"],
                          "KL":result["KL"]["float_diagnostic"],
                          "admitted":result["KL"]["admitted_under_frozen_K"],
                          "certificate":result["certificate"]["float_diagnostic"],
                          "full_TV":result["full_law_tv"]["float_diagnostic"],
                          "CPU_s":result["cost"]["process_cpu_seconds"]}),flush=True)
    receipt = {"started_utc":started,"completed_utc":utc(),
               "code_sha256":digest(source),"freeze_sha256":digest(inputs),
               "all_model_checks_pass":all(r["model_checks_pass"] for r in results),
               "all_frozen_gates_pass":all(r["all_frozen_gates_pass"] for r in results),
               "fixtures_changed":False,"numerical_asymptotic_claim":False,
               "process_cpu_seconds":time.process_time()-cpu0,
               "wall_seconds":time.monotonic()-wall0,
               "peak_RSS_KiB_linux":resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
               "inference_cost":None,"total_discovery_cost":None}
    (args.output_dir/"RESOURCE_RECEIPT.json").write_text(json.dumps(receipt,indent=2)+"\n")
    (args.output_dir/"EXACT_INPUTS.json").write_bytes(inputs)
    print(json.dumps(receipt,indent=2),flush=True)
    return 0 if receipt["all_frozen_gates_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
