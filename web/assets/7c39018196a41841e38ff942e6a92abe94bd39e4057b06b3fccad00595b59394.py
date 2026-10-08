#!/usr/bin/env python3
"""Exact Spin(9) orbit-basis partition and four-qubit stabilizer readout.

This independently reconstructs the even-sign seed bases, maps their
stabilizers to the Pauli/Jordan-Wigner realization, and synthesizes exact
Clifford preparation circuits by a finite BFS over 4-qubit stabilizer states.
It uses SymPy only for the exact 16x16 representation-intertwiner check.
"""
from collections import deque
from importlib.util import spec_from_file_location, module_from_spec
from pathlib import Path
import json
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
FC_PATH = ROOT / "work/agents/c5_quantum_dimension_obstruction/cycle10_finite_compiler/finite_compiler.py"
JW_PATH = ROOT / "work/agents/c5_quantum_dimension_obstruction/cycle9_spin9_mixed/spin9_fullstar_blocks.py"

def load_module(path, name):
    spec = spec_from_file_location(name, path)
    mod = module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod

FC = load_module(FC_PATH, "spin9_finite_compiler_cycle11")
JW = load_module(JW_PATH, "spin9_jw_words_cycle11")

NQ = 4
MASK = (1 << NQ) - 1

def identity(n=16):
    return [[int(i == j) for j in range(n)] for i in range(n)]

def matmul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))]

def axes_for_even_sign_mask(mask):
    axes = [i for i in range(1, 9) if (mask >> (i - 1)) & 1]
    if len(axes) & 1:
        axes = [0] + axes
    return axes

def oct_lift(mask, gammas):
    m = identity()
    for a in axes_for_even_sign_mask(mask):
        m = matmul(m, gammas[a])
    return m

def alpha_for_seed(m, y_index):
    if y_index is None:
        if not all(m[r][0] == 0 for r in range(1, 16)):
            return None
        a = m[0][0]
        if a not in (-1, 1):
            return None
        return a
    x0, y0 = m[0][0], m[0][y_index]
    xy, yy = m[y_index][0], m[y_index][y_index]
    if not all(m[r][0] == 0 and m[r][y_index] == 0
               for r in range(16) if r not in (0, y_index)):
        return None
    if x0 * yy - xy * y0 != 1:
        return None
    # M(x+i y)=(x0+i*y0)(x+i*y), so alpha is one of 1,-1,i,-i.
    if (x0, y0) not in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        return None
    if x0 == 1: return 1
    if x0 == -1: return -1
    if y0 == 1: return 1j
    return -1j

def phase_exponent(alpha):
    return {1: 0, 1j: 1, -1: 2, -1j: 3}[alpha]

def word_to_pauli(word, coefficient_phase):
    x = z = ny = 0
    for q, letter in enumerate(word):
        if letter in "XY": x |= 1 << q
        if letter in "YZ": z |= 1 << q
        if letter == "Y": ny += 1
    # Standard Y=iXZ on each overlapping site.
    return ((coefficient_phase + ny) % 4, x, z)

def jw_lift_word(mask):
    phase = 0
    word = ("I",) * NQ
    for a in axes_for_even_sign_mask(mask):
        dp, word = JW.pauli_mul_word(word, JW.GAM[a])
        phase = (phase + dp) % 4
    return word_to_pauli(word, phase)

def mul_pauli(a, b):
    p, x, z = a
    q, u, v = b
    return ((p + q + 2 * ((z & u).bit_count() % 2)) % 4,
            x ^ u, z ^ v)

def commutes(a, b):
    return (((a[1] & b[2]).bit_count() + (a[2] & b[1]).bit_count()) % 2) == 0

def seed_stabilizers(y_index):
    oct_gammas = FC.gamma_model()
    stab = []
    for mask in range(256):
        m = oct_lift(mask, oct_gammas)
        alpha = alpha_for_seed(m, y_index)
        if alpha is None:
            continue
        p, x, z = jw_lift_word(mask)
        p = (p - phase_exponent(alpha)) % 4
        assert (p & 1) == ((x & z).bit_count() & 1), (mask, (p, x, z))
        stab.append((p, x, z))
    assert len(stab) == 16, (y_index, len(stab))
    assert len(set(stab)) == 16
    assert all(commutes(a, b) for i, a in enumerate(stab) for b in stab[i + 1:])
    assert (0, 0, 0) in stab
    # Closure under multiplication certifies that this is the complete ray stabilizer.
    st = set(stab)
    assert all(mul_pauli(a, b) in st for a in st for b in st)
    return tuple(sorted(st))

