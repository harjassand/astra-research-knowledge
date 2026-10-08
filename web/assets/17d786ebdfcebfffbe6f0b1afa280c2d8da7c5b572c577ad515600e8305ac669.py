#!/usr/bin/env python3
"""Exact Spin(9) circuit audit and finite-sampling spot checks for cycle 12.

This script independently reconstructs the listed JW readout circuits and an
exact Clifford+Toffoli synthesis of the fixed octonion/JW intertwiner.  It
also checks the parity-corrected Fisher--Yates map on small groups.  The
all-n proof is in FINAL_REPORT.md; finite checks here are not its proof.
"""

from collections import Counter
from fractions import Fraction
from importlib.util import module_from_spec, spec_from_file_location
from itertools import combinations, product
from math import ceil, comb, log2
from pathlib import Path
import json
import sys

import sympy as sp

ROOT = Path(__file__).resolve().parents[3]
OLD = ROOT / "work/agents/c5_quantum_dimension_obstruction"
READOUT_DIR = OLD / "cycle11_basis_partition"
CERT = json.loads((READOUT_DIR / "STABILIZER_READOUT_CERTIFICATE.json").read_text())
FINITE_CERT = json.loads((OLD / "cycle10_finite_compiler/FINITE_CERTIFICATE.json").read_text())
BASIS_CERT = json.loads((READOUT_DIR / "BASIS_CERTIFICATE.json").read_text())

I2 = sp.eye(2)
X2 = sp.Matrix([[0, 1], [1, 0]])
Y2 = sp.Matrix([[0, -sp.I], [sp.I, 0]])
Z2 = sp.diag(1, -1)
H2 = sp.Matrix([[1, 1], [1, -1]]) / sp.sqrt(2)
S2 = sp.diag(1, sp.I)
SDG2 = sp.diag(1, -sp.I)
T2 = sp.diag(1, sp.exp(sp.I * sp.pi / 4))
TDG2 = T2.H
ONE_Q_PAULI = {"I": I2, "X": X2, "Y": Y2, "Z": Z2}


def load_module(path, name):
    spec = spec_from_file_location(name, path)
    mod = module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


FC = load_module(OLD / "cycle10_finite_compiler/finite_compiler.py", "c12_fc")
JW = load_module(OLD / "cycle9_spin9_mixed/spin9_fullstar_blocks.py", "c12_jw")


def pauli_word_matrix(word):
    out = sp.Matrix([[1]])
    # The stored word order is q0,...,q(n-1); q0 is the least significant bit.
    for letter in reversed(word):
        out = sp.kronecker_product(out, ONE_Q_PAULI[letter])
    return out


def exact_w_matrix():
    cv = {"0": 0, "1": 1, "-1": -1, "I": sp.I, "-I": -sp.I}
    return sp.Matrix([[cv[x] for x in row]
                      for row in CERT["representation_intertwiner"]["intertwiner_matrix"]])


def check_intertwiner_and_clifford_status():
    W = exact_w_matrix()
    oct_gammas = [sp.Matrix(rows) for rows in FC.gamma_model()]
    jw_gammas = [pauli_word_matrix(word) for word in JW.GAM]
    for a in range(9):
        assert W * oct_gammas[a] == jw_gammas[a] * W
    assert W.H * W == 2 * sp.eye(16)
    U = W / sp.sqrt(2)
    assert U.H * U == sp.eye(16)

    # A Clifford unitary must send every Pauli generator to one signed Pauli.
    # Exact expansion of U X_0 U* supplies a decisive non-Clifford witness.
    image = sp.simplify(U * pauli_word_matrix("XIII") * U.H)
    expansion = []
    for letters in product("IXYZ", repeat=4):
        word = "".join(letters)
        coefficient = sp.simplify(sp.trace(pauli_word_matrix(word) * image) / 16)
        if coefficient:
            expansion.append((str(coefficient), word))
    assert expansion == [("1/2", "XXXY"), ("-1/2", "XXYX"),
                         ("1/2", "XYXX"), ("-1/2", "XYYY")]
    assert sp.simplify(sum((sp.sympify(c) * pauli_word_matrix(w)
                            for c, w in expansion), sp.zeros(16)) - image) == sp.zeros(16)
    return U, expansion


