#!/usr/bin/env python3
"""Exact finite verification of a SAT research continuation.

The CNF compiler is uniform and polynomial. The reference contractions and
matrix tests enumerate states; they are NOT a polynomial SAT algorithm.
Only standard-library integer and rational arithmetic is used.
"""
from collections import defaultdict
from fractions import Fraction as Q
from itertools import product, permutations
from math import comb, factorial, prod
from pathlib import Path
import json
import random

ROOT = Path(__file__).resolve().parent


def valuation(x):
    x = Q(x)
    if not x:
        return None
    a, b = abs(x.numerator), x.denominator
    return (a & -a).bit_length() - (b & -b).bit_length()


def residue(x, p):
    x = Q(x)
    assert x.denominator % 2
    return x.numerator * pow(x.denominator, -1, 1 << p) % (1 << p)


def matmul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))]


def transpose(a):
    return [list(r) for r in zip(*a)]


def determinant(a):
    a = [[Q(x) for x in row] for row in a]
    sign = 1
    value = Q(1)
    for k in range(len(a)):
        pivot = next((i for i in range(k, len(a)) if a[i][k]), None)
        if pivot is None:
            return Q(0)
        if pivot != k:
            a[k], a[pivot] = a[pivot], a[k]
            sign *= -1
        v = a[k][k]
        value *= v
        for i in range(k + 1, len(a)):
            ratio = a[i][k] / v
            for j in range(k + 1, len(a)):
                a[i][j] -= ratio * a[k][j]
            a[i][k] = 0
    return sign * value


def permanent(a):
    return sum((prod(a[i][sigma[i]] for i in range(len(a)))
                for sigma in permutations(range(len(a)))), Q(0))


def K(t):
    return [[1, 1 - t], [0, t]]


def G(t):
    return [[1, 1], [1, 1 + t]]


def J(t):
    return [[t, t - 1], [0, 1]]


def tensor_matrix(local):
    b = len(local)
    return [[prod(local[i][(y >> i) & 1][(x >> i) & 1] for i in range(b))
             for x in range(1 << b)] for y in range(1 << b)]


def smith_valuations_mod2(a, p):
    """Elementary row/column reduction over Z/2^p; returns nonzero valuations."""
    modulus = 1 << p
    a = [[int(x) % modulus for x in row] for row in a]
    m = len(a)
    n = len(a[0]) if m else 0
    values = []
    for k in range(min(m, n)):
        candidates = [(valuation(a[i][j]), i, j) for i in range(k, m)
                      for j in range(k, n) if a[i][j]]
        if not candidates:
            break
        v, i, j = min(candidates)
        a[k], a[i] = a[i], a[k]
        for row in a:
            row[k], row[j] = row[j], row[k]
        odd = a[k][k] >> v
        inv = pow(odd, -1, modulus)
        a[k] = [(x * inv) % modulus for x in a[k]]
        assert a[k][k] == 1 << v
        for i in range(k + 1, m):
            assert a[i][k] % (1 << v) == 0
            q = a[i][k] >> v
            a[i] = [(x - q * y) % modulus for x, y in zip(a[i], a[k])]
            assert a[i][k] == 0
        for j in range(k + 1, n):
            assert a[k][j] % (1 << v) == 0
            q = a[k][j] >> v
            for i in range(m):
                a[i][j] = (a[i][j] - q * a[i][k]) % modulus
            assert a[k][j] == 0
        values.append(v)
    return values


def check_ranks():
    records = []
    families = [tuple([d] * b) for b in range(6) for d in (1, 2, 3)]
    families += [(1, 2, 3), (1, 3, 1, 2), (2, 1, 2, 1, 3)]
    families = sorted(set(families), key=lambda x: (len(x), x))
    odds = [1, -1, 3, 5, -3]
    for ds in families:
        ts = [(1 << d) * odds[i] for i, d in enumerate(ds)]
        matrices = [tensor_matrix([K(t) for t in ts]), tensor_matrix([G(t) for t in ts])]
        for p in range(1, sum(ds) + 3):
            expected = sorted(sum(ds[i] for i in range(len(ds)) if s & (1 << i))
                              for s in range(1 << len(ds)))
            expected = [v for v in expected if v < p]
            for matrix in matrices:
                assert smith_valuations_mod2(matrix, p) == expected, (ds, p)
            records.append({"valuations": ds, "precision": p,
                            "separated_terms_required": len(expected), "invariant_valuations": expected})
    return records


