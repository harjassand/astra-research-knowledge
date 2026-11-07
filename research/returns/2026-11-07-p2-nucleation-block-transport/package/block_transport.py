"""Exact conditional Ising sums on a supplied ordered region.

This is NOT a two-dimensional nucleation predictor.  The exterior is frozen.
All conditional configurations are included.  Exact integer arithmetic is used
for normalizers, magnetization coefficients and comparison constants.

Spins are represented by 0 (minus) and 1 (plus).  A rational activity u=p/q
weights disagreeing edges; v=r/s weights minus spins.  Each site has its own
rate-one proposal clock in the physical comparison theorem in the report.

The sampling method takes an external getrandbits callable.  Its guarantee
requires independent fair bits; a seeded PRNG is used only by the finite tests.
"""

from dataclasses import dataclass
from fractions import Fraction
from typing import Callable, Iterable, Optional, Sequence


@dataclass(frozen=True)
class OrderedRegion:
    """Vertex labels 0,...,m-1 ARE the supplied processing order.

    boundary[i] lists the frozen exterior spin at each boundary edge incident
    to i.  Different edges may have the same frozen endpoint.  Internal edges
    are simple; internal degree plus boundary-edge count must be at most four.
    """

    m: int
    edges: tuple
    boundary: tuple
    u: Fraction
    v: Fraction

    def __post_init__(self):
        if not isinstance(self.m, int) or self.m < 1:
            raise ValueError("m must be an explicitly counted positive integer")
        u, v = Fraction(self.u), Fraction(self.v)
        if not (0 < u <= 1 and 0 < v <= 1):
            raise ValueError("activities must satisfy 0 < u,v <= 1")
        object.__setattr__(self, "u", u)
        object.__setattr__(self, "v", v)
        if len(self.boundary) != self.m:
            raise ValueError("one boundary list is required for every vertex")
        boundary = tuple(tuple(x) for x in self.boundary)
        if any(b not in (0, 1) for pins in boundary for b in pins):
            raise ValueError("boundary spins must be 0 or 1")
        edges = tuple(sorted(tuple(sorted(e)) for e in self.edges))
        if len(set(edges)) != len(edges):
            raise ValueError("internal edges must not be duplicated")
        degree = [len(pins) for pins in boundary]
        for e in edges:
            if len(e) != 2:
                raise ValueError("an edge must have exactly two endpoints")
            a, b = e
            if not (isinstance(a, int) and isinstance(b, int)
                    and 0 <= a < b < self.m):
                raise ValueError("invalid internal edge")
            degree[a] += 1
            degree[b] += 1
        if max(degree) > 4:
            raise ValueError("the stated implementation contract is degree <=4")
        object.__setattr__(self, "boundary", boundary)
        object.__setattr__(self, "edges", edges)

    @property
    def edge_count(self):
        return len(self.edges) + sum(map(len, self.boundary))

    @property
    def common_denominator(self):
        return self.u.denominator ** self.edge_count * self.v.denominator ** self.m

    @property
    def integer_bit_bound(self):
        # log2 Z_integer <= m + e log2 q + m log2 s.  bit_length
        # deliberately overestimates logs, including denominators equal to 1.
        return (1 + self.m + self.edge_count * self.u.denominator.bit_length()
                + self.m * self.v.denominator.bit_length())

    def integer_weight(self, configuration: Sequence[int]):
        if len(configuration) != self.m or any(x not in (0, 1) for x in configuration):
            raise ValueError("configuration must list m binary spins")
        d = sum(configuration[a] != configuration[b] for a, b in self.edges)
        d += sum(configuration[i] != pin
                 for i, pins in enumerate(self.boundary) for pin in pins)
        minus = self.m - sum(configuration)
        p, q = self.u.numerator, self.u.denominator
        r, s = self.v.numerator, self.v.denominator
        return p ** d * q ** (self.edge_count - d) * r ** minus * s ** (self.m - minus)


