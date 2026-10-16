"""Independent finite diagnostics; analytic claims live in the accompanying proofs.

Run with the bundled Python+NumPy runtime. No SciPy or acquired scripts used.
"""
from __future__ import annotations

import itertools
import json
import math
from pathlib import Path

import numpy as np


OUT = Path(__file__).resolve().parent
I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.diag([1, -1]).astype(complex)


def kron(*matrices):
    answer = np.array([[1.0]], dtype=complex)
    for matrix in matrices:
        answer = np.kron(answer, matrix)
    return answer


def unitary(hamiltonian, duration):
    values, vectors = np.linalg.eigh(hamiltonian)
    return (vectors * np.exp(-1j * duration * values)) @ vectors.conj().T


def expm(matrix):
    """Scaling/squaring Taylor series; used only on tiny Bloch matrices."""
    norm = np.linalg.norm(matrix, ord=np.inf)
    scale = max(0, math.ceil(math.log2(max(1.0, float(norm)))))
    small = matrix / (2**scale)
    term = np.eye(matrix.shape[0], dtype=matrix.dtype)
    result = term.copy()
    for order in range(1, 100):
        term = term @ small / order
        result += term
        if np.linalg.norm(term, ord=np.inf) < 2e-17:
            break
    else:
        raise AssertionError("Taylor exponential did not converge")
    for _ in range(scale):
        result = result @ result
    return result


def exact_certificate(J, segments):
    """Integrate x'=1-lambda*x, C'=2 J^2 x segment by segment."""
    x = 0.0
    integral_x = 0.0
    for duration, rate in segments:
        if duration == 0:
            continue
        if rate == 0:
            integral_x += x * duration + duration * duration / 2
            x += duration
        else:
            one_minus = -math.expm1(-rate * duration)
            integral_x += x * one_minus / rate + duration / rate - one_minus / rate**2
            x = (1 - one_minus) * x + one_minus / rate
    return 2 * J * J * integral_x


def cap_schedule(T, L, exposure):
    if exposure < 0 or exposure > L * T + 1e-13:
        raise ValueError("infeasible exposure")
    if exposure == 0:
        return [(T, 0.0)]
    if L * T >= exposure + 2:
        h = T / (exposure + 2)
        return [(h, 0.0), (T - 2 * h, (exposure + 2) / T), (h, 0.0)]
    h = (T - exposure / L) / 2
    return [(h, 0.0), (exposure / L, L), (h, 0.0)]


def cap_value(J, T, L, exposure):
    if exposure > L * T + 1e-13:
        raise ValueError("infeasible exposure")
    a = J * T
    if exposure == 0:
        return a * a
    if L * T >= exposure + 2:
        return 2 * a * a / (exposure + 2)
    d = J / L
    q = (a - d * exposure) / 2
    decay = math.exp(-exposure)
    return (2 * d * d * (exposure - 1 + decay)
            + 4 * d * q * (1 - decay)
            + 2 * q * q * (1 + decay))


def actual_endpoint(J, segments):
    yz = np.array([0.0, 1.0])
    for duration, rate in segments:
        generator = np.array([[-rate, -2 * J], [2 * J, 0.0]])
        yz = expm(duration * generator) @ yz
    return (1 - float(yz[1])) / 2


def cap_diagnostics():
    cases = [(1.0, 2.0, 2.0, 3.0), (.3, 1.0, 2.0, 2.0),
             (.7, 2.0, 2.0, 2.0), (.5, 1.0, 1.0, 0.0),
             (.4, 1.0, 3.0, 2.0), (.4, 1.0, 6.0, 2.0),
             (0.0, 1.0, 3.0, 2.0), (.4, 0.0, 3.0, 0.0),
             (.4, 1.0, 0.0, 0.0)]
    rows = []
    for J, T, L, exposure in cases:
        schedule = cap_schedule(T, L, exposure)
        value = cap_value(J, T, L, exposure)
        direct = exact_certificate(J, schedule)
        assert abs(value - direct) < 2e-12
        assert abs(sum(h * rate for h, rate in schedule) - exposure) < 1e-12
        assert all(0 <= rate <= L + 1e-13 for _, rate in schedule)
        a = J * T
        actual = actual_endpoint(J, schedule)
        if 0 < a < math.pi:
            lower = (math.sin(a) / a)**2 * value
            assert lower - 2e-12 <= actual <= value + 2e-12
        else:
            lower = None
        rows.append(dict(J=J, T=T, L=L, exposure=exposure,
                         certificate=value, integrated_certificate=direct,
                         actual_constant_X_error=actual, sinc_lower=lower,
                         schedule=schedule))

    # Exhaust an explicit coarse feasible family at fixed exposure and cap.
    brute = []
    for a in [.3, 1.4, 2.8]:
        best_C, best_p = float("inf"), float("inf")
        for on in itertools.combinations(range(8), 4):
            schedule = [(1 / 8, 4.0 if i in on else 0.0) for i in range(8)]
            C = exact_certificate(a, schedule)
            p = actual_endpoint(a, schedule)
            assert C >= cap_value(a, 1, 4, 2) - 1e-12
            assert p >= (math.sin(a) / a)**2 * C - 1e-12
            assert p <= C + 1e-12
            best_C = min(best_C, C)
            best_p = min(best_p, p)
        brute.append(dict(a=a, profiles=70, minimum_certificate_on_grid=best_C,
                          certificate_global_optimum=cap_value(a, 1, 4, 2),
                          minimum_actual_known_X_error_on_grid=best_p,
                          actual_known_X_error_of_certificate_optimizer=
                          actual_endpoint(a, cap_schedule(1, 4, 2))))
    return dict(boundaries=rows, coarse_exhaustion=brute)


