"""Exact ordinary-code counterexample to positive-polar tensor stability.

This does NOT settle quantum-capacity computability.  It certifies why one
specific attempt to apply tensor-polar divergence theorems to ordinary code
cones fails, even for the rational qubit erasure channel with p=1/10.
"""
import itertools
import json
import time
from fractions import Fraction as F
from pathlib import Path

from finite_block import G, ONE, ZERO, identity, is_psd, matmul, trace, zeros


def transpose(a):
    return [[a[j][i].conj() for j in range(len(a))] for i in range(len(a[0]))]


def as_matrix(a):
    return [[G(z) for z in row] for row in a]


def bits(i, n):
    return tuple((i >> (n-1-j)) & 1 for j in range(n))


def integer(bs):
    out = 0
    for bit in bs:
        out = 2*out+bit
    return out


def raw_encoding():
    # V=W/sqrt(2); four orthogonal complement pairs, all of even parity.
    pairs = [(0, 15), (3, 12), (5, 10), (6, 9)]
    W = zeros(16, 4)
    for logical, pair in enumerate(pairs):
        for x in pair:
            W[x][logical] = ONE
    return W


def one_qubit_slice(W, lost, value):
    out = zeros(8, 4)
    for physical in range(16):
        bs = bits(physical, 4)
        if bs[lost] == value:
            remaining = integer(bs[:lost]+bs[lost+1:])
            out[remaining] = W[physical][:]
    return out


def raw_erasure_slice(W, lost_sites, lost_values):
    kept = [i for i in range(4) if i not in lost_sites]
    out = zeros(2**len(kept), 4)
    for physical in range(16):
        bs = bits(physical, 4)
        if tuple(bs[i] for i in lost_sites) == lost_values:
            remaining = integer(tuple(bs[i] for i in kept))
            out[remaining] = W[physical][:]
    return out


def single_site_pauli(site, kind):
    out = zeros(16)
    for i in range(16):
        bs = list(bits(i, 4))
        bit = bs[site]
        if kind == "Z":
            out[i][i] = G(1 if bit == 0 else -1)
        else:
            bs[site] ^= 1
            factor = ONE if kind == "X" else G(0, 1 if bit == 0 else -1)
            out[integer(bs)][i] = factor
    return out


def monogamy_projectors():
    # Ordering R A B, all qubits. P=Phi_RA tensor I_B, Q=Phi_RB tensor I_A.
    P, Q = zeros(8), zeros(8)
    for r, a, b, s, c, d in itertools.product(range(2), repeat=6):
        i, j = 4*r+2*a+b, 4*s+2*c+d
        if r == a and s == c and b == d:
            P[i][j] = G(F(1, 2))
        if r == b and s == d and a == c:
            Q[i][j] = G(F(1, 2))
    assert matmul(P, P) == P and matmul(Q, Q) == Q
    assert matmul(matmul(P, Q), P) == [[z/4 for z in row] for row in P]
    certificate = [[G(F(3, 2) if i == j else 0)-P[i][j]-Q[i][j]
                    for j in range(8)] for i in range(8)]
    assert is_psd(certificate)
    # Tightness is also exact: P+Q has a nonzero vector at eigenvalue 3/2.
    vP = [ZERO]*8
    vP[0] = vP[6] = ONE  # unnormalized Phi_RA tensor |0>_B
    qv = [sum((Q[i][j]*vP[j] for j in range(8)), ZERO) for i in range(8)]
    v = [vP[i]+2*qv[i] for i in range(8)]
    assert any(z != ZERO for z in v)
    assert all(sum(((P[i][j]+Q[i][j])*v[j] for j in range(8)), ZERO)
               == G(F(3, 2))*v[i] for i in range(8))


def conditional_decoded_fidelity(W, erased):
    """Actual chosen decoder fidelity for this erasure-flag branch."""
    if not erased:
        # The inverse encoding decoder is exact on the code subspace.
        assert matmul(transpose(W), W) == [[2*z for z in row] for row in identity(4)]
        return F(1)
    if len(erased) == 1:
        j = erased[0]
        slices = [one_qubit_slice(W, j, x) for x in range(2)]
        # Bob uses Kraus maps W_{j,y}^*: 8-dimensional survivor -> logical 4.
        completeness = zeros(8)
        squared_traces = F(0)
        for y in range(2):
            D = transpose(slices[y])
            dd = matmul(slices[y], D)
            completeness = [[completeness[i][k]+dd[i][k] for k in range(8)] for i in range(8)]
            for x in range(2):
                decoded_raw = matmul(D, slices[x])
                expected = identity(4) if x == y else zeros(4)
                assert decoded_raw == expected
                # Actual encoder slice includes the omitted factor 1/sqrt(2).
                squared_traces += trace(decoded_raw)**2/2
        assert completeness == identity(8)
        return squared_traces/16
    # On every >=2-erasure branch Bob deliberately discards all survivors and
    # prepares logical |0>. Sum squared traces of its composed Kraus maps.
    squared_traces = F(0)
    for values in itertools.product(range(2), repeat=len(erased)):
        L = raw_erasure_slice(W, erased, values)
        for row in L:
            # Decoder Kraus |0><row_index| gives trace=raw amplitude in col 0.
            squared_traces += row[0].abs2()/2
    assert squared_traces == 1
    return squared_traces/16


