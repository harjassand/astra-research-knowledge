"""Ported native interface of Mausberg2026, fixed-rank conditional learning.

Implements LOCAL padding, exact dyadic token smoothing, and one consistent
cached binary-logit estimator. No original logit VALUE, hidden factors,
outcome bias, polynomial surrogate or full GLS learner is implemented here.
Theorems/programs consumed by the port are bound in FIXED_RANK_NATIVE_PORT.md.
"""
from fractions import Fraction as F
from math import comb


def ceil_fraction(q):
    q = F(q)
    return -(-q.numerator // q.denominator)


def power_two(k):
    return F(1 << k) if k >= 0 else F(1, 1 << (-k))


def ceil_log2(q):
    q = F(q)
    if q <= 0:
        raise ValueError("positive rational required")
    k = q.numerator.bit_length() - q.denominator.bit_length()
    return k + int(q > power_two(k))


def log_unit_interval(y, tolerance):
    """Rational lower log(y), 1<=y<=2, with the explicit atanh tail."""
    y, tolerance = F(y), F(tolerance)
    if not 1 <= y <= 2 or tolerance <= 0:
        raise ValueError("invalid logarithm interval")
    z = (y - 1) / (y + 1)
    if not z:
        return F(0)
    z2, term, total, j = z * z, z, F(0), 0
    while True:
        total += 2 * term / (2 * j + 1)
        term *= z2
        j += 1
        tail = 2 * term / ((2 * j + 1) * (1 - z2))
        if tail <= tolerance:
            return total


def rational_log(q, tolerance):
    q, tolerance = F(q), F(tolerance)
    if q <= 0 or tolerance <= 0:
        raise ValueError("positive log input and tolerance required")
    j = q.numerator.bit_length() - q.denominator.bit_length()
    if q < power_two(j):
        j -= 1
    y = q / power_two(j)
    local = tolerance / (2 * (abs(j) + 1))
    return log_unit_interval(y, local) + j * log_unit_interval(F(2), local)


def round_dyadic(q, bits):
    scaled = F(q) * (1 << bits)
    nearest = (2 * scaled.numerator + scaled.denominator) // (2 * scaled.denominator)
    return F(nearest, 1 << bits)


class SmoothedPaddedBinary:
    """Exact stochastic kernel, conditional on exact iid native/fair services.

    native.next(prefix) returns one independent original next bit. The optional
    native.count(prefix,n) is just an aggregation of n such paid calls, never
    one free experiment. coins.bernoulli/count/bit provide independent local
    randomness; diagnostic implementations may use seeded PRNGs explicitly.
    """
    def __init__(self, native, original_length, padded_length, tau, coins):
        self.native, self.T, self.H, self.coins = native, original_length, padded_length, coins
        self.tau = F(tau)
        if not 1 <= self.T <= self.H or not 0 < self.tau < F(1, 2):
            raise ValueError("invalid padding/smoothing contract")
        if self.tau.denominator & (self.tau.denominator - 1):
            raise ValueError("primary smoothing uses a dyadic mixing parameter")
        self.gamma = self.tau / 2
        self.stats = {k: 0 for k in (
            "logical_next_requests", "logical_submitted_symbols", "logical_returned_symbols",
            "native_next_draws", "native_submitted_symbols", "native_returned_symbols",
            "smoothing_uniform_outputs", "local_padding_outputs")}

    def validate(self, prefix):
        h = tuple(prefix)
        if len(h) >= self.H or any(o not in (0, 1) for o in h):
            raise ValueError("not a legal padded next-token context")
        return h

    def _logical(self, h, n):
        self.stats["logical_next_requests"] += n
        self.stats["logical_submitted_symbols"] += n * len(h)
        self.stats["logical_returned_symbols"] += n

    def next(self, prefix):
        h = self.validate(prefix)
        self._logical(h, 1)
        if len(h) >= self.T:
            self.stats["local_padding_outputs"] += 1
            return self.coins.bit()
        if self.coins.bernoulli(self.tau):
            self.stats["smoothing_uniform_outputs"] += 1
            return self.coins.bit()
        self.stats["native_next_draws"] += 1
        self.stats["native_submitted_symbols"] += len(h)
        self.stats["native_returned_symbols"] += 1
        return self.native.next(h)

    def count(self, prefix, n):
        h = self.validate(prefix)
        if n < 0:
            raise ValueError("nonnegative count required")
        self._logical(h, n)
        if len(h) >= self.T:
            self.stats["local_padding_outputs"] += n
            return self.coins.count(F(1, 2), n)
        # Count-only aggregation is exact by exchangeability; it is NOT used
        # for an evolving-prefix future, which uses next() at each native time.
        noisy = self.coins.count(self.tau, n)
        self.stats["smoothing_uniform_outputs"] += noisy
        native_n = n - noisy
        self.stats["native_next_draws"] += native_n
        self.stats["native_submitted_symbols"] += native_n * len(h)
        self.stats["native_returned_symbols"] += native_n
        if hasattr(self.native, "count"):
            native_heads = self.native.count(h, native_n)
        else:
            native_heads = sum(self.native.next(h) for _ in range(native_n))
        return native_heads + self.coins.count(F(1, 2), noisy)

    def future(self, prefix=()):
        h = list(prefix)
        if len(h) > self.H or any(o not in (0, 1) for o in h):
            raise ValueError("invalid padded future context")
        answer = []
        while len(h) < min(self.T, self.H):
            o = self.next(h)
            answer.append(o)
            h.append(o)
        # Uniform padding needs no original query, even after a noisy prefix.
        begin, count = len(h), self.H - len(h)
        self.stats["logical_next_requests"] += count
        self.stats["logical_submitted_symbols"] += count * (begin + self.H - 1) // 2
        self.stats["logical_returned_symbols"] += count
        self.stats["local_padding_outputs"] += count
        answer.extend(self.coins.bit() for _ in range(count))
        return tuple(answer)


class CachedBinaryLogits:
    """Mausberg Lemma6 plus caching; all measurements are of Ptau itself."""
    def __init__(self, adapter, tolerance, failure_per_context, max_draws=None):
        self.adapter = adapter
        self.xi, self.failure = F(tolerance), F(failure_per_context)
        if not 0 < self.xi <= 1 or not 0 < self.failure < 1:
            raise ValueError("invalid estimator accuracy/confidence")
        self.draws = ceil_fraction(
            48 * ceil_log2(4 / self.failure) / (self.adapter.gamma * self.xi ** 2))
        self.bits = max(0, ceil_log2(32 / self.xi))
        self.max_draws, self.cache, self.records, self.hits = max_draws, {}, [], 0

    def get(self, prefix):
        h = self.adapter.validate(prefix)
        if h in self.cache:
            self.hits += 1
            return self.cache[h]
        if len(h) >= self.adapter.T:
            self.cache[h] = F(0)  # Ptau padding is mathematically exactly fair.
            self.records.append({"prefix_length": len(h), "draws": 0, "reason": "known local uniform padding"})
            return F(0)
        if self.max_draws is not None and self.draws > self.max_draws:
            raise RuntimeError("declared native measurement budget exceeded before acquisition")
        heads = self.adapter.count(h, self.draws)
        empirical = F(heads, self.draws)
        clipped = min(1 - self.adapter.gamma / 2,
                      max(self.adapter.gamma / 2, empirical))
        raw = (rational_log(clipped, self.xi / 8) -
               rational_log(1 - clipped, self.xi / 8)) / 2
        value = round_dyadic(raw, self.bits)
        self.cache[h] = value
        self.records.append({"prefix_length": len(h), "draws": self.draws,
                             "heads": heads, "empirical": str(empirical),
                             "clipped": str(clipped), "scalar_centered_logit": str(value),
                             "dyadic_fractional_bits": self.bits})
        return value


def primary_binary_parameters(T, d, alpha, epsilon, delta):
    """Exact finite selectors in the published proof, without running GLS.

    Returned integers are often huge. Their numerical value is not a claim
    that the complete native protocol is practically affordable.
    """
    epsilon, delta, alpha = F(epsilon), F(delta), F(alpha)
    if T < 1 or d < 1 or alpha < 1 or not 0 < epsilon < F(1, 2) or not 0 < delta < F(1, 2):
        raise ValueError("outside the port contract")
    H = max(32, T, ceil_fraction(alpha * alpha))
    tau = power_two(-ceil_log2(8 * H / epsilon))
    L = ceil_log2(4 / tau) + 3
    Cq = 52
    J = ceil_log2(2 * H * Cq * (d + 1) * L / (epsilon * delta)) + 10
    N = 100 * Cq * (d + 1) * J
    degree = 8 * H * N
    lifted_rank = comb(d + degree, d)
    V = F(2 * H * lifted_rank * L) / (epsilon * delta)
    # Source bounds are inequalities, not the actual GLS tolerance or caps.
    return {"original_length": T, "padded_length": H, "rank_budget": d,
            "tau": tau, "floor": tau / 2, "smoothed_logit_bound_integer": L,
            "J": J, "precision_exponent_N": N, "polynomial_degree": degree,
            "lifted_rank_D": lifted_rank, "V": V,
            "source_request_cap_upper": V ** 22,
            "source_inverse_tolerance_upper": V ** 11,
            "source_training_token_cap_upper": V ** 52}