def cnf_count(n, clauses):
    return sum(all(any(bool(x & (1 << (abs(lit) - 1))) == (lit > 0) for lit in c)
                   for c in clauses) for x in range(1 << n))


def positive_kernel_cnf(ds):
    b = len(ds)
    clauses = []
    nxt = 3 * b + 1
    for i, d in enumerate(ds):
        x, y, s = i + 1, b + i + 1, 2 * b + i + 1
        clauses += [(-s, x), (-s, y)]
        for _ in range(d):
            clauses.append((s, -nxt))
            nxt += 1
    return nxt - 1, clauses


def check_cnf_boundary_families():
    out = []
    for ds in [(1,), (2,), (1, 1), (1, 2), (2, 2), (1, 1, 1), (1, 2, 1), (2, 2, 2)]:
        n, clauses = positive_kernel_cnf(ds)
        b = len(ds)
        counts = [[0] * (1 << b) for _ in range(1 << b)]
        for z in range(1 << n):
            if all(any(bool(z & (1 << (abs(lit) - 1))) == (lit > 0) for lit in c) for c in clauses):
                x = z & ((1 << b) - 1)
                y = (z >> b) & ((1 << b) - 1)
                counts[y][x] += 1
        expected = tensor_matrix([G(1 << d) for d in ds])
        assert counts == expected
        out.append({"valuations": ds, "n": n, "clauses": clauses, "conditional_counts": counts})
    return out


class NetworkBuilder:
    def __init__(self, n):
        self.n = n
        self.next_signal = n + 1
        self.vertices = []
        self.signals = defaultdict(list)
        self.edges = []

    def vertex(self, kind, arity, table, signals=None):
        idx = len(self.vertices)
        assert len(table) == 1 << arity
        self.vertices.append({"kind": kind, "arity": arity, "table": list(table)})
        if signals is not None:
            assert len(signals) == arity
            for port, signal in enumerate(signals):
                self.signals[signal].append((idx, port))
        return idx

    def add_clause(self, clause):
        if len(clause) <= 3:
            table = [int(any(bool(z & (1 << i)) == (lit > 0) for i, lit in enumerate(clause)))
                     for z in range(1 << len(clause))]
            self.vertex("clause", len(clause), table, [abs(lit) for lit in clause])
            return
        current = clause[0]
        for lit in clause[1:]:
            signal = self.next_signal
            self.next_signal += 1
            table = []
            for z in range(8):
                a = bool(z & 1) == (current > 0)
                b = bool(z & 2) == (lit > 0)
                out = bool(z & 4)
                table.append(int(out == (a or b)))
            self.vertex("OR", 3, table, [abs(current), abs(lit), signal])
            current = signal
        self.vertex("assert_true", 1, [0, 1], [current])

    def eq_vertex(self, d):
        return self.vertex("equality", d,
                           [int(z == 0 or z == (1 << d) - 1) for z in range(1 << d)])

    def finish(self):
        for signal in range(1, self.next_signal):
            ports = list(self.signals.get(signal, []))
            if not ports:
                assert signal <= self.n
                self.vertex("unused_input", 0, [2])
                continue
            if len(ports) == 1:
                v = self.vertex("free_input", 1, [1, 1])
                self.edges.append((ports[0], (v, 0)))
                continue
            while len(ports) > 3:
                v = self.eq_vertex(3)
                self.edges += [(ports[0], (v, 0)), (ports[1], (v, 1))]
                ports = [(v, 2)] + ports[2:]
            v = self.eq_vertex(len(ports))
            self.edges += [(port, (v, i)) for i, port in enumerate(ports)]
        all_ports = {(i, j) for i, v in enumerate(self.vertices) for j in range(v["arity"])}
        used_ports = [tuple(port) for edge in self.edges for port in edge]
        assert len(used_ports) == len(set(used_ports))
        assert set(used_ports) == all_ports
        return {"original_inputs": self.n, "vertices": self.vertices, "edges": self.edges,
                "wire_count": len(self.edges), "max_degree": max([v["arity"] for v in self.vertices], default=0)}