def sparse_polar_witness(U2):
    # J of a single use: axes (physical input 2, physical output 3).
    J = {(0, 0): F(9, 20), (0, 4): F(9, 20), (4, 0): F(9, 20),
         (4, 4): F(9, 20), (2, 2): F(1, 20), (5, 5): F(1, 20)}
    X = {}
    for ((r0, c0), v0), ((r1, c1), v1) in itertools.product(J.items(), repeat=2):
        a0, b0, j0, d0 = r0//3, r0 % 3, c0//3, c0 % 3
        a1, b1, j1, d1 = r1//3, r1 % 3, c1//3, c1 % 3
        a, b, j, d = 2*a0+a1, 3*b0+b1, 2*j0+j1, 3*d0+d1
        for logical_row, logical_col in itertools.product(range(2), repeat=2):
            row = ((logical_row*4+a)*9+b)*2+logical_row
            col = ((logical_col*4+j)*9+d)*2+logical_col
            X[row, col] = F(4*9, 2)*v0*v1/U2
    assert len(X) == 144
    return X


def sparse_chosen_code_chois(W):
    # Encoding normalized Choi E, axes logical 4 x physical input 16.
    positions = [(l*16+i) for l in range(4) for i in range(16) if W[i][l] == ONE]
    E = {(i, j): F(1, 8) for i, j in itertools.product(positions, repeat=2)}
    # Decoder normalized Choi D, axes physical output 81 x logical 4.
    D = {}

    def add(r, l, s, k, value):
        if value:
            key = (r*4+l, s*4+k)
            D[key] = D.get(key, F(0))+value/81
            if not D[key]:
                del D[key]

    for lost_count in range(5):
        for erased in itertools.combinations(range(4), lost_count):
            kept = [i for i in range(4) if i not in erased]
            indices = []
            for rem in range(2**len(kept)):
                word = [2]*4
                for site, bit in zip(kept, bits(rem, len(kept))):
                    word[site] = bit
                index = 0
                for digit in word:
                    index = 3*index+digit
                indices.append(index)
            if not erased:
                for r, s in itertools.product(range(16), repeat=2):
                    P_rs = sum((W[r][l].re*W[s][l].re for l in range(4)), F(0))/2
                    for l, k in itertools.product(range(4), repeat=2):
                        value = W[r][l].re*W[s][k].re/2
                        if l == k == 0:
                            value += int(r == s)-P_rs
                        add(indices[r], l, indices[s], k, value)
            elif len(erased) == 1:
                slices = [one_qubit_slice(W, erased[0], value) for value in range(2)]
                for r, s, l, k in itertools.product(range(8), range(8), range(4), range(4)):
                    value = sum((L[r][l].re*L[s][k].re for L in slices), F(0))
                    add(indices[r], l, indices[s], k, value)
            else:
                for r in indices:
                    add(r, 0, r, 0, F(1))
    for r, s in itertools.product(range(81), repeat=2):
        assert sum((D.get((r*4+l, s*4+l), F(0)) for l in range(4)), F(0)) == F(int(r == s), 81)
    for r, s in itertools.product(range(4), repeat=2):
        assert sum((E.get((r*16+i, s*16+i), F(0)) for i in range(16)), F(0)) == F(int(r == s), 4)
    return E, D


def split_x_axis(i):
    output_logical, i = i % 2, i//2
    physical_b, i = i % 9, i//9
    physical_a, logical = i % 4, i//4
    return logical, physical_a, physical_b, output_logical


def combined_code_indices(i, j):
    l1, a1, b1, k1 = split_x_axis(i)
    l2, a2, b2, k2 = split_x_axis(j)
    return (2*l1+l2)*16+4*a1+a2, (9*b1+b2)*4+2*k1+k2


def verify_sparse_polar_pairing(X, E, D):
    # This independently evaluates the bilinear Choi objective on the complete
    # chosen four-use encoder/decoder, instead of reusing branch fidelities.
    pairing = F(0)
    for ((r, s), v), ((t, u), w) in itertools.product(X.items(), repeat=2):
        e_row, d_row = combined_code_indices(r, t)
        e_col, d_col = combined_code_indices(s, u)
        pairing += v*w*E.get((e_col, e_row), F(0))*D.get((d_col, d_row), F(0))
    return pairing


