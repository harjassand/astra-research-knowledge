"""Operation-quotient validation with an actual module-forest design consumer.

General validator accepts an explicit orbit-pair sampler. Main executable uses
known two-site physical modules, unknown dense noninvariant quadratic terms,
and an enormous arbitrary occupancy-only nuisance. Full contrast least squares
is a strong ordinary acquisition baseline; no useful graph/solver is supplied.
"""

from __future__ import annotations

import itertools
import json
import math
from fractions import Fraction
from pathlib import Path

import numpy as np

from residual_certificate import ForestModel


def module_features(configurations):
    x = np.asarray(configurations, dtype=np.int8)
    if x.ndim == 1:
        x = x[None, :]
    k = x.shape[1]//2
    modules = x.reshape(len(x), k, 2)
    q = (modules[:, :, 0]-modules[:, :, 1])/math.sqrt(2)
    s = (modules[:, :, 0]+modules[:, :, 1])/math.sqrt(2)
    columns = [q]
    for a in range(k):
        for b in range(a+1, k):
            columns.append(np.column_stack((q[:, a]*q[:, b],
                                            q[:, a]*s[:, b],
                                            s[:, a]*q[:, b])))
    return np.concatenate(columns, axis=1)


def module_orbit_pairs(rng, pair_count, site_count):
    k = site_count//2
    x = rng.choice(np.array([-1, 1], dtype=np.int8), (pair_count, site_count))
    y = x.reshape(pair_count, k, 2).copy()
    mask = rng.integers(0, 2, (pair_count, k), dtype=np.int8).astype(bool)
    swapped = y[:, :, ::-1]
    y = np.where(mask[:, :, None], swapped, y).reshape(pair_count, site_count)
    pairs = np.empty((2*pair_count, site_count), dtype=np.int8)
    pairs[0::2], pairs[1::2] = x, y
    assert np.array_equal((x.reshape(pair_count, k, 2).sum(axis=2)+2)//2,
                          (y.reshape(pair_count, k, 2).sum(axis=2)+2)//2)
    return pairs, {"orbit_sampling_fair_bits": pair_count*k,
                   "initial_configuration_fair_bits": pair_count*site_count}


def total_cardinality_pairs(rng, pair_count, site_count):
    x = rng.choice(np.array([-1, 1], dtype=np.int8), (pair_count, site_count))
    y = np.array([rng.permutation(row) for row in x], dtype=np.int8)
    assert np.array_equal(x.sum(axis=1), y.sum(axis=1))
    pairs = np.empty((2*pair_count, site_count), dtype=np.int8)
    pairs[0::2], pairs[1::2] = x, y
    return pairs, {"orbit_sampling_permutations": pair_count,
                   "initial_configuration_fair_bits": pair_count*site_count}


class ModuleModel:
    def __init__(self, k, theta):
        self.k = int(k)
        self.n = 2*k
        self.theta = np.asarray(theta, dtype=float)
        assert len(self.theta) == k+3*k*(k-1)//2

    def evaluate(self, configurations):
        one = np.asarray(configurations).ndim == 1
        values = module_features(configurations)@self.theta
        return float(values[0]) if one else values

    def edge_groups(self):
        result = []
        index = self.k
        for a in range(self.k):
            for b in range(a+1, self.k):
                result.append((a, b, self.theta[index:index+3].copy()))
                index += 3
        return result

    def forest_projection(self):
        groups = self.edge_groups()
        ranked = sorted(((float(weight@weight), a, b, weight)
                         for a, b, weight in groups), reverse=True)
        parent = list(range(self.k))

        def find(a):
            while parent[a] != a:
                parent[a] = parent[parent[a]]
                a = parent[a]
            return a

        chosen = {}
        for squared, a, b, weight in ranked:
            aa, bb = find(a), find(b)
            if aa != bb:
                parent[bb] = aa
                chosen[a, b] = weight
        theta = np.zeros_like(self.theta)
        theta[:self.k] = self.theta[:self.k]
        index = self.k
        for a, b, weight in groups:
            if (a, b) in chosen:
                theta[index:index+3] = weight
            index += 3
        return ModuleForestModel(self.k, theta)


class ModuleForestModel(ModuleModel):
    def __init__(self, k, theta):
        self.k = int(k)
        self.n = 2*k
        theta = np.asarray(theta, dtype=float)
        self.unaries = theta[:k].copy()
        self.retained_groups = []
        index = k
        for a in range(k):
            for b in range(a+1, k):
                weights = theta[index:index+3].copy()
                if np.any(weights):
                    self.retained_groups.append((a, b, weights))
                index += 3

    @property
    def theta(self):
        """Compatibility accessor; call coefficient_vector() for explicit cost."""
        return self.coefficient_vector()

    def coefficient_vector(self):
        # Dense reconstruction is used only by fixture verification. The
        # executable service retains O(k) unaries/forest edges and its actual
        # evaluate/solve methods never construct this dense vector.
        result = np.zeros(self.k+3*self.k*(self.k-1)//2)
        result[:self.k] = self.unaries
        lookup = {(a, b): w for a, b, w in self.retained_groups}
        index = self.k
        for a in range(self.k):
            for b in range(a+1, self.k):
                if (a, b) in lookup:
                    result[index:index+3] = lookup[a, b]
                index += 3
        return result

    def edge_groups(self):
        return self.retained_groups

    def evaluate(self, configurations):
        # Actual sparse O(k)-edge evaluation, not a hidden dense feature pass.
        x = np.asarray(configurations, dtype=np.int8)
        one = x.ndim == 1
        if one:
            x = x[None, :]
        modules = x.reshape(len(x), self.k, 2)
        q = (modules[:, :, 0]-modules[:, :, 1])/math.sqrt(2)
        s = (modules[:, :, 0]+modules[:, :, 1])/math.sqrt(2)
        values = q@self.unaries
        for a, b, (qq, qs, sq) in self.edge_groups():
            if qq != 0 or qs != 0 or sq != 0:
                values += qq*q[:, a]*q[:, b]+qs*q[:, a]*s[:, b]+sq*s[:, a]*q[:, b]
        return float(values[0]) if one else values

    def solve_context(self, occupancies, fields):
        c = np.asarray(occupancies, dtype=int)
        h = np.asarray(fields, dtype=float).reshape(self.k, 2)
        if len(c) != self.k or np.any((c < 0) | (c > 2)):
            raise ValueError("Each module occupancy must be 0, 1, or 2")
        active = [a for a in range(self.k) if c[a] == 1]
        index = {a: i for i, a in enumerate(active)}
        local_fields = np.array([math.sqrt(2)*self.unaries[a]+h[a, 0]-h[a, 1]
                                 for a in active])
        edges = []
        for a, b, (qq, qs, sq) in self.edge_groups():
            if a in index and b in index:
                if qq != 0:
                    edges.append((index[a], index[b], 2*qq))
            elif a in index:
                local_fields[index[a]] += 2*qs*(c[b]-1)
            elif b in index:
                local_fields[index[b]] += 2*sq*(c[a]-1)
        result = np.empty((self.k, 2), dtype=np.int8)
        for a in range(self.k):
            result[a] = (-1, -1) if c[a] == 0 else (1, 1)
        if active:
            orientation, operations = ForestModel(local_fields, edges).solve(np.zeros(len(active)))
            for a in active:
                z = orientation[index[a]]
                result[a] = (z, -z)
        else:
            operations = {"candidate_comparisons": 0, "retained_dp_entries": 0}
        assert np.array_equal((result.sum(axis=1)+2)//2, c)
        return result.reshape(-1), {"active_modules": len(active),
                                    "active_forest_edges": len(edges), **operations}


class ModuleEnergyExperiment:
    """Unknown quadratic plus unknown arbitrary occupancy nuisance."""
    def __init__(self, k, theta, nuisance_amplitude, sigma, seed):
        self.k = k
        self.n = 2*k
        self._theta = np.asarray(theta, dtype=float)
        self._amplitude = float(nuisance_amplitude)
        self.sigma = float(sigma)
        self.rng = np.random.default_rng(seed)
        self.energy_samples = 0
        self.prepared_configurations = 0
        self.control_bit_changes = 0
        self.max_absolute_energy_observed = 0.
        self.last = None

    def nuisance(self, configurations):
        x = np.asarray(configurations, dtype=np.int8)
        if x.ndim == 1:
            x = x[None, :]
        counts = ((x.reshape(len(x), self.k, 2).sum(axis=2)+2)//2).astype(np.uint64)
        radix = np.array([3**a for a in range(self.k)], dtype=np.uint64)
        code = counts@radix
        # A deterministic pseudorandom table indexed by the full context. The
        # learner never sees this evaluator; the theorem permits an arbitrary
        # function, not just this efficient fixture generator.
        with np.errstate(over="ignore"):
            z = code+np.uint64(0x9E3779B97F4A7C15)
            z = (z^(z >> np.uint64(30)))*np.uint64(0xBF58476D1CE4E5B9)
            z = (z^(z >> np.uint64(27)))*np.uint64(0x94D049BB133111EB)
            z = z^(z >> np.uint64(31))
        return self._amplitude*(z.astype(np.float64)/2**64-.5)

    def noiseless(self, configurations):
        return module_features(configurations)@self._theta+self.nuisance(configurations)

    def measure_many(self, configurations, repetitions=1):
        x = np.asarray(configurations, dtype=np.int8)
        if x.ndim == 1:
            x = x[None, :]
        if self.last is None:
            self.control_bit_changes += self.n
        else:
            self.control_bit_changes += int(np.count_nonzero(x[0] != self.last))
        self.control_bit_changes += int(np.count_nonzero(x[1:] != x[:-1]))
        self.last = x[-1].copy()
        self.energy_samples += len(x)*repetitions
        self.prepared_configurations += len(x)
        energy = self.noiseless(x)
        noise = self.rng.normal(0., self.sigma, (len(x), repetitions)).mean(axis=1)
        values = energy+noise
        self.max_absolute_energy_observed = max(self.max_absolute_energy_observed,
                                                float(np.max(np.abs(values))))
        return values

    def costs(self):
        return {"energy_samples": self.energy_samples,
                "prepared_configurations": self.prepared_configurations,
                "control_bit_changes": self.control_bit_changes}


def validate_group_action(experiment, candidate, epsilon_per_site, pair_sampler,
                          feature_radius, global_failure=.05, candidate_number=1,
                          seed=444, block_size=464):
    """Generic finite-group orbit validator, with explicit sampler callback.

    The mathematical contract requires: uniform X, Y conditionally iid on its
    orbit; group action preserves degree; arbitrary nuisance is orbit-invariant.
    The main caller constructs independent physical within-pair swaps directly.
    """
    delta = global_failure/(candidate_number*(candidate_number+1))
    threshold = epsilon_per_site*candidate.n/(2*feature_radius)
    nu = threshold/8
    blocks = math.ceil(8*math.log(4/delta))
    if blocks % 2 == 0:
        blocks += 1
    pair_count = block_size*blocks
    repetitions = max(1, math.ceil(4*experiment.sigma**2/nu**2
                                   * math.log(4*pair_count/delta)))
    rng = np.random.default_rng(seed)
    configurations, random_cost = pair_sampler(rng, pair_count, candidate.n)
    before = experiment.costs()
    observations = experiment.measure_many(configurations, repetitions)
    residual = observations-candidate.evaluate(configurations)
    contrast = residual[0::2]-residual[1::2]
    block_rms = np.sqrt(np.mean(contrast.reshape(blocks, block_size)**2, axis=1))
    median = float(np.median(block_rms))
    S = median+nu
    gamma = 2*feature_radius*S
    after = experiment.costs()
    return {"candidate_number": candidate_number, "allocated_failure": delta,
            "block_size": block_size, "blocks": blocks, "pairs": pair_count,
            "repetitions_per_configuration": repetitions,
            "noise_tolerance": nu, "median_orbit_residual_RMS": median,
            "quotient_residual_norm_upper": S,
            "all_context_regret_upper": gamma,
            "requested_regret": epsilon_per_site*candidate.n,
            "accepted": bool(gamma <= epsilon_per_site*candidate.n),
            "raw_residual_RMS_on_same_observations": float(np.sqrt(np.mean(residual**2))),
            "cost": {key: after[key]-before[key] for key in after},
            **random_cost}


def statistical_validate_group_action(experiment, candidate, epsilon_per_site,
                                      pair_sampler, feature_radius,
                                      global_failure=.05, candidate_number=1,
                                      seed=445, block_size=464, averages=None,
                                      contrast_rounding_radius=0.,
                                      exact_statistics=False,
                                      feature_radius_squared=None):
    """Replicated cross-product validator; conditional finite variance suffices.

    At each orbit pair independently measure TWO paired residual differences
    U,V. Their product has conditional expectation D^2, so centered noise bias
    is removed statistically. No per-observation confidence interval or union
    bound is used. Four raw energy shots per pair (times `averages`) are paid.
    An optional deterministic contrast-rounding interval is propagated upward.
    """
    delta = global_failure/(candidate_number*(candidate_number+1))
    target = epsilon_per_site*candidate.n/(2*feature_radius)
    if averages is None:
        averages = max(1, math.ceil(8*experiment.sigma**2/target**2))
    if averages < 1 or int(averages) != averages:
        raise ValueError("averages must be a positive integer")
    averages = int(averages)
    t = experiment.sigma**2/averages
    blocks = math.ceil(8*math.log(1/delta))
    if blocks % 2 == 0:
        blocks += 1
    pair_count = block_size*blocks
    rng = np.random.default_rng(seed)
    configurations, random_cost = pair_sampler(rng, pair_count, candidate.n)
    candidate_values = candidate.evaluate(configurations)
    before = experiment.costs()
    # Adjacent identical configurations hold two independent replicate means.
    # They cost 4N*averages shots but need no additional changed control bits.
    replicated = np.repeat(configurations, 2, axis=0)
    observations = experiment.measure_many(replicated, averages).reshape(-1, 2)
    residuals = observations-candidate_values[:, None]
    paired = residuals[0::2]-residuals[1::2]
    U, V = paired[:, 0], paired[:, 1]
    rho = float(contrast_rounding_radius)
    if rho < 0:
        raise ValueError("Roundoff radius cannot be negative")
    product = U*V
    deterministic_correction = rho*(np.abs(U)+np.abs(V))+rho*rho
    upper_product = product+deterministic_correction
    block_upper_means = np.mean(upper_product.reshape(blocks, block_size), axis=1)
    block_plain_means = np.mean(product.reshape(blocks, block_size), axis=1)
    exact_details = {}
    if exact_statistics:
        # U,V are the actually reported finite numbers. rho accounts for
        # their readout/evaluation/subtraction error. All subsequent products,
        # sums, medians and the acceptance comparison below are exact rationals.
        rho_q = Fraction.from_float(rho)
        upper_blocks, plain_blocks, correction_blocks = [], [], []
        for start in range(0, pair_count, block_size):
            plain_total = Fraction(0)
            correction_total = Fraction(0)
            for i in range(start, start+block_size):
                u_q, v_q = Fraction.from_float(float(U[i])), Fraction.from_float(float(V[i]))
                plain_total += u_q*v_q
                correction_total += rho_q*(abs(u_q)+abs(v_q))+rho_q*rho_q
            plain_blocks.append(plain_total/block_size)
            correction_blocks.append(correction_total/block_size)
            upper_blocks.append((plain_total+correction_total)/block_size)
        median_q = sorted(upper_blocks)[blocks//2]
        t_q = Fraction.from_float(float(experiment.sigma))**2/averages
        bound_q = max(Fraction(0), median_q+t_q)
        radius_q = (Fraction(feature_radius_squared) if feature_radius_squared is not None
                    else Fraction.from_float(float(feature_radius))**2)
        request_q = Fraction.from_float(float(epsilon_per_site))*candidate.n
        regret_squared_q = 4*radius_q*bound_q
        accepted = bool(regret_squared_q <= request_q*request_q)

        def upward_sqrt(value):
            result = math.sqrt(float(value))
            while Fraction.from_float(result)**2 < value:
                result = math.nextafter(result, math.inf)
            return result

        S, gamma = upward_sqrt(bound_q), upward_sqrt(regret_squared_q)
        median_upper = float(median_q)
        median_plain = float(sorted(plain_blocks)[blocks//2])
        maximum_correction = float(max(correction_blocks))
        exact_details = {"exact_rational_products_and_block_means": True,
                         "acceptance_by_exact_squared_comparison": True,
                         "exact_feature_radius_squared_supplied": feature_radius_squared is not None,
                         "norm_squared_bound_fraction": str(bound_q),
                         "largest_statistic_numerator_bits": max(
                             abs(q.numerator).bit_length() for q in upper_blocks),
                         "largest_statistic_denominator_bits": max(
                             q.denominator.bit_length() for q in upper_blocks)}
    else:
        median_upper = float(np.median(block_upper_means))
        norm_squared_upper = max(0., median_upper+t)
        S = math.sqrt(norm_squared_upper)
        gamma = 2*feature_radius*S
        accepted = bool(gamma <= epsilon_per_site*candidate.n)
        median_plain = float(np.median(block_plain_means))
        maximum_correction = float(np.max(
            np.mean(deterministic_correction.reshape(blocks, block_size), axis=1)))
    after = experiment.costs()
    return {"method": "independent_replicate_cross_products",
            "candidate_number": candidate_number, "allocated_failure": delta,
            "block_size": block_size, "blocks": blocks, "pairs": pair_count,
            "independent_paired_replicates": 2,
            "averages_per_raw_energy": averages,
            "variance_scale_t": t,
            "contrast_rounding_radius": rho,
            "median_plain_cross_product": median_plain,
            "median_upper_cross_product": median_upper,
            "largest_block_rounding_correction": maximum_correction,
            "quotient_residual_norm_upper": S,
            "all_context_regret_upper": gamma,
            "requested_regret": epsilon_per_site*candidate.n,
            "accepted": accepted,
            "cost": {key: after[key]-before[key] for key in after},
            **random_cost, **exact_details}


def full_contrast_regression(experiment, k, seed, design_multiplier=8):
    """Strong ordinary acquisition baseline: all noninvariant coefficients."""
    D = k+3*k*(k-1)//2
    rows = design_multiplier*D
    rng = np.random.default_rng(seed)
    x, random_cost = module_orbit_pairs(rng, rows, 2*k)
    features = module_features(x)
    design = (features[0::2]-features[1::2])/math.sqrt(2)
    before = experiment.costs()
    observations = experiment.measure_many(x)
    response = (observations[0::2]-observations[1::2])/math.sqrt(2)
    fitted, _, rank, singular = np.linalg.lstsq(design, response, rcond=None)
    assert rank == D
    candidate = ModuleModel(k, fitted).forest_projection()
    confidence_failure = .01
    # A strong ordinary uniform parameter ball from the same retained data.
    # Paired /sqrt(2) response noise has proxy sigma^2. A 1/2-net of the
    # D-sphere has size <=5^D, so this bound is conditional on the actual A.
    parameter_radius = (2*experiment.sigma/singular[-1]
                        * math.sqrt(2*(D*math.log(5)+math.log(2/confidence_failure))))
    fitted_forest_distance = float(np.linalg.norm(fitted-candidate.coefficient_vector()))
    conventional_residual_upper = fitted_forest_distance+parameter_radius
    after = experiment.costs()
    return candidate, {"method": "full_orbit_contrast_least_squares_then_grouped_forest",
                        "feature_dimension": D, "design_rows": rows,
                        "matrix_rank": int(rank),
                        "normalized_smallest_singular_value": float(singular[-1]/math.sqrt(rows)),
                        "normalized_largest_singular_value": float(singular[0]/math.sqrt(rows)),
                        "retained_edge_groups": sum(bool(np.any(w)) for _, _, w in candidate.edge_groups()),
                        "same_data_certificate_failure": confidence_failure,
                        "same_data_parameter_error_radius": parameter_radius,
                        "fitted_full_model_to_forest_distance": fitted_forest_distance,
                        "same_data_quotient_residual_upper": conventional_residual_upper,
                        "same_data_all_context_regret_upper": 2*math.sqrt(2)*k*conventional_residual_upper,
                        "same_data_extra_energy_shots": 0,
                        "cost": {key: after[key]-before[key] for key in after},
                        **random_cost}


def make_module_fixture(k, seed, dense_tail=.002):
    rng = np.random.default_rng(seed)
    D = k+3*k*(k-1)//2
    theta = rng.uniform(-.2, .2, D)
    theta[k:] *= 0.
    tree = set()
    for b in range(1, k):
        tree.add((int(rng.integers(b)), b))
    index = k
    for a in range(k):
        for b in range(a+1, k):
            if (a, b) in tree:
                theta[index:index+3] = rng.uniform(-.45, .45, 3)
                if np.linalg.norm(theta[index:index+3]) < .2:
                    theta[index] += .3
            theta[index:index+3] += dense_tail/k*rng.uniform(-1, 1, 3)
            index += 3
    return theta, tree


def feasible_orientations(context):
    choices = [[(-1, -1)] if c == 0 else [(1, 1)] if c == 2
               else [(-1, 1), (1, -1)] for c in context]
    return np.array([np.array(parts).reshape(-1) for parts in itertools.product(*choices)],
                    dtype=np.int8)


def verify_module_fixture(k, seed, queries):
    theta, true_tree = make_module_fixture(k, seed)
    experiment = ModuleEnergyExperiment(k, theta, 1.e6, .0001, seed+1)
    zero = ModuleForestModel(k, np.zeros_like(theta))
    rejected = validate_group_action(experiment, zero, .02, module_orbit_pairs,
                                     math.sqrt(2)*k, candidate_number=1, seed=seed+2)
    assert not rejected["accepted"]
    candidate, training = full_contrast_regression(experiment, k, seed+3)
    accepted = validate_group_action(experiment, candidate, .02, module_orbit_pairs,
                                     math.sqrt(2)*k, candidate_number=2, seed=seed+4)
    assert accepted["accepted"]
    v = float(np.sum((theta-candidate.theta)**2))
    assert math.sqrt(v) <= training["same_data_quotient_residual_upper"]
    assert math.sqrt(v) <= accepted["quotient_residual_norm_upper"]
    assert accepted["quotient_residual_norm_upper"] <= math.sqrt(3*v)+2*accepted["noise_tolerance"]
    found_tree = {(a, b) for a, b, w in candidate.edge_groups() if np.any(w)}
    assert found_tree == true_tree
    rng = np.random.default_rng(seed+5)
    previous = np.ones(2*k, dtype=np.int8)
    context_records = []
    max_solver_gap = 0.
    max_true_regret = 0.
    for t in range(queries):
        # Context itself depends on earlier answers; every request is fixed
        # before its design solve, and fields can change arbitrarily.
        context = rng.integers(0, 3, k)
        if t == 0:
            context[:] = 1
        elif t == 1:
            context[:] = 0
        elif t % 3 == 0:
            context = (np.maximum(0, previous.reshape(k, 2)[:, 0])+t) % 3
        fields = rng.uniform(-.7, .7, 2*k)+.1*previous
        answer, operations = candidate.solve_context(context, fields)
        feasible = feasible_orientations(context)
        # Full orientation enumeration per context is feasible in these tests,
        # but is not used by the acquired O(k) tree solver.
        fitted = candidate.evaluate(feasible)+feasible@fields
        true = module_features(feasible)@theta+feasible@fields
        fitted_answer = candidate.evaluate(answer)+answer@fields
        true_answer = float((module_features(answer)@theta+answer@fields).item())
        gap = fitted_answer-float(np.min(fitted))
        regret = true_answer-float(np.min(true))
        assert abs(gap) <= 1e-10
        active = int(np.sum(context == 1))
        context_bound = (2*math.sqrt(2*active*(2*k-active))
                         * accepted["quotient_residual_norm_upper"])
        assert -1e-10 <= regret <= context_bound+1e-10
        max_solver_gap = max(max_solver_gap, gap)
        max_true_regret = max(max_true_regret, regret)
        context_records.append({"context": context.tolist(),
                                "active_modules": active,
                                "DP_comparisons": operations["candidate_comparisons"],
                                "context_specific_regret_bound": context_bound})
        previous = answer
    return {"modules": k, "sites": 2*k, "possible_contexts": str(3**k),
            "all_site_configurations": str(4**k),
            "nuisance_amplitude": 1.e6,
            "largest_measured_absolute_energy": experiment.max_absolute_energy_observed,
            "earlier_bad_candidate": rejected,
            "strong_conventional_acquisition": training,
            "accepted_certificate": accepted,
            "fixture_only_true_quotient_residual_norm": math.sqrt(v),
            "adaptive_contexts_and_fields_checked": context_records,
            "max_surrogate_DP_gap_against_orientation_enumeration": max_solver_gap,
            "max_true_orientation_regret": max_true_regret,
            "total_experimental_cost": experiment.costs()}


def exact_covariance_check():
    k = 3
    x_all = np.array(list(itertools.product((-1, 1), repeat=2*k)), dtype=np.int8)
    rows = []
    for x in x_all:
        for mask in itertools.product((0, 1), repeat=k):
            y = x.reshape(k, 2).copy()
            for a, swap in enumerate(mask):
                if swap:
                    y[a] = y[a, ::-1]
            feature = module_features(np.array([x, y.reshape(-1)]))
            rows.append((feature[0]-feature[1])/math.sqrt(2))
    design = np.asarray(rows)
    covariance = design.T@design/len(design)
    error = float(np.max(np.abs(covariance-np.eye(covariance.shape[0]))))
    assert error < 1e-12
    return {"modules": k, "all_exact_pairs": len(rows),
            "feature_dimension": covariance.shape[0], "maximum_covariance_error": error}


def context_selection_failure():
    # Both models give identically zero same-orbit contrasts. They demand
    # different occupancy choices if that unearned task is requested.
    k = 5
    first = np.zeros(k, dtype=int)
    second = np.full(k, 2, dtype=int)
    return {"modules": k, "all_orbit_contrasts_in_both_worlds": 0,
            "world_one_nuisance": "g(c)=100*sum(c)",
            "world_two_nuisance": "g(c)=-100*sum(c)",
            "world_one_best_context": first.tolist(),
            "world_two_best_context": second.tolist(),
            "conclusion": "Context selection is not identified by orientation contrasts"}


def compare_statistical_validator():
    comparisons = []
    k = 5
    for index, sigma in enumerate((.0001, .002)):
        theta, _ = make_module_fixture(k, 1811+index)
        experiment = ModuleEnergyExperiment(k, theta, 1.e6, sigma, 1821+index)
        candidate, training = full_contrast_regression(experiment, k, 1831+index)
        old = validate_group_action(experiment, candidate, .02, module_orbit_pairs,
                                     math.sqrt(2)*k, candidate_number=2, seed=1841+index)
        new = statistical_validate_group_action(
            experiment, candidate, .02, module_orbit_pairs, math.sqrt(2)*k,
            candidate_number=2, seed=1851+index, contrast_rounding_radius=1.e-8)
        v = float(np.sum((theta-candidate.coefficient_vector())**2))
        assert old["accepted"] and new["accepted"]
        assert math.sqrt(v) <= new["quotient_residual_norm_upper"]
        completeness_squared = (3*v+2*new["variance_scale_t"]
                                +2*new["largest_block_rounding_correction"])
        assert new["quotient_residual_norm_upper"]**2 <= completeness_squared+1e-10
        comparisons.append({"modules": k, "sigma": sigma,
                            "epsilon_per_site": .02,
                            "actual_acquisition": training,
                            "fixture_only_true_quotient_residual_norm": math.sqrt(v),
                            "pointwise_noise_validator": old,
                            "replicate_product_validator": new,
                            "old_over_new_shot_ratio": old["cost"]["energy_samples"]
                              /new["cost"]["energy_samples"]})
    return comparisons


def main():
    results = {"status": "all orbit certificates, exact covariance, and acquired DP checks passed",
               "scope": "arbitrary occupancy nuisance plus quadratic orientation dependence",
               "covariance": exact_covariance_check(),
               "fixtures": [verify_module_fixture(5, 771, 10),
                            verify_module_fixture(10, 991, 14)],
               "context_selection_failure": context_selection_failure(),
               "statistical_validator_comparison": compare_statistical_validator()}
    target = Path(__file__).with_name("orbit_certificate_results.json")
    target.write_text(json.dumps(results, indent=2)+"\n")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