def compile_cnf(n, clauses):
    b = NetworkBuilder(n)
    for c in clauses:
        assert all(1 <= abs(lit) <= n for lit in c)
        b.add_clause(c)
    return b.finish()


def original_factors(network):
    port_var = {}
    for e, edge in enumerate(network["edges"]):
        for port in edge:
            port_var[tuple(port)] = e
    return [(tuple(port_var[(i, j)] for j in range(v["arity"])), tuple(v["table"]))
            for i, v in enumerate(network["vertices"])]


def weak_factors(network):
    port_var = {}
    extra = []
    for e, (left, right) in enumerate(network["edges"]):
        # Each original wire is a K-H-K^T gadget. All four variables are explicit.
        yl, yr, xl, xr = 4 * e, 4 * e + 1, 4 * e + 2, 4 * e + 3
        port_var[tuple(left)], port_var[tuple(right)] = yl, yr
        extra.append(((yl, xl), (1, 0, -1, 2)))
        extra.append(((yr, xr), (1, 0, -1, 2)))
        extra.append(((xl, xr), (5, 1, 1, 1)))
    old = [(tuple(port_var[(i, j)] for j in range(v["arity"])), tuple(v["table"]))
           for i, v in enumerate(network["vertices"])]
    return old + extra


def contract_reference(factors, modulus=None):
    """Exact variable elimination; exponential tables are allowed and counted."""
    factors = [(tuple(vs), tuple(a if modulus is None else a % modulus for a in tab))
               for vs, tab in factors]
    max_scope, evaluated = 0, 0
    while True:
        variables = sorted({v for vs, _ in factors for v in vs})
        if not variables:
            result = prod(tab[0] for _, tab in factors)
            if modulus is not None:
                result %= modulus
            return result, {"max_elimination_scope": max_scope, "table_assignments_evaluated": evaluated}
        def key(v):
            return (len({w for vs, _ in factors if v in vs for w in vs}), v)
        v = min(variables, key=key)
        selected = [(vs, tab) for vs, tab in factors if v in vs]
        factors = [(vs, tab) for vs, tab in factors if v not in vs]
        union = sorted({w for vs, _ in selected for w in vs})
        remain = [w for w in union if w != v]
        max_scope = max(max_scope, len(union))
        locations = {w: i for i, w in enumerate(remain)}
        table = []
        for mask in range(1 << len(remain)):
            total = 0
            for bit in (0, 1):
                term = 1
                for vs, tab in selected:
                    index = sum((bit if w == v else (mask >> locations[w]) & 1) << i
                                for i, w in enumerate(vs))
                    term *= tab[index]
                total += term
                evaluated += 1
            table.append(total if modulus is None else total % modulus)
        factors.append((tuple(remain), tuple(table)))


