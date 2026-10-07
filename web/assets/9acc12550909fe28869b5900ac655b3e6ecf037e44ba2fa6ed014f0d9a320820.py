"""Finite ellipsoid archive and exact-law/certified scalar calculations."""

from __future__ import annotations

from bisect import bisect_right
from dataclasses import dataclass
from fractions import Fraction
from math import prod

from certified import IV, SCALE, ceil_div, log_interval, normal_mass, normal_pdf, sqrt_log_upper_endpoint


@dataclass(frozen=True)
class Axis:
    j: int
    a: Fraction
    h: Fraction
    T: Fraction
    M: int

    @property
    def labels(self):
        return self.M + 2

    @property
    def bits(self):
        return (self.labels - 1).bit_length()

    @property
    def width(self):
        return 2 * self.T / self.M

    def bounds(self, label):
        if not 0 <= label < self.labels:
            raise ValueError("Invalid bin label")
        if label == 0:
            return None, -self.T
        if label == self.M + 1:
            return self.T, None
        return (-self.T + 2 * self.T * (label - 1) / self.M,
                -self.T + 2 * self.T * label / self.M)

    def encode(self, x):
        """Exact for a rational input. Real X uses the same ideal comparisons."""
        x = Fraction(x)
        if x < -self.T:
            return 0
        if x >= self.T:
            return self.M + 1
        return 1 + ((x + self.T) * self.M // (2 * self.T))


@dataclass(frozen=True)
class Archive:
    A: Fraction
    alpha: int
    eps: Fraction
    d: int
    axes: tuple[Axis, ...]

    @property
    def k(self):
        return len(self.axes)

    @property
    def alphabet_size(self):
        return prod(axis.labels for axis in self.axes)

    @property
    def mixed_radix_bits(self):
        return (self.alphabet_size - 1).bit_length()

    @property
    def vector_bits(self):
        return sum(axis.bits for axis in self.axes)

    def encode(self, observations):
        # Streaming input: consumes only k entries, never accepts theta.
        it = iter(observations)
        return tuple(axis.encode(next(it)) for axis in self.axes)

    def encode_packed(self, observations):
        # The compact API returns one message, so callers need not retain both
        # a label vector and a packed duplicate. Source input buffers must be
        # released by the caller when the archive boundary is reached.
        it = iter(observations)
        message = 0
        for axis in self.axes:
            label = axis.encode(next(it))
            message = message * axis.labels + label
        return message

    def pack(self, labels):
        if len(labels) != self.k:
            raise ValueError("Wrong number of labels")
        message = 0
        for axis, label in zip(self.axes, labels):
            if not 0 <= label < axis.labels:
                raise ValueError("Invalid label")
            message = message * axis.labels + label
        return message

    def unpack(self, message):
        if not 0 <= message < self.alphabet_size:
            raise ValueError("Invalid message")
        labels = []
        for axis in reversed(self.axes):
            message, label = divmod(message, axis.labels)
            labels.append(label)
        return tuple(reversed(labels))


def make_archive(A, alpha, eps, d):
    A, eps = Fraction(A), Fraction(eps)
    if alpha < 1 or not isinstance(alpha, int):
        raise ValueError("Experiment uses positive integer alpha, theorem permits alpha>0")
    if not (A > 0 and 0 < eps <= 1 and d >= 1):
        raise ValueError("Invalid design inputs")
    axes = []
    for j in range(1, d + 1):
        a = A / j**alpha
        if a <= eps:
            break
        h = eps / a
        T = sqrt_log_upper_endpoint(a, h)
        M = ceil_div((2 * T / h).numerator, (2 * T / h).denominator)
        axis = Axis(j, a, h, T, M)
        assert axis.width <= h
        axes.append(axis)
    return Archive(A, alpha, eps, d, tuple(axes))


def axis_kl(axis: Axis, theta) -> tuple[IV, list[dict]]:
    """KL(P_theta || phi * P_theta(bin)/P_0(bin)), with certified enclosures.

    The coordinate probabilities and logarithms are enclosing intervals. There
    are no Monte Carlo estimates or adaptive numerical tolerance guesses.
    """
    theta = Fraction(theta)
    if theta == 0:
        return IV.exact(0), []
    if abs(theta) > axis.a:
        raise ValueError("Scalar mean exceeds supplied axis radius")
    discrete_kl = IV.exact(0)
    details = []
    for label in range(axis.labels):
        left, right = axis.bounds(label)
        pt = normal_mass(left, right, theta)
        p0 = normal_mass(left, right, 0)
        log_ratio = log_interval(pt) - log_interval(p0)
        discrete_kl += pt * log_ratio
        # Weighted conditional KL, avoiding a conditional-mean division.
        pl = IV.exact(0) if left is None else normal_pdf(left - theta)
        pr = IV.exact(0) if right is None else normal_pdf(right - theta)
        weighted_cond = theta * (theta * pt + pl - pr) - theta * theta / 2 * pt - pt * log_ratio
        bound = theta * theta / 2 if left is None or right is None else theta * theta * axis.width**2 / 8
        # Division is used only for reported scalar conditional diagnostics.
        conditional_kl = weighted_cond / pt
        if conditional_kl.lo > IV.exact(bound).hi:
            raise AssertionError("Conditional KL enclosure disproves analytic bound")
        details.append({"label": label, "left": left, "right": right,
                        "p_theta": pt, "p_reference": p0,
                        "conditional_kl": conditional_kl,
                        "weighted_conditional_kl": weighted_cond,
                        "conditional_bound": bound})
    kl = IV.exact(theta * theta / 2) - discrete_kl
    if kl.lo < 0 <= kl.hi:
        kl = IV(0, kl.hi)
    total_bound = theta * theta * axis.h**2 / 4
    if kl.lo > IV.exact(total_bound).hi:
        raise AssertionError("KL enclosure disproves uniform analytic bound")
    return kl, details


def axis_tv(axis: Axis, theta) -> IV:
    """Exact scalar TV formula, integrated using certified Gaussian masses."""
    theta = Fraction(theta)
    if theta == 0:
        return IV.exact(0)
    if theta < 0:
        return axis_tv(axis, -theta)
    tv = IV.exact(0)
    for label in range(axis.labels):
        left, right = axis.bounds(label)
        pt = normal_mass(left, right, theta)
        p0 = normal_mass(left, right, 0)
        ratio = pt / p0
        crossing = (log_interval(pt) - log_interval(p0) + theta * theta / 2) / theta
        # The crossing lies inside its bin. Bound its uncertain location by
        # integration at the two rational enclosing endpoints; evaluate the
        # positive (right-hand) part because theta>0.
        c_lo, c_hi = Fraction(crossing.lo, SCALE), Fraction(crossing.hi, SCALE)
        if left is not None:
            c_lo, c_hi = max(left, c_lo), max(left, c_hi)
        if right is not None:
            c_lo, c_hi = min(right, c_lo), min(right, c_hi)
        ptl = normal_mass(c_lo, right, theta)
        p0l = normal_mass(c_lo, right, 0)
        pth = normal_mass(c_hi, right, theta)
        p0h = normal_mass(c_hi, right, 0)
        value_l = ptl - ratio * p0l
        value_h = pth - ratio * p0h
        # The endpoint formula's derivative vanishes at the true crossing.
        # A completely safe enclosure allows every integral in [c_lo,c_hi].
        uncertainty = normal_mass(c_lo, c_hi, theta) + ratio * normal_mass(c_lo, c_hi, 0)
        low = min(value_l.lo, value_h.lo) - uncertainty.hi
        high = max(value_l.hi, value_h.hi) + uncertainty.hi
        tv += IV(max(0, low), high)
    return tv.clip_probability()


def rounded_decoder_table(axis: Axis | None, label: int | None,
                          boundaries: tuple[Fraction, ...]) -> tuple[IV, ...]:
    """Law of clipping/rounding the exact conditional-reference output.

    Finite output cells are (-inf,b0),[b0,b1),...,[b_last,inf).
    With axis=None this is the rounded standard-normal reference law.
    """
    if axis is None:
        left, right = None, None
        denominator = IV.exact(1)
    else:
        left, right = axis.bounds(label)
        denominator = normal_mass(left, right, 0)
    cells = tuple(zip((None,) + boundaries, boundaries + (None,)))
    result = []
    for cell_l, cell_r in cells:
        l = cell_l if left is None else left if cell_l is None else max(left, cell_l)
        r = cell_r if right is None else right if cell_r is None else min(right, cell_r)
        if l is not None and r is not None and l >= r:
            result.append(IV.exact(0))
        else:
            result.append((normal_mass(l, r, 0) / denominator).clip_probability())
    return tuple(result)


def compile_dyadic_cdf(probabilities: tuple[IV, ...], random_bits=40):
    """Compile a fair-bit categorical sampler with an explicit TV bound.

    Approximate each exact cumulative probability by the midpoint of its
    certified interval, then floor it to a dyadic multiple of 2^-random_bits.
    If cumulative error is bounded by e, TV<=sum_i e_i; this follows by
    telescoping the adjacent cumulative differences.
    """
    denom = 1 << random_bits
    cumulative = IV.exact(0)
    cutoffs = []
    error_sum = Fraction(0)
    for p in probabilities[:-1]:
        cumulative += p
        midpoint = cumulative.midpoint()
        cutoff = (midpoint * denom).numerator // (midpoint * denom).denominator
        cutoff = max(0, min(denom, cutoff))
        if cutoffs and cutoff < cutoffs[-1]:
            raise ArithmeticError("Numerical enclosures too loose to compile monotone CDF")
        error = max(abs(Fraction(cumulative.lo, SCALE) - Fraction(cutoff, denom)),
                    abs(Fraction(cumulative.hi, SCALE) - Fraction(cutoff, denom)))
        error_sum += error
        cutoffs.append(cutoff)
    # The last cell gets all the remaining mass; exact normalization by design.
    return tuple(cutoffs), error_sum


def sample_dyadic_cdf(cutoffs, random_bits, rng):
    # Returns a cell index. Randomness is decoder-fresh and independent of X.
    return bisect_right(cutoffs, rng.getrandbits(random_bits))


def dyadic_cell_probabilities(cutoffs, random_bits):
    points = (0,) + tuple(cutoffs) + (1 << random_bits,)
    return tuple(Fraction(b - a, 1 << random_bits) for a, b in zip(points, points[1:]))