def one_qubit_gate(name):
    return {"H": H2, "S": S2, "SDG": SDG2, "X": X2,
            "Y": Y2, "Z": Z2}[name]


def gate_matrix(gate, nq=4):
    name, a, b = gate
    dim = 1 << nq
    if name in ("H", "S", "SDG", "T", "TDG", "X", "Y", "Z"):
        M = {"T": T2, "TDG": TDG2}[name] if name in ("T", "TDG") else one_qubit_gate(name)
        out = sp.zeros(dim)
        for col in range(dim):
            source = (col >> a) & 1
            for target in (0, 1):
                row = (col & ~(1 << a)) | (target << a)
                out[row, col] = M[target, source]
        return out
    if name == "CNOT":
        out = sp.zeros(dim)
        for col in range(dim):
            row = col ^ ((1 << b) if (col >> a) & 1 else 0)
            out[row, col] = 1
        return out
    if name == "CZ":
        out = sp.eye(dim)
        for state in range(dim):
            if ((state >> a) & 1) and ((state >> b) & 1):
                out[state, state] = -1
        return out
    raise ValueError(gate)


def circuit_unitary(gates):
    U = sp.eye(16)
    for gate in gates:
        U = gate_matrix(gate) * U
    return U


def pauli_tuple_matrix(record, nq=4):
    phase, x, z = record
    out = sp.Integer(1) * sp.eye(1)
    for q in reversed(range(nq)):
        local = I2
        if (x >> q) & 1:
            local = local * X2
        if (z >> q) & 1:
            local = local * Z2
        out = sp.kronecker_product(out, local)
    return sp.simplify((sp.I ** phase) * out)


def check_seed_diagonalizers():
    results = {}
    # Build the complete computational-Z group without relying on the source tableau routine.
    zgroup = set()
    for mask in range(16):
        zgroup.add(sp.ImmutableMatrix(pauli_tuple_matrix((0, 0, mask))))
    for name, item in CERT["seeds"].items():
        target = {sp.ImmutableMatrix(pauli_tuple_matrix(tuple(p)))
                  for p in item["stabilizer_paulis"]}
        C = circuit_unitary([tuple(g) for g in item["preparation_clifford"]])
        D = circuit_unitary([tuple(g) for g in item["measurement_diagonalizer"]])
        assert sp.simplify(D - C.H) == sp.zeros(16)
        mapped = {sp.ImmutableMatrix(sp.simplify(C * M * C.H)) for M in zgroup}
        assert mapped == target
        pulled_back = {sp.ImmutableMatrix(sp.simplify(D * M * D.H)) for M in target}
        assert pulled_back == zgroup
        results[name] = {
            "preparation_gates": item["preparation_clifford"],
            "measurement_gates": item["measurement_diagonalizer"],
            "verified_full_stabilizer_group_order": len(mapped),
        }
    return results


def _even_sign_actions(gammas):
    """Return the 256 exact signed-monomial D+ actions on R^9."""
    identity = FC.zero_matrix(16)
    for i in range(16):
        identity[i][i] = 1
    actions = []
    for mask in range(256):
        axes = [i for i in range(1, 9) if (mask >> (i - 1)) & 1]
        if len(axes) & 1:
            axes = [0] + axes
        matrix = identity
        for axis in axes:
            matrix = FC.matmul(matrix, gammas[axis])
        rows, signs = [], []
        for row in matrix:
            sources = [j for j, value in enumerate(row) if value]
            assert len(sources) == 1
            j = sources[0]
            assert abs(row[j]) == 1
            rows.append(j)
            signs.append(row[j])
        actions.append((rows, signs))
    assert len(actions) == 256
    return actions