def random_hermitian(rng, dimension, norm):
    raw = rng.normal(size=(dimension, dimension)) + 1j * rng.normal(size=(dimension, dimension))
    matrix = (raw + raw.conj().T) / 2
    return matrix * (norm / max(abs(np.linalg.eigvalsh(matrix))))


def finite_grid_diagnostics():
    # Two selected signs share the same four-dimensional physical system/bath.
    # Different deterministic own grids cross in time. The physical coefficients
    # are noncommuting, time dependent and independent of every private bit.
    own_cuts = [[.25, .7], [.2, .5, .8]]
    norms = [.4, .6]
    events = sorted((time, parent) for parent, cuts in enumerate(own_cuts) for time in cuts)
    times = [0.0] + [time for time, _ in events] + [1.0]
    durations = np.diff(times)
    pminus = np.array([[.5, -.5], [-.5, .5]], dtype=complex)
    plus = np.array([1, 1], dtype=complex) / math.sqrt(2)
    prepare = np.kron(np.kron(plus, plus)[:, None], np.eye(4))
    virtual_X = [kron(X, I2, np.eye(4)), kron(I2, X, np.eye(4))]
    virtual_Z = [kron(Z, I2), kron(I2, Z)]
    witness = kron(pminus, pminus, np.eye(4))
    c = [norms[i]**2 * sum(np.diff([0] + own_cuts[i] + [1])**2) for i in range(2)]
    bound = c[0] * c[1]
    rows = []
    for seed in range(12):
        rng = np.random.default_rng(83910 + seed)
        baseline = [random_hermitian(rng, 4, 1.7) for _ in durations]
        coefficients = [[random_hermitian(rng, 4, norm) for _ in durations] for norm in norms]
        effect = np.zeros((4, 4), dtype=complex)
        for refresh in itertools.product([0, 1], repeat=len(events)):
            K = np.zeros((4, 4), dtype=complex)
            for initial in itertools.product([0, 1], repeat=2):
                signs = np.array([(-1)**bit for bit in initial])
                U = np.eye(4, dtype=complex)
                for segment, duration in enumerate(durations):
                    H = baseline[segment] + sum(signs[i] * coefficients[i][segment] for i in range(2))
                    U = unitary(H, duration) @ U
                    if segment < len(events):
                        signs[events[segment][1]] *= (-1)**refresh[segment]
                K += (-1)**sum(initial) * U / 4
            effect += K.conj().T @ K / (2**len(events))

        # Independently calculate the deterministic virtual-pinch endpoint effect.
        E = witness.copy()
        for segment in reversed(range(len(durations))):
            if segment < len(events):
                flip = virtual_X[events[segment][1]]
                E = (E + flip @ E @ flip) / 2
            H = np.kron(np.eye(4), baseline[segment])
            H += sum(np.kron(virtual_Z[i], coefficients[i][segment]) for i in range(2))
            U = unitary(H, durations[segment])
            E = U.conj().T @ E @ U
        virtual_effect = prepare.conj().T @ E @ prepare
        difference = float(np.linalg.norm(effect - virtual_effect, ord=2))
        largest = float(np.linalg.eigvalsh(effect).max())
        assert difference < 1e-12
        assert largest <= bound + 1e-12
        rows.append(dict(seed=seed, largest_whole_input_effect=largest,
                         product_certificate=bound, ratio=largest / bound,
                         original_Walsh_vs_virtual_pinch_error=difference))

    # Equal-action single-qubit case also has a closed actual-error formula.
    equal_rows = []
    for a, N in [(0.4, 0), (0.4, 1), (0.4, 8), (1.2, 4)]:
        p = .5 * (1 - math.cos(2 * a / (N + 1))**(N + 1))
        C = a * a / (N + 1)
        lower = (math.sin(a) / a)**2 * C
        assert lower - 1e-12 <= p <= C + 1e-12
        equal_rows.append(dict(a=a, N=N, physical_mean_internal_toggles=N / 2,
                               actual_known_X_error=p, certificate=C,
                               Poisson_best_uncapped_certificate_at_equal_mean=
                               a * a / (N / 2 + 1)))
    return dict(shared_bath_effects=rows, equal_action_comparison=equal_rows)


