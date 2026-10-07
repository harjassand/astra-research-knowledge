"""Exact normalized filtered columns and outward compressed posterior metrics.

These helpers do not invoke a numerical LP or a quantum optimizer.  They
verify the actual rational candidate with true exponential enclosures.
"""
from fractions import Fraction as F
from axial_acquisition import (sector_matrix, spin_dimensions, matvec,
                                exp_neg_dyadic, ceil_log2, choose,
                                round_dyadic_probabilities)


def simplex(v):
    v = list(map(F, v))
    if not v or min(v) < 0 or sum(v) != 1:
        raise ValueError("exact nonnegative rational simplex required")
    return v


def exp_neg_enclosure(x, bits):
    x = F(x)
    if x < 0:
        raise ValueError("negative exponential argument required")
    if x == 0:
        return F(1), F(1)
    value = exp_neg_dyadic(x, bits + 2)
    error = F(1, 1 << (bits + 2))
    return max(F(0), value - error), min(F(1), value + error)


def interval_sum(terms, weights=None):
    terms = list(terms)
    weights = [F(1)] * len(terms) if weights is None else list(map(F, weights))
    if len(weights) != len(terms) or min(weights, default=0) < 0:
        raise ValueError("nonnegative interval combination required")
    return (sum((w * t[0] for w, t in zip(weights, terms)), F(0)),
            sum((w * t[1] for w, t in zip(weights, terms)), F(0)))


def positive_interval_product(a, b):
    if min(a[0], b[0]) < 0 or a[1] < a[0] or b[1] < b[0]:
        raise ValueError("valid nonnegative intervals required")
    return a[0] * b[0], a[1] * b[1]


def positive_normalize(raw):
    total = interval_sum(raw)
    if total[0] <= 0:
        raise ValueError("normalizer lower endpoint is not positive")
    return [(max(F(0), lo / total[1]), min(F(1), hi / total[0]))
            for lo, hi in raw], total


def interval_TV_upper(a, b):
    if len(a) != len(b):
        raise ValueError("matching vector dimensions required")
    return sum((max(abs(x[0] - y[1]), abs(x[1] - y[0]))
                for x, y in zip(a, b)), F(0)) / 2


def scaled_filter_values(N, delta, h, bits):
    delta, h = F(delta), F(h)
    if N < 1 or not 0 <= delta <= 1:
        raise ValueError("current admitted domain is N>=1,delta<=1")
    H = abs(h) * N / 2
    values, intervals = [], []
    for t in range(N + 1):
        m = F(2 * t - N, 2)
        x = H + delta * m * m / N - h * m
        if x < 0:
            raise AssertionError("global exponent shift was not an upper bound")
        values.append(exp_neg_dyadic(x, bits))
        intervals.append(exp_neg_enclosure(x, bits))
    return values, intervals


