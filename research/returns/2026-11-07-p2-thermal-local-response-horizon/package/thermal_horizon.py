"""Exact finite encodings for the local thermal-response information theorem.

Standard-library only. Fractions are reduced exact rationals. A chain stores
diagonals d and SQUARED hoppings b2; the Hamiltonian hopping is the positive
square root of b2. No exponentially large spin matrix is constructed here.

The acquisition schedule is a mathematical costed Gaussian-channel algorithm.
It does not claim to implement a laboratory imaginary-time measurement.
"""
from fractions import Fraction as Q
from math import comb, factorial, isqrt


def ceilq(x):
    x = Q(x)
    return -((-x.numerator) // x.denominator)


def floorq(x):
    x = Q(x)
    return x.numerator // x.denominator


def ceil_log2(x):
    """Nonnegative integer >= log_2(x), using integer comparisons only."""
    x = Q(x)
    if x <= 1:
        return 0
    k = max(0, x.numerator.bit_length() - x.denominator.bit_length())
    if Q(1 << k) < x:
        k += 1
    return k


def dyadic_floor(x, bits):
    return Q(floorq(Q(x) * (1 << bits)), 1 << bits)


def dyadic_ceil(x, bits):
    return Q(ceilq(Q(x) * (1 << bits)), 1 << bits)


def exp_negative_interval(x, bits):
    """Proved rational enclosure of exp(-x), x>=0, width <=2^-bits.

    Range-reduce to [0,1], use alternating Taylor bounds, and round outward
    after every squaring. Arithmetic precision is O(bits+bit_length(x)).
    """
    x = Q(x)
    if x < 0 or bits < 0:
        raise ValueError("x and bits must be nonnegative")
    if not x:
        return Q(1), Q(1)
    k = ceil_log2(x)
    y = x / (1 << k)
    precision = bits + k + 6
    tolerance = Q(1, 1 << (precision + 2))
    term, total = Q(1), Q(1)
    lower, upper = Q(0), Q(1)
    j = 0
    while True:
        j += 1
        term *= y / j
        total += -term if j & 1 else term
        if j & 1:
            lower = total
        else:
            upper = total
        if upper - lower <= tolerance:
            break
    lower = max(Q(0), dyadic_floor(lower, precision))
    upper = min(Q(1), dyadic_ceil(upper, precision))
    for _ in range(k):
        lower = max(Q(0), dyadic_floor(lower * lower, precision))
        upper = min(Q(1), dyadic_ceil(upper * upper, precision))
    assert 0 <= lower <= upper <= 1
    assert upper - lower <= Q(1, 1 << bits)
    return lower, upper


def exp_negative_dyadic(x, bits):
    lo, hi = exp_negative_interval(x, bits + 4)
    middle = (lo + hi) / 2
    rounded = Q(floorq(middle * (1 << bits) + Q(1, 2)), 1 << bits)
    rounded = min(Q(1), max(Q(0), rounded))
    assert max(abs(rounded - lo), abs(rounded - hi)) <= Q(1, 1 << bits)
    return rounded, (lo, hi)


def pi_interval(bits):
    """Rational Machin-formula bounds; used only to name a binary query time."""
    tolerance = Q(1, 1 << (bits + 6))
    def arctan_bounds(x):
        total, power = Q(0), x
        lower, upper = Q(0), x
        k = 0
        while upper - lower > tolerance:
            term = power / (2 * k + 1)
            total += -term if k & 1 else term
            if k & 1:
                lower = total
            else:
                upper = total
            power *= x * x
            k += 1
        return lower, upper
    a, b = arctan_bounds(Q(1, 5))
    c, d = arctan_bounds(Q(1, 239))
    lo, hi = 16 * a - 4 * d, 16 * b - 4 * c
    assert hi - lo <= Q(1, 1 << bits)
    return lo, hi


def jacobi_from_rational_measure(atoms, weights):
    """Monic three-term recurrence; no numerical diagonalization.

    Returns d_i and b_i^2, exactly rational, and all monic norms. The final
    monic polynomial vanishes at every supplied atom; this is checked exactly.
    """
    atoms, weights = list(map(Q, atoms)), list(map(Q, weights))
    if len(atoms) != len(weights) or not atoms:
        raise ValueError("nonempty matching arrays required")
    if len(set(atoms)) != len(atoms) or any(w <= 0 for w in weights):
        raise ValueError("distinct atoms and strictly positive weights required")
    if sum(weights) != 1:
        raise ValueError("weights must sum to one")
    size = len(atoms)
    previous = [Q(0)] * size
    current = [Q(1)] * size
    previous_norm = None
    diagonal, squared_hoppings, norms = [], [], []
    for k in range(size):
        norm = sum(w * p * p for w, p in zip(weights, current))
        assert norm > 0
        d = sum(w * x * p * p for w, x, p in zip(weights, atoms, current)) / norm
        b2 = Q(0) if k == 0 else norm / previous_norm
        diagonal.append(d)
        norms.append(norm)
        if k:
            squared_hoppings.append(b2)
        following = [(x - d) * p - b2 * old
                     for x, p, old in zip(atoms, current, previous)]
        previous, current = current, following
        previous_norm = norm
    assert all(p == 0 for p in current)
    return {"diagonal": diagonal, "squared_hoppings": squared_hoppings,
            "monic_norms": norms}


def polynomial_mul_linear(poly, root):
    out = [Q(0)] * (len(poly) + 1)
    for k, c in enumerate(poly):
        out[k] -= root * c
        out[k + 1] += c
    return out


def characteristic_polynomial(chain):
    previous, current = [Q(0)], [Q(1)]
    for k, d in enumerate(chain["diagonal"]):
        following = polynomial_mul_linear(current, d)
        if k:
            b2 = chain["squared_hoppings"][k - 1]
            for j, c in enumerate(previous):
                following[j] -= b2 * c
        previous, current = current, following
    return current


def endpoint_moments(chain, count):
    """Use a rational matrix similar to the symmetric Jacobi matrix."""
    d, b2 = chain["diagonal"], chain["squared_hoppings"]
    v = [Q(1)] + [Q(0)] * (len(d) - 1)
    out = []
    for _ in range(count):
        out.append(v[0])
        v = [d[i] * v[i] + (b2[i - 1] * v[i - 1] if i else 0)
             + (v[i + 1] if i + 1 < len(d) else 0)
             for i in range(len(d))]
    return out


def construct_pair(n, beta=Q(1), omega=Q(1), background="binomial"):
    """Construct a polynomial-description isospectral pair and certificates."""
    beta, omega = Q(beta), Q(omega)
    if n < 1 or beta <= 0 or omega <= 0:
        raise ValueError("n>=1, beta>0, omega>0 required")
    if background not in ("binomial", "uniform"):
        raise ValueError("background must be binomial or uniform")
    if background == "uniform" and n % 2 != 1:
        raise ValueError("the uniform-background theorem uses odd n")
    h = 2 * omega / (4 * n + 1)
    atoms = [omega * Q(2 * n + 1 + 2 * j, 4 * n + 1) for j in range(n + 1)]
    base = [Q(comb(n, j), 1 << n) for j in range(n + 1)]
    delta = (beta * omega / (4 * n + 1)) ** n
    gamma0 = beta * omega / (4 + beta * omega)
    xi = min(delta / 64, gamma0 / 64, Q(1, 32))
    precision = ceil_log2(1 / xi)
    exponentials, enclosures = [], []
    for atom in atoms:
        r, interval = exp_negative_dyadic(beta * atom, precision)
        exponentials.append(r)
        enclosures.append(interval)
    pair = []
    for sign in (1, -1):
        if background == "binomial":
            mu = [w * (1 + Q(sign * (-1) ** j, 2)) for j, w in enumerate(base)]
        else:
            mu = [Q(1, 2 * (n + 1)) + w * Q(1 + sign * (-1) ** j, 2)
                  for j, w in enumerate(base)]
        unnormalized = [p * (1 + r) for p, r in zip(mu, exponentials)]
        normalizer = sum(unnormalized)
        weights = [w / normalizer for w in unnormalized]
        chain = jacobi_from_rational_measure(atoms, weights)
        chain.update({"sign": sign, "weights": weights, "original_mu": mu})
        pair.append(chain)
    pi_bits = ceil_log2(64 * omega / (h * gamma0))
    pi_lo, pi_hi = pi_interval(pi_bits)
    time_lo, time_hi = pi_lo / h, pi_hi / h
    time_bits = ceil_log2(64 * omega / gamma0)
    time = Q(floorq((time_lo + time_hi) * (1 << time_bits) / 2 + Q(1, 2)),
             1 << time_bits)
    time_error = max(abs(time - time_lo), abs(time - time_hi))
    assert time_error <= gamma0 / (16 * omega)
    return {"n": n, "sites": n + 1, "background": background,
            "beta": beta, "omega": omega,
            "h": h, "atoms": atoms, "base_weights": base, "delta": delta,
            "gamma0": gamma0, "xi": xi, "precision_bits": precision,
            "exponentials": exponentials, "exponential_enclosures": enclosures,
            "rational_query_time": time, "query_time_error_bound": time_error,
            "pair": pair}


def thermal_kernel_interval(atom, tau, beta=Q(1), bits=100):
    atom, tau, beta = Q(atom), Q(tau), Q(beta)
    if not (0 <= tau <= beta):
        raise ValueError("imaginary time outside the thermal interval")
    a, b = exp_negative_interval(tau * atom, bits)
    c, d = exp_negative_interval((beta - tau) * atom, bits)
    e, f = exp_negative_interval(beta * atom, bits)
    return (a + c) / (1 + f), min(Q(1), (b + d) / (1 + e))


def correlator_interval(atoms, weights, tau, beta=Q(1), bits=100):
    intervals = [thermal_kernel_interval(x, tau, beta, bits) for x in atoms]
    return (sum(w * a for w, (a, _) in zip(weights, intervals)),
            sum(w * b for w, (_, b) in zip(weights, intervals)))


def response_at_alignment_interval(model, chain_index, bits=120):
    """R(pi/h), using exact sin(omega_j*pi/h)=(-1)^(n+j)."""
    lo, hi = Q(0), Q(0)
    for j, (x, w) in enumerate(zip(model["atoms"], model["pair"][chain_index]["weights"])):
        a, b = exp_negative_interval(model["beta"] * x, bits)
        left, right = (1 - b) / (1 + b), (1 - a) / (1 + a)
        if (model["n"] + j) & 1:
            left, right = -right, -left
        lo += w * left
        hi += w * right
    return lo, hi


def acquisition_schedule(T, epsilon, confidence_failure, beta=Q(1),
                         omega=Q(1), variance=Q(1)):
    """Finite schedule, exact remainder bound, and finite readout cost.

    Each setting uses r independent ideal Gaussian readings before bounded
    clipping/quantization. Split failure allowance equally between mean tails
    and clipping tails. Settings and digit errors fit the deterministic eta.
    """
    T, epsilon, alpha, beta, omega, variance = map(
        Q, (T, epsilon, confidence_failure, beta, omega, variance))
    if T < 0 or not (0 < epsilon < 1) or not (0 < alpha < Q(1, 2)):
        raise ValueError("invalid horizon, accuracy, or confidence")
    if min(beta, omega, variance) <= 0:
        raise ValueError("positive beta, bandwidth, variance required")
    radius = beta + T
    degree_plus_one = 2
    remainder = (omega * radius) ** 2 / 2
    while remainder > epsilon / 4:
        degree_plus_one += 1
        remainder *= omega * radius / degree_plus_one
    m = degree_plus_one - 1
    amplification = (2 * m * radius / beta) ** m / factorial(m)
    eta = epsilon / (4 * amplification)
    tail_log_bound = ceil_log2(4 * (m + 1) / alpha)
    repeats = max(1, ceilq(8 * variance * tail_log_bound / eta ** 2))
    total_reads = repeats * (m + 1)
    clipping_log_bound = ceil_log2(4 * total_reads / alpha)
    clipping_square = ceilq(2 * variance * clipping_log_bound)
    clip_bound = 2 + isqrt(clipping_square)
    quantization_bits = ceil_log2(4 / eta)
    assert Q(1, 1 << quantization_bits) <= eta / 4
    return {"T": T, "epsilon": epsilon, "confidence_failure": alpha,
            "beta": beta, "omega": omega, "variance": variance,
            "degree": m, "nodes": [beta * j / m for j in range(m + 1)],
            "remainder_bound": remainder, "amplification_bound": amplification,
            "node_error_budget": eta, "repeats_per_node": repeats,
            "total_raw_reads": total_reads, "clip_bound": clip_bound,
            "quantization_bits": quantization_bits,
            "maximum_setting_error": eta / (4 * omega),
            "uniform_error_certificate": remainder + amplification * eta}


def interpolate_power_coefficients(nodes, values):
    """Exact rational Newton interpolation expanded in powers of z."""
    nodes, values = list(map(Q, nodes)), list(map(Q, values))
    if len(nodes) != len(values) or len(set(nodes)) != len(nodes):
        raise ValueError("matching distinct nodes required")
    divided = values[:]
    for order in range(1, len(nodes)):
        for j in range(len(nodes) - 1, order - 1, -1):
            divided[j] = (divided[j] - divided[j - 1]) / (nodes[j] - nodes[j - order])
    coefficients = [Q(0)] * len(nodes)
    basis = [Q(1)]
    for j, a in enumerate(divided):
        for k, b in enumerate(basis):
            coefficients[k] += a * b
        basis = polynomial_mul_linear(basis, nodes[j])
    return coefficients


def compile_response_record(schedule, node_estimates):
    """Valid under the schedule's simultaneous node-error event."""
    coefficients = interpolate_power_coefficients(schedule["nodes"], node_estimates)
    response = [Q(0)] * len(coefficients)
    for k in range(1, len(coefficients), 2):
        response[k] = -((-1) ** ((k - 1) // 2)) * coefficients[k]
    return {"response_coefficients": response,
            "uniform_error_certificate": schedule["uniform_error_certificate"],
            "horizon": schedule["T"],
            "condition": "all node means within the declared node_error_budget"}


def evaluate_record(record, time):
    time = Q(time)
    if not 0 <= time <= record["horizon"]:
        raise ValueError("outside the certified horizon")
    value = Q(0)
    for a in reversed(record["response_coefficients"]):
        value = value * time + a
    return value


def consume_quantized_readings(schedule, readings):
    """Perform exactly the charged finite reading/averaging operation.

    `readings` must supply one already clipped/digitized rational observation
    per charged raw query, in node-major order, under the declared noise and
    calibration contract. This routine neither generates nor acquires them.
    """
    stream = iter(readings)
    means = []
    r = schedule["repeats_per_node"]
    scale = 1 << schedule["quantization_bits"]
    cap = schedule["clip_bound"]
    for _ in schedule["nodes"]:
        total = 0
        for _ in range(r):
            sample = Q(next(stream))
            scaled = sample * scale
            if scaled.denominator != 1 or abs(sample) > cap:
                raise ValueError("readout violates its finite digit/range contract")
            total += scaled.numerator
        means.append(Q(total, r * scale))
    return compile_response_record(schedule, means)


def rational_json(value):
    if isinstance(value, Q):
        return str(value)
    if isinstance(value, dict):
        return {k: rational_json(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [rational_json(v) for v in value]
    return value
