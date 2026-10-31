"""Astra: acquisition of a metric transition table from scalar return moments.

Python 3 + numpy. The learner only sees scalar Gram estimates; latent vectors,
coordinate permutations and matrices remain behind the simulation interface.
Every simulated episode and its full primitive word length are counted.
The signed-orbit fixture uses an explicitly SUPPLIED finite separated-orbit
promise. The continuous fixtures use exact moments as algebraic diagnostics,
not as finite-noise executions. No external packages or network are needed.
"""
from __future__ import annotations
import argparse
import json
import math
from pathlib import Path
import time
import numpy as np


class SignedOrbitSource:
    """Hidden uniform bits, observed bit 0, unknown reversible signed permutations.

    Each control is an involution preserving the uniform law. A return-word
    endpoint product is +/-1 with mean equal to the feature Gram entry.
    Binomial batching samples EXACTLY that episode-count law; it avoids CPU
    replay of identical primitive paths but does not discount source costs.
    """
    def __init__(self, dimension=12, seed=20261031):
        self.d = dimension
        self.rng = np.random.default_rng(seed)
        p0 = np.arange(dimension)
        p1 = np.arange(dimension)
        for i in range(0, dimension-1, 2):
            p0[i], p0[i+1] = p0[i+1], p0[i]
        for i in range(1, dimension-1, 2):
            p1[i], p1[i+1] = p1[i+1], p1[i]
        if dimension % 2 == 0:
            p1[0], p1[-1] = p1[-1], p1[0]
        signs = np.ones(dimension, dtype=int)
        flip = signs.copy()
        flip[0] = -1
        self.maps = [(p0, signs.copy()), (p1, signs.copy()),
                     (np.arange(dimension), flip)]
        self.m = len(self.maps)
        self.episodes = 0
        self.primitive_steps = 0
        self.readouts = 0
        self.calls = 0

    def _feature(self, word):
        j, sign = 0, 1
        for a in word:
            perm, signs = self.maps[a]
            sign *= int(signs[j])
            j = int(perm[j])
        return j, sign

    def truth_gram(self, u, v):
        i, si = self._feature(u)
        j, sj = self._feature(v)
        return float(si * sj if i == j else 0)

    def sample_mean(self, u, v, n):
        mu = self.truth_gram(u, v)
        plus = self.rng.binomial(n, (1 + mu)/2)
        self.episodes += n
        self.primitive_steps += n * (len(u) + len(v))
        self.readouts += 2 * n
        self.calls += 1
        return 2 * plus / n - 1


class MomentCache:
    """One cached mean per unordered actual-word pair at a fixed accuracy.

    Conditional per-call failure <= delta/[k(k+1)] using Hoeffding for [-1,1].
    Conditional fresh episodes, rather than independence of adaptive queries,
    suffice. Here math is floating point; certificate comparisons in this
    simulator have a large margin. A general deployment needs outward rounding.
    """
    def __init__(self, source, tolerance, delta):
        self.source, self.tol, self.delta = source, tolerance, delta
        self.values = {}
        self.max_error = 0.0  # audit-only; never used for learner decisions
        self.all_covered = True

    @staticmethod
    def key(u, v):
        return (u, v) if u <= v else (v, u)

    def get(self, u, v):
        key = self.key(u, v)
        if key not in self.values:
            k = len(self.values) + 1
            dk = self.delta / (k * (k+1))
            n = math.ceil(2 / self.tol**2 * math.log(2/dk))
            estimate = self.source.sample_mean(u, v, n)
            self.values[key] = estimate
            error = abs(estimate-self.source.truth_gram(u, v))
            self.max_error = max(self.max_error, error)
            self.all_covered &= error <= self.tol
        return self.values[key]


def finite_orbit_metric(cache, n_actions):
    """Optimized exact-gap corollary for the SUPPLIED unit signed-orbit promise.

    All vectors have unit norm; distinct vectors have distance >=sqrt(2).
    Hence <u,v> is in {-1,0,1}, and threshold 1/2 decides equality when
    the mean error is <1/2. This is the metric compiler using the same extra
    structure given to the strong signed-frame comparator below.
    """
    words, edges = [()], []
    i = 0
    while i < len(words):
        row = []
        for a in range(n_actions):
            candidate = words[i] + (a,)
            destination = None
            for j, word in enumerate(words):
                if cache.get(candidate, word) > 0.5:
                    destination = j
                    break
            if destination is None:
                destination = len(words)
                words.append(candidate)
            row.append(destination)
        edges.append(row)
        i += 1
    outputs = [int(round(cache.get((), word))) for word in words]
    return {"words": words, "edges": edges, "outputs": outputs}


