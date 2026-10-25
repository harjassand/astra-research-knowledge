"""Independent exact check of the canonical Bell-chain bottleneck theorem.

No physical devices; standard tensor contraction, no fitted constants.
Python standard library only. Fractions keep all success probabilities exact.
"""
from collections import Counter
from fractions import Fraction
from itertools import product
from math import prod
import json


def network_contraction(dimensions):
    """Enumerate all edge-basis terms and contract internal Bell bras.

    Amplitudes share denominator sqrt(prod(edge ranks)*prod(internal dims)).
    Integers returned here are the resulting endpoint amplitude numerators.
    Retained internal Bell kets have unit norm and are not written out.
    """
    dims = tuple(dimensions)
    ranks = [min(a, b) for a, b in zip(dims, dims[1:])]
    coefficients = Counter()
    for terms in product(*(range(r) for r in ranks)):
        if all(terms[i - 1] == terms[i] for i in range(1, len(terms))):
            coefficients[(terms[0], terms[-1])] += 1
    denominator_squared = prod(ranks) * prod(dims[1:-1])
    probability = Fraction(sum(c*c for c in coefficients.values()), denominator_squared)
    return coefficients, probability


def theorem_prediction(dims):
    m = min(dims)
    ranks = [min(a, b) for a, b in zip(dims, dims[1:])]
    return Counter({(i, i): 1 for i in range(m)}), Fraction(m, prod(ranks)*prod(dims[1:-1]))


def paths_in_tree(adjacency):
    paths = []
    for start in range(len(adjacency)):
        stack = [(start, -1, [start])]
        while stack:
            v, parent, path = stack.pop()
            if v > start:
                paths.append(path)
            stack.extend((w, v, path+[w]) for w in adjacency[v] if w != parent)
    return paths


def tree_from_prufer(code):
    n = len(code) + 2
    degrees = [1]*n
    for v in code:
        degrees[v] += 1
    adjacency = [[] for _ in range(n)]
    for v in code:
        leaf = next(i for i, d in enumerate(degrees) if d == 1)
        adjacency[leaf].append(v)
        adjacency[v].append(leaf)
        degrees[leaf] -= 1
        degrees[v] -= 1
    a, b = [i for i, d in enumerate(degrees) if d == 1]
    adjacency[a].append(b)
    adjacency[b].append(a)
    return adjacency


def superlevels_connected(adjacency, dims):
    for threshold in set(dims):
        chosen = {i for i, d in enumerate(dims) if d >= threshold}
        stack = [next(iter(chosen))]
        seen = set(stack)
        while stack:
            for w in adjacency[stack.pop()]:
                if w in chosen and w not in seen:
                    seen.add(w)
                    stack.append(w)
        if seen != chosen:
            return False
    return True


def main():
    chain_cases = 0
    for vertices in range(2, 7):
        for dims in product(range(2, 5), repeat=vertices):
            assert network_contraction(dims) == theorem_prediction(dims), dims
            coefficients, _ = network_contraction(dims)
            type_closed = len(coefficients) == min(dims[0], dims[-1])
            assert type_closed == (min(dims) == min(dims[0], dims[-1]))
            chain_cases += 1
    tree_cases = 0
    for n in range(2, 5):
        for code in product(range(n), repeat=n-2):
            adjacency = tree_from_prufer(code)
            paths = paths_in_tree(adjacency)
            for dims in product(range(2, 5), repeat=n):
                path_closed = all(min(dims[v] for v in path) == min(dims[path[0]], dims[path[-1]]) for path in paths)
                assert path_closed == superlevels_connected(adjacency, dims), (adjacency, dims)
                tree_cases += 1
    examples = {}
    for dims in [(2,3,2), (3,2,3), (4,3,2,4), (2,4,3,2), (3,4,3)]:
        coefficients, p = network_contraction(dims)
        examples[str(dims)] = {"endpoint_schmidt_rank":len(coefficients), "required_type_rank":min(dims[0],dims[-1]), "joint_success_probability":str(p)}
    return {"chain_cases":chain_cases,"tree_cases":tree_cases,"examples":examples,"claim_scope":"exact finite canonical aligned-support contraction; not physical validation or novelty proof"}


if __name__ == '__main__':
    print(json.dumps(main(), indent=2))
