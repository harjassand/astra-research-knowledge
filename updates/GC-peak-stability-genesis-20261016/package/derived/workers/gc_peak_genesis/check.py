"""Independent finite-dimensional checks; not proofs of uniform theorems.

Uses NumPy only. Acquired/input author scripts are not executed.
"""
from __future__ import annotations

import hashlib
import itertools
import json
import math
import pathlib
import sys

import numpy as np


HERE = pathlib.Path(__file__).resolve().parent
RNG = np.random.default_rng(890104)
I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Z = np.diag([1, -1]).astype(complex)
P0 = np.diag([1, 0]).astype(complex)
P1 = np.diag([0, 1]).astype(complex)


def expm_small(matrix):
    """Scaling, convergent Taylor series, squaring; independent of SciPy."""
    matrix = np.asarray(matrix, dtype=complex)
    norm = np.linalg.norm(matrix, ord=np.inf)
    scale = max(0, math.ceil(math.log2(norm))) if norm > 1 else 0
    arg = matrix / (2**scale)
    result = np.eye(matrix.shape[0], dtype=complex)
    term = result.copy()
    for k in range(1, 160):
        term = term @ arg / k
        result = result + term
        if np.linalg.norm(term, ord=np.inf) < 2e-17:
            break
    else:
        raise AssertionError("expm series did not converge")
    for _ in range(scale):
        result = result @ result
    return result


def unitary(hamiltonian, duration=1):
    values, vectors = np.linalg.eigh(hamiltonian)
    return (vectors * np.exp(-1j * duration * values)) @ vectors.conj().T


def hermitian(dim, norm):
    raw = RNG.normal(size=(dim, dim)) + 1j * RNG.normal(size=(dim, dim))
    raw = (raw + raw.conj().T) / 2
    return raw * norm / np.max(np.abs(np.linalg.eigvalsh(raw)))


def exposure(segments):
    """Exact segment propagation of x'=j-lambda*x and C'=2*j*x."""
    x = 0.0
    energy = 0.0
    for duration, j, rate in segments:
        if rate == 0:
            energy += 2 * j * x * duration + (j * duration) ** 2
            x += j * duration
        else:
            drop = -math.expm1(-rate * duration)
            integral_x = x * drop / rate + j * (duration / rate - drop / rate**2)
            energy += 2 * j * integral_x
            x = x * (1 - drop) + j * drop / rate
    return energy


def actual_qubit(segments):
    """Bloch y,z solution of the literal continuous dephasing master equation."""
    yz = np.array([0, 1], dtype=complex)
    for duration, j, rate in segments:
        generator = np.array([[-rate, -2 * j], [2 * j, 0]], dtype=complex)
        yz = expm_small(duration * generator) @ yz
    assert abs(yz[1].imag) < 1e-12
    return float((1 - yz[1].real) / 2)


def peak(J, T, L, budget):
    assert 0 <= budget <= L * T + 1e-12
    if budget == 0:
        return (J * T) ** 2, [(T, J, 0.0)]
    if L * T >= budget + 2:
        hold = T / (budget + 2)
        rate = (budget + 2) / T
        segments = [(hold, J, 0.0), (T - 2 * hold, J, rate), (hold, J, 0.0)]
        return 2 * (J * T) ** 2 / (budget + 2), segments
    d = J / L
    q = (J * T - d * budget) / 2
    e = math.exp(-budget)
    value = 2 * d * d * (budget - 1 + e) + 4 * d * q * (1 - e) + 2 * q * q * (1 + e)
    hold = (T - budget / L) / 2
    return value, [(hold, J, 0.0), (budget / L, J, L), (hold, J, 0.0)]


def project_rates(raw, L, budget, T):
    lo, hi = -2 * L, 2 * L
    for _ in range(100):
        shift = (lo + hi) / 2
        total = np.clip(raw + shift, 0, L).mean() * T
        if total < budget:
            lo = shift
        else:
            hi = shift
    return np.clip(raw + (lo + hi) / 2, 0, L)


def endpoint_effect(hamiltonian_actions, z, target):
    """Heisenberg effect of fixed-gap unitary evolution and actual pinches."""
    effect = target.copy()
    for k in reversed(range(len(hamiltonian_actions))):
        u = unitary(hamiltonian_actions[k])
        effect = u.conj().T @ effect @ u
        if k > 0:
            effect = (effect + z @ effect @ z) / 2
    return (effect + effect.conj().T) / 2


def walsh_odd_effect(hamiltonian_actions):
    gaps = len(hamiltonian_actions)
    dim = hamiltonian_actions[0].shape[0]
    effect = np.zeros((dim, dim), dtype=complex)
    for toggles in itertools.product([0, 1], repeat=gaps - 1):
        prop = []
        for f in [0, 1]:
            sign = (-1) ** f
            u = np.eye(dim, dtype=complex)
            for k, action in enumerate(hamiltonian_actions):
                u = unitary(sign * action) @ u
                if k < gaps - 1:
                    sign *= (-1) ** toggles[k]
            prop.append(u)
        odd = (prop[0] - prop[1]) / 2
        effect += odd.conj().T @ odd / (2 ** (gaps - 1))
    return (effect + effect.conj().T) / 2


