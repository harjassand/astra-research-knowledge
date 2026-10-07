"""Exact, exponential small-instance checks; this is not an FPRAS implementation."""
from fractions import Fraction
from functools import lru_cache
from itertools import combinations
import json
import random
import time


class Graph:
    def __init__(self):
        self.n = 0
        self.edges = {}
        self.monomers = {}

    def vertex(self):
        v = self.n
        self.n += 1
        return v

    def edge(self, u, v, w=1):
        assert u != v
        key = tuple(sorted((u, v)))
        assert key not in self.edges
        self.edges[key] = Fraction(w)

    def monomer(self, v, w=1):
        self.monomers[v] = Fraction(w)

    def count(self, deleted=()):
        adj = [[] for _ in range(self.n)]
        for (u, v), w in self.edges.items():
            if w:
                adj[u].append((v, w))
                adj[v].append((u, w))

        @lru_cache(None)
        def rec(mask):
            if not mask:
                return Fraction(1)
            if not self.monomers and mask.bit_count() % 2:
                return Fraction(0)
            # Choosing the least-degree remaining vertex reduces the exact check.
            verts = [v for v in range(self.n) if mask >> v & 1]
            u = min(verts, key=lambda v: sum(mask >> z & 1 for z, _ in adj[v]))
            rest = mask ^ (1 << u)
            return self.monomers.get(u, Fraction(0)) * rec(rest) + sum(
                (w * rec(rest ^ (1 << v)) for v, w in adj[u]
                 if rest >> v & 1), Fraction(0))

        mask = (1 << self.n) - 1
        for v in deleted:
            mask &= ~(1 << v)
        return rec(mask)


def parity_city(g, d, parity):
    """Ports have signature 1 exactly when deleted-port parity is parity."""
    assert d >= 0 and parity in (0, 1)
    if d == 0:
        if parity:
            g.vertex()  # Unmatchable, correctly representing infeasibility.
        return []
    if d == 1:
        a = g.vertex()
        if parity == 0:
            g.edge(a, g.vertex())
        return [a]
    if d == 2 and parity == 0:
        a, b = g.vertex(), g.vertex()
        g.edge(a, b)
        return [a, b]
    # A cubic tree with D leaves has D-2 triangle nodes. The parity of its
    # external selected edges is D-2 (mod 2). Add one inactive port if needed.
    D = d if d % 2 == parity else d + 1
    node_count = D - 2
    ports = []
    previous_out = None
    for i in range(node_count):
        tri = [g.vertex() for _ in range(3)]
        for a, b in combinations(tri, 2):
            g.edge(a, b)
        if previous_out is not None:
            g.edge(previous_out, tri[0])
        else:
            ports.append(tri[0])
        ports.append(tri[1])
        if i + 1 < node_count:
            previous_out = tri[2]
        else:
            ports.append(tri[2])
    assert len(ports) == D
    return ports[:d]  # Any extra port is inactive: no external edge is attached.


def syndrome_graph(n, edges, weights, syndrome):
    g = Graph()
    incidence = [[] for _ in range(n)]
    for j, (u, v) in enumerate(edges):
        incidence[u].append(j)
        incidence[v].append(j)
    port = {}
    for v, inds in enumerate(incidence):
        pv = parity_city(g, len(inds), syndrome >> v & 1)
        for j, p in zip(inds, pv):
            port[v, j] = p
    for j, (u, v) in enumerate(edges):
        g.edge(port[u, j], port[v, j], weights[j])
    return g


def direct_syndrome(n, edges, weights):
    out = [Fraction(0) for _ in range(1 << n)]
    for x in range(1 << len(edges)):
        s, w = 0, Fraction(1)
        for j, (u, v) in enumerate(edges):
            if x >> j & 1:
                s ^= (1 << u) | (1 << v)
                w *= weights[j]
        out[s] += w
    return out


