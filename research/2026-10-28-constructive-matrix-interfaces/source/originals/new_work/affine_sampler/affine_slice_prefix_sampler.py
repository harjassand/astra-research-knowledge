#!/usr/bin/env python3
"""Exact prefix counts and uniform samples for arbitrary binary affine Hom slices.

The cost is 2**c times a polynomial, where c is the actual binary codimension.
The native wrapper admits c < bit_length(actual circuit bytes).  It acquires
all field/matrix coordinates, rather than accepting a planted decomposition.
Full-fiber rejection is never used.  A partially fixed row is integrated by
three rank-update classes, not by enumerating its binary Fourier characters.
"""
from pathlib import Path
import argparse
import json
import random
import sys
import time

sys.dont_write_bytecode = True
BASE = Path(__file__).resolve().parents[2]
SOURCE = BASE / 'recovered_source'
sys.path[:0] = [str(SOURCE / p) for p in (
    'work_source_free_sampling', 'work_matrix_root', 'work_trace_frontier',
    'work_multiprimary_audit', 'work_partition_free_agent')]
from rank_one_slice_sampler import (
    BinaryCoordinates, apply_binary, affine_solutions, dot, transpose,
    pack_vector, unpack_vector, solve_field, rank_field, matmul,
    sample_field_affine)
from source_free_uniform_sampler import equations_from_columns
from acquired_rank_one_slice_sampler import ManufacturedMatrixCoordinates
from unsaturated_bilinear_counter import signed_universal_product, slice_target_fiber
from affine_unsaturated_bilinear_counter import (
    acquire_affine_hom_slice, transpose_affine_split,
    acquire_source_free_bilinear_split)
from adjoint_matrix_product_counter import (
    acquire_reversible_terminal_and, invert_terminal, validate_trace_program)


def trace_bit(F, value):
    total = 0
    x = value
    for _ in range(F.a):
        total ^= x
        x = F.mul(x, x)
    if total not in (0, F.one):
        raise AssertionError('absolute field trace is outside its prime field')
    return int(total != 0)


def trace_dual_basis(F):
    """Coefficients v_j with Tr(v_j * sum x_i e_i) = x_j."""
    rows = [sum(trace_bit(F, F.mul(1 << i, 1 << j)) << j
                for j in range(F.a)) for i in range(F.a)]
    result = []
    for j in range(F.a):
        solved = affine_solutions([(row, int(i == j))
                                   for i, row in enumerate(rows)], F.a)
        if solved is None or solved[1]:
            raise AssertionError('field trace pairing is not nondegenerate')
        result.append(solved[0])
    return result


def signed_affine_mass(columns, target, height, weight):
    """Sum (-1)^(weight . z) over the binary solutions columns*z=target."""
    solved = affine_solutions(equations_from_columns(columns, target, height),
                              len(columns))
    if solved is None:
        return 0
    offset, kernel = solved
    if any((weight & v).bit_count() & 1 for v in kernel):
        return 0
    size = 1 << len(kernel)
    return -size if (weight & offset).bit_count() & 1 else size


