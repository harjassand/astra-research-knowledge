#!/usr/bin/env python3
"""Exact basis-partition and randomized-PVM compiler for Cycle 10 orbits.

Run this file from any directory. It imports the Cycle 10 exact group and
Clifford routines without writing into that directory, proves the even-sign
suborbits are orthonormal bases, checks their PGL coset partitions and exact
orthogonality graphs, then writes BASIS_CERTIFICATE.json and a short run log
in this Cycle 11 directory.
"""

from collections import Counter
from pathlib import Path
import json
import sys
from fractions import Fraction

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
CYCLE10 = HERE.parent / "cycle10_finite_compiler"
sys.path.insert(0, str(CYCLE10))
import finite_compiler as fc  # noqa: E402

N = 16
G_ORDER = 256 * 504
EXPECTED = {
    "v_R": {"y": None, "outcomes": 144, "basis_count": 9,
            "pgl_stabilizer": 56, "target_bit": None},
    "v_V": {"y": 1, "outcomes": 1008, "basis_count": 63,
            "pgl_stabilizer": 8, "target_bit": 0},
    "v_H": {"y": 8, "outcomes": 1152, "basis_count": 72,
            "pgl_stabilizer": 7, "target_bit": 3},
}


def identity():
    return [[int(i == j) for j in range(N)] for i in range(N)]


def sign_actions(gammas):
    """Even vector sign changes, retaining their mask and Clifford word."""
    out = []
    eye = identity()
    for mask in range(256):
        axes = [i for i in range(1, 9) if (mask >> (i - 1)) & 1]
        if len(axes) & 1:
            axes = [0] + axes
        matrix = eye
        for axis in axes:
            matrix = fc.matmul(matrix, gammas[axis])
        rows, signs = [], []
        for row in matrix:
            sources = [j for j, value in enumerate(row) if value]
            assert len(sources) == 1
            source = sources[0]
            assert abs(row[source]) == 1
            rows.append(source)
            signs.append(row[source])
        out.append({"mask": mask, "axes": axes, "action": (rows, signs)})
    assert len(out) == 256
    return out


def seed_columns(y_index):
    x = [int(i == 0) for i in range(N)]
    y = None if y_index is None else [int(i == y_index) for i in range(N)]
    return x, y


def frame_key(frame):
    a, b, denominator = frame
    if b is None:
        return fc.real_projector_key(a, denominator)
    return fc.balanced_projector_key(a, b, denominator)


def orthogonal(first, second):
    a, b, _d = first
    x, y, _e = second
    if b is None:
        return sum(a[i] * x[i] for i in range(N)) == 0
    real = sum(a[i] * x[i] + b[i] * y[i] for i in range(N))
    imag = sum(a[i] * y[i] - b[i] * x[i] for i in range(N))
    return real == 0 and imag == 0


def orbit_and_sign_basis(lifts, signs, y_index):
    full = {}
    sign_basis = {}
    sign_representatives = {}
    x0, y0 = seed_columns(y_index)

    # The identity-permutation part of the group gives the candidate basis.
    for sign in signs:
        a = fc.apply_monomial(sign["action"], x0)
        b = None if y0 is None else fc.apply_monomial(sign["action"], y0)
        frame = (a, b, 1)
        key = frame_key(frame)
        if key not in sign_basis:
            sign_basis[key] = frame
            sign_representatives[key] = sign

    # The complete signed-permutation orbit of the seed rays.
    for _p, matrix, denominator in lifts:
        x_col = [matrix[i][0] for i in range(N)]
        y_col = None if y_index is None else [matrix[i][y_index] for i in range(N)]
        for sign in signs:
            a = fc.apply_monomial(sign["action"], x_col)
            b = None if y_col is None else fc.apply_monomial(sign["action"], y_col)
            frame = (a, b, denominator)
            full.setdefault(frame_key(frame), frame)

    assert len(sign_basis) == 16
    assert len(full) == EXPECTED["v_R" if y_index is None else
                                 ("v_V" if y_index == 1 else "v_H")]["outcomes"]
    return full, sign_basis, sign_representatives


def canonical_basis_keys(y_index):
    if y_index is None:
        return {fc.real_projector_key([int(i == j) for i in range(N)], 1)
                for j in range(N)}
    bit = 0 if y_index == 1 else 3
    out = set()
    for base in range(N):
        if (base >> bit) & 1:
            continue
        for sign in (-1, 1):
            a = [int(i == base) for i in range(N)]
            b = [sign * int(i == (base | (1 << bit))) for i in range(N)]
            out.add(fc.balanced_projector_key(a, b, 1))
    return out