def _frame_key(frame):
    a, b, denominator = frame
    return (FC.real_projector_key(a, denominator) if b is None else
            FC.balanced_projector_key(a, b, denominator))


def _orthogonal_frames(first, second):
    a, b, _ = first
    x, y, _ = second
    if b is None:
        return sum(a[i] * x[i] for i in range(16)) == 0
    real = sum(a[i] * x[i] + b[i] * y[i] for i in range(16))
    imag = sum(a[i] * y[i] - b[i] * x[i] for i in range(16))
    return real == 0 and imag == 0


def _permutation_compose(p, q):
    return tuple(p[q[i]] for i in range(9))


def _left_cosets(permutations, subgroup):
    remaining = set(permutations)
    representatives = []
    while remaining:
        representative = min(remaining)
        coset = {_permutation_compose(representative, h) for h in subgroup}
        assert coset <= remaining
        representatives.append(representative)
        remaining.difference_update(coset)
    assert len(representatives) * len(subgroup) == len(permutations)
    return representatives


def check_spin9_basis_partitions_and_channel_data():
    """Rebuild the 9/63/72 PGL(2,8) D+-basis partitions exactly."""
    perms = FC.projective_permutations()
    assert len(perms) == 504
    assert all(FC.permutation_parity(p) == 0 for p in perms)
    pgl_layers = {}
    for k in range(1, 5):
        sizes = FC.subset_orbit_sizes(perms, k)
        assert sizes == [comb(9, k)]
        pgl_layers[str(k)] = sizes

    gammas = FC.gamma_model()
    signs = _even_sign_actions(gammas)
    identity = FC.zero_matrix(16)
    for i in range(16):
        identity[i][i] = 1
    lifts, lifts_by_perm = [], {}
    for p in sorted(perms):
        matrix, denominator = FC.spin_lift_of_permutation(p, gammas, identity)
        lifts.append((p, matrix, denominator))
        lifts_by_perm[p] = (matrix, denominator)

    expected = {"v_R": (None, (1, 0, 0, 14), 9, 144, 56),
                "v_V": (1, (1, 4, 4, 6), 63, 1008, 8),
                "v_H": (8, (0, 1, 7, 7), 72, 1152, 7)}
    summaries = {}
    for label, (y_index, expected_moments, nbases, nrays, horder) in expected.items():
        x0 = [int(i == 0) for i in range(16)]
        y0 = None if y_index is None else [int(i == y_index) for i in range(16)]

        # Independent exact Clifford-monomial moment calculation in JW coordinates.
        psi = circuit_unitary([tuple(g) for g in CERT["seeds"][label]["preparation_clifford"]]) * sp.eye(16)[:, 0]
        jw_gammas = [pauli_word_matrix(word) for word in JW.GAM]
        moments = []
        for k in range(1, 5):
            total = sp.Integer(0)
            for axes in combinations(range(9), k):
                monomial = sp.eye(16)
                for axis in axes:
                    monomial = monomial * jw_gammas[axis]
                value = sp.simplify((psi.H * monomial * psi)[0])
                total += sp.simplify(value * sp.conjugate(value))
            moments.append(int(total))
        assert tuple(moments) == expected_moments
        assert tuple(moments) == tuple(FINITE_CERT["seeds"][label]["moment_vector"])

        full, frames = {}, {}
        sign_basis = set()
        for pi, matrix, denominator in lifts:
            col_a = [matrix[i][0] for i in range(16)]
            col_b = None if y_index is None else [matrix[i][y_index] for i in range(16)]
            for action in signs:
                a = FC.apply_monomial(action, col_a)
                b = None if col_b is None else FC.apply_monomial(action, col_b)
                frame = (a, b, denominator)
                key = _frame_key(frame)
                full[key] = frame
                frames[key] = frame
                if pi == tuple(range(9)):
                    sign_basis.add(key)

        assert len(sign_basis) == 16
        assert len(full) == nrays == nbases * 16
        ray_stabilizer = set()
        for pi, matrix, denominator in lifts:
            col_a = [matrix[i][0] for i in range(16)]
            col_b = None if y_index is None else [matrix[i][y_index] for i in range(16)]
            if _frame_key((col_a, col_b, denominator)) in sign_basis:
                ray_stabilizer.add(pi)
        assert len(ray_stabilizer) == horder
        assert all(_permutation_compose(a, b) in ray_stabilizer
                   for a in ray_stabilizer for b in ray_stabilizer)
        reps = _left_cosets(perms, ray_stabilizer)
        assert len(reps) == nbases

        blocks = []
        for pi in reps:
            matrix, denominator = lifts_by_perm[pi]
            col_a = [matrix[i][0] for i in range(16)]
            col_b = None if y_index is None else [matrix[i][y_index] for i in range(16)]
            block = set()
            for action in signs:
                a = FC.apply_monomial(action, col_a)
                b = None if col_b is None else FC.apply_monomial(action, col_b)
                block.add(_frame_key((a, b, denominator)))
            assert len(block) == 16
            block_frames = [frames[key] for key in block]
            assert all(_orthogonal_frames(block_frames[i], block_frames[j])
                       for i in range(16) for j in range(i + 1, 16))
            for frame in block_frames:
                a, b, den = frame
                norm_numerator = sum(x * x for x in a)
                if b is None:
                    assert norm_numerator == den * den
                else:
                    norm_numerator += sum(x * x for x in b)
                    assert norm_numerator == 2 * den * den
            blocks.append(block)

        union = set().union(*blocks)
        assert union == set(full)
        assert sum(len(block) for block in blocks) == len(union)
        effect_weight = Fraction(1, nbases)
        assert effect_weight == Fraction(16, nrays)
        summaries[label] = {
            "permutation_count": len(perms),
            "Dplus_sign_actions": len(signs),
            "seed_moments_direct": moments,
            "basis_count": nbases,
            "projectors": nrays,
            "basis_coset_stabilizer": horder,
            "disjoint_complete_partition": True,
            "orthonormality_verified_per_basis": True,
            "effect_weight": str(effect_weight),
            "effect_weight_equals_16_over_N": True,
        }
    return {"PGL_subset_orbit_sizes_k1_to_4": pgl_layers,
            "seeds": summaries}