def check_compiler():
    rng = random.Random(6110627)
    instances = [(0, []), (0, [()]), (3, []), (1, [(1,), (-1,)]),
                 (2, [(1, -1, 2)]), (3, [(1, 1, 2), (-1, 3)]),
                 (6, [(1, -2, 3, 4, -5, 6), (-1, 2), (-3,)])]
    # Forces equality trees at an input with more than three occurrences.
    instances.append((3, [(1, 2), (1, -2), (-1, 3), (-1, -3), (1, 3)]))
    for n in range(1, 6):
        for _ in range(6):
            clauses = []
            for _ in range(rng.randrange(1, 6)):
                width = rng.randrange(1, min(n + 2, 5))
                clauses.append(tuple(rng.choice([-1, 1]) * rng.randrange(1, n + 1) for _ in range(width)))
            instances.append((n, clauses))
    records, fixtures = [], []
    for n, clauses in instances:
        expected = cnf_count(n, clauses)
        network = compile_cnf(n, clauses)
        direct, ordinary_stats = contract_reference(original_factors(network))
        weak, weak_stats = contract_reference(weak_factors(network))
        e = 2 * network["wire_count"]
        p = e + n + 1
        modular, _ = contract_reference(weak_factors(network), 1 << p)
        assert direct == expected
        assert weak == (expected << e)
        assert modular == weak % (1 << p)
        assert modular % (1 << e) == 0
        assert modular >> e == expected
        assert network["max_degree"] <= 3
        record = {"n": n, "clauses": clauses, "count": expected,
                  "original_wires": network["wire_count"], "weak_wires": e,
                  "precision": p, "weak_contraction": weak,
                  "ordinary_reference": ordinary_stats, "weak_reference": weak_stats}
        records.append(record)
        if len(fixtures) < 8:
            fixtures.append({"record": record, "network": network,
                             "weak_factors": weak_factors(network)})
    return records, fixtures


def budget_subsets(weights, p):
    """Polynomial-delay enumeration; every visited prefix has a valid extension."""
    def visit(i, mask, cost):
        if i == len(weights):
            yield mask
            return
        yield from visit(i + 1, mask, cost)
        if cost + weights[i] < p:
            yield from visit(i + 1, mask | (1 << i), cost + weights[i])
    yield from visit(0, 0, 0)


def weighted_zeta(table, scope, ts, modulus):
    table = [a % modulus for a in table]
    for i, edge in enumerate(scope):
        c = (1 - ts[edge]) % modulus
        for y in range(len(table)):
            if not y & (1 << i):
                table[y] = (table[y] + c * table[y | (1 << i)]) % modulus
    return tuple(table)


def weak_wire_contract(a_factors, b_factors, ts, p):
    """Exact global contraction with explicit retained-state count, not poly SAT."""
    e = len(ts)
    modulus = 1 << p
    a_edges = [v for scope, _ in a_factors for v in scope]
    b_edges = [v for scope, _ in b_factors for v in scope]
    assert sorted(a_edges) == list(range(e)) == sorted(b_edges)
    bs = [(scope, weighted_zeta(table, scope, ts, modulus)) for scope, table in b_factors]
    ds = [p if t % modulus == 0 else valuation(t % modulus) for t in ts]
    answer, states = 0, 0
    for y in budget_subsets(ds, p):
        value = prod(ts[i] for i in range(e) if y & (1 << i)) % modulus
        for scope, table in list(a_factors) + bs:
            index = sum(((y >> v) & 1) << i for i, v in enumerate(scope))
            value = value * table[index] % modulus
        answer = (answer + value) % modulus
        states += 1
    return answer, states