def deterministic_diagnostics():
    a = .4
    rows = []
    for N in [0, 1, 2, 8, 64]:
        # Rectify an arbitrary public alternating sign path in the lab coupling.
        Us = []
        for initial in [0, 1]:
            U = I2.copy()
            for segment in range(N + 1):
                public_sign = (-1)**segment
                A_lab = public_sign * a * X
                H_toggling = (-1)**initial * public_sign * A_lab
                U = unitary(H_toggling, 1 / (N + 1)) @ U
            Us.append(U)
        K = (Us[0] - Us[1]) / 2
        effect = K.conj().T @ K
        actual = float(np.linalg.eigvalsh(effect).max())
        assert np.linalg.norm(effect - math.sin(a)**2 * I2) < 1e-12
        rows.append(dict(N=N, nonzero_character_effect=actual,
                         invalid_equal_gap_suppression=a * a / (N + 1)))

    # Complete local detection/no-logical check for the five-qubit code.
    paulis = {"I": I2, "X": X, "Y": Y, "Z": Z}
    generators = [kron(*(paulis[x] for x in word))
                  for word in ["XZZXI", "IXZZX", "XIXZZ", "ZXIXZ"]]
    assert all(np.linalg.norm(g @ h - h @ g) < 1e-12 for g in generators for h in generators)
    invisible = []
    for letter, matrix in paulis.items():
        P = kron(matrix, I2, I2, I2, I2)
        if all(np.linalg.norm(P @ g - g @ P) < 1e-12 for g in generators):
            invisible.append(letter)
    assert invisible == ["I"]
    return dict(rectified_paths=rows, single_site_centralizer=invisible,
                scope="Nonzero-character suppression only; no logical failure inferred.")


def finite_action_diagnostic():
    a, exposure, L = 3.1, 2.0, 100.0
    delta = exposure / L
    optimizer = cap_schedule(1, L, exposure)
    competitor = [((1 - delta) / 2, 0.0), (delta, L), ((1 - delta) / 2, 0.0)]
    lower_optimizer = (1 - math.sin(a) / a) / (2 * math.e)
    upper_competitor = max(a * a * delta * delta, (abs(math.sin(a)) + 2 * a * delta)**2)
    actual_optimizer = actual_endpoint(a, optimizer)
    actual_competitor = actual_endpoint(a, competitor)
    assert actual_optimizer >= lower_optimizer - 1e-12
    assert actual_competitor <= upper_competitor + 1e-12
    assert lower_optimizer > upper_competitor
    return dict(a=a, exposure=exposure, L=L, delta=delta,
                optimizer_actual_error=actual_optimizer,
                optimizer_analytic_lower=lower_optimizer,
                competitor_actual_error=actual_competitor,
                competitor_analytic_upper=upper_competitor,
                optimizer_certificate=exact_certificate(a, optimizer),
                competitor_certificate=exact_certificate(a, competitor),
                scope="Strict known-H finite-action separation; not unknown-H minimax.")


def main():
    result = dict(status="PASS", scope="Finite diagnostics only; universality is analytic.",
                  cap=cap_diagnostics(), finite_grid=finite_grid_diagnostics(),
                  deterministic=deterministic_diagnostics(),
                  finite_action=finite_action_diagnostic())
    (OUT / "checks.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(dict(status=result["status"],
                         shared_bath_cases=len(result["finite_grid"]["shared_bath_effects"]),
                         maximum_shared_bath_effect_ratio=max(row["ratio"] for row in result["finite_grid"]["shared_bath_effects"]),
                         maximum_Walsh_virtual_pinch_difference=max(row["original_Walsh_vs_virtual_pinch_error"] for row in result["finite_grid"]["shared_bath_effects"]),
                         finite_action=result["finite_action"]), indent=2))


if __name__ == "__main__":
    main()
