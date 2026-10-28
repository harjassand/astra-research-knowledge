#!/usr/bin/env python3
"""Acquired two-factor affine counts through an explicit E6 flag census.

The new operation admits different target carriers.  Production enumerates
fixed-type multiplicities, never field elements, matrices, or subspaces.
The recovered source is imported read-only; no bytecode is written there.
"""
from __future__ import annotations
from collections import Counter
from functools import lru_cache
from itertools import product as cartesian_product
from pathlib import Path
import argparse
import json
import sys
import time

sys.dont_write_bytecode = True
RECOVERED = Path(__file__).resolve().parents[2] / 'recovered_source'
sys.path[:0] = [str(RECOVERED / p) for p in (
    'work_matrix_root', 'work_trace_frontier', 'work_multiprimary_audit',
    'work_partition_free_agent', 'work_phase_diamond')]
from matrix_affine_flag_counter import (
    BinaryCoordinates, canonical_binary_span, gaussian_binomial,
    polynomial_product, signed_rectangular_rank_polynomial,
    acquire_matrix_phase_carriers, signed_universal_product,
    acquire_semisimple_matrix_dual, acquire_source_free_bilinear_split,
    acquire_reversible_terminal_and, invert_terminal, validate_trace_program)
from affine_unsaturated_bilinear_counter import (
    acquire_affine_hom_slice, transpose_affine_split)

# Vertices: R, J, E1, F1, E2, F2. All arrows point toward R.
ARROWS = ((1, 0), (2, 0), (3, 2), (4, 0), (5, 4))


def binary_rank(rows):
    pivots = {}
    for value in rows:
        while value:
            bit = value.bit_length() - 1
            if bit not in pivots:
                pivots[bit] = value
                break
            value ^= pivots[bit]
    return len(pivots)


def intersection_dimension(first, second):
    return len(first) + len(second) - binary_rank(tuple(first) + tuple(second))


def is_contained(first, second):
    return binary_rank(tuple(first) + tuple(second)) == len(second)


def flag_representation(name, ambient, J, E1, F1, E2, F2):
    """Fixed binary inclusions, also valid over every characteristic-two field."""
    spaces = (tuple(1 << i for i in range(ambient)), tuple(J), tuple(E1),
              tuple(F1), tuple(E2), tuple(F2))
    maps = []
    for source, target in ARROWS:
        coordinates = BinaryCoordinates(spaces[target])
        maps.append(tuple(coordinates.coordinates(v) for v in spaces[source]))
    return dict(name=name, dims=tuple(map(len, spaces)), maps=tuple(maps),
                spaces=spaces)


def injective_catalogue():
    types = []
    # E-level 0: absent; 1: E only; 2: F=E. These are eighteen thin roots.
    for level1, level2, j in cartesian_product(range(3), range(3), range(2)):
        types.append(flag_representation(
            f'thin_{level1}{level2}_j{j}', 1, [1] if j else [],
            [1] if level1 else [], [1] if level1 == 2 else [],
            [1] if level2 else [], [1] if level2 == 2 else []))
    # Nine two-dimensional blocks. Their three distinguished lines are e1,
    # e2, and e1+e2, so their endomorphisms are exactly the common scalars.
    left = (([1], []), ([1], [1]), ([1, 2], [1]))
    right = (([2], []), ([2], [2]), ([1, 2], [2]))
    for i, (E1, F1) in enumerate(left):
        for j, (E2, F2) in enumerate(right):
            types.append(flag_representation(f'plane_{i}{j}', 2, [3], E1, F1, E2, F2))
    # Two three-dimensional blocks. The base pair of flags forces a diagonal
    # endomorphism; preserving J forces its three diagonal entries to agree.
    for j, J in ((1, [7]), (2, [3, 6])):
        types.append(flag_representation(f'three_j{j}', 3, J,
                     [1, 2], [1], [2, 4], [4]))
    return tuple(types)


TYPES = injective_catalogue()


def hom_dimension(source, target):
    """Dimension of the commuting-square kernel over F2 and hence F_(2^a)."""
    sd, td = source['dims'], target['dims']
    offsets = []
    unknowns = 0
    for s, t in zip(sd, td):
        offsets.append(unknowns)
        unknowns += s * t
    equations = []
    for (u, v), A, B in zip(ARROWS, source['maps'], target['maps']):
        for row in range(td[v]):
            for col in range(sd[u]):
                equation = 0
                for mid in range(sd[v]):
                    if (A[col] >> mid) & 1:
                        equation ^= 1 << (offsets[v] + row * sd[v] + mid)
                for mid in range(td[u]):
                    if (B[mid] >> row) & 1:
                        equation ^= 1 << (offsets[u] + mid * sd[u] + col)
                equations.append(equation)
    return unknowns - binary_rank(equations)


