"""Acquire a symbolic dictionary from noisy controlled junta experiments.

The learner receives only a count-observation interface, known N, M, d, gamma,
and a failure budget. It never receives hidden scopes, response tables, or a
numeric oracle. A count of n trials represents n independent physical bit
experiments: batching is only a simulation convenience and does not discount
the experiment bill. The retained dictionary launches fresh experiments; it
does not substitute fitted means for the unknown response law.

All stopping comparisons and confidence caps use integer/Fraction arithmetic.
The conservative logarithm bound ln(x) <= ceil(log2(x)) avoids a floating-point
rounding premise in the displayed sufficient confidence calculation.
"""

from collections import deque
from dataclasses import dataclass, field
from fractions import Fraction
from itertools import product
from typing import Protocol


class CountSource(Protocol):
    component_count: int
    input_dimension: int

    def draw_count(self, component: int, context: tuple[int, ...], shots: int) -> int:
        """Return successes in fresh independent trials at the chosen context."""


def ceil_fraction(x: Fraction) -> int:
    return -((-x.numerator) // x.denominator)


def ceil_log2(x: Fraction) -> int:
    """Exact ceil(log2(x)) for rational x >= 1."""
    if x < 1:
        raise ValueError("the confidence arguments must be at least one")
    k = max(0, x.numerator.bit_length() - x.denominator.bit_length())
    if x.numerator > (x.denominator << k):
        k += 1
    return k


class AcquisitionFailure(RuntimeError):
    """A charged deterministic cap or a promised structural invariant failed."""


@dataclass(frozen=True)
class DiscoveryLimits:
    completion_count: int
    completion_test_cap: int
    mean_assay_cap: int
    shots_per_assay: int
    estimation_radius: Fraction
    chain_threshold: Fraction
    failure_budget: Fraction

    @classmethod
    def construct(cls, M: int, N: int, d: int,
                  gamma: Fraction, delta: Fraction):
        if not (M >= 1 and N >= 1 and 0 <= d <= N):
            raise ValueError("invalid dimensions")
        if not (0 < gamma <= 1 and 0 < delta < 1):
            raise ValueError("invalid source promise or failure budget")
        dimension = max(1, d)
        radius = gamma / (256 * dimension)
        threshold = gamma / (16 * dimension)
        # The final no-missing-parent test is included among d+1 stages.
        blocks = M * (d + 1) * (1 << d)
        completions = (1 << d) * ceil_log2(Fraction(2 * blocks * (1 << d), 1) / delta)
        depth = (N - 1).bit_length()
        # On the confidence event there are <= d live intervals per depth and
        # at most d parent enrichments per component. A cap failure is allowed
        # off that event and cannot silently produce a claimed dictionary.
        assays = blocks * completions + M * d * d * depth + 1
        shots = ceil_fraction(Fraction(ceil_log2(Fraction(4 * assays, 1) / delta), 1)
                              / (2 * radius * radius))
        return cls(completions, blocks, assays, shots, radius, threshold, delta)


@dataclass(frozen=True, order=True)
class Address:
    component: int
    assignment: tuple[int, ...]

    def label(self) -> str:
        return f"component_{self.component}:" + "".join(map(str, self.assignment))


@dataclass
class ExperimentalDictionary:
    """A finite set of executable addresses, not a calibrated numeric table."""
    source: CountSource
    scopes: tuple[tuple[int, ...], ...]

    def addresses(self) -> tuple[Address, ...]:
        return tuple(Address(j, tuple(c)) for j, scope in enumerate(self.scopes)
                     for c in product((0, 1), repeat=len(scope)))

    def canonical_context(self, address: Address) -> tuple[int, ...]:
        scope = self.scopes[address.component]
        if len(scope) != len(address.assignment):
            raise ValueError("address length does not match acquired scope")
        context = [0] * self.source.input_dimension
        for variable, value in zip(scope, address.assignment):
            if value not in (0, 1):
                raise ValueError("non-binary address")
            context[variable] = value
        return tuple(context)

    def address_for_context(self, component: int,
                            context: tuple[int, ...]) -> Address:
        if len(context) != self.source.input_dimension:
            raise ValueError("wrong context dimension")
        return Address(component, tuple(context[i] for i in self.scopes[component]))

    def draw_count(self, address: Address, shots: int) -> int:
        return self.source.draw_count(address.component,
                                      self.canonical_context(address), shots)

    def flip(self, address: Address) -> int:
        return self.draw_count(address, 1)


@dataclass
class AcquisitionStatistics:
    mean_assays: int = 0
    represented_bit_trials: int = 0
    input_setting_bit_work: int = 0
    completion_tests: int = 0
    sampled_completions: int = 0
    chain_midpoints: int = 0
    pruned_intervals: int = 0
    tested_singletons: int = 0
    maximum_live_intervals: int = 0
    discovery_order: list[list[int]] = field(default_factory=list)


class JuntaDictionaryLearner:
    def __init__(self, source: CountSource, d: int, gamma: Fraction,
                 delta: Fraction, completion_rng):
        self.source, self.d = source, d
        self.gamma, self.delta = Fraction(gamma), Fraction(delta)
        self.rng = completion_rng
        self.limits = DiscoveryLimits.construct(source.component_count,
                                               source.input_dimension, d,
                                               self.gamma, self.delta)
        self.stats = AcquisitionStatistics()
        self._estimates: dict[tuple[int, tuple[int, ...]], Fraction] = {}

    def estimate(self, component: int, context: tuple[int, ...]) -> Fraction:
        key = (component, context)
        if key not in self._estimates:
            if self.stats.mean_assays >= self.limits.mean_assay_cap:
                raise AcquisitionFailure("deterministic mean-assay cap exhausted")
            n = self.limits.shots_per_assay
            count = self.source.draw_count(component, context, n)
            if not (isinstance(count, int) and 0 <= count <= n):
                raise ValueError("source returned an invalid count")
            self._estimates[key] = Fraction(count, n)
            self.stats.mean_assays += 1
            self.stats.represented_bit_trials += n
            self.stats.input_setting_bit_work += n * self.source.input_dimension
        return self._estimates[key]

    def _completion_witness(self, component: int, scope: tuple[int, ...]):
        N = self.source.input_dimension
        outside = tuple(i for i in range(N) if i not in scope)
        for assignment in product((0, 1), repeat=len(scope)):
            self.stats.completion_tests += 1
            if self.stats.completion_tests > self.limits.completion_test_cap:
                raise AcquisitionFailure("completion-test cap exhausted")
            minimum, maximum = None, None
            min_context, max_context = None, None
            # All L are sampled, although an early contrast could suffice.
            for _ in range(self.limits.completion_count):
                context = [0] * N
                for variable, bit in zip(scope, assignment):
                    context[variable] = bit
                for variable in outside:
                    context[variable] = self.rng.randrange(2)
                context = tuple(context)
                self.stats.sampled_completions += 1
                value = self.estimate(component, context)
                if minimum is None or value < minimum:
                    minimum, min_context = value, context
                if maximum is None or value > maximum:
                    maximum, max_context = value, context
            if maximum - minimum > self.gamma / 2:
                return min_context, max_context
        return None

    def _find_parent(self, component: int, left: tuple[int, ...],
                     right: tuple[int, ...], known_scope: tuple[int, ...]) -> int:
        changing = tuple(i for i in range(len(left)) if left[i] != right[i])
        if any(i in known_scope for i in changing):
            raise AssertionError("the witness must fix known parents")
        if not changing:
            raise AcquisitionFailure("positive witness has an empty chain")

        def chain_context(position):
            context = list(left)
            for variable in changing[:position]:
                context[variable] = right[variable]
            return tuple(context)

        # Level-wise traversal makes the d-live-interval promise explicit.
        level = deque([(0, len(changing))])
        while level:
            next_level = deque()
            live = 0
            for lo, hi in level:
                a = self.estimate(component, chain_context(lo))
                b = self.estimate(component, chain_context(hi))
                if abs(a - b) <= self.limits.chain_threshold:
                    self.stats.pruned_intervals += 1
                    continue
                live += 1
                if live > self.d:
                    raise AcquisitionFailure("too many nonzero chain intervals")
                if hi - lo == 1:
                    self.stats.tested_singletons += 1
                    return changing[lo]
                mid = (lo + hi) // 2
                self.estimate(component, chain_context(mid))
                self.stats.chain_midpoints += 1
                next_level.extend(((lo, mid), (mid, hi)))
            self.stats.maximum_live_intervals = max(self.stats.maximum_live_intervals,
                                                    live)
            level = next_level
        raise AcquisitionFailure("nonzero witness lost every singleton")

    def acquire(self) -> ExperimentalDictionary:
        scopes = []
        for component in range(self.source.component_count):
            # Under a zero-junta promise, all coordinates are irrelevant by
            # assumption and no observation is needed to discover the scope.
            if self.d == 0:
                scopes.append(())
                self.stats.discovery_order.append([])
                continue
            known: list[int] = []
            for stage in range(self.d + 1):
                scope = tuple(sorted(known))
                witness = self._completion_witness(component, scope)
                if witness is None:
                    scopes.append(scope)
                    self.stats.discovery_order.append(known)
                    break
                if stage == self.d:
                    raise AcquisitionFailure("contrast remains after d parents")
                parent = self._find_parent(component, *witness, scope)
                if parent in known:
                    raise AssertionError("already known parent rediscovered")
                known.append(parent)
            else:
                raise AcquisitionFailure("scope acquisition failed to stop")
        return ExperimentalDictionary(self.source, tuple(scopes))