def retaining_signed_frame(cache, n_actions):
    """Ordinary retaining linear learner, same source and same supplied promise.

    An action image is +/- an old orthonormal direction or a new direction.
    This is standard range/basis exploration, not a new Astra learner.
    """
    words, edges = [()], []
    i = 0
    while i < len(words):
        row = []
        for a in range(n_actions):
            candidate = words[i] + (a,)
            destination = None
            for j, word in enumerate(words):
                value = cache.get(candidate, word)
                if abs(value) > 0.5:
                    destination = [j, 1 if value > 0 else -1]
                    break
            if destination is None:
                destination = [len(words), 1]
                words.append(candidate)
            row.append(destination)
        edges.append(row)
        i += 1
    outputs = [int(round(cache.get((), word))) for word in words]
    return {"words": words, "edges": edges, "outputs": outputs}


def metric_predict(model, word):
    state = 0
    for a in word:
        state = model["edges"][state][a]
    return model["outputs"][state]


def frame_predict(model, word):
    state, sign = 0, 1
    for a in word:
        state, multiplier = model["edges"][state][a]
        sign *= multiplier
    return sign * model["outputs"][state]


class ExactMatrixSource:
    """Exact-moment numerical diagnostic; NOT a noisy acquisition execution."""
    def __init__(self, matrices, seed):
        self.matrices = matrices
        self.seed = np.asarray(seed, dtype=float)
        self.features = {(): self.seed}
        self.cache = {}
        self.primitive_word_bill = 0

    def _feature(self, word):
        if word not in self.features:
            self.features[word] = self.matrices[word[-1]] @ self._feature(word[:-1])
        return self.features[word]

    def get(self, u, v):
        key = MomentCache.key(u, v)
        if key not in self.cache:
            self.cache[key] = float(self._feature(u) @ self._feature(v))
            self.primitive_word_bill += len(u)+len(v)
        return self.cache[key]


def general_metric_compiler(source, n_actions, rho, max_centers=10000):
    """General metric algorithm. Source.get must meet the declared mean bounds.

    This executable path uses ExactMatrixSource for algebraic diagnostics.
    A fixed-precision MomentCache with tolerance <=rho^2/32 implements the
    theorem's finite-noise interface without changing this algorithm.
    """
    words, edges = [()], []
    i = 0
    while i < len(words):
        row = []
        for a in range(n_actions):
            candidate = words[i] + (a,)
            destination = None
            cc = source.get(candidate, candidate)
            for j, word in enumerate(words):
                squared = cc + source.get(word, word) - 2*source.get(candidate, word)
                if squared <= 0.75*rho*rho:
                    destination = j
                    break
            if destination is None:
                if len(words) >= max_centers:
                    raise RuntimeError("diagnostic resource cap; no completed table")
                destination = len(words)
                words.append(candidate)
            row.append(destination)
        edges.append(row)
        i += 1
    outputs = [source.get((), word) for word in words]
    return {"words": words, "edges": edges, "outputs": outputs}


def convex_projection(gram, cross, squared_norm, rho):
    """Inexact Frank-Wolfe in the absolute convex hull; no Gram inverse.

    These diagnostics use exact moments. The stopping rules allow a declared
    per-entry moment error tau=rho^2/256. FW gradients and objective values
    then have the uniform errors proved in PROOF.txt. Returned coefficients
    have a rational representation (integer atom counts / triangular number).
    """
    if not 0 < rho <= 1:
        raise ValueError("rho must be in (0,1]")
    n = len(cross)
    tau = rho*rho/256
    # Metric guard preserves the finite expected-work argument off-event.
    # Check every atom, not only the maximum cross entry: norms may differ.
    distances = squared_norm + np.diag(gram) - 2*np.abs(cross)
    j = int(np.argmin(distances))
    if distances[j] <= 0.75*rho*rho:
        counts = np.zeros(n, dtype=np.int64)
        counts[j] = 1 if cross[j] >= 0 else -1
        return {"accept": True, "counts": counts, "denominator": 1,
                "iterations": 0, "estimated_residual": float(distances[j]),
                "mode": "signed_atom"}
    if squared_norm <= 0.75*rho*rho:
        return {"accept": True, "counts": np.zeros(n, dtype=np.int64),
                "denominator": 1, "iterations": 0,
                "estimated_residual": squared_norm, "mode": "zero"}

    counts = np.zeros(n, dtype=np.int64)
    gram_counts = np.zeros(n)
    denominator = 1
    limit = math.ceil(256/rho**2)
    if limit*(limit+1)//2 > np.iinfo(np.int64).max:
        raise ValueError("diagnostic int64 capacity exceeded; use arbitrary-precision integers")
    for t in range(limit+1):
        coefficients = counts/denominator
        gram_c = gram_counts/denominator
        objective = float(squared_norm - 2*cross@coefficients + coefficients@gram_c)
        if objective <= 0.75*rho*rho:
            return {"accept": True, "counts": counts, "denominator": denominator,
                    "iterations": t, "estimated_residual": objective,
                    "mode": "convex_combination"}
        gradient = 2*(gram_c-cross)
        j = int(np.argmax(np.abs(gradient)))
        sign = -1 if gradient[j] >= 0 else 1
        gap = float(gradient@coefficients + abs(gradient[j]))
        if objective-gap-12*tau > 0.5*rho*rho:
            return {"accept": False, "iterations": t,
                    "estimated_residual": objective, "mode": "separated"}
        if t == limit:
            return {"accept": False, "iterations": t,
                    "estimated_residual": objective, "mode": "iteration_bound"}
        k = t+1
        counts[j] += sign*k
        gram_counts += sign*k*gram[:,j]
        denominator = k*(k+1)//2


