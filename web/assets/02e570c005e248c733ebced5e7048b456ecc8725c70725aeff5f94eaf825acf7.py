"""Bounded independent physical/exact checks; no full generic iid backend."""
from fractions import Fraction as F
from itertools import product, combinations
from decimal import Decimal, localcontext
from math import exp, comb
import json
import random
import time
import signal
from pathlib import Path
import numpy as np

from axial_acquisition import (
    choose, sphere_moment, pauli_orbit_coefficient, pauli_orbit_columns,
    sector_column, sector_matrix, spin_dimensions, exp_neg_dyadic, ceil_log2,
    cutoffs, isotropic_sector_vector, exact_simplex_fixture, acquire_k_weights,
    matvec, total_variation, acquire_branches, block_orbit_coefficients,
    unrank_subset, qubit_state_is_psd, sample_hierarchy, phase_four_iid_fixture,
    round_dyadic_probabilities,
)

ASSERTIONS = 0
DETAILS = {}


def check(condition):
    global ASSERTIONS
    ASSERTIONS += 1
    assert condition


def zeros(n):
    return [[F(0) for _ in range(n)] for _ in range(n)]


def identity(n):
    return [[F(int(i == j)) for j in range(n)] for i in range(n)]


def add(A, B):
    return [[a + b for a, b in zip(x, y)] for x, y in zip(A, B)]


def scale(c, A):
    return [[c * x for x in row] for row in A]


def mm(A, B):
    n = len(A)
    C = zeros(n)
    for i in range(n):
        for k, a in enumerate(A[i]):
            if a:
                for j, b in enumerate(B[k]):
                    if b:
                        C[i][j] += a * b
    return C


def tr(A):
    return sum((A[i][i] for i in range(len(A))), F(0))


def equal(A, B):
    for r, s in zip(A, B):
        for x, y in zip(r, s):
            check(x == y)


