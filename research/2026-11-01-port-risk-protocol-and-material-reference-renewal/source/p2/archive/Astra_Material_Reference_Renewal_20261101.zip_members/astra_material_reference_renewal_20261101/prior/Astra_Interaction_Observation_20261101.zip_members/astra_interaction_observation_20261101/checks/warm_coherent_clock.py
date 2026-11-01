"""Finite-dimensional checks for first-passage coherent gates and their failures."""
import json
import numpy as np
from scipy.linalg import expm


def passage(rng, target, slow, fast):
    signed, elapsed, parity, waits = 0.0, 0.0, 0, []
    while True:
        waiting = rng.exponential(1 / (slow if parity == 0 else fast))
        if parity == 0 and waiting >= target - signed:
            last = target - signed
            waits.append((last, False))
            return elapsed + last, waits
        signed += waiting if parity == 0 else -waiting
        elapsed += waiting
        waits.append((waiting, True))
        parity ^= 1


def main():
    rng = np.random.default_rng(20261102)
    x = np.array([[0, 1], [1, 0]], complex)
    y = np.array([[0, -1j], [1j, 0]], complex)
    z = np.diag([1, -1])
    eye = np.eye(2)
    slow, fast, target, samples = 1.0, 4.0, 3.0, 100000
    times = np.array([passage(rng, target, slow, fast)[0] for _ in range(samples)])
    d, total = fast - slow, fast + slow
    theory_mean = target * total / d
    theory_var = 8 * slow * fast * target / d ** 3
    laplace = {}
    for s in [0.1, 0.5, 1.0]:
        k = (-d + np.sqrt(d * d + 4 * s * (s + total))) / 2
        laplace[str(s)] = {"theory": float(np.exp(-target * k)),
                           "monte_carlo": float(np.mean(np.exp(-s * times)))}

    unknown_b = np.array([[0.31, 0.17 + 0.13j], [0.17 - 0.13j, -0.54]])
    h = np.kron(z, unknown_b)
    theta = 0.713
    jump = np.kron(np.cos(theta) * x + np.sin(theta) * y, eye)
    residuals = []
    for _ in range(50):
        _, waits = passage(rng, target, slow, fast)
        actual = np.eye(4, dtype=complex)
        for duration, event in waits:
            actual = expm(-1j * h * duration) @ actual
            if event:
                actual = jump @ actual
        residuals.append(np.linalg.norm(actual - expm(-1j * target * h), 2))

    # Two first-passage paths with the same physical and signed time differ
    # when an inaccessible target self-Hamiltonian fails to commute with B.
    free = np.kron(eye, x)
    coupling = np.kron(z, z)
    def path(first, odd, last):
        return expm(-1j * (free + coupling) * last) @ expm(-1j * (free - coupling) * odd) @ expm(-1j * (free + coupling) * first)
    first = path(0.2, 0.4, 1.2)
    second = path(0.6, 0.4, 0.8)
    noncommuting_difference = np.linalg.norm(first - second, 2)

    # Two odd endpoint transitions return parity even, but finite sampling
    # leaves a dephasing factor below one.
    gamma, interval, gap = 1.0, 0.6, 0.8
    root = np.sqrt(complex(gamma ** 2 - gap ** 2))
    odd_factor = gamma * np.sinh(interval * root) / (root * np.sinh(gamma * interval))
    result = {
        "first_passage": {"mean_theory": theory_mean, "mean_empirical": float(times.mean()),
                          "mean_standard_error": float(times.std(ddof=1) / np.sqrt(samples)),
                          "variance_theory": theory_var, "variance_empirical": float(times.var(ddof=1)),
                          "laplace": laplace},
        "unknown_target_gate_max_operator_residual": float(max(residuals)),
        "noncommuting_equal_clock_path_difference": float(noncommuting_difference),
        "finite_observer": {"gamma": gamma, "interval": interval, "spectral_gap": gap,
                            "two_odd_intervals_coherence_modulus": float(abs(odd_factor) ** 2),
                            "diamond_norm_lower_bound": float(1 - abs(odd_factor) ** 2)}
    }
    assert max(residuals) < 1e-11
    assert noncommuting_difference > 0.1
    assert abs(odd_factor) < 1
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
