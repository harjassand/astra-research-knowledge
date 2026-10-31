"""Learn a forest only where decisions interact.

q_a*s_b coefficients can be cyclic/dense: after occupancy is specified they
are unary orientation fields. Only q_a*q_b coefficients need a forest. The
compiled service retains sparse coefficients, evaluates a rational fixed-point
candidate, and solves its actual finite-field input with exact integer DP.
"""

from __future__ import annotations

import itertools
import json
import math
from fractions import Fraction
from pathlib import Path

import numpy as np

from orbit_certificate import (ModuleEnergyExperiment, ModuleModel,
                               module_features, module_orbit_pairs,
                               statistical_validate_group_action,
                               feasible_orientations)


def pair_locations(k):
    index = k
    for a in range(k):
        for b in range(a+1, k):
            yield a, b, index
            index += 3


def project_conditional_coefficients(k, theta, cross_budget=None):
    """Exact Euclidean support projection in the orthonormal q/s basis.

    All unaries are retained; qq uses a maximum-squared-weight forest; cross
    terms use top-|coefficient| selection. No rounding is done in this helper.
    """
    theta = np.asarray(theta, dtype=float)
    D = k+3*k*(k-1)//2
    if theta.shape != (D,):
        raise ValueError("Wrong coefficient dimension")
    maximum_cross = k*(k-1)
    if cross_budget is None:
        cross_budget = maximum_cross
    if not isinstance(cross_budget, (int, np.integer)) or not 0 <= cross_budget <= maximum_cross:
        raise ValueError("Invalid cross coefficient budget")
    output = np.zeros_like(theta)
    output[:k] = theta[:k]
    qq_candidates = []
    cross_candidates = []
    for a, b, index in pair_locations(k):
        # Absolute-value ordering is exactly squared-weight ordering and avoids
        # overflow or a rounded square comparison for finite binary inputs.
        qq_candidates.append((abs(float(theta[index])), a, b, index))
        cross_candidates.extend([(abs(float(theta[index+1])), index+1),
                                 (abs(float(theta[index+2])), index+2)])
    parent = list(range(k))

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    for _, a, b, index in sorted(qq_candidates, reverse=True):
        aa, bb = find(a), find(b)
        if aa != bb:
            parent[bb] = aa
            output[index] = theta[index]
    for _, index in sorted(cross_candidates, reverse=True)[:cross_budget]:
        output[index] = theta[index]
    return output