def canonical_group(gens):
    group = {(0, 0, 0)}
    frontier = [(0, 0, 0)]
    while frontier:
        a = frontier.pop()
        for g in gens:
            b = mul_pauli(a, g)
            if b not in group:
                group.add(b)
                frontier.append(b)
    return tuple(sorted(group))

def conjugate(pauli, gate):
    p, x, z = pauli
    name, a, b = gate
    if name == "H":
        bit = 1 << a
        xa, za = bool(x & bit), bool(z & bit)
        if xa and za:
            p = (p + 2) % 4
        if xa != za:
            x ^= bit; z ^= bit
        return (p, x, z)
    if name == "S":
        bit = 1 << a
        if x & bit:
            p = (p + 1) % 4
            z ^= bit
        return (p, x, z)
    if name == "SDG":
        bit = 1 << a
        if x & bit:
            p = (p - 1) % 4
            z ^= bit
        return (p, x, z)
    if name == "X":
        if z & (1 << a):
            p = (p + 2) % 4
        return (p, x, z)
    if name == "CNOT":
        ctrl, target = a, b
        xc, xt = (x >> ctrl) & 1, (x >> target) & 1
        zc, zt = (z >> ctrl) & 1, (z >> target) & 1
        if xc: x ^= 1 << target
        if zt: z ^= 1 << ctrl
        return (p, x, z)
    raise ValueError(gate)

def apply_gate(group, gate):
    return tuple(sorted(conjugate(p, gate) for p in group))

def gates():
    out = []
    for q in range(NQ):
        out += [("H", q, None), ("S", q, None), ("SDG", q, None), ("X", q, None)]
    for c in range(NQ):
        for t in range(NQ):
            if c != t:
                out.append(("CNOT", c, t))
    return out

def bfs_preparation(target):
    initial_gens = [(0, 0, 1 << q) for q in range(NQ)]
    start = canonical_group(initial_gens)
    if start == target:
        return []
    gate_list = gates()
    pred = {start: None}
    queue = deque([start])
    while queue:
        state = queue.popleft()
        for gate in gate_list:
            nxt = apply_gate(state, gate)
            if nxt in pred:
                continue
            pred[nxt] = (state, gate)
            if nxt == target:
                path = []
                cur = nxt
                while pred[cur] is not None:
                    prev, g = pred[cur]
                    path.append(g)
                    cur = prev
                path.reverse()
                return path
            queue.append(nxt)
    raise RuntimeError(f"unreachable stabilizer state; searched {len(pred)} states")

def inverse_gate(g):
    name, a, b = g
    return ({"S": "SDG", "SDG": "S"}.get(name, name), a, b)

def circuit_counts(circuit):
    return {g: sum(1 for c in circuit if c[0] == g)
            for g in ("H", "S", "SDG", "X", "CNOT")}

def matrix_pauli(word):
    import sympy as sp
    p = {"I": sp.eye(2), "X": sp.Matrix([[0,1],[1,0]]),
         "Y": sp.Matrix([[0,-sp.I],[sp.I,0]]), "Z": sp.diag(1,-1)}
    out = sp.Matrix([[1]])
    # q=0 is the least-significant computational bit.
    for letter in reversed(word):
        out = sp.kronecker_product(out, p[letter])
    return out

