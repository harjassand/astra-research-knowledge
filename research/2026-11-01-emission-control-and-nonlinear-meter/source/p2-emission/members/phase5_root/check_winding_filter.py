"""Balanced physical counterrotation: spectrum, actuator excursion, action bound.

This is a linearized six-mode calculation, not a complete noisy cat channel.
The complementary cross-Gaussian program handles joint readout/backaction.
No physical noise is removed by a software frame change.
"""
from pathlib import Path
import itertools
import json
import numpy as np
from scipy.linalg import expm

G, gamma, n, nu = 1.0, 10.0, 8.0, 0.2
alpha = np.sqrt(n)
kc = 2 * G * G / gamma
h = nu * G * G / gamma
F = h * alpha
K = np.ones((3, 3)) - np.eye(3)
I3 = np.eye(3)
Pc = np.ones((3, 3)) / 3
Pd = I3 - Pc
m = np.array([1.0, 2.0, -3.0])


def all_port_power(force, cycle, parity):
    """Force has c-dot=-i force; keeps conjugate source and dark modes."""
    nf = len(force)
    fw = np.fft.fft(force, axis=0) / nf
    fcw = np.fft.fft(force.conj(), axis=0) / nf
    w = 2 * np.pi * np.fft.fftfreq(nf, d=cycle / nf)
    s = 1j * w
    D = s * (s + gamma / 2) + G * G
    bw = np.zeros_like(fw)
    for proj, delta in ((Pc, 2 * h * parity), (Pd, -h * parity)):
        numerator = D[:, None] * (fw @ proj) + (
            1j * delta * (s + gamma / 2)[:, None] * (fcw @ proj)
        )
        denominator = D * D - delta * delta * (s + gamma / 2) ** 2
        bw += -G * numerator / denominator[:, None]
    return float(np.sum(np.abs(bw) ** 2))


def affine_drift(deterr, parity):
    A = np.zeros((13, 13), complex)
    A[:3, :3] = -1j * np.diag(deterr)
    A[3:6, 3:6] = 1j * np.diag(deterr)
    A[:3, 3:6] = -1j * h * parity * K
    A[3:6, :3] = 1j * h * parity * K
    A[:3, 6:9] = -1j * G * I3
    A[3:6, 9:12] = 1j * G * I3
    A[6:9, :3] = -1j * G * I3
    A[9:12, 3:6] = 1j * G * I3
    A[6:9, 6:9] = -gamma / 2 * I3
    A[9:12, 9:12] = -gamma / 2 * I3
    A[:3, 12] = -1j * (F * parity + alpha * deterr)
    A[3:6, 12] = 1j * (F * parity + alpha * deterr)
    return A


def gauge_excursion(ratio, eps, parity):
    detuning = ratio * kc
    omega = detuning / np.max(abs(m))
    half = 2 * np.pi / omega
    As = [affine_drift(sign * eps * omega * m, parity) for sign in (1, -1)]
    Us = [expm(A * half) for A in As]
    U = Us[1] @ Us[0]
    z = np.zeros(13, complex)
    z[-1] = 1
    z[:12] = np.linalg.solve(np.eye(12) - U[:12, :12], U[:12, 12])
    max_pop = 0.0
    sum_pop = 0.0
    steps = 1024
    for A in As:
        u = expm(A * half / steps)
        for _ in range(steps):
            z = u @ z
            pop = abs(z[:3]) ** 2
            max_pop = max(max_pop, float(np.max(pop)))
            sum_pop += float(np.sum(pop))
    return {
        "fractional_CD_error": eps,
        "parity": parity,
        "cycle_duration": 2 * half,
        "max_single_mode_coherent_gauge_population": max_pop,
        "mean_total_coherent_gauge_population": sum_pop / (2 * steps),
        "Floquet_radius": float(max(abs(np.linalg.eigvals(U[:12, :12])))),
    }


def main():
    samples = 2**15
    x = np.arange(samples) / samples
    theta = np.where(x < 0.5, 4 * np.pi * x, 4 * np.pi * (1 - x))
    monomials = []
    for coeff in itertools.product((-1, 0, 1), repeat=3):
        weight = sum(c != 0 for c in coeff)
        if weight not in (1, 2):
            continue
        # A and A-dagger are the same Hermitian contamination; keep one.
        if next(c for c in coeff if c) < 0:
            continue
        coeff = np.asarray(coeff)
        freq = float(coeff @ m)
        phase = np.exp(1j * freq * theta)
        force = np.zeros((samples, 3), complex)
        for j, sigma in enumerate(coeff):
            if sigma:
                force[:, j] = phase if sigma > 0 else phase.conj()
        monomials.append((coeff.tolist(), freq, force))
    rows = []
    for ratio in (10.0, 50.0, 200.0):
        delta = ratio * kc
        cycle = 4 * np.pi * max(abs(m)) / delta
        cases = []
        for coeff, freq, force in monomials:
            reference = np.where(np.asarray(coeff) != 0, 1.0, 0.0)[None, :]
            ratios = []
            for parity in (-1, 1):
                ratios.append(all_port_power(force, cycle, parity) /
                              all_port_power(reference, cycle, parity))
            cases.append({"monomial_signs": coeff,
                          "winding_frequency_multiple": freq,
                          "max_zero_frequency_force": float(max(abs(force.mean(axis=0)))),
                          "all_port_leaked_power_ratio": max(ratios)})
        gauges = [gauge_excursion(ratio, eps, parity)
                  for eps in (0.0, 0.001, 0.01) for parity in (-1, 1)]
        rows.append({"max_detuning_over_confinement": ratio,
                     "cycle_duration": cycle,
                     "parasitic_cases": cases,
                     "worst_power_ratio": max(c["all_port_leaked_power_ratio"] for c in cases),
                     "actuator_excursions": gauges})
    laws = []
    for weight in range(2, 13):
        N = 2 ** (weight - 1)
        mu = N * (N * N + 2) / 12
        winding = np.array([2**j for j in range(weight - 1)] + [-(N - 1)])
        action_bound = 4 * np.pi * np.sqrt(mu / N)
        balanced_action = 4 * np.pi * np.sqrt(np.dot(winding, winding))
        laws.append({"parity_weight": weight, "orthogonal_characters": N,
                     "squared_frequency_sum_lower_bound": mu,
                     "phase_action_lower_bound": float(action_bound),
                     "balanced_winding_phase_action": float(balanced_action),
                     "peak_detuning_times_cycle_lower_bound": float(action_bound / np.sqrt(weight)),
                     "balanced_winding_peak_detuning_times_cycle": float(4 * np.pi * max(abs(winding)))})
    out = {"parameters": {"G": G, "gamma": gamma, "n": n, "nu": nu,
                           "confinement_rate": kc, "winding": m.tolist()},
           "filter_and_control": rows, "universal_phase_null_action_bound": laws,
           "scope": "Steady periodic linear response with all output ports and desired parity-dependent squeezing. Actuator excursion is a separate affine mean calculation, not a joint logical channel or finite-cat guarantee. Arbitrary mixed creation/annihilation parasitics of weights1,2 are included."}
    dest = Path(__file__).with_name("winding_filter_results.json")
    dest.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({"worst_power_ratios": [(x["max_detuning_over_confinement"], x["worst_power_ratio"]) for x in rows],
                      "one_percent_max_gauge_populations": [(x["max_detuning_over_confinement"], max(y["max_single_mode_coherent_gauge_population"] for y in x["actuator_excursions"] if y["fractional_CD_error"] == .01)) for x in rows],
                      "result_file": str(dest)}, indent=2))


if __name__ == "__main__":
    main()
