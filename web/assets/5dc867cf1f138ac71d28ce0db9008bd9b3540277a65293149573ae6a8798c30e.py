"""Bounded exact-positive acquisition/tilt check for the N-call refinement."""
from fractions import Fraction as F
import json
import time
import signal
from pathlib import Path
import numpy as np
import axial_acquisition as a
from check_axial_acquisition import hierarchy_expectation, target_numpy, CountedRandom


def main():
    def wall_limit(signum, frame):
        raise TimeoutError("owned bounded fixture exceeded the declared20second wall cap")
    signal.signal(signal.SIGALRM, wall_limit)
    signal.alarm(20)
    started = time.perf_counter()
    assertions = 0
    def check(value):
        nonlocal assertions
        assertions += 1
        assert value
    records = []
    delivered = []
    for N, alpha, delta, h in [(2, F(1, 2), F(1), F(1, 3)),
                               (3, F(1, 3), F(1), F(-1, 2)),
                               (3, F(1), F(1, 2), F(1, 3))]:
        eps = F(1, 8)
        Hcap = abs(h) + delta
        B = a.ceil_fraction(2 * N * Hcap)
        eta = eps / (1 << (B + 10))
        w, metadata = a.acquire_k_weights(N, alpha, delta, h, eps,
                                          lp_backend=a.exact_simplex_fixture)
        branches, branch_data = a.acquire_branches(N, delta, h, w, eps)
        base = {}
        base_nodes = 0
        for k in range(1, N + 1):
            p, acquisition = a.acquire_zero_field_probabilities(N, k, delta, eta)
            mixture, fixture = a.symmetric_octahedron_fixture(k, p, eta / 2)
            check(fixture["population_L1_error_before_rounding"] == 0)
            check(fixture["optimization_executed"] is False)
            check(fixture["rounding_TV"] <= eta / 16)
            check(acquisition["acquisition_TV_bound"] <= eta / 16)
            check(sum(v[0] for v in mixture) == 1)
            base[k] = mixture
            base_nodes += len(mixture)
        inner = {}
        filtered_nodes = 0
        for branch in branches:
            k, u, m = branch["k"], branch["u"], branch["m"]
            if not k:
                continue
            hprime = h - 2 * delta * m / N
            check(abs(hprime) <= Hcap)
            mixture, tilt = a.tilt_iid_mixture(N, k, hprime, Hcap, base[k], eps)
            check(tilt["B"] == B and tilt["eta"] == eta)
            check(tilt["weight_rounding_TV"] <= eps / 128)
            check(sum(v[0] for v in mixture) == 1)
            D0, D1 = tilt["exact_rational_filter"]
            check(D0 > 0 and D1 > 0)
            check(min(D0, D1) ** (2 * k) >= F(1, 4 * (1 << B)))
            for weight, state in mixture:
                check(weight >= 0 and a.qubit_state_is_psd(state))
                d0, d1, re, im = state
                check(d0 * d1 == re * re + im * im)  # fixture atoms are pure
            inner[(k, u)] = mixture
            filtered_nodes += len(mixture)
        expected = hierarchy_expectation(N, branches, inner)
        target = target_numpy(N, alpha, delta, h)
        error = float(np.abs(np.linalg.eigvalsh(expected - target)).sum() / 2)
        check(error < float(eps / 8))
        check(abs(np.trace(expected) - 1) < 1e-12)
        rng = CountedRandom(17003 + N)
        maximum_bits = 0
        for trial in range(64):
            before = rng.bits
            local, label = a.sample_hierarchy(N, branches, inner, eps, rng)
            check(len(local) == N and all(a.qubit_state_is_psd(s) for s in local))
            maximum_bits = max(maximum_bits, rng.bits - before)
        delivered.append({"N": N, "alpha": str(alpha), "delta": str(delta),
                          "h": str(h), "eps": str(eps),
                          "rational_K_weights": [str(v) for v in w],
                          "outer_types": [{"k": b["k"], "u": b["u"],
                                            "dyadic_probability": str(b["probability"])}
                                           for b in branches],
                          "rational_inner_mixtures": {
                              str((k, u)): [{"dyadic_weight": str(weight),
                                             "qubit_matrix_d0_d1_re_im": list(map(str, state))}
                                            for weight, state in mixture]
                              for (k, u), mixture in inner.items()},
                          "sampled_last_label": {key: list(val) if isinstance(val, tuple) else val
                                                 for key, val in label.items()},
                          "sampled_rational_local_states": [list(map(str, state)) for state in local]})
        records.append({"N": N, "alpha": str(alpha), "delta": str(delta),
                        "h": str(h), "zero_field_acquisition_calls": N,
                        "nonempty_type_count": len(inner), "base_nodes": base_nodes,
                        "filtered_branch_nodes": filtered_nodes,
                        "base_error_budget_eta": str(eta),
                        "numeric_uniform_subset_trace_error": error,
                        "finite_bit_draws": 64,
                        "maximum_observed_fair_bits_per_draw": maximum_bits})
    result = {"status": "PASS", "assertions": assertions,
              "elapsed_seconds_shared_machine": time.perf_counter() - started,
              "records": records,
              "evidence_scope": "bounded exact-positive six-node zero-field witness and rational tilt; trace errors numerical; generic certified Turing iid backend not executed",
              "hardware_preparation": "NOT_EXECUTED", "novelty_priority": "UNKNOWN"}
    signal.alarm(0)
    Path(__file__).with_name("reusable_tilt_checks.json").write_text(json.dumps(result, indent=2) + "\n")
    Path(__file__).with_name("bounded_reusable_mixtures.json").write_text(json.dumps({
        "status": "ACQUIRED_BOUNDED_EXAMPLES", "basis": "0 down,1 up",
        "qubit_encoding": "matrix [[d0,re+i im],[re-i im,d1]]",
        "uniform_subset_and_complement": "bounded rank floor(M U/2^b),2^b>=128M/eps",
        "certification_scope": "exact local PSD/simplex/tilt; uniform-subset whole trace errors numerical in reusable_tilt_checks.json",
        "cases": delivered}, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
