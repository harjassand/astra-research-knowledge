"""Exact local sampler for triangular modular dynamics over Z/MZ.

This is a research implementation of the subgroup-absorption extension in
N610_AUDIT.md. It is deliberately separate from the capital's producer code.
The random.Random source is for reproducible diagnostics, not ideal physical
randomness. Requires SymPy for exact Hermite normal form.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import lcm
import random
from typing import Callable, Sequence

from sympy import Matrix
from sympy.matrices.normalforms import hermite_normal_form


@dataclass(frozen=True)
class ModularModel:
    n: int
    c: int
    modulus: int
    s: Fraction
    r: Fraction
    parents: object
    coeffs: object
    forcing: Callable[[int, int, Sequence[tuple[int, ...]]], int]
    residual: object

    def check(self) -> None:
        assert self.n > 0 and self.c > 0 and self.modulus > 1
        assert 0 < self.s <= 1 and 0 <= self.r and self.s + self.r <= 1
        # Deliberately O(1): do not scan/acquire the N-site model to answer a
        # local query. Validate each descriptor only when it is acquired.

    def parent_list(self, site: int) -> tuple[int, ...]:
        parents = tuple(self.parents(site)) if callable(self.parents) else tuple(self.parents[site])
        if any(not (0 <= j < self.n) for j in parents):
            raise ValueError(f"invalid parent address at site {site}")
        return parents

    def layer_coeffs(self, site: int, ell: int, parent_count: int | None = None) -> tuple[int, ...]:
        values = tuple(self.coeffs(site, ell)) if callable(self.coeffs) else tuple(self.coeffs[site][ell])
        if parent_count is None:
            parent_count = len(self.parent_list(site))
        if len(values) != parent_count:
            raise ValueError(f"coefficient/parent mismatch at ({site},{ell})")
        return values

    def residual_state(self, site: int) -> tuple[int, ...]:
        values = tuple(self.residual(site)) if callable(self.residual) else tuple(self.residual[site])
        if len(values) != self.c:
            raise ValueError(f"invalid residual state at site {site}")
        return values


class EventOracle:
    """One shared independent category field, memoized by (site,time)."""

    def __init__(self, model: ModularModel, rng: random.Random):
        self.model, self.rng = model, rng
        self.den = lcm(model.s.denominator, model.r.denominator)
        self.ns = int(model.s * self.den)
        self.nr = int(model.r * self.den)
        self.events: dict[tuple[int, int], str] = {}
        self.fresh = 0
        self.parent_lookups = 0
        self.forcing_calls = 0

    def event(self, z: tuple[int, int]) -> tuple[str, bool]:
        if z in self.events:
            return self.events[z], False
        self.fresh += 1
        x = self.rng.randrange(self.den)
        kind = "haar" if x < self.ns else "residual" if x < self.ns + self.nr else "gate"
        self.events[z] = kind
        return kind, True


class Subgroup:
    """A subgroup of (Z/MZ)^m represented by its lifted integer lattice.

    B is a full-rank column basis for M Z^m <= L <= Z^m. The represented
    subgroup is L / M Z^m. HNF keeps membership and exact uniform draws simple.
    """

    def __init__(self, modulus: int, dimension: int):
        self.modulus = modulus
        self.dimension = dimension
        self.B = modulus * Matrix.eye(dimension)
        self.Binv = self.B.inv()

    def contains(self, vector: Sequence[int]) -> bool:
        v = Matrix([int(x) % self.modulus for x in vector])
        coeff = self.Binv * v
        return all(x.q == 1 for x in coeff)

    def add_image(self, vector: Sequence[int]) -> None:
        v = Matrix([int(x) % self.modulus for x in vector])
        if not self.contains(vector):
            self.B = hermite_normal_form(self.B.row_join(v))
            self.Binv = self.B.inv()

    def sample(self, rng: random.Random) -> tuple[int, ...]:
        # B maps uniform Z_M^m onto L/MZ^m with equal-size fibers.
        z = Matrix([rng.randrange(self.modulus) for _ in range(self.dimension)])
        y = self.B * z
        return tuple(int(y[i]) % self.modulus for i in range(self.dimension))


def add_pending(pending, key, vector, modulus):
    vector = tuple(int(x) % modulus for x in vector)
    if key not in pending:
        pending[key] = list(vector)
    else:
        pending[key] = [(a + b) % modulus for a, b in zip(pending[key], vector)]
    if not any(pending[key]):
        pending.pop(key)


def resolve_layer(model: ModularModel, queries, ell: int, oracle: EventOracle):
    modulus = model.modulus
    m = len(queries)
    pending = {}
    for ix, (site, t, layer) in enumerate(queries):
        assert layer == ell
        e = [0] * m
        e[ix] = 1
        add_pending(pending, (site, t), e, modulus)
    subgroup = Subgroup(modulus, m)
    offset = [0] * m
    terms = []

    while pending:
        z = max(pending, key=lambda key: (key[1], key[0]))
        v = pending.pop(z)
        # For phi(x)=v*x, im(phi) is contained in H iff v belongs to H.
        if subgroup.contains(v):
            continue
        kind, _ = oracle.event(z)
        if kind == "haar":
            # The Haar value contributes a uniform element of the cyclic image.
            subgroup.add_image(v)
        elif kind == "residual":
            a = model.residual_state(z[0])[ell] % modulus
            offset = [(x + a * y) % modulus for x, y in zip(offset, v)]
        else:
            parents = model.parent_list(z[0])
            coeffs = model.layer_coeffs(z[0], ell, len(parents))
            terms.append((tuple(v), z, parents))
            oracle.parent_lookups += len(parents)
            for parent, a in zip(parents, coeffs):
                add_pending(pending, (parent, z[1] - 1), [a * x for x in v], modulus)

    prerequisites = set()
    if ell:
        for _, (_, t), parents in terms:
            for parent in parents:
                for lower in range(ell):
                    prerequisites.add((parent, t - 1, lower))
    return offset, terms, subgroup, sorted(prerequisites)


def sample_coordinates(model: ModularModel, targets, rng=None, diagnostics=False):
    """Sample an exact joint stationary output law under ideal random bits."""
    model.check()
    rng = rng or random.Random()
    oracle = EventOracle(model, rng)
    targets = list(targets)
    for site, _, ell in targets:
        assert 0 <= site < model.n and 0 <= ell < model.c
    layer_stats = []

    def solve(ell, requested):
        if not requested:
            return []
        top = [(ix, key) for ix, key in enumerate(requested) if key[2] == ell]
        rest = [(ix, key) for ix, key in enumerate(requested) if key[2] < ell]
        if not top:
            return solve(ell - 1, requested)
        offset, terms, subgroup, prerequisites = resolve_layer(
            model, [key for _, key in top], ell, oracle
        )
        needs = [key for _, key in rest]
        seen = set(needs)
        for key in prerequisites:
            if key not in seen:
                seen.add(key)
                needs.append(key)
        lower = solve(ell - 1, needs) if needs else []
        env = dict(zip(needs, lower))
        answers = list(offset)
        for v, (site, t), parents in terms:
            rows = [tuple(env[(p, t - 1, h)] for h in range(ell)) for p in parents]
            f = model.forcing(site, ell, rows) % model.modulus
            oracle.forcing_calls += 1
            answers = [(x + a * f) % model.modulus for x, a in zip(answers, v)]
        uniform = subgroup.sample(rng)
        answers = [(x + y) % model.modulus for x, y in zip(answers, uniform)]
        out = [0] * len(requested)
        for (ix, _), value in zip(top, answers):
            out[ix] = value
        for ix, key in rest:
            out[ix] = env[key]
        layer_stats.append({"layer": ell, "targets": len(top), "prerequisites": len(prerequisites)})
        return out

    values = solve(model.c - 1, targets)
    info = {"fresh_events": oracle.fresh, "parent_lookups": oracle.parent_lookups,
            "forcing_calls": oracle.forcing_calls, "layers": layer_stats}
    return (values, info) if diagnostics else values


def dependency_cone_sample(model: ModularModel, targets, rng=None, diagnostics=False):
    """Reference perfect sampler that materializes the complete causal cone."""
    model.check()
    rng = rng or random.Random()
    oracle = EventOracle(model, rng)
    states = {}

    def state(site, t):
        z = (site, t)
        if z in states:
            return states[z]
        kind, _ = oracle.event(z)
        if kind == "haar":
            value = tuple(rng.randrange(model.modulus) for _ in range(model.c))
        elif kind == "residual":
            value = model.residual_state(site)
        else:
            parents = model.parent_list(site)
            oracle.parent_lookups += len(parents)
            parent_rows = [state(p, t - 1) for p in parents]
            out = []
            for ell in range(model.c):
                same_layer = sum(a * row[ell] for a, row in zip(model.layer_coeffs(site, ell, len(parents)), parent_rows))
                low = [tuple(row[h] for h in range(ell)) for row in parent_rows]
                oracle.forcing_calls += 1
                out.append((same_layer + model.forcing(site, ell, low)) % model.modulus)
            value = tuple(out)
        states[z] = value
        return value

    values = [state(site, t)[ell] for site, t, ell in targets]
    info = {"fresh_events": oracle.fresh, "parent_lookups": oracle.parent_lookups,
            "forcing_calls": oracle.forcing_calls}
    return (values, info) if diagnostics else values


def demo_model(n=2, modulus=4):
    """Tiny composite-ring model with nonunits, shared ancestors and lower forcing."""
    parents = ((0, 1, 1), (0, 0, 1))
    coeffs = (
        ((1, 2, 3), (2, 1, 3)),
        ((1, 3, 2), (3, 2, 1)),
    )
    residual = ((1, 0), (2, 3))
    force = lambda site, ell, rows: (
        0 if ell == 0 else (rows[0][0] * rows[-1][0] + site) % modulus
    )
    return ModularModel(n, 2, modulus, Fraction(1, 3), Fraction(1, 6),
                        parents, coeffs, force, residual)


def implicit_model(n=1_000_000, modulus=4):
    """Succinct local-oracle example; never materializes N parent/coeff arrays."""
    def parents(site):
        return ((site + 1) % n, (site * 17 + 13) % n, (site * 37 + 7) % n)

    def coeffs(site, ell):
        return tuple((site + 2 * j + ell + 1) % modulus for j in range(3))

    def residual(site):
        return (site % modulus, (site + 1) % modulus)

    def force(site, ell, rows):
        return 0 if ell == 0 else (rows[0][0] * rows[-1][0] + site) % modulus

    return ModularModel(n, 2, modulus, Fraction(1, 3), Fraction(1, 6),
                        parents, coeffs, force, residual)


if __name__ == "__main__":
    model = demo_model()
    targets = [(0, 0, 1), (1, 1, 0), (1, 0, 0)]
    rng = random.Random(6102026)
    for _ in range(5):
        print(sample_coordinates(model, targets, rng, diagnostics=True))
    large = implicit_model()
    print("implicit-N=1e6", sample_coordinates(
        large, [(3, 0, 1), (987654, 0, 1)], rng, diagnostics=True
    ))
