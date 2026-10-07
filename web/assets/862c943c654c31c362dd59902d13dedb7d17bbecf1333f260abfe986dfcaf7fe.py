"""Exact, capped exchange component for the lifted XXZ trace count.

Only standard-library rational/integer arithmetic is used. The transition law
is Chen--Liu Eq. (19); its general gap is an IMPORTED preprint dependency.
This module implements transitions, not their field-acquisition FPRAS.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from fractions import Fraction as F
from itertools import combinations, product
import random


class TapeAbort(RuntimeError):
    """The entire enclosing sample/count must abort after this exception."""


@dataclass
class CoinTape:
    seed: int = 0
    bit_cap: int = 32
    choice_cap: int = 1000000
    rng: random.Random = field(init=False)
    choices: int = 0
    bits: int = 0

    def __post_init__(self):
        if self.bit_cap < 1 or self.choice_cap < 1:
            raise ValueError("positive deterministic tape caps required")
        self.rng = random.Random(self.seed)

    def bernoulli(self, p: F) -> bool:
        p = F(p)
        if not 0 <= p <= 1:
            raise ValueError("invalid rational coin")
        if p == 0:
            return False
        if p == 1:
            return True
        self.choices += 1
        if self.choices > self.choice_cap:
            raise TapeAbort("binary-choice cap")
        prefix = 0
        for used in range(1, self.bit_cap + 1):
            prefix = 2 * prefix + self.rng.getrandbits(1)
            self.bits += 1
            threshold = p.numerator << used
            if (prefix + 1) * p.denominator <= threshold:
                return True
            if prefix * p.denominator >= threshold:
                return False
        raise TapeAbort("unresolved rational coin at bit cap")

    def uniform(self, size: int) -> int:
        if size < 1:
            raise ValueError("empty uniform choice")
        lo, hi = 0, size
        while hi - lo > 1:
            mid = (lo + hi) // 2
            if self.bernoulli(F(mid - lo, hi - lo)):
                hi = mid
            else:
                lo = mid
        return lo

    def categorical(self, values: list[tuple[int, F]]) -> int:
        values = [(v, F(w)) for v, w in values if w > 0]
        if not values:
            raise ValueError("empty supported categorical choice")
        remaining = sum((w for _, w in values), F(0))
        for v, w in values[:-1]:
            if self.bernoulli(w / remaining):
                return v
            remaining -= w
        return values[-1][0]


class WeightTree:
    """Exact weighted dynamic set. O(log size) rational updates/choices."""

    def __init__(self, weights):
        weights = [F(w) for w in weights]
        if any(w < 0 for w in weights):
            raise ValueError("negative weight")
        self.size = len(weights)
        self.leaves = 1
        while self.leaves < max(1, self.size):
            self.leaves *= 2
        self.nodes = [F(0) for _ in range(2 * self.leaves)]
        for i, w in enumerate(weights):
            self.nodes[self.leaves + i] = w
        for node in range(self.leaves - 1, 0, -1):
            self.nodes[node] = self.nodes[2 * node] + self.nodes[2 * node + 1]

    @property
    def total(self):
        return self.nodes[1]

    def set(self, i, value):
        if not 0 <= i < self.size or value < 0:
            raise ValueError("invalid leaf update")
        node = self.leaves + i
        self.nodes[node] = F(value)
        node //= 2
        while node:
            self.nodes[node] = self.nodes[2 * node] + self.nodes[2 * node + 1]
            node //= 2

    def choose(self, tape: CoinTape):
        if self.total <= 0:
            raise ValueError("empty tree")
        node = 1
        while node < self.leaves:
            left = 2 * node
            if tape.bernoulli(self.nodes[left] / self.nodes[node]):
                node = left
            else:
                node = left + 1
        index = node - self.leaves
        assert index < self.size and self.nodes[node] > 0
        return index


@dataclass(frozen=True)
class LocalFactor:
    coordinates: tuple[int, ...]
    table: dict[int, F]

    def weight(self, chosen: set[int]):
        mask = sum(1 << j for j, u in enumerate(self.coordinates) if u in chosen)
        return self.table.get(mask, F(0))


@dataclass
class TraceInstance:
    n: int
    factors: list[LocalFactor]
    groups: list[tuple[tuple[int, ...], int]]
    inactive_qubits: int = 0

    def __post_init__(self):
        flat_mu = [u for f in self.factors for u in f.coordinates]
        flat_nu = [u for coords, _ in self.groups for u in coords]
        if sorted(flat_mu) != list(range(self.n)) or sorted(flat_nu) != list(range(self.n)):
            raise ValueError("both factorizations must partition the ground set")
        self.factor_of = {u: i for i, f in enumerate(self.factors) for u in f.coordinates}
        self.group_of = {u: i for i, (coords, _) in enumerate(self.groups) for u in coords}
        self.mu_degree = sum(next(iter(f.table)).bit_count() for f in self.factors)
        for f in self.factors:
            if not f.table or any(w <= 0 or m.bit_count() != next(iter(f.table)).bit_count()
                                  for m, w in f.table.items()):
                raise ValueError("positive fixed-degree local tables required")
        self.nu_degree = sum(rank for _, rank in self.groups)
        if self.mu_degree + self.nu_degree != self.n:
            raise ValueError("degrees must sum to ground-set size")

    def mu(self, chosen):
        chosen = set(chosen)
        if not chosen <= set(range(self.n)):
            return F(0)
        return product_fraction(f.weight(chosen) for f in self.factors)

    def nu(self, chosen):
        chosen = set(chosen)
        return F(int(chosen <= set(range(self.n)) and
                     all(len(chosen.intersection(coords)) == rank for coords, rank in self.groups)))

    def seed(self, mu_in=frozenset(), mu_out=frozenset(), nu_in=frozenset(), nu_out=frozenset()):
        if mu_in & mu_out or nu_in & nu_out:
            raise ValueError("inconsistent pinning")
        S, T = set(), set()
        for factor in self.factors:
            allowed = []
            for mask in sorted(factor.table):
                subset = {u for j, u in enumerate(factor.coordinates) if mask >> j & 1}
                if mu_in.intersection(factor.coordinates) <= subset and not (mu_out & subset):
                    allowed.append(subset)
            if not allowed:
                raise ValueError("empty conditioned mu factor")
            S |= allowed[0]
        for coordinates, rank in self.groups:
            forced = nu_in.intersection(coordinates)
            available = [u for u in coordinates if u not in forced and u not in nu_out]
            if len(forced) > rank or len(forced) + len(available) < rank:
                raise ValueError("empty conditioned nu quota")
            T |= set(forced) | set(available[:rank - len(forced)])
        return S, T

    def complement_symmetric(self):
        return (self.mu_degree * 2 == self.n and self.nu_degree * 2 == self.n and
                all(f.table.get(((1 << len(f.coordinates)) - 1) ^ mask, F(0)) == value
                    for f in self.factors for mask, value in f.table.items()) and
                all(2 * rank == len(coordinates) for coordinates, rank in self.groups))


def product_fraction(values):
    result = F(1)
    for value in values:
        result *= value
    return result


def edge_table(s, alpha, gamma):
    s, alpha, gamma = F(s), F(alpha), F(gamma)
    if s < 0 or alpha < abs(gamma):
        raise ValueError("outside admitted XXZ cone")
    a, b, c = 1 + s * (3 * alpha + gamma), 1 + s * (3 * alpha - gamma), 2 * s * alpha
    return {mask: value for mask, value in ((3, a), (12, a), (6, b), (9, b), (5, c), (10, c))
            if value > 0}


def field_table(s, b, c):
    s, b, c = F(s), F(b), F(c)
    if s < 0 or b < 0:
        raise ValueError("outside admitted nonnegative X field")
    r, d = b + abs(c), s * b
    u, v = 1 + s * (r - c), 1 + s * (r + c)
    return {mask: value for mask, value in ((3, d), (12, d), (5, u / 2), (9, u / 2),
                                           (6, v / 2), (10, v / 2)) if value > 0}


def compile_trace(qubits, gates):
    """gates: ('edge',(u,v),s,alpha,gamma) or ('field',(u,),s,b,c)."""
    factors, timeline, dummy = [], [[] for _ in range(qubits)], []
    field_count = 0
    for index, (kind, vertices, s, a, g) in enumerate(gates):
        start = 4 * index
        coordinates = tuple(range(start, start + 4))
        if kind == "edge":
            if len(vertices) != 2 or vertices[0] == vertices[1]:
                raise ValueError("loopless edge required")
            table = edge_table(s, a, g)
            for j, vertex in enumerate(vertices):
                timeline[vertex].append((start + j, start + 2 + j))
        elif kind == "field":
            if len(vertices) != 1:
                raise ValueError("single field vertex required")
            table = field_table(s, a, g)
            timeline[vertices[0]].append((start, start + 1))
            dummy.extend((start + 2, start + 3))
            field_count += 1
        else:
            raise ValueError("unknown gate")
        factors.append(LocalFactor(coordinates, table))
    groups, inactive = [], 0
    for visits in timeline:
        if not visits:
            inactive += 1
            continue
        for j, (row, _) in enumerate(visits):
            previous_col = visits[j - 1][1]
            groups.append(((previous_col, row), 1))
    if dummy:
        groups.append((tuple(dummy), field_count))
    return TraceInstance(4 * len(gates), factors, groups, inactive)


class LocalExchange:
    """Supported local state with exact Eq.(19) candidate cancellation."""

    def __init__(self, instance: TraceInstance, z=None, t=F(1, 16),
                 pins=(frozenset(), frozenset(), frozenset(), frozenset()), state=None):
        self.instance = instance
        self.n, self.t = instance.n, F(t)
        if self.n < 1 or not 0 < self.t <= 1:
            raise ValueError("nontrivial instance and scalar penalty in (0,1] required")
        self.z = [F(1) for _ in range(self.n)] if z is None else list(map(F, z))
        if len(self.z) != self.n or any(v <= 0 for v in self.z):
            raise ValueError("positive field required")
        self.mu_in, self.mu_out, self.nu_in, self.nu_out = map(frozenset, pins)
        self.S, self.T = instance.seed(*pins) if state is None else map(set, state)
        if (instance.mu(self.S) <= 0 or instance.nu(self.T) <= 0 or
                not self.mu_in <= self.S or self.mu_out & self.S or
                not self.nu_in <= self.T or self.nu_out & self.T):
            raise ValueError("initial state is unsupported or violates pins")
        self.Slist, self.Tlist = sorted(self.S), sorted(self.T)
        self.Spos = {u: i for i, u in enumerate(self.Slist)}
        self.Tpos = {u: i for i, u in enumerate(self.Tlist)}
        self.trees = {}
        self.local_tree_index = {}
        for j, (coordinates, _) in enumerate(instance.groups):
            if len(coordinates) > 2:
                self.trees[j] = WeightTree([self.z[u] if u not in self.T and u not in self.nu_out else 0
                                            for u in coordinates])
                self.local_tree_index.update({u: k for k, u in enumerate(coordinates)})

    def supported_weight(self):
        return (self.instance.mu(self.S) * self.instance.nu(self.T) *
                self.t ** len(self.S & self.T) *
                product_fraction(self.z[u] for u in self.S) *
                product_fraction(self.z[u] for u in self.T))

    def candidates(self, side, u):
        selected, forced, excluded = ((self.S, self.mu_in, self.mu_out) if side == 0 else
                                      (self.T, self.nu_in, self.nu_out))
        if u not in selected:
            raise ValueError("deletion requires present copy")
        if u in forced:
            return [(u, F(1))]
        rest = selected - {u}
        if side == 0:
            factor = self.instance.factors[self.instance.factor_of[u]]
            local_rest = rest.intersection(factor.coordinates)
            result = []
            for v in factor.coordinates:
                if v in rest or v in excluded:
                    continue
                subset = local_rest | {v}
                value = factor.weight(subset)
                if value > 0:
                    result.append((v, self.z[v] * value))
            return result
        coordinates, _ = self.instance.groups[self.instance.group_of[u]]
        return [(v, self.z[v]) for v in coordinates if v not in rest and v not in excluded]

    def _choose_nu(self, u, tape):
        if u in self.nu_in:
            return u
        group = self.instance.group_of[u]
        if group not in self.trees:
            return tape.categorical(self.candidates(1, u))
        tree = self.trees[group]
        # Selected u is initially absent from the eligible-complement tree.
        # Reinsertion-u is a separate positive option, so no temporary mutation
        # can survive a tape abort.
        if tape.bernoulli(self.z[u] / (self.z[u] + tree.total)):
            return u
        index = tree.choose(tape)
        return self.instance.groups[group][0][index]

    def step(self, tape):
        if len(self.Slist) + len(self.Tlist) != self.n:
            raise AssertionError("base degrees changed")
        copy = tape.uniform(self.n)
        side = int(copy >= len(self.Slist))
        u = self.Slist[copy] if side == 0 else self.Tlist[copy - len(self.Slist)]
        other = self.T if side == 0 else self.S
        if not tape.bernoulli(F(1, 2) if u in other else self.t / 2):
            return
        if side == 0:
            v = tape.categorical(self.candidates(0, u))
        else:
            v = self._choose_nu(u, tape)
        if u == v:
            return
        selected, listed, positions = ((self.S, self.Slist, self.Spos) if side == 0 else
                                      (self.T, self.Tlist, self.Tpos))
        selected.remove(u)
        selected.add(v)
        position = positions.pop(u)
        listed[position] = v
        positions[v] = position
        if side == 1:
            group = self.instance.group_of[u]
            if group in self.trees:
                self.trees[group].set(self.local_tree_index[u], self.z[u])
                self.trees[group].set(self.local_tree_index[v], F(0))

    def set_field(self, u, value):
        value = F(value)
        if value <= 0:
            raise ValueError("positive field required")
        self.z[u] = value
        group = self.instance.group_of[u]
        if group in self.trees and u not in self.T and u not in self.nu_out:
            self.trees[group].set(self.local_tree_index[u], value)

    def kernel_row(self):
        """Exact audit helper; expands only one row, not production sampling."""
        start = (frozenset(self.S), frozenset(self.T))
        row = {start: F(1)}
        for side, selected, other in ((0, self.S, self.T), (1, self.T, self.S)):
            for u in selected:
                candidates = self.candidates(side, u)
                total = sum((w for _, w in candidates), F(0))
                scale = (F(1, 2) if u in other else self.t / 2) / self.n
                for v, w in candidates:
                    if v == u:
                        continue
                    moved = frozenset((selected - {u}) | {v})
                    target = (moved, frozenset(self.T)) if side == 0 else (frozenset(self.S), moved)
                    probability = scale * w / total
                    row[target] = row.get(target, F(0)) + probability
                    row[start] -= probability
        return row


def enumerate_supports(instance, pins=(frozenset(), frozenset(), frozenset(), frozenset()),
                       pair_cap=10000):
    """Exponential diagnostic/exact-subclass helper. Never called by transitions."""
    mu_in, mu_out, nu_in, nu_out = map(set, pins)
    choices = []
    for factor in instance.factors:
        local = []
        for mask in factor.table:
            subset = frozenset(u for j, u in enumerate(factor.coordinates) if mask >> j & 1)
            if mu_in.intersection(factor.coordinates) <= subset and not mu_out.intersection(subset):
                local.append(subset)
        choices.append(local)
    Ssets = [frozenset().union(*parts) for parts in product(*choices)]
    quotas = []
    for coordinates, rank in instance.groups:
        forced = nu_in.intersection(coordinates)
        eligible = [u for u in coordinates if u not in forced and u not in nu_out]
        quotas.append([frozenset(forced) | frozenset(part)
                       for part in combinations(eligible, rank - len(forced))]
                      if 0 <= rank - len(forced) <= len(eligible) else [])
    Tsets = [frozenset().union(*parts) for parts in product(*quotas)]
    if len(Ssets) * len(Tsets) > pair_cap:
        raise ValueError("exact-enumeration admission cap exceeded")
    return [(S, T) for S in Ssets for T in Tsets]


def ceil_log2_fraction(value):
    value = F(value)
    if value <= 0:
        raise ValueError("positive value required")
    q = value.numerator // value.denominator
    k = max(0, q.bit_length() - 1)
    while F(1 << k) < value:
        k += 1
    return k


def mixing_steps(instance, t, z, tv, coefficient_range=None):
    """Sufficient gap-based step certificate, conditional on Lemma 5.5.

    From TV <= (1/2) pi_start^(-1/2) exp(-gap*j), with gap>=t/(2N).
    Binary logs upper-bound natural logs, deliberately overcounting.
    """
    n, t, tv = instance.n, F(t), F(tv)
    if not 0 < tv < 1 or not 0 < t <= 1:
        raise ValueError("invalid sampling accuracy or penalty")
    if coefficient_range is None:
        coefficient_range = product_fraction(max(f.table.values()) / min(f.table.values())
                                              for f in instance.factors)
    height = (2 * n + ceil_log2_fraction(coefficient_range) +
              n * ceil_log2_fraction(max(z) / min(z)) +
              min(instance.mu_degree, instance.nu_degree) * ceil_log2_fraction(1 / t))
    numerator = 2 * n * (height + ceil_log2_fraction(1 / tv) + 1)
    return (numerator * t.denominator + t.numerator - 1) // t.numerator


def thermal_plan(qubits, edges, fields, beta, error):
    """No allocations proportional to m: charge the actual Euler circuit first."""
    beta, error = F(beta), F(error)
    if beta < 0 or not 0 < error <= 1:
        raise ValueError("positive temperature/error interface")
    for _, _, alpha, gamma in edges:
        if F(alpha) < abs(F(gamma)):
            raise ValueError("outside XXZ cone")
    for _, b, _ in fields:
        if F(b) < 0:
            raise ValueError("negative X field")
    C = 3 * sum((F(alpha) for _, _, alpha, _ in edges), F(0)) + sum(
        (F(b) + abs(F(c)) for _, b, c in fields), F(0))
    tau = 2 * beta * C
    raw = max(F(1), 4 * tau, 20 * tau * tau / error)
    m = (raw.numerator + raw.denominator - 1) // raw.denominator
    p = len(edges) + len(fields)
    return {"qubits": qubits, "C": C, "tau": tau, "m": m, "s": beta / (2 * m),
            "local_terms": p, "gates": 2 * m * p, "ground_size": 8 * m * p,
            "log_generator_error_bound": 5 * tau * tau / m,
            "complement_symmetric": all(F(c) == 0 for _, _, c in fields)}
