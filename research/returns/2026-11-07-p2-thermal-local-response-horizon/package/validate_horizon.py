"""Exact finite construction checks plus separately labeled floating diagnostics.

The proofs in REPORT.md are the universal argument. Finite checks do not
establish a worst-case theorem, obtain physical data, or execute huge budgets.
"""
from fractions import Fraction as Q
from pathlib import Path
from time import perf_counter
import json
import math
import thermal_horizon as th

ROOT = Path(__file__).resolve().parent
checks = 0


def require(claim):
    global checks
    checks += 1
    if not claim:
        raise AssertionError(f"exact check {checks} failed")


def max_bits(rationals):
    return max(max(abs(q.numerator).bit_length(), q.denominator.bit_length())
               for q in rationals)


def check_model(n, beta=Q(1), omega=Q(1), background="binomial"):
    start = perf_counter()
    model = th.construct_pair(n, beta, omega, background)
    atoms = model["atoms"]
    target_poly = [Q(1)]
    for x in atoms:
        target_poly = th.polynomial_mul_linear(target_poly, x)
    require(omega / 2 < min(atoms) and max(atoms) == omega)
    require(model["query_time_error_bound"] <= model["gamma0"] / (16 * omega))
    for x, r, (lo, hi) in zip(atoms, model["exponentials"], model["exponential_enclosures"]):
        require(0 <= lo <= hi <= 1)
        require(max(abs(r - lo), abs(r - hi)) <= Q(1, 1 << model["precision_bits"]))
        require(Q(1, 1 << model["precision_bits"]) <= model["xi"])
    for chain in model["pair"]:
        weights = chain["weights"]
        require(sum(weights) == 1 and min(weights) > 0)
        if background == "uniform":
            require(min(weights) >= Q(1, 4 * (n + 1)))
        require(th.characteristic_polynomial(chain) == target_poly)
        moment_count = 2 * n + 5
        direct = [sum(w * x ** k for w, x in zip(weights, atoms))
                  for k in range(moment_count)]
        for actual, expected in zip(th.endpoint_moments(chain, moment_count), direct):
            require(actual == expected)
        for d in chain["diagonal"]:
            require(min(atoms) <= d <= max(atoms))
        for i, b2 in enumerate(chain["squared_hoppings"], 1):
            if background == "binomial":
                base_b2 = model["h"] ** 2 * i * (n + 1 - i) / 4
                require(b2 >= base_b2 / 6)
                require(b2 >= omega ** 2 / (225 * n))
            else:
                require(b2 >= model["h"] ** 2 / (36 * (n + 1)))
            require(b2 <= omega ** 2 / 16)
    bits = model["precision_bits"] + 30
    gap_intervals = [th.response_at_alignment_interval(model, i, bits) for i in range(2)]
    a, b = gap_intervals
    gap_lower = max(a[0] - b[1], b[0] - a[1])
    gap_at_binary_time_lower = gap_lower - 2 * omega * model["query_time_error_bound"]
    require(gap_lower >= 15 * model["gamma0"] / 16)
    require(gap_at_binary_time_lower >= model["gamma0"] / 2)
    # These are finite sampled checks, not the proof of the ALL-time bound.
    largest_checked_difference = Q(0)
    for tau in [beta * Q(j, 8) for j in range(9)]:
        intervals = [th.correlator_interval(atoms, p["weights"], tau, beta, bits)
                     for p in model["pair"]]
        a, b = intervals
        difference_upper = max(abs(a[0] - b[1]), abs(a[1] - b[0]))
        require(difference_upper <= 2 * model["delta"])
        largest_checked_difference = max(largest_checked_difference, difference_upper)
    data = {
        "n": n, "sites": n + 1, "background": background,
        "beta": str(beta), "omega": str(omega),
        "thermal_weight_bits": model["precision_bits"],
        "maximum_coefficient_numerator_or_denominator_bits": max(
            max_bits(p["diagonal"] + p["squared_hoppings"]) for p in model["pair"]),
        "rational_query_time": str(model["rational_query_time"]),
        "time_approximate_for_display_only": float(model["rational_query_time"]),
        "all_tau_pair_difference_proved_upper": str(2 * model["delta"]),
        "gap_at_binary_time_certified_lower": str(gap_at_binary_time_lower),
        "gap_lower_decimal_for_display_only": float(gap_at_binary_time_lower),
        "gaussian_read_lower_bound_variance_one_confidence_two_thirds":
            str(Q(1, 9) / model["delta"] ** 2),
        "log10_read_lower_bound_for_display_only":
            -math.log10(9) - 2 * math.log10(float(model["delta"])),
        "nine_point_interval_check_maximum": str(largest_checked_difference),
        "elapsed_seconds": perf_counter() - start,
    }
    return model, data