def convex_compiler(source, n_actions, rho, max_centers=10000, previous=None):
    if hasattr(source, "tol") and source.tol > rho*rho/256:
        raise ValueError("moment-cache tolerance does not satisfy the convex theorem")
    if previous is None:
        words, columns = [()], []
    else:
        if previous["rho"] != rho or len(previous["matrices"]) > n_actions:
            raise ValueError("incremental extension requires fixed rho and an enlarged action menu")
        words = list(previous["words"])
        columns = [list(row)+[None]*(n_actions-len(row))
                   for row in previous["rational_columns"]]
    fw_iterations = 0
    modes = {}
    i = 0
    while i < len(words):
        if i == len(columns):
            columns.append([None]*n_actions)
        row = columns[i]
        for a in range(n_actions):
            if row[a] is not None:
                continue
            candidate = words[i] + (a,)
            n = len(words)
            gram = np.array([[source.get(u,v) for v in words] for u in words])
            cross = np.array([source.get(u,candidate) for u in words])
            squared_norm = source.get(candidate,candidate)
            answer = convex_projection(gram, cross, squared_norm, rho)
            fw_iterations += answer["iterations"]
            modes[answer["mode"]] = modes.get(answer["mode"],0)+1
            if answer["accept"]:
                row[a] = {"counts": answer["counts"].tolist(),
                          "denominator": answer["denominator"]}
            else:
                if n >= max_centers:
                    raise RuntimeError("diagnostic resource cap; no completed convex model")
                words.append(candidate)
                counts = [0]*(n+1)
                counts[n] = 1
                row[a] = {"counts": counts, "denominator": 1}
        i += 1
    n = len(words)
    matrices = [np.zeros((n,n)) for _ in range(n_actions)]
    for i,row in enumerate(columns):
        for a,entry in enumerate(row):
            counts = entry["counts"]
            matrices[a][:len(counts),i] = np.array(counts)/entry["denominator"]
    outputs = np.array([source.get((),word) for word in words])
    return {"words": words, "matrices": matrices, "outputs": outputs,
            "rational_columns": columns, "fw_iterations": fw_iterations,
            "branch_counts": modes, "rho": rho}


def convex_predict(model, word):
    coefficients = np.zeros(len(model["words"]))
    coefficients[0] = 1
    for a in word:
        coefficients = model["matrices"][a]@coefficients
    return float(model["outputs"]@coefficients)