def check_global_weak_algorithm():
    rng = random.Random(18110626)
    records = []
    for e in range(1, 11):
        for repetition in range(3):
            ts = [(1 << rng.randrange(1, 4)) * rng.choice([1, 3, -1]) for _ in range(e)]
            p = rng.randrange(1, sum(valuation(t) for t in ts) + 3)
            sides = []
            for _ in range(2):
                order = list(range(e))
                rng.shuffle(order)
                side = []
                while order:
                    d = min(len(order), rng.randrange(1, 4))
                    scope, order = tuple(order[:d]), order[d:]
                    side.append((scope, tuple(rng.randrange(-3, 4) for _ in range(1 << d))))
                sides.append(side)
            a, b = sides
            factors = [(tuple(2 * v for v in scope), table) for scope, table in a]
            factors += [(tuple(2 * v + 1 for v in scope), table) for scope, table in b]
            factors += [((2 * i, 2 * i + 1), (1, 0, 1 - t, t)) for i, t in enumerate(ts)]
            expected, reference_stats = contract_reference(factors, 1 << p)
            got, states = weak_wire_contract(a, b, ts, p)
            ds = [valuation(t) for t in ts]
            count = sum(sum(ds[i] for i in range(e) if y & (1 << i)) < p for y in range(1 << e))
            assert got == expected and states == count
            records.append({"wires":e,"precision":p,"repetition":repetition,"states":states,
                            "residue":got,"reference":reference_stats})
    # Normalizing the weak gadget restores a scaled equality, with no loss of SAT constraints.
    for t in [2, 4, 6, -2, -12]:
        h = matmul(J(t), transpose(J(t)))
        for p in [1, 2, 4, 8, 16]:
            table = tuple(h[a][b] for b in range(2) for a in range(2))
            transformed = weighted_zeta(table, (0, 1), [t,t], 1 << p)
            assert transformed == (t*t % (1 << p), 0, 0, 1)
    return records


def compositions(total, length):
    if length == 1:
        yield (total,)
    else:
        for a in range(total + 1):
            for rest in compositions(total - a, length - 1):
                yield (a,) + rest


def check_zero_order_coefficients():
    records = []
    for n in range(1, 7):
        row_nodes = [20 + 2 * i for i in range(n)]
        for k in range(1, min(3, n) + 1):
            tile_nodes = [2 * j + 1 for j in range(k)]
            for beta in compositions(n, k):
                columns = [(j, r) for j, b in enumerate(beta) for r in range(b)]
                denom = [[Q(1, (a - tile_nodes[j]) ** (r + 1)) for j, r in columns] for a in row_nodes]
                numer = [[Q(r + 1, (a - tile_nodes[j]) ** (r + 2)) for j, r in columns] for a in row_nodes]
                repeated = [[Q(1, a - tile_nodes[j]) for j, r in columns] for a in row_nodes]
                factorials = prod(factorial(b) for b in beta)
                by_determinants = determinant(numer) / determinant(denom) / factorials
                by_permanent = permanent(repeated) / factorials
                assert by_determinants == by_permanent
                records.append({"L": n, "beta": beta, "coefficient": str(by_determinants)})
    return records


def cauchy_failure(a):
    assert a >= 3
    l = 1 << a
    t = 2 * l + 1
    w = (-1) ** (l - 1) * comb(3 * l + 1, l) * comb(2 * l, l - 1)
    g = t * w
    source_g = Q(prod(t - r for r in range(-l, l)), prod(-r for r in range(-l, l) if r))
    assert source_g == g
    ds = [t, t + 2, t + 4]
    matrix = [[Q(g * (1 << b), d ** (b + 1)) for b in range(3)] for d in ds]
    correct = permanent(matrix)
    quotient = determinant([[v * v for v in row] for row in matrix]) / determinant(matrix)
    difference = quotient - correct
    assert difference == Q(16 * g ** 3, prod(d * d for d in ds))
    assert valuation(w) == a + 1
    assert valuation(difference) == 3 * a + 7
    p = 3 * a + 8
    assert residue(correct, p) == 1 << (p - 1)
    assert residue(quotient, p) == 0
    return {"a": a, "L": l, "node": 1, "zeta": 1, "T": t,
            "tile_y0": 0, "row_slots": [0, 2, 4], "mode_orders": [0, 1, 2],
            "g": str(g), "matrix": [[str(x) for x in row] for row in matrix],
            "precision": p, "correct_mod_2p": residue(correct, p),
            "naive_quotient_mod_2p": residue(quotient, p),
            "difference_valuation": valuation(difference)}


def scalar_gauge_checks():
    records = []
    for t in [2, 4, 6, -2, -12, 16]:
        assert matmul(K(t), J(t)) == [[t, 0], [0, t]]
        h = matmul(J(t), transpose(J(t)))
        assert matmul(matmul(K(t), h), transpose(K(t))) == [[t*t, 0], [0, t*t]]
        records.append({"t": t, "K": K(t), "J": J(t), "H": h})
    return records