def deterministic_q(actions):
    return 1 - math.prod(math.cos(min(x, math.pi / 2)) ** 2 for x in actions)


def check_peak():
    rows = []
    for J, T, L, budget in [(.3, 1, 3, 2), (.4, 2, 2, 3), (.2, 1, 8, 3), (.3, 1, 4, 2), (.5, 1, 2, 2), (.4, 1, 2, 0)]:
        value, schedule = peak(J, T, L, budget)
        direct = exposure(schedule)
        assert abs(direct - value) < 2e-13
        assert abs(sum(h * rate for h, _, rate in schedule) - budget) < 2e-13
        assert all(0 <= rate <= L + 1e-12 for _, _, rate in schedule)
        least_margin = math.inf
        for _ in range(60):
            rates = project_rates(RNG.uniform(0, L, size=32), L, budget, T)
            candidate = exposure([(T / 32, J, float(rate)) for rate in rates])
            least_margin = min(least_margin, candidate - value)
            assert candidate >= value - 3e-12
        p = actual_qubit(schedule)
        a = J * T
        kappa = (math.sin(a) / a) ** 2 if a else 1
        assert kappa * value <= p + 2e-12 <= value + 4e-12
        rows.append(dict(J=J, T=T, L=L, budget=budget, formula=value, segment_energy=direct,
                         random_feasible_min_margin=least_margin, actual_qubit=p, lower=kappa * value))
    return rows


def check_physical_sandwich():
    largest_upper_ratio = 0.0
    smallest_lower_margin = math.inf
    for _ in range(160):
        count = 9
        durations = RNG.dirichlet(np.ones(count))
        envelope = RNG.uniform(.1, 3, size=count)
        desired_action = RNG.uniform(.015, 2.8)
        envelope *= desired_action / np.dot(durations, envelope)
        rates = RNG.uniform(0, 18, size=count)
        segments = list(zip(durations, envelope, rates))
        a = float(np.dot(durations, envelope))
        C = exposure(segments)
        p = actual_qubit(segments)
        kappa = (math.sin(a) / a) ** 2
        assert p <= C + 3e-12
        assert p >= kappa * C - 3e-12
        largest_upper_ratio = max(largest_upper_ratio, p / C)
        smallest_lower_margin = min(smallest_lower_margin, p - kappa * C)
    return dict(cases=160, largest_p_over_C=largest_upper_ratio, smallest_p_minus_lower=smallest_lower_margin)


def check_sink_and_walsh():
    rows = []
    action_lists = [[.1, .3, .2], [.4, .4, .4, .4], [2.0, .1], [.001, .002, .003, .004]]
    for actions in action_lists:
        m = len(actions)
        bath = m + 1
        matrices = []
        for k, action in enumerate(actions):
            coupling = np.zeros((bath, bath), dtype=complex)
            coupling[0, k + 1] = coupling[k + 1, 0] = min(action, math.pi / 2)
            matrices.append(np.kron(X, coupling))
        z = np.kron(Z, np.eye(bath))
        target = np.kron(P1, np.eye(bath))
        endpoint = endpoint_effect(matrices, z, target)[:bath, :bath]
        walsh_full = walsh_odd_effect(matrices)
        walsh = walsh_full[:bath, :bath]
        q = deterministic_q(actions)
        assert abs(endpoint[0, 0].real - q) < 5e-13
        assert abs(np.linalg.eigvalsh(endpoint)[-1] - q) < 5e-13
        assert np.max(np.abs(endpoint - walsh)) < 8e-13
        assert abs(np.linalg.eigvalsh(walsh_full)[-1] - q) < 8e-13
        rows.append(dict(actions=actions, theorem=q, actual_u_input=float(endpoint[0, 0].real),
                         largest_endpoint_eigenvalue=float(np.linalg.eigvalsh(endpoint)[-1]),
                         walsh_endpoint_matrix_error=float(np.max(np.abs(endpoint - walsh)))))
    for m in [1, 2, 3, 6]:
        for a in [.1, .7, 1.4, 3.0, 10.0]:
            qopt = 1 - math.cos(min(a / m, math.pi / 2)) ** (2 * m)
            for _ in range(80):
                actions = a * RNG.dirichlet(np.ones(m))
                assert deterministic_q(actions) >= qopt - 2e-13
    return dict(sink_cases=rows, global_slot_partition_checks=1600)