class AffineMatrixSliceSampler:
    """Literal-coordinate engine; native acquisition is a separate checked layer.

    equations contains (binary mask, bit) pairs on row-major field-coordinate
    bits of Y.  Prefixes fix complete rows and low bits of the next row.
    They are acquired-coordinate constraints, not arbitrary original-bit pins.
    """

    def __init__(self, F, target, inner_dimension, equations=(), rng=None):
        begun = time.perf_counter()
        self.F = F
        self.Z = [list(row) for row in target]
        self.p = len(self.Z)
        self.r = len(self.Z[0]) if self.Z else 0
        self.d = inner_dimension
        if self.p < 1 or self.r < 1 or self.d < 1:
            raise ValueError('positive matrix dimensions required')
        if any(len(row) != self.r or any(type(x) is not int or not 0 <= x < F.q
                                        for x in row) for row in self.Z):
            raise ValueError('invalid target matrix')
        self.row_bits = F.a * self.r
        self.width = self.d * self.row_bits
        self.rng = rng if rng is not None else random.SystemRandom()
        equations = list(equations)
        if any(type(mask) is not int or mask < 0 or mask.bit_length() > self.width
               or type(rhs) is not int or rhs not in (0, 1) for mask, rhs in equations):
            raise ValueError('invalid binary affine equation')
        sol = affine_solutions(equations, self.width)
        self.empty_slice = sol is None
        independent = BinaryCoordinates()
        self.equations = []
        for mask, rhs in equations:
            if independent.insert(mask) is not None:
                self.equations.append((mask, rhs))
        self.c = len(self.equations)
        self.duals = trace_dual_basis(F)
        self.character_columns = []
        self.phase_mask = 0
        for j, (mask, rhs) in enumerate(self.equations):
            coefficient = []
            for entry in range(self.d * self.r):
                bits = (mask >> (F.a * entry)) & (F.q - 1)
                coefficient.append(apply_binary(self.duals, bits))
            self.character_columns.append(pack_vector(F, coefficient))
            self.phase_mask |= rhs << j
        self.rank_fiber_cache = {}
        self.stats = dict(prefix_queries=0, original_dual_characters=0,
                          partial_row_characters_enumerated=0,
                          samples=0, witnesses=0, full_fiber_rejection_trials=0,
                          max_partial_row_bits=0)
        self.population = self.count_prefix([], 0, 0)
        self.stats['preprocessing_seconds'] = time.perf_counter() - begun

    def _fiber(self, remaining, quotient_columns, k, rank, target_rank):
        key = remaining, quotient_columns, k, rank, target_rank
        if key not in self.rank_fiber_cache:
            self.rank_fiber_cache[key] = signed_universal_product(
                self.p, remaining, quotient_columns, self.F.a, k, rank, target_rank)
        return self.rank_fiber_cache[key]

    def _partial_signed(self, D, rows, bits, used_bits, row_rank, target_quotient_rank):
        """One original character, including fixed-row phase and prefix filter."""
        F = self.F
        t = len(rows)
        remaining = self.d - t
        first = D[t]
        rest = D[t + 1:]
        # Complete-row summation along A=rowspan(rows) kills these characters.
        if any(dot(F, v, y) for v in rest for y in rows):
            return 0
        first_frequencies = []
        for j in range(used_bits):
            v = [0] * self.r
            v[j // F.a] = self.duals[j % F.a]
            first_frequencies.append(v)
        l0 = rank_field(F, rest, self.r)
        images = [[dot(F, z, v) for z in self.Z] for v in rest]
        rho0 = rank_field(F, images, self.p)
        # A0=rowspan(rest) is contained in B0={v: Z*v in image(Z*rest^T)}.
        a_annihilator = solve_field(F, rest, [0] * len(rest), self.r)[1]
        image_annihilator = solve_field(F, images, [0] * len(images), self.p)[1]
        b_equations = rows + [[dot(F, b, column) for column in transpose(self.Z, self.r)]
                              for b in image_annihilator]

        def mass(linear_rows):
            target = pack_vector(F, [dot(F, h, first) for h in linear_rows])
            columns = [pack_vector(F, [dot(F, h, v) for h in linear_rows])
                       for v in first_frequencies]
            return signed_affine_mass(columns, target, F.a * len(linear_rows), bits)

        ma = mass(a_annihilator)
        mb = mass(b_equations)
        mh = mass(rows)
        value = 0
        for weight, l, rho in ((ma, l0, rho0),
                               (mb - ma, l0 + 1, rho0),
                               (mh - mb, l0 + 1, rho0 + 1)):
            if weight:
                value += weight * self._fiber(remaining, self.r - row_rank,
                                               target_quotient_rank, l, rho)
        # A-components of all remaining rows, and the old left columns.
        value *= F.q ** (row_rank * remaining + self.p * (t - row_rank))
        value, rem = divmod(value, 1 << used_bits)
        if rem:
            raise AssertionError('partial-row character inversion was not integral')
        phase = 0
        for i, row in enumerate(rows):
            phase ^= trace_bit(F, dot(F, D[i], row))
        return -value if phase else value

    def count_prefix(self, complete_rows, partial_word=0, partial_bits=0):
        """Exact number of product solutions with this acquired right-row prefix."""
        rows = [list(row) for row in complete_rows]
        if len(rows) > self.d or any(len(row) != self.r or
                any(type(x) is not int or not 0 <= x < self.F.q for x in row) for row in rows):
            raise ValueError('invalid complete-row prefix')
        if not 0 <= partial_bits <= self.row_bits or partial_word < 0 or partial_word.bit_length() > partial_bits:
            raise ValueError('invalid partial-row prefix')
        if len(rows) == self.d and partial_bits:
            raise ValueError('partial row follows a complete matrix')
        self.stats['prefix_queries'] += 1
        self.stats['max_partial_row_bits'] = max(self.stats['max_partial_row_bits'], partial_bits)
        if self.empty_slice:
            return 0
        if partial_bits == self.row_bits:
            rows.append(unpack_vector(self.F, partial_word, self.r))
            partial_word = partial_bits = 0
        a0 = rank_field(self.F, rows, self.r)
        k = rank_field(self.F, rows + self.Z, self.r) - a0
        if len(rows) == self.d:
            if k:
                return 0
            word = pack_vector(self.F, [x for row in rows for x in row])
            if any(((mask & word).bit_count() & 1) != rhs for mask, rhs in self.equations):
                return 0
            return self.F.q ** (self.p * (self.d - a0))
        total = 0
        for word in range(1 << self.c):
            packed = apply_binary(self.character_columns, word)
            D = [unpack_vector(self.F, packed >> (i * self.row_bits), self.r)
                 for i in range(self.d)]
            value = self._partial_signed(D, rows, partial_word, partial_bits, a0, k)
            if (word & self.phase_mask).bit_count() & 1:
                value = -value
            total += value
            self.stats['original_dual_characters'] += 1
        answer, rem = divmod(total, 1 << self.c)
        if rem or answer < 0:
            raise AssertionError('affine slice prefix count is not a nonnegative integer')
        return answer

    def _construct(self, randomize):
        if not self.population:
            raise ValueError('cannot sample an empty product slice')
        remaining = self.population
        rows = []
        for i in range(self.d):
            word = 0
            for used in range(self.row_bits):
                zero = self.count_prefix(rows, word, used + 1)
                if not 0 <= zero <= remaining:
                    raise AssertionError('prefix branch population outside its parent')
                choose_zero = self.rng.randrange(remaining) < zero if randomize else zero > 0
                if choose_zero:
                    remaining = zero
                else:
                    word |= 1 << used
                    remaining -= zero
            rows.append(unpack_vector(self.F, word, self.r))
        Y = rows
        X = []
        system = transpose(Y, self.r)
        nullity = None
        for z in self.Z:
            solved = solve_field(self.F, system, z, self.d)
            if solved is None:
                raise AssertionError('positive prefix count led to an inconsistent left fiber')
            if nullity is None:
                nullity = len(solved[1])
            X.append(sample_field_affine(self.F, *solved, self.rng) if randomize else solved[0])
        if remaining != self.F.q ** (self.p * nullity):
            raise AssertionError('terminal prefix population disagrees with linear fiber')
        if matmul(self.F, X, Y, self.r) != self.Z:
            raise AssertionError('sampled matrices do not have the target product')
        self.stats['samples' if randomize else 'witnesses'] += 1
        return X, Y

    def sample(self):
        """Draw Y by completion counts, then X uniformly in its linear fiber."""
        return self._construct(True)

    def witness(self):
        """Take a positive branch and a particular left solution, without rejection."""
        return self._construct(False)


class AcquiredAffineSliceSampler:
    """Source-free consumer using the corrected original affine reconstruction."""

    def __init__(self, split, certificate, target, rng=None):
        begun = time.perf_counter()
        self.split, self.C, self.target = split, certificate, target
        self.rng = rng if rng is not None else random.SystemRandom()
        self.offset = certificate.get('affine_hom_offset', 0)
        self.count = slice_target_fiber(certificate, target, self.offset)
        self.population = self.count['population']
        self.stats = {'samples': 0}
        if not self.population:
            self.stats['preprocessing_seconds'] = time.perf_counter() - begun
            return
        self.coords = Q = ManufacturedMatrixCoordinates(certificate, self.rng)
        N = certificate['nucleus']
        self.y = self.count['target_output_coordinates']
        Z = Q.matrix(Q.output_inverse.coordinates(self.y), Q.p, Q.r)
        coordinate_rows = [Q.hom_inverse.coordinates(1 << j)
                           for j in range(Q.a * Q.d * Q.r)]
        equations = []
        for lam in certificate['right_annihilator_basis']:
            mask = sum(((lam & h).bit_count() & 1) << j
                       for j, h in enumerate(coordinate_rows))
            equations.append((mask, (lam & self.offset).bit_count() & 1))
        self.engine = AffineMatrixSliceSampler(Q.F, Z, Q.d, equations, self.rng)
        if self.engine.population != self.population:
            raise AssertionError('manufactured prefix count disagrees with acquired character count')
        keys = ('original_affine_input_offset', 'original_input_coordinate_columns')
        if any(k in certificate for k in keys):
            if not all(k in certificate for k in keys):
                raise ValueError('incomplete native affine reconstruction')
            self.original_offset = certificate[keys[0]]
            self.original_columns = certificate[keys[1]]
        else:
            self.original_offset = split['affine_offset']
            self.original_columns = split['coordinate_columns']
        self.stats.update(coordinate_acquisition=Q.stats, binary_codimension=self.engine.c,
                          preprocessing_seconds=time.perf_counter() - begun)

    def _reconstruct(self, X, Y):
        if not self.population:
            raise ValueError('cannot sample an empty target fiber')
        Q = self.coords
        u = apply_binary(Q.input_columns, Q.word(X))
        h = Q.hom_inverse.coordinates(Q.word(Y))
        v = Q.right_inverse.coordinates(h ^ self.offset)
        local = u | (v << Q.U)
        assignment = self.original_offset ^ apply_binary(self.original_columns, local)
        return dict(assignment=assignment, left=u, right=v,
                    full_hom_coordinates=h, local_assignment=local,
                    native_target_reconstruction=True)

    def sample(self):
        if not self.population:
            raise ValueError('cannot sample an empty target fiber')
        result = self._reconstruct(*self.engine.sample())
        self.stats['samples'] += 1
        return result

    def witness(self):
        if not self.population:
            raise ValueError('cannot find a witness in an empty target fiber')
        result = self._reconstruct(*self.engine.witness())
        self.stats['witnesses'] = self.stats.get('witnesses', 0) + 1
        return result

    def prefix_constraints_on_original(self, complete_rows, partial_word=0, partial_bits=0):
        """Translate a valid acquired Y-prefix to exact original-input equations.

        The equations can be dense and redundant. Arbitrary supplied original
        constraints do not have the prefix guarantee.
        """
        if not self.population:
            raise ValueError('no coordinates manufactured for an empty target fiber')
        self.engine.count_prefix(complete_rows, partial_word, partial_bits)
        Q = self.coords
        used = len(complete_rows) * Q.a * Q.r + partial_bits
        word = Q.word(complete_rows) | (partial_word << (len(complete_rows)*Q.a*Q.r))
        yoffset = apply_binary(Q.hom_columns, self.offset)
        ycolumns = [apply_binary(Q.hom_columns, h) for h in self.C['right_embedding_columns']]
        inverse = BinaryCoordinates(self.original_columns)
        local_columns = [inverse.coordinates(1 << j) for j in range(len(self.original_columns))]
        equations = []
        for bit in range(used):
            local_mask = sum(((column >> bit) & 1) << (Q.U+j) for j, column in enumerate(ycolumns))
            mask = sum(((local_mask & column).bit_count() & 1) << j
                       for j, column in enumerate(local_columns))
            rhs = ((word ^ yoffset) >> bit) & 1
            rhs ^= (mask & self.original_offset).bit_count() & 1
            equations.append((mask, rhs))
        return equations


def compile_native(program, rng=None):
    """Polynomial admission by actual description length; internal wires are not inputs."""
    begun = time.perf_counter()
    n = program.get('inputs', program.get('n'))
    if type(n) is not int or n < 1 or n > len(program.get('gates', [])) + 1:
        raise ValueError('source-free admission requires explicit input ancestry')
    n, gates, output = validate_trace_program(program, n)
    length = len(json.dumps(program, separators=(',', ':')).encode())
    terminal = acquire_reversible_terminal_and(program)
    target = invert_terminal(terminal)
    polar = acquire_source_free_bilinear_split(terminal['initial_quadratics'], n,
                 require_shared_center=False, allow_paired_components=True)
    accepted, declines = [], []
    for oriented in (polar, transpose_affine_split(polar)):
        try:
            acquired = acquire_affine_hom_slice(oriented)
        except ValueError as error:
            declines.append(str(error))
            continue
        accepted.append((acquired, oriented))
    if not accepted:
        raise ValueError('neither acquired orientation admits the affine Hom slice: ' + '; '.join(declines))
    C, split = min(accepted, key=lambda pair: pair[0]['codimension'])
    if C['codimension'] >= length.bit_length():
        raise ValueError('binary codimension exceeds description-bounded character budget')
    sampler = AcquiredAffineSliceSampler(split, C, target, rng)
    report = dict(original_input_bits=n, ordinary_gates=len(gates),
                  description_bytes=length, population=sampler.population,
                  binary_codimension=C['codimension'], auxiliary_independent_inputs=0,
                  orientation_declines=declines,
                  original_assignments_enumerated=0,
                  arbitrary_original_bit_conditioning_claim=False,
                  unrestricted_polynomial_counting_claim=False,
                  compilation_seconds=time.perf_counter() - begun)
    return sampler, report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('--samples', type=int, default=1)
    parser.add_argument('--seed', type=int)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    if args.samples < 0:
        parser.error('sample count must be nonnegative')
    rng = random.Random(args.seed) if args.seed is not None else random.SystemRandom()
    sampler, result = compile_native(json.loads(args.source.read_text()), rng)
    begun = time.perf_counter()
    result['samples'] = [sampler.sample() for _ in range(args.samples)] if sampler.population else []
    result['witness'] = sampler.witness() if sampler.population else None
    result['sampling_seconds'] = time.perf_counter() - begun
    result['sampler_stats'] = sampler.stats
    if hasattr(sampler, 'engine'):
        result['prefix_engine_stats'] = sampler.engine.stats
    content = json.dumps(result, indent=2) + '\n'
    if args.output:
        args.output.write_text(content)
    else:
        print(content, end='')


if __name__ == '__main__':
    main()
