"""Small deterministic checks for endpoint temporal-order spectroscopy.

No physical experiment is claimed. All computations are three-to-six-level
matrix exponentials or small ODE integrations.
"""
import json
from pathlib import Path
import numpy as np
from scipy.linalg import expm
from scipy.integrate import solve_ivp


def chain_hamiltonian(word, a):
    h = np.zeros((len(word) + 1, len(word) + 1))
    for j, letter in enumerate(word):
        h[j + 1, j] = h[j, j + 1] = a[letter]
    return h


def propagate(word, segments, coupling):
    n = len(word) + 1
    u = np.eye(n, dtype=complex)
    for duration, a in segments:
        u = expm(-1j * coupling * duration * chain_hamiltonian(word, a)) @ u
    return u


def signature_word(word, segments):
    # Nilpotent chain computes the requested iterated integral exactly,
    # up to ordinary floating-point matrix exponential rounding.
    n = len(word) + 1
    v = np.zeros(n)
    v[0] = 1
    for duration, a in segments:
        h = np.zeros((n, n))
        for j, letter in enumerate(word):
            h[j + 1, j] = a[letter]
        v = expm(duration * h) @ v
    return float(v[-1])


def witness(word, segments, coupling):
    u = propagate(word, segments, coupling)
    return (1j ** len(word) * (u[-1, 0] - u[0, -1])).real


def chiral_numeric(coupling, omega=1.0, phi=0.0):
    duration = 2 * np.pi / abs(omega)
    def rhs(t, u):
        a = [np.cos(omega * t + phi), np.sin(omega * t + phi)]
        return (-1j * coupling * chain_hamiltonian([0, 1], a)
                @ u.reshape(3, 3)).ravel()
    solution = solve_ivp(rhs, [0, duration], np.eye(3, dtype=complex).ravel(),
                         rtol=1e-11, atol=1e-13)
    u = solution.y[:, -1].reshape(3, 3)
    return float(-(u[2, 0] - u[0, 2]).real)


def main():
    rng = np.random.default_rng(19)
    results = {}
    segments = [(float(rng.uniform(.1, .6)), rng.uniform(-1, 1, 3))
                for _ in range(7)]
    reciprocity_errors = []
    coefficient_tests = []
    for word in [[0, 1], [0, 1, 2], [0, 0, 1, 2], [0, 1, 0, 1, 2]]:
        u = propagate(word, segments, .7)
        ur = propagate(word, segments[::-1], .7)
        reciprocity_errors.append(float(np.max(np.abs(ur - u.T))))
        delta = signature_word(word, segments) - signature_word(word[::-1], segments)
        estimates = []
        for coupling in [.2, .1, .05]:
            estimates.append({"coupling": coupling,
                              "normalized_witness": witness(word, segments, coupling)
                              / coupling ** len(word)})
        coefficient_tests.append({"word": word, "signature_difference": delta,
                                  "estimates": estimates})
    results["max_reversal_transpose_error"] = max(reciprocity_errors)
    results["leading_coefficients"] = coefficient_tests

    ab = [(1.0, np.array([1., 0.])), (1.0, np.array([0., 1.]))]
    ba = ab[::-1]
    results["ordered_pulses"] = {"AB": witness([0, 1], ab, np.pi / 2),
                                 "BA": witness([0, 1], ba, np.pi / 2)}

    chiral = []
    for coupling in [.1, .3, .75, 1.2]:
        vals = [chiral_numeric(coupling, phi=phi) for phi in [0., .31, 1.57, 4.3]]
        omega = 1.
        big_omega = np.sqrt(omega ** 2 + coupling ** 2)
        exact = 2 * omega / big_omega * np.sin(2 * np.pi * big_omega / omega)
        chiral.append({"coupling": coupling, "exact": float(exact),
                       "numerical_by_phase": vals,
                       "max_absolute_error": float(max(abs(v - exact) for v in vals)),
                       "reverse_numeric": chiral_numeric(coupling, omega=-1)})
    results["stationary_chiral_input"] = chiral

    # A dark reference exposes the complex amplitude, rather than its square.
    active = propagate([0, 1], ab, np.pi / 2)
    total = np.eye(4, dtype=complex)
    total[1:, 1:] = active
    state = np.zeros(4, dtype=complex)
    state[[0, 1]] = 1 / np.sqrt(2)
    state = total @ state
    readout = np.zeros((4, 4))
    readout[0, 3] = readout[3, 0] = 1
    results["reference_readout"] = {
        "measured_real_amplitude": float(np.vdot(state, readout @ state).real),
        "target_real_amplitude": float(active[2, 0].real)}

    assert results["max_reversal_transpose_error"] < 1e-12
    assert abs(results["ordered_pulses"]["AB"] - 1) < 1e-12
    assert abs(results["ordered_pulses"]["BA"] + 1) < 1e-12
    assert max(x["max_absolute_error"] for x in chiral) < 1e-8
    text = json.dumps(results, indent=2)
    Path(__file__).with_name("verification_results.json").write_text(text + "\n")
    print(text)


if __name__ == "__main__":
    main()