HOM = tuple(tuple(hom_dimension(A, B) for B in TYPES) for A in TYPES)
if len(TYPES) != 29 or any(HOM[i][i] != 1 for i in range(29)):
    raise AssertionError('explicit injective E6 catalogue is not a list of bricks')


def e6_positive_roots():
    """Constant-size root-system verification, independent of the input field."""
    neighbors = [[] for _ in range(6)]
    for u, v in ARROWS:
        neighbors[u].append(v)
        neighbors[v].append(u)
    roots = {tuple(int(i == j) for i in range(6)) for j in range(6)}
    todo = list(roots)
    while todo:
        alpha = todo.pop()
        for vertex in range(6):
            beta = list(alpha)
            beta[vertex] = sum(alpha[j] for j in neighbors[vertex]) - alpha[vertex]
            beta = tuple(beta)
            if beta not in roots:
                roots.add(beta)
                todo.append(beta)
                if len(roots) > 72:
                    raise AssertionError('E6 root system exceeded its fixed cardinality')
    positive = {x for x in roots if all(v >= 0 for v in x)}
    if len(roots) != 72 or len(positive) != 36:
        raise AssertionError('incorrect E6 root census')
    omitted = positive - {T['dims'] for T in TYPES}
    expected = {(0, 1, 0, 0, 0, 0)}
    for E, F in ((2, 3), (4, 5)):
        for e, f in ((1, 0), (0, 1), (1, 1)):
            dims = [0] * 6
            dims[E], dims[F] = e, f
            expected.add(tuple(dims))
    if omitted != expected or len(positive & {T['dims'] for T in TYPES}) != 29:
        raise AssertionError('catalogue does not cover precisely the injective positive roots')
    return tuple(sorted(positive))


ROOTS = e6_positive_roots()


def pair_flag_grid(R, F1, E1, F2, E2, ap=1):
    """Acquire the nine simultaneous-basis multiplicities of two actual flags."""
    first = ((), tuple(F1), tuple(E1), tuple(R))
    second = ((), tuple(F2), tuple(E2), tuple(R))
    if ap < 1 or any(len(S) % ap for S in first + second):
        raise ValueError('nonintegral actual module dimensions')
    for chain in (first, second):
        if any(not is_contained(A, B) for A, B in zip(chain, chain[1:])):
            raise ValueError('data are not two nested pairs of actual submodules')
    intersections = [[intersection_dimension(A, B) for B in second] for A in first]
    if any(value % ap for row in intersections for value in row):
        raise ValueError('intersection is not a natural module dimension')
    grid = tuple((intersections[i][j] - intersections[i-1][j]
                  - intersections[i][j-1] + intersections[i-1][j-1]) // ap
                 for i in range(1, 4) for j in range(1, 4))
    if min(grid, default=0) < 0 or sum(grid) != len(R) // ap:
        raise AssertionError('invalid two-flag grid')
    return grid


TYPE_GRIDS = tuple(pair_flag_grid(T['spaces'][0], T['spaces'][3], T['spaces'][2],
                                 T['spaces'][5], T['spaces'][4]) for T in TYPES)
TYPE_STATS = tuple((T['dims'][1],
                   intersection_dimension(T['spaces'][1], T['spaces'][2]),
                   intersection_dimension(T['spaces'][1], T['spaces'][3]),
                   intersection_dimension(T['spaces'][1], T['spaces'][4]),
                   intersection_dimension(T['spaces'][1], T['spaces'][5])) for T in TYPES)
THIN = {}
for i, T in enumerate(TYPES[:18]):
    cell = TYPE_GRIDS[i].index(1)
    THIN[cell, T['dims'][1]] = i
THICK = tuple(range(18, 29))


@lru_cache(None)
def gl_order(n, q):
    value = 1
    for j in range(n):
        value *= q**n - q**j
    return value


def automorphism_order(parts, q):
    active = [(i, m) for i, m in enumerate(parts) if m]
    end_dimension = sum(m*n*HOM[i][j] for i, m in active for j, n in active)
    radical = end_dimension - sum(m*m for _, m in active)
    if radical < 0:
        raise AssertionError('negative radical dimension')
    answer = q**radical
    for _, multiplicity in active:
        answer *= gl_order(multiplicity, q)
    return answer


