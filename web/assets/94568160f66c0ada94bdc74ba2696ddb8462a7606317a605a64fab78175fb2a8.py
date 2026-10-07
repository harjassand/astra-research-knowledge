"""Implicit higher-spin projectors, positive Taylor gates and exact Eq19 chain.

Projector supports are never expanded by production code. Diagnostic enumeration
is separately capped. General mixing uses imported Chen--Liu Lemma5.5.
"""
from dataclasses import dataclass
from fractions import Fraction as F
from itertools import combinations, product
from math import comb, factorial
from pathlib import Path
import sys

OWN = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(OWN))
from xxz_local_chain import (LocalFactor, LocalExchange, WeightTree, CoinTape,
                             TapeAbort, product_fraction, ceil_log2_fraction,
                             mixing_steps)
from nofield_counter import ResourceRefusal


def table_degree(factor):
    return factor.q if isinstance(factor, ProjectorFactor) else next(iter(factor.table)).bit_count()


@dataclass(frozen=True)
class ProjectorFactor:
    rows: tuple
    cols: tuple

    @property
    def q(self):
        return len(self.rows)

    @property
    def coordinates(self):
        return self.rows + self.cols

    def weight(self, chosen):
        selected = set(chosen).intersection(self.coordinates)
        if len(selected) != self.q:
            return F(0)
        return F(1, comb(self.q, len(selected.intersection(self.rows))))


