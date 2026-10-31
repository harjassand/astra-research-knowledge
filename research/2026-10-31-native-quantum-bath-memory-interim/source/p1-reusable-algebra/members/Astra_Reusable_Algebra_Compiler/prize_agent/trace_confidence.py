"""Reusable trace confidence sets for an acquired finite matrix *-algebra.

The algebra is fixed independently of the Gaussian probes.  Its simple blocks
have irreducible sizes r[a] and ambient sizes n[a] = r[a] * m[a].  At a fixed
sample count q[a], cyclic closure reveals s[a] = min(m[a], q[a] * r[a]), and
the accumulated central energy W[a] has Gamma(q[a] * n[a], 1) distribution.

For a future algebra element X, write slope[a] = tr(X[a]) / r[a].  Its ambient
trace is sum(n[a] * slope[a]).  This module bounds that trace by optimizing a
linear objective over a simultaneous confidence box intersected with the known
equation sum(n[a]) = N.  The same confidence event covers all future slopes,
including signed slopes and slopes selected after seeing the samples.

The probability claim follows from the mathematical gamma Chernoff bound.  The
implementation uses double precision with conservative inversion brackets; it
is a reproducible numerical implementation, not a formal interval-arithmetic
certificate.  Exact ranks and a correct acquired block decomposition are inputs.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Iterable, Sequence


def gamma_deviance(observed: float, shape: float) -> float:
    """D(w, nu) = w - nu - nu log(w / nu), extended by continuity."""
    if not math.isfinite(observed) or observed < 0:
        raise ValueError("The observed energy must be finite and nonnegative.")
    if not math.isfinite(shape) or shape < 0:
        raise ValueError("The proposed shape must be finite and nonnegative.")
    if shape == 0:
        return observed
    if observed == 0:
        return math.inf
    x = (observed - shape) / shape
    if abs(x) < 1e-4:
        # x - log(1+x), avoiding subtraction of nearly equal quantities.
        term = x * x
        value = term / 2.0
        for power in range(3, 13):
            term *= -x
            value += term / power
        return max(0.0, shape * value)
    return max(0.0, observed - shape + shape * math.log(shape / observed))


def gamma_shape_interval(observed: float, threshold: float) -> tuple[float, float]:
    """Invert D(observed, nu) <= threshold using conservative root brackets.

    For W ~ Gamma(nu, 1), the interval contains nu except on an event of
    probability at most 2 exp(-threshold).  When observed <= threshold the
    lower endpoint is zero.  An observed zero leads to [0, 0], an impossible
    event for a nonzero block in the exact Gaussian model.
    """
    if not math.isfinite(observed) or observed < 0:
        raise ValueError("The observed energy must be finite and nonnegative.")
    if not math.isfinite(threshold) or threshold < 0:
        raise ValueError("The threshold must be finite and nonnegative.")
    if observed == 0 or threshold == 0:
        return observed, observed

    if observed <= threshold:
        lower = 0.0
    else:
        lo, hi = 0.0, observed
        for _ in range(100):
            mid = lo + (hi - lo) / 2.0
            if mid == lo or mid == hi:
                break
            if gamma_deviance(observed, mid) > threshold:
                lo = mid
            else:
                hi = mid
        lower = max(0.0, math.nextafter(lo, -math.inf))

    lo, hi = observed, max(2.0 * observed, observed + 2.0 * threshold, 1.0)
    while gamma_deviance(observed, hi) < threshold:
        hi *= 2.0
        if not math.isfinite(hi):
            raise OverflowError("Cannot bracket the upper gamma shape root.")
    for _ in range(100):
        mid = lo + (hi - lo) / 2.0
        if mid == lo or mid == hi:
            break
        if gamma_deviance(observed, mid) <= threshold:
            lo = mid
        else:
            hi = mid
    upper = math.nextafter(hi, math.inf)
    return lower, upper


@dataclass(frozen=True)
class BlockObservation:
    """Exact acquired block data plus its Gaussian central energy."""

    irreducible_size: int
    reduced_multiplicity: int
    probes: int
    energy: float

    def validate(self) -> None:
        for name in ("irreducible_size", "reduced_multiplicity", "probes"):
            value = getattr(self, name)
            if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
                raise ValueError(f"{name} must be a positive integer.")
        if self.reduced_multiplicity > self.probes * self.irreducible_size:
            raise ValueError("Reduced multiplicity cannot exceed q*r.")
        if not math.isfinite(self.energy) or self.energy < 0:
            raise ValueError("Energy must be finite and nonnegative.")

    @property
    def resolved(self) -> bool:
        return self.reduced_multiplicity < self.probes * self.irreducible_size


@dataclass(frozen=True)
class TraceBounds:
    lower: float
    upper: float
    minimizing_sizes: tuple[float, ...]
    maximizing_sizes: tuple[float, ...]


@dataclass(frozen=True)
class TraceConfidenceSet:
    """A real box for n[a], intersected with the equality sum(n[a]) = N.

    The real relaxation deliberately omits integrality and divisibility.  It
    contains the true feasible discrete sizes and permits O(b log b) exact
    linear optimization in real arithmetic.  It must not be described as an
    exact discrete posterior or an integer-optimization algorithm.
    """

    lower_sizes: tuple[float, ...]
    upper_sizes: tuple[float, ...]
    ambient_dimension: int

    def __post_init__(self) -> None:
        if len(self.lower_sizes) != len(self.upper_sizes) or not self.lower_sizes:
            raise ValueError("The lower and upper sizes must have equal positive length.")
        if self.ambient_dimension <= 0:
            raise ValueError("The ambient dimension must be positive.")
        for lower, upper in zip(self.lower_sizes, self.upper_sizes):
            if not all(math.isfinite(x) for x in (lower, upper)):
                raise ValueError("Block bounds must be finite.")
            if lower < 0 or lower > upper:
                raise ValueError("An invalid or empty block interval was observed.")
        if math.fsum(self.lower_sizes) > self.ambient_dimension:
            raise ValueError("The confidence box is incompatible with the known total.")
        if math.fsum(self.upper_sizes) < self.ambient_dimension:
            raise ValueError("The confidence box is incompatible with the known total.")

    def tighten_total(self) -> TraceConfidenceSet:
        """Return the exact coordinate projections of the equality-constrained box."""
        total_lower = math.fsum(self.lower_sizes)
        total_upper = math.fsum(self.upper_sizes)
        lower, upper = [], []
        for i, (lo, hi) in enumerate(zip(self.lower_sizes, self.upper_sizes)):
            lower.append(max(lo, self.ambient_dimension - total_upper + hi))
            upper.append(min(hi, self.ambient_dimension - total_lower + lo))
        return TraceConfidenceSet(tuple(lower), tuple(upper), self.ambient_dimension)

    def contains(self, sizes: Sequence[float], tolerance: float = 1e-9) -> bool:
        if len(sizes) != len(self.lower_sizes):
            return False
        if abs(math.fsum(sizes) - self.ambient_dimension) > tolerance:
            return False
        return all(lo - tolerance <= size <= hi + tolerance
                   for lo, size, hi in zip(self.lower_sizes, sizes, self.upper_sizes))

    def optimize(self, slopes: Sequence[float], maximize: bool = False) -> tuple[float, tuple[float, ...]]:
        """Optimize any signed trace slopes by greedy bounded allocation."""
        if len(slopes) != len(self.lower_sizes) or not all(math.isfinite(x) for x in slopes):
            raise ValueError("Supply one finite slope per block.")
        sizes = list(self.lower_sizes)
        remaining = self.ambient_dimension - math.fsum(sizes)
        for i in sorted(range(len(sizes)), key=lambda j: slopes[j], reverse=maximize):
            amount = min(remaining, self.upper_sizes[i] - sizes[i])
            sizes[i] += amount
            remaining -= amount
            if remaining <= 0:
                break
        if remaining > 1e-10 * max(1, self.ambient_dimension):
            raise ArithmeticError("Greedy allocation could not meet the known total.")
        return math.fsum(slope * size for slope, size in zip(slopes, sizes)), tuple(sizes)

    def trace_bounds(self, slopes: Sequence[float]) -> TraceBounds:
        lower, minimizing = self.optimize(slopes)
        upper, maximizing = self.optimize(slopes, maximize=True)
        return TraceBounds(lower, upper, minimizing, maximizing)


def confidence_set_from_observations(
    observations: Iterable[BlockObservation],
    ambient_dimension: int,
    *,
    delta: float | None = None,
    threshold: float | None = None,
    tighten_total: bool = True,
) -> TraceConfidenceSet:
    """Construct a simultaneous block-size confidence set at fixed probe counts.

    Specify either delta or an explicit threshold t.  With delta, the union
    bound uses t=log(2*b/delta).  With t, failure is bounded by 2*b*exp(-t).
    For predetermined stages, an external summable allocation of delta makes
    stagewise sets valid at arbitrary stopping times.  The caller must not use
    a fixed-stage delta after choosing probe counts from these same samples.
    """
    blocks = tuple(observations)
    if not blocks:
        raise ValueError("At least one nonzero algebra block is required.")
    if (delta is None) == (threshold is None):
        raise ValueError("Specify exactly one of delta and threshold.")
    if delta is not None:
        if not 0 < delta < 1:
            raise ValueError("delta must lie strictly between zero and one.")
        threshold = math.log(2.0 * len(blocks) / delta)
    assert threshold is not None
    if not math.isfinite(threshold) or threshold <= 0:
        raise ValueError("The confidence threshold must be positive and finite.")

    for block in blocks:
        block.validate()
    unresolved = [i for i, block in enumerate(blocks) if not block.resolved]
    # Deterministic information is stronger than a confidence interval.  If
    # only one size is unknown, infer it from N before looking at its energy.
    # This stays exact even if that energy lies in a rare gamma tail.
    if tighten_total and len(unresolved) <= 1:
        exact_sizes = [block.irreducible_size * block.reduced_multiplicity
                       if block.resolved else 0 for block in blocks]
        if unresolved:
            i = unresolved[0]
            size = ambient_dimension - sum(exact_sizes)
            block = blocks[i]
            if (size < block.probes * block.irreducible_size ** 2
                    or size % block.irreducible_size != 0):
                raise ValueError("The acquired exact structure is incompatible with N.")
            exact_sizes[i] = size
        elif sum(exact_sizes) != ambient_dimension:
            raise ValueError("The fully resolved exact structure is incompatible with N.")
        exact = tuple(float(size) for size in exact_sizes)
        return TraceConfidenceSet(exact, exact, ambient_dimension)

    lower, upper = [], []
    for block in blocks:
        r, q, s = block.irreducible_size, block.probes, block.reduced_multiplicity
        if block.resolved:
            lower.append(float(r * s))
            upper.append(float(r * s))
        else:
            shape_lower, shape_upper = gamma_shape_interval(block.energy, threshold)
            lower.append(max(float(q * r * r), shape_lower / q))
            upper.append(min(float(ambient_dimension), shape_upper / q))
    result = TraceConfidenceSet(tuple(lower), tuple(upper), ambient_dimension)
    return result.tighten_total() if tighten_total else result
