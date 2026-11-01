"""Finite audit of catalytic-completion-dependent RNP recovery.

This is NOT a ribosome simulator and predicts NO assembly or recovery yield.
It computes exact resource/acceptance identities, exposes physical bypass
paths, and evaluates dimensionless specification thresholds. Experimental
release distributions for the proposed construct are explicitly unavailable.

Run: python3 stage2_root/completion_exit.py
Optional figure: python3 stage2_root/completion_exit.py --plot
"""
from __future__ import annotations

import argparse
import csv
import json
import math
from collections import deque
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "results"


def posterior_active(p: float, a: float, b: float) -> float:
    """p: incoming good fraction; a,b: whole-process accept probabilities."""
    den = p * a + (1 - p) * b
    return p * a / den if den else math.nan


def max_false_true_ratio(p: float, desired_purity: float) -> float:
    if not (0 < p < 1 and 0 < desired_purity < 1):
        raise ValueError("Fractions must lie strictly between zero and one")
    return p * (1 - desired_purity) / ((1 - p) * desired_purity)


def necessary_rate_ratio(recovery: float, false_probability: float) -> float:
    """Only for the explicitly assumed, one-exponential discrimination case."""
    return math.log1p(-recovery) / math.log1p(-false_probability)


def zero_event_sample_count(upper_probability: float, alpha: float = .05) -> int:
    """Independent Bernoulli challenges, zero observed false acceptances.

    Exact one-sided bound: p_upper = 1-alpha**(1/n). This establishes only
    the sampled control distribution, not every possible defective particle.
    """
    return math.ceil(math.log(alpha) / math.log1p(-upper_probability))


def ideal_two_step_cdf(t: float, hydrolysis: float, escape: float) -> float:
    """Two serial exponential steps, not fitted to a physical ribosome."""
    h, e = hydrolysis, escape
    if min(h, e, t) < 0:
        raise ValueError("Nonnegative inputs required")
    if h == 0 or e == 0:
        return 0.0
    if math.isclose(h, e, rel_tol=1e-10):
        return 1 - (1 + h * t) * math.exp(-h * t)
    return 1 - (e * math.exp(-h * t) - h * math.exp(-e * t)) / (e - h)


def competed_exit(t: float, h: float, e: float, bypass: float) -> dict:
    """B--h-->H--e-->valid; B--bypass-->invalid, exact transient solution.

    Values used in numerical checks are unitless algebra test vectors.
    Neither a chosen h nor a measured dipeptide rate earns a reporter rate.
    """
    if min(t, h, e, bypass) < 0:
        raise ValueError("Nonnegative inputs required")
    a = h + bypass
    if a == 0:
        return dict(bound=1.0, hydrolyzed_bound=0.0, valid=0.0, invalid=0.0)
    bound = math.exp(-a * t)
    if math.isclose(a, e, rel_tol=1e-10, abs_tol=1e-14):
        hb = h * t * math.exp(-a * t)
    else:
        hb = h * (math.exp(-a * t) - math.exp(-e * t)) / (e - a)
    invalid = bypass / a * (-math.expm1(-a * t))
    valid = 1 - bound - hb - invalid
    return dict(bound=bound, hydrolyzed_bound=hb,
                valid=max(valid, 0.0), invalid=invalid)


def renewal(p: float, f: float, d: float) -> dict:
    """Exact homogeneous, independent-repreparation abstraction.

    p = correctly accepted probability per attempt;
    f = falsely accepted probability per attempt;
    d = irreversible loss conditional on rejection.
    NO proposed physical values are supplied. An unresettable chemical defect
    violates the homogeneous renewal premise, as explained in PROOFS.txt.
    """
    if min(p, f, d) < 0 or p + f > 1 or d > 1:
        raise ValueError("Invalid probabilities")
    r = (1 - p - f) * (1 - d)
    if r == 1:
        return dict(retry_probability=r, mean_attempts=math.inf)
    denominator = 1 - r
    return dict(retry_probability=r, mean_attempts=1 / denominator,
                good_output=p / denominator,
                false_output=f / denominator,
                lost_output=(1 - p - f) * d / denominator,
                accepted_purity=p / (p + f) if p + f else math.nan)