class FrontierLaw:
    """Construct the entire conditional law through frontier messages.

    Space is exponential in the supplied ordering's vertex frontier, NOT in
    the number m of variables.  No ordering-optimization oracle is invoked.
    """

    def __init__(self, region: OrderedRegion, magnetization: bool = False):
        self.region = region
        m = region.m
        past = [[] for _ in range(m)]
        future = [[] for _ in range(m)]
        for a, b in region.edges:
            past[b].append(a)
            future[a].append(b)
        self.past = past
        self.future = future

        # Frontier immediately before vertex k: processed vertices with a
        # neighbor at or after k.  Constructed from the explicit edge list.
        self.frontiers = []
        active = set()
        last_future = [max(x) if x else -1 for x in future]
        for k in range(m + 1):
            self.frontiers.append(tuple(sorted(active)))
            if k < m:
                active = {i for i in active if last_future[i] > k}
                if last_future[k] > k:
                    active.add(k)
        assert not self.frontiers[-1]
        self.frontier_width = max(map(len, self.frontiers))
        diff = [0] * (m + 1)
        for a, b in region.edges:
            diff[a + 1] += 1
            diff[b + 1] -= 1
        running = self.cutwidth = 0
        for k in range(m + 1):
            running += diff[k]
            self.cutwidth = max(self.cutwidth, running)
        assert self.frontier_width <= self.cutwidth

        self.transitions = []
        p, q = region.u.numerator, region.u.denominator
        r, s = region.v.numerator, region.v.denominator
        for k in range(m):
            front, after = self.frontiers[k], self.frontiers[k + 1]
            position = {vertex: i for i, vertex in enumerate(front)}
            if any(i not in position for i in past[k]):
                raise AssertionError("an edge endpoint was forgotten early")
            t = len(past[k]) + len(region.boundary[k])
            layer = []
            for state in range(1 << len(front)):
                choices = []
                for spin in (0, 1):
                    disagreements = sum(((state >> position[i]) & 1) != spin for i in past[k])
                    disagreements += sum(pin != spin for pin in region.boundary[k])
                    factor = p ** disagreements * q ** (t - disagreements) * (r if spin == 0 else s)
                    next_state = 0
                    for j, i in enumerate(after):
                        value = spin if i == k else (state >> position[i]) & 1
                        next_state |= value << j
                    choices.append((next_state, factor))
                layer.append(tuple(choices))
            self.transitions.append(layer)

        self.messages = [None] * (m + 1)
        self.messages[m] = [1]
        for k in range(m - 1, -1, -1):
            following = self.messages[k + 1]
            self.messages[k] = [sum(factor * following[nxt] for nxt, factor in choices)
                                for choices in self.transitions[k]]
        self.z_integer = self.messages[0][0]
        self.normalizer = Fraction(self.z_integer, region.common_denominator)
        self.count_messages = None
        self.coefficients = None
        if magnetization:
            self.add_magnetization()

    @property
    def gamma(self):
        """Proved upper bound on physical inverse gap, per-site clocks."""
        return 2 * self.region.m * self.region.u ** (-2 * self.cutwidth)

    def add_magnetization(self):
        """Integer coefficients of sum_x W_integer(x) z^(# plus spins)."""
        if self.count_messages is not None:
            return
        m = self.region.m
        tables = [None] * (m + 1)
        tables[m] = [[1]]
        for k in range(m - 1, -1, -1):
            layer = []
            for choices in self.transitions[k]:
                poly = [0] * (m - k + 1)
                for spin, (nxt, factor) in enumerate(choices):
                    for j, coefficient in enumerate(tables[k + 1][nxt]):
                        poly[j + spin] += factor * coefficient
                layer.append(poly)
            tables[k] = layer
        self.count_messages = tables
        self.coefficients = tuple(tables[0][0])
        assert sum(self.coefficients) == self.z_integer

    def count_probability(self, accepted_counts: Iterable[int]):
        self.add_magnetization()
        accepted = set(accepted_counts)
        if any(not isinstance(k, int) or not 0 <= k <= self.region.m for k in accepted):
            raise ValueError("invalid plus count")
        return Fraction(sum(self.coefficients[k] for k in accepted), self.z_integer)

    def umbrella_normalizer(self, weights: Sequence[Fraction]):
        """Exact sum for a supplied nonnegative table; no mixing assertion."""
        self.add_magnetization()
        if len(weights) != self.region.m + 1:
            raise ValueError("one umbrella weight per plus count is required")
        weights = tuple(map(Fraction, weights))
        if any(x < 0 for x in weights) or not any(weights):
            raise ValueError("umbrella weights must be nonnegative and nonzero")
        return sum((weight * coefficient for weight, coefficient in zip(weights, self.coefficients)),
                   Fraction(0)) / self.region.common_denominator

    def _branch_weights(self, k, state, remaining):
        choices = self.transitions[k][state]
        if remaining is None:
            return tuple(factor * self.messages[k + 1][nxt] for nxt, factor in choices)
        answer = []
        for spin, (nxt, factor) in enumerate(choices):
            coefficients = self.count_messages[k + 1][nxt]
            j = remaining - spin
            answer.append(factor * coefficients[j] if 0 <= j < len(coefficients) else 0)
        return tuple(answer)

    def sample(self, getrandbits: Callable[[int], int], bits_per_site: int,
               plus_count: Optional[int] = None):
        """TV error <= m*2^(-bits_per_site), including after count conditioning.

        Runtime has a fixed finite random-bit budget.  The count, if supplied,
        is satisfied exactly; approximate probabilities affect only the law
        inside that slice.  This is NOT a physical trajectory simulation.
        """
        if not isinstance(bits_per_site, int) or bits_per_site < 1:
            raise ValueError("bits_per_site must be positive")
        if plus_count is not None:
            if not isinstance(plus_count, int) or not 0 <= plus_count <= self.region.m:
                raise ValueError("invalid plus count")
            self.add_magnetization()
        state = 0
        remaining = plus_count
        output = []
        scale = 1 << bits_per_site
        for k in range(self.region.m):
            w0, w1 = self._branch_weights(k, state, remaining)
            total = w0 + w1
            if total <= 0:
                raise AssertionError("zero conditional weight on sampled path")
            draw = getrandbits(bits_per_site)
            if not isinstance(draw, int) or not 0 <= draw < scale:
                raise ValueError("random-bit provider returned an invalid integer")
            spin = int(draw * total < w1 * scale)
            state = self.transitions[k][state][spin][0]
            output.append(spin)
            if remaining is not None:
                remaining -= spin
        if remaining not in (None, 0) or state != 0:
            raise AssertionError("sampling did not terminate consistently")
        return tuple(output)

    def sample_exact(self, getrandbits: Callable[[int], int],
                     plus_count: Optional[int] = None):
        """Exactly distributed output with polynomial EXPECTED bit work.

        At each site draw a uniform integer below the rational branch total
        using binary rejection.  Every trial succeeds with probability >=1/2.
        There is no fixed worst-case random-bit budget in this method.  For
        a fixed finite budget and an explicit TV guarantee use sample().
        """
        if plus_count is not None:
            if not isinstance(plus_count, int) or not 0 <= plus_count <= self.region.m:
                raise ValueError("invalid plus count")
            self.add_magnetization()
        state, remaining = 0, plus_count
        output = []
        for k in range(self.region.m):
            w0, w1 = self._branch_weights(k, state, remaining)
            total = w0 + w1
            if total <= 0:
                raise AssertionError("zero conditional weight on sampled path")
            if not w1:
                spin = 0
            elif not w0:
                spin = 1
            else:
                bit_count = (total - 1).bit_length()
                while True:
                    draw = getrandbits(bit_count)
                    if not isinstance(draw, int) or not 0 <= draw < (1 << bit_count):
                        raise ValueError("random-bit provider returned an invalid integer")
                    if draw < total:
                        break
                spin = int(draw < w1)
            state = self.transitions[k][state][spin][0]
            output.append(spin)
            if remaining is not None:
                remaining -= spin
        assert remaining in (None, 0) and state == 0
        return tuple(output)

    def rounded_probability(self, configuration: Sequence[int], bits_per_site: int,
                            plus_count: Optional[int] = None):
        """Exact distribution of the finite-bit sampler, for tiny validation."""
        if len(configuration) != self.region.m or any(x not in (0, 1) for x in configuration):
            raise ValueError("invalid configuration")
        if plus_count is not None:
            self.add_magnetization()
            if sum(configuration) != plus_count:
                return Fraction(0)
        state, remaining, probability = 0, plus_count, Fraction(1)
        scale = 1 << bits_per_site
        for k, spin in enumerate(configuration):
            w0, w1 = self._branch_weights(k, state, remaining)
            total = w0 + w1
            if total == 0:
                return Fraction(0)
            favorable_one = (w1 * scale + total - 1) // total
            probability *= Fraction(favorable_one if spin else scale - favorable_one, scale)
            state = self.transitions[k][state][spin][0]
            if remaining is not None:
                remaining -= spin
        return probability


