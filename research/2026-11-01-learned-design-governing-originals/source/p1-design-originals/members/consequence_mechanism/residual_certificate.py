"""Executable noisy residual certificate and acquired constrained tree solver.

This is a source-cost-accounted simulation of prepared energy experiments.
Every noise draw counted in `energy_samples` is actually generated. Learning,
holdout validation and execution are separate functions. The learner sees only
the measurement API; true coefficients are used solely by fixture verification.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import dataclass
from pathlib import Path

import numpy as np


class DenseEnergyExperiment:
    def __init__(self, b, J, sigma, seed):
        self._b = np.asarray(b, dtype=float)
        self._J = np.asarray(J, dtype=float)
        self.sigma = float(sigma)
        self.rng = np.random.default_rng(seed)
        self.energy_samples = 0
        self.prepared_configurations = 0
        self.control_bit_changes = 0
        self.last = None

    def measure_many(self, configurations, repetitions=1):
        x = np.asarray(configurations, dtype=np.int8)
        if x.ndim == 1:
            x = x[None, :]
        if self.last is None:
            self.control_bit_changes += x.shape[1]
        else:
            self.control_bit_changes += int(np.count_nonzero(x[0] != self.last))
        self.control_bit_changes += int(np.count_nonzero(x[1:] != x[:-1]))
        self.last = x[-1].copy()
        self.prepared_configurations += len(x)
        self.energy_samples += len(x) * repetitions
        energies = x @ self._b + .5 * np.einsum("bi,ij,bj->b", x, self._J, x,
                                                optimize=True)
        # Actual M noise draws per energy observation, not just a cheap draw
        # from a precomputed aggregate distribution.
        noise = self.rng.normal(0., self.sigma, (len(x), repetitions)).mean(axis=1)
        return energies + noise

    def costs(self):
        return {"energy_samples": self.energy_samples,
                "prepared_configurations": self.prepared_configurations,
                "control_bit_changes": self.control_bit_changes}


@dataclass
class QuadraticModel:
    b: np.ndarray
    edges: list

    @property
    def n(self):
        return len(self.b)

    def evaluate(self, configurations):
        x = np.asarray(configurations, dtype=np.int8)
        one = x.ndim == 1
        if one:
            x = x[None, :]
        values = x @ self.b
        for i, j, weight in self.edges:
            values = values + weight * x[:, i] * x[:, j]
        return float(values[0]) if one else values

    def matrix(self):
        result = np.zeros((self.n, self.n))
        for i, j, weight in self.edges:
            result[i, j] = result[j, i] = weight
        return result


class ForestModel(QuadraticModel):
    def __post_init__(self):
        # Dataclass inheritance does not automatically call this hook, so the
        # topology is built lazily by the explicit method below.
        pass

    def topology(self):
        adjacency = [[] for _ in range(self.n)]
        for i, j, weight in self.edges:
            adjacency[i].append((j, weight))
            adjacency[j].append((i, weight))
        parent = [-2] * self.n
        children = [[] for _ in range(self.n)]
        order = []
        roots = []
        for root in range(self.n):
            if parent[root] != -2:
                continue
            roots.append(root)
            parent[root] = -1
            stack = [root]
            while stack:
                i = stack.pop()
                order.append(i)
                for j, weight in adjacency[i]:
                    if j == parent[i]:
                        continue
                    if parent[j] != -2:
                        raise ValueError("Supplied candidate is not a forest")
                    parent[j] = i
                    children[i].append((j, weight))
                    stack.append(j)
        return children, order, roots

    def solve(self, fields, cardinality=None):
        """Exact tree DP; optional exact global number of +1 spins.

        The cardinality solver stores count and root spin, performs actual
        child-table convolutions, and backtracks an actual configuration.
        No optimizer or planning oracle is called.
        """
        h = np.asarray(fields, dtype=float)
        if len(h) != self.n:
            raise ValueError("Wrong field dimension")
        total_fields = self.b + h
        if cardinality is None:
            return self._unconstrained(total_fields)
        if not isinstance(cardinality, (int, np.integer)) or not 0 <= cardinality <= self.n:
            raise ValueError("Cardinality must be an integer between 0 and n")
        if cardinality > self.n // 2:
            x, metadata = self._cardinality(-total_fields, self.n-cardinality)
            metadata["complemented_budget"] = True
            return -x, metadata
        return self._cardinality(total_fields, cardinality)

    def _unconstrained(self, fields):
        children, order, roots = self.topology()
        dp = {}
        choices = {}
        operations = 0
        for i in reversed(order):
            dp[i] = {}
            for s in (-1, 1):
                value = fields[i] * s
                for child, weight in children[i]:
                    candidates = [(dp[child][t] + weight*s*t, t) for t in (-1, 1)]
                    best, chosen = min(candidates)
                    value += best
                    choices[i, s, child] = chosen
                    operations += 2
                dp[i][s] = float(value)
        x = np.zeros(self.n, dtype=np.int8)
        stack = [(root, min((-1, 1), key=lambda s: dp[root][s])) for root in roots]
        while stack:
            i, s = stack.pop()
            x[i] = s
            stack.extend((child, choices[i, s, child]) for child, _ in children[i])
        return x, {"solver": "two_state_tree_dp", "candidate_comparisons": operations,
                   "retained_dp_entries": 2*self.n}

    def _cardinality(self, fields, budget):
        children, order, roots = self.topology()
        dp = {}
        traces = {}
        operations = 0
        entries = 0
        for i in reversed(order):
            dp[i] = {}
            for s in (-1, 1):
                initial_count = int(s == 1)
                current = ({initial_count: float(fields[i]*s)}
                           if initial_count <= budget else {})
                child_traces = []
                for child, weight in children[i]:
                    # For each child count find its best root spin, conditional
                    # on the current node's root spin.
                    child_options = {}
                    for t in (-1, 1):
                        for count, value in dp[child][t].items():
                            candidate = (value+weight*s*t, t)
                            if count not in child_options or candidate < child_options[count]:
                                child_options[count] = candidate
                    updated = {}
                    record = {}
                    for previous_count, previous_value in current.items():
                        for child_count, (child_value, t) in child_options.items():
                            count = previous_count + child_count
                            if count > budget:
                                continue
                            value = previous_value + child_value
                            operations += 1
                            if count not in updated or value < updated[count]:
                                updated[count] = value
                                record[count] = (previous_count, child_count, t)
                    current = updated
                    child_traces.append(record)
                dp[i][s] = current
                traces[i, s] = child_traces
                entries += len(current)
        # Join disconnected components through a dummy zero-field root.
        current = {0: 0.}
        global_traces = []
        for root in roots:
            options = {}
            for s in (-1, 1):
                for count, value in dp[root][s].items():
                    candidate = value, s
                    if count not in options or candidate < options[count]:
                        options[count] = candidate
            updated = {}
            record = {}
            for previous_count, previous_value in current.items():
                for root_count, (root_value, s) in options.items():
                    count = previous_count+root_count
                    if count > budget:
                        continue
                    operations += 1
                    value = previous_value+root_value
                    if count not in updated or value < updated[count]:
                        updated[count] = value
                        record[count] = previous_count, root_count, s
            current = updated
            global_traces.append(record)
        if budget not in current:
            raise RuntimeError("No feasible assignment in cardinality DP")
        x = np.zeros(self.n, dtype=np.int8)
        stack = []
        count = budget
        for k in reversed(range(len(roots))):
            previous_count, root_count, s = global_traces[k][count]
            stack.append((roots[k], s, root_count))
            count = previous_count
        while stack:
            i, s, count = stack.pop()
            x[i] = s
            records = traces[i, s]
            for k in reversed(range(len(children[i]))):
                child, _ = children[i][k]
                previous_count, child_count, t = records[k][count]
                stack.append((child, t, child_count))
                count = previous_count
            assert count == int(s == 1)
        assert int(np.sum(x == 1)) == budget
        return x, {"solver": "cardinality_tree_dp", "effective_budget": budget,
                   "convolution_candidates": operations,
                   "retained_dp_entries": entries, "complemented_budget": False}


def acquire_forest(experiment, n, repetitions=1):
    """Noisy whole-quadratic pilot, then exact maximum-spanning-forest projection.

    A deliberately strong conventional construction, not a claimed optimal
    learner. The final validator does not depend on parameter-wise guarantees.
    """
    plus = np.ones(n, dtype=np.int8)
    minus = -plus
    configurations = [plus.copy(), minus.copy()]
    plus_indices = {}
    minus_indices = {}
    for i in range(n):
        x = plus.copy()
        x[i] = -1
        plus_indices[i] = len(configurations)
        configurations.append(x)
        x = minus.copy()
        x[i] = +1
        minus_indices[i] = len(configurations)
        configurations.append(x)
    pair_indices = {}
    for i in range(n):
        for j in range(i+1, n):
            x = plus.copy()
            x[i] = x[j] = -1
            pair_indices[i, j] = len(configurations)
            configurations.append(x)
    before = experiment.costs()
    observations = experiment.measure_many(np.asarray(configurations), repetitions)
    b = np.array([(observations[0]-observations[plus_indices[i]]
                   + observations[minus_indices[i]]-observations[1])/4
                  for i in range(n)])
    candidate_edges = []
    for (i, j), index in pair_indices.items():
        weight = (observations[0]-observations[plus_indices[i]]
                  -observations[plus_indices[j]]+observations[index])/4
        candidate_edges.append((float(weight*weight), i, j, float(weight)))
    candidate_edges.sort(reverse=True)
    parent = list(range(n))
    rank = [0]*n

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    edges = []
    for _, i, j, weight in candidate_edges:
        a, b_root = find(i), find(j)
        if a == b_root:
            continue
        if rank[a] < rank[b_root]:
            a, b_root = b_root, a
        parent[b_root] = a
        if rank[a] == rank[b_root]:
            rank[a] += 1
        edges.append((i, j, weight))
    after = experiment.costs()
    metadata = {"method": "noisy_four_point_then_maximum_squared_weight_forest",
                "repetitions": repetitions,
                "cost": {key: after[key]-before[key] for key in after},
                "coefficients_proposed": n+n*(n-1)//2,
                "retained_unaries": n, "retained_edges": len(edges)}
    return ForestModel(b, edges), metadata


def validate(experiment, candidate, epsilon_per_site, global_failure=.05,
             candidate_number=1, seed=1221, relative_noise_tolerance=.125):
    """Fresh adaptive-safe median-of-means operational certificate."""
    n = candidate.n
    K = n+n*(n-1)//2
    delta = 6*global_failure/(math.pi**2*candidate_number**2)
    threshold = epsilon_per_site*n/(2*math.sqrt(K))
    nu = relative_noise_tolerance*threshold
    block_size = 128
    blocks = math.ceil(8*math.log(4/delta))
    if blocks % 2 == 0:
        blocks += 1
    pairs = block_size*blocks
    repetitions = max(1, math.ceil(4*experiment.sigma**2/nu**2
                                   * math.log(4*pairs/delta)))
    rng = np.random.default_rng(seed)
    configurations = rng.choice(np.array([-1, 1], dtype=np.int8), (2*pairs, n))
    before = experiment.costs()
    measured = experiment.measure_many(configurations, repetitions)
    residuals = measured-candidate.evaluate(configurations)
    differences = residuals[0::2]-residuals[1::2]
    block_rms = np.sqrt(np.mean(differences.reshape(blocks, block_size)**2, axis=1))
    median = float(np.median(block_rms))
    S = median+nu
    gamma = 2*math.sqrt(K)*S
    after = experiment.costs()
    return {"candidate_number": candidate_number, "allocated_failure": delta,
            "block_size": block_size, "blocks": blocks, "independent_pairs": pairs,
            "repetitions_per_configuration": repetitions,
            "pair_noise_tolerance": nu, "median_block_rms": median,
            "residual_L2_upper": S, "oscillation_upper": gamma,
            "task_regret_budget": epsilon_per_site*n,
            "accepted": bool(gamma <= epsilon_per_site*n),
            "cost": {key: after[key]-before[key] for key in after},
            "candidate_evaluations": 2*pairs,
            "candidate_monomial_evaluations": 2*pairs*(n+len(candidate.edges))}


def truth_energy(configurations, b, J, h=None):
    x = np.asarray(configurations, dtype=np.int8)
    one = x.ndim == 1
    if one:
        x = x[None, :]
    fields = b if h is None else b+np.asarray(h)
    result = x @ fields + .5*np.einsum("bi,ij,bj->b", x, J, x, optimize=True)
    return float(result[0]) if one else result


def all_configurations(n):
    return np.array(list(itertools.product((-1, 1), repeat=n)), dtype=np.int8)


def make_dense_perturbed_tree(n, seed, perturbation=.004):
    rng = np.random.default_rng(seed)
    b = rng.uniform(-.2, .2, n)
    J = np.zeros((n, n))
    # Random parent construction is a tree, unknown to the learner.
    true_tree = set()
    for i in range(1, n):
        j = int(rng.integers(i))
        J[i, j] = J[j, i] = rng.choice((-1, 1))*rng.uniform(.25, .8)
        true_tree.add((j, i))
    # Every pair gets a generic nonzero perturbation: the true graph is dense.
    for i in range(n):
        for j in range(i+1, n):
            J[i, j] += perturbation/n*rng.uniform(-1, 1)
            J[j, i] = J[i, j]
    return b, J, true_tree


def check_fixture(n, seed, query_count, full_enumeration):
    b, J, tree = make_dense_perturbed_tree(n, seed)
    experiment = DenseEnergyExperiment(b, J, .0002, seed+1)
    zero = ForestModel(np.zeros(n), [])
    rejected = validate(experiment, zero, .03, candidate_number=1, seed=seed+2)
    assert not rejected["accepted"]
    candidate, learning = acquire_forest(experiment, n, repetitions=1)
    accepted = validate(experiment, candidate, .03, candidate_number=2, seed=seed+3)
    assert accepted["accepted"]
    coefficient_residual = J-candidate.matrix()
    v = float(np.sum((b-candidate.b)**2)
              + np.sum(np.triu(coefficient_residual, 1)**2))
    assert math.sqrt(v) <= accepted["residual_L2_upper"]
    assert accepted["residual_L2_upper"] <= math.sqrt(3*v)+2*accepted["pair_noise_tolerance"]
    assert {(i, j) for i, j, _ in candidate.edges} == tree
    configs = all_configurations(n) if full_enumeration else None
    if full_enumeration:
        residual_values = truth_energy(configs, b, J)-candidate.evaluate(configs)
        true_oscillation = float(np.ptp(residual_values))
        assert true_oscillation <= accepted["oscillation_upper"]
    else:
        true_oscillation = None
    rng = np.random.default_rng(seed+4)
    previous = np.ones(n, dtype=np.int8)
    max_regret = 0.
    max_solver_gap = 0.
    max_dp_operations = 0
    budgets = []
    for t in range(query_count):
        h = rng.uniform(-.8, .8, n)+.1*previous*((-1)**t)
        budget = None if t % 4 == 0 else int(rng.integers(n+1))
        budgets.append(budget)
        answer, solver = candidate.solve(h, budget)
        max_dp_operations = max(max_dp_operations,
                                solver.get("convolution_candidates",
                                           solver.get("candidate_comparisons", 0)))
        if budget is not None:
            assert int(np.sum(answer == 1)) == budget
        if full_enumeration:
            feasible = configs if budget is None else configs[np.sum(configs == 1, axis=1) == budget]
            true_optimum = float(np.min(truth_energy(feasible, b, J, h)))
            fitted_optimum = float(np.min(candidate.evaluate(feasible)+feasible@h))
            fitted_answer = float(candidate.evaluate(answer)+answer@h)
            gap = fitted_answer-fitted_optimum
            assert abs(gap) <= 1e-10
            max_solver_gap = max(max_solver_gap, gap)
            regret = truth_energy(answer, b, J, h)-true_optimum
            assert -1e-10 <= regret <= accepted["oscillation_upper"]+1e-10
            max_regret = max(max_regret, regret)
        previous = answer
    return {"n": n, "true_nonzero_edges": n*(n-1)//2,
            "learned_forest_edges": len(candidate.edges),
            "earlier_candidate": rejected, "acquisition": learning,
            "accepted_certificate": accepted, "total_experiment_cost": experiment.costs(),
            "fixture_only_true_residual_L2": math.sqrt(v),
            "fixture_only_true_residual_oscillation": true_oscillation,
            "adaptive_fields_and_cardinalities": budgets,
            "largest_DP_candidate_count": max_dp_operations,
            "full_enumeration_checked": full_enumeration,
            "max_true_regret_when_enumerated": max_regret if full_enumeration else None,
            "max_surrogate_solver_gap_when_enumerated": max_solver_gap if full_enumeration else None,
            "full_configuration_count": str(2**n)}


def rank_one_prediction_failure():
    rows = []
    for n in (32, 128, 512):
        alpha = 1.
        possible_S = np.arange(-n, n+1, 2)
        objective = alpha/(2*n)*(possible_S**2-n)-alpha*possible_S/4
        optimum = float(np.min(objective))
        output = alpha/(2*n)*(n*n-n)-alpha*n/4
        regret = output-optimum
        assert abs(regret-9*alpha*n/32) < 1e-10
        rms = alpha*math.sqrt(n*(n-1)/2)/n
        rows.append({"n": n, "each_edge_error": alpha/n,
                     "per_site_random_prediction_RMS": rms/n,
                     "optimization_regret": regret, "regret_per_site": regret/n,
                     "true_best_magnetization": int(possible_S[np.argmin(objective)])})
    n = 32
    J = (np.ones((n, n))-np.eye(n))/n
    experiment = DenseEnergyExperiment(np.zeros(n), J, 0., 11)
    certificate = validate(experiment, ForestModel(np.zeros(n), []), .01, seed=12)
    assert not certificate["accepted"]
    return {"scaling": rows, "independent_certificate_rejects": certificate}


def holdout_reuse_failure():
    n = 12
    rng = np.random.default_rng(9001)
    old_pairs = 8
    configurations = rng.choice(np.array([-1, 1], dtype=np.int8), (2*old_pairs, n))
    pairs = list(itertools.combinations(range(n), 2))

    def features(x):
        return np.concatenate([x, np.array([x[:, i]*x[:, j] for i, j in pairs]).T], axis=1)

    feature_rows = features(configurations)
    differences = feature_rows[0::2]-feature_rows[1::2]
    _, _, vh = np.linalg.svd(differences.astype(float), full_matrices=True)
    coefficients = vh[-1]
    model = QuadraticModel(coefficients[:n], [(i, j, float(w))
                            for (i, j), w in zip(pairs, coefficients[n:])])
    old_error = float(np.max(np.abs(differences@coefficients)))
    assert old_error < 1e-12
    experiment = DenseEnergyExperiment(np.zeros(n), np.zeros((n, n)), 0., 1991)
    fresh = validate(experiment, model, .01, seed=1992)
    assert not fresh["accepted"]
    return {"old_pair_count": old_pairs, "quadratic_feature_dimension": len(coefficients),
            "max_old_validation_pair_error": old_error,
            "true_residual_L2": float(np.linalg.norm(coefficients)),
            "fresh_validation": fresh}


def check_quadratic_moment_constant():
    n = 10
    x = all_configurations(n)
    rng = np.random.default_rng(9102)
    maximum_ratio = 0.
    for _ in range(20):
        b = rng.normal(size=n)
        J = rng.normal(size=(n, n))
        J = (J+J.T)/2
        np.fill_diagonal(J, 0.)
        values = truth_energy(x, b, J)
        values -= np.mean(values)
        variance = float(np.mean(values**2))
        ratio = float(np.mean(values**4)/variance**2)
        maximum_ratio = max(maximum_ratio, ratio)
        assert ratio <= 15+1e-10
    return {"exhaustive_random_quadratics": 20, "dimension": n,
            "maximum_fourth_over_variance_squared": maximum_ratio,
            "proved_bound": 15}


def main():
    output = {"status": "all residual, adaptive-use, and constrained-DP checks passed",
              "scope": "unknown dense quadratic residual; actual learned forest and cardinality DP",
              "fixtures": [check_fixture(14, 33, 12, True),
                           check_fixture(64, 559, 15, False)],
              "prediction_failure": rank_one_prediction_failure(),
              "holdout_reuse_failure": holdout_reuse_failure(),
              "moment_checks": check_quadratic_moment_constant()}
    target = Path(__file__).with_name("residual_certificate_results.json")
    target.write_text(json.dumps(output, indent=2)+"\n")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
