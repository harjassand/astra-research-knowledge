"""Closed-loop force budget and inaccessible-output leakage checks.

Integrated squared coupling E is not thermodynamic energy in joules.
"""
import json
import numpy as np
from scipy.integrate import simpson


def random_loop_check(rng, kappa):
    t = np.linspace(0, 2 * np.pi, 16385)
    harmonics = np.arange(1, 9)
    waves = np.exp(1j * harmonics[:, None] * t[None, :])
    c = (rng.normal(size=(2, len(harmonics))) + 1j * rng.normal(size=(2, len(harmonics)))) / harmonics[None, :] ** 2
    alpha = c @ (waves - 1)
    velocity = (c * (1j * harmonics)[None, :]) @ waves
    force = 1j * (velocity + kappa * alpha / 2)
    j = float(simpson(np.sum(abs(alpha) ** 2, axis=0), x=t))
    k = float(simpson(np.sum(abs(velocity) ** 2, axis=0), x=t))
    e = float(simpson(np.sum(abs(force) ** 2, axis=0), x=t))
    theta = float(simpson(np.imag(alpha[0].conj() * velocity[1] + alpha[1].conj() * velocity[0]), x=t))
    discriminant = e * e - kappa * kappa * theta * theta
    lower_j = 2 * theta * theta / (e + np.sqrt(discriminant))
    assert abs(e - (k + kappa * kappa * j / 4)) < 1e-9
    assert theta * theta <= j * k + 1e-9
    assert j >= lower_j - 1e-9
    return {"J": j, "K": k, "E": e, "theta": theta,
            "J_lower_bound": float(lower_j), "area_Cauchy_ratio": theta * theta / (j * k)}


def circle_family(theta=np.pi / 4, kappa=0.1, force_cap=1.0, double_coherence_decay=0.002):
    rows = []
    for loops in [1, 4, 16, 64, 256]:
        radius = np.sqrt(theta / (4 * np.pi * loops))
        frequency = np.sqrt((force_cap / radius) ** 2 - kappa * force_cap / radius)
        duration = 2 * np.pi * loops / frequency
        j = 4 * radius * radius * duration  # Both identical qubit paths.
        k = 2 * radius * radius * frequency * frequency * duration
        e = k + kappa * kappa * j / 4
        peak = radius * (np.sqrt(frequency * frequency + kappa * kappa / 4) + kappa / 2)
        assert abs(peak - force_cap) < 1e-12
        assert abs(4 * np.pi * loops * radius * radius - theta) < 1e-12
        rows.append({"loops": loops, "radius": float(radius), "frequency": float(frequency),
                     "duration": float(duration), "J": float(j), "E": float(e),
                     "peak_force_per_qubit": float(peak),
                     "unmonitored_double_flip_dephasing_exponent": float(4 * kappa * j),
                     "bus_plus_data_exponent": float(4 * kappa * j + double_coherence_decay * duration)})
    return rows


def near_saturating_two_tone(theta=np.pi / 4, kappa=0.1, duration=10.0):
    rows = []
    base_frequency = 2 * np.pi / duration
    for harmonic in [1, 4, 16, 64]:
        c_squared = theta / (4 * np.pi * (2 * harmonic + 1))
        j = 4 * duration * c_squared
        k = 2 * duration * base_frequency ** 2 * (harmonic ** 2 + (harmonic + 1) ** 2) * c_squared
        e = k + kappa ** 2 * j / 4
        ratio = theta ** 2 / (j * k)
        exact_ratio = (2 * harmonic + 1) ** 2 / (2 * (harmonic ** 2 + (harmonic + 1) ** 2))
        assert abs(ratio - exact_ratio) < 1e-12
        rows.append({"harmonic": harmonic, "duration": duration, "J": j, "E": e,
                     "maximum_carrier_frequency": (harmonic + 1) * base_frequency,
                     "area_Cauchy_ratio": ratio})
    return rows


def main():
    rng = np.random.default_rng(20261101)
    results = {"random_closed_loop_checks": [random_loop_check(rng, 0.3) for _ in range(5)],
               "fixed_peak_force_circle_family": circle_family(),
               "near_saturating_two_tone": near_saturating_two_tone()}
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