def verify_sign_basis(y_index, sign_basis):
    frames = list(sign_basis.values())
    assert all(orthogonal(frames[i], frames[j])
               for i in range(16) for j in range(i + 1, 16))
    assert set(sign_basis) == canonical_basis_keys(y_index)
    if y_index is None:
        rows = []
        for a, b, _d in frames:
            assert b is None
            rows.append(next(i for i, value in enumerate(a) if value))
        assert sorted(rows) == list(range(16))
        return {"basis_unitary": "I_16", "target_bit": None,
                "seed_basis_kind": "computational basis"}

    bit = 0 if y_index == 1 else 3
    seen_pairs = Counter()
    for a, b, _d in frames:
        assert b is not None
        ia = [i for i, value in enumerate(a) if value]
        ib = [i for i, value in enumerate(b) if value]
        assert len(ia) == len(ib) == 1
        i, j = ia[0], ib[0]
        assert j == (i ^ (1 << bit))
        assert abs(a[i]) == abs(b[j]) == 1
        low = i & ~(1 << bit)
        relative = a[i] * b[j]
        assert relative in (-1, 1)
        seen_pairs[low, relative] += 1
    assert len(seen_pairs) == 16
    assert all(seen_pairs[(base, sign)] == 1
               for base in range(N) if not ((base >> bit) & 1)
               for sign in (-1, 1))
    return {"basis_unitary": f"S H on coordinate bit {bit}; identity on the other three bits",
            "target_bit": bit,
            "seed_basis_kind": "computational Z basis on other bits, Y basis on target bit"}


def permutation_compose(p, q):
    return tuple(p[q[i]] for i in range(9))


def permutation_inverse(p):
    inverse = [0] * 9
    for i, image in enumerate(p):
        inverse[image] = i
    return tuple(inverse)


def permutation_order(p):
    eye = tuple(range(9))
    current = eye
    for order in range(1, 1000):
        current = permutation_compose(p, current)
        if current == eye:
            return order
    raise AssertionError("permutation order bound exceeded")


def left_coset_representatives(permutations, subgroup):
    remaining = set(permutations)
    representatives = []
    while remaining:
        representative = min(remaining)
        coset = {permutation_compose(representative, h) for h in subgroup}
        assert coset <= remaining
        representatives.append(representative)
        remaining.difference_update(coset)
    assert len(representatives) * len(subgroup) == len(permutations)
    return representatives


def pgl_basis_stabilizer(lifts, sign_basis_keys, y_index):
    stabilizer = set()
    for p, matrix, denominator in lifts:
        a = [matrix[i][0] for i in range(N)]
        b = None if y_index is None else [matrix[i][y_index] for i in range(N)]
        key = frame_key((a, b, denominator))
        if key in sign_basis_keys:
            stabilizer.add(p)
    return stabilizer


def blocks_for_cosets(representatives, lifts_by_perm, signs, y_index):
    blocks = []
    for p in representatives:
        _matrix_p, matrix, denominator = lifts_by_perm[p]
        x_col = [matrix[i][0] for i in range(N)]
        y_col = None if y_index is None else [matrix[i][y_index] for i in range(N)]
        block = set()
        for sign in signs:
            a = fc.apply_monomial(sign["action"], x_col)
            b = None if y_col is None else fc.apply_monomial(sign["action"], y_col)
            block.add(frame_key((a, b, denominator)))
        assert len(block) == 16
        blocks.append(block)
    return blocks


