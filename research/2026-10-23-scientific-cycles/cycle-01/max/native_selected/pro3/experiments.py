#!/usr/bin/env python3
"""Principal finite-law calculation. No random simulation; stdlib only.

All probabilities are computed at user-selected Decimal precision. These are
rounded numerical checks, not interval arithmetic or a universal proof.
"""
import argparse
import csv
from decimal import Decimal as D, localcontext
import hashlib
import json
from math import factorial
from pathlib import Path
import platform
import resource
import sys
from time import perf_counter, process_time

ZERO, ONE = D(0), D(1)
COUNTS = {"matrix_multiplications": 0, "row_matrix_multiplications": 0,
          "sir_count_vectors": 0}


def identity(size):
    return [[D(i == j) for j in range(size)] for i in range(size)]


def multiply(a, b):
    COUNTS["matrix_multiplications"] += 1
    return [[sum((x*y for x, y in zip(row, col)), ZERO)
             for col in zip(*b)] for row in a]


def row_multiply(v, a):
    COUNTS["row_matrix_multiplications"] += 1
    return [sum((x*y for x, y in zip(v, col)), ZERO) for col in zip(*a)]


def law_after(v, a, steps):
    assert steps >= 0
    result, power = list(v), a
    while steps:
        if steps % 2:
            result = row_multiply(result, power)
        steps //= 2
        if steps:
            power = multiply(power, power)
    return result


def convex_mix(a, b, alpha):
    return [[alpha*x+(ONE-alpha)*y for x, y in zip(ar, br)]
            for ar, br in zip(a, b)]


def mh_kernel(pi, proposal):
    """General finite MH, including nonsymmetric proposal matrices."""
    size = len(pi)
    kernel = [[ZERO for _ in pi] for _ in pi]
    for i in range(size):
        for j in range(size):
            if i != j and proposal[i][j] > 0:
                kernel[i][j] = min(proposal[i][j],
                                   pi[j]*proposal[j][i]/pi[i])
        kernel[i][i] = ONE-sum(kernel[i], ZERO)
    return kernel


def path_proposal(size):
    proposal = [[ZERO for _ in range(size)] for _ in range(size)]
    for i in range(size):
        for direction in (-1, 1):
            j = min(size-1, max(0, i+direction))
            proposal[i][j] += ONE/2
    return proposal


def tv(mu, pi):
    return sum((abs(x-y) for x, y in zip(mu, pi)), ZERO)/2


def divergence(mu, pi, kind):
    if kind == "TV":
        return tv(mu, pi)
    if kind == "E4":
        return sum((max(ZERO, x-4*y) for x, y in zip(mu, pi)), ZERO)
    if kind == "chi_square":
        return sum(((x-y)**2/y for x, y in zip(mu, pi)), ZERO)
    raise ValueError(kind)


def kl(mu, nu):
    return sum((x*(x/y).ln() for x, y in zip(mu, nu)), ZERO)


def kernel_checks(pi, kernel, reversible=True):
    residual = max(abs(sum(row, ZERO)-ONE) for row in kernel)
    invariant = max(abs(x-y) for x, y in zip(row_multiply(pi, kernel), pi))
    balance = max(abs(pi[i]*kernel[i][j]-pi[j]*kernel[j][i])
                  for i in range(len(pi)) for j in range(len(pi)))
    assert all(x >= 0 for row in kernel for x in row)
    assert residual < D("1e-300") and invariant < D("1e-300")
    if reversible:
        assert balance < D("1e-300")
    return {"row_sum_residual": fmt(residual),
            "invariance_residual": fmt(invariant),
            "detailed_balance_residual": fmt(balance),
            "reversibility_required": reversible}


def family(p, K=ONE):
    c = K/4
    b = ONE-(-c).exp()
    r = p*(-c/p).exp()
    s = p*(-2*c/p).exp()
    pi, q = [p, s, ONE-p-s], [r, b, ONE-b-r]
    assert p <= min(ONE/4, (-c).exp()*b)
    assert kl(pi, q) <= 3*K/4
    G = mh_kernel(pi, [list(q) for _ in pi])
    L = mh_kernel(pi, path_proposal(len(pi)))
    return pi, q, G, L


def count_vectors(n, dimension):
    if dimension == 1:
        yield (n,)
    else:
        for first in range(n+1):
            for rest in count_vectors(n-first, dimension-1):
                yield (first,)+rest