class ImplicitTrace:
    def __init__(self, n, factors, groups, first_rows, qubits):
        self.n, self.factors, self.groups = n, factors, groups
        self.first_rows, self.qubits = first_rows, qubits
        self.inactive_qubits = qubits - len(first_rows)
        if sorted(u for f in factors for u in f.coordinates) != list(range(n)):
            raise ValueError("mu factors must partition all coordinates")
        if sorted(u for coords, _ in groups for u in coords) != list(range(n)):
            raise ValueError("nu quotas must partition all coordinates")
        self.factor_of = {u: j for j, f in enumerate(factors) for u in f.coordinates}
        self.group_of = {u: j for j, (coords, _) in enumerate(groups) for u in coords}
        self.mu_degree = sum(table_degree(f) for f in factors)
        self.nu_degree = sum(rank for _, rank in groups)
        if 2 * self.mu_degree != n or self.mu_degree != self.nu_degree:
            raise ValueError("trace factors must have half degree")
        for f in factors:
            if isinstance(f, ProjectorFactor):
                if f.q < 1 or len(f.cols) != f.q:
                    raise ValueError("nonempty equal row/column projector arity")
            elif any(v <= 0 or m.bit_count() != table_degree(f) for m, v in f.table.items()):
                raise ValueError("positive fixed-degree local table required")

    def mu(self, chosen):
        chosen = set(chosen)
        if len(chosen) != self.mu_degree or not chosen <= set(range(self.n)):
            return F(0)
        return product_fraction(f.weight(chosen) for f in self.factors)

    def nu(self, chosen):
        chosen = set(chosen)
        return F(int(chosen <= set(range(self.n)) and
                     all(len(chosen.intersection(c)) == r for c, r in self.groups)))

    def seed(self, mu_in=frozenset(), mu_out=frozenset(), nu_in=frozenset(), nu_out=frozenset()):
        mu_in, mu_out, nu_in, nu_out = map(frozenset, (mu_in, mu_out, nu_in, nu_out))
        if mu_in & mu_out or nu_in & nu_out:
            raise ValueError("inconsistent pins")
        if not (mu_in | mu_out | nu_in | nu_out) <= set(range(self.n)):
            raise ValueError("pins outside ground set")
        S, T = set(), set()
        for f in self.factors:
            forced = mu_in.intersection(f.coordinates)
            if isinstance(f, ProjectorFactor):
                available = [u for u in f.coordinates if u not in forced and u not in mu_out]
                need = f.q - len(forced)
                if not 0 <= need <= len(available):
                    raise ValueError("empty pinned projector")
                S.update(forced); S.update(available[:need])
            else:
                for m in sorted(f.table):
                    selected = {u for j, u in enumerate(f.coordinates) if m >> j & 1}
                    if forced <= selected and not selected & mu_out:
                        S.update(selected); break
                else:
                    raise ValueError("empty pinned quadratic factor")
        for coords, rank in self.groups:
            forced = nu_in.intersection(coords)
            available = [u for u in coords if u not in forced and u not in nu_out]
            need = rank - len(forced)
            if not 0 <= need <= len(available):
                raise ValueError("empty pinned nu quota")
            T.update(forced); T.update(available[:need])
        return S, T

    def coefficient_range(self):
        return product_fraction(comb(f.q, f.q // 2) if isinstance(f, ProjectorFactor)
                                else max(f.table.values()) / min(f.table.values())
                                for f in self.factors)

    def complement_ratio(self):
        if any(2 * rank != len(coords) for coords, rank in self.groups):
            raise ValueError("nu support must be complement invariant")
        ratio = F(1)
        for f in self.factors:
            if isinstance(f, ProjectorFactor):
                continue
            full = (1 << len(f.coordinates)) - 1
            if any(full ^ m not in f.table for m in f.table):
                raise ValueError("mu support not complement invariant")
            ratio *= max(v / f.table[full ^ m] for m, v in f.table.items())
        return ratio

    def complement_symmetric(self):
        return self.complement_ratio() == 1


def mm(A, B):
    return [[sum((A[i][k] * B[k][j] for k in range(len(B))), F(0))
             for j in range(len(B[0]))] for i in range(len(A))]


def taylor_matrix(A, s, degree):
    if not 1 <= degree <= 12 or F(s) < 0:
        raise ValueError("positive Taylor degree/step admission")
    d = len(A)
    result = power = [[F(i == j) for j in range(d)] for i in range(d)]
    for k in range(1, degree + 1):
        power = mm(power, A)
        result = [[result[i][j] + F(s) ** k * power[i][j] / factorial(k)
                   for j in range(d)] for i in range(d)]
    return result


@dataclass(frozen=True)
class Gate:
    kind: str
    vertices: tuple
    table: tuple = ()


def local_gate(kind, vertices, s, a, g, degree=2):
    a, g = F(a), F(g)
    if kind == "edge":
        if a < abs(g) or len(vertices) != 2 or vertices[0] == vertices[1]:
            raise ValueError("loopless easy-plane edge required")
        A = [[3*a+g,0,0,0],[0,3*a-g,2*a,0],[0,2*a,3*a-g,0],[0,0,0,3*a+g]]
    elif kind == "field":
        if a < 0 or len(vertices) != 1:
            raise ValueError("nonnegative X field required")
        r = a + abs(g)
        A = [[r+g,a],[a,r-g]]
    else:
        raise ValueError("unknown local gate")
    G = taylor_matrix(A, F(s), degree)
    return Gate(kind, tuple(vertices), tuple(map(tuple, G)))


def compile_projected_trace(qubits, gates, *, coordinate_cap=100000):
    required = sum(2 * len(g.vertices) + (2 if g.kind == "field" else 0) for g in gates)
    if required > coordinate_cap:
        raise ValueError("circuit coordinate admission exceeded before allocation")
    factors, timeline, dummies, first_rows = [], [[] for _ in range(qubits)], [], {}
    cursor = 0
    for g in gates:
        if not g.vertices or len(set(g.vertices)) != len(g.vertices) or any(not 0 <= v < qubits for v in g.vertices):
            raise ValueError("distinct legal gate vertices required")
        q = len(g.vertices)
        rows = tuple(range(cursor, cursor + q)); cursor += q
        cols = tuple(range(cursor, cursor + q)); cursor += q
        dummy = tuple(range(cursor, cursor + 2)) if g.kind == "field" else ()
        cursor += len(dummy)
        if g.kind == "projector":
            factors.append(ProjectorFactor(rows, cols))
        else:
            coords, table = rows + cols + dummy, {}
            for selected in combinations(range(len(coords)), 2):
                mask = sum(1 << j for j in selected)
                row = sum(((mask >> j) & 1) << j for j in range(q))
                col = sum((1 - ((mask >> (q+j)) & 1)) << j for j in range(q))
                value = F(g.table[row][col])
                if g.kind == "field" and row == col:
                    value /= 2
                if value:
                    table[mask] = value
            factors.append(LocalFactor(coords, table))
        dummies.extend(dummy)
        for j, v in enumerate(g.vertices):
            timeline[v].append((rows[j], cols[j]))
            first_rows.setdefault(v, rows[j])
    groups = []
    for visits in timeline:
        for j, (row, _) in enumerate(visits):
            groups.append(((visits[j-1][1], row), 1))
    if dummies:
        groups.append((tuple(dummies), len(dummies) // 2))
    return ImplicitTrace(cursor, factors, groups, first_rows, qubits)


class ProjectedExchange(LocalExchange):
    """Production projectors use two trees and integer class weights, no binomial."""
    def __init__(self, instance, z=None, t=F(1, 16), pins=(frozenset(),)*4, state=None):
        super().__init__(instance, z=z, t=t, pins=pins, state=state)
        self.projectors, self.projector_location = {}, {}
        for j, f in enumerate(instance.factors):
            if not isinstance(f, ProjectorFactor):
                continue
            trees = tuple(WeightTree([self.z[u] if u not in self.S and u not in self.mu_out else 0
                                      for u in group]) for group in (f.rows, f.cols))
            self.projectors[j] = [trees, len(self.S.intersection(f.rows))]
            for side, group in enumerate((f.rows, f.cols)):
                for k, u in enumerate(group):
                    self.projector_location[u] = (j, side, k)

    def _choose_mu(self, u, tape):
        if u in self.mu_in:
            return u
        j = self.instance.factor_of[u]
        if j not in self.projectors:
            return tape.categorical(self.candidates(0, u))
        f = self.instance.factors[j]
        trees, row_count = self.projectors[j]
        _, side_u, _ = self.projector_location[u]
        r = row_count - int(side_u == 0)
        assert 0 <= r < f.q
        # Multiply both exact binomial weights by their common positive scale.
        # 1/binom(q,r+1) : 1/binom(q,r) = (r+1) : (q-r).
        scales = (r + 1, f.q - r)
        totals = [scales[k] * (trees[k].total + (self.z[u] if k == side_u else 0)) for k in (0,1)]
        side = 0 if tape.bernoulli(totals[0] / sum(totals, F(0))) else 1
        eligible_total = trees[side].total + (self.z[u] if side == side_u else 0)
        if side == side_u and tape.bernoulli(self.z[u] / eligible_total):
            return u
        k = trees[side].choose(tape)
        return (f.rows, f.cols)[side][k]

    def step(self, tape):
        copy = tape.uniform(self.n)
        side = int(copy >= len(self.Slist))
        u = self.Slist[copy] if side == 0 else self.Tlist[copy-len(self.Slist)]
        other = self.T if side == 0 else self.S
        if not tape.bernoulli(F(1,2) if u in other else self.t / 2):
            return
        v = self._choose_mu(u,tape) if side == 0 else self._choose_nu(u,tape)
        if u == v:
            return
        selected, listed, positions = ((self.S,self.Slist,self.Spos) if side == 0 else
                                       (self.T,self.Tlist,self.Tpos))
        selected.remove(u); selected.add(v)
        pos = positions.pop(u); listed[pos] = v; positions[v] = pos
        if side == 0 and self.instance.factor_of[u] in self.projectors:
            j, su, ku = self.projector_location[u]
            jj, sv, kv = self.projector_location[v]
            assert j == jj
            trees, row_count = self.projectors[j]
            trees[su].set(ku, self.z[u]); trees[sv].set(kv,F(0))
            self.projectors[j][1] = row_count + int(sv == 0) - int(su == 0)
        elif side == 1:
            group = self.instance.group_of[u]
            if group in self.trees:
                self.trees[group].set(self.local_tree_index[u],self.z[u])
                self.trees[group].set(self.local_tree_index[v],F(0))

    def set_field(self, u, value):
        super().set_field(u,value)
        if u in self.projector_location and u not in self.S and u not in self.mu_out:
            j, side, k = self.projector_location[u]
            self.projectors[j][0][side].set(k,F(value))


def sampler_plan(instance, tv=F(1,4), *, allow_bounded_bias=False):
    tv = F(tv)
    if not 0 < tv <= F(1,4) or instance.n < 1:
        raise ValueError("nontrivial trace and TV in (0,1/4] required")
    bias = instance.complement_ratio()
    if bias != 1 and not allow_bounded_bias:
        raise ValueError("numeric bias must be admitted explicitly")
    n = instance.n
    t = F(1, 256*n*n) / bias
    tries = ceil_log2_fraction(4/tv)
    theta = tv/(4*tries)
    steps = mixing_steps(instance,t,[F(1)]*n,theta,instance.coefficient_range())
    height = max(1,(n-1).bit_length())
    choices = tries * steps * (2*height+3) + instance.inactive_qubits
    bits = ceil_log2_fraction(4*choices/tv)
    return {"n":n,"t":t,"complement_ratio":bias,"tv":tv,"tries":tries,
            "soft_tv":theta,"steps_per_try":steps,"total_steps":tries*steps,
            "choice_cap":choices,"bits_per_choice":bits,"random_bits_cap":choices*bits,
            "coefficient_range":instance.coefficient_range(),
            "scope":"Source-conditional mixing; independent fair bits. Seeded replay is not an entropy certificate."}


def sample_projected(instance, qsets, tv=F(1,4), *, max_steps=10000000, seed=0,
                     allow_bounded_bias=False):
    """Return physical site Sz charges for a layerwise projected spin circuit.

    The trace cut precedes B0. Individual constituent bits are auxiliary; site
    charge projectors commute with Pi, so their aggregated law equals that of
    (Pi B0 Pi)**m on the symmetric spin space. A general constituent observable
    cannot use this trace-cut readout without an additional projector.
    """
    if sorted(v for qs in qsets for v in qs)!=list(range(instance.qubits)):
        raise ValueError("physical site constituent sets must partition qubits")
    plan = sampler_plan(instance,tv,allow_bounded_bias=allow_bounded_bias)
    if plan["total_steps"] > max_steps:
        raise ResourceRefusal(plan)
    tape = CoinTape(seed,plan["bits_per_choice"],plan["choice_cap"])
    executed = attempts = 0
    try:
        for _ in range(plan["tries"]):
            attempts += 1
            chain = ProjectedExchange(instance,t=plan["t"])
            for _ in range(plan["steps_per_try"]):
                chain.step(tape); executed += 1
            if not chain.S.isdisjoint(chain.T):
                continue
            bits = [int(instance.first_rows[v] in chain.S) if v in instance.first_rows
                    else int(tape.bernoulli(F(1,2))) for v in range(instance.qubits)]
            return {"accepted":True,"aborted":False,"bits":bits,
                    "twice_Sz":[len(qs)-2*sum(bits[v] for v in qs) for qs in qsets],
                    "S":sorted(chain.S),"T":sorted(chain.T),"plan":plan,
                    "steps":executed,"attempts":attempts,"coin_choices":tape.choices,"coin_bits":tape.bits}
        reason = "hard rejection cap"
    except TapeAbort as e:
        reason = str(e)
    return {"accepted":False,"aborted":reason != "hard rejection cap","bits":[0]*instance.qubits,
            "twice_Sz":[len(qs) for qs in qsets],"plan":plan,"steps":executed,
            "attempts":attempts,"coin_choices":tape.choices,"coin_bits":tape.bits,
            "fallback_reason":reason}


def enumerate_pairs(instance, *, pair_cap=10000):
    """Bounded exponential audit; never called in production sampling."""
    support_mu = []
    for f in instance.factors:
        count = comb(len(f.coordinates),table_degree(f)) if isinstance(f,ProjectorFactor) else len(f.table)
        support_mu.append(count)
    count_mu = 1
    for c in support_mu: count_mu *= c
    count_nu = 1
    for coords, rank in instance.groups: count_nu *= comb(len(coords),rank)
    if count_mu*count_nu > pair_cap:
        raise ValueError("pair enumeration refused before support allocation")
    choices = []
    for f in instance.factors:
        choices.append([frozenset(c) for c in combinations(f.coordinates,f.q)] if isinstance(f,ProjectorFactor)
                       else [frozenset(u for j,u in enumerate(f.coordinates) if m >> j & 1) for m in f.table])
    S = [frozenset().union(*local) for local in product(*choices)]
    quotas = [[frozenset(c) for c in combinations(coords,rank)] for coords,rank in instance.groups]
    T = [frozenset().union(*local) for local in product(*quotas)]
    return [(s,t) for s in S for t in T]
