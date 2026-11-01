"""Deterministic Pauli-stabilizer extraction from an exact open-boundary MPS.

All tensor entries are Gaussian integers. Gaussian rational tensors are reduced
to this case by clearing one common denominator per site, a harmless global
nonzero scaling. No sampling, truncation, canonicalization or zero tolerance.
The algorithm expands the GF(2) span of the NONZERO Pauli coefficients, rather
than pruning prefixes of the unknown stabilizers. Exact arithmetic is essential.
"""
from dataclasses import dataclass
import numpy as np


@dataclass
class ZMatrix:
    re: np.ndarray
    im: np.ndarray

    @staticmethod
    def make(re, im=None):
        a = np.array(re, dtype=object)
        assert a.ndim == 2
        b = np.zeros(a.shape, dtype=object) if im is None else np.array(im, dtype=object)
        assert a.shape == b.shape
        assert all(isinstance(x, (int, np.integer)) for x in a.flat)
        assert all(isinstance(x, (int, np.integer)) for x in b.flat)
        return ZMatrix(a, b)

    @staticmethod
    def zero(rows, cols):
        return ZMatrix.make(np.zeros((rows, cols), dtype=object))

    def __add__(self, other):
        return ZMatrix(self.re + other.re, self.im + other.im)

    def __sub__(self, other):
        return ZMatrix(self.re - other.re, self.im - other.im)

    def __matmul__(self, other):
        return ZMatrix(self.re @ other.re - self.im @ other.im,
                       self.re @ other.im + self.im @ other.re)

    def adjoint(self):
        return ZMatrix(self.re.T, -self.im.T)

    def conjugate(self):
        return ZMatrix(self.re, -self.im)

    def times_i(self):
        return ZMatrix(-self.im, self.re)

    def scalar(self):
        assert self.re.shape == (1, 1)
        return int(self.re[0, 0]), int(self.im[0, 0])

    def kron(self, other):
        return ZMatrix(np.kron(self.re, other.re) - np.kron(self.im, other.im),
                       np.kron(self.re, other.im) + np.kron(self.im, other.re))


# Interleaved binary labels (x_0,z_0,x_1,z_1,...); local I,X,Y,Z.
PAULI_BITS = (0, 1, 3, 2)
PAULI_NAMES = "IXYZ"


def nullspace(rows, width):
    """Basis of the ordinary dot-product annihilator over GF(2)."""
    a = list(dict.fromkeys(int(v) for v in rows if v))
    pivots = []
    head = 0
    for col in range(width):
        k = next((j for j in range(head, len(a)) if (a[j] >> col) & 1), None)
        if k is None:
            continue
        a[head], a[k] = a[k], a[head]
        for j in range(len(a)):
            if j != head and ((a[j] >> col) & 1):
                a[j] ^= a[head]
        pivots.append(col)
        head += 1
    basis = []
    for col in range(width):
        if col in pivots:
            continue
        v = 1 << col
        for row, pivot in zip(a[:head], pivots):
            if (row >> col) & 1:
                v |= 1 << pivot
        assert all((v & row).bit_count() % 2 == 0 for row in rows)
        basis.append(v)
    return basis


def independent(rows, v):
    return any((u & v).bit_count() % 2 for u in nullspace(rows, max([1, v.bit_length()] + [x.bit_length() for x in rows])))


def symplectic_swap(v, n):
    out = 0
    for i in range(n):
        x, z = (v >> (2*i)) & 1, (v >> (2*i+1)) & 1
        out |= z << (2*i)
        out |= x << (2*i+1)
    return out


def pauli_name(v, n):
    return "".join(PAULI_NAMES[PAULI_BITS.index((v >> (2*i)) & 3)] for i in range(n))