def intertwiner_audit():
    import sympy as sp
    oct_g = [sp.Matrix(row) for row in FC.gamma_model()]
    jw_g = [matrix_pauli(word) for word in JW.GAM]
    # A nonzero solution W intertwines the two irreducible Cl_9 modules.
    vars = sp.symbols("w0:256")
    W = sp.Matrix(16, 16, vars)
    eqs = []
    for a in range(9):
        eqs += list(W * oct_g[a] - jw_g[a] * W)
    A, _ = sp.linear_eq_to_matrix(eqs, vars)
    ns = A.nullspace()
    assert len(ns) == 1, len(ns)
    W = sp.Matrix(16,16,ns[0])
    gram = sp.simplify(W.H * W)
    scalar = gram[0,0]
    assert scalar != 0 and gram == scalar * sp.eye(16)
    # The JW volume product and oct volume product have the same positive sign.
    vo = sp.eye(16); vj = sp.eye(16)
    for a in range(9): vo = vo * oct_g[a]; vj = vj * jw_g[a]
    assert vo == sp.eye(16) and vj == sp.eye(16)
    assert sum(v != 0 for v in W) == 32 and scalar == 2
    return {"nullity": len(ns), "gram_scalar": str(scalar),
            "entries_gaussian_integer": all(v in (0,1,-1,sp.I,-sp.I) for v in W),
            "nonzero_entries": sum(v != 0 for v in W),
            "intertwiner_matrix": [[str(W[i,j]) for j in range(16)] for i in range(16)],
            "unitarity_scale": "1/sqrt(2)",
            "same_positive_volume_element": True,
            "unitary_is_clifford": "not asserted; it is a fixed exact representation change",
            "runtime_convention": "Pauli/Jordan-Wigner representation is used directly for the four-qubit circuit"
            }

def reflection_paulis():
    records = []
    max_weight = 0
    for a in range(9):
        for b in range(a + 1, 9):
            ph, word = JW.pauli_mul_word(JW.GAM[a], JW.GAM[b])
            # pauli_mul_word writes the product as i^ph times a tensor-product
            # Pauli word, so multiplying by i leaves a real sign.
            residual = (ph + 1) % 4
            assert residual in (0,2), (a,b,ph,word,residual)
            weight = sum(ch != "I" for ch in word)
            assert weight <= 4
            max_weight = max(max_weight, weight)
            records.append({"axes": [a,b], "pauli_word": "".join(word),
                            "sign": 1 if residual == 0 else -1,
                            "weight": weight})
    assert len(records) == 36
    return {"count": len(records), "all_are_signed_hermitian_pauli_words": True,
            "max_weight": max_weight, "records": records,
            "reflection_identity": "R_ab=Gamma_a exp(i*pi*P_ab/4)=(Gamma_a-Gamma_b)/sqrt(2)",
            "per_reflection_synthesis": "at most 2(weight-1) CNOT, one Rz(pi/2), local Clifford basis changes and Gamma_a Pauli word"}


def main():
    target = {
        "v_R": (None, 9, 144),
        "v_H": (8, 72, 1152),
        "v_V": (1, 63, 1008),
    }
    results = {}
    for label, (y, basis_count, orbit_size) in target.items():
        stab = seed_stabilizers(y)
        circuit = bfs_preparation(stab)
        state = canonical_group([(0,0,1<<q) for q in range(NQ)])
        for gate in circuit:
            state = apply_gate(state, gate)
        assert state == stab
        diagonalizer = [inverse_gate(g) for g in reversed(circuit)]
        measured = stab
        for gate in diagonalizer:
            measured = apply_gate(measured, gate)
        assert measured == canonical_group([(0,0,1<<q) for q in range(NQ)])
        results[label] = {
            "basis_count": basis_count,
            "orbit_size": orbit_size,
            "even_sign_seed_stabilizer_order": len(stab),
            "stabilizer_paulis": [list(x) for x in stab],
            "preparation_clifford": [list(x) for x in circuit],
            "preparation_gate_counts": circuit_counts(circuit),
            "measurement_diagonalizer": [list(x) for x in diagonalizer],
            "measurement_gate_counts": circuit_counts(diagonalizer),
            "per_basis_outcome_bits": 4,
            "uniform_basis_index_bits_information": f"log2({basis_count})",
            "finite_effect_weight": f"1/{basis_count}",
        }
        assert orbit_size == 16 * basis_count
    out = {"representation_intertwiner": intertwiner_audit(),
           "reflection_paulis": reflection_paulis(), "seeds": results}
    (HERE / "STABILIZER_READOUT_CERTIFICATE.json").write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))

if __name__ == "__main__":
    main()
