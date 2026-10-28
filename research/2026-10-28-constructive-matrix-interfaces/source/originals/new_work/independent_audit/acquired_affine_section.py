#!/usr/bin/env python3
"""Construct an affine right inverse for certified regular matrix-dual slices.

This is a search/section consumer, not a uniform-fiber sampler. It accepts
arbitrary affine phases and targets when every acquired matrix-dual factor
has natural multiplicity at least two. All coordinates and an invertible
dual map are manufactured from the actual binary certificate.
"""
from pathlib import Path
import argparse
import json
import random
import sys
import time

sys.dont_write_bytecode = True
SNAPSHOT = Path(__file__).resolve().parents[2] / 'recovered_source'
sys.path[:0] = [str(SNAPSHOT / name) for name in (
    'work_source_free_sampling', 'work_matrix_root', 'work_trace_frontier',
    'work_multiprimary_audit', 'work_partition_free_agent', 'work_phase_diamond')]

from acquired_rank_one_slice_sampler import ManufacturedMatrixCoordinates
from source_free_uniform_sampler import AcquiredProductFiberSampler, equations_from_columns
from adjoint_matrix_product_counter import (
    BinaryCoordinates, apply_binary, unpack, pack, product, affine_solutions,
    independent_basis)
from unsaturated_bilinear_counter import rectangular_unpack
from central_quadratic_tensor_compiler import compose_quadratic
from matrix_target_geometry import acquire_semisimple_matrix_dual
from acquired_bilinear_counter import (
    validate_trace_program, acquire_reversible_terminal_and, invert_terminal,
    acquire_source_free_bilinear_split, acquire_affine_hom_slice,
    transpose_affine_split)


def xor_all(values):
    answer = 0
    for value in values:
        answer ^= value
    return answer


class SimpleMatrixUnits:
    """Actual matrix units, with expected-polynomial primitive splitting."""
    primitive_decomposition = AcquiredProductFiberSampler.primitive_decomposition

    def __init__(self, algebra, actual_basis, dimension, rng):
        self.algebra = algebra
        self.table = algebra['multiplication_table']
        self.K = len(self.table)
        self.one = algebra['unit_coordinates']
        self.a = algebra['field_degree']
        self.s = algebra['matrix_degree']
        self.basis = actual_basis
        self.dimension = dimension
        self.rng = rng
        self.stats = dict(corner_random_trials=0, corner_splits=0)
        full_rank = len(independent_basis(self.action(self.one)))
        self.rank_multiplier, rem = divmod(full_rank, self.s)
        if rem or not self.rank_multiplier:
            raise AssertionError('simple action has incompatible multiplicity')
        self.atoms = self.primitive_decomposition(self.one)
        if len(self.atoms) != self.s:
            raise AssertionError('primitive decomposition lost matrix rows')
        self.e = self.atoms[0]
        self.forward = []
        self.backward = []
        for atom in self.atoms:
            a = next(self.mul(atom, self.mul(1 << j, self.e))
                     for j in range(self.K)
                     if self.mul(atom, self.mul(1 << j, self.e)))
            corner = BinaryCoordinates(self.mul(self.e, self.mul(1 << j, atom))
                                       for j in range(self.K)).basis
            images = [self.mul(x, a) for x in corner]
            solution = affine_solutions(
                equations_from_columns(images, self.e, self.K), len(corner))
            if solution is None or solution[1]:
                raise AssertionError('connecting inverse must be unique')
            b = apply_binary(corner, solution[0])
            if self.mul(b, a) != self.e or self.mul(a, b) != atom:
                raise AssertionError('connecting matrix identities failed')
            self.forward.append(a)
            self.backward.append(b)

    def mul(self, x, y):
        return apply_binary([apply_binary(row, y) for row in self.table], x)

    def action(self, coordinate):
        return unpack(apply_binary(self.basis, coordinate), self.dimension)

    def matrix_rank(self, coordinate):
        rank, rem = divmod(len(independent_basis(self.action(coordinate))),
                          self.rank_multiplier)
        if rem:
            raise AssertionError('nonintegral natural simple-algebra rank')
        return rank