def diagonal_gate(nq, conditions, phase):
    """Return a diagonal matrix with phase on basis strings meeting conditions."""
    out = sp.eye(1 << nq)
    for state in range(1 << nq):
        if all(((state >> q) & 1) == bit for q, bit in conditions):
            out[state, state] = phase
    return out


def ccz_parity_circuit(a, b, c):
    """Exact CCZ from 7 T/T-dagger phases and 10 CNOTs, no ancilla.

    The phase identity is 4abc = a+b+c-(a xor b)-(a xor c)-
    (b xor c)+(a xor b xor c), for bits a,b,c.
    """
    gates = [("T", a, None), ("T", b, None), ("T", c, None)]
    for control, target in ((a, b), (a, c), (b, c)):
        gates.extend([("CNOT", control, target), ("TDG", target, None),
                      ("CNOT", control, target)])
    gates.extend([("CNOT", a, c), ("CNOT", b, c), ("T", c, None),
                  ("CNOT", b, c), ("CNOT", a, c)])
    return gates


def single_on_nq(M, q, nq=4):
    dim = 1 << nq
    out = sp.zeros(dim)
    for col in range(dim):
        source = (col >> q) & 1
        for target in (0, 1):
            row = (col & ~(1 << q)) | (target << q)
            out[row, col] = M[target, source]
    return out


def cnot_nq(control, target, nq=4):
    out = sp.zeros(1 << nq)
    for col in range(1 << nq):
        row = col ^ ((1 << target) if ((col >> control) & 1) else 0)
        out[row, col] = 1
    return out