def check_full_spin_trace(model):
    """Independent finite-temperature full Hilbert-space floating diagnostic."""
    import numpy as np
    size = model["sites"]
    dimension = 1 << size
    beta = float(model["beta"])
    atoms = np.array(list(map(float, model["atoms"])))
    largest_error = 0.0
    spectra = []
    for chain in model["pair"]:
        d = list(map(float, chain["diagonal"]))
        b = [math.sqrt(float(q)) for q in chain["squared_hoppings"]]
        H = np.zeros((dimension, dimension))
        A = np.zeros_like(H)
        for state in range(dimension):
            H[state, state] = sum(d[i] for i in range(size) if state >> i & 1)
            A[state, state ^ 1] = 1
            for i in range(size - 1):
                if ((state >> i) ^ (state >> (i + 1))) & 1:
                    H[state, state ^ (3 << i)] = b[i]
        eigenvalues, eigenvectors = np.linalg.eigh(H)
        spectra.append(eigenvalues)
        A_eigen = eigenvectors.T @ A @ eigenvectors
        transition_weights = A_eigen * A_eigen
        Z = np.exp(-beta * eigenvalues).sum()
        weights = np.array(list(map(float, chain["weights"])))
        expected_spectrum = sorted(sum(atoms[i] for i in range(size) if state >> i & 1)
                                   for state in range(dimension))
        largest_error = max(largest_error, float(np.max(np.abs(eigenvalues - expected_spectrum))))
        for tau in [0.0, beta / 7, beta / 2, beta]:
            direct = (np.exp(-(beta - tau) * eigenvalues[:, None]
                             - tau * eigenvalues[None, :]) * transition_weights).sum() / Z
            spectral = np.sum(weights * (np.exp(-tau * atoms) + np.exp(-(beta - tau) * atoms))
                              / (1 + np.exp(-beta * atoms)))
            largest_error = max(largest_error, abs(float(direct - spectral)))
        for time in [0.3, 2.0, float(model["rational_query_time"])]:
            direct = (np.exp(-beta * eigenvalues[:, None]
                             + 1j * time * (eigenvalues[:, None] - eigenvalues[None, :]))
                      * transition_weights).sum() / Z
            spectral = np.sum(weights * np.tanh(beta * atoms / 2) * np.sin(time * atoms))
            largest_error = max(largest_error, abs(float(-direct.imag - spectral)))
    largest_error = max(largest_error, float(np.max(np.abs(spectra[0] - spectra[1]))))
    if largest_error >= 1e-11:
        raise AssertionError("floating full-spin trace diagnostic failed")
    return {"sites": size, "hilbert_dimension": dimension,
            "largest_absolute_error": largest_error,
            "status": "floating diagnostic; not an interval proof"}