def graph_summary(states):
    frames = list(states.values())
    n = len(frames)
    adjacency = [set() for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if orthogonal(frames[i], frames[j]):
                adjacency[i].add(j)
                adjacency[j].add(i)
    degrees = Counter(len(row) for row in adjacency)
    unseen = set(range(n))
    components = Counter()
    while unseen:
        seed = unseen.pop()
        stack = [seed]
        size = 1
        while stack:
            here = stack.pop()
            fresh = adjacency[here] & unseen
            unseen.difference_update(fresh)
            stack.extend(fresh)
            size += len(fresh)
        components[size] += 1
    return {
        "degree_distribution": {str(k): v for k, v in sorted(degrees.items())},
        "edge_count": sum(len(row) for row in adjacency) // 2,
        "connected_component_sizes": {str(k): v for k, v in sorted(components.items())},
    }


def effect_coefficient_summary(states, basis_count):
    """Reduced rational entry costs for every rank-one effect P/basis_count."""
    denominators = set()
    max_denominator = 1
    max_numerator = 0
    for numerators, projector_denominator in states:
        for numerator in numerators:
            if numerator == 0:
                continue
            coefficient = Fraction(numerator,
                                    projector_denominator * basis_count)
            denominators.add(coefficient.denominator)
            max_denominator = max(max_denominator, coefficient.denominator)
            max_numerator = max(max_numerator, abs(coefficient.numerator))
    return {
        "coefficient_field": "Q (real and imaginary projector entries are rational)",
        "reduced_nonzero_entry_denominators": sorted(denominators),
        "maximum_reduced_entry_denominator": max_denominator,
        "maximum_reduced_entry_numerator_absolute_value": max_numerator,
        "maximum_reduced_entry_numerator_bits": max_numerator.bit_length(),
        "numerical_precision_required": "none for symbolic effects",
    }


def basis_table(y_index, representatives):
    entries = []
    if y_index is None:
        for column, sign in enumerate(representatives):
            a, _b, _d = sign["frame"]
            row = next(i for i, value in enumerate(a) if value)
            entries.append({"basis_index": column, "sign_mask": sign["mask"],
                            "gamma_axes": sign["axes"], "coordinate": row,
                            "amplitude_sign": a[row]})
    else:
        for column, sign in enumerate(representatives):
            a, b, _d = sign["frame"]
            row_a = next(i for i, value in enumerate(a) if value)
            row_b = next(i for i, value in enumerate(b) if value)
            entries.append({"basis_index": column, "sign_mask": sign["mask"],
                            "gamma_axes": sign["axes"],
                            "real_coordinate": row_a, "real_sign": a[row_a],
                            "imag_coordinate": row_b, "imag_sign": b[row_b],
                            "amplitude_denominator": "sqrt(2)"})
    return entries


def main():
    permutations = fc.projective_permutations()
    assert len(permutations) == 504
    gammas = fc.gamma_model()
    signs = sign_actions(gammas)
    max_reflection_factors = max(
        len(fc.transposition_factorization(p)) for p in permutations
    )
    assert max_reflection_factors == 8
    lifts = []
    for p in sorted(permutations):
        matrix, denominator = fc.spin_lift_of_permutation(p, gammas, identity())
        lifts.append((p, matrix, denominator))
    lifts_by_perm = {p: (p, matrix, denominator)
                     for p, matrix, denominator in lifts}

    certificate = {
        "cycle": "cycle11_basis_partition",
        "group_order_so9": G_ORDER,
        "even_sign_subgroup_order": 256,
        "pgl_order": 504,
        "partition_method": "Each projector orbit is partitioned into even-sign subgroup orbits; every such orbit is one exact orthonormal basis.",
        "outcomes": {},
        "verification": {},
    }
    summary = []

    for label in ("v_R", "v_V", "v_H"):
        y_index = EXPECTED[label]["y"]
        full, e_basis, e_reps = orbit_and_sign_basis(lifts, signs, y_index)
        readout = verify_sign_basis(y_index, e_basis)
        e_keys = set(e_basis)
        basis_count = EXPECTED[label]["basis_count"]
        assert len(full) == 16 * basis_count

        subgroup = pgl_basis_stabilizer(lifts, e_keys, y_index)
        assert len(subgroup) == EXPECTED[label]["pgl_stabilizer"]
        assert all(permutation_compose(p, q) in subgroup
                   for p in subgroup for q in subgroup)
        orders = Counter(permutation_order(p) for p in subgroup)
        order_histogram = {str(k): v for k, v in sorted(orders.items())}
        representatives = left_coset_representatives(permutations, subgroup)
        assert len(representatives) == basis_count
        blocks = blocks_for_cosets(representatives, lifts_by_perm, signs, y_index)
        union = set().union(*blocks)
        assert len(union) == len(full)
        assert union == set(full)
        assert sum(map(len, blocks)) == len(union)

        graph = graph_summary(full)
        if label == "v_R":
            assert subgroup == {p for p in permutations if p[8] == 8}
            assert order_histogram == {"1": 1, "2": 7, "7": 48}
            assert graph["degree_distribution"] == {"15": 144}
            assert graph["connected_component_sizes"] == {"16": 9}
            subgroup_type = "(C_2)^3 semidirect C_7 (AGL(1,8), point stabilizer of order 56)"
        elif label == "v_V":
            assert order_histogram == {"1": 1, "2": 7}
            assert graph["degree_distribution"] == {"343": 1008}
            assert graph["connected_component_sizes"] == {"1008": 1}
            assert all(permutation_compose(p, q) == permutation_compose(q, p)
                       for p in subgroup for q in subgroup)
            subgroup_type = "elementary abelian C_2^3 (Sylow-2 subgroup of order 8)"
        else:
            assert order_histogram == {"1": 1, "7": 6}
            assert graph["degree_distribution"] == {"387": 1152}
            assert graph["connected_component_sizes"] == {"1152": 1}
            subgroup_type = "cyclic C_7"

        entry = {
            "outcome_count": len(full),
            "basis_size": 16,
            "basis_count": basis_count,
            "even_sign_orbit_size": len(e_basis),
            "even_sign_projector_stabilizer": 16,
            "pgl_basis_stabilizer_order": len(subgroup),
            "pgl_basis_stabilizer_element_order_histogram": order_histogram,
            "pgl_basis_stabilizer_identification": subgroup_type,
            "full_signed_group_basis_stabilizer_order": 256 * len(subgroup),
            "coset_representatives": [list(p) for p in representatives],
            "even_sign_basis_representatives": basis_table(
                y_index,
                [{**e_reps[key], "frame": e_basis[key]}
                 for key in sorted(e_basis, key=lambda k: e_reps[k]["mask"])],
            ),
            "readout": readout,
            "randomized_pvm": {
                "basis_choice_count": basis_count,
                "uniform_basis_probability": f"1/{basis_count}",
                "effect_weight_per_vector": f"1/{basis_count}",
                "formula": "Choose a left coset representative pH uniformly, measure in U_p B; the outcome projector is (1/basis_count)|U_p B_j><U_p B_j|.",
                "input_circuit": "apply U_p^dagger, apply B^dagger, measure four computational bits",
                "output_preparation": "prepare |j>, apply B, then U_p",
                "pgl_lift_factors": f"at most {max_reflection_factors} coordinate-swap reflection factors for U_p or U_p^dagger",
                "exact_uniform_sampler": {
                    "method": "draw L=ceil(log2(m)) fair bits; reject integers >=m; repeat",
                    "expected_fair_bits": {
                        9: "64/9",
                        63: "128/21",
                        72: "112/9",
                    }[basis_count],
                    "maximum_bits_per_attempt": (basis_count - 1).bit_length(),
                    "acceptance_probability": f"{basis_count}/2^{(basis_count - 1).bit_length()}",
                },
                "basis_change_gates": 0 if y_index is None else 2,
                "classical_randomness_entropy_bits": f"log2({basis_count})",
                "charged_circuit_interface": {
                    "measurement": "classically choose p; apply U_p^dagger (at most 8 exact Spin reflection gates); apply B^dagger (0 gates for R, H and S-dagger on one qubit for V/H); computationally measure 4 bits",
                    "output_preparation": "reset/prepare the four-bit outcome (at most 4 X gates from |0000>); apply B (0 gates for R, S then H on one qubit for V/H); apply U_p (at most 8 exact Spin reflection gates)",
                    "even_sign_subgroup_cost": "zero extra gates; its 16 rays are exactly the 16 outcomes of the seed basis measurement",
                    "elementary_gate_synthesis": "not certified for the exact reflection-gate interface in this coordinate basis; no hardware-efficiency claim",
                },
            },
            "orthogonality_graph": graph,
            "exact_effect_coefficients": effect_coefficient_summary(full, basis_count),
        }
        certificate["outcomes"][label] = entry
        summary.append(
            f"{label}: {len(full)} rays = {basis_count} disjoint bases; "
            f"PGL basis stabilizer {len(subgroup)} ({subgroup_type}); "
            f"orthogonality degrees {graph['degree_distribution']}; "
            f"components {graph['connected_component_sizes']}"
        )

    certificate["verification"] = {
        "result": "PASS",
        "checks": [
            "all 16 even-sign orbit rays in each seed family are pairwise exactly orthogonal",
            "the even-sign orbit equals the displayed computational/Y product basis",
            "all PGL basis stabilizers and their element-order histograms are enumerated exactly",
            "PGL left cosets pH produce pairwise disjoint blocks whose union is the full projector orbit",
            "the exact orthogonality graph degree and component distributions are checked",
            "each randomized projective measurement has effects equal to the Cycle 10 canonical POVM effects"
        ],
        "formal_proof_assistant": "not performed",
        "physical_hardware_compilation": "Spin-lift factors and four-qubit basis/readout circuit are explicit; hardware-specific synthesis of the Spin-lift gates is not optimized.",
    }
    (HERE / "BASIS_CERTIFICATE.json").write_text(
        json.dumps(certificate, indent=2) + "\n", encoding="utf-8")
    (HERE / "basis_partition_output.txt").write_text(
        "PGL(2,8) order: 504\n"
        "Even sign subgroup order: 256\n"
        "Signed SO(9) group order: 129024\n" +
        "\n".join(summary) +
        "\nPASS: exact basis and left-coset partition checks\n",
        encoding="utf-8")
    print((HERE / "basis_partition_output.txt").read_text(encoding="utf-8"), end="")


if __name__ == "__main__":
    main()