def check_joint_walsh_identity():
    """Actual noncommuting shared-bath model, not a scalar formula substitution."""
    bath = 2
    m = 3
    durations = [.27, .42, .31]
    j = [.19, .26]
    bases = [hermitian(bath, .6) for _ in range(m)]
    coeffs = [[hermitian(bath, j[i]) for _ in range(m)] for i in range(2)]
    x1 = np.kron(X, I2)
    x2 = np.kron(I2, X)
    z1 = np.kron(np.kron(Z, I2), np.eye(bath))
    z2 = np.kron(np.kron(I2, Z), np.eye(bath))
    target = np.kron(np.kron(P1, P1), np.eye(bath))
    actions = [durations[k] * (np.kron(np.eye(4), bases[k]) + np.kron(x1, coeffs[0][k]) + np.kron(x2, coeffs[1][k])) for k in range(m)]
    effect = target.copy()
    for k in reversed(range(m)):
        u = unitary(actions[k])
        effect = u.conj().T @ effect @ u
        if k > 0:
            effect = (effect + z1 @ effect @ z1) / 2
            effect = (effect + z2 @ effect @ z2) / 2
    endpoint = effect[:bath, :bath]
    walsh = np.zeros((bath, bath), dtype=complex)
    for toggle_tuple in itertools.product([0, 1], repeat=2 * (m - 1)):
        toggles = [toggle_tuple[:m - 1], toggle_tuple[m - 1:]]
        odd = np.zeros((bath, bath), dtype=complex)
        for f in itertools.product([0, 1], repeat=2):
            signs = [(-1) ** f[0], (-1) ** f[1]]
            u = np.eye(bath, dtype=complex)
            for k in range(m):
                h = bases[k] + signs[0] * coeffs[0][k] + signs[1] * coeffs[1][k]
                u = unitary(h, durations[k]) @ u
                if k < m - 1:
                    for i in range(2):
                        signs[i] *= (-1) ** toggles[i][k]
            odd += (-1) ** sum(f) * u / 4
        walsh += odd.conj().T @ odd / (2 ** (2 * (m - 1)))
    err = float(np.max(np.abs(endpoint - walsh)))
    certificate = math.prod(sum((ji * h) ** 2 for h in durations) for ji in j)
    largest = float(np.linalg.eigvalsh((walsh + walsh.conj().T) / 2)[-1])
    assert err < 2e-13
    assert largest <= certificate + 2e-13
    return dict(matrix_identity_error=err, largest_effect_eigenvalue=largest,
                selected_product_certificate=certificate, bath_is_shared=True,
                noncommuting_coefficient_norm=float(np.linalg.norm(coeffs[0][0] @ coeffs[1][0] - coeffs[1][0] @ coeffs[0][0])))


def check_counts_and_obstruction():
    allocation_rows = []
    for r in [2, 3, 4]:
        for total in range(9):
            q, s = divmod(total, r)
            expected = (q + 1) ** (r - s) * (q + 2) ** s
            candidates = [math.prod(n + 1 for n in allocation)
                          for allocation in itertools.product(range(total + 1), repeat=r)
                          if sum(allocation) == total]
            assert max(candidates) == expected
            allocation_rows.append(dict(parents=r, total_slots=total, best_denominator=expected))
    dominance_rows = []
    for N in [1, 2, 3, 8, 20]:
        for a in [.03, .2, math.pi / 4]:
            qdet = 1 - math.cos(a / (N + 1)) ** (2 * (N + 1))
            lower_poi = (math.sin(a) / a) ** 2 * 2 * a * a / (N + 2)
            assert qdet < lower_poi
            dominance_rows.append(dict(N=N, a=a, exact_fixed_minimax=qdet, poisson_minimax_lower=lower_poi))
    burst_rows = []
    L, a = 5.0, .4
    for width in [1.0, .1, .01, .001]:
        segments = [(width, a / width, L)]
        C = exposure(segments)
        p = actual_qubit(segments)
        assert C >= math.exp(-L * width) * a * a - 2e-12
        assert p >= math.exp(-L * width / 2) * math.sin(a) ** 2 - 2e-12
        burst_rows.append(dict(width=width, C_over_a_squared=C / a**2, actual_qubit=p,
                              no_control_limit=math.sin(a) ** 2))
    return dict(integer_allocation_cases=allocation_rows, strict_robust_dominance=dominance_rows,
                unknown_profile_bursts=burst_rows)


def main():
    result = dict(
        status="PASS",
        scope="Finite identities, explicit worst-case witness matrices, algebraic boundaries, and diagnostics only. Uniform/global claims require the saved analytic proofs.",
        python=sys.executable,
        numpy=np.__version__,
        peak_reconstruction=check_peak(),
        actual_qubit_sandwich=check_physical_sandwich(),
        exact_fixed_slot_sink=check_sink_and_walsh(),
        joint_shared_bath_walsh=check_joint_walsh_identity(),
        counts_and_unknown_profile=check_counts_and_obstruction(),
    )
    output = HERE / "CHECK_RESULTS.json"
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(dict(status=result["status"], output=str(output),
                          joint_matrix_error=result["joint_shared_bath_walsh"]["matrix_identity_error"],
                          check_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest()), indent=2))


if __name__ == "__main__":
    main()