def integer_signature(g, P):
    """Returns ports a,b with counts full=1 and ports-deleted=P."""
    assert P >= 1
    # A simple DAG whose number of source-to-target paths has binary recurrence.
    arcs = [(0, 1)]
    node_count, previous = 2, 1
    for bit in bin(P)[3:]:
        current, helper = node_count, node_count + 1
        node_count += 2
        arcs += [(previous, current), (previous, helper), (helper, current)]
        if bit == "1":
            arcs.append((0, current))
        previous = current
    source, target = 0, previous
    left = {v: g.vertex() for v in range(node_count) if v != target}
    right = {v: g.vertex() for v in range(node_count) if v != source}
    for v in range(node_count):
        if v not in (source, target):
            g.edge(left[v], right[v])
    for u, v in arcs:
        g.edge(left[u], right[v])
    a, b = g.vertex(), g.vertex()
    g.edge(a, left[source])
    g.edge(b, right[target])
    return a, b


def integer_edge(g, u, v, P):
    if P == 1:
        g.edge(u, v)
    else:
        a, b = integer_signature(g, P)
        g.edge(u, a)
        g.edge(v, b)


def unweight(g):
    """#PM(new)=product(denominators)*weighted-PM(g), exact, poly-bit size."""
    h = Graph()
    for _ in range(g.n):
        h.vertex()
    factor = 1
    for (u, v), w in g.edges.items():
        if not w:
            continue
        P, Q = w.numerator, w.denominator
        factor *= Q
        if Q == 1:
            integer_edge(h, u, v, P)
        else:
            c, d = h.vertex(), h.vertex()
            integer_edge(h, u, c, P)
            integer_edge(h, c, d, Q)
            integer_edge(h, d, v, 1)
    return h, factor


def binary_subspaces(n):
    known = {frozenset([0])}
    queue = [frozenset([0])]
    for C in queue:
        for x in range(1, 1 << n):
            if x not in C:
                D = C | frozenset(x ^ y for y in C)
                if D not in known:
                    known.add(D)
                    queue.append(D)
    return queue


def affine_classification_check(n, C, monomers=False):
    even = monomers or all(x.bit_count() % 2 == 0 for x in C)
    exchange = even and all(
        (monomers and (1 << i) in C) or
        any((1 << i) ^ (1 << j) in C for j in range(n)
            if j != i and z >> j & 1)
        for z in C for i in range(n) if z >> i & 1
    )
    generated = {0}
    for z in C:
        if z.bit_count() == 2 or (monomers and z.bit_count() == 1):
            generated |= {x ^ z for x in generated}
    return exchange, generated == set(C)


def exchange_graph_checks(g, d, monomers=False):
    f = [g.count([i for i in range(d) if s >> i & 1])
         for s in range(1 << d)]
    tested = 0
    for s in range(1 << d):
        for t in range(1 << d):
            diff = s ^ t
            for i in range(d):
                if not diff >> i & 1:
                    continue
                rhs = sum((f[s ^ (1 << i) ^ (1 << j)] *
                           f[t ^ (1 << i) ^ (1 << j)]
                           for j in range(d) if j != i and diff >> j & 1),
                          Fraction(0))
                if monomers:
                    rhs += f[s ^ (1 << i)] * f[t ^ (1 << i)]
                assert f[s] * f[t] <= rhs, (s, t, i, f)
                tested += 1
    # The square-root-free polynomial form of GHZ fidelity <= 1/2 is
    # (sum_{nonendpoint} f)^2 >= 4 f(empty) f(all).
    leakage = sum(f[1:-1], Fraction(0))
    assert leakage ** 2 >= 4 * f[0] * f[-1]
    return tested


def echelon(vectors):
    rows = {}
    for x in vectors:
        for p in sorted(rows, reverse=True):
            if x >> p & 1:
                x ^= rows[p]
        if x:
            rows[x.bit_length() - 1] = x
    return rows


def canonical(x, rows):
    for p in sorted(rows, reverse=True):
        if x >> p & 1:
            x ^= rows[p]
    return x


