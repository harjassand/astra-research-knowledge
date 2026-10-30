"""Exact and outward-rounded posterior-risk / fixed-batch design compiler.

Scientific contract: independent Beta primitive probabilities; direct Bernoulli
observations of primitives; an explicitly supplied read-once tree of bounded
multiaffine gates.  A planned batch is fixed before its outcomes.  Adaptive past
choices and local changes of the target gate are allowed and recorded.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as F
from itertools import product
from math import inf, nextafter
from typing import Callable


def down(x):
    return nextafter(x, -inf)


def up(x):
    return nextafter(x, inf)


@dataclass(frozen=True, slots=True)
class IV:
    lo: float
    hi: float

    @staticmethod
    def exact(x):
        if isinstance(x, IV):
            return x
        q = F(x)
        z = float(q)
        if F(z) == q:
            return IV(z, z)
        return IV(down(z), z) if F(z) > q else IV(z, up(z))

    def __add__(self, other):
        b = IV.exact(other)
        if b.lo == b.hi == 0:
            return self
        if self.lo == self.hi == 0:
            return b
        return IV(down(self.lo + b.lo), up(self.hi + b.hi))

    __radd__ = __add__

    def __neg__(self):
        return IV(-self.hi, -self.lo)

    def __sub__(self, other):
        return self + (-IV.exact(other))

    def __rsub__(self, other):
        return IV.exact(other) + (-self)

    def __mul__(self, other):
        b = IV.exact(other)
        if self.lo == self.hi == 0 or b.lo == b.hi == 0:
            return IV(0.0, 0.0)
        xs = (self.lo * b.lo, self.lo * b.hi,
              self.hi * b.lo, self.hi * b.hi)
        return IV(down(min(xs)), up(max(xs)))

    __rmul__ = __mul__

    def __truediv__(self, other):
        b = IV.exact(other)
        if b.lo <= 0 <= b.hi:
            raise ZeroDivisionError("interval denominator contains zero")
        return self * IV(down(1.0 / b.hi), up(1.0 / b.lo))

    def square(self):
        if self.lo <= 0 <= self.hi:
            return IV(0.0, up(max(self.lo * self.lo, self.hi * self.hi)))
        vals = (self.lo * self.lo, self.hi * self.hi)
        return IV(max(0.0, down(min(vals))), up(max(vals)))

    def bounded(self, lo, hi):
        # Used only with separately proved range constraints.
        a, b = max(lo, self.lo), min(hi, self.hi)
        if a > b:
            raise ArithmeticError("incompatible proven range")
        return IV(a, b)

    def contains(self, q):
        return F(self.lo) <= q <= F(self.hi)


def square(x):
    return x.square() if isinstance(x, IV) else x * x


def bounded(x, lo, hi):
    return x.bounded(lo, hi) if isinstance(x, IV) else x


def low(x):
    return x.lo if isinstance(x, IV) else x


def high(x):
    return x.hi if isinstance(x, IV) else x


def hull_opt(candidates):
    """Lower bound achieved by selected plan; upper bound on optimal gain."""
    best = max(range(len(candidates)), key=lambda j: low(candidates[j][0]))
    chosen, allocation = candidates[best]
    if isinstance(chosen, IV):
        return IV(chosen.lo, max(c[0].hi for c in candidates)), allocation
    return chosen, allocation


def compositions(b, k):
    if k == 1:
        yield (b,)
    else:
        for a in range(b + 1):
            for rest in compositions(b - a, k - 1):
                yield (a,) + rest


def gate_coefficients(table, make=F):
    """Truth-table values indexed by the child-bit mask -> monomial coefficients."""
    c = [make(x) for x in table]
    k = (len(table) - 1).bit_length()
    assert len(table) == 1 << k
    for j in range(k):
        bit = 1 << j
        for mask in range(1 << k):
            if mask & bit:
                c[mask] = c[mask] - c[mask ^ bit]
    return c


def shifted_derivatives(coefficients, means):
    """Exact multiaffine Taylor coefficients at the current means."""
    d = list(coefficients)
    for j, mean in enumerate(means):
        bit = 1 << j
        for mask in range(len(d)):
            if not mask & bit:
                d[mask] = d[mask] + mean * d[mask | bit]
    return d


def variance_transfer(squared_derivatives, variances):
    zero = squared_derivatives[0] * 0
    products = [zero + 1] * len(squared_derivatives)
    total = zero
    for mask in range(1, len(squared_derivatives)):
        bit = mask & -mask
        j = bit.bit_length() - 1
        products[mask] = products[mask ^ bit] * variances[j]
        total = total + squared_derivatives[mask] * products[mask]
    return bounded(total, 0, 0.25)


@dataclass(slots=True)
class Node:
    children: tuple[int, ...] = ()
    table: tuple = ()
    parent: int = -1
    alpha: F = F(0)
    beta: F = F(0)
    coefficients: list | None = None
    mean: object = None
    variance: object = None
    gain: list | None = None
    allocation: list | None = None
    derivative: list | None = None


class RiskTree:
    def __init__(self, nodes: list[Node], budget=2, interval=False):
        self.nodes = nodes
        self.root = len(nodes) - 1
        self.budget = budget
        self.interval = interval
        self.make = IV.exact if interval else F
        self.gate_rebuilds = 0
        self.leaf_rebuilds = 0
        self.candidate_evaluations = 0
        self.derivative_entries = 0
        seen = [0] * len(nodes)
        for i, node in enumerate(nodes):
            if node.children:
                assert len(set(node.children)) == len(node.children)
                assert len(node.table) == 1 << len(node.children)
                assert all(F(0) <= F(x) <= F(1) for x in node.table)
                node.coefficients = gate_coefficients(node.table, self.make)
                for ch in node.children:
                    assert 0 <= ch < i
                    nodes[ch].parent = i
                    seen[ch] += 1
            else:
                node.alpha, node.beta = F(node.alpha), F(node.beta)
                assert node.alpha > 0 and node.beta > 0
        assert seen[:-1] == [1] * (len(nodes) - 1) and seen[-1] == 0
        for i in range(len(nodes)):
            self.rebuild(i)

    def rebuild(self, i):
        node = self.nodes[i]
        if not node.children:
            a, b = self.make(node.alpha), self.make(node.beta)
            s = a + b
            node.mean = bounded(a / s, 0, 1)
            node.variance = bounded(node.mean * (1 - node.mean) / (s + 1), 0, 0.25)
            node.gain = [self.make(0)] + [bounded(node.variance * z / (s + z), 0, 0.25)
                                            for z in range(1, self.budget + 1)]
            node.allocation = [None] * (self.budget + 1)
            self.leaf_rebuilds += 1
            return
        children = [self.nodes[j] for j in node.children]
        k = len(children)
        d = shifted_derivatives(node.coefficients, [c.mean for c in children])
        ds = [square(x) for x in d]
        node.derivative = d
        node.mean = bounded(d[0], 0, 1)
        node.variance = variance_transfer(ds, [c.variance for c in children])
        node.gain = [self.make(0)]
        node.allocation = [(0,) * k]
        for budget in range(1, self.budget + 1):
            candidates = []
            for allocation in compositions(budget, k):
                active = [j for j, bj in enumerate(allocation) if bj]
                if budget <= 2:
                    gain = self.make(0)
                    for j in active:
                        gain = gain + ds[1 << j] * children[j].gain[allocation[j]]
                    if len(active) == 2:
                        j, l = active
                        gain = gain + ds[(1 << j) | (1 << l)] * children[j].gain[1] * children[l].gain[1]
                    gain = bounded(gain, 0, 0.25)
                else:
                    gain = variance_transfer(ds, [c.gain[bj] for c, bj in zip(children, allocation)])
                candidates.append((gain, allocation))
            node.gain.append(None)
            node.allocation.append(None)
            node.gain[budget], node.allocation[budget] = hull_opt(candidates)
            self.candidate_evaluations += len(candidates)
        self.gate_rebuilds += 1
        self.derivative_entries += len(d)

    def refresh_ancestors(self, i):
        while i >= 0:
            self.rebuild(i)
            i = self.nodes[i].parent

    def observe(self, leaf, outcome):
        node = self.nodes[leaf]
        assert not node.children and outcome in (0, 1)
        node.alpha += outcome
        node.beta += 1 - outcome
        self.refresh_ancestors(leaf)

    def edit_gate(self, gate, table):
        node = self.nodes[gate]
        assert node.children and len(table) == 1 << len(node.children)
        assert all(F(0) <= F(x) <= F(1) for x in table)
        node.table = tuple(table)
        node.coefficients = gate_coefficients(node.table, self.make)
        self.refresh_ancestors(gate)

    def plan(self, budget=None, node=None):
        if budget is None:
            budget = self.budget
        if node is None:
            node = self.root
        if budget == 0:
            return []
        item = self.nodes[node]
        if not item.children:
            return [node] * budget
        answer = []
        for ch, b in zip(item.children, item.allocation[budget]):
            if b:
                answer.extend(self.plan(b, ch))
        return answer

    def fixed_plan_gain(self, allocation):
        """Independent O(n) evaluation; used for exact verification."""
        vals = []
        for i, node in enumerate(self.nodes):
            if not node.children:
                b = allocation.get(i, 0)
                vals.append(node.variance * b / (self.make(node.alpha + node.beta) + b))
            else:
                ds = [square(x) for x in node.derivative]
                vals.append(variance_transfer(ds, [vals[ch] for ch in node.children]))
        return vals[-1]


def truth_table(k: int, fn: Callable):
    return tuple(fn(tuple((mask >> j) & 1 for j in range(k))) for mask in range(1 << k))


FOUR_MAJ = truth_table(4, lambda x: int(2*x[0] + sum(x[1:]) >= 3))
AND2 = (0, 0, 0, 1)
OR2 = (0, 1, 1, 1)
XOR2 = (0, 1, 1, 0)
MUX3 = truth_table(3, lambda x: x[1] if x[0] else x[2])


def balanced_tree(depth, arity=4, table=FOUR_MAJ, alpha=2, beta=2,
                  budget=2, interval=False, initial_bits=None):
    n = arity ** depth
    nodes = [Node(alpha=F(alpha), beta=F(beta)) for _ in range(n)]
    if initial_bits is not None:
        assert len(initial_bits) == n
        for node, x in zip(nodes, initial_bits):
            node.alpha += int(x)
            node.beta += 1 - int(x)
    layer = list(range(n))
    while len(layer) > 1:
        nxt = []
        for start in range(0, len(layer), arity):
            nxt.append(len(nodes))
            nodes.append(Node(children=tuple(layer[start:start+arity]), table=tuple(table)))
        layer = nxt
    return RiskTree(nodes, budget, interval)