def write(name, value):
    (ROOT / name).write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def main():
    ranks = check_ranks()
    cnf_boundaries = check_cnf_boundary_families()
    compiler, fixtures = check_compiler()
    global_weak = check_global_weak_algorithm()
    zero_order = check_zero_order_coefficients()
    cauchy = [cauchy_failure(a) for a in (4, 6, 8)]
    gauges = scalar_gauge_checks()
    results = {"status": "PASS", "unrestricted_sat_status": "NOT_RESOLVED",
               "arithmetic": "exact integers, finite residues and rational fractions",
               "finite_ring_rank_cases": ranks, "boundary_cnf_cases": cnf_boundaries,
               "cnf_compiler_cases": compiler, "zero_order_coefficient_cases": zero_order,
               "global_weak_contraction_cases": global_weak,
               "higher_mode_failures": cauchy, "gauge_cases": gauges,
               "novelty_claimed": False,
               "warning": "Finite checks and representation-specific theorems are not a resolution of unrestricted SAT. Reference contractions enumerate states."}
    write("results.json", results)
    write("NETWORK_FIXTURES.json", fixtures)
    transfer = {
        "sent": False,
        "objects": [
            {"id": "C3-PRECISION-SEPARATION", "local_matrix": [[1,-1],[0,2]],
             "family": "K^(tensor b) over Z/(2^p)",
             "exact_required_separated_terms": "sum_{j=0}^{min(b,p-1)} binom(b,j)",
             "failed_claim": "Even cross-boundary coefficients force a universal exact separated representation with polynomially many terms at all polynomial precisions.",
             "scope": "Exact separated linear boundary representations only; the product family itself has easy contractions for product boundary inputs."},
            {"id": "C3-POSITIVE-CNF-BOUNDARY", "construction": "For each i: (!s_i OR x_i), (!s_i OR y_i), and (s_i OR !a_i,j) for j<=delta_i.",
             "conditional_count_matrix": "tensor_i [[1,1],[1,1+2^delta_i]]",
             "failed_claim": "Such bounded-width CNF conditional-count matrices always have polynomial exact separated dimension at polynomial 2-adic precision.",
             "scope": "Conditional count representations, not SAT decision or arbitrary algorithms.",
             "finite_instances": cnf_boundaries},
            {"id": "C3-WEAK-WIRE-GADGET", "K": [[1,-1],[0,2]], "H": [[5,1],[1,1]],
             "K_H_K_transpose": [[4,0],[0,4]],
             "failed_claim": "Rank-one wire matrices modulo two by themselves remove the need to handle unrestricted SAT at a precision linear in the network size.",
             "scope": "A uniform reduction demonstrating retained generality, not an algorithm impossibility theorem."},
            {"id": "C3-HIGHER-MODE-BORCHARDT", "family": "M_{r,b}=g*2^b/(T+2r)^(b+1), r,b in {0,1,2}; L=2^a, T=2L+1, g=C(T)/C'(0)",
             "failed_claim": "The packet's higher-mode coefficient permanent(M) always equals det(M entrywise squared)/det(M).",
             "scope": "This determinant quotient for higher-mode matrices only; not Borchardt's theorem on ordinary Cauchy matrices or all determinant methods.",
             "finite_instances": cauchy}
        ]
    }
    write("TRANSFER_OBJECTS.json", transfer)
    print(json.dumps({"status":"PASS","rank_cases":len(ranks),"boundary_cnf_cases":len(cnf_boundaries),
                      "compiler_cases":len(compiler),"zero_order_coefficients":len(zero_order),
                      "global_weak_contractions":len(global_weak),
                      "higher_mode_failures":len(cauchy),"gauge_cases":len(gauges),
                      "unrestricted_sat_status":"NOT_RESOLVED"},indent=2))


if __name__ == "__main__":
    main()