def check_exact_w_synthesis(U):
    """Verify U=P Q and expand Q's open controls exactly in Clifford+T."""
    # Q's control bits are q1=a, q2=b; q0 is the block target.
    z0 = single_on_nq(Z2, 0)
    z2 = single_on_nq(Z2, 2)
    h0 = single_on_nq(H2, 0)
    sdg0 = single_on_nq(SDG2, 0)
    cz12 = diagonal_gate(4, [(1, 1), (2, 1)], -1)
    cz10 = diagonal_gate(4, [(1, 1), (0, 1)], -1)
    ccz = circuit_unitary(ccz_parity_circuit(1, 2, 0))
    assert sp.simplify(ccz - diagonal_gate(4, [(1, 1), (2, 1), (0, 1)], -1)) == sp.zeros(16)
    neg_ccz_gates = [("X", 1, None), ("X", 2, None)]
    neg_ccz_gates += ccz_parity_circuit(1, 2, 0)
    neg_ccz_gates += [("X", 2, None), ("X", 1, None)]
    qseq = neg_ccz_gates + [
        ("SDG", 0, None), ("H", 0, None), ("CZ", 1, 0),
        ("Z", 0, None), ("CZ", 1, 2), ("Z", 2, None),
    ]
    Q = (-sp.I) * circuit_unitary(qseq)
    ccz_negative = diagonal_gate(4, [(1, 0), (2, 0), (0, 1)], -1)
    Q_reference = (-sp.I) * z2 * cz12 * z0 * cz10 * h0 * sdg0 * ccz_negative
    assert sp.simplify(Q - Q_reference) == sp.zeros(16)

    # The block structure in U has columns (2t,2t+1) and rows (r,15-r).
    # Q acts within (2t,2t+1); P sends them to the row pair.
    Q_from_blocks = sp.zeros(16)
    row_pairs = []
    for t in range(8):
        cols = [2 * t, 2 * t + 1]
        support_rows = [r for r in range(16)
                        if any(exact_w_matrix()[r, c] != 0 for c in cols)]
        assert len(support_rows) == 2
        lo = next(r for r in support_rows if r < 8)
        hi = next(r for r in support_rows if r >= 8)
        assert hi == 15 - lo
        row_pairs.append((lo, hi))
        block = sp.Matrix([[U[lo, cols[0]], U[lo, cols[1]]],
                           [U[hi, cols[0]], U[hi, cols[1]]]])
        for i in range(2):
            for j in range(2):
                Q_from_blocks[2 * t + i, 2 * t + j] = block[i, j]
    assert sp.simplify(Q - Q_from_blocks) == sp.zeros(16)

    def affine_index(x):
        b, a, c, d = ((x >> q) & 1 for q in range(4))
        y = (b ^ a ^ c ^ d, 1 ^ a ^ b, 1 ^ b ^ c, b)
        return sum(y[q] << q for q in range(4))

    P = sp.zeros(16)
    for x in range(16):
        P[affine_index(x), x] = 1
    seq = [("CNOT", 0, 1), ("CNOT", 0, 2), ("CNOT", 1, 3),
           ("CNOT", 2, 3), ("CNOT", 3, 0), ("CNOT", 0, 3),
           ("X", 1, None), ("X", 2, None)]
    P_from_gates = circuit_unitary(seq)
    assert P_from_gates == P
    assert sp.simplify(P * Q - U) == sp.zeros(16)

    # Verify the three distinct one-qubit blocks and their control partition.
    block_signatures = []
    for t in range(8):
        lo, hi = row_pairs[t]
        block_signatures.append(tuple(str(U[r, c]) for r in (lo, hi)
                                       for c in (2 * t, 2 * t + 1)))
    assert block_signatures[0] == block_signatures[4]
    assert block_signatures[1] == block_signatures[3] == block_signatures[5] == block_signatures[7]
    assert block_signatures[2] == block_signatures[6]
    return {
        "basis_pair_row_map": row_pairs,
        "affine_output_bits": ["q0^q1^q2^q3", "1^q0^q1", "1^q0^q2", "q0"],
        "affine_gate_sequence": [list(g) for g in seq],
        "controlled_block_factorization": "(-i Z2 CZ12)(Z0 CZ10) H0 S0^dagger CCZ(controls q1=q2=0,target q0)",
        "negative_control_CCZ_expansion": {
            "control_toggle_sequence": ["X1 X2", "CCZ(q1,q2;q0)", "X2 X1"],
            "CCZ_phase_identity": "4abc=a+b+c-(a xor b)-(a xor c)-(b xor c)+(a xor b xor c)",
            "CCZ_CNOT_count": 10,
            "CCZ_T_count": 7,
            "CCZ_ancillas": 0,
            "CCZ_exact_matrix_verified": True,
        },
        "block_partition": {"q1q2=00": "B0", "q1=1": "B1", "q1q2=01": "B2"},
        "verified_exact_matrix_equality": "P Q = W/sqrt(2)",
        "gate_model_count": {
            "CNOT_with_CZ_decomposed": 18, "T_or_Tdg": 7,
            "X": 6, "H": 5, "Sdg": 1, "Z": 2,
            "global_phase": "-i (irrelevant to the channel)",
            "ancillas": 0,
        },
    }