def main():
    start = time.monotonic()
    monogamy_projectors()
    W = raw_encoding()
    for site in range(4):
        for kind in ["X", "Y", "Z"]:
            kl = matmul(matmul(transpose(W), single_site_pauli(site, kind)), W)
            assert kl == zeros(4)

    p = F(1, 10)
    U2 = (1-p)**2+p*(1-p)*F(3, 2)+p*p/4
    assert U2 == F(379, 400)
    actual_F4, branch_results = F(0), []
    for lost_count in range(5):
        for erased in itertools.combinations(range(4), lost_count):
            prob = p**lost_count*(1-p)**(4-lost_count)
            fidelity = conditional_decoded_fidelity(W, erased)
            actual_F4 += prob*fidelity
            branch_results.append({"erased_sites": list(erased), "probability": str(prob),
                                   "decoded_entanglement_fidelity": str(fidelity)})
    assert actual_F4 == F(30431, 32000) == F(152155, 160000)
    assert actual_F4 > U2**2
    U_poly = [F(1), F(-1, 2), F(-1, 4)]
    U_squared = [sum((U_poly[i]*U_poly[k-i] for i in range(3) if 0 <= k-i < 3), F(0))
                 for k in range(5)]
    F4_poly = [F(1), F(0), F(-45, 8), F(15, 2), F(-45, 16)]
    delta_poly = [x-y for x, y in zip(F4_poly, U_squared)]
    assert delta_poly == [F(0), F(1), F(-43, 8), F(29, 4), F(-23, 8)]
    # Delta=p(1-p)(23p^2-35p+8)/8; the quadratic decreases to 11/16
    # on [0,1/4], so the strict inequality holds throughout (0,1/4].
    assert 23*F(1, 4)**2-35*F(1, 4)+8 == F(11, 16)
    X = sparse_polar_witness(U2)
    E, D = sparse_chosen_code_chois(W)
    pairing = verify_sparse_polar_pairing(X, E, D)
    assert pairing == actual_F4/(U2**2)
    witness = {
        "X_dimension": 144,
        "X_axis_dimensions": [2, 4, 9, 2],
        "X_axis_order": ["logical_input", "physical_input_two_uses", "physical_output_two_uses", "logical_output"],
        "X_sparse_entries": [[r, s, str(v)] for (r, s), v in sorted(X.items())],
        "tensor_square_combined_axis_dimensions": [4, 16, 81, 4],
        "tensor_square_axis_permutation": [0, 4, 1, 5, 2, 6, 3, 7],
        "four_use_encoder_choi_dimension": 64,
        "four_use_encoder_sparse_entries": [[r, s, str(v)] for (r, s), v in sorted(E.items())],
        "four_use_decoder_choi_dimension": 324,
        "four_use_decoder_sparse_entries": [[r, s, str(v)] for (r, s), v in sorted(D.items())],
        "exact_Choi_objective_pairing": str(pairing),
        "scope": "X is in the positive polar by the analytic two-use upper bound; X tensor X violates the four-use positive polar by this explicit code",
    }
    (Path(__file__).resolve().parent/"POLAR_WITNESS.json").write_text(json.dumps(witness, indent=2)+"\n")
    result = {
        "status": "exact_quantum_counterexample_passed",
        "scope": "positive-polar tensor closure for ordinary encoder-decoder code sets fails",
        "ordinary_capacity_computability": "UNRESOLVED",
        "channel": "qubit erasure, p=1/10; normalized Choi rational, 6 by 6",
        "two_use_logical_dimension": 2,
        "two_use_optimal_fidelity_upper_bound": str(U2),
        "product_upper_bound": str(U2**2),
        "four_use_logical_dimension": 4,
        "four_use_constructed_fidelity": str(actual_F4),
        "strict_gap": str(actual_F4-U2**2),
        "general_strict_gap_formula": "p(1-p)(23p^2-35p+8)/8",
        "proved_parameter_interval": "0 < p <= 1/4",
        "polar_tensor_violation_factor_lower_bound": str(actual_F4/(U2**2)),
        "independent_sparse_Choi_pairing": str(pairing),
        "sparse_X_entries": len(X),
        "sparse_encoder_entries": len(E),
        "sparse_decoder_entries": len(D),
        "erasure_pattern_branches": branch_results,
        "encoder_orthogonality": "exact_pass",
        "KL_single_site_Paulis": 12,
        "decoded_good_branches": "all 0 or 1 erasure branches exactly identity",
        "monogamy_projector_norm": "exactly 3/2, exact PSD and eigenvector certificates",
        "largest_dense_matrix_dimension_executed": 16,
        "larger_polar_witness": "factored expression only; 144 dimensional X, tensor square 20736",
        "elapsed_seconds": time.monotonic()-start,
    }
    (Path(__file__).resolve().parent/"POLAR_RESULTS.json").write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({k:v for k,v in result.items() if k != "erasure_pattern_branches"}, indent=2))


if __name__ == "__main__":
    main()
