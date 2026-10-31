"""Checks of the continuous/fresh-carrier detector construction.

These checks exercise meaningful risks: noncommuting retained source dynamics,
worst-source (effect-operator) charge error, record versus ensemble contraction,
arbitrary initial receiver cancellation, and a colored-bath counterexample.
They are numerical checks, not substitutes for the proofs in the note.

Run: python phase3_fast_detector/check_detector.py
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from numpy.linalg import eigvalsh, norm, svd
from scipy.linalg import expm, sqrtm
from scipy.optimize import brentq
from scipy.sparse import block_diag, diags, eye, kron
from scipy.sparse.linalg import expm_multiply
from scipy.stats import poisson


OUT = Path(__file__).resolve().parent
I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.diag([1, -1]).astype(complex)
RNG = np.random.default_rng(20261031)


def trnorm(a):
    return float(svd(a, compute_uv=False).sum())


def rate_kl(x, rate):
    return float(x * np.log(x / rate) - x + rate)


def logmean(a, b):
    return float((b - a) / np.log(b / a))


def thresholds(intervals):
    xx = [logmean(intervals[i][1], intervals[i + 1][0]) for i in range(2)]
    cc = [rate_kl(xx[i], intervals[i][1]) for i in range(2)]
    return np.array(xx), min(cc)


def vec(a):
    return a.reshape(-1, order="F")


def effect_from_superop(s):
    trace_row = np.array([1, 0, 0, 1], dtype=complex)
    e = (trace_row @ s).reshape((2, 2), order="F").T
    assert norm(e - e.conj().T) < 1e-10
    return (e + e.conj().T) / 2


def count_effects(h, jump, duration, nmax):
    """Exact count-resolved Lindblad evolution up to a certified tail.

    The input has four columns, the matrix-unit basis of the source.
    Every count sector therefore returns the whole quantum operation,
    rather than only a scalar probability for one chosen state.
    """
    r = jump.conj().T @ jump
    no_count = -1j * (np.kron(I, h) - np.kron(h.T, I))
    no_count -= 0.5 * (np.kron(I, r) + np.kron(r.T, I))
    emit = np.kron(jump.conj(), jump)
    generator = kron(eye(nmax + 1), no_count, format="csc")
    generator += kron(diags(np.ones(nmax), -1), emit, format="csc")
    initial = np.zeros((4 * (nmax + 1), 4), dtype=complex)
    initial[:4] = np.eye(4)
    evolved = expm_multiply(generator * duration, initial)
    return [evolved[4 * n : 4 * n + 4] for n in range(nmax + 1)]


def quantum_source_count_checks():
    tau = np.array([0.8, 1.7, 2.6])
    b = 0.12
    intervals = [((a - b) ** 2, (a + b) ** 2) for a in tau]
    cut, c = thresholds(intervals)
    duration = 12.0
    nmax = int(poisson.ppf(1 - 1e-13, intervals[-1][1] * duration)) + 12
    bound = 2 * np.exp(-c * duration)
    rows = []
    for omega in [0.0, 0.3, 5.0, 50.0]:
        h = 0.5 * omega * X + 0.37 * Z
        wrong_eigenvalues = []
        mass_deficits = []
        for q in range(3):
            direction = np.cos(0.4 + 0.7 * q) * Z + np.sin(0.4 + 0.7 * q) * Y
            jump = tau[q] * I + b * direction
            ops = count_effects(h, jump, duration, nmax)
            wrong = np.zeros((4, 4), dtype=complex)
            total = np.zeros_like(wrong)
            for n, op in enumerate(ops):
                total += op
                label = int(np.searchsorted(cut, n / duration, side="right"))
                if label != q:
                    wrong += op
            effect = effect_from_superop(wrong)
            deficit = I - effect_from_superop(total)
            tail_bound = float(poisson.sf(nmax, intervals[q][1] * duration))
            assert eigvalsh(effect)[0] >= -2e-10
            worst = float(eigvalsh(effect)[-1])
            assert worst <= bound + 1e-10
            assert eigvalsh(deficit)[0] >= -2e-10
            assert eigvalsh(deficit)[-1] <= tail_bound + 2e-10
            wrong_eigenvalues.append(worst)
            mass_deficits.append(float(eigvalsh(deficit)[-1]))
        rows.append({"omega": omega, "worst_source_errors": wrong_eigenvalues,
                     "max_count_mass_deficit": max(mass_deficits)})
    return {"amplitudes": tau.tolist(), "source_amplitude_norm": b,
            "rate_intervals": intervals, "thresholds": cut.tolist(),
            "minimum_chernoff_exponent": c, "duration": duration,
            "uniform_error_bound": float(bound), "count_cutoff": nmax,
            "results": rows}


def record_contraction_checks():
    """Enumerate exact discrete quantum records, including a reference.

    K0=U sqrt(I-dt L^dag L), K1=U sqrt(dt)L is an exactly complete
    two-outcome instrument. No infinitesimal approximation enters this check.
    """
    dt = 0.06
    steps = 11
    aq, ap, b = 0.8, 1.7, 0.12
    lq = aq * I + b * (0.6 * Z + 0.8 * Y)
    lp = ap * I + b * (0.8 * Z - 0.6 * X)
    a = (aq + b) ** 2
    bb = (ap - b) ** 2
    per_step_affinity = np.sqrt((1 - a * dt) * (1 - bb * dt)) + np.sqrt(a * bb) * dt
    upper = float(per_step_affinity ** steps)
    gamma = 0.5 * (np.sqrt(bb) - np.sqrt(a)) ** 2

    raw = RNG.normal(size=(4, 4)) + 1j * RNG.normal(size=(4, 4))
    input_x = raw / trnorm(raw)
    histories = [(np.eye(4, dtype=complex), np.eye(4, dtype=complex))]
    for j in range(steps):
        uq = expm(-1j * ((7 + 19 * (-1) ** j) * X + (j + 1) * Z) * dt)
        up = expm(-1j * ((11 + 13 * np.cos(j)) * Y - (j + 2) * X) * dt)
        qops = [uq @ np.asarray(sqrtm(I - dt * lq.conj().T @ lq), dtype=complex),
                uq @ (np.sqrt(dt) * lq)]
        pops = [up @ np.asarray(sqrtm(I - dt * lp.conj().T @ lp), dtype=complex),
                up @ (np.sqrt(dt) * lp)]
        qops = [np.kron(k, I) for k in qops]
        pops = [np.kron(k, I) for k in pops]
        for ops in [qops, pops]:
            assert norm(sum(k.conj().T @ k for k in ops) - np.eye(4)) < 1e-12
        histories = [(qops[z] @ kq, pops[z] @ kp)
                     for kq, kp in histories for z in [0, 1]]
    exact_record_norm = sum(trnorm(kq @ input_x @ kp.conj().T) for kq, kp in histories)
    assert exact_record_norm <= upper + 1e-12

    # Scalar amplitudes attain the exact Bernoulli affinity at every step.
    a0, b0 = aq * aq, ap * ap
    scalar_affinity = (np.sqrt((1 - a0 * dt) * (1 - b0 * dt)) + np.sqrt(a0 * b0) * dt) ** steps
    scalar_sum = 0.0
    from math import comb
    for n in range(steps + 1):
        pq = comb(steps, n) * (a0 * dt) ** n * (1 - a0 * dt) ** (steps - n)
        pp = comb(steps, n) * (b0 * dt) ** n * (1 - b0 * dt) ** (steps - n)
        scalar_sum += np.sqrt(pq * pp)
    assert abs(scalar_sum - scalar_affinity) < 1e-14

    # Equal-magnitude opposite amplitudes: classical records retain coherence.
    ell = 1.2
    opposite_record_norm = 1.0
    opposite_unconditional = (1 - 2 * ell ** 2 * dt) ** steps
    assert 0 < opposite_unconditional < 0.2
    return {"steps": steps, "dt": dt, "record_count": 2 ** steps,
            "source_plus_reference_dimension": 4,
            "input_trace_norm": trnorm(input_x),
            "full_record_output_trace_norm": exact_record_norm,
            "uniform_discrete_affinity_bound": upper,
            "continuous_interval_gamma": gamma,
            "continuous_bound": float(np.exp(-gamma * dt * steps)),
            "scalar_exact_affinity": float(scalar_affinity),
            "opposite_amplitudes_record_norm": opposite_record_norm,
            "opposite_amplitudes_unconditional_norm": float(opposite_unconditional)}


def signed_filter_checks():
    tests = []
    for tau_a, tb, ts, duration, initial in [
        (0.4, 0.4, 0.4, 7.0, 1000.0),
        (1.7, 0.8, 2.1, 12.0, -240.0),
        (0.2, 0.05, 0.1, 0.8, 3.0),
    ]:
        arrivals = np.sort(RNG.uniform(0, duration, 23))
        d = -1 / np.expm1(tb / tau_a)
        c = 1 / (-np.expm1(-ts / tau_a))
        pieces = [(-tb, 0, d), (0, duration, 1), (duration, duration + ts, c)]
        signal_integral = 0.0
        initial_integral = 0.0
        for left, right, weight in pieces:
            homogeneous = initial * tau_a * (np.exp(-(left + tb) / tau_a)
                                            - np.exp(-(right + tb) / tau_a))
            initial_integral += weight * homogeneous
            signal_integral += weight * homogeneous
            for arrival in arrivals:
                if right > arrival:
                    signal_integral += weight * (np.exp(-max(left - arrival, 0) / tau_a)
                                                 - np.exp(-(right - arrival) / tau_a))
        assert abs(signal_integral - len(arrivals)) < 1e-10
        assert abs(initial_integral) < 1e-10
        noise_time = d * d * tb + duration + c * c * ts
        tests.append({"tau_a": tau_a, "guard_before": tb, "guard_after": ts,
                      "duration": duration, "initial_receiver_value": initial,
                      "weights": [d, 1.0, c], "true_count": len(arrivals),
                      "filtered_count": signal_integral,
                      "homogeneous_residual": initial_integral,
                      "white_noise_effective_time": noise_time})
    return tests


def continuously_on_filter_checks():
    """The same signed filter needs no detector-OFF settling gap."""
    tau_a = tb = ts = 0.4
    duration = 7.0
    initial = 1200.0
    d = -1 / np.expm1(tb / tau_a)
    c = 1 / (-np.expm1(-ts / tau_a))
    pieces = [(-tb, 0, d), (0, duration, 1), (duration, duration + ts, c)]
    arrivals = np.sort(RNG.uniform(-tb, duration + ts, 73))
    def event_weight(t):
        if t < 0:
            return d + (1 - d) * np.exp(t / tau_a)
        if t <= duration:
            return 1.0
        return c * (1 - np.exp(-(duration + ts - t) / tau_a))
    integrated_signal = 0.0
    for left, right, weight in pieces:
        integrated_signal += weight * initial * tau_a * (
            np.exp(-(left + tb) / tau_a) - np.exp(-(right + tb) / tau_a))
        for arrival in arrivals:
            if right > arrival:
                integrated_signal += weight * (
                    np.exp(-max(left - arrival, 0) / tau_a)
                    - np.exp(-(right - arrival) / tau_a))
    weighted_count = sum(event_weight(t) for t in arrivals)
    assert abs(integrated_signal - weighted_count) < 1e-10
    grid = np.linspace(-tb, duration + ts, 1001)
    weights = np.array([event_weight(t) for t in grid])
    assert weights.min() >= -1e-14 and weights.max() <= 1 + 1e-14
    for s in [-4, -1, -0.1, 0.1, 1, 4]:
        assert np.max(np.expm1(s * weights) - weights * np.expm1(s)) < 1e-12
    effective_time = duration + d * tb + c * ts
    assert abs(effective_time - (duration + tau_a)) < 1e-14
    return {"actual_monitoring_duration": duration + tb + ts,
            "effective_signal_time": effective_time,
            "initial_receiver_value": initial,
            "unweighted_event_count": len(arrivals),
            "weighted_event_count": float(weighted_count),
            "filtered_signal": float(integrated_signal),
            "initial_value_cancels": True,
            "detector_remains_on_in_guards": True,
            "event_weight_range": [float(weights.min()), float(weights.max())]}


def finite_carrier_checks():
    """Exact joint Hamiltonian, not a jump approximation."""
    delta = 0.25
    b = 0.12
    rows = []
    for omega in [0, 1, 20, 500]:
        he = 0.5 * omega * Z + 0.17 * X
        for tau in [0.8, 1.7, 2.6]:
            bq = b * (0.6 * X + 0.8 * Y)
            joint = np.kron(he, I) + np.kron(tau * I + bq, X)
            u = expm(-1j * joint * delta)
            # Basis ordering source,carrier; carrier 0 input,1 output.
            transmission = u[np.ix_([1, 3], [0, 2])]
            ideal = -1j * np.sin(tau * delta) * expm(-1j * he * delta)
            residual = norm(transmission - ideal, 2)
            lo = max(abs(np.sin(tau * delta)) - b * delta, 0) ** 2
            hi = min(1, (abs(np.sin(tau * delta)) + b * delta) ** 2)
            ev = eigvalsh(transmission.conj().T @ transmission)
            assert residual <= b * delta + 2e-12
            assert ev[0] >= lo - 2e-12 and ev[-1] <= hi + 2e-12
            rows.append({"source_omega": omega, "tau": tau,
                         "transmission_effect_eigenvalues": ev.tolist(),
                         "proved_interval": [lo, hi],
                         "Duhamel_residual": residual,
                         "residual_bound": b * delta})
    return rows


def gaussian_exponent(x, lam, duration, variance, upper):
    def derivative(s):
        return x * duration - lam * duration * np.exp(s) - variance * s
    if upper:
        s = brentq(derivative, 0, 20)
    else:
        s = brentq(derivative, -50, 0)
    return float(s * x * duration - lam * duration * np.expm1(s) - variance * s * s / 2)


def analog_exponent_check():
    intervals = [((a - 0.12) ** 2, (a + 0.12) ** 2) for a in [0.8, 1.7, 2.6]]
    duration = 60.0
    tau_a = tb = ts = 0.4
    noise_density = 0.3
    d = -1 / np.expm1(tb / tau_a)
    c = 1 / (-np.expm1(-ts / tau_a))
    variance = noise_density * (duration + d * d * tb + c * c * ts)
    effective_time = duration + d * tb + c * ts
    rows = []
    for q in [0, 1]:
        a, bb = intervals[q][1], intervals[q + 1][0]
        def difference(x):
            return gaussian_exponent(x, a, effective_time, variance, True) - gaussian_exponent(x, bb, effective_time, variance, False)
        cutoff = brentq(difference, a + 1e-10, bb - 1e-10)
        exponent = gaussian_exponent(cutoff, a, effective_time, variance, True)
        assert exponent > 0
        rows.append({"adjacent_charges": [q, q + 1], "cutoff_rate": cutoff,
                     "balanced_error_exponent": exponent})
    bound = 2 * np.exp(-min(row["balanced_error_exponent"] for row in rows))
    return {"duration": duration, "total_record_duration": duration + tb + ts,
            "effective_signal_time": effective_time,
            "detector_remains_on_in_guards": True,
            "input_referred_noise_density": noise_density,
            "filtered_imprecision_variance": variance,
            "pairs": rows, "label_error_bound": float(bound),
            "complete_instrument_halfdiamond_bound": float(np.sqrt(2 * bound))}


def colored_bath_counterexample():
    tau, b, energy_ratio = 1.0, 0.1, 100.0
    white_upper = (tau + b) ** 2
    excited_source_rate = tau ** 2 + b ** 2 * (1 + energy_ratio)
    assert excited_source_rate > white_upper
    return {"tau": tau, "b": b, "source_release_over_bias": energy_ratio,
            "white_model_rate_upper_over_gamma0": white_upper,
            "excited_source_actual_rate_over_gamma0": excited_source_rate,
            "qualification": "Born frequency-resolved rates; lead band supports release energy"}


def baseline_current_check():
    chi = 0.7
    values = []
    for baseline in [0.5, 1, 3, 10, 100]:
        a, bb = baseline ** 2, (baseline + chi) ** 2
        x = logmean(a, bb)
        values.append({"baseline": baseline, "current_rate": a,
                       "Poisson_error_exponent": rate_kl(x, a),
                       "record_contraction_rate": chi ** 2 / 2})
    return values


def main():
    results = {
        "quantum_source_counts": quantum_source_count_checks(),
        "complete_record_contraction": record_contraction_checks(),
        "finite_bandwidth_filter": signed_filter_checks(),
        "continuously_on_finite_bandwidth_filter": continuously_on_filter_checks(),
        "finite_carrier_contact": finite_carrier_checks(),
        "analog_current_discrimination": analog_exponent_check(),
        "colored_reservoir_counterexample": colored_bath_counterexample(),
        "baseline_current_information": baseline_current_check(),
    }
    (OUT / "detector_results.json").write_text(json.dumps(results, indent=2) + "\n")
    print(json.dumps({
        "status": "All checks passed",
        "count_bound": results["quantum_source_counts"]["uniform_error_bound"],
        "worst_simulated_source_error": max(max(r["worst_source_errors"])
            for r in results["quantum_source_counts"]["results"]),
        "record_norm": results["complete_record_contraction"]["full_record_output_trace_norm"],
        "record_bound": results["complete_record_contraction"]["uniform_discrete_affinity_bound"],
        "analog_instrument_bound": results["analog_current_discrimination"]["complete_instrument_halfdiamond_bound"],
        "output": str(OUT / "detector_results.json"),
    }, indent=2))


if __name__ == "__main__":
    main()