def diagnostics(outdir):
    started = time.perf_counter()
    delta = 0.01
    reports = {}
    models = {}
    for name, learner in [("metric_gap", finite_orbit_metric),
                          ("ordinary_signed_frame", retaining_signed_frame)]:
        source = SignedOrbitSource(12, 20261031)
        cache = MomentCache(source, tolerance=0.2, delta=delta)
        model = learner(cache, source.m)
        rng = np.random.default_rng(81031)
        predictor = metric_predict if name == "metric_gap" else frame_predict
        disagreements = 0
        used_words = 0
        for length in [0, 1, 2, 10, 50, 200, 1000]:
            for _ in range(200):
                word = tuple(int(a) for a in rng.integers(source.m, size=length))
                disagreements += predictor(model, word) != source.truth_gram((), word)
                used_words += 1
        # Whole transition table audit is stronger than the held-out sample.
        table_errors = 0
        for i, word in enumerate(model["words"]):
            for a in range(source.m):
                if name == "metric_gap":
                    destination = model["edges"][i][a]
                    value = source.truth_gram(word+(a,), model["words"][destination])
                    table_errors += value != 1
                else:
                    destination, sign = model["edges"][i][a]
                    value = source.truth_gram(word+(a,), model["words"][destination])
                    table_errors += value != sign
        reports[name] = {
            "hidden_microstates": 2**source.d,
            "supplied_promise": "unit signed orthonormal orbit; outputs in {-1,0,1}",
            "retained_states_or_directions": len(model["words"]),
            "scalar_mean_estimates": len(cache.values),
            "simulated_episodes": source.episodes,
            "primitive_control_steps_charged": source.primitive_steps,
            "endpoint_readouts_charged": source.readouts,
            "stationary_preparations_charged": source.episodes,
            "maximum_acquisition_word_length": max(map(len, model["words"])),
            "confidence_delta": delta,
            "maximum_observed_mean_error_audit_only": cache.max_error,
            "all_mean_errors_within_declared_tolerance": bool(cache.all_covered),
            "full_table_errors": table_errors,
            "heldout_programs": used_words,
            "heldout_disagreements": int(disagreements),
            "later_source_calls": 0,
        }
        models[name] = model

    # Continuous real contractions, exactly computed moments. This pair commutes.
    # A 2D rotation and its inverse are admissible in the abstract theorem.
    # It also factors into two self-adjoint orthogonal reflections.
    theta = 0.31
    rotation = np.array([[math.cos(theta), -math.sin(theta)],
                         [math.sin(theta), math.cos(theta)]])
    rotation_reports = []
    for rho in [0.3, 0.15, 0.075, 0.0375]:
        source = ExactMatrixSource([rotation, rotation.T], [1,0])
        model = general_metric_compiler(source, 2, rho)
        rng = np.random.default_rng(99)
        maximum_error, maximum_ratio = 0.0, 0.0
        for length in [1,3,10,30,100]:
            for _ in range(100):
                word = tuple(int(a) for a in rng.integers(2, size=length))
                truth = float(source._feature(word)[0])
                error = abs(metric_predict(model, word)-truth)
                maximum_error = max(maximum_error, error)
                maximum_ratio = max(maximum_ratio, error/(length*rho))
        residual_max = 0.0
        for i, word in enumerate(model["words"]):
            for a in range(2):
                j = model["edges"][i][a]
                residual_max = max(residual_max, float(np.linalg.norm(
                    source._feature(word+(a,))-source._feature(model["words"][j]))))
        rotation_reports.append({
            "rho": rho, "states": len(model["words"]),
            "true_linear_rank": 2, "exact_gram_queries": len(source.cache),
            "exact_query_primitive_word_bill": source.primitive_word_bill,
            "maximum_local_merge_residual": residual_max,
            "maximum_prediction_error": maximum_error,
            "maximum_error_divided_by_length_rho": maximum_ratio,
            "finite_noise_acquisition_executed": False,
            "ordinary_rotation_family_parameters": 1,
            "ordinary_same_family_exact_moments_needed": 1,
            "ordinary_noisy_precision_warning": "cos(theta) error must shrink with future horizon; not claimed free",
        })
        assert residual_max <= rho + 1e-12
        assert maximum_ratio <= 1 + 1e-10
    reports["continuous_rotation_diagnostics"] = rotation_reports

    convex_reports = []
    for rho in [0.3, 0.15, 0.075, 0.0375]:
        source = ExactMatrixSource([rotation, rotation.T], [1,0])
        model = convex_compiler(source, 2, rho)
        residual_max = 0.0
        vertices = np.column_stack([source._feature(w) for w in model["words"]])
        for a in range(2):
            residuals = source.matrices[a]@vertices - vertices@model["matrices"][a]
            residual_max = max(residual_max, float(np.max(np.linalg.norm(residuals,axis=0))))
        maximum_l1_column = max(float(np.max(np.sum(abs(m),axis=0))) for m in model["matrices"])
        rng = np.random.default_rng(99)
        maximum_error, maximum_ratio = 0.0, 0.0
        for length in [1,3,10,30,100]:
            for _ in range(100):
                word = tuple(int(a) for a in rng.integers(2,size=length))
                error = abs(convex_predict(model,word)-float(source._feature(word)[0]))
                maximum_error = max(maximum_error,error)
                maximum_ratio = max(maximum_ratio,error/(length*rho))
        convex_reports.append({
            "rho": rho, "retained_atoms": len(model["words"]), "true_linear_rank": 2,
            "exact_gram_queries": len(source.cache),
            "exact_query_primitive_word_bill": source.primitive_word_bill,
            "fw_iterations": model["fw_iterations"], "branch_counts": model["branch_counts"],
            "maximum_local_residual": residual_max,
            "maximum_l1_column_norm": maximum_l1_column,
            "maximum_prediction_error": maximum_error,
            "maximum_error_divided_by_length_rho": maximum_ratio,
            "finite_noise_acquisition_executed": False,
        })
        assert residual_max <= rho+1e-10
        assert maximum_l1_column <= 1+1e-10
        assert maximum_ratio <= 1+1e-10
    reports["bounded_combination_rotation_diagnostics"] = convex_reports

    # Genuine incremental acquisition: two baseline controls fix the seed;
    # a later third control activates directions absent from their entire orbit.
    def swap_matrix(i,j,n=4):
        p = np.eye(n)
        p[[i,j]] = p[[j,i]]
        return p
    controls = [swap_matrix(0,1), swap_matrix(2,3),
                0.6*np.eye(4)+0.4*swap_matrix(1,2)]
    source = ExactMatrixSource(controls, [0.5,0.5,-0.5,-0.5])
    old = convex_compiler(source,2,0.05)
    old_jobs = len(source.cache)
    old_bill = source.primitive_word_bill
    old_columns = json.dumps(old["rational_columns"],sort_keys=True)
    extended = convex_compiler(source,3,0.05,previous=old)
    preserved = json.dumps([row[:2] for row in extended["rational_columns"][:len(old["words"])]],
                           sort_keys=True)==old_columns
    V = np.column_stack([source._feature(w) for w in extended["words"]])
    maximum_residual = max(float(np.max(np.linalg.norm(controls[a]@V-V@extended["matrices"][a],axis=0)))
                           for a in range(3))
    reports["incremental_intervention_diagnostic"] = {
        "physical_model": "four hidden states, uniform stationary law, symmetric stochastic controls",
        "rho": 0.05, "baseline_atoms": len(old["words"]),
        "extended_atoms": len(extended["words"]),
        "baseline_scalar_moment_jobs": old_jobs,
        "additional_scalar_moment_jobs": len(source.cache)-old_jobs,
        "baseline_primitive_word_bill": old_bill,
        "additional_primitive_word_bill": source.primitive_word_bill-old_bill,
        "old_coefficient_columns_preserved": preserved,
        "all_old_moments_retained_in_cache": True,
        "maximum_local_residual": maximum_residual,
        "new_fit_FW_iterations": extended["fw_iterations"],
        "finite_noise_acquisition_executed": False,
    }
    assert preserved and maximum_residual <= 0.05+1e-10

    # No global finite separation => tiny local merges do NOT give all-horizon accuracy.
    small_angle = 0.01
    rho = 0.02
    rot = np.array([[math.cos(small_angle), -math.sin(small_angle)],
                    [math.sin(small_angle), math.cos(small_angle)]])
    source = ExactMatrixSource([rot], [1,0])
    model = general_metric_compiler(source, 1, rho)
    length = 157
    truth = math.cos(length*small_angle)
    prediction = metric_predict(model, (0,)*length)
    reports["unlimited_horizon_counterexample"] = {
        "angle": small_angle, "rho": rho, "states": len(model["words"]),
        "length": length, "prediction": prediction, "truth": truth,
        "absolute_error": abs(prediction-truth),
        "valid_length_rho_bound": length*rho,
        "demonstrates": "A finite-precision merge is not exact without a warranted orbit gap."
    }
    # Diagonal norms alone cannot provide distances/cross moments.
    reports["diagonal_only_failure"] = {
        "vectors": [[1,0], [0,1], [-1,0]],
        "all_squared_norms": [1,1,1],
        "pairwise_squared_distances_from_first": [0,2,4],
        "demonstrates": "One-feature squared norms do not replace acquired cross correlations."
    }
    reports["run_seconds"] = time.perf_counter()-started
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir/"results.json").write_text(json.dumps(reports, indent=2)+"\n")
    (outdir/"compiled_models.json").write_text(json.dumps(models, indent=2)+"\n")
    print(json.dumps(reports, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path(__file__).parent)
    args = parser.parse_args()
    diagnostics(args.output)