def filtered_sector_columns(N, filter_values):
    f = list(map(F, filter_values))
    if len(f) != N + 1 or min(f) < 0 or max(f) > 1:
        raise ValueError("scaled nonnegative magnetization grid required")
    A = sector_matrix(N)
    c = [sum(f[b:N - b + 1]) / (N - 2 * b + 1) for b in range(N // 2 + 1)]
    Z = [sum((A[b][k] * c[b] for b in range(len(c))), F(0))
         for k in range(N + 1)]
    if min(Z) <= 0:
        raise ValueError("all filtered K normalizers must be positive")
    C = [[A[b][k] * c[b] / Z[k] for k in range(N + 1)] for b in range(len(c))]
    assert all(sum(C[b][k] for b in range(len(c))) == 1 for k in range(N + 1))
    return C, c, Z


def filtered_isotropic_target(N, alpha, filter_values, bits):
    alpha = F(alpha)
    if alpha < 0:
        raise ValueError("ferromagnetic alpha>=0 required")
    _, c, _ = filtered_sector_columns(N, filter_values)
    dims = spin_dimensions(N)
    r = [exp_neg_dyadic(alpha * b * F(N + 1 - b, N), bits)
         for b in range(len(c))]
    raw = [D * v * cb for D, v, cb in zip(dims, r, c)]
    Z = sum(raw)
    if Z <= 0:
        raise ValueError("target normalizer is not positive")
    return [v / Z for v in raw]


def backconvert_filtered_weights(v, Z):
    """Optional practical conversion; certify actual returned w, not fitted v."""
    v, Z = simplex(v), list(map(F, Z))
    if len(v) != len(Z) or min(Z) <= 0:
        raise ValueError("positive filtered normalizers required")
    raw = [weight / normalizer for weight, normalizer in zip(v, Z)]
    denominator = sum(raw)
    return [v / denominator for v in raw]


def filtered_posterior(N, alpha, delta, h, bits, *, isotropic_weights=None,
                       direct_filtered_weights=None):
    """Outward full trace-distance certificate via the shared true filter."""
    if (isotropic_weights is None) == (direct_filtered_weights is None):
        raise ValueError("supply exactly one actual candidate interface")
    alpha = F(alpha)
    if alpha < 0:
        raise ValueError("alpha>=0 required")
    values, fiv = scaled_filter_values(N, delta, h, bits)
    A = sector_matrix(N)
    civ = []
    for b in range(N // 2 + 1):
        lo, hi = interval_sum(fiv[b:N - b + 1])
        civ.append((lo / (N - 2 * b + 1), hi / (N - 2 * b + 1)))
    dims = spin_dimensions(N)
    riv = [exp_neg_enclosure(alpha * b * F(N + 1 - b, N), bits)
           for b in range(len(civ))]
    target_raw = [positive_interval_product(r, c) for r, c in zip(riv, civ)]
    target_raw = [(lo * D, hi * D) for (lo, hi), D in zip(target_raw, dims)]
    target, target_Z = positive_normalize(target_raw)
    if isotropic_weights is not None:
        w = simplex(isotropic_weights)
        if len(w) != N + 1:
            raise ValueError("wrong K-weight count")
        a = matvec(A, w)
        candidate_raw = [(x * lo, x * hi) for x, (lo, hi) in zip(a, civ)]
        candidate, candidate_Z = positive_normalize(candidate_raw)
        interface = "actual rational isotropic w"
    else:
        v = simplex(direct_filtered_weights)
        if len(v) != N + 1:
            raise ValueError("wrong filtered-weight count")
        columns = []
        candidate_Z = []
        for k in range(N + 1):
            raw = [(A[b][k] * lo, A[b][k] * hi) for b, (lo, hi) in enumerate(civ)]
            column, Zk = positive_normalize(raw)
            columns.append(column)
            candidate_Z.append(Zk)
        candidate = [interval_sum([column[b] for column in columns], v)
                     for b in range(len(civ))]
        interface = "actual rational normalized-filtered v"
    upper = interval_TV_upper(target, candidate)
    return {"TV_upper": upper, "target_sector_intervals": target,
            "candidate_sector_intervals": candidate,
            "target_scaled_normalizer_interval": target_Z,
            "candidate_scaled_normalizer_intervals": candidate_Z,
            "candidate_interface": interface, "precision_bits": bits,
            "physical_multiplicities_retained": True,
            "block_sampler_errors_included": False}


def direct_filtered_branch_data(N, delta, h, v, eps):
    """Positive finite type probabilities; zero slices deliberately not divided."""
    eps = F(eps)
    v = simplex(v)
    if len(v) != N + 1:
        raise ValueError("wrong filtered-weight count")
    bits = 2 * N + max(1, ceil_log2(1 / eps)) + 14
    f, _ = scaled_filter_values(N, delta, h, bits)
    _, c, Z = filtered_sector_columns(N, f)
    branches = []
    for k in range(N + 1):
        n = N - k
        column_sum = F(0)
        for u in range(n + 1):
            interval_sum_value = sum(f[u:u + k + 1])
            R = F(choose(n, u), (k + 1) * (1 << n)) * interval_sum_value
            p = R / Z[k]
            column_sum += p
            branches.append({"k": k, "u": u, "m": F(2 * u - n, 2),
                             "pre_rounding_probability": v[k] * p,
                             "global_slice_sum": interval_sum_value})
        assert column_sum == 1
    raw = [b["pre_rounding_probability"] for b in branches]
    probabilities, draw_bits = round_dyadic_probabilities(raw, F(256 * len(raw)) / eps)
    for branch, probability in zip(branches, probabilities):
        branch["probability"] = probability
    return branches, {"scalar_bits": bits, "outer_draw_bits": draw_bits,
                      "filter_values": f, "filtered_K_normalizers": Z,
                      "zero_global_slices": sum(b["global_slice_sum"] == 0 for b in branches)}


def conditional_max_shift_probabilities(N, k, u, delta, h, eps):
    """PSD Dicke input at precision independent of numerical field magnitude."""
    delta, h, eps = map(F, (delta, h, eps))
    if not 0 <= k <= N or not 0 <= u <= N - k:
        raise ValueError("invalid branch")
    exponents = []
    for l in range(k + 1):
        m = F(2 * (l + u) - N, 2)
        exponents.append(-delta * m * m / N + h * m)
    maximum = max(exponents)
    bits = max(1, ceil_log2(F(256 * (k + 1)) / eps))
    raw = [exp_neg_dyadic(maximum - e, bits) for e in exponents]
    Z = sum(raw)
    assert Z >= 1
    return [v / Z for v in raw], {"scalar_bits": bits,
                                 "normalizer_at_least_one": True,
                                 "target_TV_bound": eps / 256}