def field_basis(candidates, scalar_images, field_degree, required):
    """Choose a field basis using the actual binary scalar action."""
    span = BinaryCoordinates()
    chosen = []
    for value in candidates:
        try:
            span.coordinates(value)
        except ValueError:
            chosen.append(value)
            for scalar in scalar_images:
                span.insert(scalar(value))
    if len(chosen) != required or len(span.basis) != field_degree * required:
        raise AssertionError('acquired field-basis dimension mismatch')
    return chosen


class AcquiredAffineSection:
    """An original-input affine section for every consistent marked target."""

    def __init__(self, split, certificate, compression=None, rng=None):
        began = time.perf_counter()
        self.split = split
        self.C = certificate
        self.N = certificate['nucleus']
        self.rng = rng if rng is not None else random.SystemRandom()
        self.compression = (acquire_semisimple_matrix_dual(certificate)
                            if compression is None else compression)
        if self.N['left_dimension'] != self.N['output_dimension']:
            raise ValueError('section theorem requires equal module dimensions')
        pieces = self.compression['components']
        if any(item['natural_multiplicity'] < 2 for item in pieces):
            raise ValueError('section theorem requires every natural multiplicity >= 2')
        self.U = self.N['left_dimension']
        self.M = self.N['output_dimension']
        self.offset = certificate.get('affine_hom_offset', 0)
        keys = ('original_affine_input_offset', 'original_input_coordinate_columns')
        if any(key in certificate for key in keys):
            if not all(key in certificate for key in keys):
                raise ValueError('incomplete acquired original-input reconstruction')
            self.original_offset = certificate[keys[0]]
            self.original_columns = certificate[keys[1]]
        else:
            self.original_offset = split['affine_offset']
            self.original_columns = split['coordinate_columns']

        self.Q = ManufacturedMatrixCoordinates(certificate, self.rng)
        Q = self.Q
        F = Q.F
        center_ops = [unpack(apply_binary(self.N['nucleus_input_operators'], z), self.U)
                      for z in Q.algebra['center_basis']]
        S_e_ops = unpack(apply_binary(self.N['nucleus_input_operators'], Q.e), self.U)

        # Construct D0 from one F-basis in each primitive left ideal e_i C_i.
        D0 = 0
        unit_data = []
        coordinate_seeds = []
        for item in pieces:
            units = SimpleMatrixUnits(item['local_algebra_certificate'],
                                      item['factor_basis'], self.U, self.rng)
            E = units.action(units.e)
            projected_dual = independent_basis(
                pack(product(E, rectangular_unpack(D, self.U, self.M)), self.U)
                for D in item['component_basis'])
            scalar_maps = [lambda D, Z=Z:
                           pack(product(Z, rectangular_unpack(D, self.U, self.M)), self.U)
                           for Z in center_ops]
            rows = field_basis(projected_dual, scalar_maps, Q.a, units.s)
            for forward, D in zip(units.forward, rows):
                D0 ^= pack(product(units.action(forward),
                                   rectangular_unpack(D, self.U, self.M)), self.U)

            # h vectors in the common primitive S/A corner.
            vectors = independent_basis(product(S_e_ops, E))
            vector_scalars = [lambda v, Z=Z: apply_binary(Z, v) for Z in center_ops]
            seeds = field_basis(vectors, vector_scalars, Q.a,
                                item['natural_multiplicity'])
            first_row = [apply_binary(units.action(forward), v)
                         for v in seeds for forward in units.forward]
            coordinate_seeds.extend(first_row)
            unit_data.append((item, units))

        D0_ops = rectangular_unpack(D0, self.U, self.M)
        self.D0_inverse = BinaryCoordinates(D0_ops)
        if len(self.D0_inverse.basis) != self.U:
            raise AssertionError('manufactured D0 is not an isomorphism')
        BinaryCoordinates(certificate['dual_reverse_matrices']).coordinates(D0)
        self.D0 = D0

        # Coordinate order: nucleus row, factor, repeated block, A index, bit.
        self.module_columns = [
            Q.action(Q.input_ops, s, apply_binary(Z, v))
            for s in Q.forward for v in coordinate_seeds for Z in center_ops]
        self.module_inverse = BinaryCoordinates(self.module_columns)
        if len(self.module_inverse.basis) != self.U:
            raise AssertionError('joint module coordinates are not bijective')

        h0_ops = rectangular_unpack(apply_binary(certificate['hom_basis'], self.offset),
                                     self.M, self.U)
        T0_ops = product(D0_ops, h0_ops)
        d = Q.d
        T0 = []
        for j in range(d):
            u = apply_binary(self.module_columns, F.one << (Q.a * j))
            image = self.module_inverse.coordinates(apply_binary(T0_ops, u))
            if image >> (Q.a * d):
                raise AssertionError('S-linear action left its first natural row')
            T0.append(Q.matrix(image, 1, d)[0])

        # An invertible block cycle realizes every prescribed partial trace.
        T = [[0] * d for _ in range(d)]
        start = 0
        partial_traces = []
        for item in pieces:
            s = item['matrix_degree']
            h = item['natural_multiplicity']
            H = [[xor_all(T0[start + block*s + i][start + block*s + j]
                          for block in range(h)) for j in range(s)] for i in range(s)]
            partial_traces.append(H)
            for i in range(s):
                for j in range(s):
                    T[start+i][start+j] = H[i][j]
            for block in range(h):
                next_block = (block + 1) % h
                for j in range(s):
                    T[start + block*s + j][start + next_block*s + j] = F.one
            start += h*s
        if start != d:
            raise AssertionError('factor dimensions do not exhaust the module')

        T_columns = []
        for row in range(Q.p):
            for j in range(d):
                for ell in range(Q.a):
                    native = [F.mul(1 << ell, value) for value in T[j]]
                    word = Q.word([native]) << (Q.a * d * row)
                    T_columns.append(apply_binary(self.module_columns, word))
        T_actual = [apply_binary(T_columns, self.module_inverse.coordinates(1 << j))
                    for j in range(self.U)]
        H_actual = [self.D0_inverse.coordinates(v) for v in T_actual]
        self.H_inverse = BinaryCoordinates(H_actual)
        if len(self.H_inverse.basis) != self.U:
            raise AssertionError('partial-trace completion is not invertible')
        self.hom_word = BinaryCoordinates(certificate['hom_basis']).coordinates(
            pack(H_actual, self.M))
        self.right_inverse = BinaryCoordinates(certificate['right_embedding_columns'])
        self.v = self.right_inverse.coordinates(self.hom_word ^ self.offset)
        if any((lam & (self.hom_word ^ self.offset)).bit_count() % 2
               for lam in certificate['right_annihilator_basis']):
            raise AssertionError('completed map is outside the exact affine slice')
        self.H_actual = H_actual
        self.section_offset = self.original_offset ^ apply_binary(
            self.original_columns, self.v << self.U)
        self.section_columns = [apply_binary(self.original_columns,
            self.H_inverse.coordinates(1 << j)) for j in range(self.M)]
        if len(independent_basis(self.section_columns)) != self.M:
            raise AssertionError('all-output section is not injective')
        self.stats = dict(
            expected_polynomial_preprocessing=True,
            coordinate_acquisition=Q.stats,
            factor_coordinate_acquisition=[units.stats for item, units in unit_data],
            factor_degrees=[item['matrix_degree'] for item in pieces],
            factor_multiplicities=[item['natural_multiplicity'] for item in pieces],
            codimension=certificate['codimension'], partial_traces=partial_traces,
            invertible_dual_map_manufactured=True,
            invertible_primal_map_manufactured=True, rare_invertible_search=False,
            original_assignments_enumerated=0,
            uniform_full_fiber_sampling_claim=False,
            preprocessing_seconds=time.perf_counter()-began)

    def export_section(self):
        """x=offset+columns*y; marked target=constant+output_columns*y."""
        output_columns = [sum(((row >> j) & 1) << i
                              for i, row in enumerate(self.N['marked_output_coordinates']))
                          for j in range(self.M)]
        return dict(original_input_bits=self.N['input_bits'],
                    independent_output_bits=self.M,
                    marked_output_bits=self.N['marked_quadratics'],
                    original_input_offset=self.section_offset,
                    original_input_columns=self.section_columns,
                    marked_output_constant=self.N['output_constant'],
                    marked_output_columns=output_columns,
                    right_input_fixed=self.v,
                    exact_all_target_affine_section=True,
                    uniform_full_fiber_sampling_claim=False)

    def witness(self, target):
        m = self.N['marked_quadratics']
        if type(target) is not int or target < 0 or target.bit_length() > m:
            raise ValueError('invalid marked output target')
        rhs = target ^ self.N['output_constant']
        y = sum(((rhs >> j) & 1) << i
                for i, j in enumerate(self.N['output_basis_mark_indices']))
        if any((row & y).bit_count() % 2 != ((rhs >> i) & 1)
               for i, row in enumerate(self.N['marked_output_coordinates'])):
            return dict(satisfiable=False, reason='inconsistent marked output dependency')
        u = self.H_inverse.coordinates(y)
        if apply_binary(self.H_actual, u) != y:
            raise AssertionError('actual evaluation inverse failed')
        local = u | (self.v << self.U)
        x = self.original_offset ^ apply_binary(self.original_columns, local)
        return dict(satisfiable=True, assignment=x, left=u, right=self.v,
                    local_assignment=local, marked_target=target,
                    full_hom_coordinates=self.hom_word,
                    native_target_reconstruction=True, uniform_full_fiber_sample=False)


