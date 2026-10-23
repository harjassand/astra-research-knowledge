"""Finite-block exact operator-system probe for the genuine infinite tree.

This explores n-slot Kraus operators for a finite set of actual initial vertices;
there is no reflecting tree cutoff. Full rank modulo a prime certifies full
complex operator-system rank at the rational unitary alpha=3/5,beta=4/5.
Failure to get full rank is not a code construction or rank upper bound.
"""
import argparse
import itertools
import json
import time
import numpy as np


def edge(a, v):
    side, word = v
    if a:
        return 0, (side, word + (a,))
    if word:
        return word[-1], (side, word[:-1])
    return 0, (1-side, ())


def add_basis(v, basis, prime):
    v = v.copy()
    for pivot, row in basis:
        k = int(v[pivot])
        if k:
            v = (v-k*row) % prime
    nz = np.flatnonzero(v)
    if len(nz) == 0:
        return False
    pivot = int(nz[0])
    v = (v * pow(int(v[pivot]), -1, prime)) % prime
    basis.append((pivot, v))
    basis.sort(key=lambda x: x[0])
    return True


def operators(n, prime, alpha, beta):
    imaginary = next(i for i in range(2, prime) if i*i % prime == prime-1)
    letters = list(itertools.product(range(3), repeat=n))
    starts = [(0, w) for length in range(n+1)
              for w in itertools.product((1, 2), repeat=length)]
    d = 3**n
    result = []
    records = []
    for v in starts:
        matrices = {}
        for column, word in enumerate(letters):
            states = {((), v): 1}
            for a in word:
                next_states = {}
                for (out, bath), coeff in states.items():
                    key = out+(a,), bath
                    next_states[key] = (next_states.get(key, 0)+coeff*beta*imaginary) % prime
                    y, w = edge(a, bath)
                    key = out+(y,), w
                    next_states[key] = (next_states.get(key, 0)+coeff*alpha) % prime
                states = next_states
            for (out, w), coeff in states.items():
                if w not in matrices:
                    matrices[w] = np.zeros((d, d), dtype=np.int64)
                row = 0
                for a in out:
                    row = 3*row+a
                matrices[w][row, column] = coeff
        for w, matrix in matrices.items():
            if np.any(matrix):
                result.append(matrix)
                records.append({'start': v, 'end': w})
    return result, records, imaginary


def run(n, prime, alpha, beta):
    start = time.perf_counter()
    ops, records, imaginary = operators(n, prime, alpha, beta)
    d = 3**n
    basis = []
    independent = []
    indices = []
    for i, matrix in enumerate(ops):
        if add_basis(matrix.reshape(-1), basis, prime):
            independent.append(matrix)
            indices.append(i)
    system = []
    chosen_pairs = []
    # All matrices have a common real/imaginary phase fixed by endpoint parity.
    # Thus transpose products and adjoint products span the same complex space.
    pairs = list(itertools.product(range(len(independent)), repeat=2))
    np.random.default_rng(20261021+n).shuffle(pairs)
    for i, j in pairs:
        product = (independent[i].T @ independent[j]) % prime
        if add_basis(product.reshape(-1), system, prime):
            chosen_pairs.append([indices[i], indices[j]])
        if len(system) == d*d:
            break
    return {
        'slots': n, 'port_block_dimension': d,
        'alpha_beta_unnormalized': [alpha, beta],
        'prime': prime, 'imaginary_root': imaginary,
        'actual_vertex_kraus_count': len(ops),
        'kraus_span_rank_mod_prime': len(independent),
        'operator_system_rank_mod_prime': len(system),
        'full_operator_system_certified': len(system) == d*d,
        'independent_product_pairs': chosen_pairs,
        'kraus_records': records,
        'wall_seconds': time.perf_counter()-start,
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--slots', type=int, default=2)
    parser.add_argument('--prime', type=int, default=1009)
    parser.add_argument('--alpha', type=int, default=3)
    parser.add_argument('--beta', type=int, default=4)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    result = run(args.slots, args.prime, args.alpha, args.beta)
    with open(args.output, 'w') as f:
        json.dump(result, f, indent=2)
    print(json.dumps({k: v for k, v in result.items()
                      if k not in ('independent_product_pairs', 'kraus_records')}, indent=2))