def multiplicity_profiles(grid):
    """Eleven thick multiplicities, then one J-split per occupied base atom.

    The operation uses at most (k+1)^20 tuples, or (k+1)^19 when R=E1+E2.
    This is a charged fixed polynomial exponent, not a practical-speed claim.
    """
    parts = [0] * len(TYPES)
    # More restrictive three-dimensional blocks first helps finite executions.
    thick = tuple(reversed(THICK))

    def thin_visit(cell, remaining):
        if cell == 9:
            yield tuple(parts)
            return
        count = remaining[cell]
        for j_count in range(count + 1):
            parts[THIN[cell, 0]] = count - j_count
            parts[THIN[cell, 1]] = j_count
            yield from thin_visit(cell + 1, remaining)

    def visit(index, remaining):
        if index == len(thick):
            yield from thin_visit(0, remaining)
            return
        number = thick[index]
        shape = TYPE_GRIDS[number]
        maximum = min(remaining[cell] // value for cell, value in enumerate(shape) if value)
        for count in range(maximum + 1):
            parts[number] = count
            yield from visit(index + 1, tuple(x - count*y for x, y in zip(remaining, shape)))

    yield from visit(0, tuple(grid))


@lru_cache(None)
def two_flag_subspace_census(grid, a):
    """Positive counts of J by (dim J, dim JE1, dim JF1, dim JE2, dim JF2)."""
    if len(grid) != 9 or any(type(x) is not int or x < 0 for x in grid):
        raise ValueError('nine nonnegative acquired base multiplicities required')
    q = 1 << a
    k = sum(grid)
    base = [0] * len(TYPES)
    for cell, count in enumerate(grid):
        base[THIN[cell, 0]] = count
    numerator = automorphism_order(base, q)
    census = Counter()
    profiles = 0
    for parts in multiplicity_profiles(grid):
        denominator = automorphism_order(parts, q)
        weight, remainder = divmod(numerator, denominator)
        if remainder:
            raise AssertionError('E6 stabilizer does not divide fixed-pair automorphism order')
        stats = tuple(sum(parts[i]*TYPE_STATS[i][j] for i in range(len(TYPES))) for j in range(5))
        census[stats] += weight
        profiles += 1
    for j in range(k + 1):
        if sum(value for stats, value in census.items() if stats[0] == j) != gaussian_binomial(k, j, a):
            raise AssertionError('E6 orbits fail to exhaust the Grassmannian')
    return dict(census), profiles


def affine_e6_histogram(components, a, ap):
    """Exactly two acquired matrix factors, arbitrary one-copy targets/phases."""
    begun = time.perf_counter()
    if len(components) != 2:
        raise ValueError('E6 consumer requires exactly two certified matrix factors')
    data = []
    d = c = 0
    for item in components:
        E = canonical_binary_span(item['target_rows'])
        F = canonical_binary_span(item['phase_kernel_rows'])
        g, rem = divmod(len(E), ap)
        f, rem2 = divmod(len(F), ap)
        s, h, t = (item['matrix_degree'], item['natural_multiplicity'], item['phase_rank'])
        if rem or rem2 or not 0 <= g <= s or not 0 <= t <= s:
            raise ValueError('nonintegral or impossible acquired factor ranks')
        if not max(0, g-t) <= f <= min(g, s-t) or not is_contained(F, E):
            raise ValueError('invalid acquired phase carrier')
        data.append(dict(E=E, F=F, g=g, f=f, s=s, h=h, t=t))
        d += h*s
        c += a*s*s
    R = canonical_binary_span(data[0]['E'] + data[1]['E'])
    k, rem = divmod(len(R), ap)
    if rem:
        raise AssertionError('nonintegral target join')
    grid = pair_flag_grid(R, data[0]['F'], data[0]['E'], data[1]['F'], data[1]['E'], ap)
    if grid[8] != 0:
        raise AssertionError('R is not the target-carrier join')
    census, profile_count = two_flag_subspace_census(grid, a)
    moments = [[0] * (d+1) for _ in range(k+1)]
    local_cache = {}
    for (j, ell1, eta1, ell2, eta2), weight in census.items():
        value = [1]
        for i, (ell, eta) in enumerate(((ell1, eta1), (ell2, eta2))):
            item = data[i]
            r = item['s'] - item['g'] + ell
            tau = item['t'] - item['g'] + ell + item['f'] - eta
            key = (i, r, tau)
            if key not in local_cache:
                local_cache[key] = signed_rectangular_rank_polynomial(item['s'], r, tau, item['h'], a)
            value = polynomial_product(value, local_cache[key])
        for t, coefficient in enumerate(value):
            moments[j][t] += weight*coefficient
    exact = []
    histogram = {}
    for rho in range(k+1):
        value = moments[rho][:]
        for u in range(rho):
            scale = gaussian_binomial(k-u, rho-u, a)
            for t, coefficient in enumerate(exact[u]):
                value[t] -= scale*coefficient
        exact.append(value)
        for t, coefficient in enumerate(value):
            if coefficient:
                histogram[t, rho] = coefficient
    if histogram.get((0, 0)) != 1:
        raise AssertionError('zero character lost')
    expected_mass = 1 << c if all(item['t'] == 0 for item in data) else 0
    if sum(histogram.values()) != expected_mass:
        raise AssertionError('signed dual mass lost')
    return histogram, dict(
        target_rank=k, dual_maximum_rank=d, codimension=c,
        target_carrier_ranks=[item['g'] for item in data],
        phase_carrier_ranks=[item['f'] for item in data],
        pair_flag_grid=list(grid), catalogue_types=29,
        multiplicity_profiles=profile_count, geometric_statistics=len(census),
        histogram_states=len(histogram), characters_enumerated=0,
        subspaces_enumerated=0, field_elements_enumerated=0,
        seconds=time.perf_counter()-begun)


def affine_matrix_e6_target(certificate, compression, target, affine_hom_offset=0):
    acquired = acquire_matrix_phase_carriers(certificate, compression, target, affine_hom_offset)
    if 'population' in acquired:
        return acquired
    C = certificate['nucleus']
    a, p, d = C['field_degree'], C['left_matrix_rows'], C['inner_dimension']
    histogram, geometry = affine_e6_histogram(acquired['components'], a, a*p)
    k = geometry['target_rank']
    if acquired['target_rank'] != k or geometry['dual_maximum_rank'] != d:
        raise AssertionError('E6 census changed acquired target or dual rank')
    if geometry['codimension'] != compression['codimension']:
        raise AssertionError('E6 census changed acquired codimension')
    total = sum(weight*signed_universal_product(p, d, d, a, k, t, rho)
                for (t, rho), weight in histogram.items())
    answer, rem = divmod(total, 1 << compression['codimension'])
    if rem or not 0 <= answer <= 1 << C['input_bits']:
        raise AssertionError('invalid original-input E6 count')
    return dict(population=answer, matrix_target_rank=k,
        codimension=compression['codimension'],
        phase_carrier_acquisition=acquired['phase_carrier_acquisition'],
        e6_certificate=geometry,
        rank_pair_histogram={f'{t},{rho}': value for (t, rho), value in sorted(histogram.items())},
        histogram_states=len(histogram), characters_enumerated=0,
        original_assignments_enumerated=0)


def count_affine_e6_native(program):
    """Ordinary gate DAG -> acquired algebra/flags -> exact original-input count."""
    begun = time.perf_counter()
    n = program.get('inputs', program.get('n'))
    if type(n) is not int or n < 1 or n > len(program.get('gates', [])) + 1:
        raise ValueError('explicit input ancestry guard failed')
    n, gates, _ = validate_trace_program(program, n)
    terminal = acquire_reversible_terminal_and(program)
    target = invert_terminal(terminal)
    split = acquire_source_free_bilinear_split(terminal['initial_quadratics'], n,
                require_shared_center=False, allow_paired_components=True)
    declines = []
    for oriented in sorted((split, transpose_affine_split(split)), key=lambda S: S['left_dimension']):
        try:
            C = acquire_affine_hom_slice(oriented)
            compression = acquire_semisimple_matrix_dual(C)
            result = affine_matrix_e6_target(C, compression, target, C['affine_hom_offset'])
        except ValueError as error:
            declines.append(str(error))
            continue
        ones = result['population']
        return dict(original_input_bits=n, ordinary_gates=len(gates),
            description_bytes=len(json.dumps(program, separators=(',', ':')).encode()),
            ones=ones, zeros=(1 << n)-ones, target=target,
            method='two acquired matrix factors with arbitrary one-copy targets and affine phases: E6',
            fiber=result, affine_slice_certificate=C, compression_certificate=compression,
            split_certificate=oriented, reversible_certificate=terminal,
            other_branch_declines=declines, auxiliary_independent_inputs=0,
            original_assignments_enumerated=0, unrestricted_polynomial_counting_claim=False,
            seconds=time.perf_counter()-begun)
    raise ValueError('not admitted by the two-factor E6 family: ' + '; '.join(declines))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = count_affine_e6_native(json.loads(args.source.read_text()))
    encoded = json.dumps(result, indent=2) + '\n'
    if args.output:
        args.output.write_text(encoded)
    else:
        print(encoded, end='')


if __name__ == '__main__':
    main()