def sir_law(pi, q, n):
    weights = [x/y for x, y in zip(pi, q)]
    result = [ZERO for _ in pi]
    for counts in count_vectors(n, len(pi)):
        COUNTS["sir_count_vectors"] += 1
        coefficient = factorial(n)
        for count in counts:
            coefficient //= factorial(count)
        probability = D(coefficient)
        for qi, count in zip(q, counts):
            probability *= qi**count
        denominator = sum((D(c)*w for c, w in zip(counts, weights)), ZERO)
        for j in range(len(pi)):
            result[j] += probability*counts[j]*weights[j]/denominator
    assert abs(sum(result, ZERO)-ONE) < D("1e-300")
    return result


def fmt(x):
    return format(x, ".30E")


def record_law(v):
    return [fmt(x) for x in v]


def stable_log1m(x, precision):
    if x < D(10)**(-precision//2):
        # Relative error <= x here; below half the working significant digits.
        return -x
    return (ONE-x).ln()


def run(digits):
    started, cpu_started = perf_counter(), process_time()
    COUNTS.update({k: 0 for k in COUNTS})
    with localcontext() as ctx:
        ctx.prec = digits
        alpha, K, eps = D(".5"), ONE, D(".01")
        families, csv_rows = [], []
        for ptext in (".05", ".01", ".001"):
            p = D(ptext)
            pi, q, G, L = family(p)
            H = convex_mix(G, L, alpha)
            LG, GL = multiply(L, G), multiply(G, L)
            checks = {name: kernel_checks(pi, a, name not in ("LG", "GL"))
                      for name, a in (("G", G), ("L", L), ("H", H), ("LG", LG), ("GL", GL))}
            exitG, exitL = ONE-G[0][0], ONE-L[0][0]
            d = q[1]*(ONE-alpha)/2
            h = ONE-H[0][0]
            rows = []
            for candidates in (4, 11, 101, 2049, 10001, 1000001):
                n = candidates-1
                distributions = {
                    "pure_IMH": law_after(q, G, n),
                    "local_then_global": law_after(q, LG, n),
                    "global_then_local": law_after(q, GL, n),
                    "mixture_expected_global_match": law_after(q, H, 2*n),
                }
                lower_lg = q[1]/2*(ONE-exitG)*((ONE-exitG)*(ONE-exitL))**(n-1)-p
                lower_gl = q[1]**2/2*((ONE-exitG)*(ONE-exitL))**(n-1)-p
                lower_h = d*(ONE-h)**(2*n-1)-p
                assert tv(distributions["local_then_global"], pi) >= lower_lg-D("1e-280")
                assert tv(distributions["global_then_local"], pi) >= lower_gl-D("1e-280")
                assert tv(distributions["mixture_expected_global_match"], pi) >= lower_h-D("1e-280")
                row = {"total_global_candidates": candidates,
                       "pure_IMH_transitions": n, "cycle_count": n,
                       "mixture_total_transitions": 2*n,
                       "TV": {key: fmt(tv(value, pi)) for key, value in distributions.items()},
                       "laws": {key: record_law(value) for key, value in distributions.items()}}
                rows.append(row)
                csv_rows.append({"p": str(p), "global_candidates": candidates, **row["TV"]})
            # This analytic escape bound is evaluated, not traversed in a simulation.
            threshold = (d/(p+eps)).ln()/(-stable_log1m(h, digits)) if d > p+eps else None
            # Certificate-selected initialization; this is not a fitted numerical choice.
            N0 = int((16*(2*K+ONE).exp()*(3/eps).ln()).to_integral_value(rounding="ROUND_CEILING"))
            initialized = law_after(q, G, N0-1)
            total_candidates = 1000001
            remaining = total_candidates-N0
            initialized_final = law_after(initialized, LG, remaining)
            assert tv(initialized_final, pi) <= tv(initialized, pi)+D("1e-280")
            families.append({
                "p": str(p), "pi": record_law(pi), "q": record_law(q),
                "forward_KL": fmt(kl(pi, q)), "reverse_KL": fmt(kl(q, pi)),
                "kernel_checks": checks, "matched_cost_results": rows,
                "analytic_log10_insufficient_mixture_steps_at_TV_0.01":
                    fmt(threshold.log10()) if threshold else None,
                "certified_initialization": {
                    "N0_total_candidates": N0, "TV_after_initialization": fmt(tv(initialized, pi)),
                    "E4_after_initialization": fmt(divergence(initialized, pi, "E4")),
                    "general_E4_upper_bound": fmt((-D(N0)/(16*(2*K+ONE).exp())).exp()),
                    "final_total_candidates": total_candidates,
                    "later_local_global_cycles": remaining,
                    "TV_after_local_global": fmt(tv(initialized_final, pi)),
                    "note": "Exact finite example only; certificate is approximate warmness, not the displayed TV."
                }})

        # Exact multinomial sum for ordinary SIR versus strongest same-pool comparator.
        pi, q, G, _ = family(D(".05"))
        sir_comparison = []
        for candidates in (2, 4, 8, 16):
            sir = sir_law(pi, q, candidates)
            imh = law_after(q, G, candidates-1)
            divergences = {}
            for kind in ("TV", "E4", "chi_square"):
                a, b = divergence(imh, pi, kind), divergence(sir, pi, kind)
                assert a <= b+D("1e-280")
                divergences[kind] = {"IMH": fmt(a), "SIR": fmt(b)}
            sir_comparison.append({"candidate_draws": candidates, "divergences": divergences,
                                   "SIR_law": record_law(sir), "IMH_law": record_law(imh)})

        # Independently evaluate the full warm-start bound in the proved units.
        pi = list(map(D, (".01", ".10", ".29", ".60")))
        q = list(map(D, (".0001", ".20", ".30", ".4999")))
        G = mh_kernel(pi, [list(q) for _ in pi])
        L = mh_kernel(pi, path_proposal(4))
        C = convex_mix(identity(4), convex_mix(G, L, alpha), ONE/2)
        kernel_checks(pi, C)
        nu = [ZERO, ZERO, ZERO, ONE]
        B = ONE/pi[-1]
        warm_rows = []
        for R in map(D, (3, 10, 30, 101)):
            tail = sum((a for a, b in zip(pi, q) if a/b > R), ZERO)
            for n in (1, 10, 100, 1000):
                r = (-alpha*D(n)/(2*R)).exp()
                bound = ((r*(B-ONE)+tail*B*B)*(r/4+tail)).sqrt()
                actual = tv(law_after(nu, C, 2*n), pi)
                assert actual <= bound+D("1e-280")
                warm_rows.append({"R": str(R), "n": n, "lazy_transitions": 2*n,
                                  "tail_mass": fmt(tail), "TV": fmt(actual), "bound": fmt(bound)})

        # Stable analytic lower sequence; no n-step loop is performed.
        baseline = []
        for t in map(D, (10, 30, 100, 300, 1000)):
            p = K/(t+2*t.ln())
            proposal_hit_factor = (-K/p).exp()
            nreal = t.exp()
            # Integer n; log(n) differs from t by less than exp(-t).
            n = int(nreal)
            err = p*((D(n)+ONE)*stable_log1m(proposal_hit_factor, digits)).exp()
            baseline.append({"log_n": fmt(D(n).ln()), "n_decimal_digits": len(str(n)),
                             "p": fmt(p), "TV": fmt(err),
                             "log_n_times_TV": fmt(D(n).ln()*err)})

        result = {"contract": "EXPERIMENT_CONTRACT.md", "K": "1", "alpha": "0.5",
                  "decimal_precision": digits, "arithmetic": "rounded Decimal, not interval-certified",
                  "all_assertions_passed": True, "families": families,
                  "SIR_comparison": sir_comparison,
                  "warm_bound_test": {"pi": record_law(pi), "q": record_law(q),
                                      "B": fmt(B), "rows": warm_rows},
                  "sharp_baseline_lower_sequence": baseline}
    result["resources"] = {
        "wall_seconds": perf_counter()-started,
        "process_cpu_seconds": process_time()-cpu_started,
        "peak_process_RSS_KiB_linux": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        "python": sys.version, "platform": platform.platform(),
        "arithmetic_operation_counts": dict(COUNTS),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "full_research_or_training_cost": "not measured; no model training or physical experiment performed",
    }
    return result, csv_rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("replay"))
    parser.add_argument("--digits", type=int, default=360)
    args = parser.parse_args()
    if args.digits < 340:
        parser.error("At least 340 digits required by the cancellation/check tolerances")
    result, rows = run(args.digits)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir/"principal_results.json").write_text(json.dumps(result, indent=2)+"\n")
    with (args.output_dir/"matched_cost.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(json.dumps({"all_assertions_passed": result["all_assertions_passed"],
                      "output_dir": str(args.output_dir), "resources": result["resources"],
                      "p_0.001_last_comparison": result["families"][-1]["matched_cost_results"][-1],
                      "p_0.001_initialization": result["families"][-1]["certified_initialization"]}, indent=2))


if __name__ == "__main__":
    main()
