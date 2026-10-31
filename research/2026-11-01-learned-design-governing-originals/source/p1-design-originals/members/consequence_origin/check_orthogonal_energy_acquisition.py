"""Finite checks of the ordinary acquisition implementation.

True coefficients are used only by fixtures and independent scoring, never
passed to acquire_orthogonal_quadratic. This is not a proof of the probability
bound; its exact derivation is in the accompanying ordinary proof note.
"""
from __future__ import annotations

import itertools
import json
from fractions import Fraction
from pathlib import Path
import sys

import numpy as np

from orthogonal_energy_acquisition import (
    acquire_orthogonal_quadratic, quadratic_character_design,
    _configuration_block, _sqrt_upper,
)

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "consequence_mechanism"))
from latent_design import ScalarQuadraticExperiment, compile_acquired, make_fixture, true_energy


def represented_energy(full, X):
    denominator = full["denominator"]
    A = np.asarray(full["A_units"], dtype=float)/denominator
    b = np.asarray(full["b_units"], dtype=float)/denominator
    return (full["constant_units"]/denominator + X@b
            + .5*np.einsum("bi,ij,bj->b", X, A, X))


def run():
    labels_checked = []
    for n in [1, 2, 3, 4, 5, 8, 9, 16, 17, 32, 33, 64, 65, 129, 257]:
        labels, pairs, meta = quadratic_character_design(n)
        assert len(set([0]+labels+[p[2] for p in pairs])) == 1+n+n*(n-1)//2
        labels_checked.append({key: meta[key] for key in
                               ["n", "design_rows", "field_degree", "irreducible_polynomial_bits"]})
    gram_checked = []
    for n in [1, 2, 3, 5, 8, 9, 16]:
        labels, pairs, meta = quadratic_character_design(n)
        X = _configuration_block(labels, 0, meta["design_rows"]).astype(np.int64)
        Phi = np.column_stack([np.ones(len(X), dtype=np.int64)]
                              + [X[:, i] for i in range(n)]
                              + [X[:, i]*X[:, j] for i, j, _ in pairs])
        gram = Phi.T@Phi
        assert np.array_equal(gram, len(X)*np.eye(Phi.shape[1], dtype=np.int64))
        gram_checked.append(n)

    rng = np.random.default_rng(20261031)
    n = 8
    upper = rng.integers(-16, 17, size=(n, n))
    A = (np.triu(upper, 1)+np.triu(upper, 1).T)/8
    b = rng.integers(-8, 9, size=n)/4
    offset = 4096.
    noiseless = ScalarQuadraticExperiment(A, b, offset=offset, sigma=0, seed=1)
    full0, rec0 = acquire_orthogonal_quadratic(noiseless, n, replicates=3,
                                              grid_bits=20, report_rounding_radius=0)
    scale = full0["denominator"]
    assert np.array_equal(np.asarray(full0["b_units"]), b*scale)
    expected = A*scale
    actual = np.asarray(full0["A_units"])
    assert np.array_equal(actual[np.triu_indices(n, 1)], expected[np.triu_indices(n, 1)])
    assert all(sum(row) == 0 for row in full0["A_units"])
    X = np.asarray(list(itertools.product((-1, 1), repeat=n)), dtype=float)
    exact = offset+X@b+.5*np.einsum("bi,ij,bj->b", X, A, X)
    exact_error = float(np.max(np.abs(represented_energy(full0, X)-exact)))
    assert exact_error == 0
    assert rec0["raw_source_reports"] == noiseless.energy_shots
    assert rec0["received_report_bits"] == 64*noiseless.energy_shots

    noisy = ScalarQuadraticExperiment(A, b, offset=offset, sigma=.15, seed=2)
    full1, rec1 = acquire_orthogonal_quadratic(noisy, n, global_failure=.01,
                                              replicates=3, grid_bits=24,
                                              report_rounding_radius=Fraction(1, 10**10))
    uniform_observed_error = float(np.max(np.abs(represented_energy(full1, X)-exact)))
    certified_error = Fraction(rec1["prediction_error_bound"])
    assert uniform_observed_error <= float(certified_error)
    max_observed_regret = 0.
    for _ in range(64):
        field = rng.uniform(-2, 2, n)
        chosen = int(np.argmin(represented_energy(full1, X)+X@field))
        regret = float(exact[chosen]+X[chosen]@field-np.min(exact+X@field))
        max_observed_regret = max(max_observed_regret, regret)
    assert max_observed_regret <= float(Fraction(rec1["source_regret_bound"]))

    # An end-to-end check against the separate acquired-contraction consumer.
    n = 12
    A2, b2, fixture_labels, _, _ = make_fixture(n, 3, 341)
    source = ScalarQuadraticExperiment(A2, b2, sigma=5.e-6, seed=342)
    full2, rec2 = acquire_orthogonal_quadratic(source, n, global_failure=.01,
                                              grid_bits=30,
                                              report_rounding_radius=Fraction(1, 10**9))
    service, compilation = compile_acquired(
        full2, H=Fraction(1, 5), epsilon_per_site=Fraction(1, 50),
        source_regret_bound=Fraction(rec2["source_regret_bound"]),
        confidence_failure=.01)
    assert service is not None, compilation
    X2 = np.asarray(list(itertools.product((-1, 1), repeat=n)), dtype=np.int8)
    field2 = [Fraction(int(v), 1000) for v in rng.integers(-200, 201, size=n)]
    solution = service.solve(field2)
    if isinstance(solution, tuple):
        solution = solution[0]
    solution = np.asarray(solution)
    physical_regret = float(true_energy(A2, b2, solution, field2)
                            - np.min(true_energy(A2, b2, X2, field2)))
    assert physical_regret <= n/50+1.e-10

    # Verify exact outward square-root arithmetic on non-dyadic examples.
    for value in [Fraction(0), Fraction(1, 3), Fraction(2), Fraction(37, 1000),
                  Fraction(10**70+1, 10**21+3)]:
        outward = _sqrt_upper(value)
        assert outward*outward >= value

    return {
        "labels_checked": labels_checked,
        "exact_integer_gram_checked_at_n": gram_checked,
        "noiseless": {"n": 8, "every_configuration_prediction_error": exact_error,
                      "record": rec0},
        "noisy": {"n": 8, "enumerated_configurations": len(X),
                  "observed_uniform_prediction_error": uniform_observed_error,
                  "observed_maximum_regret_over_64_fields": max_observed_regret,
                  "record": rec1},
        "consumer_integration": {"n": n, "source_shots": source.energy_shots,
                                 "physical_regret_on_one_exhaustive_query": physical_regret,
                                 "acquisition": rec2, "compilation": compilation},
    }


if __name__ == "__main__":
    result = run()
    output = HERE / "orthogonal_energy_acquisition_results.json"
    output.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({"result_file": str(output),
                      "noiseless_error": result["noiseless"]["every_configuration_prediction_error"],
                      "noisy_uniform_error": result["noisy"]["observed_uniform_prediction_error"],
                      "noisy_source_regret_bound": result["noisy"]["record"]["source_regret_bound_float_upper"],
                      "consumer_physical_regret": result["consumer_integration"]["physical_regret_on_one_exhaustive_query"]}, indent=2))