def logical_subgraph_checks(n, edges):
    cycle = []
    for x in range(1 << len(edges)):
        s = 0
        for j, (u, v) in enumerate(edges):
            if x >> j & 1:
                s ^= (1 << u) | (1 << v)
        if not s:
            cycle.append(x)
    cb = list(echelon(cycle).values())
    checked = 0
    for abstract in binary_subspaces(len(cb)):
        C = {__import__('functools').reduce(int.__xor__,
            (row for j, row in enumerate(cb) if x >> j & 1), 0)
             for x in abstract}
        rows = echelon(C)
        deleted = sum(1 << p for p in rows)
        survivors = [x for x in cycle if not x & deleted]
        logical = {canonical(x, rows) for x in cycle}
        assert len(survivors) == len(logical)
        assert {canonical(x, rows) for x in survivors} == logical
        assert set(survivors) & C == {0}
        if len(logical) > 1:
            dx = min(x.bit_count() for x in cycle if x not in C)
            gp = min(x.bit_count() for x in survivors if x)
            assert dx <= gp
        checked += 1
    return checked


def exact_cover_syndrome_checks():
    """Column-weight-three reduction; no counting algorithm is implemented."""
    checks = families = concentration = 0
    for n in (3, 6):
        universe = list(combinations(range(n), 3))
        for m in range(min(3, len(universe)) + 1):
            for edges in combinations(universe, m):
                families += 1
                lam = Fraction(1, 1 << (m + 3))
                total = low = Fraction(0)
                for x in range(1 << m):
                    degrees = [0] * n
                    for j, triple in enumerate(edges):
                        if x >> j & 1:
                            for v in triple:
                                degrees[v] += 1
                    syndrome_valid = all(d % 2 == 1 for d in degrees)
                    cover = all(d == 1 for d in degrees)
                    assert (syndrome_valid and x.bit_count() <= n // 3) == cover
                    checks += 1
                    if syndrome_valid:
                        w = lam ** x.bit_count()
                        total += w
                        if cover:
                            low += w
                if low:
                    assert (total - low) / total <= (1 << m) * lam
                    concentration += 1
    return families, checks, concentration


def run():
    t0 = time.time()
    stats = {}
    profiles = 0
    for d in range(8):
        for parity in (0, 1):
            g = Graph()
            ports = parity_city(g, d, parity)
            for x in range(1 << d):
                deleted = [ports[i] for i in range(d) if x >> i & 1]
                got = g.count(deleted)
                assert got == int(x.bit_count() % 2 == parity), (d, parity, x, got)
                profiles += 1
    stats["parity_signature_profiles"] = profiles
    integer_profiles = 0
    max_integer_vertices = 0
    for P in range(1, 129):
        g = Graph()
        a, b = integer_signature(g, P)
        assert g.count() == 1, P
        assert g.count([a, b]) == P, P
        assert g.count([a]) == g.count([b]) == 0, P
        integer_profiles += 4
        max_integer_vertices = max(max_integer_vertices, g.n)
    stats["integer_signature_profiles"] = integer_profiles
    stats["max_integer_test_vertices"] = max_integer_vertices
    rng = random.Random(20261007)
    syndrome_tests = rational_tests = 0
    logical_checks = 0
    max_matching_vertices = 0
    for n in range(1, 5):
        universe = list(combinations(range(n), 2))
        for mask in range(1 << len(universe)):
            edges = [e for j, e in enumerate(universe) if mask >> j & 1]
            logical_checks += logical_subgraph_checks(n, edges)
            weights = [Fraction(rng.randint(0, 5), rng.randint(1, 5)) for _ in edges]
            expected = direct_syndrome(n, edges, weights)
            for s in range(1 << n):
                g = syndrome_graph(n, edges, weights, s)
                assert g.count() == expected[s], (n, edges, weights, s)
                syndrome_tests += 1
                # The rational-to-unweighted check is expensive exponential
                # counting, so run it on graphs with at most three edges.
                if len(edges) <= 3:
                    h, factor = unweight(g)
                    assert h.count() == factor * expected[s], (n, edges, s)
                    rational_tests += 1
                    max_matching_vertices = max(max_matching_vertices, h.n)
    stats["graph_syndrome_weighted_identities"] = syndrome_tests
    stats["rational_unweighted_identities"] = rational_tests
    stats["max_unweighted_test_vertices"] = max_matching_vertices
    stats["graph_CSS_logical_subgraph_checks"] = logical_checks
    classified = 0
    classified_passes = {}
    monomer_classified_passes = {}
    for n in range(1, 7):
        passing = 0
        monomer_passing = 0
        for C in binary_subspaces(n):
            exchange, generated = affine_classification_check(n, C)
            assert exchange == generated, (n, C)
            classified += 1
            passing += exchange
            exchange, generated = affine_classification_check(n, C, True)
            assert exchange == generated, (n, C, "monomers")
            monomer_passing += exchange
        classified_passes[str(n)] = passing
        monomer_classified_passes[str(n)] = monomer_passing
    stats["binary_linear_subspaces_classified"] = classified
    stats["matching_realizable_spaces_by_dimension"] = classified_passes
    stats["monomer_matching_realizable_spaces_by_dimension"] = monomer_classified_passes
    exchange_tests = 0
    exchange_graphs = 0
    for N in (4, 5):
        universe = list(combinations(range(N), 2))
        for mask in range(1 << len(universe)):
            g = Graph()
            for _ in range(N):
                g.vertex()
            for j, (u, v) in enumerate(universe):
                if mask >> j & 1:
                    g.edge(u, v, Fraction(rng.randint(1, 5), rng.randint(1, 5)))
            exchange_tests += exchange_graph_checks(g, 4)
            exchange_graphs += 1
    # Nonterminal auxiliary vertices and six ports are also exercised.
    for _ in range(64):
        g = Graph()
        for _ in range(8):
            g.vertex()
        for u, v in combinations(range(8), 2):
            if rng.random() < 0.4:
                g.edge(u, v, Fraction(rng.randint(1, 5), rng.randint(1, 5)))
        exchange_tests += exchange_graph_checks(g, 6)
        exchange_graphs += 1
    stats["weighted_exchange_graphs"] = exchange_graphs
    stats["weighted_exchange_inequalities"] = exchange_tests
    stats["GHZ_leakage_inequalities"] = exchange_graphs
    monomer_exchange_tests = monomer_graphs = 0
    for N in (3, 4):
        universe = list(combinations(range(N), 2))
        for mask in range(1 << len(universe)):
            g = Graph()
            for _ in range(N):
                v = g.vertex()
                g.monomer(v, Fraction(rng.randint(0, 5), rng.randint(1, 5)))
            for j, (u, v) in enumerate(universe):
                if mask >> j & 1:
                    g.edge(u, v, Fraction(rng.randint(1, 5), rng.randint(1, 5)))
            monomer_exchange_tests += exchange_graph_checks(g, N, True)
            monomer_graphs += 1
    for d in (3, 4, 6):
        for _ in range(32):
            g = Graph()
            for _ in range(8):
                v = g.vertex()
                g.monomer(v, Fraction(rng.randint(0, 5), rng.randint(1, 5)))
            for u, v in combinations(range(8), 2):
                if rng.random() < 0.4:
                    g.edge(u, v, Fraction(rng.randint(1, 5), rng.randint(1, 5)))
            monomer_exchange_tests += exchange_graph_checks(g, d, True)
            monomer_graphs += 1
    stats["monomer_weighted_exchange_graphs"] = monomer_graphs
    stats["monomer_weighted_exchange_inequalities"] = monomer_exchange_tests
    stats["monomer_GHZ_leakage_inequalities"] = monomer_graphs
    families, checks, concentration = exact_cover_syndrome_checks()
    stats["column_weight_three_X3C_families"] = families
    stats["column_weight_three_X3C_subset_identities"] = checks
    stats["column_weight_three_low_temperature_bounds"] = concentration
    stats["seconds"] = round(time.time() - t0, 3)
    stats["scope"] = "Exact exponential finite checks; no FPRAS or coherent compiler run."
    return stats


if __name__ == "__main__":
    result = run()
    print(json.dumps(result, indent=2))
    with open("work/cycle1/combinatorics_matching_checks.json", "w") as f:
        json.dump(result, f, indent=2)
        f.write("\n")