def parity(permutation):
    return sum(permutation[i] > permutation[j]
               for i in range(len(permutation))
               for j in range(i + 1, len(permutation))) & 1


def fisher_yates_outcomes(m):
    counts = Counter()
    ranges = [range(k) for k in range(m, 1, -1)]
    for choices in product(*ranges):
        p = list(range(m))
        for k, j in zip(range(m, 1, -1), choices):
            p[k - 1], p[j] = p[j], p[k - 1]
        if parity(p):
            # Compose on the left with the fixed transposition (0 1).
            p = [1 if x == 0 else 0 if x == 1 else x for x in p]
        counts[tuple(p)] += 1
    return counts


def check_uniform_sampler():
    out = {}
    for m in (3, 5, 6):
        counts = fisher_yates_outcomes(m)
        # all values in a dict are equal; independently count even permutations
        # to verify support cardinality m!/2.
        assert all(parity(p) == 0 for p in counts)
        expected = 1
        import math
        for k in range(2, m + 1):
            expected *= k
        assert len(counts) == expected // 2
        assert set(counts.values()) == {2}
        out[str(m)] = {"even_permutations": len(counts), "preimages_each": 2}
    m = 9
    bit_cost = sum((Fraction(ceil(log2(k)) * (1 << ceil(log2(k))), k)
                    for k in range(2, m + 1)), Fraction(0))
    out["m=9_expected_fair_bits"] = {"exact": str(bit_cost), "decimal": float(bit_cost)}
    return out


def main():
    U, witness = check_intertwiner_and_clifford_status()
    circuits = check_seed_diagonalizers()
    finite_basis_audit = check_spin9_basis_partitions_and_channel_data()
    synthesis = check_exact_w_synthesis(U)
    sampler = check_uniform_sampler()
    output = {
        "status": "exact internal matrix/tableau and sampler checks passed",
        "intertwiner": {
            "WdagW": "2 I_16", "U=W/sqrt(2)": "unitary and intertwines the two listed Cl_9 models",
            "U_is_JW_Pauli_Clifford": False,
            "exact_nonClifford_witness_U_X0_Udag_Pauli_expansion": witness,
        },
        "seed_readouts": circuits,
        "finite_spin9_basis_and_channel_audit": finite_basis_audit,
        "W_exact_synthesis": synthesis,
        "parity_corrected_sampler": sampler,
        "scope": "Spin(9) finite checks only; all-n result is the algebraic proof in FINAL_REPORT.md",
    }
    out = Path(__file__).with_name("VERIFICATION.json")
    out.write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
