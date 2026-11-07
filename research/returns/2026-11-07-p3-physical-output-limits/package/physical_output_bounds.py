"""Exact finite certificates for the physical-output bounds in the report.

This compiler consumes WARRANTED rate, support and operator-norm bounds.
It does not infer a native law or acquire a noise model from observations.
All certification arithmetic below uses integers/Fraction.  No external
numerical packages, physical oracle, sampler, or controller are called.
"""

from dataclasses import dataclass
from fractions import Fraction as F
from math import isqrt
from typing import Iterable


def rational(value):
    if isinstance(value, float):
        raise TypeError("Use exact integers, strings, or Fraction; float is not a certificate")
    result = F(value)
    # Normalize numpy integer subclasses too: certificate integers must have
    # Python's unbounded arithmetic, not a fixed-width scalar's multiplication.
    return F(int(result.numerator), int(result.denominator))


def sqrt_interval(value, bits=80):
    value = rational(value)
    if value < 0 or bits < 0:
        raise ValueError("nonnegative radicand and bits required")
    scale = 1 << bits
    low_integer = isqrt((value.numerator * scale * scale) // value.denominator)
    low = F(low_integer, scale)
    high = low if low * low == value else F(low_integer + 1, scale)
    assert low * low <= value <= high * high
    return low, high


def exp_negative_upper(value, order=64):
    """e**(-value) <= 1/sum(value**j/j!, j=0..order), exactly.

    This is an upper bound, not a claim of fixed absolute approximation error.
    Arithmetic and output length depend on order and the rational input size.
    """
    value = rational(value)
    if value < 0 or order < 0:
        raise ValueError("nonnegative argument and order required")
    term = total = F(1)
    for k in range(1, order + 1):
        term = term * value / k
        total += term
    return 1 / total


@dataclass(frozen=True)
class LocalBudget:
    """Bounds on local target-frame return and off-diagonal blocks.

    The Hamiltonian/jump constructor gives target-independent sufficient
    bounds.  A smaller supplied bound must be warranted for the actual target
    frame, including any graph conjugation and every allowed auxiliary state.
    """
    support: tuple[int, ...]
    return_bound: F
    offdiag_bound: F

    def __post_init__(self):
        object.__setattr__(self, "support", tuple(sorted(set(self.support))))
        object.__setattr__(self, "return_bound", rational(self.return_bound))
        object.__setattr__(self, "offdiag_bound", rational(self.offdiag_bound))
        if self.return_bound < 0 or self.offdiag_bound < 0:
            raise ValueError("negative budget")

    @classmethod
    def from_hamiltonian_and_jumps(cls, support, h_norm, jump_norm_squared_sum):
        h, d = rational(h_norm), rational(jump_norm_squared_sum)
        if h < 0 or d < 0:
            raise ValueError("negative physical norm bound")
        return cls(tuple(support), d, h + d / 2)


@dataclass(frozen=True)
class Envelope:
    leakage: F
    return_rate: F
    offdiag_squared: F

    def __post_init__(self):
        for name in ("leakage", "return_rate", "offdiag_squared"):
            object.__setattr__(self, name, rational(getattr(self, name)))
        if self.leakage <= 0 or self.return_rate < 0 or self.offdiag_squared < 0:
            raise ValueError("positive leakage and nonnegative other bounds required")

    def drift_sign(self, fidelity):
        """Sign of -leakage*f + return_rate*(1-f) + 2*sqrt(B2*f*(1-f))."""
        f = rational(fidelity)
        if not 0 <= f <= 1:
            raise ValueError("fidelity outside [0,1]")
        u = self.leakage * f - self.return_rate * (1 - f)
        z = 4 * self.offdiag_squared * f * (1 - f)
        if u < 0:
            return 1
        if u == 0:
            return 0 if z == 0 else 1
        difference = u * u - z
        return -1 if difference > 0 else (0 if difference == 0 else 1)

    def root_interval(self, bits=80):
        low, high = F(0), F(1)
        if self.drift_sign(low) == 0 and self.return_rate == self.offdiag_squared == 0:
            return low, low
        for _ in range(bits):
            mid = (low + high) / 2
            sign = self.drift_sign(mid)
            if sign == 0:
                return mid, mid
            if sign > 0:
                low = mid
            else:
                high = mid
        assert self.drift_sign(low) >= 0 and self.drift_sign(high) <= 0
        return low, high

    def drift_interval(self, fidelity, bits=80):
        f = rational(fidelity)
        if not 0 <= f <= 1:
            raise ValueError("fidelity outside [0,1]")
        base = -self.leakage * f + self.return_rate * (1 - f)
        low, high = sqrt_interval(self.offdiag_squared * f * (1 - f), bits)
        return base + 2 * low, base + 2 * high

    def exclusion_certificate(self, fidelity, bits=80):
        f = rational(fidelity)
        if not 0 <= f <= 1:
            raise ValueError("fidelity outside [0,1]")
        u = self.leakage * f - self.return_rate * (1 - f)
        squared_margin = u * u - 4 * self.offdiag_squared * f * (1 - f)
        excluded = u > 0 and squared_margin > 0
        drift_low, drift_high = self.drift_interval(f, bits)
        return {
            "fidelity": f,
            "positive_linear_margin": u,
            "squared_margin": squared_margin,
            "strictly_above_barrier": excluded,
            "drift_lower": drift_low,
            "drift_upper": drift_high,
        }

    def dwell_upper(self, fidelity, bits=80):
        """Maximum length of one uninterrupted interval F >= fidelity, F(0)<=1."""
        f = rational(fidelity)
        cert = self.exclusion_certificate(f, bits)
        if not cert["strictly_above_barrier"] or cert["drift_upper"] >= 0:
            raise ValueError("not a strict exclusion, or increase square-root precision")
        return (1 - f) / (-cert["drift_upper"])

    def linear_parameters(self, theta=F(1, 2)):
        theta = rational(theta)
        if not 0 < theta < 1:
            raise ValueError("theta must lie strictly between 0 and 1")
        if self.offdiag_squared == 0:
            c = self.return_rate
            gamma = self.leakage + c
            return c, gamma, c / gamma
        c = self.return_rate + self.offdiag_squared / (theta * self.leakage)
        gamma = (1 - theta) * self.leakage + c
        return c, gamma, c / gamma

    def delivery_upper(self, delay, theta=F(1, 2), exp_order=64, initial_fidelity=1):
        delay, f0 = rational(delay), rational(initial_fidelity)
        if delay < 0 or not 0 <= f0 <= 1:
            raise ValueError("invalid delay or initial fidelity")
        _, gamma, floor = self.linear_parameters(theta)
        exponent_upper = exp_negative_upper(gamma * delay, exp_order)
        # For f0 below the linear fixed point, using zero for the exponential
        # gives a conservative upper bound.  No wrong-sign rounding occurs.
        return min(F(1), floor + max(F(0), f0 - floor) * exponent_upper)

    def accepted_probability_upper(self, delay, conditional_fidelity, **kwargs):
        f = rational(conditional_fidelity)
        if not 0 < f <= 1:
            raise ValueError("positive conditional fidelity required")
        return min(F(1), self.delivery_upper(delay, **kwargs) / f)

    def with_residual(self, rate_error):
        """For |Tr P Delta(rho)| <= rate_error; e.g. half diamond <= rate_error."""
        eta = rational(rate_error)
        if eta < 0:
            raise ValueError("negative residual budget")
        return Envelope(self.leakage - eta, self.return_rate + eta,
                        self.offdiag_squared)


def compile_local(n: int, noise_rates: Iterable, budgets: Iterable[LocalBudget],
                  graph_edges=None, invariant_target=False):
    """Product |0^n> with X noise, or graph state with physical Z noise.

    graph_edges=None selects the product case.  For a graph, actual control
    supports are enlarged by closed neighborhoods; the physical noise is Z_i.
    The bounds must apply in that enlarged target frame.  Bounds made by
    from_hamiltonian_and_jumps apply automatically because norms are invariant.
    Ancilla-only budgets (empty work support) have zero target action.
    invariant_target=True requires the separately warranted whole controller
    to preserve the pure work subspace for EVERY ancillary state.
    """
    if not isinstance(n, int) or n < 1:
        raise ValueError("positive number of output qubits required")
    rates = tuple(rational(x) for x in noise_rates)
    if len(rates) != n or any(x < 0 for x in rates) or sum(rates) <= 0:
        raise ValueError("one nonnegative noise rate per output; positive total")
    neighborhoods = [{i} for i in range(n)]
    if graph_edges is not None:
        for i, j in graph_edges:
            if not 0 <= i < n or not 0 <= j < n or i == j:
                raise ValueError("invalid simple graph edge")
            neighborhoods[i].add(j)
            neighborhoods[j].add(i)
    incidence_return = [F(0) for _ in range(n)]
    incidence_offdiag = [F(0) for _ in range(n)]
    total_offdiag = F(0)
    mapped = []
    for budget in budgets:
        if any(not 0 <= i < n for i in budget.support):
            raise ValueError("work support outside output register")
        if not budget.support:
            continue
        support = set().union(*(neighborhoods[i] for i in budget.support))
        for i in support:
            incidence_return[i] += budget.return_bound
            incidence_offdiag[i] += budget.offdiag_bound
        total_offdiag += budget.offdiag_bound
        mapped.append(tuple(sorted(support)))
    r = max(incidence_return)
    v = max(incidence_offdiag)
    b2 = F(0) if invariant_target else total_offdiag * v
    envelope = Envelope(sum(rates), max(rates) + r, b2)
    return envelope, {
        "N": n,
        "mapped_supports": mapped,
        "return_incidence": incidence_return,
        "offdiag_incidence": incidence_offdiag,
        "total_offdiag": total_offdiag,
        "invariant_target_assumed": bool(invariant_target),
    }


def compile_uniform(n, noise_rate, return_per_site, offdiag_per_site,
                    maximum_graph_degree=0, invariant_target=False):
    """O(1) arithmetic for supplied uniform incidence bounds.

    The target-frame support expansion multiplies incidence by D=degree+1,
    but does not multiply the sum of term off-diagonal bounds.
    """
    if not isinstance(n, int) or n < 1 or maximum_graph_degree < 0:
        raise ValueError("invalid size or degree")
    lam, r, b = map(rational, (noise_rate, return_per_site, offdiag_per_site))
    if lam <= 0 or r < 0 or b < 0:
        raise ValueError("invalid rates")
    D = maximum_graph_degree + 1
    return Envelope(n * lam, lam + D * r,
                    0 if invariant_target else D * n * b * b)


def coherent_strength_necessary(n, noise_rate, infidelity, degree=0, bits=80):
    """Necessary common per-site generator bound J, returned as rational interval.

    Uses return_per_site <= J and offdiag_per_site <= J.  This is necessary,
    not a sufficient coherent-control construction or an optimal threshold.
    """
    lam, e = rational(noise_rate), rational(infidelity)
    if n < 1 or lam <= 0 or not 0 < e < 1 or degree < 0:
        raise ValueError("invalid parameters")
    D = degree + 1
    num = lam * max(F(0), n * (1 - e) - e)
    low, high = sqrt_interval(D * n * e * (1 - e), bits)
    return num / (D * e + 2 * high), num / (D * e + 2 * low)


def invariant_return_necessary(n, noise_rate, infidelity):
    lam, e = rational(noise_rate), rational(infidelity)
    if n < 1 or lam <= 0 or not 0 < e < 1:
        raise ValueError("invalid parameters")
    return max(F(0), lam * (n * (1 - e) / e - 1))


def ceil_log2_rational(value):
    value = rational(value)
    if value <= 1:
        return 0
    k = max(0, value.numerator.bit_length() - value.denominator.bit_length())
    while F(1 << k) < value:
        k += 1
    while k and F(1 << (k - 1)) >= value:
        k -= 1
    return k


def ideal_pumping_comparison(n, noise_upper, complete_error, holding_time=0, degree=0):
    """Costed MATHEMATICAL comparator; requires warranted ideal stabilizer pumps.

    This does NOT claim the previous noisy native family supplies these pumps.
    Its intrinsic actuator noise floor is a different law.
    """
    lam, eps, hold = map(rational, (noise_upper, complete_error, holding_time))
    if n < 1 or lam <= 0 or not 0 < eps < 1 or hold < 0 or degree < 0:
        raise ValueError("invalid comparator parameters")
    kappa = 2 * n * lam / eps
    m = ceil_log2_rational(4 * n / eps)
    time = 2 * m / kappa
    return {
        "N": n,
        "requires_ideal_native_pumps": True,
        "per_pump_rate": kappa,
        "total_peak_rate": n * kappa,
        "physical_site_incidence_upper": (degree + 1) * kappa,
        "jump_support_upper": degree + 1,
        "preparation_time": time,
        "integrated_preparation_rate": n * kappa * time,
        "integrated_holding_rate": n * kappa * hold,
        "stationary_trace_error_upper": n * lam / (kappa + 2 * lam),
        "complete_transient_error_upper": F(2 * n, 1 << m),
    }


def json_exact(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {str(k): json_exact(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_exact(v) for v in value]
    return value