def paths_to_collection(include_recycling: bool, include_passenger: bool):
    """Graph witness: none of these operations implies a measured rate.

    Boolean path state remembers whether the candidate passed cognate
    hydrolysis. The graph deliberately includes experimentally known or
    physically unavoidable bypasses. Removing a reagent removes its edge,
    not the intrinsic contact-dissociation edges.
    """
    edges = [
        ("captured", "hydrolyzed", "cognate RF hydrolysis", True),
        ("hydrolyzed", "collected", "peptide leaves tunnel / RNP leaves support", False),
        ("captured", "collected", "intrinsic peptidyl-tRNA drop-off", False),
        ("captured", "collected", "affinity attachment dissociation", False),
        ("captured", "collected", "non-cognate or RF-independent ester hydrolysis", False),
    ]
    if include_recycling:
        edges.append(("captured", "collected", "RF3/RRF-assisted nonhydrolytic drop-off", False))
    if include_passenger:
        edges.append(("captured", "collected", "another ribosome releases shared polysome message", False))
    q = deque([("captured", False, [])])
    result = []
    while q:
        state, passed, path = q.popleft()
        if state == "collected":
            result.append(dict(passed_cognate_hydrolysis=passed, path=path))
            continue
        for src, dst, event, cert in edges:
            if src == state:
                q.append((dst, passed or cert, path + [event]))
    return result


def poisson_passenger_limit(tolerance: float) -> float:
    """Largest lambda s.t. P(N>=2 | N>=1) <= tolerance for Poisson loading.

    This is a specified random-loading model, not a ribosome initiation model.
    """
    def conditional(lam):
        return 1 - lam / math.expm1(lam)
    lo, hi = 1e-12, 10.0
    for _ in range(100):
        mid = (lo + hi) / 2
        if conditional(mid) > tolerance:
            hi = mid
        else:
            lo = mid
    lam = (lo + hi) / 2
    return dict(tolerance=tolerance, maximum_mean_loading=lam,
                occupied_fraction=-math.expm1(-lam),
                sites_per_expected_ribosome=1 / lam,
                scope="Probability of multiple occupancy conditional on an occupied site; not the particle-weighted risk",
                particle_weighted_multioccupancy_fraction=-math.expm1(-lam),
                maximum_mean_for_particle_weighted_tolerance=-math.log1p(-tolerance),
                sites_per_particle_for_particle_weighted_tolerance=1/(-math.log1p(-tolerance)))


def exact_ligation_input_ledger(q=0.272, purification=0.8):
    """Corrects equal-per-leaf accounting for the actual unequal-depth tree.

    q is borrowed ONLY as a scenario, not transferred as an rRNA prediction.
    Each parent needs one mole of each child divided by its recovery q*r.
    """
    base = HERE.parent / "stage2_alternative" / "data"
    tree = json.loads((base / "full25_assembly_tree.json").read_text())
    with (base / "full25_fragments.csv").open() as f:
        fragments = list(csv.DictReader(f))
    nodes = {x["id"]: x for x in tree}
    needed = {}
    def visit(node, amount, depth):
        if node not in nodes:
            needed[node] = {"input_moles_per_output_mole": amount,
                            "purified_operations_on_path": depth}
            return
        for child in nodes[node]["children"]:
            visit(child, amount / (q * purification), depth + 1)
    visit(tree[-1]["id"], 1.0, 0)
    # File column names are checked explicitly rather than inferred by order.
    input_nt = 0
    for f in fragments:
        rid = f["id"]
        needed[rid]["length_nt"] = int(f["length"])
        needed[rid]["kind"] = f["method"]
        input_nt += needed[rid]["input_moles_per_output_mole"] * int(f["length"])
    chemical_nt = sum(x["input_moles_per_output_mole"] * x["length_nt"]
                      for x in needed.values() if x["kind"] == "chemical_synthesis")
    return dict(status="SCENARIO_NOT_MEASURED_YIELD", q=q, purification=purification,
                fragments=needed, input_nucleotides_per_output_RNA=input_nt,
                chemical_nucleotides_per_output_RNA=chemical_nt,
                note="Specified q already charges RNA loss in unsuccessful ligations. ATP turnover, enzymes, splint DNA, end-processing, initial fragment manufacture and later ribosome assembly remain uncharged.")