def check_recovery():
    def sine_interval(x, bits=120):
        if x < 0:
            lo, hi = sine_interval(-x, bits)
            return -hi, -lo
        total, term, k = Q(0), Q(x), 0
        while True:
            total += (-1) ** k * term
            ratio = x * x / ((2 * k + 2) * (2 * k + 3))
            following = term * ratio
            if ratio <= 1 and following <= Q(1, 1 << bits):
                other = total + (-1) ** (k + 1) * following
                return min(total, other), max(total, other)
            term, k = following, k + 1
    results = []
    for T in [Q(1, 2), Q(2), Q(5)]:
        schedule = th.acquisition_schedule(T, Q(1, 64), Q(1, 20))
        require(schedule["uniform_error_certificate"] <= Q(1, 128))
        require(schedule["maximum_setting_error"] == schedule["node_error_budget"] / 4)
        model = th.construct_pair(3)
        chain = model["pair"][0]
        precision = th.ceil_log2(64 / schedule["node_error_budget"])
        intervals = [th.correlator_interval(model["atoms"], chain["weights"], tau, bits=precision)
                     for tau in schedule["nodes"]]
        # Synthetic deterministic data: bounded deliberate errors; no acquired
        # Gaussian data and no huge sample budget is claimed to have been run.
        estimates = []
        for j, (lo, hi) in enumerate(intervals):
            datum = (lo + hi) / 2 + (-1) ** j * schedule["node_error_budget"] / 2
            require(max(abs(datum - lo), abs(datum - hi)) <= schedule["node_error_budget"])
            estimates.append(datum)
        record = th.compile_response_record(schedule, estimates)
        tanh_intervals = []
        for x in model["atoms"]:
            lo, hi = th.exp_negative_interval(x, 120)
            tanh_intervals.append(((1 - hi) / (1 + hi), (1 - lo) / (1 + lo)))
        worst_upper = Q(0)
        for j in range(101):
            t = T * j / 100
            truth_lo, truth_hi = Q(0), Q(0)
            for x, w, (a, b) in zip(model["atoms"], chain["weights"], tanh_intervals):
                c, d = sine_interval(x * t)
                products = [a * c, a * d, b * c, b * d]
                truth_lo += w * min(products)
                truth_hi += w * max(products)
            estimate = th.evaluate_record(record, t)
            error_upper = max(abs(estimate - truth_lo), abs(estimate - truth_hi))
            worst_upper = max(worst_upper, error_upper)
            require(error_upper <= schedule["uniform_error_certificate"])
        results.append({"horizon": str(T), "degree": schedule["degree"],
                        "quantization_bits": schedule["quantization_bits"],
                        "total_raw_reads_required_not_executed": str(schedule["total_raw_reads"]),
                        "uniform_proved_certificate": str(schedule["uniform_error_certificate"]),
                        "101_point_rational_interval_maximum_error_bound": str(worst_upper),
                        "maximum_error_decimal_for_display_only": float(worst_upper),
                        "data_status": "synthetic deterministic bounded-error data"})
    # Execute the read/average/compile path at a separately tiny variance so
    # that its actual finite budget fits a small, explicitly synthetic test.
    schedule = th.acquisition_schedule(Q(1, 100), Q(1, 4), Q(1, 4), variance=Q(1, 10**80))
    require(schedule["repeats_per_node"] == 1)
    record = th.consume_quantized_readings(schedule, [Q(1)] * schedule["total_raw_reads"])
    require(th.evaluate_record(record, Q(0)) == 0)
    return results


def main():
    start = perf_counter()
    models, rows = [], []
    for n in [1, 2, 4, 8, 12, 16]:
        model, row = check_model(n)
        models.append(model)
        rows.append(row)
        print(f"exact construction n={n}, coefficient bits={row['maximum_coefficient_numerator_or_denominator_bits']}", flush=True)
    for n, beta, omega in [(3, Q(1, 8), Q(1)), (3, Q(3), Q(2)), (3, Q(16), Q(1, 2))]:
        _, row = check_model(n, beta, omega)
        rows.append(row)
    uniform_models = []
    for n in [1, 3, 7, 15]:
        model, row = check_model(n, background="uniform")
        uniform_models.append(model)
        rows.append(row)
        print(f"uniform-background construction n={n}, coefficient bits={row['maximum_coefficient_numerator_or_denominator_bits']}", flush=True)
    full_trace = [check_full_spin_trace(m) for m in models[:3]]
    full_trace.append(check_full_spin_trace(uniform_models[1]))
    recovery = check_recovery()
    output = {"exact_rational_assertions": checks, "finite_models": rows,
              "full_spin_diagnostics": full_trace, "recovery_diagnostics": recovery,
              "elapsed_seconds": perf_counter() - start,
              "scope": "Finite checks support implementation; universal proof is in REPORT.md. No physical measurements or enormous Gaussian acquisition schedules executed."}
    (ROOT / 'VALIDATION.json').write_text(json.dumps(output, indent=2) + '\n')
    (ROOT / 'EXPLICIT_PAIR_n8.json').write_text(json.dumps(th.rational_json(models[3]), indent=2) + '\n')
    (ROOT / 'EXPLICIT_PAIR_n7_uniform.json').write_text(json.dumps(th.rational_json(uniform_models[2]), indent=2) + '\n')
    print(json.dumps({"assertions": checks, "elapsed_seconds": output["elapsed_seconds"],
                      "full_spin_errors": [r["largest_absolute_error"] for r in full_trace]}))


if __name__ == '__main__':
    main()