def pauli_action(word, y):
    x = y
    y_count = 0
    sign = 1
    for i, letter in enumerate(word):
        bit = (y >> i) & 1
        if letter == 1:
            x ^= 1 << i
        elif letter == 2:
            x ^= 1 << i
            y_count += 1
            sign *= -1 if bit else 1
        elif letter == 3:
            sign *= -1 if bit else 1
    assert y_count % 2 == 0
    return x, sign * (-1 if (y_count // 2) % 2 else 1)


def K_physical(N, k):
    d = 1 << N
    K = zeros(d)
    full = d - 1
    for S in combinations(range(N), k):
        mask = sum(1 << i for i in S)
        outside = full ^ mask
        for x in range(d):
            l = (x & mask).bit_count()
            for y in range(d):
                if (x & outside) == (y & outside) and (y & mask).bit_count() == l:
                    K[x][y] += F(1, choose(N, k) * (k + 1)
                                  * (1 << (N - k)) * choose(k, l))
    return K


def K_pauli(N, k):
    d = 1 << N
    K = zeros(d)
    for word in product(range(4), repeat=N):
        a, b, c = (word.count(v) for v in (1, 2, 3))
        coefficient = pauli_orbit_coefficient(N, k, a, b, c)
        if coefficient:
            for y in range(d):
                x, sign = pauli_action(word, y)
                K[x][y] += coefficient * sign
    return K


def spin_projectors(N):
    d = 1 << N
    J2 = scale(F(3 * N, 4), identity(d))
    for i, j in combinations(range(N), 2):
        for letter in (1, 2, 3):
            word = tuple(letter if t in (i, j) else 0 for t in range(N))
            P = zeros(d)
            for y in range(d):
                x, sign = pauli_action(word, y)
                P[x][y] = sign
            J2 = add(J2, scale(F(1, 2), P))
    energies = [F(N - 2 * b, 2) * F(N - 2 * b + 2, 2)
                for b in range(N // 2 + 1)]
    projectors = []
    for b, e in enumerate(energies):
        P = identity(d)
        for c, ec in enumerate(energies):
            if b != c:
                P = mm(P, scale(1 / (e - ec), add(J2, scale(-ec, identity(d)))))
        projectors.append(P)
    return projectors


def exact_algebra_checks():
    check(sphere_moment(0, 0, 0) == 1)
    check(sphere_moment(2, 0, 0) == F(1, 3))
    check(sphere_moment(2, 2, 0) == F(1, 15))
    physical_cases = 0
    for N in range(1, 5):
        d = 1 << N
        types, columns = pauli_orbit_columns(N)
        check(len(types) == choose(N + 3, 3))
        check(len(columns) == N + 1)
        P = spin_projectors(N)
        dims = spin_dimensions(N)
        check(sum(dims) == d)
        total_P = zeros(d)
        for b, projector in enumerate(P):
            equal(mm(projector, projector), projector)
            check(tr(projector) == dims[b])
            total_P = add(total_P, projector)
        equal(total_P, identity(d))
        for k in range(N + 1):
            K = K_physical(N, k)
            equal(K, K_pauli(N, k))
            check(tr(K) == 1)
            sector = sector_column(N, k)
            check(min(sector) >= 0 and sum(sector) == 1)
            recovered = zeros(d)
            for b, projector in enumerate(P):
                check(tr(mm(projector, K)) == sector[b])
                recovered = add(recovered, scale(sector[b] / dims[b], projector))
            equal(recovered, K)
            physical_cases += 1
        # Verify the Dicke matrix-unit orbit formula independently.
        probs = [F(l + 1, choose(N + 2, 2)) for l in range(N + 1)]
        orbit = block_orbit_coefficients(N, probs)
        check(len(orbit) == choose(N + 3, 3))
        for x in range(d):
            for y in range(d):
                table = [0] * 4
                for i in range(N):
                    table[2 * ((x >> i) & 1) + ((y >> i) & 1)] += 1
                expected = probs[x.bit_count()] / choose(N, x.bit_count()) if x.bit_count() == y.bit_count() else F(0)
                check(orbit[tuple(table)] == expected)
    # Larger sizes use exact compressed data only, never physical enumeration.
    for N in [7, 13, 31, 64]:
        for k in range(N + 1):
            column = sector_column(N, k)
            check(min(column) >= 0)
            check(sum(column) == 1)
        check(sum(spin_dimensions(N)) == 1 << N)
    DETAILS["exact_physical_cases"] = physical_cases
    DETAILS["compressed_sizes"] = [7, 13, 31, 64]


def exact_branch_checks():
    cases = 0
    for N in range(1, 5):
        d = 1 << N
        w = [F(k + 1, choose(N + 2, 2)) for k in range(N + 1)]
        values = [F((t + 1) * (t + 3), 7 * (N + 1)) for t in range(N + 1)]
        X = zeros(d)
        for k in range(N + 1):
            X = add(X, scale(w[k], K_physical(N, k)))
        filtered = zeros(d)
        for x in range(d):
            for y in range(d):
                if x.bit_count() == y.bit_count():
                    filtered[x][y] = X[x][y] * values[x.bit_count()]
                else:
                    check(X[x][y] == 0)
        beta = tr(filtered)
        reconstructed = zeros(d)
        raw_sum = F(0)
        for k in range(N + 1):
            n = N - k
            for u in range(n + 1):
                Z = sum(values[u:u + k + 1])
                raw = w[k] * F(choose(n, u), (k + 1) * (1 << n)) * Z
                raw_sum += raw
                for S in combinations(range(N), k):
                    mask = sum(1 << i for i in S)
                    Sc = tuple(i for i in range(N) if i not in S)
                    outside = (d - 1) ^ mask
                    for one_positions in combinations(Sc, u):
                        ones = sum(1 << i for i in one_positions)
                        for x in range(d):
                            if x & outside != ones:
                                continue
                            l = (x & mask).bit_count()
                            for y in range(d):
                                if y & outside == ones and (y & mask).bit_count() == l:
                                    reconstructed[x][y] += raw / beta / choose(N, k) / choose(n, u) * values[l + u] / Z / choose(k, l)
        check(beta == raw_sum)
        equal(reconstructed, scale(1 / beta, filtered))
        cases += 1
    DETAILS["arbitrary_positive_filter_exact_cases"] = cases


def scalar_and_cutoff_checks():
    scalar_cases = 0
    for bits in [3, 7, 17, 33, 65, 129]:
        for x in [F(0), F(1, 7), F(1, 2), F(1), F(3, 2), F(8, 3), F(10), F(64)]:
            v = exp_neg_dyadic(x, bits)
            with localcontext() as ctx:
                ctx.prec = 120
                truth = (-(Decimal(x.numerator) / Decimal(x.denominator))).exp()
                value = Decimal(v.numerator) / Decimal(v.denominator)
                check(abs(value - truth) <= Decimal(1) / (Decimal(2) ** bits))
            check(0 <= v <= 1)
            check(v.denominator <= 1 << (bits + 1))
            scalar_cases += 1
    huge = F(1 << 256)
    check(exp_neg_dyadic(huge, 129) == 0)
    c = cutoffs(7, huge, F(1, 2), 0, F(1, 1024))
    check(c["mode"] == "top_spin")
    check(c["bounded_generator_norm"] < 10000)
    check(c["gamma"].denominator.bit_length() < 100)
    for h in [huge, -huge]:
        c = cutoffs(7, huge, F(1, 2), h, F(1, 1024))
        check(c["mode"] == "extremal_field")
        check(c["orientation"] == int(h > 0))
    c = cutoffs(16, huge, F(1, 2), F(151, 2), F(1, 1 << 64))
    check(c["mode"] == "top_spin")
    check(c["s"] < 2500)
    check(c["gamma"].denominator.bit_length() < 2600)
    # A rejected promise is retained as a control, not clipped into admission.
    for parameters in [(2, -1, 0, 0, F(1, 8)), (2, 1, F(3, 2), 0, F(1, 8))]:
        try:
            cutoffs(*parameters)
        except ValueError:
            check(True)
        else:
            check(False)
    DETAILS["scalar_enclosure_comparisons"] = scalar_cases
    DETAILS["large_binary_magnitude_bits"] = 257


def exact_lp_checks():
    cases = 0
    for N in range(1, 7):
        columns = [sector_column(N, k) for k in range(N + 1)]
        wtrue = [F(k + 1, choose(N + 2, 2)) for k in range(N + 1)]
        target = matvec(sector_matrix(N), wtrue)
        w, objective = exact_simplex_fixture(target, columns)
        check(objective == 0)
        check(min(w) >= 0 and sum(w) == 1)
        check(matvec(sector_matrix(N), w) == target)
        cases += 1
    columns = [sector_column(2, k) for k in range(3)]
    w, objective = exact_simplex_fixture([F(0), F(1)], columns)
    check(objective == F(3, 4))  # singlet is outside the admitted K_k hull
    check(min(w) >= 0 and sum(w) == 1)
    p = [F(1, 7), F(2, 7), F(4, 7)]
    rounded, bits = round_dyadic_probabilities(p, 1024)
    check(sum(rounded) == 1 and min(rounded) >= 0)
    check(total_variation(p, rounded) <= F(3, 1 << bits))
    DETAILS["exact_simplex_hull_cases"] = cases
    DETAILS["singlet_K_hull_negative_control_TV"] = "3/4"


def rejected_interface_controls():
    rejected = []
    def reject(name, callable_):
        try:
            callable_()
        except (ValueError, AssertionError):
            check(True)
            rejected.append(name)
        else:
            check(False)
    reject("negative_LP_weight", lambda: acquire_k_weights(
        2, F(1), F(1), F(0), F(1, 8),
        lp_backend=lambda q, c: ([F(-1), F(1), F(1)], F(0))))
    reject("false_LP_objective", lambda: acquire_k_weights(
        2, F(1), F(1), F(0), F(1, 8),
        lp_backend=lambda q, c: ([F(1), F(0), F(0)], F(0))))
    reject("unnormalized_Dicke_input", lambda: block_orbit_coefficients(2, [F(1)] * 3))
    reject("negative_branch_weight", lambda: acquire_branches(
        2, F(1), F(0), [F(-1), F(1), F(1)], F(1, 8)))
    reject("subset_rank_out_of_range", lambda: unrank_subset(4, 2, 6))
    check(not qubit_state_is_psd((F(1, 2), F(1, 2), F(1), F(0))))
    check(not qubit_state_is_psd((F(-1), F(2), F(0), F(0))))
    rejected += ["nonPSD_local_state", "negative_local_diagonal"]
    DETAILS["rejected_interface_controls"] = rejected


def combinatorial_sampling_checks():
    subset_count = 0
    for n in range(0, 10):
        for k in range(n + 1):
            expected = list(combinations(range(n), k))
            for rank, combination in enumerate(expected):
                check(unrank_subset(n, k, rank) == combination)
                subset_count += 1
    for M in range(1, 33):
        bits = max(0, ceil_log2(F(128 * M) / F(1, 8)))
        Q = 1 << bits
        def ceiling_div(a, b):
            return (a + b - 1) // b
        probs = [F(ceiling_div((r + 1) * Q, M) - ceiling_div(r * Q, M), Q)
                 for r in range(M)]
        check(sum(probs) == 1)
        check(min(probs) > 0)
        check(total_variation(probs, [F(1, M)] * M) <= F(M, Q))
        check(F(M, Q) <= F(1, 1024))
    DETAILS["exact_subset_unrank_labels"] = subset_count
    DETAILS["rank_bucket_cases"] = 32


class CountedRandom:
    def __init__(self, seed):
        self.rng = random.Random(seed)
        self.bits = 0
    def getrandbits(self, b):
        self.bits += b
        return self.rng.getrandbits(b)


def local_numpy(state):
    d0, d1, re, im = map(float, state)
    return np.array([[d0, re + 1j * im], [re - 1j * im, d1]], dtype=complex)


def tensor_local(local):
    result = np.ones((1, 1), complex)
    # Physical integer convention is little endian.
    for state in reversed(local):
        result = np.kron(result, local_numpy(state))
    return result


def hierarchy_expectation(N, branches, inner):
    d = 1 << N
    result = np.zeros((d, d), complex)
    for branch in branches:
        k, u = branch["k"], branch["u"]
        if not branch["probability"]:
            continue
        for S in combinations(range(N), k):
            Sc = tuple(i for i in range(N) if i not in S)
            for ones in combinations(Sc, u):
                local = [(F(0), F(1), F(0), F(0)) if i in ones
                         else (F(1), F(0), F(0), F(0)) for i in range(N)]
                mixture = inner[(k, u)] if k else [(F(1), (F(1), F(0), F(0), F(0)))]
                for weight, state in mixture:
                    current = list(local)
                    for i in S:
                        current[i] = state
                    result += float(branch["probability"] * weight
                                    / choose(N, k) / choose(N - k, u)) * tensor_local(current)
    return result


def target_numpy(N, alpha, delta, h):
    projectors = spin_projectors(N)
    raw = np.zeros((1 << N, 1 << N), complex)
    for b, P in enumerate(projectors):
        j = N / 2 - b
        coef = exp(float(alpha) * j * (j + 1) / N)
        raw += coef * np.array(P, dtype=float)
    for y in range(1 << N):
        z = y.bit_count() - N / 2
        raw[:, y] *= exp(-float(delta) * z * z / N + float(h) * z)
    return raw / np.trace(raw)


def end_to_end_bounded_fixture():
    records = []
    for case_id, (N, alpha, delta, h) in enumerate([
            (2, F(1, 2), F(1, 2), F(1, 3)),
            (3, F(1, 3), F(1, 2), F(-1, 2)),
            (2, F(1, 2), F(1), F(1, 3)),
            (3, F(1, 3), F(1), F(-1, 2))]):
        eps = F(1, 8)
        w, metadata = acquire_k_weights(N, alpha, delta, h, eps,
                                        lp_backend=exact_simplex_fixture)
        check(min(w) >= 0 and sum(w) == 1)
        check(metadata["LP_objective"] <= metadata["gamma"] / 8)
        check(metadata["weight_rounding_TV"] <= metadata["gamma"] / 16)
        branches, data = acquire_branches(N, delta, h, w, eps)
        check(len(branches) == choose(N + 2, 2))
        check(len(data["N_exponential_values"]) == N + 1)
        check(sum(v["probability"] for v in branches) == 1)
        check(data["outer_rounding_TV"] <= eps / 128)
        inner = {}
        nodes = 0
        for branch in branches:
            check(min(branch["dicke"]) > 0 and sum(branch["dicke"]) == 1)
            if branch["k"]:
                mixture, diagnostics = phase_four_iid_fixture(branch["k"], branch["dicke"], eps / 32)
                inner[(branch["k"], branch["u"])] = mixture
                check(diagnostics["LP_objective"] <= eps / 128)
                check(diagnostics["rounding_TV"] <= eps / 256)
                for weight, state in mixture:
                    check(weight >= 0 and qubit_state_is_psd(state))
                nodes += len(mixture)
        expected = hierarchy_expectation(N, branches, inner)
        target = target_numpy(N, alpha, delta, h)
        T = float(np.sum(np.abs(np.linalg.eigvalsh(expected - target))) / 2)
        check(T < float(eps / 8))
        check(abs(np.trace(expected) - 1) < 1e-12)
        check(np.linalg.eigvalsh(expected).min() > -1e-12)
        rng = CountedRandom(7303 + case_id)
        max_bits = 0
        for trial in range(64):
            before = rng.bits
            local, label = sample_hierarchy(N, branches, inner, eps, rng)
            check(len(local) == N)
            check(all(qubit_state_is_psd(v) for v in local))
            check(len(label["subset"]) == label["k"])
            check(len(label["complement_ones"]) == label["u"])
            check(not set(label["subset"]) & set(label["complement_ones"]))
            max_bits = max(max_bits, rng.bits - before)
        records.append({"N": N, "alpha": str(alpha), "delta": str(delta), "h": str(h),
                        "eps": str(eps), "numeric_uniform_subset_trace_error": T,
                        "scoped_inner_fixture_nodes": nodes, "draws": 64,
                        "maximum_observed_fair_bits_per_draw": max_bits,
                        "scalar_precision_bits": data["scalar_bits"],
                        "generic_iid_backend_executed": False,
                        "bounded_exact_simplex_backend": True})
    DETAILS["end_to_end_scoped_examples"] = records


def serialize(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {str(k): serialize(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [serialize(x) for x in value]
    return value


def main():
    def wall_limit(signum, frame):
        raise TimeoutError("owned bounded fixture exceeded the declared30second wall cap")
    signal.signal(signal.SIGALRM, wall_limit)
    signal.alarm(30)
    started = time.perf_counter()
    for routine in [exact_algebra_checks, exact_branch_checks, scalar_and_cutoff_checks,
                    exact_lp_checks, rejected_interface_controls, combinatorial_sampling_checks,
                    end_to_end_bounded_fixture]:
        routine()
    result = {"status": "PASS", "assertions": ASSERTIONS,
              "elapsed_seconds_shared_machine": time.perf_counter() - started,
              "evidence": DETAILS,
              "proof_scope": "exact acquired formulas plus bounded fixtures; general polynomial compiler imports certified LP and fixed-variable iid theorem",
              "hardware_preparation": "NOT_EXECUTED", "backend_gpu_cost": "UNKNOWN",
              "novelty_priority": "UNKNOWN"}
    signal.alarm(0)
    path = Path(__file__).with_name("axial_acquisition_checks.json")
    path.write_text(json.dumps(serialize(result), indent=2) + "\n")
    print(json.dumps(serialize(result), indent=2))


if __name__ == "__main__":
    main()
