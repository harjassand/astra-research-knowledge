"""Paid noisy acquisition followed by compact, certified contraction fitting.

The source below simulates exact binomial batches of genuine stationary
endpoint-product reports for symmetric four-state Markov controls. It counts
all physical episodes and primitive steps; batching saves simulation CPU only.
The learner receives scalar reports, actual-word names and acquired rules.

NumPy proposes decompositions/fits. Final rule residuals, the geometry error,
the rank lower certificate and stored contraction norms are checked with exact
rational arithmetic. Source confidence is probabilistic, not a truth audit.
The universal finite-precision optimizer is described in PROOF.txt; this code
can stop unsuccessfully under a declared numerical resource cap.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as F
import itertools
import json
import math
from pathlib import Path
import sys
import time

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "cumulative_intelligence"))
sys.path.insert(0, str(Path(__file__).resolve().parent / "notes"))
from metric_compiler import convex_compiler, MomentCache
from spectral_baseline import (
    certified_contraction, fit_minimax_contraction, project_contraction,
    rational_matrix, sqrt_upper, transpose, multiply, subtract,
)

COIN_ROUNDING_BIAS = 2.0**-52


def ceil_fraction(value):
    return -(-value.numerator//value.denominator)


def log_upper_integer(value):
    """Integer upper bound on natural log(value), for value>=1.

    ln(value)<=ceil(log2(value)); no floating logarithm enters a confidence
    schedule. Integer arithmetic decides the power-of-two comparison.
    """
    if value <= 1:
        return 0
    exponent = max(0,value.numerator.bit_length()-value.denominator.bit_length())
    if F(1 << exponent) < value:
        exponent += 1
    return exponent


class StationaryEndpointSource:
    """Simulator only. No latent arrays are passed to the learner."""
    def __init__(self, mixing: float = 0.4, random_seed: int = 20261031):
        self._rng = np.random.default_rng(random_seed)
        p = np.eye(4)[[1, 0, 2, 3]]
        q = np.eye(4)[[0, 1, 3, 2]]
        r = np.eye(4)[[0, 2, 1, 3]]
        self._operators = [p, q, (1-mixing)*np.eye(4)+mixing*r]
        self._seed = np.array([0.5, 0.5, -0.5, -0.5])
        self._features = {(): self._seed}
        self._exact_mixing = F(str(mixing))
        self._exact_features = {(): (F(1,2),F(1,2),F(-1,2),F(-1,2))}
        self._counts = {"stationary_preparations": 0, "primitive_controls": 0,
                        "endpoint_readings": 0, "scalar_jobs": 0,
                        "maximum_return_depth": 0}
        self._last_exact_mean: F | None = None
        self._raw_batches = []

    def _feature(self, word):
        word = tuple(word)
        if word not in self._features:
            self._features[word] = self._operators[word[-1]] @ self._feature(word[:-1])
        return self._features[word]

    def truth_gram(self, u, v):
        """Source implementation and audit only; never a learner query."""
        return float(self._feature(u) @ self._feature(v))

    def _exact_feature(self, word):
        word = tuple(word)
        if word not in self._exact_features:
            v = list(self._exact_feature(word[:-1]))
            if word[-1] == 0:
                v[0],v[1] = v[1],v[0]
            elif word[-1] == 1:
                v[2],v[3] = v[3],v[2]
            else:
                t = self._exact_mixing
                v[1],v[2] = (1-t)*v[1]+t*v[2], t*v[1]+(1-t)*v[2]
            self._exact_features[word] = tuple(v)
        return self._exact_features[word]

    def sample_mean(self, u, v, n):
        if not 0 < n < np.iinfo(np.int64).max:
            raise ValueError("binomial simulator capacity exceeded; split the paid batch")
        # Exact rational physical moment; binary64 coin probability introduces
        # at most 2^-52 mean bias, reserved explicitly in both shot schedules.
        mu = sum((x*y for x,y in zip(self._exact_feature(u),self._exact_feature(v))), F(0))
        probability = float((1+mu)/2)
        plus = int(self._rng.binomial(n, probability))
        self._last_exact_mean = F(2*plus-n, n)
        self._counts["stationary_preparations"] += n
        self._counts["primitive_controls"] += n*(len(u)+len(v))
        self._counts["endpoint_readings"] += 2*n
        self._counts["scalar_jobs"] += 1
        self._counts["maximum_return_depth"] = max(
            self._counts["maximum_return_depth"], len(u)+len(v))
        self._raw_batches.append({"u": list(u), "v": list(v),
                                 "n": n, "positive_reports": plus})
        return float(self._last_exact_mean)

    def ledger(self):
        return dict(self._counts)


class ExactRecordedCache:
    """Float proposals accompanied by exact rational measured means."""
    def __init__(self, source, tolerance, delta):
        self.source, self.tol, self.delta = source, tolerance, delta
        self.values, self.exact_values = {}, {}

    def get(self, u, v):
        key = MomentCache.key(tuple(u), tuple(v))
        if key not in self.values:
            k = len(self.values)+1
            dk = F(str(self.delta))/(k*(k+1))
            statistical_tolerance = F.from_float(float(self.tol))-F(1,1 << 52)
            if statistical_tolerance <= 0:
                raise ValueError("source simulation precision cannot meet requested tolerance")
            n = ceil_fraction(2*log_upper_integer(2/dk)/statistical_tolerance**2)
            self.values[key] = self.source.sample_mean(u, v, n)
            self.exact_values[key] = self.source._last_exact_mean
        return self.values[key]

    def exact(self, u, v):
        self.get(u, v)
        return self.exact_values[MomentCache.key(tuple(u), tuple(v))]


def subtract_ledger(after, before):
    return {key: after[key]-before.get(key, 0) for key in after
            if key != "maximum_return_depth"} | {
                "maximum_return_depth_overall": after["maximum_return_depth"]}


def rational_rules(model):
    n, m = len(model["words"]), len(model["matrices"])
    out = [[[F(0) for _ in range(n)] for _ in range(n)] for _ in range(m)]
    for i, row in enumerate(model["rational_columns"]):
        for a, entry in enumerate(row):
            for j, count in enumerate(entry["counts"]):
                out[a][j][i] = F(int(count), int(entry["denominator"]))
    return out


def certify_reference(model, cache, rules):
    """Exact measured residual upper bounds, conditional on scalar confidence."""
    words = model["words"]
    gram = [[cache.exact(u, v) for v in words] for u in words]
    tau = F.from_float(float(cache.tol))
    rho2 = F.from_float(float(model["rho"]))**2
    maximum, maximum_l1 = F(0), F(0)
    for a, mat in enumerate(rules):
        for i, w in enumerate(words):
            c = [row[i] for row in mat]
            l1 = sum(map(abs, c), F(0))
            maximum_l1 = max(maximum_l1, l1)
            nz = [(j, v) for j, v in enumerate(c) if v]
            candidate = tuple(w)+(a,)
            value = cache.exact(candidate, candidate)
            value -= 2*sum((cj*cache.exact(words[j], candidate) for j,cj in nz), F(0))
            value += sum((ci*cj*gram[i][j] for i,ci in nz for j,cj in nz), F(0))
            upper = value+tau*(1+l1)**2
            maximum = max(maximum, upper)
            if l1 > 1 or upper > rho2:
                raise RuntimeError("reference certificate failed; no model is emitted")
    return {"all_rule_residuals_certified_from_reports": True,
            "maximum_squared_residual_upper": float(maximum),
            "maximum_squared_residual_upper_exact": str(maximum),
            "maximum_l1_column_norm": float(maximum_l1),
            "conditional_on_scalar_confidence_event": True}


def gram_shot_schedule(n, eta, delta):
    """Return integer shots/pair, exact statistical eta, exact stage delta."""
    delta_r = delta if isinstance(delta,F) else F(str(delta))
    if n <= 0 or not 0 < delta_r < 1:
        raise ValueError("invalid Gram stage size or confidence")
    statistical_eta = F.from_float(float(eta))-n*F(1,1 << 52)
    if statistical_eta <= 0:
        raise ValueError("source simulation coin precision cannot meet Gram tolerance")
    log_budget = 3*n+log_upper_integer(2/delta_r)
    shots = ceil_fraction(16*log_budget/statistical_eta**2)
    return shots,statistical_eta,delta_r


def acquire_geometry(source, words, eta, delta):
    """Fresh symmetric Gram stage. Net concentration controls operator error."""
    n = len(words)
    shots,statistical_eta,delta_r = gram_shot_schedule(n,eta,delta)
    exact = [[F(0) for _ in range(n)] for _ in range(n)]
    for i, u in enumerate(words):
        for j in range(i, n):
            source.sample_mean(u, words[j], shots)
            exact[i][j] = exact[j][i] = source._last_exact_mean
    return exact, {"eta": eta, "delta": float(delta_r), "delta_exact": str(delta_r),
                   "fresh_shots_per_pair": shots,
                   "statistical_eta_after_coin_rounding_reserve": float(statistical_eta),
                   "per_report_mean_rounding_bias_bound": COIN_ROUNDING_BIAS,
                   "pair_count": n*(n+1)//2,
                   "known_report_range": 1,
                   "confidence_method": "conditional Hoeffding + 1/4 sphere net",
                   "shot_count_precision": "integer rational arithmetic; ln9<3 and ln(x)<=ceil(log2 x)"}


def row_sum_norm(a):
    return max((sum(map(abs, row), F(0)) for row in a), default=F(0))


def certify_geometry(gram_exact, eta, x):
    """Exact rational geometry/rank certificate; eigenvectors are proposals."""
    xr = rational_matrix(x)
    b = multiply(transpose(xr), xr)
    residual = subtract(gram_exact, b)
    eb = row_sum_norm(residual)
    total = F.from_float(float(eta))+eb
    xx = multiply(xr, transpose(xr))
    lower = min((xx[i][i]-sum((abs(xx[i][j]) for j in range(len(xx)) if j!=i), F(0))
                 for i in range(len(xx))), default=F(0))
    rank_ok = len(xx)==0 or lower > total
    if not rank_ok:
        raise RuntimeError("numerical rank certificate failed; no compact model emitted")
    return {"gram_factor_residual_upper": float(eb),
            "gram_factor_residual_upper_exact": str(eb),
            "total_true_gram_error_upper": float(total),
            "total_true_gram_error_upper_exact": str(total),
            "physical_column_error_upper": float(sqrt_upper(total)),
            "retained_squared_singular_lower": float(lower),
            "rank_no_larger_than_true_rank_certified": rank_ok,
            "exact_rational_final_certificate": True,
            "conditional_on_gram_confidence_event": True}


def true_target_exact(x, rule):
    return multiply(rational_matrix(x), rule)


def certified_rule_fit(a, x, rule):
    """Certify against exact acquired rational rules, not rounded targets."""
    ax = multiply(rational_matrix(a), rational_matrix(x))
    target = true_target_exact(x, rule)
    residual = subtract(ax, target)
    squared = [sum((v*v for v in col), F(0)) for col in zip(*residual)]
    return sqrt_upper(max(squared, default=F(0)))


def compact_from_reference(model, gram_exact, eta, zeta, rules):
    gram = np.array([[float(v) for v in row] for row in gram_exact])
    values, vectors = np.linalg.eigh(gram)
    kept = values > 2*eta
    x = np.sqrt(values[kept])[:, None]*vectors[:, kept].T
    geometry = certify_geometry(gram_exact, eta, x)
    alpha = geometry["physical_column_error_upper"]
    target_bound = model["rho"]+2*alpha+zeta
    matrices, fits = [], []
    for a, rule in enumerate(rules):
        target_r = true_target_exact(x, rule)
        target = np.array([[float(v) for v in row] for row in target_r])
        # A data-derived initial proposal, not a promised optimizer or basis.
        proposal = project_contraction(np.linalg.lstsq(x.T, target.T, rcond=None)[0].T)
        safe, norm_certificate = certified_contraction(proposal, perturbation_budget=1e-7)
        residual = certified_rule_fit(safe, x, rule)
        trace = {"least_squares_proposal_attempts": 1,
                 "projected_subgradient_iterations": 0,
                 "least_squares_residual_upper": float(residual)}
        if float(residual) > target_bound:
            proposal, fitted = fit_minimax_contraction(
                x, target, excess=zeta/2, max_steps=200_000,
                stop_at=target_bound-zeta/4)
            safe, norm_certificate = certified_contraction(proposal, perturbation_budget=1e-7)
            residual = certified_rule_fit(safe, x, rule)
            trace["projected_subgradient_iterations"] = fitted["iterations"]
            trace["fit_trace"] = fitted
        if float(residual) > target_bound:
            raise RuntimeError("declared optimizer cap exhausted; acquisition unsuccessful")
        trace |= {"operation": a, "certificate_threshold": target_bound,
                  "exact_fit_residual_upper": float(residual),
                  "exact_fit_residual_upper_fraction": str(residual),
                  "contraction": norm_certificate}
        matrices.append(safe)
        fits.append(trace)
    return {"x": x, "matrices": matrices, "geometry": geometry,
            "fits": fits, "beta": max(f["exact_fit_residual_upper"] for f in fits)}


def predict_compact(model, word):
    y = model["x"][:, 0].copy()
    for a in word:
        y = model["matrices"][a]@y
    return float(model["x"][:, 0]@y)


def predict_reference(model, word):
    c = np.zeros(len(model["words"]))
    c[0] = 1
    for a in word:
        c = model["matrices"][a]@c
    return float(model["outputs"]@c)


def binary64_prediction_error_bound(k, horizon, seed_norm):
    """Exact rational standard rounding bound, including subnormal reserve."""
    if k == 0:
        return F(0)
    u = F(1,1 << 53)
    gamma = k*u/(1-k*u)
    root_k = sqrt_upper(F(k))
    q = gamma*root_k
    underflow = root_k*k*F(1,1 << 1074)
    growth = (1+q)**horizon
    state_error = seed_norm*(growth-1)+horizon*underflow*growth
    state_norm = seed_norm*growth+horizon*underflow*growth
    return seed_norm*state_error+gamma*seed_norm*state_norm+underflow


def candidate_words(alphabet, horizon, seed):
    # Exhaustive short words plus paid, explicitly counted longer diagnostics.
    for length in range(6):
        yield from itertools.product(range(alphabet), repeat=length)
    rng = np.random.default_rng(seed)
    for length in [horizon, 32, 128, 512]:
        for _ in range(120):
            yield tuple(int(t) for t in rng.integers(alphabet, size=length))


def run_case(name, mixing, rho=0.02, alpha_goal=0.005, zeta=0.005,
             horizon=8, epsilon=0.5, seed=20261101):
    started = time.perf_counter()
    source = StationaryEndpointSource(mixing, seed)
    cache = ExactRecordedCache(source, rho*rho/256, delta=0.005)
    before = source.ledger()
    reference = convex_compiler(cache, 3, rho, max_centers=200)
    rules = rational_rules(reference)
    rule_certificate = certify_reference(reference, cache, rules)
    acquired = source.ledger()
    eta = alpha_goal**2/16
    gram_exact, sampling = acquire_geometry(source, reference["words"], eta, delta=0.005)
    refined = source.ledger()
    compact = compact_from_reference(reference, gram_exact, eta, zeta, rules)
    n, k = len(reference["words"]), compact["x"].shape[0]
    beta = compact["beta"]
    d = compact["geometry"]["total_true_gram_error_upper"]
    xnorm = float(np.linalg.norm(compact["x"][:,0]))
    beta_r = max(F(f["exact_fit_residual_upper_fraction"]) for f in compact["fits"])
    d_r = F(compact["geometry"]["total_true_gram_error_upper_exact"])
    xnorm_r = sqrt_upper(sum((F.from_float(float(v))**2 for v in compact["x"][:,0]),F(0)))
    exact_model_bound = horizon*F.from_float(float(rho))+d_r+xnorm_r*horizon*beta_r
    evaluation_bound = binary64_prediction_error_bound(k,horizon,xnorm_r)
    complete_bound = exact_model_bound+evaluation_bound
    if complete_bound > F.from_float(float(epsilon)):
        raise RuntimeError("task error certificate not attained; no success is claimed")

    # This block is audit-only. The learner above did not inspect source truth.
    vertices = np.column_stack([source._feature(w) for w in reference["words"]])
    true_gram = vertices.T@vertices
    raw_gram_float = np.array([[float(t) for t in row] for row in gram_exact])
    source_good = float(np.linalg.norm(raw_gram_float-true_gram, 2)) <= eta
    reference_good = all(abs(float(mean)-source.truth_gram(*pair)) <= cache.tol
                         for pair, mean in cache.exact_values.items())
    max_error, max_reference, max_ratio, programs = 0.0, 0.0, 0.0, 0
    task_max = 0.0
    for word in candidate_words(3, horizon, seed+1):
        truth = source.truth_gram((), word)
        error = abs(predict_compact(compact, word)-truth)
        old_error = abs(predict_reference(reference, word)-truth)
        bound = len(word)*rho+d+xnorm*len(word)*beta
        if error > bound+1e-10:
            raise AssertionError("held-out audit violates acquired error certificate")
        max_error, max_reference = max(max_error,error), max(max_reference,old_error)
        max_ratio = max(max_ratio, error/max(bound, 1e-15))
        if len(word) <= horizon:
            task_max = max(task_max,error)
        programs += 1
    assert source.ledger() == refined
    report = {
        "case": name, "source": "common-stationary symmetric four-state Markov controls",
        "source_control_mixing_for_audit_only": mixing,
        "acquisition_interface": "bounded endpoint product, scalar reports only",
        "physically_executed": False,
        "simulation_method": "exact aggregate binomial report law; all primitive steps charged",
        "old_atoms": n, "learned_euclidean_dimension": k,
        "retained_word_rank_audit_only": int(np.linalg.matrix_rank(vertices,tol=1e-11)),
        "source_reachable_rank_audit_only": int(np.linalg.matrix_rank(
            np.column_stack([source._feature(w) for w in [(),(2,),(2,0)]]),tol=1e-11)),
        "rho": rho, "alpha_goal": alpha_goal, "optimizer_excess_goal": zeta,
        "task_horizon": horizon, "task_epsilon": epsilon,
        "all_word_error_certificate_at_task_horizon": float(complete_bound),
        "exact_stored_model_error_bound": float(exact_model_bound),
        "binary64_evaluation_error_bound": float(evaluation_bound),
        "complete_error_bound_exact": str(complete_bound),
        "joint_failure_probability_at_most": 0.01,
        "reference_acquisition_bill": subtract_ledger(acquired,before),
        "fresh_gram_bill": subtract_ledger(refined,acquired),
        "complete_physical_bill": refined,
        "old_fw_iterations": reference["fw_iterations"],
        "old_branch_counts": reference["branch_counts"],
        "reference_certificate": rule_certificate,
        "fresh_gram_sampling": sampling,
        "geometry_certificate": compact["geometry"],
        "operator_fits": compact["fits"],
        "certified_beta": beta,
        "stored_old_dense_transition_entries": 3*n*n,
        "stored_new_dense_transition_entries": 3*k*k,
        "old_dense_scalar_multiplications_per_future_step": n*n,
        "new_dense_scalar_multiplications_per_future_step": k*k,
        "later_source_calls": 0,
        "observed_reference_confidence_event_audit_only": reference_good,
        "observed_gram_confidence_event_audit_only": source_good,
        "observed_gram_operator_error_audit_only": float(np.linalg.norm(raw_gram_float-true_gram,2)),
        "heldout_words": programs,
        "maximum_error_over_declared_task_audit": task_max,
        "maximum_error_over_all_checked_lengths_audit": max_error,
        "old_reference_maximum_error_same_words_audit": max_reference,
        "maximum_observed_error_to_proved_bound_ratio": max_ratio,
        "simulation_cpu_seconds": time.perf_counter()-started,
        "comparison_scope": "ordinary spectral/contraction fitter uses exactly this construction; no architecture advantage",
    }
    saved = {"case": name, "words": [list(w) for w in reference["words"]],
             "rational_columns": reference["rational_columns"],
             "compact_x": compact["x"].tolist(),
             "compact_matrices": [a.tolist() for a in compact["matrices"]],
             "scalar_batch_ledger": source._raw_batches}
    return report, saved


def run(outdir):
    outdir.mkdir(parents=True, exist_ok=True)
    reports, models = [], []
    for name,mixing in [("mixed_controls",0.4), ("weak_reachable_directions",1e-8)]:
        report, model = run_case(name,mixing)
        reports.append(report)
        models.append(model)
    (outdir/"compact_geometry_results.json").write_text(json.dumps(reports,indent=2)+"\n")
    (outdir/"compact_geometry_models.json").write_text(json.dumps(models,indent=2)+"\n")
    print(json.dumps([{key:r[key] for key in ["case","old_atoms","learned_euclidean_dimension",
        "all_word_error_certificate_at_task_horizon","maximum_error_over_declared_task_audit",
        "complete_physical_bill","certified_beta","simulation_cpu_seconds"]} for r in reports],indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--out",type=Path,default=Path(__file__).resolve().parent)
    run(parser.parse_args().out)