def precision_for_tv(m: int, eta: Fraction):
    """Smallest b>=1 with m*2^-b <= eta, using integers only."""
    eta = Fraction(eta)
    if m < 1 or not 0 < eta < 1:
        raise ValueError("m>=1 and 0<eta<1 are required")
    b = max(1, (m * eta.denominator).bit_length() - eta.numerator.bit_length())
    while eta.numerator * (1 << b) < m * eta.denominator:
        b += 1
    return b


def periodic_strip(length: int, width: int, top: Sequence[int], bottom: Sequence[int],
                   u: Fraction, v: Fraction):
    """A strip periodic along its length and with two frozen exterior rows.

    This is an actual induced strip of a larger square torus when the two
    exterior rows and geometry are consistently supplied.  No exterior law
    is acquired here.  length>=3 avoids parallel-edge conventions.
    """
    if length < 3 or width < 1 or len(top) != length or len(bottom) != length:
        raise ValueError("invalid explicitly supplied strip")
    edges = set()
    boundary = [[] for _ in range(length * width)]
    for col in range(length):
        for row in range(width):
            i = col * width + row
            j = ((col + 1) % length) * width + row
            edges.add(tuple(sorted((i, j))))
            if row + 1 < width:
                edges.add((i, i + 1))
        boundary[col * width].append(top[col])
        boundary[col * width + width - 1].append(bottom[col])
    return OrderedRegion(length * width, tuple(edges), tuple(map(tuple, boundary)), u, v)