def acquire_native_section(program, rng=None):
    """Input is only the ordinary DAG; no supplied algebra or decomposition."""
    began = time.perf_counter()
    n = program.get('inputs', program.get('n'))
    if type(n) is not int or n < 1 or n > len(program.get('gates', [])) + 1:
        raise ValueError('explicit input ancestry condition failed')
    n, gates, output = validate_trace_program(program, n)
    R = acquire_reversible_terminal_and(program)
    target = invert_terminal(R)
    split = acquire_source_free_bilinear_split(
        R['initial_quadratics'], n, require_shared_center=False,
        allow_paired_components=True)
    declines = []
    for oriented in sorted((split, transpose_affine_split(split)),
                           key=lambda obj: obj['left_dimension']):
        try:
            C = acquire_affine_hom_slice(oriented)
            compression = acquire_semisimple_matrix_dual(C)
            section = AcquiredAffineSection(oriented, C, compression, rng)
            exported = section.export_section()
            for i, form in enumerate(R['initial_quadratics']):
                observed = compose_quadratic(set(form), exported['original_input_offset'],
                                             exported['original_input_columns'])
                expected = ({0} if exported['marked_output_constant'] >> i & 1 else set())
                expected ^= {1 << j for j, column in enumerate(exported['marked_output_columns'])
                             if column >> i & 1}
                if observed != expected:
                    raise AssertionError('original quadratic all-target section identity failed')
            section.stats['original_quadratic_section_identity_verified'] = True
            witness = section.witness(target)
            return section, dict(
                original_input_bits=n, ordinary_gates=len(gates), target=target,
                witness=witness, section_certificate=section.stats,
                affine_section=exported,
                acquisition_seconds=time.perf_counter()-began,
                auxiliary_independent_inputs=0, other_orientation_declines=declines)
        except ValueError as error:
            declines.append(str(error))
    raise ValueError('section certificate declined: ' + '; '.join(declines))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    section, result = acquire_native_section(json.loads(args.source.read_text()))
    rendered = json.dumps(result, indent=2) + '\n'
    if args.output:
        args.output.write_text(rendered)
    else:
        print(rendered, end='')
