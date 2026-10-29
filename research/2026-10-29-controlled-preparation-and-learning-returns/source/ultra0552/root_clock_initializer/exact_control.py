"""Exact positive augmentation/coverage/marginal controls, plus trace diagnostic.

Finite controls of algebra, not an execution of the full code initializer.
"""
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path
import json
import time
import numpy as np


def subsets(items):
    items = tuple(items)
    for bits in product((0, 1), repeat=len(items)):
        yield frozenset(x for x, bit in zip(items, bits) if bit)


def run():
    start = time.perf_counter()
    vertices = frozenset(range(4))
    edges = ((0, 1), (1, 2), (2, 3))
    # (declared connected support, actual parity support, favored parity, v)
    bonds = (
        (frozenset((0, 1)), frozenset((0,)), -1, F(1, 7)),
        (frozenset((1, 2)), frozenset((1, 2)), 1, F(1, 11)),
        (frozenset((2, 3)), frozenset((3,)), -1, F(1, 13)),
        (vertices, frozenset((0, 2)), 1, F(1, 17)),
    )
    x = F(1, 19)

    def valid(t):
        return ((0 in t) == (1 in t)) and ((2 in t) == (3 in t))

    def favorable(b, t):
        return (-1 if len(b[1] & t) % 2 else 1) == b[2]

    def components(u):
        pending = set(u)
        out = []
        while pending:
            seen = {pending.pop()}
            todo = list(seen)
            while todo:
                v = todo.pop()
                for a, b in edges:
                    z = b if a == v else a if b == v else None
                    if z in pending:
                        pending.remove(z)
                        seen.add(z)
                        todo.append(z)
            out.append(frozenset(seen))
        return out

    def z_of(w, fixed_t=None):
        total = F(0)
        for t in subsets(w):
            if not valid(t) or (fixed_t is not None and t != fixed_t):
                continue
            weight = x ** len(t)
            for b in bonds:
                if b[0] <= w and favorable(b, t):
                    weight *= 1 + b[3]
            total += weight
        return total

    def coverage(u, fixed_t=None):
        return sum(((-1) ** len(u - w) * z_of(w, fixed_t)
                    for w in subsets(u)), F(0))

    all_sets = list(subsets(vertices))
    connected = [u for u in all_sets if u and len(components(u)) == 1]
    activities = {u: coverage(u) for u in connected}
    assert all(w >= 0 for w in activities.values())

    # Independent explicit active-bond expansion, including zero-history bonds.
    expanded = {t: F(0) for t in all_sets if valid(t)}
    brute_coverage = {u: F(0) for u in all_sets}
    for t in expanded:
        for active in subsets(range(len(bonds))):
            if not all(favorable(bonds[j], t) for j in active):
                continue
            u = t | frozenset().union(*(bonds[j][0] for j in active))
            weight = x ** len(t)
            for j in active:
                weight *= bonds[j][3]
            expanded[t] += weight
            brute_coverage[u] += weight
    assert all(coverage(u) == brute_coverage[u] for u in all_sets)

    # Reconstruct full gas, drawing internal T only after the supports.
    gas_marginal = {t: F(0) for t in expanded}
    gas_z = F(0)
    for family in subsets(range(len(connected))):
        supports = [connected[j] for j in family]
        occupied = frozenset().union(*supports)
        if sorted(map(sorted, components(occupied))) != sorted(map(sorted, supports)):
            continue
        options = [[(t, coverage(u, t)) for t in subsets(u)
                    if valid(t) and coverage(u, t)] for u in supports]
        for draw in product(*options):
            t = frozenset().union(*(z[0] for z in draw))
            weight = F(1)
            for _, w in draw:
                weight *= w
            gas_z += weight
            gas_marginal[t] += weight
    assert gas_marginal == expanded
    assert gas_z == z_of(vertices)
    assert coverage(frozenset((1, 2)), frozenset()) > 0

    # Form bound -> density-of-states test for a non-number-conserving K.
    # T = X_0 Q_1 annihilates the vacuum and ||T||<=Q_{0,1}<=N.
    eye = np.eye(2)
    q = np.diag((0.0, 1.0))
    pauli_x = np.array(((0.0, 1.0), (1.0, 0.0)))
    number = np.kron(q, eye) + np.kron(eye, q)
    lam = 0.2
    k = number + lam * np.kron(pauli_x, q)
    assert np.linalg.norm(k @ number - number @ k) > 0
    assert np.linalg.eigvalsh(k - (1 - lam) * number).min() >= -1e-14
    trace_rows = []
    eig = np.linalg.eigvalsh(k)
    for t in (1.0, 4.0, 10.0):
        z = float(np.exp(-t * eig).sum())
        bound = float((1 + np.exp(-(1 - lam) * t)) ** 2)
        assert z <= bound + 1e-13
        trace_rows.append(dict(t=t, trace=z, minmax_bound=bound,
                               actual_excited_probability=1-1/z))

    return dict(scope="finite exact algebra/marginal controls; not full initializer",
                all_fraction_identities_pass=True, vertices=4, bonds=len(bonds),
                connected_supports=len(connected), valid_histories=len(expanded),
                rational_partition=str(gas_z),
                background_bond_weight=str(coverage(frozenset((1, 2)), frozenset())),
                activities={','.join(map(str, sorted(u))): str(w)
                            for u, w in activities.items()},
                noncommuting_trace_diagnostic=trace_rows,
                elapsed_seconds=time.perf_counter()-start)


if __name__ == '__main__':
    result = run()
    Path(__file__).with_name('EXACT_CONTROL.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))