def comparison_factor(site_count: int, blocks: Sequence[tuple]):
    """Lambda for a fixed family of (site-list, nonnegative clock, FrontierLaw).

    The caller must supply actual conditional blocks of the same full model.
    This helper checks dimensions/labels and computes the rational constant;
    it cannot infer or verify an unstated physical exterior representation.
    """
    load = [Fraction(0) for _ in range(site_count)]
    for sites, rate, law in blocks:
        rate = Fraction(rate)
        if rate < 0 or len(sites) != law.region.m or len(set(sites)) != len(sites):
            raise ValueError("invalid block sites or clock")
        for i in sites:
            if not isinstance(i, int) or not 0 <= i < site_count:
                raise ValueError("invalid site label")
            load[i] += rate * law.gamma
    return 1 + max(load, default=Fraction(0))


def first_passage_upper(time, capacity_a, capacity_b, comparison=1):
    """Rational upper bound from an ALREADY VALID all-clock capacity envelope.

    Required theorem hypotheses: C_kappa/Z_A <= a+b*kappa for every kappa>0,
    attractive chain, decreasing core, increasing target, minimal start, and
    E_aux <= comparison*E_physical.  This routine does not establish them.
    Uses e<3.  This is a one-sided bound, not an epsilon-accurate full CDF.
    """
    time, a, b, lam = map(Fraction, (time, capacity_a, capacity_b, comparison))
    if time < 0 or a < 0 or b < 0 or lam <= 0:
        raise ValueError("invalid time, capacity envelope or comparison")
    if not time:
        return Fraction(0)
    return min(Fraction(1), 3 * (lam * a * time + b))


def proposal_hit_upper(proposals, capacity_a, capacity_b, gamma_max):
    """Rational proposal-count bound, under the report's fixed-block contract.

    No actual capacity or global residence is acquired by this processor.
    """
    if not isinstance(proposals, int) or proposals < 0:
        raise ValueError("proposals must be a nonnegative integer")
    a, b, gamma = map(Fraction, (capacity_a, capacity_b, gamma_max))
    if a < 0 or b < 0 or gamma < 1:
        raise ValueError("invalid envelope or inverse-gap bound")
    if not proposals:
        return Fraction(0)
    return min(Fraction(1), 24 * gamma * a * proposals + 6 * b)