class ExactPauliMPS:
    def __init__(self, tensors):
        self.n = len(tensors)
        assert self.n >= 1 and tensors[0][0].re.shape[0] == 1
        assert tensors[-1][0].re.shape[1] == 1
        for i, (a0, a1) in enumerate(tensors):
            assert a0.re.shape == a1.re.shape
            if i:
                assert tensors[i-1][0].re.shape[1] == a0.re.shape[0]
        self.b = []
        for a0, a1 in tensors:
            c00 = a0.conjugate().kron(a0)
            c01 = a0.conjugate().kron(a1)
            c10 = a1.conjugate().kron(a0)
            c11 = a1.conjugate().kron(a1)
            self.b.append((c00+c11, c01+c10, (c10-c01).times_i(), c00-c11))
        self.query_count = 0
        self.max_energy_bits = 0
        self.norm = self.coefficient(0)
        assert self.norm > 0, "The input MPS must be nonzero."

    def coefficient(self, label):
        row = ZMatrix.make([[1]])
        for i, bs in enumerate(self.b):
            row = row @ bs[PAULI_BITS.index((label >> (2*i)) & 3)]
        a, b = row.scalar()
        assert b == 0, "A Hermitian Pauli expectation is real."
        return a

    def suffix_environments(self, linear_form):
        """Exact squared-coefficient energy for one parity and any prefix.

        R[i][p] sums B_i...B_n B_n^dagger...B_i^dagger over suffix
        words of parity p. This is a width-two parity automaton on an MPS
        of bond at most D^2, with no intermediate bond growth.
        """
        self.query_count += 1
        r = [None] * (self.n+1)
        r[self.n] = (ZMatrix.make([[1]]), ZMatrix.make([[0]]))
        for i in reversed(range(self.n)):
            dim = self.b[i][0].re.shape[0]
            pair = [ZMatrix.zero(dim, dim), ZMatrix.zero(dim, dim)]
            u = (linear_form >> (2*i)) & 3
            for code, b in zip(PAULI_BITS, self.b[i]):
                parity = (u & code).bit_count() % 2
                for p in (0, 1):
                    pair[p] = pair[p] + b @ r[i+1][p ^ parity] @ b.adjoint()
            r[i] = tuple(pair)
        a, b = r[0][1].scalar()
        assert b == 0 and a >= 0
        self.max_energy_bits = max(self.max_energy_bits, a.bit_length())
        return r

    def outside_hyperplane(self, linear_form):
        r = self.suffix_environments(linear_form)
        energy, imag = r[0][1].scalar()
        assert imag == 0
        if energy == 0:
            return None
        row = ZMatrix.make([[1]])
        parity = 0
        label = 0
        for i, bs in enumerate(self.b):
            u = (linear_form >> (2*i)) & 3
            for code, b in zip(PAULI_BITS, bs):
                next_row = row @ b
                next_parity = parity ^ ((u & code).bit_count() % 2)
                val, imag = (next_row @ r[i+1][1 ^ next_parity] @ next_row.adjoint()).scalar()
                assert imag == 0 and val >= 0
                if val:
                    row, parity = next_row, next_parity
                    label |= code << (2*i)
                    break
            else:
                raise AssertionError("Positive prefix energy lost all children.")
        coefficient, imag = row.scalar()
        assert imag == 0 and coefficient != 0 and parity == 1
        assert (linear_form & label).bit_count() % 2 == 1
        return label, coefficient, energy

    def extract(self):
        support_basis = []
        witnesses = []
        while True:
            normals = nullspace(support_basis, 2*self.n)
            for u in normals:
                found = self.outside_hyperplane(u)
                if found is None:
                    continue
                v, coefficient, energy = found
                assert independent(support_basis, v)
                support_basis.append(v)
                witnesses.append({"linear_form": u, "support_label": v,
                                  "coefficient_bits": abs(coefficient).bit_length(),
                                  "parity_energy_bits": energy.bit_length()})
                break
            else:
                break
        generators = []
        for u in normals:
            v = symplectic_swap(u, self.n)
            coefficient = self.coefficient(v)
            assert abs(coefficient) == self.norm
            generators.append({"label": v, "pauli": pauli_name(v, self.n),
                               "sign": 1 if coefficient > 0 else -1})
        for g in generators:
            for h in generators:
                assert (symplectic_swap(g["label"], self.n) & h["label"]).bit_count() % 2 == 0
        assert len(generators) <= self.n
        return {"qubits": self.n, "stabilizer_dimension": len(generators),
                "stabilizer_nullity": self.n-len(generators), "generators": generators,
                "support_span_dimension": len(support_basis), "support_basis": support_basis,
                "support_witnesses": witnesses, "parity_contractions": self.query_count,
                "largest_root_energy_bit_length": self.max_energy_bits}


def ghz_phase(n, left=(5, 0), right=(3, 4)):
    assert n >= 2
    tensors = [(ZMatrix.make([[left[0], 0]], [[left[1], 0]]),
                ZMatrix.make([[0, right[0]]], [[0, right[1]]]))]
    for _ in range(n-2):
        tensors.append((ZMatrix.make([[1, 0], [0, 0]]), ZMatrix.make([[0, 0], [0, 1]])))
    tensors.append((ZMatrix.make([[1], [0]]), ZMatrix.make([[0], [1]])))
    return tensors


def paper_algorithm6(mps, schmidt_ranks):
    """Literal intended prefix heuristic with implicit identity and stable ties.

    Liu--Clark Appendix F Algorithm 6, local order I,X,Y,Z. Empty G is
    interpreted as including the identity prefix, otherwise its first loop
    has no candidates at all. No claim about an unavailable implementation.
    """
    suffix = mps.suffix_environments(0)
    denom = (1 << mps.n)*mps.norm**2
    generators = []
    traces = []
    for k in range(1, mps.n+1):
        candidates = []
        seen = set()
        for prefix in [0] + generators:
            for code in PAULI_BITS:
                v = prefix | (code << (2*(k-1)))
                if v in seen:
                    continue
                seen.add(v)
                row = ZMatrix.make([[1]])
                for i in range(k):
                    row = row @ mps.b[i][PAULI_BITS.index((v >> (2*i)) & 3)]
                energy, imag = (row @ suffix[k][0] @ row.adjoint()).scalar()
                assert imag == 0
                if energy*(1 << k)*schmidt_ranks[k-1] >= denom:
                    candidates.append((v, energy))
        candidates.sort(key=lambda t: -t[1])
        generators = []
        for v, _ in candidates:
            if independent(generators, v):
                generators.append(v)
        traces.append({"prefix_qubits": k, "retained": [pauli_name(v, k) for v in generators]})
    return {"dimension": len(generators), "generators": [pauli_name(v, mps.n) for v in generators],
            "trace": traces, "tie_order": "I,X,Y,Z; stable descending exact probability"}