class ModuleConditionalForestModel:
    def __init__(self, k, unary, qq_edges, cross_terms, grid_bits=40):
        self.k = int(k)
        self.n = 2*self.k
        if not isinstance(grid_bits, int) or grid_bits < 0:
            raise ValueError("grid_bits must be a nonnegative integer")
        self.grid_bits = grid_bits
        self.denominator = 1 << grid_bits
        if len(unary) != k:
            raise ValueError("Wrong unary dimension")
        # Store the actual rational candidate in orientation coordinates:
        # d=(x1-x2)/2 and z=(x1+x2)/2, each in {-1,0,1}.
        self.unary_units = [int(round(math.sqrt(2)*float(value)*self.denominator))
                            for value in unary]
        self.qq_units = []
        parent = list(range(k))

        def find(a):
            while parent[a] != a:
                parent[a] = parent[parent[a]]
                a = parent[a]
            return a

        seen = set()
        for a, b, value in qq_edges:
            a, b = min(int(a), int(b)), max(int(a), int(b))
            if not 0 <= a < b < k or (a, b) in seen:
                raise ValueError("Invalid or duplicate qq edge")
            seen.add((a, b))
            weight = int(round(2*float(value)*self.denominator))
            if weight == 0:
                continue
            aa, bb = find(a), find(b)
            if aa == bb:
                raise ValueError("qq support must be a forest")
            parent[bb] = aa
            self.qq_units.append((a, b, weight))
        cross_accumulator = {}
        for active, context, value in cross_terms:
            active, context = int(active), int(context)
            if active == context or not 0 <= active < k or not 0 <= context < k:
                raise ValueError("Invalid cross coefficient")
            key = active, context
            cross_accumulator[key] = cross_accumulator.get(key, 0.)+float(value)
        self.cross_units = []
        for (active, context), value in sorted(cross_accumulator.items()):
            weight = int(round(2*value*self.denominator))
            if weight:
                self.cross_units.append((active, context, weight))
        self.absolute_units_bound = (sum(abs(w) for w in self.unary_units)
                                     + sum(abs(w) for _, _, w in self.qq_units)
                                     + sum(abs(w) for _, _, w in self.cross_units))

    @classmethod
    def from_coefficients(cls, k, theta, cross_budget=None, grid_bits=40):
        projected = project_conditional_coefficients(k, theta, cross_budget)
        qq, cross = [], []
        for a, b, index in pair_locations(k):
            if projected[index]:
                qq.append((a, b, projected[index]))
            if projected[index+1]:
                cross.append((a, b, projected[index+1]))
            if projected[index+2]:
                cross.append((b, a, projected[index+2]))
        return cls(k, projected[:k], qq, cross, grid_bits)

    def coefficient_vector(self):
        """Explicit dense reconstruction; not used by the retained service."""
        theta = np.zeros(self.k+3*self.k*(self.k-1)//2)
        theta[:self.k] = np.array(self.unary_units, dtype=float)/(self.denominator*math.sqrt(2))
        qq = {(a, b): w for a, b, w in self.qq_units}
        cross = {(a, b): w for a, b, w in self.cross_units}
        for a, b, index in pair_locations(self.k):
            theta[index] = qq.get((a, b), 0)/(2*self.denominator)
            theta[index+1] = cross.get((a, b), 0)/(2*self.denominator)
            theta[index+2] = cross.get((b, a), 0)/(2*self.denominator)
        return theta

    def evaluate(self, configurations):
        x = np.asarray(configurations, dtype=np.int8)
        one = x.ndim == 1
        if one:
            x = x[None, :]
        modules = x.reshape(len(x), self.k, 2)
        d = ((modules[:, :, 0]-modules[:, :, 1])//2)
        s = ((modules[:, :, 0]+modules[:, :, 1])//2)
        dtype = np.int64 if self.absolute_units_bound < 2**62 else object
        d = d.astype(dtype)
        s = s.astype(dtype)
        values = d@np.asarray(self.unary_units, dtype=dtype)
        for a, b, weight in self.qq_units:
            values += weight*d[:, a]*d[:, b]
        for a, b, weight in self.cross_units:
            values += weight*d[:, a]*s[:, b]
        result = np.asarray(values, dtype=float)/self.denominator
        if not np.all(np.isfinite(result)):
            raise OverflowError("Energy readout requires a larger numeric dynamic range")
        return float(result[0]) if one else result

    def solve_context(self, occupancies, fields):
        """Exact minimizer of compiled rational F plus exact finite input h.

        Floating input fields are treated as their exact represented binary
        rationals. Fractions and integer fields are accepted directly. No
        floating comparison is used in the actual optimization.
        """
        raw_context = list(occupancies)
        c = [int(v) for v in raw_context]
        if (len(c) != self.k or any(v not in (0, 1, 2) for v in c)
                or any(v != integer for v, integer in zip(raw_context, c))):
            raise ValueError("Invalid occupancy vector")
        raw_fields = np.asarray(fields, dtype=object).reshape(self.k, 2)
        rational_fields = []
        scale = self.denominator
        for value in raw_fields.flat:
            if isinstance(value, Fraction):
                f = value
            elif isinstance(value, (int, np.integer)):
                f = Fraction(int(value))
            elif isinstance(value, (float, np.floating)):
                f = Fraction.from_float(float(value))
            else:
                f = Fraction(value)
            rational_fields.append(f)
            scale = math.lcm(scale, f.denominator)
        field_units = [f.numerator*(scale//f.denominator) for f in rational_fields]
        multiplier = scale//self.denominator
        active = [a for a in range(self.k) if c[a] == 1]
        active_set = set(active)
        local = {a: self.unary_units[a]*multiplier
                    + field_units[2*a]-field_units[2*a+1] for a in active}
        for a, b, weight in self.cross_units:
            if a in active_set:
                local[a] += weight*multiplier*(c[b]-1)
        adjacency = {a: [] for a in active}
        for a, b, weight in self.qq_units:
            if a in active_set and b in active_set:
                adjacency[a].append((b, weight*multiplier))
                adjacency[b].append((a, weight*multiplier))
        parent = {}
        children = {a: [] for a in active}
        order, roots = [], []
        for root in active:
            if root in parent:
                continue
            parent[root] = None
            roots.append(root)
            stack = [root]
            while stack:
                a = stack.pop()
                order.append(a)
                for b, weight in adjacency[a]:
                    if b == parent[a]:
                        continue
                    if b in parent:
                        raise RuntimeError("Corrupt compiled forest")
                    parent[b] = a
                    children[a].append((b, weight))
                    stack.append(b)
        dp, choices = {}, {}
        comparisons = 0
        for a in reversed(order):
            for z in (-1, 1):
                value = local[a]*z
                for b, weight in children[a]:
                    minus, plus = dp[b, -1]-weight*z, dp[b, 1]+weight*z
                    chosen = -1 if minus <= plus else 1
                    value += minus if chosen == -1 else plus
                    choices[a, z, b] = chosen
                    comparisons += 1
                dp[a, z] = value
        answer = np.empty((self.k, 2), dtype=np.int8)
        for a in range(self.k):
            answer[a] = (-1, -1) if c[a] == 0 else (1, 1)
        stack = [(root, -1 if dp[root, -1] <= dp[root, 1] else 1) for root in roots]
        while stack:
            a, z = stack.pop()
            answer[a] = (z, -z)
            stack.extend((b, choices[a, z, b]) for b, _ in children[a])
        return answer.reshape(-1), {"active_modules": len(active),
                                    "exact_integer_DP": True,
                                    "integer_comparisons": comparisons,
                                    "cross_terms_scanned": len(self.cross_units),
                                    "common_denominator_bits": scale.bit_length(),
                                    "largest_integer_DP_bits": max(
                                        (abs(value).bit_length() for value in dp.values()), default=0),
                                    "largest_input_field_numerator_bits": max(
                                        (abs(f.numerator).bit_length() for f in rational_fields), default=0),
                                    "retained_scalar_coefficients": self.k
                                      +len(self.qq_units)+len(self.cross_units)}


def conditional_iht(design, response, k, cross_budget, iterations=100,
                    step=1., initial=None, compile_grid_bits=40):
    """Actual projection/IHT helper. A valid design condition is NOT asserted."""
    A = np.asarray(design, dtype=float)
    y = np.asarray(response, dtype=float)
    m, D = A.shape
    theta = np.zeros(D) if initial is None else np.asarray(initial, dtype=float).copy()
    history = []
    for _ in range(iterations):
        proposal = theta+step*(A.T@(y-A@theta))/m
        theta = project_conditional_coefficients(k, proposal, cross_budget)
        residual = A@theta-y
        history.append(float(np.mean(residual*residual)))
        if not np.isfinite(history[-1]):
            raise FloatingPointError("IHT diverged; no acquisition claim is certified")
    candidate = ModuleConditionalForestModel.from_coefficients(
        k, theta, cross_budget, compile_grid_bits)
    return candidate, {"iterations": iterations, "step": step,
                       "training_squared_residual_history": history,
                       "projection_calls": iterations,
                       "note": "Training fit is not a certificate; validate independently"}


def full_contrast_conditional_regression(experiment, k, cross_budget, seed,
                                         design_multiplier=4, grid_bits=40):
    """Strong ordinary full-parameter alternative, with same-data certificate."""
    D = k+3*k*(k-1)//2
    m = design_multiplier*D
    rng = np.random.default_rng(seed)
    configurations, random_cost = module_orbit_pairs(rng, m, 2*k)
    phi = module_features(configurations)
    A = (phi[0::2]-phi[1::2])/math.sqrt(2)
    before = experiment.costs()
    measured = experiment.measure_many(configurations)
    y = (measured[0::2]-measured[1::2])/math.sqrt(2)
    fitted, _, rank, singular = np.linalg.lstsq(A, y, rcond=None)
    if rank != D:
        raise RuntimeError("Full contrast design did not acquire the whole coefficient space")
    candidate = ModuleConditionalForestModel.from_coefficients(k, fitted, cross_budget, grid_bits)
    conventional_grouped = ModuleModel(k, fitted).forest_projection()
    delta = .01
    radius = 2*experiment.sigma/singular[-1]*math.sqrt(2*(D*math.log(5)+math.log(2/delta)))
    after = experiment.costs()
    distance = float(np.linalg.norm(fitted-candidate.coefficient_vector()))
    return candidate, conventional_grouped, fitted, {
        "method": "full_contrast_OLS_then_operation_specific_projection",
        "feature_dimension": D, "design_rows": m, "rank": int(rank),
        "smallest_normalized_singular_value": float(singular[-1]/math.sqrt(m)),
        "cost": {key: after[key]-before[key] for key in after}, **random_cost,
        "same_data_parameter_radius": radius,
        "same_data_residual_norm_upper": distance+radius,
        "same_data_all_context_regret_upper": 2*math.sqrt(2)*k*(distance+radius),
        "same_data_failure": delta, "same_data_extra_shots": 0}


def make_cyclic_cross_fixture(k, seed, tail=.001):
    rng = np.random.default_rng(seed)
    theta = np.zeros(k+3*k*(k-1)//2)
    theta[:k] = rng.uniform(-.15, .15, k)
    qq_tree = {(int(rng.integers(b)), b) for b in range(1, k)}
    cross_support = {(a, (a+offset) % k) for a in range(k) for offset in (1, 2, 5, 7)}
    for a, b, index in pair_locations(k):
        if (a, b) in qq_tree:
            theta[index] = rng.choice((-1, 1))*rng.uniform(.15, .35)
        if (a, b) in cross_support:
            theta[index+1] = rng.choice((-1, 1))*rng.uniform(.2, .5)
        if (b, a) in cross_support:
            theta[index+2] = rng.choice((-1, 1))*rng.uniform(.2, .5)
        theta[index:index+3] += tail/k*rng.uniform(-1, 1, 3)
    return theta, qq_tree, cross_support


def verify_projection_small():
    # Exhaustive check of the two independent support optimizations.
    k = 4
    rng = np.random.default_rng(331)
    theta = rng.normal(size=k+3*k*(k-1)//2)
    budget = 3
    projected = project_conditional_coefficients(k, theta, budget)
    qq = [(a, b, index) for a, b, index in pair_locations(k)]
    best = math.inf
    for mask in itertools.product((0, 1), repeat=len(qq)):
        parent = list(range(k))
        feasible = True
        score = 0.
        for selected, (a, b, index) in zip(mask, qq):
            if not selected:
                score += theta[index]**2
                continue
            def find(v):
                while parent[v] != v:
                    v = parent[v]
                return v
            aa, bb = find(a), find(b)
            if aa == bb:
                feasible = False
                break
            parent[bb] = aa
        if feasible:
            best = min(best, score)
    cross_indices = [index+offset for _, _, index in qq for offset in (1, 2)]
    cross_best = min(sum(theta[i]**2 for i in cross_indices if i not in selected)
                     for selected in itertools.combinations(cross_indices, budget))
    error = float(np.sum((theta-projected)**2))
    assert abs(error-best-cross_best) < 1e-12
    return {"k": k, "cross_budget": budget, "exhaustive_optimal_projection_error": best+cross_best,
            "implemented_projection_error": error}


def run_fixture(k=24, seed=441):
    theta, true_qq, cross_support = make_cyclic_cross_fixture(k, seed)
    experiment = ModuleEnergyExperiment(k, theta, 1.e6, .0002, seed+1)
    conditional, grouped, fitted, acquisition = full_contrast_conditional_regression(
        experiment, k, len(cross_support), seed+2)
    grouped_certificate = statistical_validate_group_action(
        experiment, grouped, .02, module_orbit_pairs, math.sqrt(2)*k,
        candidate_number=1, seed=seed+3, contrast_rounding_radius=1.e-8,
        exact_statistics=True, feature_radius_squared=2*k*k)
    conditional_certificate = statistical_validate_group_action(
        experiment, conditional, .02, module_orbit_pairs, math.sqrt(2)*k,
        candidate_number=2, seed=seed+4, contrast_rounding_radius=1.e-8,
        exact_statistics=True, feature_radius_squared=2*k*k)
    assert not grouped_certificate["accepted"]
    assert conditional_certificate["accepted"]
    residual = float(np.linalg.norm(theta-conditional.coefficient_vector()))
    assert residual <= conditional_certificate["quotient_residual_norm_upper"]
    assert residual <= acquisition["same_data_residual_norm_upper"]
    found_qq = {(a, b) for a, b, _ in conditional.qq_units}
    found_cross = {(a, b) for a, b, _ in conditional.cross_units}
    assert found_qq == true_qq
    assert found_cross == cross_support
    rng = np.random.default_rng(seed+5)
    previous = np.ones(2*k, dtype=np.int8)
    query_results = []
    max_grouped_regret = 0.
    max_conditional_regret = 0.
    for t in range(16):
        context = rng.choice((0, 2), k)
        active = k if t == 0 else 0 if t == 1 else 8
        context[rng.choice(k, active, replace=False)] = 1
        fields = rng.uniform(-.3, .3, 2*k)+.07*previous
        answer, work = conditional.solve_context(context, fields)
        other, _ = grouped.solve_context(context, fields)
        active_count = int(np.sum(context == 1))
        exact_checked = active_count <= 10
        if exact_checked:
            feasible = feasible_orientations(context)
            actual = module_features(feasible)@theta+feasible@fields
            optimum = float(np.min(actual))
            value = float((module_features(answer)@theta).item()+answer@fields)
            other_value = float((module_features(other)@theta).item()+other@fields)
            regret = value-optimum
            grouped_regret = other_value-optimum
            fitted_values = conditional.evaluate(feasible)+feasible@fields
            gap = conditional.evaluate(answer)+answer@fields-float(np.min(fitted_values))
            assert abs(gap) < 1e-10
            bound = (2*math.sqrt(2*active_count*(2*k-active_count))
                     * conditional_certificate["quotient_residual_norm_upper"])
            assert -1e-10 <= regret <= bound+1e-10
            max_conditional_regret = max(max_conditional_regret, regret)
            max_grouped_regret = max(max_grouped_regret, grouped_regret)
        else:
            regret = grouped_regret = None
        query_results.append({"active_modules": active_count,
                              "exact_orientation_enumeration_checked": exact_checked,
                              "conditional_true_regret": regret,
                              "grouped_forest_true_regret": grouped_regret,
                              "actual_executor": work})
        previous = answer
    assert max_grouped_regret > .02*2*k
    return {"modules": k, "sites": 2*k, "possible_contexts": str(3**k),
            "noninvariant_feature_dimension": len(theta),
            "true_qq_tree_edges": len(true_qq),
            "strong_cyclic_cross_coefficients": len(cross_support),
            "dense_noninvariant_tail_added": True, "nuisance_amplitude": 1.e6,
            "full_conventional_acquisition": acquisition,
            "grouped_forest_certificate": grouped_certificate,
            "operation_specific_certificate": conditional_certificate,
            "true_conditional_residual_norm_for_fixture_only": residual,
            "retained_scalar_coefficients": k+len(conditional.qq_units)+len(conditional.cross_units),
            "retained_grid_bits": conditional.grid_bits,
            "adaptive_context_checks": query_results,
            "max_checked_grouped_forest_regret": max_grouped_regret,
            "max_checked_conditional_forest_regret": max_conditional_regret,
            "total_source_cost": experiment.costs()}


def main():
    output = {"status": "conditional interaction projection and exact compiled executor passed",
              "projection_check": verify_projection_small(), "fixture": run_fixture()}
    target = Path(__file__).with_name("conditional_forest_results.json")
    target.write_text(json.dumps(output, indent=2)+"\n")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