def main(plot=False):
    OUT.mkdir(exist_ok=True)
    cases = []
    for p in [.001, .01, .1, .5]:
        for target in [.95, .99, .999]:
            r = max_false_true_ratio(p, target)
            assert abs(posterior_active(p, 0.5, 0.5 * r) - target) < 1e-12
            cases.append(dict(input_good_fraction=p, target_purity=target,
                              maximum_false_true_acceptance_ratio=r))
    max_conservation_error = 0.0
    for h, e, b in [(1, 1, 0), (1, 2, 1), (.3, 4, .1), (0, 2, .4), (3, 0, .2)]:
        for t in [0, 1e-4, .1, 1, 10, 100]:
            x = competed_exit(t, h, e, b)
            max_conservation_error = max(max_conservation_error, abs(sum(x.values()) - 1))
            assert min(x.values()) > -1e-12
            if b == 0:
                assert abs(x["valid"] - ideal_two_step_cdf(t, h, e)) < 1e-10
    # Exact counterexample: a persistent defective subtype passes both tests.
    # It has no independent error events; multiplying marginal error rates fails.
    correlation_counterexample = dict(
        defective_population=10000, persistent_cheaters=100,
        first_test_false_fraction=.01, second_test_false_fraction=.01,
        actual_joint_false_fraction=.01,
        incorrect_independence_prediction=.0001,
        status="LOGICAL_WITNESS_NOT_DATA")
    result = dict(
        status="THEOREM_AND_RESOURCE_AUDIT__NO_NEW_LABORATORY_RESULT",
        physical_parameters_for_new_construct=None,
        purity_requirements=cases,
        zero_event_negative_challenges_for_p01_a05_P99_95confidence=zero_event_sample_count(.5*max_false_true_ratio(.01,.99)),
        statistical_scope="Independent identically distributed negative challenges; cannot bound unrepresented defect classes",
        exponential_ratio_for_95percent_recovery_0p1percent_false=necessary_rate_ratio(.95,.001),
        rate_ratio_scope="Only one-step exponential signal/background model; physical hydrolysis and escape need not be a single step",
        simultaneous_recycling_paths=paths_to_collection(True, True),
        separated_recycling_single_cohort_paths=paths_to_collection(False, False),
        single_loading_requirements=[poisson_passenger_limit(x) for x in [.01, .001, .0001]],
        correlated_failure_counterexample=correlation_counterexample,
        physical_round_survival_scenarios={str(q):{str(n):q**n for n in [1,2,5,10]} for q in [.5,.8,.95]},
        survival_scope="Specified per-round conditional recovery values; not measurements",
        two_step_exit_conservation_error=max_conservation_error,
        renewal_algebra_check=renewal(.1,.001,.02),
        renewal_algebra_scope="Unitless verification vector, not an assembly/recovery prediction",
        particle_count_increase_by_selection_alone=0,
        productive_polishing_advantage_established=False,
        full_synthetic_23S_activity_established=False)
    ledger = exact_ligation_input_ledger()
    (OUT / "ligation_input_ledger.json").write_text(json.dumps(ledger, indent=2) + "\n")
    (OUT / "completion_exit_results.json").write_text(json.dumps(result, indent=2) + "\n")
    with (OUT / "purity_requirements.csv").open("w") as f:
        w=csv.DictWriter(f,fieldnames=cases[0]);w.writeheader();w.writerows(cases)
    if plot:
        import numpy as np
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(1,2,figsize=(11,4.3), layout="constrained")
        ps=np.logspace(-4,math.log10(.8),300)
        for target in [.95,.99,.999]:
            ratios=[max_false_true_ratio(p,target) for p in ps]
            ax[0].loglog(ps,ratios,label=f"{100*target:g}% accepted purity")
        ax[0].set(xlabel="Incoming good-particle fraction p",ylabel="Largest permitted b/a",
                  title="Rare functional products demand stronger exclusion")
        ax[0].legend(frameon=False);ax[0].grid(alpha=.2,which="both")
        n=np.arange(1,11)
        for q in [.5,.8,.95]:
            ax[1].plot(n,q**n,"o-",label=f"Per-round recovery {q:g}")
        ax[1].set(xlabel="Number of qualification rounds",ylabel="Fraction of original good particles retained",
                  title="Qualification consumes physical yield",ylim=(0,1),xticks=[1,2,4,6,8,10])
        ax[1].legend(frameon=False);ax[1].grid(alpha=.2)
        fig.suptitle("Exact accounting boundaries — specified scenarios, not predicted ribosome performance",fontsize=11)
        fig.savefig(OUT/"completion_boundaries.png",dpi=180)
        fig.savefig(OUT/"completion_boundaries.svg")
    print(json.dumps({"status":result["status"],
        "p_1percent_purity99_max_b_over_a":max_false_true_ratio(.01,.99),
        "simple_exponential_ratio":result["exponential_ratio_for_95percent_recovery_0p1percent_false"],
        "remaining_bypass_paths_after_separation":sum(not x["passed_cognate_hydrolysis"] for x in result["separated_recycling_single_cohort_paths"]),
        "algebra_conservation_error":max_conservation_error,
        "ligation_scenario_input_nt":ledger["input_nucleotides_per_output_RNA"]},indent=2))


if __name__ == "__main__":
    parser=argparse.ArgumentParser();parser.add_argument("--plot",action="store_true")
    main(parser.parse_args().plot)
