"""Exact acquired data for the axial ensemble compiler.

The uniform polynomial compiler imports a certified Turing LP implementation
and the audited fixed-variable iid recovery theorem.  This file implements
the acquired rational data, precision, rounding, and sampling.  The explicit
SymPy simplex helpers are bounded evidence, not polynomial-time backends.
"""
from fractions import Fraction as F
from math import comb
from itertools import combinations


def choose(n, k):
    return comb(n, k) if 0 <= k <= n else 0


def ceil_fraction(x):
    x = F(x)
    return -((-x.numerator) // x.denominator)


def ceil_log2(x):
    """Smallest integer b with 2**b >= positive rational x."""
    x = F(x)
    if x <= 0:
        raise ValueError("positive argument required")
    b = x.numerator.bit_length() - x.denominator.bit_length()
    def pow2(k):
        return F(1 << k) if k >= 0 else F(1, 1 << (-k))
    while pow2(b) < x:
        b += 1
    while pow2(b - 1) >= x:
        b -= 1
    return b


def odd_double_factorial(n):
    result = 1
    for v in range(n, 0, -2):
        result *= v
    return result


def sphere_moment(a, b, c):
    if min(a, b, c) < 0:
        raise ValueError("nonnegative counts required")
    if a % 2 or b % 2 or c % 2:
        return F(0)
    return F(odd_double_factorial(a - 1) * odd_double_factorial(b - 1)
             * odd_double_factorial(c - 1), odd_double_factorial(a + b + c + 1))


def pauli_orbit_coefficient(N, k, a, b, c):
    r = a + b + c
    if not 0 <= k <= N or r > N:
        raise ValueError("invalid sizes")
    if r > k:
        return F(0)
    return F(choose(N - r, k - r), (1 << N) * choose(N, k)) * sphere_moment(a, b, c)


def pauli_orbit_columns(N):
    types = [(N - a - b - c, a, b, c)
             for a in range(N + 1) for b in range(N - a + 1)
             for c in range(N - a - b + 1)]
    return types, [[pauli_orbit_coefficient(N, k, *t[1:]) for t in types]
                   for k in range(N + 1)]


def spin_dimensions(N):
    return [(N - 2 * b + 1) * (choose(N, b) - choose(N, b - 1))
            for b in range(N // 2 + 1)]


def sector_column(N, k):
    return [F((N - 2 * b + 1)
              * (choose(N - k, b) - choose(N - k, b - k - 1)),
              (k + 1) * (1 << (N - k))) for b in range(N // 2 + 1)]


def sector_matrix(N):
    columns = [sector_column(N, k) for k in range(N + 1)]
    return [[col[b] for col in columns] for b in range(N // 2 + 1)]


def exp_neg_dyadic(x, precision_bits):
    """0<=v<=1 rational, |v-exp(-x)|<=2^-precision_bits, no float."""
    x = F(x)
    b = int(precision_bits)
    if x < 0 or b < 1:
        raise ValueError("x>=0 and positive precision required")
    if x == 0:
        return F(1)
    if x >= b + 1:
        return F(0)
    r = 8 * (ceil_fraction(x) + b + 4)
    term = total = F(1)
    for j in range(1, r + 1):
        term *= x / j
        total += term
    denominator = 1 << (b + 1)
    numerator = denominator * total.denominator // total.numerator
    return F(numerator, denominator)


def cutoffs(N, alpha, delta, h, eps, admitted_floor=F(1)):
    alpha, delta, h, eps = map(F, (alpha, delta, h, eps))
    if N < 1 or alpha < 0 or not 0 <= delta <= admitted_floor or not 0 < eps < 1:
        raise ValueError("outside the explicitly admitted interface")
    p = max(0, ceil_log2(1 / eps))
    q = ceil_log2(F(128 * (N + 1)) / eps)
    if abs(h) >= delta + q:
        return {"mode": "extremal_field", "orientation": int(h > 0),
                "p": p, "q": q, "error_bound": eps / 64}
    C = delta * N / 4 + abs(h) * N
    s = ceil_fraction(2 * C)
    gamma = eps / (1 << (s + 8))
    A = N + s + p + 10
    return {"mode": "top_spin" if alpha >= A else "fit",
            "p": p, "q": q, "C": C, "s": s, "gamma": gamma,
            "alpha_cutoff": A, "bounded_generator_norm": A * F(N + 2, 4)}


def isotropic_sector_vector(N, alpha, gamma):
    alpha, gamma = F(alpha), F(gamma)
    tau = gamma / (1 << (N + 4))
    b = max(1, ceil_log2(1 / tau))
    dims = spin_dimensions(N)
    values = [exp_neg_dyadic(alpha * r * F(N + 1 - r, N), b)
              for r in range(N // 2 + 1)]
    raw = [dim * value for dim, value in zip(dims, values)]
    Z = sum(raw)
    assert Z >= N + 1
    return [v / Z for v in raw], {"bits": b, "tau_bound": F(1, 1 << b),
                                 "normalizer": Z, "values": values}


def total_variation(p, q):
    return sum((abs(F(a) - F(b)) for a, b in zip(p, q)), F(0)) / 2


def matvec(A, w):
    return [sum((v * x for v, x in zip(row, w)), F(0)) for row in A]


def round_dyadic_probabilities(p, requested_denominator):
    p = list(map(F, p))
    if not p or min(p) < 0 or sum(p) != 1:
        raise ValueError("positive simplex vector required")
    b = max(0, ceil_log2(F(requested_denominator)))
    Q = 1 << b
    nums = [(x.numerator * Q) // x.denominator for x in p[:-1]]
    nums.append(Q - sum(nums))
    return [F(x, Q) for x in nums], b


def exact_simplex_fixture(qhat, columns):
    """Bounded rational LP fixture; simplex worst-case time NOT claimed poly."""
    from sympy import Rational
    from sympy.solvers.simplex import linprog
    def rational(x):
        x = F(x)
        return Rational(x.numerator, x.denominator)
    def fraction(x):
        return F(int(x.p), int(x.q)) if hasattr(x, "p") else F(x)
    qhat = list(map(F, qhat))
    M, K = len(qhat), len(columns)
    A = [[columns[k][b] for k in range(K)] for b in range(M)]
    rows, rhs = [], []
    for b in range(M):
        for sign in (1, -1):
            rows.append([rational(sign * x) for x in A[b]]
                        + [rational(-int(c == b)) for c in range(M)])
            rhs.append(rational(sign * qhat[b]))
    objective = [0] * K + [Rational(1, 2)] * M
    optimum, solution = linprog(objective, rows, rhs,
                                A_eq=[[1] * K + [0] * M], b_eq=[1],
                                bounds=[(0, 1)] * K + [(0, 4)] * M)
    w = [fraction(v) for v in solution[:K]]
    residuals = [fraction(v) for v in solution[K:]]
    assert min(w) >= 0 and sum(w) == 1
    objective_exact = total_variation(qhat, matvec(A, w))
    assert objective_exact == fraction(optimum)
    assert all(t >= abs(q - a) for t, q, a in zip(residuals, qhat, matvec(A, w)))
    return w, objective_exact


def acquire_k_weights(N, alpha, delta, h, eps, lp_backend=None):
    """LP backend(qhat, columns)->(exact feasible w, rational objective)."""
    metadata = cutoffs(N, alpha, delta, h, eps)
    if metadata["mode"] == "extremal_field":
        return None, metadata
    gamma = metadata["gamma"]
    if F(alpha) == 0:
        return [F(int(k == 0)) for k in range(N + 1)], metadata
    if metadata["mode"] == "top_spin":
        return [F(int(k == N)) for k in range(N + 1)], metadata
    qhat, scalar_data = isotropic_sector_vector(N, alpha, gamma)
    columns = [sector_column(N, k) for k in range(N + 1)]
    if lp_backend is None:
        raise NotImplementedError("supply the charged rational Turing LP backend")
    w, objective = lp_backend(qhat, columns)
    w = list(map(F, w))
    if len(w) != N + 1 or min(w) < 0 or sum(w) != 1:
        raise ValueError("LP backend did not return exactly feasible weights")
    objective_check = total_variation(qhat, matvec(sector_matrix(N), w))
    if F(objective) != objective_check or objective_check > gamma / 8:
        raise ValueError("LP backend did not meet the certified objective contract")
    rounded, bits = round_dyadic_probabilities(w, F(16 * (N + 1)) / gamma)
    metadata.update({"sector_input": qhat, "LP_objective": objective_check,
                     "weight_rounding_TV": total_variation(w, rounded),
                     "weight_bits": bits, "scalar_data": scalar_data})
    return rounded, metadata


def block_orbit_coefficients(k, p):
    p = list(map(F, p))
    if len(p) != k + 1 or min(p) < 0 or sum(p) != 1:
        raise ValueError("normalized Dicke probabilities required")
    result = {}
    for m00 in range(k + 1):
        for m01 in range(k - m00 + 1):
            for m10 in range(k - m00 - m01 + 1):
                m11 = k - m00 - m01 - m10
                key = (m00, m01, m10, m11)
                result[key] = (p[m11 + m10] / choose(k, m11 + m10)
                               if m01 == m10 else F(0))
    return result


def acquire_branches(N, delta, h, w, eps):
    delta, h, eps = map(F, (delta, h, eps))
    w = list(map(F, w))
    if len(w) != N + 1 or min(w) < 0 or sum(w) != 1:
        raise ValueError("exact nonnegative K_k weights required")
    C = delta * N / 4 + N * abs(h)
    s = ceil_fraction(2 * C)
    gamma = eps / (1 << (s + 8))
    bits = max(1, ceil_log2(1 / gamma))
    H = abs(h) * N / 2
    values = []
    for t in range(N + 1):
        z = F(2 * t - N, 2)
        x = H + delta * z * z / N - h * z
        value = exp_neg_dyadic(x, bits)
        assert value > 0
        values.append(value)
    prefix = [F(0)]
    for v in values:
        prefix.append(prefix[-1] + v)
    branches = []
    for k in range(N + 1):
        n = N - k
        for u in range(n + 1):
            Z = prefix[u + k + 1] - prefix[u]
            raw = w[k] * F(choose(n, u), (k + 1) * (1 << n)) * Z
            probs = [v / Z for v in values[u:u + k + 1]]
            branches.append({"k": k, "u": u, "m": F(2 * u - n, 2),
                             "Z": Z, "raw": raw, "dicke": probs})
    normalizer = sum(v["raw"] for v in branches)
    assert normalizer > 0
    original = [v["raw"] / normalizer for v in branches]
    rounded, outer_bits = round_dyadic_probabilities(original,
                                                    F(128 * len(branches)) / eps)
    for branch, weight in zip(branches, rounded):
        branch["probability"] = weight
    return branches, {"N_exponential_values": values, "scalar_bits": bits,
                      "s": s, "gamma": gamma, "scaled_normalizer": normalizer,
                      "outer_bits": outer_bits,
                      "outer_rounding_TV": total_variation(original, rounded)}


def qubit_state_is_psd(state):
    d0, d1, re, im = map(F, state)
    return d0 >= 0 and d1 >= 0 and d0 + d1 == 1 and d0 * d1 >= re * re + im * im


def sample_dyadic(weights, rng):
    weights = list(map(F, weights))
    if min(weights) < 0 or sum(weights) != 1:
        raise ValueError("dyadic simplex vector required")
    for v in weights:
        if v.denominator & (v.denominator - 1):
            raise ValueError("dyadic denominator required")
    bits = max(v.denominator.bit_length() - 1 for v in weights)
    Q = 1 << bits
    draw = rng.getrandbits(bits) if bits else 0
    cumulative = 0
    for i, weight in enumerate(weights):
        cumulative += weight.numerator * (Q // weight.denominator)
        if draw < cumulative:
            return i
    raise AssertionError("simplex interval lookup failed")


def bounded_uniform_rank(M, eps, rng):
    if M < 1:
        raise ValueError("nonempty rank range required")
    if M == 1:
        return 0
    bits = max(0, ceil_log2(F(128 * M) / F(eps)))
    Q = 1 << bits
    U = rng.getrandbits(bits)
    return (M * U) // Q


def unrank_subset(n, k, rank):
    if not 0 <= k <= n or not 0 <= rank < choose(n, k):
        raise ValueError("invalid subset rank")
    result = []
    for i in range(n):
        if not k:
            break
        first = choose(n - i - 1, k - 1)
        if rank < first:
            result.append(i)
            k -= 1
        else:
            rank -= first
    assert k == 0 and rank == 0
    return tuple(result)


def sample_hierarchy(N, branches, inner_mixtures, eps, rng):
    """Each inner mixture consists of (dyadic_weight, rational_qubit_state)."""
    outer = sample_dyadic([b["probability"] for b in branches], rng)
    branch = branches[outer]
    k, u = branch["k"], branch["u"]
    S = unrank_subset(N, k, bounded_uniform_rank(choose(N, k), eps, rng))
    Sc = tuple(i for i in range(N) if i not in S)
    ones_positions = unrank_subset(N - k, u,
                                  bounded_uniform_rank(choose(N - k, u), eps, rng))
    ones = {Sc[i] for i in ones_positions}
    local = [(F(0), F(1), F(0), F(0)) if i in ones
             else (F(1), F(0), F(0), F(0)) for i in range(N)]
    inner_label = None
    if k:
        mixture = inner_mixtures[(k, u)]
        inner_label = sample_dyadic([v[0] for v in mixture], rng)
        state = mixture[inner_label][1]
        assert qubit_state_is_psd(state)
        for i in S:
            local[i] = state
    return local, {"outer_label": outer, "k": k, "u": u, "subset": S,
                   "complement_ones": tuple(sorted(ones)), "inner_label": inner_label}


def phase_four_iid_fixture(k, dicke_probabilities, error_budget):
    """Bounded k<=3 rational pure-node diagnostic; not the generic iid oracle."""
    if not 1 <= k <= 3:
        raise ValueError("phase-four bounded fixture admits only k=1,2,3")
    parameters = {F(0), F(1)}
    for numerator in range(1, 33):
        t = F(numerator, 8)
        parameters.add(t)
        parameters.add(1 / t)
    parameter_list = sorted(parameters) + [None]
    xs = [F(1) if t is None else t * t / (1 + t * t) for t in parameter_list]
    columns = [[F(choose(k, l)) * x ** l * (1 - x) ** (k - l)
                for l in range(k + 1)] for x in xs]
    weights, objective = exact_simplex_fixture(dicke_probabilities, columns)
    if objective > F(error_budget) / 4:
        raise ValueError("bounded fixture net did not reach the requested error")
    mixture = []
    for t, x, w in zip(parameter_list, xs, weights):
        if not w:
            continue
        off = F(0) if t is None else t / (1 + t * t)
        for re, im in [(off, F(0)), (F(0), off), (-off, F(0)), (F(0), -off)]:
            state = (1 - x, x, re, im)
            assert qubit_state_is_psd(state)
            mixture.append((w / 4, state))
    rounded, bits = round_dyadic_probabilities([v[0] for v in mixture],
                                              F(8 * len(mixture)) / F(error_budget))
    final = [(w, v[1]) for w, v in zip(rounded, mixture)]
    return final, {"LP_objective": objective, "rounding_TV": total_variation(
        [v[0] for v in mixture], rounded), "bits": bits, "nodes": len(mixture)}


def acquire_zero_field_probabilities(N, k, delta, eta):
    """Target for one zero-field iid recovery call at each k."""
    if not 1 <= k <= N:
        raise ValueError("nonempty subset size required")
    delta, eta = F(delta), F(eta)
    s0 = ceil_fraction(delta * k * k / (2 * N))
    tau0 = eta / (1 << (s0 + 4))
    bits = max(1, ceil_log2(1 / tau0))
    raw = [exp_neg_dyadic(delta * F(2 * l - k, 2) ** 2 / N, bits)
           for l in range(k + 1)]
    assert min(raw) > 0
    Z = sum(raw)
    return [v / Z for v in raw], {"s0": s0, "bits": bits,
                                 "acquisition_TV_bound": eta / 16}


def tilt_iid_mixture(N, k, hprime, Hcap, mixture, eps):
    """Exact rational local tilt of an acquired base iid mixture, then dyadic weights."""
    hprime, Hcap, eps = map(F, (hprime, Hcap, eps))
    if not 1 <= k <= N or abs(hprime) > Hcap:
        raise ValueError("invalid shared field cap")
    B = ceil_fraction(2 * N * Hcap)
    eta = eps / (1 << (B + 10))
    tauD = eta / (N + 1)
    bits = max(1, ceil_log2(1 / tauD))
    if hprime >= 0:
        D0, D1 = exp_neg_dyadic(hprime / 2, bits), F(1)
    else:
        D0, D1 = F(1), exp_neg_dyadic(-hprime / 2, bits)
    assert min(D0, D1) > 0
    atoms, raw = [], []
    for weight, state in mixture:
        d0, d1, re, im = map(F, state)
        assert qubit_state_is_psd(state)
        a = D0 * D0 * d0 + D1 * D1 * d1
        assert a > 0
        atom = (D0 * D0 * d0 / a, D1 * D1 * d1 / a,
                D0 * D1 * re / a, D0 * D1 * im / a)
        assert qubit_state_is_psd(atom)
        atoms.append(atom)
        raw.append(F(weight) * a ** k)
    Z = sum(raw)
    assert Z > 0
    weights = [v / Z for v in raw]
    rounded, draw_bits = round_dyadic_probabilities(weights,
                                                    F(128 * len(atoms)) / eps)
    return list(zip(rounded, atoms)), {"B": B, "eta": eta,
                                       "filter_bits": bits,
                                       "weight_bits": draw_bits,
                                       "weight_rounding_TV": total_variation(weights, rounded),
                                       "exact_rational_filter": (D0, D1)}


def symmetric_octahedron_fixture(k, p, error_budget):
    """Direct exact zero-field witness at k<=3, no optimization backend."""
    p = list(map(F, p))
    if not 1 <= k <= 3 or len(p) != k + 1 or sum(p) != 1 or p != p[::-1]:
        raise ValueError("symmetric low-N Dicke fixture required")
    if k == 1:
        equator, pole = F(1), F(0)
    elif k == 2:
        equator, pole = 2 * p[1], p[0] - p[1] / 2
    else:
        equator, pole = 8 * p[1] / 3, p[0] - p[1] / 3
    if min(equator, pole) < 0:
        raise ValueError("outside the direct octahedral witness cone")
    equatorial = [(F(1, 2), F(1, 2), F(1, 2), F(0)),
                  (F(1, 2), F(1, 2), F(0), F(1, 2)),
                  (F(1, 2), F(1, 2), F(-1, 2), F(0)),
                  (F(1, 2), F(1, 2), F(0), F(-1, 2))]
    mixture = [(equator / 4, state) for state in equatorial]
    mixture += [(pole, (F(1), F(0), F(0), F(0))),
                (pole, (F(0), F(1), F(0), F(0)))]
    reconstructed = [equator * F(choose(k, l), 1 << k)
                     + pole * int(l == 0) + pole * int(l == k)
                     for l in range(k + 1)]
    assert reconstructed == p
    rounded, bits = round_dyadic_probabilities([v[0] for v in mixture],
                                              F(8 * len(mixture)) / F(error_budget))
    return [(weight, item[1]) for weight, item in zip(rounded, mixture)], {
        "population_L1_error_before_rounding": F(0),
        "rounding_TV": total_variation([v[0] for v in mixture], rounded),
        "bits": bits, "nodes": len(mixture), "optimization_executed": False}
